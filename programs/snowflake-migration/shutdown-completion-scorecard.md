# Redshift Shutdown Completion Scorecard

**Program:** `snowflake-migration`
**Last Updated:** 2026-09-15
**Target:** $0 Redshift spend ($1,556/day | $10,892/week | $47,225/month | $567K annualized)

**VP Summary:** See [vp-weekly-scorecard.md](vp-weekly-scorecard.md) for the weekly executive update.
**Communication Plan:** See [communication-plan.md](communication-plan.md).
**Jira Issues:** See [tickets/](tickets/) directory.

## Overall: 16% Complete

| Phase | Weight | Status | % Done | Weighted |
|-------|-------:|--------|-------:|--------:|
| Phase 1: Quick Wins | 7% | Assessment done, execution not started | 30% | 2.1% |
| Phase 2: Resize 5→3 | 33% | CloudWatch validated, resize not executed | 20% | 6.6% |
| Phase 3: Pipeline Migration | 15% | ECM in progress, OpenAir blocked | 13% | 2.0% |
| Phase 4: Resize 3→2 | 16% | Blocked on workload reduction | 0% | 0.0% |
| Phase 5: Full Decommission | 29% | Blocked on OpenAir | 0% | 0.0% |
| | | | | **16%** |
| **Savings realized to date** | | | | **$0/day of $1,556** |

Weights are proportional to annualized savings, except Phase 3 which has no direct savings but gates Phases 4 and 5 (assigned 15%, deducted proportionally from 4+5).

---

## Phase 1: Quick Wins (30% complete, weight: 7%)

Savings: ~$105/day | ~$735/week | ~$3,167/month | ~$38K/year. No coordination required.

| Sub-task | Status | Notes |
|----------|--------|-------|
| Identify duplicated Fivetran connectors | Done | 16 of 18 duplicated; 8 safe to pause (RS data orphaned), 8 have active RS consumers |
| Pause 8 orphaned Fivetran connectors | Not started | navan, google_analytics_4, 6x google_drive (no RS consumers) |
| Delete 16 already-paused connectors | Not started | Dead weight cleanup |
| Identify orphaned MV refreshes | Done | 52 orphaned MVs confirmed via stl_scan pipeline |
| Stop 52 orphaned MV refreshes | Not started | ~16K refresh compute-seconds recoverable |
| Identify dormant Overlord jobs | Done | 8 jobs, zero consumers |
| Disable dormant Overlord jobs | Not started | |
| Identify inactive users | Done | ~130 enabled but inactive, 10 already disabled |
| Disable ~130 inactive user accounts | Not started | CONNECTION LIMIT 0, recoverable |
| Build daily monitoring pipeline | Done | Prefect + dbt, stl_scan → Snowflake |

**Scoring:** 5 of 10 sub-tasks complete (all assessment, no execution) = 30% (assessment is necessary but not sufficient -- weighted lower than execution).

---

## Phase 2: Resize 5→3 Nodes (20% complete, weight: 33%)

Savings: $507/day | $3,549/week | $15,400/month | $185K/year. Requires Phase 1 execution + CloudWatch confirmation.

| Sub-task | Status | Notes |
|----------|--------|-------|
| Validate resize feasibility via CloudWatch | Done | Peak CPU 43.5% → ~73% on 3 nodes, safe |
| Execute Phase 1 quick wins (prerequisite) | Not started | Reduces workload, improves safety margin |
| Submit resize request (5→3) | Not started | Elastic resize, ~15 min downtime |
| Validate post-resize stability (24h) | Not started | Monitor CPU, connections, query latency |
| Confirm savings in next billing cycle | Not started | Target: $507/day reduction |

**Scoring:** 1 of 5 sub-tasks complete = 20%.

---

## Phase 3: Pipeline Migration (15% complete, weight: 15%)

No direct savings. Gates Phases 4 and 5.

| Sub-task | Status | Notes |
|----------|--------|-------|
| Map OpenAir reverse ETL dependencies | Done | 23 jobs identified in data_services_etl repo |
| Provision OpenAir non-prod environment | Blocked | Delayed, cross-team dependency |
| Stand up Fivetran OpenAir connector (Snowflake) | Not started | |
| Validate OpenAir data parity | Not started | SOX -- Finance/Accounting sign-off |
| Cut over OpenAir to Snowflake | Not started | Critical path for full shutdown |
| Migrate fivetran_log to Snowflake | Not started | Last RS-exclusive Fivetran connector |
| Pause remaining 8 duplicated Fivetran connectors | Not started | intacct, coupa, zendesk, concur, google_sheets, workramp -- blocked on RS consumer migration |
| Migrate ECM QuickSight datasets | In progress | DNA-6080, Alexandre Cerqueira |
| Complete Overlord strangler pattern | In progress | DNA-6072, per retirement analysis |

**Scoring:** 1 done + 2 in progress out of 9 = 13%.

---

## Phase 4: Resize 3→2 Nodes (0% complete, weight: 16%)

Savings: $253/day | $1,771/week | $7,683/month | $92K/year (incremental over Phase 2). Requires workload reduction.

| Sub-task | Status | Notes |
|----------|--------|-------|
| Reduce peak CPU below 35% (on 5-node baseline) | Not started | Currently 43.5%, needs Phase 1+3 |
| Submit resize request (3→2) | Not started | |
| Validate post-resize stability (24h) | Not started | |
| Confirm savings in next billing cycle | Not started | |

**Scoring:** 0 of 4 = 0%. Blocked on upstream phases.

---

## Phase 5: Full Decommission (0% complete, weight: 29%)

Savings: $601/day | $4,207/week | $18,250/month | $220K/year (remaining compute + storage + snapshots + Fivetran).

| Sub-task | Status | Notes |
|----------|--------|-------|
| Achieve 0 active queries for 7 consecutive days | Not started | Requires OpenAir cutover |
| Terminate Redshift cluster | Not started | |
| Delete snapshots | Not started | |
| Clean up S3 buckets | Not started | 3 buckets identified |
| Remove IAM roles, security groups, VPC endpoints | Not started | |
| Validate $0 Redshift in billing | Not started | |

**Scoring:** 0 of 6 = 0%. Blocked on OpenAir cutover.

---

## How to Update

Re-score after each execution milestone. The percentage reflects actual progress, not planning effort:

- **Assessment tasks** (identify, validate, map): count toward phase completion but are weighted lower than execution
- **Execution tasks** (pause, disable, resize, migrate): full weight
- **Confirmation tasks** (validate stability, confirm billing): ensure savings are real

Update cadence: weekly, or after any phase sub-task completes.

---

## Projection

| Scenario | % Complete | Daily | Weekly | Monthly | Annualized | Timeline Driver |
|----------|----------:|------:|-------:|--------:|-----------:|----------------|
| Phase 1 executed | 37% | $105 | $735 | $3,167 | $38K | No blockers |
| + Phase 2 (resize to 3) | 70% | $612 | $4,284 | $18,567 | $223K | Resize window scheduling |
| + Phase 3 complete | 85% | $612 | $4,284 | $18,567 | $223K | OpenAir cutover (critical path) |
| + Phase 4 (resize to 2) | 91% | $865 | $6,055 | $26,250 | $315K | CPU drops below threshold |
| Phase 5 (full shutdown) | 100% | $1,556 | $10,892 | $47,225 | $567K | 7 days at 0 queries |
