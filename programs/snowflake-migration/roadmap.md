# Complete Snowflake Migration

**Slug:** `snowflake-migration`
**Period:** 2026 H2
**Goal:** Deliver a modernized Enterprise Data Platform
**Owner:** Dean McCall
**RICE:** R=5, I=5, C=5, E=5 (SUM=20)
**Source:** `shared/data/dna-roadmap.xlsx` tab `DnA_H226` row 5

## Q3 Scope

* Phase out Redshift consumption, redirect remaining downstream dependencies to Snowflake, and execute a controlled infrastructure teardown.
* Weekly reporting of Redshift data consumption.

**Targets:**
* 0 active queries running on Redshift by end of August.
* 100% decommissioning of Redshift clusters by end of Q3.
* $0 ongoing Amazon Redshift Infrastructure spend in Q4.

## Q4 Scope

No Q4 scope defined -- method completes in Q3.

## Resource Allocations

| Person | Allocation |
|--------|-----------|
| Derek Veroff (Sr. Data Platform Engineer) | 0.1 |
| Lincoln Lopes Silva (Data Engineer Contractor) | 0.75 |
| Sreekanth Komma (Staff Data Platform and AI Engineer Contractor) | 1.0 |
| Daniel Petty | 0.1 |
| Yao Wang | 0.5 |
| Alexandre Cerqueira (Critical River) | 1.0 |
| Diego Arguello (Critical River) | 1.0 |

Note: Yao Wang, Alexandre Cerqueira, and Diego Arguello are in Alison Weingarten's org (stakeholder scope). They appear on the H2 sheet allocation grid but are not assignable capacity in Dean's org per `shared/org.md`.

## Stakeholders

Sales, Product, CPX, Marketing, Engineering, Growth, Corp Ops, Finance, P&C, Security, Legal, BT-Foundation

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-31 | **At Risk** | August zero-query target missed. Revised: 0 active queries by mid-September, cluster decommission by end of Q3. |
| 2026-09-15 | **At Risk** | Sept 15 assessment: 22 active users (down from 36), but ~100K queries/day flat due to automated workloads. MV refreshes consume 375 compute-hours/wk. 16/18 Fivetran connectors duplicated in Snowflake. Phased shutdown plan created. OpenAir remains critical-path blocker for full decommission. Cluster resize (5 to 2 nodes, $760/day savings) achievable after quick wins + MV migration. See `redshift-shutdown-plan.md`. |

### Risks (as of 2026-09-15)

1. **OpenAir dependency:** SOX-compliant, revenue-impacting. 23 bidirectional sync jobs still running via datasciadmin (12,488 queries/wk, 4.3 runtime hours). Non-prod env provisioning delayed. Cross-team (CPX, BizTech, Finance). Most likely to push past Q3.
2. **Materialized views:** `mv_spectrum.*` consumes 375 compute-hours/week -- largest single workload on the cluster. Must be migrated or disabled before cluster resize is viable.
3. **ECM dashboards:** QuickSight datasets still reading from Redshift (~11,900 queries/wk). DNA-6080 in progress (Alexandre Cerqueira).
4. **Resource gap:** Lincoln Lopes Silva was unavailable for 2 weeks, reducing migration velocity during a critical window.

### Path to Green

- **Phase 1 (immediate):** Pause 16 duplicated Fivetran connectors, disable inactive users, kill dormant Overlord jobs.
- **Phase 2:** Migrate or disable `mv_spectrum.*` materialized views (375 compute-hours/week).
- **Phase 3:** Migrate fivetran_log, ECM QuickSight datasets, OpenAir cutover.
- **Phase 4:** Resize cluster 5 to 2 nodes ($760/day savings, $277K annualized).
- **Phase 5:** Full decommission after OpenAir clears ($1,466/day total, $535K annualized).
- See `redshift-shutdown-plan.md` for full assessment and execution details.

## Mapping

Jira: No epic linked on H2 sheet. Related active issues:
- DNA-6072: Map unused Redshift pipeline outputs (Shobhit Pandey, In Progress)
- DNA-5454: Migrate suv_account_opportunity (Diego Arguello, Blocked)
- DNA-6080: QuickSight datasets failing to refresh (Alexandre Cerqueira, In Progress)
