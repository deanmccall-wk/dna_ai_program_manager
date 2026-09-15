#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$PROJECT_ROOT"
export PREFECT_API_URL="${PREFECT_API_URL:-http://127.0.0.1:4200/api}"

usage() {
    echo "Usage: ./run.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo "  pipeline       Run the Redshift scan inventory pipeline (extract + dbt)"
    echo "  deploy         Deploy dbt project to Snowflake"
    echo "  server         Start the Prefect server"
    echo ""
    echo "Options are passed through to the underlying script."
    echo ""
    echo "Examples:"
    echo "  ./run.sh pipeline"
    echo "  ./run.sh pipeline --target prod"
    echo "  ./run.sh pipeline --include-lineage"
    echo "  ./run.sh deploy"
    echo "  ./run.sh deploy --target prod --skip-test"
    echo "  ./run.sh server"
}

case "${1:-}" in
    pipeline)
        shift
        python "$PROJECT_ROOT/pipelines/redshift_scan_pipeline.py" "$@"
        ;;
    deploy)
        shift
        python "$PROJECT_ROOT/pipelines/deploy_dbt.py" "$@"
        ;;
    server)
        prefect server start
        ;;
    *)
        usage
        exit 1
        ;;
esac
