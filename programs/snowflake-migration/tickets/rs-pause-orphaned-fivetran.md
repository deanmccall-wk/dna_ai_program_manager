# Pause 8 orphaned Fivetran RS connectors

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Shobhit Pandey
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to pause the 8 Fivetran connectors targeting Redshift that have no active consumers **so that** we stop unnecessary data loading and reduce Fivetran MAR costs.

## Background

Assessment confirmed 8 of 18 active Fivetran RS connectors load to staging schemas with zero non-Fivetran consumer scans. All 8 have active Snowflake equivalents in BT_FIVETRAN_PROD. Pausing is reversible.

## Scope

**In scope**
- Pause these connectors: navan, google_analytics_4, google_drive (x6)

**Out of scope**
- The 10 connectors with active RS consumers (intacct, coupa, zendesk, concur, google_sheets x3, workramp)
- Deleting the 16 already-paused connectors (separate cleanup)

## Inputs

- Fivetran dashboard / API
- Orphan analysis: `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY`

## Outputs / Deliverables

- 8 connectors paused in Fivetran
- Confirmation screenshot or API response

## Acceptance Criteria

1. All 8 named connectors show "paused" status in Fivetran
2. No errors reported by downstream consumers after 48 hours

## Definition of Done

- [ ] Connectors paused
- [ ] Validated no breakage after 48h
- [ ] Documented in shutdown plan

## Dependencies

- Blocked by: none
- Blocking: Phase 2 resize (reduces workload)

## Estimated Effort

Unknown
