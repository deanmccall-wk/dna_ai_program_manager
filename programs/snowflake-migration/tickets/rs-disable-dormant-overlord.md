# Disable dormant Overlord jobs

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Shobhit Pandey
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to disable 8 dormant Overlord ETL jobs with zero consumers **so that** we reduce unnecessary staging loads on the cluster.

## Background

8 Overlord jobs load data that has zero downstream consumers: Crunchbase/SPAC (hourly, 0 consumers), Intelligize (0 rows), FERC, Lattice, WDATA (0 queries in 90 days), CPXDNA (confirm with CPX first).

## Scope

**In scope**
- Disable: Crunchbase/SPAC, Intelligize, FERC, Lattice, WDATA, CPXDNA (after CPX confirmation)

**Out of scope**
- Active Overlord jobs (OpenAir, Salesforce, etc.)

## Inputs

- Overlord scheduler configuration
- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY`

## Outputs / Deliverables

- 8 Overlord jobs disabled
- CPX confirmation obtained for CPXDNA before disabling

## Acceptance Criteria

1. All 8 jobs no longer execute on schedule
2. CPX team confirms CPXDNA can be disabled before it is stopped
3. No consumer-reported errors after 7 days

## Definition of Done

- [ ] Jobs disabled
- [ ] CPX confirmation documented
- [ ] Validated no breakage after 7 days

## Dependencies

- Blocked by: CPX confirmation for CPXDNA
- Blocking: none

## Estimated Effort

Unknown
