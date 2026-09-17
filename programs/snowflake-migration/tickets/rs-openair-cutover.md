# OpenAir reverse ETL cutover to Snowflake

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Lincoln Lopes Silva
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to cut over the 23 OpenAir reverse ETL jobs from Redshift to Snowflake **so that** the last critical-path blocker for full Redshift shutdown is removed.

## Background

23 bidirectional Salesforce-OpenAir sync jobs run via datasciadmin in Redshift (12 upload to OpenAir, 11 upload to Salesforce). These are SOX-compliant and revenue-impacting. Source tables: public.openair_* views reading from mv_spectrum.oa_* MVs. The OpenAir non-prod environment provisioning has been delayed. Finance/Accounting sign-off required before production cutover.

## Scope

**In scope**
- Stand up Fivetran OpenAir connector targeting Snowflake
- Validate data parity for all 23 jobs
- Obtain Finance/Accounting SOX sign-off
- Disable Overlord OpenAir jobs in Redshift

**Out of scope**
- Modifying the OpenAir system itself

## Inputs

- data_services_etl repo (upload/openair, upload/salesforce)
- Redshift public.openair_* views
- OpenAir non-prod environment (when available)

## Outputs / Deliverables

- OpenAir data flowing through Snowflake
- Parity validation report
- Finance sign-off documentation
- Overlord OpenAir jobs disabled

## Acceptance Criteria

1. All 23 sync jobs operational via Snowflake
2. Data parity validated against Redshift for all OpenAir tables
3. Finance/Accounting sign-off obtained and documented
4. datasciadmin OpenAir queries drop to zero in daily scan pipeline

## Definition of Done

- [ ] Fivetran connector operational
- [ ] Parity validated
- [ ] SOX sign-off obtained
- [ ] Overlord jobs disabled
- [ ] Documented

## Dependencies

- Blocked by: OpenAir non-prod environment provisioning
- Blocking: Phase 5 full cluster shutdown

## Estimated Effort

Unknown (estimated through end of October)
