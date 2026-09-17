"""Extract Atlan lineage for Redshift landing tables, load to Snowflake.

Two-phase approach:
  1. get_lineage() per landing table -- returns graph edges (relations) and bare GUIDs
  2. bulk_enrich_guids() -- batch-resolves GUIDs to names/schemas via index search

Handles slow API with rate limiting, timeouts, and progress logging.
"""

from __future__ import annotations

import json
import logging
import time

import snowflake.connector
from prefect import task

from lib import atlan
from pipelines.tasks.snowflake_loader import load_to_snowflake

logger = logging.getLogger(__name__)

RAW_LINEAGE_TABLE = "gold_dev.data_platform.raw_atlan_lineage"

CREATE_LINEAGE_SQL = f"""\
CREATE TABLE IF NOT EXISTS {RAW_LINEAGE_TABLE} (
    raw_data VARIANT,
    _row_hash VARCHAR,
    _extracted_at TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file VARCHAR DEFAULT 'atlan_lineage'
);
"""

PROCESS_TYPES = {"DbtProcess", "Process", "BIProcess"}

RELATIONAL_TYPES = {
    "Table", "View", "MaterialisedView", "DbtModel", "DbtSource",
    "QuickSightDataset",
}

LANDING_TABLES_QUERY = """\
SELECT schema_name, object_name, object_type, load_mechanism
FROM gold_dev.data_platform.redshift_orphan_inventory
WHERE is_landing_table = TRUE
  AND classification != 'orphan'
ORDER BY consumer_queries DESC
"""


def _get_snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    return snowflake.connector.connect(
        account="KEAZVSO-BUSINESS_TECH_PROD",
        user="dean.mccall@workiva.com",
        authenticator="externalbrowser",
        database="gold_dev",
        schema="data_platform",
        warehouse="PROD_WH",
    )


def _fetch_landing_tables(limit: int | None = None) -> list[dict]:
    conn = _get_snowflake_connection()
    try:
        cur = conn.cursor()
        cur.execute(LANDING_TABLES_QUERY)
        cols = [d[0].lower() for d in cur.description]
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        if limit:
            rows = rows[:limit]
        return rows
    finally:
        conn.close()


@task(name="extract_atlan_lineage", retries=0, log_prints=True, timeout_seconds=7200)
def extract_atlan_lineage(limit: int | None = None, test_tables: list[str] | None = None) -> int:
    """Extract downstream lineage for Redshift landing tables and load to Snowflake.

    Args:
        limit: Max number of tables to process from the inventory query.
        test_tables: Override list of 'schema.name' strings to extract instead of querying inventory.
    """
    # Ensure raw table exists even if no data is loaded (prevents dbt source errors)
    from pipelines.tasks.snowflake_loader import get_snowflake_connection
    conn = get_snowflake_connection()
    try:
        conn.cursor().execute(CREATE_LINEAGE_SQL)
    finally:
        conn.close()

    if test_tables:
        tables = []
        for t in test_tables:
            schema, name = t.split(".", 1)
            tables.append({"schema_name": schema, "object_name": name})
        print(f"[Atlan Lineage] Using {len(tables)} test table(s): {test_tables}")
    else:
        print("[Atlan Lineage] Fetching active landing tables from Snowflake...")
        tables = _fetch_landing_tables(limit)
    print(f"[Atlan Lineage] {len(tables)} landing tables to process")

    if not tables:
        print("[Atlan Lineage] No tables to process")
        return 0

    # Phase 1: Resolve object names to Atlan GUIDs (batched)
    print("[Atlan Lineage] Resolving Atlan GUIDs...")
    guid_map = atlan.bulk_resolve_guids(
        [{"schema_name": t["schema_name"], "object_name": t["object_name"]} for t in tables],
        connector="redshift",
    )
    resolved = sum(1 for t in tables if f"{t['schema_name']}.{t['object_name']}" in guid_map)
    print(f"[Atlan Lineage] Resolved {resolved}/{len(tables)} GUIDs")

    # Phase 2: Get lineage for each resolved table
    all_edges: list[dict] = []
    all_guids: set[str] = set()
    errors = 0
    skipped = 0
    pipeline_start = time.time()

    for i, table in enumerate(tables):
        key = f"{table['schema_name']}.{table['object_name']}"
        guid = guid_map.get(key)
        if not guid:
            skipped += 1
            continue

        try:
            start = time.time()
            relations, entity_map = atlan.get_lineage(guid)
            elapsed = time.time() - start

            # Build adjacency and hop over non-relational nodes (process, visual, column)
            # Atlan lineage: Table -> DbtProcess -> DbtModel, so we collapse process hops
            entity_types = {g: e.get("typeName") for g, e in entity_map.items()}

            # Build forward adjacency
            children: dict[str, list[str]] = {}
            for rel in relations:
                children.setdefault(rel["fromEntityId"], []).append(rel["toEntityId"])

            # For each relational source, BFS through non-relational nodes to find relational targets
            relational_guids_local = {g for g, t in entity_types.items() if t in RELATIONAL_TYPES}
            for src_guid_local in relational_guids_local:
                all_guids.add(src_guid_local)
                # BFS to find reachable relational nodes
                queue = list(children.get(src_guid_local, []))
                visited = {src_guid_local}
                while queue:
                    node = queue.pop(0)
                    if node in visited:
                        continue
                    visited.add(node)
                    if node in relational_guids_local:
                        all_guids.add(node)
                        all_edges.append({
                            "_src_guid": src_guid_local,
                            "_tgt_guid": node,
                            "_root_guid": guid,
                            "_root_name": table["object_name"],
                            "_root_schema": table["schema_name"],
                        })
                    else:
                        # Non-relational node: hop through it
                        queue.extend(children.get(node, []))

            if (i + 1) % 10 == 0 or elapsed > 10:
                total_elapsed = time.time() - pipeline_start
                print(
                    f"[Atlan Lineage] {i + 1}/{len(tables)} | "
                    f"{key}: {len(relations)} relations in {elapsed:.1f}s | "
                    f"Total edges: {len(all_edges)} | Elapsed: {total_elapsed:.0f}s"
                )

        except Exception as exc:
            errors += 1
            print(f"[Atlan Lineage] ERROR {key}: {exc}")

        time.sleep(0.5)  # rate limit

    print(f"[Atlan Lineage] Lineage fetched: {len(all_edges)} raw edges, {len(all_guids)} unique GUIDs, {errors} errors, {skipped} skipped")

    if not all_edges:
        print("[Atlan Lineage] No lineage data to load")
        return 0

    # Phase 3: Enrich all GUIDs with attributes
    print(f"[Atlan Lineage] Enriching {len(all_guids)} GUIDs...")
    enriched = atlan.bulk_enrich_guids(list(all_guids))
    print(f"[Atlan Lineage] Enriched {len(enriched)}/{len(all_guids)} GUIDs")

    # Phase 4: Flatten to edge records
    flat_edges: list[dict] = []
    for raw in all_edges:
        src_guid = raw["_src_guid"]
        tgt_guid = raw["_tgt_guid"]
        src = enriched.get(src_guid, {})
        tgt = enriched.get(tgt_guid, {})

        flat_edges.append({
            "source_guid": src_guid,
            "target_guid": tgt_guid,
            "source_name": src.get("name"),
            "target_name": tgt.get("name"),
            "source_schema": src.get("schemaName"),
            "target_schema": tgt.get("schemaName"),
            "source_type": src.get("typeName"),
            "target_type": tgt.get("typeName"),
            "source_connector": src.get("connectorName"),
            "target_connector": tgt.get("connectorName"),
            "source_qualified_name": src.get("qualifiedName"),
            "target_qualified_name": tgt.get("qualifiedName"),
            "root_guid": raw["_root_guid"],
            "root_name": raw["_root_name"],
            "root_schema": raw["_root_schema"],
        })

    print(f"[Atlan Lineage] {len(flat_edges)} relational edges")

    # Phase 5: Load to Snowflake
    json_strings = [json.dumps(edge, default=str) for edge in flat_edges]
    loaded = load_to_snowflake(json_strings, RAW_LINEAGE_TABLE, CREATE_LINEAGE_SQL)
    print(f"[Atlan Lineage] Loaded {loaded} edges to {RAW_LINEAGE_TABLE}")
    return loaded
