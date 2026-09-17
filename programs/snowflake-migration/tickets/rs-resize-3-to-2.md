# Resize Redshift cluster from 3 to 2 nodes

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Sreehanth Komma
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to resize the cluster from 3 to 2 nodes after consumer workload reduction **so that** we capture an additional $253/day in compute savings.

## Background

2 nodes is not safe at current workload (projected ~109% peak CPU). After Phase 3 consumer cutover reduces the active query volume, peak CPU on 3 nodes should drop. When peak hourly avg CPU on current config falls below 35%, 2 nodes becomes viable (~70% projected).

## Scope

**In scope**
- Monitor daily CloudWatch CPU metrics
- Submit resize when threshold is met
- Post-resize stability monitoring (24h)

**Out of scope**
- Consumer cutover work (separate tickets)

## Inputs

- CloudWatch CPUUtilization metrics
- Daily scan pipeline query volume trends

## Outputs / Deliverables

- Cluster running on 2 nodes
- Post-resize monitoring report

## Acceptance Criteria

1. Peak hourly avg CPU below 35% for 7 consecutive days before resize
2. Post-resize peak CPU stays below 80% for 24 hours
3. No query failures or timeouts

## Definition of Done

- [ ] Threshold confirmed
- [ ] Resize executed
- [ ] 24h monitoring passed
- [ ] Documented

## Dependencies

- Blocked by: Phase 3 consumer cutover (workload reduction)
- Blocking: Phase 5 full shutdown

## Estimated Effort

Unknown
