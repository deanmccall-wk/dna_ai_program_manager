# Re-point dbt models from Redshift to Snowflake

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Stephanie Holzschuh
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to re-point the remaining dbt models that read from Redshift sources to their Snowflake equivalents **so that** service_dbt no longer queries Redshift.

## Background

service_dbt accounts for 19.4% of Redshift query volume (~19K queries/day). These are dbt Cloud models that read from Redshift staging and public tables, then write derived tables. The Snowflake equivalents of the source data already exist. The models need their source definitions updated.

## Scope

**In scope**
- Identify all dbt models with Redshift sources (from lineage data)
- Update source definitions to point to Snowflake tables
- Test and deploy updated models

**Out of scope**
- Creating new Snowflake source data (already exists)

## Inputs

- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_DEPENDENCY_GRAPH` (dbt model dependencies)
- dbt Cloud project configuration
- data_models repo

## Outputs / Deliverables

- All dbt models re-pointed to Snowflake sources
- dbt Cloud Redshift connection decommissioned

## Acceptance Criteria

1. service_dbt has zero queries in Redshift daily scan pipeline
2. All dbt models pass CI tests against Snowflake sources
3. No data quality regressions in downstream tables

## Definition of Done

- [ ] Source definitions updated
- [ ] CI tests pass
- [ ] Deployed to production
- [ ] Validated via daily scan pipeline

## Dependencies

- Blocked by: Atlan lineage extraction (full dependency map)
- Blocking: Phase 4 resize (reduces workload)

## Estimated Effort

Unknown
