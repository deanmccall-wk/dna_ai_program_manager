"""Deploy dbt project to Snowflake via snow dbt deploy.

Run manually after model changes. Not part of the daily scan pipeline.
Runs without Prefect server -- plain function calls.

Usage:
    python pipelines/deploy_dbt.py
    python pipelines/deploy_dbt.py --target prod
    python pipelines/deploy_dbt.py --skip-test
"""

from __future__ import annotations

import argparse
import logging
import subprocess
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

DBT_PROJECT = "dna_ai_program_manager"
DATABASE = "gold_dev"
SCHEMA = "data_platform"
CONNECTION = "keazvso-business_tech_prod"
DBT_DIR = str(Path(__file__).resolve().parents[1] / "dbt")


def dbt_deploy() -> None:
    cmd = ["snow", "dbt", "deploy", DBT_PROJECT,
           "--source", DBT_DIR, "--database", DATABASE, "--schema", SCHEMA,
           "--connection", CONNECTION, "--force"]
    logger.info("Running: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.stdout:
        for line in result.stdout.strip().split("\n"):
            print(f"  {line}")
    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  [stderr] {line}")

    if result.returncode != 0:
        raise RuntimeError(f"dbt deploy failed (exit {result.returncode}): {result.stderr}")

    logger.info("dbt project deployed to %s.%s.%s", DATABASE, SCHEMA, DBT_PROJECT)


def dbt_test_deploy(target: str = "dev") -> None:
    cmd = ["snow", "dbt", "execute", DBT_PROJECT, "--args", f"build --target {target}",
           "--database", DATABASE, "--schema", SCHEMA]
    logger.info("Running post-deploy verification: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)

    if result.stdout:
        for line in result.stdout.strip().split("\n"):
            print(f"  {line}")
    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  [stderr] {line}")

    if result.returncode != 0:
        raise RuntimeError(f"Post-deploy build failed (exit {result.returncode}): {result.stderr}")

    logger.info("Post-deploy verification passed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy dbt project to Snowflake")
    parser.add_argument("--target", default="dev", choices=["dev", "prod"])
    parser.add_argument("--skip-test", action="store_true")
    args = parser.parse_args()

    print(f"=== Deploying dbt project: {DBT_PROJECT} ===")
    print(f"  Database: {DATABASE}")
    print(f"  Schema: {SCHEMA}")
    print(f"  Project dir: {DBT_DIR}")
    print()

    dbt_deploy()

    if not args.skip_test:
        print()
        dbt_test_deploy(target=args.target)
    else:
        logger.info("Skipping post-deploy verification (--skip-test)")

    print("\n=== Deploy complete ===")


if __name__ == "__main__":
    main()
