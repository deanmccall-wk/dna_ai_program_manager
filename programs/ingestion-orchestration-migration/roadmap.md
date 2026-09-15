# Legacy Ingestion and Orchestration Migration

**Slug:** `ingestion-orchestration-migration`
**Period:** 2026 H2
**Goal:** Deliver a modernized Enterprise Data Platform
**Owner:** Matt Kelley
**RICE:** R=5, I=4, C=5, E=1 (SUM=15)
**Jira:** [DNA-6050](https://jira.atl.workiva.net/browse/DNA-6050)
**Source:** `shared/data/dna-roadmap.xlsx` tab `DnA_H226` row 20

## Q3 Scope

1. **Source inventory** -- every pipeline on Overlord with volume, SLA, freshness, downstream consumers, custom logic.
2. **MWAA DAG inventory** -- count, complexity, custom operators, cross-DAG dependencies, backfill/retry semantics, SLA-bound jobs.
3. **Overlord orchestrator assessment** -- identify behaviors Airflow won't replicate cleanly.
4. **Define evaluation criteria** for both tracks -- connector coverage, extensibility, cost at volume.
5. **Ingestion vendor evaluation** -- Fivetran, Snowflake Openflow, and 1-2 alternates for commercial leverage.
6. **MWAA fitness review** at target scale -- version, worker sizing, concurrency ceilings.
7. **Ingestion and Orchestration POC** -- 3-4 representative sources: standard SaaS connector and Custom connectors.
8. **Wave plan** -- vertical slices pairing ingestion and orchestration per source group.

**Exit criteria:** both decisions on ingestion and orchestration vendors agreed, target architecture agreed, wave plan for planned sources, migration plan drafted.

## Q4 Scope

1. **Ingestion platform foundation** -- environments, landing zones, secrets, CI/CD, monitoring, access control.
2. **Orchestration hardening** -- sizing, DAG CI/CD, secrets, observability, alerting, RBAC.
3. **Migration framework** -- reusable ingestion patterns, DAG templates, parallel-run and reconciliation harness, cutover runbook, rollback path.
4. **Build the seam** -- completion-event integration between the ingestion tool and MWAA.
5. REVIEW - **Freeze new development on Overlord.** *(Do this early -- it stops the target moving.)*
6. **Wave 1 + 2: standardized sources**, migrated as vertical slices with ingestion and orchestration cut over together per source.
7. **Prove the custom-source pattern** on 2-3 sources before volume work begins.
8. **Rebuild surviving custom orchestration logic** and validate against parallel runs.
9. **Decommission plan** -- dated, with a cost-retirement schedule for both Overlord components.

**Exit criteria:** standardized majority running end-to-end on the new stack; custom-source pattern proven; decommission plan and dates.

## Resource Allocations

| Person | Allocation |
|--------|-----------|
| Stephanie Holzschuh | 0.2 |
| Daniel Petty | 0.4 |
| DE/Architect Contractor (TBH) | 0.4 |

Note: DE/Architect Contractor is TBH -- unfilled position.

## Stakeholders

BT-Foundation

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-31 | unknown | Initial program creation. Jira DNA-6050 linked -- status to be pulled. |

## Mapping

Jira: [DNA-6050](https://jira.atl.workiva.net/browse/DNA-6050)
