"""Run dbt transformations by layer via EXECUTE DBT PROJECT SQL."""

from __future__ import annotations

import logging
import os

import snowflake.connector
from prefect import task

logger = logging.getLogger(__name__)

DBT_PROJECT = "dna_ai_program_manager"
ACCOUNT = "KEAZVSO-BUSINESS_TECH_PROD"
DATABASE = "GOLD_DEV"
SCHEMA = "DATA_PLATFORM"


def _get_connection() -> snowflake.connector.SnowflakeConnection:
    return snowflake.connector.connect(
        account=ACCOUNT,
        user=os.environ.get("SNOWFLAKE_USER", "dean.mccall@workiva.com"),
        authenticator="externalbrowser",
        database=DATABASE,
        schema=SCHEMA,
        warehouse="PROD_WH",
    )


@task(retries=1, retry_delay_seconds=30, log_prints=True)
def dbt_run_layer(layer_tag: str, target: str = "dev") -> None:
    dbt_args = f"build --select tag:{layer_tag} --target {target}"
    sql = f"EXECUTE DBT PROJECT {DBT_PROJECT} ARGS = '{dbt_args}'"

    print(f"[dbt] Running {layer_tag} layer: {sql}")

    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"USE DATABASE {DATABASE}")
        cur.execute(f"USE SCHEMA {SCHEMA}")
        cur.execute(sql)
        result = cur.fetchone()

        if result:
            success = result[0]
            exception = result[1]
            stdout = result[2] if len(result) > 2 else ""

            if stdout:
                for line in stdout.strip().split("\n"):
                    clean = line.replace("[0m", "").replace("[32m", "").replace("[33m", "").replace("[31m", "")
                    if clean.strip():
                        print(f"[dbt:{layer_tag}] {clean}")

            if not success:
                raise RuntimeError(f"dbt {layer_tag} layer failed: {exception}\n{stdout}")

        print(f"[dbt] {layer_tag} layer completed successfully")
    finally:
        conn.close()
