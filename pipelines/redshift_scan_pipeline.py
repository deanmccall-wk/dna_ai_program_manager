"""Redshift scan inventory pipeline — extract stl_scan + objects, then dbt transform.

Layers:
  1. Extract  — parallel: stl_scan aggregation + object inventory from Redshift -> raw tables
  2. Bronze   — dbt: staging models (dedup)
  3. Silver   — dbt: classification rules + dim_workers join
  4. Gold     — dbt: orphan inventory + MV prioritization

Usage:
    python pipelines/redshift_scan_pipeline.py
    python pipelines/redshift_scan_pipeline.py --target prod
    python pipelines/redshift_scan_pipeline.py --include-lineage
"""

from __future__ import annotations

import argparse
import atexit
import logging
import subprocess
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

PREFECT_API_URL = "http://127.0.0.1:4200/api"
_prefect_process: subprocess.Popen | None = None


def ensure_prefect_server() -> None:
    global _prefect_process
    try:
        resp = httpx.get(f"{PREFECT_API_URL}/health", timeout=3)
        if resp.status_code == 200:
            logger.info("Prefect server already running at %s", PREFECT_API_URL)
            return
    except (httpx.ConnectError, httpx.TimeoutException):
        pass

    logger.info("Prefect server not running. Starting...")
    _prefect_process = subprocess.Popen(
        ["prefect", "server", "start"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    atexit.register(_stop_prefect_server)

    for _ in range(30):
        time.sleep(1)
        try:
            resp = httpx.get(f"{PREFECT_API_URL}/health", timeout=2)
            if resp.status_code == 200:
                logger.info("Prefect server started (pid=%d)", _prefect_process.pid)
                return
        except (httpx.ConnectError, httpx.TimeoutException):
            pass

    raise RuntimeError("Prefect server failed to start within 30 seconds")


def _stop_prefect_server() -> None:
    global _prefect_process
    if _prefect_process and _prefect_process.poll() is None:
        logger.info("Stopping Prefect server (pid=%d)", _prefect_process.pid)
        _prefect_process.terminate()
        try:
            _prefect_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            _prefect_process.kill()
        _prefect_process = None


def _preflight_checks() -> None:
    """Validate Redshift and Snowflake connectivity before starting."""
    import snowflake.connector

    from lib import redshift

    failures: list[str] = []

    try:
        info = redshift.check()
        logger.info("Preflight OK: Redshift (%s)", info)
    except Exception as exc:
        failures.append(f"Redshift: {exc}")

    try:
        sf_conn = snowflake.connector.connect(
            account="KEAZVSO-BUSINESS_TECH_PROD",
            user="dean.mccall@workiva.com",
            authenticator="externalbrowser",
            database="GOLD_DEV",
            schema="DATA_PLATFORM",
            warehouse="PROD_WH",
        )
        sf_conn.cursor().execute("SELECT 1")
        sf_conn.close()
        logger.info("Preflight OK: Snowflake")
    except Exception as exc:
        failures.append(f"Snowflake: {exc}")

    if failures:
        msg = "\n  Preflight failed:\n"
        for f in failures:
            msg += f"    - {f}\n"
        raise SystemExit(msg)


def run_pipeline(target: str, include_lineage: bool = False) -> None:
    from prefect import flow

    from pipelines.tasks.dbt_run import dbt_run_layer
    from pipelines.tasks.extract_redshift_scans import (
        extract_redshift_objects,
        extract_redshift_scans,
    )

    _preflight_checks()

    @flow(name="redshift_scan_pipeline", log_prints=True)
    def redshift_scan_pipeline() -> None:
        print("=== Redshift Scan Inventory Pipeline ===")
        print(f"  dbt target: {target}")

        # --- Extract layer (parallel) ---
        print("\n--- Extract Layer ---")
        scans_future = extract_redshift_scans.submit()
        objects_future = extract_redshift_objects.submit()

        extract_tasks = {
            "redshift_scans": scans_future,
            "redshift_objects": objects_future,
        }

        results: dict[str, int] = {}
        failures: dict[str, str] = {}

        for name, future in extract_tasks.items():
            try:
                row_count = future.result()
                results[name] = row_count
                print(f"  [OK] {name}: {row_count} rows")
            except Exception as exc:
                failures[name] = str(exc)
                print(f"  [FAIL] {name}: {exc}")

        if failures:
            raise RuntimeError(f"Extract failed: {failures}")

        total_extracted = sum(results.values())

        # --- dbt layers ---
        print("\n--- Bronze Layer (staging / dedup) ---")
        dbt_run_layer.with_options(name="bronze_layer")(layer_tag="bronze", target=target)

        print("\n--- Silver Layer (classification) ---")
        dbt_run_layer.with_options(name="silver_layer")(layer_tag="silver", target=target)

        print("\n--- Gold Layer (orphan inventory) ---")
        dbt_run_layer.with_options(name="gold_layer")(layer_tag="gold", target=target)

        # --- Optional: Atlan lineage ---
        if include_lineage:
            print("\n--- Atlan Lineage (for active objects) ---")
            print("  [STUB] Atlan lineage extraction not yet implemented")
            # TODO: extract_atlan_lineage(active_objects)
            # Re-run dbt to process lineage data

        print(f"\n=== Pipeline Complete ===")
        print(f"  Extracted: {total_extracted} rows from {len(results)} sources")

    redshift_scan_pipeline()


def main() -> None:
    parser = argparse.ArgumentParser(description="Redshift scan inventory pipeline")
    parser.add_argument("--target", default="dev", choices=["dev", "prod"])
    parser.add_argument("--include-lineage", action="store_true", help="Also extract Atlan lineage for active objects")
    args = parser.parse_args()

    ensure_prefect_server()
    run_pipeline(args.target, args.include_lineage)


if __name__ == "__main__":
    main()
