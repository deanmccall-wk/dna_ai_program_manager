# Terminate Redshift cluster and clean up infrastructure

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Sreehanth Komma
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to terminate the Redshift cluster and clean up all associated AWS resources **so that** we achieve $0 Redshift spend.

## Background

Final phase. Requires 0 active queries for 7 consecutive days (confirmed via daily scan pipeline), OpenAir cutover complete, and FedRAMP boundary change accepted by Tennessee Valley Authority.

## Scope

**In scope**
- Terminate Redshift cluster (ito-ds-redshift-dsredshift-kfbgevo589gl)
- Delete manual snapshots
- Clean up S3 buckets (ito-ds-redshift-us-east-1, audit log, itz-ds-redshift-us-east-1)
- Remove IAM roles, security groups, VPC endpoints
- Validate $0 Redshift in next billing cycle

**Out of scope**
- Archiving Redshift data (already in Snowflake)

## Inputs

- Daily scan pipeline (7-day zero-query confirmation)
- AWS Console / CLI
- OpenAir cutover confirmation
- FedRAMP acceptance confirmation

## Outputs / Deliverables

- Cluster terminated
- All associated AWS resources removed
- $0 Redshift line item confirmed in billing

## Acceptance Criteria

1. Daily scan pipeline shows 0 queries for 7 consecutive days
2. OpenAir cutover ticket marked done
3. FedRAMP acceptance ticket marked done
4. Cluster terminated and not recoverable
5. Next AWS billing cycle shows $0 Redshift spend

## Definition of Done

- [ ] Cluster terminated
- [ ] Snapshots deleted
- [ ] S3 buckets cleaned
- [ ] IAM/VPC cleaned
- [ ] Billing confirmed $0
- [ ] Documented

## Dependencies

- Blocked by: OpenAir cutover, FedRAMP acceptance, 7-day zero-query confirmation
- Blocking: none (this is the finish line)

## Estimated Effort

Unknown
