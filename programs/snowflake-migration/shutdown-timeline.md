# Redshift Shutdown Timeline

**Target:** $0 Redshift by November 1, 2026
**Original Q3 target:** Sept 30 (resize achievable; full shutdown blocked by OpenAir)

---

## Week 1: Sept 15-19 -- Phase 1 Quick Wins

| Action | Owner | Status |
|--------|-------|--------|
| Pause 8 orphaned Fivetran RS connectors (navan, google_analytics_4, 6x google_drive) | Data Platform | Ready |
| Stop 52 orphaned MV refreshes | Data Platform | Ready |
| Disable 8 dormant Overlord jobs (Crunchbase, SPAC, Intelligize, FERC, Lattice, WDATA, CPXDNA) | Data Platform | Ready |
| Disable ~130 inactive user accounts (CONNECTION LIMIT 0) | Data Platform | Ready |

**Savings unlocked:** $105/day | $735/week | $3,167/month

---

## Week 2: Sept 22-26 -- Phase 2 Resize

| Action | Owner | Status |
|--------|-------|--------|
| Submit elastic resize from 5 to 3 nodes | Data Platform | Change window needed |
| Monitor post-resize stability (CPU, connections, query latency) | Data Platform | 24h after resize |

**Additional savings unlocked:** $507/day | $3,549/week | $15,400/month
**Cumulative:** $612/day | $4,284/week | $18,567/month

---

## Weeks 2-3: Sept 22-30 -- ECM QuickSight

| Action | Owner | Status |
|--------|-------|--------|
| Re-point QuickSight datasets to Snowflake (DNA-6080) | Alison Weingarten / Alexandre Cerqueira | In progress |

---

## Weeks 2-4: Sept 22 - Oct 10 -- Consumer Cutover

| Action | Owner | Status |
|--------|-------|--------|
| Run Atlan lineage extraction for all 970 active landing tables | Data Platform | Pipeline built |
| Group remaining consumers by owning team | Data Platform | After lineage |
| Create cutover tickets for each team | Data Platform | After grouping |
| Pause remaining 10 Fivetran connectors (after RS consumers re-pointed) | Data Platform | After cutover |
| Re-point dbt models from Redshift to Snowflake | Data Platform | In progress |
| Track progress via daily scan pipeline | Data Platform | Automated |

---

## Weeks 4-5: Oct 6-17 -- Jira Pipeline

| Action | Owner | Status |
|--------|-------|--------|
| Stand up Jira data pipeline in Snowflake | Data Platform | Not started |
| Validate Jira data parity | Data Platform | After build |
| Disable Overlord Jira jobs | Data Platform | After validation |

---

## Weeks 5-7: Oct 13-31 -- OpenAir Cutover (Critical Path)

| Action | Owner | Status |
|--------|-------|--------|
| Provision OpenAir non-prod environment | CPX / BizTech | Delayed |
| Stand up Fivetran OpenAir connector targeting Snowflake | Data Platform | Not started |
| Validate parity with 23 existing Overlord sync jobs | Data Platform / Finance | SOX |
| Get Finance/Accounting sign-off | Finance | Required |
| Disable Overlord OpenAir jobs | Data Platform | After sign-off |

**Risk:** SOX compliance and cross-team coordination could push this past October.

---

## Late October -- Phase 4 Resize

| Action | Owner | Trigger |
|--------|-------|---------|
| Resize from 3 to 2 nodes | Data Platform | Peak hourly avg CPU drops below 35% |
| Monitor post-resize stability | Data Platform | 24h after resize |

**Additional savings:** $253/day | $1,771/week | $7,683/month

---

## November 1 Target -- Phase 5 Full Shutdown

**Prerequisites:** OpenAir cutover complete AND FedRAMP boundary change accepted.

| Action | Owner | Trigger |
|--------|-------|---------|
| FedRAMP boundary change accepted by Tennessee Valley Authority | Security / Compliance | Acceptance not yet received |
| Confirm 0 active queries for 7 consecutive days | Data Platform | Daily scan pipeline |
| Terminate Redshift cluster | Data Platform | After 7-day confirmation + FedRAMP acceptance |
| Delete snapshots | Data Platform | After termination |
| Clean up S3 buckets, IAM roles, security groups, VPC endpoints | Data Platform | After termination |
| Validate $0 Redshift in next billing cycle | Data Platform / FinOps | Next invoice |

**Final savings:** $1,556/day | $10,892/week | $47,225/month

---

## Risk Summary

| Risk | Impact | Mitigation |
|------|--------|------------|
| OpenAir SOX sign-off delays | Pushes full shutdown past October | Does NOT block resize; escalate through Finance |
| FedRAMP boundary change not accepted | Cannot terminate cluster | Tennessee Valley Authority must accept removal of Redshift from boundary; escalate through Security/Compliance |
| Jira pipeline build takes longer than 3-4 weeks | Delays Overlord Jira decommission | Start immediately, parallelize with consumer cutover |
| Unknown consumers discovered during lineage extraction | Additional cutover work | Daily scan pipeline will surface them |
| Resize causes performance issues | Rollback to 5 nodes | Elastic resize is reversible in ~15 min |
