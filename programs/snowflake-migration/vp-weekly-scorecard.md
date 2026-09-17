# Redshift Shutdown -- Weekly Scorecard

**Week of:** September 15, 2026
**Target:** $0 Redshift by November 1, 2026
**Status:** At Risk (assessment complete, execution starting)

---

## Key Metrics

| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| **% Complete** | 16% | 100% | -- |
| **Weekly Savings Realized** | $0 / wk | $10,892 / wk | -- |
| **Redshift Queries / Day** | ~152K | 0 | Flat |
| **Cluster Nodes** | 5 | 0 | No change |
| **Active Landing Tables** | 970 | 0 | -- |
| **Orphaned Objects Removed** | 0 / 166 | 166 / 166 | -- |

---

## Phase Status

| Phase | Status | Update |
|-------|--------|--------|
| 1. Quick Wins | Ready | 8 Fivetran connectors, 52 orphan MVs, 8 Overlord jobs, ~130 users identified. Execution this week. |
| 2. Resize 5 to 3 | Ready | CloudWatch confirms safe (43.5% peak CPU). Change window next week. |
| 3. Consumer Cutover | In Progress | Lineage pipeline built and demonstrated. ECM QuickSight (DNA-6080) in progress. 10 Fivetran schemas still have active RS consumers. |
| 4. Resize 3 to 2 | Blocked | Requires peak CPU below 35%. Depends on Phase 3 workload reduction. |
| 5. Full Shutdown | Blocked | Requires OpenAir cutover (SOX) + FedRAMP boundary acceptance from Tennessee Valley Authority. |

---

## Blockers

| Blocker | Owner | Next Action | ETA |
|---------|-------|-------------|-----|
| **OpenAir reverse ETL** (SOX, 23 jobs) | CPX / BizTech / Finance | Provision non-prod environment | End of Oct |
| **FedRAMP boundary change** (Tennessee Valley Authority) | Security / Compliance | Obtain acceptance of Redshift removal | TBD |
| **Jira pipeline missing in Snowflake** | Data Platform | Stand up ASSET/INV pipeline | 3-4 weeks |
| **ECM QuickSight datasets** (DNA-6080) | Alison Weingarten | Re-point datasets to Snowflake | End of Sept |

---

## Next Week

- Execute Phase 1: pause 8 Fivetran connectors, stop 52 orphan MVs, disable dormant Overlord jobs and inactive users
- Submit cluster resize from 5 to 3 nodes (change window)
- Run Atlan lineage extraction for all 970 active landing tables
- Begin grouping remaining consumers by owning team

---

*Updated by Dean McCall. Detailed data in `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY`.*
