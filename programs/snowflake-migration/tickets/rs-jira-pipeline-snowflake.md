# Stand up Jira pipeline in Snowflake

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Daniel Petty
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to create a Jira data pipeline in Snowflake for the ASSET and INV projects **so that** the Overlord Jira jobs in Redshift can be disabled.

## Background

`public.jira_inventory` in Redshift contains 45,899 issues across ASSET (23,857) and INV (22,042) projects. This table is loaded by Overlord and has active consumers (service_dbt reads it). No equivalent pipeline exists in Snowflake. The Jira data is sourced from Workiva's Jira instance (jira.atl.workiva.net). Fivetran already has a Jira connector in the Snowflake destination (BT_FIVETRAN_PROD) for the broader Jira dataset, but the ASSET/INV inventory data may need a separate path.

## Scope

**In scope**
- Determine the right ingestion method (Fivetran Jira connector, Openflow, or custom)
- Set up the pipeline to load ASSET and INV project data to Snowflake
- Create equivalent dbt models in Snowflake
- Validate data parity with Redshift jira_inventory table

**Out of scope**
- Jira DNA and SPP MVs (already orphaned, no consumers)

## Inputs

- Redshift `public.jira_inventory` (schema and sample data)
- Jira API / Fivetran Jira connector configuration
- BT_FIVETRAN_PROD existing Jira connector

## Outputs / Deliverables

- Jira ASSET/INV data available in Snowflake
- dbt models producing equivalent of `jira_inventory`
- Data parity validation report

## Acceptance Criteria

1. Jira ASSET and INV issues available in Snowflake with all columns from Redshift jira_inventory
2. Row counts match within 1% of Redshift source
3. Downstream dbt models that read jira_inventory can be re-pointed to Snowflake

## Definition of Done

- [ ] Pipeline operational
- [ ] Data parity validated
- [ ] dbt models created
- [ ] Documented

## Dependencies

- Blocked by: none
- Blocking: Overlord Jira job decommission

## Estimated Effort

Unknown (estimated 3-4 weeks)

## Snowflake (if applicable)

- Target database/schema: TBD (likely LAKE_PROD or SILVER_PROD)
- Expected volumes: ~46K rows, low update frequency
