# Migrate fivetran_log connector to Snowflake

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Nikitha Jadhav
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to set up a fivetran_log connector targeting the Snowflake destination **so that** the last Redshift-exclusive Fivetran connector can be paused.

## Background

fivetran_log and fivetran_metadata are the only 2 Fivetran connectors without Snowflake equivalents. They provide Fivetran platform metadata (connector status, MAR usage, sync history). 53K consumer queries in the observation window -- actively read by service_dbt, service_qs_*, datasciadmin, service_bigquery, and others.

## Scope

**In scope**
- Add fivetran_log connector to BT_FIVETRAN_PROD (Snowflake destination)
- Validate data parity
- Update any downstream consumers (lib/fivetran.py, dbt models)
- Pause the RS fivetran_log and fivetran_metadata connectors

**Out of scope**
- Restructuring the Fivetran usage reporting pipeline

## Inputs

- Fivetran admin dashboard
- BT_FIVETRAN_PROD destination configuration

## Outputs / Deliverables

- fivetran_log data available in Snowflake
- RS connectors paused

## Acceptance Criteria

1. fivetran_log tables available in BT_FIVETRAN_PROD
2. Data matches RS version (sync history, MAR, connector metadata)
3. RS fivetran_log and fivetran_metadata connectors paused

## Definition of Done

- [ ] Snowflake connector operational
- [ ] Data validated
- [ ] RS connectors paused
- [ ] Documented

## Dependencies

- Blocked by: none
- Blocking: none (but eliminates last RS-exclusive Fivetran connector)

## Estimated Effort

Unknown
