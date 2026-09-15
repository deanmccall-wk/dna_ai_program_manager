# FedRamp Sanitization Compliance for Snowflake

**Slug:** `fedramp-sanitization`
**Period:** 2026 H2
**Goal:** Deliver a modernized Enterprise Data Platform
**Owner:** Dean McCall
**RICE:** R=5, I=5, C=5, E=5 (SUM=20)
**Jira:** [DNA-5623](https://jira.atl.workiva.net/browse/DNA-5623)
**Source:** `shared/data/dna-roadmap.xlsx` tab `DnA_H226` row 6

## Q3 Scope

* Sanitize federal fields for all federal customers.
* Execution of targeted Iceberg snapshot expungement, physical S3 Parquet file purging via automated dbt Cloud jobs, and external metadata catalog synchronization.
* Modify dbt Cloud source configs and dbt project models to permanently disconnect Federal raw landing zones in S3 from commercial transformation DAGs.

**Targets:**
* 0 Residual Federal data in Snowflake.
* 0 broken or non-compliant references.

## Q4 Scope

* Automated S3 & Iceberg Life-Cycle Governance
* dbt CI/CD Static Analysis & Ingestion Guards: Integrate dbt-checkpoint and custom pre-commit hooks into dbt Cloud pipeline deployments to block pull requests that attempt to build Iceberg models over restricted S3 path patterns.
* Compliance Certification & Attestation

**Targets:**
* 100% CI/CD enforcement.
* 0 audit non-conformances.

## Resource Allocations

| Person | Allocation |
|--------|-----------|
| Stephanie Holzschuh | 0.8 |

## Stakeholders

Security

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-31 | On Track | Stephanie Holzschuh executing. Jira DNA-5623 is Open/To Do (needs transition to In Progress). FedRamp sanitization is not a dependency for Redshift decommission -- the two methods proceed independently. |

## Mapping

Jira: [DNA-5623](https://jira.atl.workiva.net/browse/DNA-5623)
