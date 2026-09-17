# Stop 52 orphaned MV refreshes

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Shobhit Pandey
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to stop the refresh scheduler for 52 orphaned materialized views in mv_spectrum **so that** we eliminate wasted compute and reduce Spectrum scan costs.

## Background

Physical read tracking confirmed 52 of 186 mv_spectrum materialized views have zero consumer scans in the 10-day observation window. These views are being refreshed daily by datasciadmin but nobody reads the output. Sources: OpenAir (16), Zendesk (10), Salesforce (8), Gainsight (5), Workday/WalkMe/Wdesk (3), SEC/EDGAR/NASDAQ (3), Jira (2), Atlan (1).

## Scope

**In scope**
- Disable refresh for the 52 orphaned MVs listed in `REDSHIFT_ORPHAN_INVENTORY WHERE object_type = 'materialized_view' AND classification = 'orphan'`

**Out of scope**
- The 102 active MVs (have consumer scans)
- The 32 low-activity MVs (need further analysis)

## Inputs

- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY`
- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_MV_PRIORITIZATION`
- Redshift Overlord scheduler configuration

## Outputs / Deliverables

- 52 MV refreshes disabled
- List of disabled MVs documented

## Acceptance Criteria

1. All 52 orphaned MVs no longer appear in active refresh schedules
2. No consumer-reported errors after 7 days
3. Spectrum scan cost visibly decreases in AWS Cost Explorer

## Definition of Done

- [ ] Refreshes disabled
- [ ] Validated no breakage after 7 days
- [ ] Documented in shutdown plan

## Dependencies

- Blocked by: none
- Blocking: Phase 2 resize (reduces compute load)

## Estimated Effort

Unknown
