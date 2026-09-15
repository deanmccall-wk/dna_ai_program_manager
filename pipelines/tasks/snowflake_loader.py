"""Shared Snowflake loader — PUT/COPY INTO via table stage.

All extract tasks write NDJSON to a temp file, then call load_to_snowflake()
to PUT the file to the table stage and COPY INTO the target table.
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import snowflake.connector
from prefect import task

logger = logging.getLogger(__name__)


def get_snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    return snowflake.connector.connect(
        account="KEAZVSO-BUSINESS_TECH_PROD",
        user="dean.mccall@workiva.com",
        authenticator="externalbrowser",
        role="DATA_PLATFORM_ANALYST",
        warehouse="PROD_WH",
        database="gold_dev",
        schema="data_platform",
    )


def write_ndjson(json_strings: list[str], output_dir: Path, filename: str = "extract.json") -> Path:
    output_path = output_dir / filename
    with open(output_path, "w") as f:
        for js in json_strings:
            f.write(js + "\n")
    return output_path


@task(name="load_to_snowflake", retries=2, retry_delay_seconds=30, log_prints=True)
def load_to_snowflake(json_strings: list[str], table_name: str, create_sql: str) -> int:
    short_name = table_name.split(".")[-1]
    conn = get_snowflake_connection()
    try:
        cur = conn.cursor()
        cur.execute("USE ROLE DATA_PLATFORM_ANALYST")
        cur.execute("USE WAREHOUSE PROD_WH")
        cur.execute("USE DATABASE gold_dev")
        cur.execute("USE SCHEMA data_platform")
        cur.execute(create_sql)
        logger.info("Ensured %s exists", table_name)

        with tempfile.TemporaryDirectory() as tmpdir:
            ndjson_path = write_ndjson(json_strings, Path(tmpdir), f"{short_name}.json")
            logger.info("Wrote %d rows to %s", len(json_strings), ndjson_path)

            put_sql = f"PUT 'file://{ndjson_path}' @%{short_name} AUTO_COMPRESS=TRUE OVERWRITE=TRUE"
            cur.execute(put_sql)
            logger.info("PUT complete for %s", short_name)

            copy_sql = f"""
                COPY INTO {table_name} (raw_data, _row_hash, _source_file)
                FROM (
                    SELECT $1, MD5($1::VARCHAR), metadata$filename
                    FROM @%{short_name}
                )
                FILE_FORMAT = (TYPE = 'JSON', STRIP_OUTER_ARRAY = FALSE)
                PURGE = TRUE
            """
            cur.execute(copy_sql)
            copy_result = cur.fetchall()
            loaded = sum(int(row[3]) for row in copy_result) if copy_result else 0
            logger.info("COPY INTO %s: %d rows loaded", short_name, loaded)

        return loaded
    finally:
        conn.close()
