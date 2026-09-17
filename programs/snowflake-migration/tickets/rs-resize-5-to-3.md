# Resize Redshift cluster from 5 to 3 nodes

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Sreehanth Komma
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to resize the Redshift cluster from 5 to 3 ra3.16xlarge nodes **so that** we reduce compute cost by $507/day ($15.4K/month) while maintaining safe performance margins.

## Background

CloudWatch data confirms the resize is safe: current 7-day peak hourly avg CPU is 43.5%, which projects to ~73% on 3 nodes (below the 80% safety threshold). Disk usage is 10.5% (RA3 managed storage, not a constraint). Elastic resize takes ~15 minutes with brief query interruption.

## Scope

**In scope**
- Submit elastic resize request (5 to 3 nodes)
- Monitor post-resize stability for 24 hours (CPU, connections, query latency)
- Rollback plan if issues arise

**Out of scope**
- Resize to 2 nodes (requires further workload reduction)

## Inputs

- AWS Console / CLI access for Redshift resize
- CloudWatch metrics: CPUUtilization, DatabaseConnections, PercentageDiskSpaceUsed

## Outputs / Deliverables

- Cluster running on 3 nodes
- Post-resize monitoring report (24h)

## Acceptance Criteria

1. Cluster resized to 3 ra3.16xlarge nodes
2. Post-resize peak CPU stays below 80% for 24 hours
3. No query failures or timeouts reported
4. AWS billing confirms reduced compute rate within next billing cycle

## Definition of Done

- [ ] Resize executed
- [ ] 24h monitoring passed
- [ ] Savings confirmed in billing
- [ ] Documented

## Dependencies

- Blocked by: Phase 1 quick wins (reduces workload, improves safety margin)
- Blocking: Phase 4 resize to 2 nodes

## Estimated Effort

Unknown

## Snowflake (if applicable)

N/A -- this is an AWS Redshift operation.
