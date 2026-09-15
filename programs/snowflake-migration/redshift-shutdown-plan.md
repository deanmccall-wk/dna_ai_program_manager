# Redshift Graceful Shutdown Plan

**Program:** `snowflake-migration`
**Created:** 2026-09-15
**Owner:** Dean McCall
**Status:** Assessment complete, ready for execution

## Current State (Sept 15 snapshot)

### Workload summary

| Metric | Aug 31 Baseline | Sept 15 Current | Delta |
|--------|----------------:|----------------:|------:|
| Active users (7-day) | 36 | 22 | -39% |
| Queries/day | ~97,000 | ~100,000 | Flat |
| Distinct users/day | 22 | 18-20 | -9% to -14% |
| Disabled users | 10 | 10 | No change |

Query volume has not dropped despite fewer users because automated processes (Fivetran, dbt, Overlord) dominate the workload.

### Query volume by workload (last 7 days)

| Workload | Queries | % | Runtime Hours | Key Users |
|----------|--------:|--:|-------------:|-----------|
| datasciadmin (Overlord + MV refresh) | 412,454 | 57.7% | 434.6 | `datasciadmin` |
| dbt | 138,800 | 19.4% | 867.1 | `service_dbt` |
| Fivetran | 124,431 | 17.4% | 30.3 | `service_fivetran` |
| Amplitude | 10,599 | 1.5% | 5.1 | `service_amplitude` |
| QuickSight | 11,902 | 1.7% | 61.2 | `service_qs_*` |
| Security monitoring (InfoSec) | 7,406 | 1.0% | 3.0 | `service_security` -- runs until cluster off, exclude from orphan analysis |
| WDC / Chains | 1,499 | 0.2% | 7.8 | `service_wdc_*` |
| Atlan | 2,375 | 0.3% | 2.3 | `service_atlan` |

**Note:** InfoSec processes (`service_security`, `info_sec.workday_worker`) run until the cluster is turned off. They are excluded from orphan analysis and do not need separate decommission -- they simply stop when the cluster stops.
| Other (human users) | 5,463 | 0.8% | 6.9 | shobhitpandey, deanmccall, etc. |
| **Total** | **714,929** | | **1,418.3** | **22 active users** |

### datasciadmin deep dive (57.7% of all queries)

`datasciadmin` is a shared service account running Overlord ETL and materialized view refreshes:

| Category | Queries | Runtime Hours | Notes |
|----------|--------:|-------------:|-------|
| MV refresh (Spectrum) | 31,324 | **374.9** | Largest compute consumer. Refreshes `mv_spectrum.workiva_filing`, `workiva_workspace`, `workiva_organization`, `workiva_role_assignment` |
| Insights Analytic | 93,016 | 18.2 | Reads from `insights_analytic` schema |
| Staging loads | 17,304 | 26.5 | Overlord writing to staging tables |
| OpenAir ETL | 12,488 | 4.3 | OpenAir-Salesforce sync jobs |
| Overhead/healthcheck | 133,257 | 2.2 | SELECT 1, pg_last_query_id, catalog queries |
| Transaction control | 110,236 | 2.9 | BEGIN, COMMIT, ROLLBACK |
| Other | 14,526 | 5.5 | Miscellaneous |

**Key finding:** Materialized view refreshes consume 375 hours/week of compute -- more than all other workloads combined. These views read from Spectrum (S3) and are the primary driver of both compute utilization and Spectrum cost ($149/day).

### Cluster configuration and cost

| Component | Daily Cost | Monthly | Annualized | Type |
|-----------|----------:|--------:|-----------:|------|
| Compute (5 x ra3.16xlarge) | $1,267 | $38,500 | $462,500 | Fixed |
| Spectrum (S3 data scanned) | $149 | $4,500 | $54,400 | Variable (per query) |
| Managed Storage (RMS) | $41 | $1,250 | $15,000 | Fixed until terminated |
| Snapshots | $9 | $275 | $3,300 | Fixed until deleted |
| Concurrency Scaling | $0 | $0 | $0 | Was $8-13K/mo in Q1, already $0 since Aug |
| **Total AWS** | **$1,466** | **$44,525** | **$535,200** | |
| Fivetran MAR (RS destination) | ~$90 | ~$2,700 | ~$32,400 | Variable |
| **Grand Total** | **$1,556** | **$47,225** | **$567,600** | |

### Fivetran connector inventory (Redshift destination)

34 total connectors: 18 active, 16 paused.

**16 of 18 active connectors are already duplicated in Snowflake (BT_FIVETRAN_PROD):**

| Service | RS Connector | SF Equivalent | Sync Freq |
|---------|-------------|---------------|-----------|
| sage_intacct | staging_intacct | intacct | Daily |
| navan | staging_navan | navan | Daily |
| coupa | staging_coupa | coupa | Daily |
| google_drive (x6) | staging_google_drive.* | google_drive | 2-6hr |
| zendesk | staging_zendesk | zendesk | Daily |
| google_analytics_4 | staging_google_analytics | google_analytics | Daily |
| concur | staging_concur | concur | Daily |
| google_sheets (x3) | staging_google_sheets.* | google_sheets.* | 6hr |
| workramp | staging_workramp | workramp | Daily |

**2 Redshift-exclusive connectors:**

| Connector | Purpose | Sync Freq | Action |
|-----------|---------|-----------|--------|
| fivetran_log | Platform Connector (usage, MAR, connector metadata) | 15 min | Migrate to Snowflake |
| fivetran_metadata | Platform metadata | Daily | Bundle with fivetran_log migration |

**16 already-paused connectors** (dead weight, can be deleted):
Workday HCM, Genesys, AWS Cost Report, Marketo (broken), Gainsight (x2), Sage Intacct Resolve, Smartsheet (incomplete), Xactly, Skilljar (broken), Google Sheets (x4), Google Drive SPP.

### User account status

| Category | Count |
|----------|------:|
| Already disabled (CONNECTION LIMIT 0) | 10 |
| Active in last 7 days | 22 |
| Enabled but inactive (>7 days) | ~130 |
| Total user accounts | ~162 |

**Already disabled (10):** ben.heller, bert.vanessen (x3), max.gregson, service_qs_cpxdna_read, service_wdc_cpx_dna_read, service_wdc_deloitte_eu, ty.sanders (x2).

**Active but candidates for disable** (no queries or only overhead in last 7 days):
- solomon.jehuappiah (8 queries) -- confirm with owner
- yao.wang (20 queries) -- stakeholder, coordinate before disabling

### Overlord dormant jobs (zero consumers, per existing analysis)

| Source | Schema | Tables | Last Altered | Action |
|--------|--------|-------:|-------------|--------|
| Crunchbase / SPAC | OTHER.SPAC_EVENT | 1 | Sep 2026 (hourly) | Decommission -- loaded hourly, zero consumers |
| Intelligize | OTHER.INTELLIGIZE_* | 2 | Jul 2026 | Decommission -- 0 rows in tables |
| FERC | OTHER.FERC_FILING | 1 | Jul 2026 | Decommission -- no consumers |
| Lattice | OTHER.LATTICE_SF_LEAD_RATING | 1 | Jul 2026 | Decommission -- no consumers |
| WDATA | WDATA.SEC_FILING | 1 | Feb 2026 | Decommission -- 0 queries in 90 days |
| CPXDNA | OTHER.CPXDNA_* | 2 | May 2026 | Confirm with CPX, then decommission |

### Orphaned materialized views (confirmed via full dependency chain)

49 views outside `mv_spectrum` reference `mv_spectrum` views in their definitions. Of those, 22 have active downstream consumers and 9 are dormant. Tracing the full chain (MV refresh -> dependent view -> end consumer) confirms:

- **20 mv_spectrum views are needed** (feed 22 active dependent views)
- **~150 mv_spectrum views are orphaned** (no downstream consumers anywhere in the chain)

| Group | Views | Weekly Refreshes | Weekly Runtime | Status |
|-------|------:|----------------:|---------------:|--------|
| Orphaned (no consumers in chain) | ~150 | 11,235 | **181.3 hrs** | Safe to stop |
| Needed (feed active views) | 20 | 202 | 0.9 hrs | Keep refreshing |
| STV_MV_INFO checks (all views) | ~170 | 19,883 | ~193 hrs | Drops proportionally |
| **Orphaned total (refresh + checks)** | | **~30K** | **~370 hrs** | |

The 20 needed mv_spectrum views and their downstream consumers:

| mv_spectrum view | Consumer view | Category |
|-----------------|--------------|----------|
| oa_deleted_booking | public.openair_booking (1,712 reads) | OpenAir |
| oa_deleted_customer | public.openair_customer (3,593 reads) | OpenAir |
| oa_deleted_project | public.openair_project (5,516 reads) | OpenAir |
| oa_deleted_projectbillingrule | public.openair_projectbillingrule (1,627) | OpenAir |
| oa_deleted_projecttask | public.openair_projecttask (120) | OpenAir |
| oa_deleted_task | public.openair_task (148) | OpenAir |
| oa_deleted_timesheet | public.openair_timesheet (127) | OpenAir |
| oa_deleted_slip | public.openair_slip (14) | OpenAir |
| oa_deleted_budget | public.openair_budget (170) | OpenAir |
| oa_deleted_user | public.openair_user (2,117) | OpenAir |
| wkdy_transform | info_sec.workday_worker (996), sensitive.workday_worker (996) | Workday / InfoSec -- runs until cluster off |
| mk_program | marketo.program (1,373) | Marketo |
| sf_dnboptimizer__dnbcompanyrecord__c | public.salesforce_dnb_company_record (14) | Salesforce |
| sf_task_type__c | public.salesforce_task_type (28) | Salesforce |
| wdesksheet_sales_forecast | salesops.sales_forecast (7) | Sales Ops |
| gn_nxt_scoring_scheme_definition | gainsight.scoring_scheme_definition (14) | Gainsight |
| walkme_survey_analysis_export | sensitive.walkme_survey_analysis_export (7) | WalkMe |
| zd_ticket_fields | public.zendesk_ticket_field (2) | Zendesk |
| refinitiv_ratios_report | public.refinitiv_ratios_report (2) | Refinitiv |
| spac_company | public.spac_company (7) | Crunchbase |

Note: 10 of the 20 needed views are OpenAir `oa_deleted_*` views. Once the OpenAir cutover to Snowflake is complete, these become orphaned too -- reducing the needed set to ~10 views.

The `mv_user_analytic` schema (2,277 views) has only 15 reads and 1 refresh in 7 days. Essentially dormant.

### Blockers

**OpenAir (critical path):**
- 23 bidirectional Salesforce-OpenAir sync jobs running via `datasciadmin`
- SOX-compliant, revenue-impacting -- Finance/Accounting sign-off required
- 12,488 queries and 4.3 runtime hours in last 7 days
- Cross-team dependency: CPX, BizTech, Accounting/Finance
- Non-prod environment provisioning was delayed
- **This is the item most likely to push past Q3**

**ECM dashboards:**
- QuickSight datasets still reading from Redshift (DNA-6080 in progress)
- ~11,900 QuickSight queries in last 7 days across service_qs_* accounts
- Alison Weingarten's team owns the migration

**Materialized views (newly identified):**
- `mv_spectrum.*` views consuming 375 runtime hours/week
- These are the largest single compute consumer on the cluster
- Must be replaced or disabled before cluster can be resized

---

## Shutdown Phases

### Phase 1: Quick Wins (no risk, immediate)

**1a. Pause 16 duplicated Fivetran connectors**
- All 16 have identical connectors running in Snowflake
- Removes 124,431 queries/week (17.4% of volume) and 30 runtime hours
- Saves ~$2,700/mo Fivetran MAR fees for Redshift destination
- Saves ~$15-30/day Spectrum cost

**1b. Delete 16 paused Fivetran connectors**
- Already paused, no impact. Clean up dead weight.

**1c. Disable dormant Overlord jobs**
- 8 jobs with zero consumers (Crunchbase, SPAC, Intelligize, FERC, Lattice, WDATA, CPXDNA)
- Reduces datasciadmin staging load volume

**1d. Disable ~130 inactive user accounts**
- Set `CONNECTION LIMIT 0` for all users with no activity in 30+ days
- Scream test showed this approach is recoverable
- 10 users already disabled with no reported breakage

### Phase 2: Stop Orphaned Materialized View Refreshes (highest compute impact)

~150 of ~170 `mv_spectrum` views have no downstream consumers (confirmed by tracing the full dependency chain: MV -> dependent view -> end consumer). Stopping their refresh eliminates ~370 compute-hours/week.

**Action:** Disable the refresh scheduler for the ~150 orphaned views. Keep refreshes running for 20 views that feed active dependent views (primarily OpenAir, Workday, Marketo, Salesforce).

No pipeline migration or cross-team coordination required. Once OpenAir migrates to Snowflake, 10 more views (the `oa_deleted_*` set) become orphaned too.

### Phase 3: Pipeline Migration

**3a. Migrate fivetran_log to Snowflake**
- Add fivetran_log connector to BT_FIVETRAN_PROD destination
- Update `lib/fivetran.py` to query Snowflake
- Last Redshift-exclusive Fivetran connector

**3b. OpenAir cutover** (blocker -- requires cross-team coordination)
- Stand up Fivetran OpenAir connector targeting Snowflake
- Validate parity with existing Overlord jobs
- Get Finance/Accounting sign-off (SOX)
- Disable Overlord OpenAir jobs

**3c. ECM QuickSight migration** (DNA-6080)
- Re-point QuickSight datasets to Snowflake data sources
- Coordinate with Alison Weingarten's team

**3d. Complete Overlord strangler pattern**
- Per overlord-retirement analysis: Fivetran for 15 sources, shares for 7, custom for 11

### Phase 4: Cluster Resize (5 to 2 nodes)

**Prerequisites:** Phases 1-2 complete, Phase 3a-3c in progress.

| Metric | Before | After | Savings |
|--------|-------:|------:|--------:|
| Compute/day | $1,267 | $507 | $760/day |
| Compute/month | $38,500 | $15,400 | $23,100/mo |
| Compute/year | $462,500 | $185,000 | $277,500/yr |

### Phase 5: Full Decommission

**Prerequisites:** 0 active queries for 7 consecutive days (requires OpenAir cleared).

1. Terminate Redshift cluster
2. Delete snapshots
3. Clean up S3 buckets (ito-ds-redshift-us-east-1, audit log, itz-ds-redshift-us-east-1)
4. Remove IAM roles, security groups, VPC endpoints
5. Validate $0 Redshift in next billing cycle

**Total savings: $1,466/day AWS + $90/day Fivetran = $567K annualized.**

---

## Savings Summary

| Milestone | Action | Daily Savings | Annualized |
|-----------|--------|-------------:|-----------:|
| Phase 1 | Pause Fivetran duplicates | ~$105 (Spectrum + Fivetran MAR) | ~$38K |
| Phase 2 | Stop 168 orphaned MV refreshes | ~$100 (Spectrum) | ~$36K |
| Phase 4 | Cluster resize (5 to 2 nodes) | $760 (compute) | $277K |
| Phase 5 | Full shutdown | $501 (remaining compute + storage + snapshots) | $183K |
| | **Cumulative** | **$1,466** | **$535K AWS + $32K Fivetran = $567K** |

---

## Related Artifacts

- Workload analysis: `~/Documents/dna_ai_analyst/analyses/ad-hoc/2026-08-05-redshift-workloads/`
- Scream test: `~/Documents/dna_ai_analyst/analyses/ad-hoc/2026-08-11-redshift-scream-test/`
- Overlord retirement: `~/Documents/dna_ai_analyst/analyses/ad-hoc/2026-09-09-overlord-retirement/`
- Cost data: `~/Documents/dna_ai_finops/reports/executive_summary_ytd_2026.md`
- Jira: DNA-5930, DNA-6072, DNA-6080, DNA-5454
