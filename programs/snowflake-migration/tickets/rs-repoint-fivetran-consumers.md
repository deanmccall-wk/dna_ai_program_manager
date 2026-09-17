# Re-point 10 Fivetran consumer schemas to Snowflake

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Stephanie Holzschuh
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to re-point the dbt, QuickSight, and Overlord consumers that read from 10 Fivetran-loaded RS staging schemas **so that** we can pause the remaining RS connectors.

## Background

10 of 18 Fivetran RS connectors are duplicated in Snowflake but their RS staging tables still have active consumers: staging_coupa (13 consumers, 95K queries), staging_concur (8, 39K), staging_zendesk (8, 39K), staging_workramp (2, 392), staging_intacct (3, 103), staging_google_sheets (1, 16). Consumers include service_dbt, service_qs_*, datasciadmin, service_bigquery, service_wdc_*.

## Scope

**In scope**
- Identify each consumer process per schema using `REDSHIFT_ORPHAN_INVENTORY` and `REDSHIFT_DEPENDENCY_GRAPH`
- Re-point or confirm Snowflake equivalent for each consumer
- Pause the 10 RS connectors after all consumers are re-pointed

**Out of scope**
- The 8 orphaned connectors (already being paused in separate ticket)

## Inputs

- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY`
- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_DEPENDENCY_GRAPH` (after lineage extraction)
- Fivetran dashboard

## Outputs / Deliverables

- All consumers re-pointed to Snowflake equivalents
- 10 RS connectors paused

## Acceptance Criteria

1. Each of the 10 staging schemas has zero non-Fivetran consumer scans in the daily pipeline
2. All 10 connectors paused in Fivetran
3. No downstream breakage after 48 hours

## Definition of Done

- [ ] Consumers re-pointed
- [ ] Connectors paused
- [ ] Validated no breakage
- [ ] Documented

## Dependencies

- Blocked by: Atlan lineage extraction (for full consumer map)
- Blocking: none (but accelerates resize to 2 nodes)

## Estimated Effort

Unknown
