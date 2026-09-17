# Disable inactive Redshift user accounts

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Nikitha Jadhav
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to disable ~130 Redshift user accounts that have no activity in 30+ days **so that** we reduce the active connection surface and prepare for cluster shutdown.

## Background

10 users already disabled with no reported breakage (scream test passed). ~130 additional enabled accounts have zero queries in the observation window. Disabling sets CONNECTION LIMIT 0 which is recoverable.

## Scope

**In scope**
- Set CONNECTION LIMIT 0 for ~130 inactive accounts
- Exclude: active service accounts, InfoSec, DNA team accounts

**Out of scope**
- Dropping user accounts (reversibility needed)

## Inputs

- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY` (consumer_user_list)
- Redshift pg_user catalog

## Outputs / Deliverables

- ~130 accounts set to CONNECTION LIMIT 0
- List of disabled accounts documented

## Acceptance Criteria

1. All identified inactive accounts have CONNECTION LIMIT 0
2. Active service accounts and InfoSec accounts remain unaffected
3. No breakage reported after 7-day scream test period

## Definition of Done

- [ ] Accounts disabled
- [ ] Validated no breakage after 7 days
- [ ] Documented

## Dependencies

- Blocked by: none
- Blocking: none

## Estimated Effort

Unknown
