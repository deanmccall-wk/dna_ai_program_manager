"""Extract Redshift stl_scan and object inventory, load to Snowflake."""

from __future__ import annotations

import json
import logging
from datetime import date

from prefect import task

from lib import redshift
from pipelines.tasks.snowflake_loader import load_to_snowflake

logger = logging.getLogger(__name__)

RAW_SCANS_TABLE = "gold_dev.data_platform.raw_redshift_scans"
RAW_OBJECTS_TABLE = "gold_dev.data_platform.raw_redshift_objects"

CREATE_SCANS_SQL = f"""\
CREATE TABLE IF NOT EXISTS {RAW_SCANS_TABLE} (
    raw_data VARIANT,
    _row_hash VARCHAR,
    _extracted_at TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file VARCHAR DEFAULT 'redshift_stl_scan'
);
"""

CREATE_OBJECTS_SQL = f"""\
CREATE TABLE IF NOT EXISTS {RAW_OBJECTS_TABLE} (
    raw_data VARIANT,
    _row_hash VARCHAR,
    _extracted_at TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file VARCHAR DEFAULT 'redshift_object_inventory'
);
"""

SCAN_QUERY = """\
SELECT
    s.starttime::date AS scan_date,
    TRIM(s.perm_table_name) AS perm_table_name,
    TRIM(u.usename) AS username,
    COUNT(DISTINCT s.query) AS distinct_queries,
    COUNT(*) AS total_scans,
    SUM(s.rows) AS rows_scanned,
    SUM(s.bytes) AS bytes_scanned,
    SUM(CASE WHEN s.type = 2 THEN s.bytes ELSE 0 END) AS spectrum_bytes,
    SUM(DATEDIFF(ms, s.starttime, s.endtime)) / 1000.0 AS compute_seconds
FROM stl_scan s
JOIN pg_user u ON s.userid = u.usesysid
WHERE s.perm_table_name NOT LIKE 'volt_tt_%%'
  AND s.perm_table_name NOT LIKE '#%%'
GROUP BY 1, 2, 3
"""

OBJECTS_QUERY = """\
SELECT TRIM(schemaname) AS schemaname, TRIM(tablename) AS objectname, 'table' AS obj_type, NULL AS mv_physical_name
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema', 'pg_internal')

UNION ALL

SELECT DISTINCT TRIM("schema") AS schemaname, TRIM("name") AS objectname, 'materialized_view' AS obj_type,
       'mv_tbl__' || TRIM("name") || '__0' AS mv_physical_name
FROM STV_MV_INFO
WHERE db_name = 'defaultdb'

UNION ALL

SELECT TRIM(schemaname) AS schemaname, TRIM(viewname) AS objectname, 'view' AS obj_type, NULL AS mv_physical_name
FROM pg_views
WHERE schemaname NOT IN ('pg_catalog', 'information_schema', 'pg_internal')
"""


def _query_to_ndjson(query: str) -> list[str]:
    conn = redshift.connect()
    try:
        cur = conn.cursor()
        cur.execute(query)
        cols = [d[0] for d in cur.description]
        rows = []
        for row in cur.fetchall():
            record = {}
            for col, val in zip(cols, row):
                if isinstance(val, date):
                    record[col] = val.isoformat()
                elif val is None:
                    record[col] = None
                else:
                    record[col] = val
            rows.append(json.dumps(record, default=str))
        return rows
    finally:
        conn.close()


@task(name="extract_redshift_scans", retries=1, retry_delay_seconds=60, log_prints=True)
def extract_redshift_scans() -> int:
    """Extract aggregated stl_scan data from Redshift (full retention window) and load to Snowflake."""
    print("[Redshift Scans] Extracting stl_scan aggregation...")
    json_strings = _query_to_ndjson(SCAN_QUERY)

    if not json_strings:
        print("[Redshift Scans] WARNING: No rows extracted")
        return 0

    print(f"[Redshift Scans] Extracted {len(json_strings)} rows, loading to Snowflake...")
    loaded = load_to_snowflake(json_strings, RAW_SCANS_TABLE, CREATE_SCANS_SQL)
    print(f"[Redshift Scans] Loaded {loaded} rows to {RAW_SCANS_TABLE}")
    return loaded


@task(name="extract_redshift_objects", retries=1, retry_delay_seconds=60, log_prints=True)
def extract_redshift_objects() -> int:
    """Extract Redshift object inventory (tables, MVs, views) and load to Snowflake."""
    print("[Redshift Objects] Extracting object inventory...")
    json_strings = _query_to_ndjson(OBJECTS_QUERY)

    if not json_strings:
        print("[Redshift Objects] WARNING: No rows extracted")
        return 0

    print(f"[Redshift Objects] Extracted {len(json_strings)} rows, loading to Snowflake...")
    loaded = load_to_snowflake(json_strings, RAW_OBJECTS_TABLE, CREATE_OBJECTS_SQL)
    print(f"[Redshift Objects] Loaded {loaded} rows to {RAW_OBJECTS_TABLE}")
    return loaded
