# Data Quality Checks and Tier 1 Issue Resolution

**Slug:** `data-quality`
**Period:** 2026 H2
**Goal:** Increase trust in data
**Owner:** Dean McCall
**RICE:** R=5, I=3, C=3, E=5 (SUM=16)
**Source:** `shared/data/dna-roadmap.xlsx` tab `DnA_H226` row 15

## Q3 Scope

End-to-end data pipeline data quality checks including a methodology for complex business quality checks.

* Implement data quality standard: Define and deploy core quality checks (Uniqueness, Completeness, Nullability, Freshness, and Referential Integrity).
* Alerting Pipeline: Configure automated notification channels (OpsGenie) triggered by threshold violations.

**Targets:**
* 100% of Tier-1 (Gold/Mart) tables covered by core quality checks.
* < 15 min latency between a quality rule violation and notification delivery.
* 0 unmonitored production pipelines feeding executive reporting.

## Q4 Scope

* Silver Layer Expansion: Extend quality check automation down to Tier-2 (Silver/Transformed) data layers.
* CI/CD Quality Gates: Integrate dbt-test / automated assertion steps into build pipelines to block bad data before deployment.
* Centralized Data Health Dashboard: Build an executive- and engineer-facing observability view.

**Targets:**
* >= 80% overall check coverage across all production schemas (Silver + Gold).
* 95% reduction in silent data corruption incidents reported by downstream business consumers.
* 100% visibility of data pipeline health status via a single-source-of-truth executive dashboard.

## Resource Allocations

| Person | Allocation |
|--------|-----------|
| Data Ops Lead (TBH) | 1.0 |
| Shobhit Pandey (Data Ops Contractor) | 1.0 |
| Nikitha Jadhav (Data Ops Contractor) | 1.0 |

## Stakeholders

BT-Foundation

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-31 | unknown | Initial program creation. No Jira linked. |

## Mapping

Jira: none linked on H2 sheet. Needs Jira epic or issue search.
