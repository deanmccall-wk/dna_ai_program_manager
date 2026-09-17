# Redshift Graceful Shutdown Plan

**Program:** `snowflake-migration`
**Created:** 2026-09-15
**Last Updated:** 2026-09-15
**Owner:** Dean McCall
**Status:** Assessment complete, ready for execution

---

## Current State (Sept 15)

### Cluster

| Attribute | Value |
|-----------|-------|
| Cluster ID | `ito-ds-redshift-dsredshift-kfbgevo589gl` |
| Node type | ra3.16xlarge |
| Node count | 5 |
| Status | available |
| Disk used | 10.5% (not a constraint) |
| 7-day peak hourly avg CPU | 43.5% |
| 7-day peak connections | 123 |

### Daily cost

| Component | Daily | Monthly | Annualized | Type |
|-----------|------:|--------:|-----------:|------|
| Compute (5 x ra3.16xl) | $1,267 | $38,500 | $462,500 | Fixed |
| Spectrum (S3 scans) | $149 | $4,500 | $54,400 | Variable per query |
| Managed Storage (RMS) | $41 | $1,250 | $15,000 | Fixed until terminated |
| Snapshots | $9 | $275 | $3,300 | Fixed until deleted |
| Concurrency Scaling | $0 | $0 | $0 | Was $8-13K/mo in Q1, $0 since Aug |
| **Total AWS** | **$1,466** | **$44,525** | **$535,200** | |
| Fivetran MAR (RS dest) | ~$90 | ~$2,700 | ~$32,400 | Variable |
| **Grand Total** | **$1,556** | **$47,225** | **$567,600** | |

### Active consumers (DNA team personal accounts excluded)

19 non-DNA service accounts and 2 non-DNA humans. All query activity is automated:

| User | Queries (7d) | Category |
|------|-------------:|----------|
| datasciadmin | 412,624 | Overlord ETL + MV refreshes |
| service_dbt | 138,800 | dbt Cloud pipelines |
| service_fivetran | 124,431 | Fivetran (16/18 duplicated in Snowflake) |
| service_amplitude | 10,596 | Amplitude analytics |
| service_qs_salesops | 7,513 | QuickSight Sales Ops |
| service_security | 7,406 | InfoSec monitoring (runs until cluster off) |
| service_salesops_sensitive_read | 3,673 | Sales Ops |
| service_atlan | 2,375 | Atlan catalog crawl |
| service_qs_public_read | 2,265 | QuickSight public |
| service_qs_sensitive_read | 2,040 | QuickSight sensitive |
| service_wdc_public_read | 1,188 | WDC / Chains |
| Other service accounts | 781 | service_ae, service_bigquery, wdc, qs |
| yao.wang | 20 | Stakeholder (non-DNA) |
| solomon.jehuappiah | 8 | Non-DNA human |

### Orphan analysis (stl_scan based)

Built via Prefect + dbt pipeline. Source: `stl_scan` aggregated by (scan_date, perm_table_name, username), loaded to `GOLD_DEV.DATA_PLATFORM.RAW_REDSHIFT_SCANS`, classified via dbt with `dim_workers` join for DNA team exclusion.

**Data tables:** `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY`, `REDSHIFT_MV_PRIORITIZATION`

| Classification | Objects | Consumer Queries |
|----------------|--------:|-----------------:|
| Orphan (0 consumer scans) | 512 | 0 |
| Low activity (1-10 scans) | 27,771 | 69,773 |
| Active (>10 scans) | 1,858 | 898,364 |

### 52 orphaned materialized views (stl_scan confirmed)

| Source | Orphaned MVs | Names |
|--------|-------------:|-------|
| OpenAir | 16 | oa_projectbillingrule, oa_hierarchynode, oa_bookingtype, oa_budget, oa_ratecard, oa_category, oa_hierarchy, oa_filterset, oa_slip, oa_slipstage + 6 oa_deleted_* |
| Zendesk | 10 | zd_conversation_log, zd_badge_categories, zd_omnichannel_engagements, zd_badges, zd_article_subscriptions, zd_queue_events, zd_translation, zd_voice_calls, zd_article_vote |
| Salesforce | 8 | sf_booking__c, sf_sec_filing__c, sf_goodwill_reserve__c, sf_opportunityhistory, sf_skilljar_student, sf_note, sf_partner_relationship_product, sf_lead, sf_cloud_contact__c, sf_contact |
| Gainsight | 5 | gn_nxt_call_to_action, gn_nxt_survey_cs_complete_csat_00189, gn_nxt_internal_post_partner_implementation, gn_nxt_graduation_survey, gn_nxt_survey_product_success_rnps |
| Workday/WalkMe/Wdesk | 3 | wkdy_rest_worker_time_off_entries, wdesksheet_corporate_plans_solution, walkme_survey_analysis_export |
| SEC/EDGAR/NASDAQ | 3 | bq_ixbrl_facts, edgar_company, nasdaq_ipo_calendar |
| Jira | 2 | jira_dna, jira_spp |
| Atlan | 1 | atlan_user_analytic_query |

Note: Earlier text-match analysis (sys_query_history) incorrectly classified ~150 MVs as orphaned. The stl_scan analysis corrected this to 52 -- many MVs have active consumers through intermediate views that text matching missed.

### Fivetran connector inventory

| Status | Count | Action |
|--------|------:|--------|
| Active, duplicated + orphaned in RS | 8 | Safe to pause now (navan, google_analytics_4, 6x google_drive) |
| Active, duplicated but RS data has consumers | 8 | Pause after RS consumers migrate (intacct, coupa, zendesk, concur, 3x google_sheets, workramp) |
| Active, Redshift-exclusive | 2 | fivetran_log + fivetran_metadata -- migrate to Snowflake |
| Already paused | 16 | Delete |

Duplication in Snowflake is necessary but not sufficient. The Redshift staging tables must also be orphaned (no active non-Fivetran consumers in stl_scan). Of the 16 duplicated connectors, 8 still feed active dbt, QuickSight, WDC, or Overlord consumers in Redshift:

| Schema | Non-FT Consumers | Queries (10d) | Key Consumers |
|--------|:----------------:|--------------:|---------------|
| staging_coupa | 13 | 95,401 | service_dbt, service_qs_*, datasciadmin, service_bigquery |
| staging_concur | 8 | 39,189 | service_dbt, service_qs_*, datasciadmin, service_wdc_* |
| staging_zendesk | 8 | 38,909 | service_dbt, service_qs_*, datasciadmin, service_wdc_* |
| staging_workramp | 2 | 392 | service_dbt, service_wdc_sensitive_read |
| staging_intacct | 3 | 103 | datasciadmin, service_dbt, service_qs_restricted_read |
| staging_google_sheets | 1 | 16 | service_dbt |
| staging_navan | 0 | 0 | -- |
| staging_google_analytics | 0 | 0 | -- |
| staging_google_drive | 0 | 0 | -- |

### Blockers

**OpenAir (critical path for full shutdown):**
- 23 bidirectional Salesforce-OpenAir sync jobs in `data_services_etl` repo
- 12 upload to OpenAir, 11 upload to Salesforce
- SOX-compliant, revenue-impacting -- Finance/Accounting sign-off required
- Cross-team: CPX, BizTech, Accounting/Finance
- Source tables: `public.openair_*` views reading from `mv_spectrum.oa_*` MVs
- Does not block cluster resize -- only blocks full shutdown

**ECM dashboards:**
- QuickSight datasets still reading from Redshift (DNA-6080 in progress)
- Alison Weingarten's team owns migration

---

## Shutdown Phases

### Phase 1: Quick Wins (no risk, no coordination)

**1a. Pause 8 Fivetran connectors (duplicated in Snowflake AND orphaned in Redshift)**
- navan, google_analytics_4, 6x google_drive
- No non-Fivetran consumers reading from these Redshift staging tables
- Saves partial Fivetran MAR

**1b. Stop 52 orphaned MV refreshes**
- Confirmed orphaned via stl_scan (0 consumer scans in 10-day window)
- Total refresh cost is ~4.4 compute-hours/10 days
- No downstream impact

**1c. Delete 16 already-paused Fivetran connectors**
- Dead weight cleanup

**1d. Disable dormant Overlord jobs**
- 8 jobs with zero consumers (Crunchbase, SPAC, Intelligize, FERC, Lattice, WDATA, CPXDNA)

**1e. Disable ~130 inactive user accounts**
- CONNECTION LIMIT 0 (recoverable)
- 10 already disabled with no breakage

### Phase 2: Cluster Resize (5 to 3 nodes)

**CloudWatch data supports an immediate resize from 5 to 3 nodes:**

| Metric | 5 nodes (current) | 3 nodes (projected) | Threshold |
|--------|-------------------:|--------------------:|-----------|
| Peak hourly avg CPU | 43.5% | ~73% | <80% safe |
| Disk used | 10.5% | 10.5% (RA3 shared) | Not a constraint |
| Peak connections | 123 | 123 (no change) | Not a constraint |

**2 nodes is not safe yet** -- projected peak CPU would be ~109%. Requires workload reduction from Phase 1 + Phase 3 first. Track peak hourly avg CPU: when it drops below 35% on current config, 2 nodes becomes viable.

| | Before | After Resize | Savings |
|---|-------:|------------:|--------:|
| Compute/day | $1,267 | $760 | **$507/day** |
| Compute/month | $38,500 | $23,100 | **$15,400/mo** |
| Compute/year | $462,500 | $277,500 | **$185,000/yr** |

### Phase 3: Pipeline Migration (coordination required)

**3a. Migrate fivetran_log to Snowflake**
- Add fivetran_log connector to BT_FIVETRAN_PROD
- Update `lib/fivetran.py` to query Snowflake
- Last Redshift-exclusive Fivetran connector

**3b. Pause remaining 8 duplicated Fivetran connectors**
- intacct, coupa, zendesk, concur, 3x google_sheets, workramp
- Blocked: RS staging tables still have active dbt/QuickSight/Overlord consumers
- Pause after those consumers migrate to Snowflake equivalents

**3c. ECM QuickSight migration** (DNA-6080)
- Re-point QuickSight datasets to Snowflake
- Coordinate with Alison Weingarten's team

**3d. OpenAir cutover** (critical path for full shutdown)
- Stand up Fivetran OpenAir connector targeting Snowflake
- Validate parity with existing Overlord jobs (23 reverse ETL jobs)
- Get Finance/Accounting sign-off (SOX)
- Disable Overlord OpenAir jobs

**3e. Complete Overlord strangler pattern**
- Per overlord-retirement analysis: Fivetran for 15 sources, shares for 7, custom for 11

### Phase 4: Resize to 2 nodes (after workload drops)

After Phase 1 + 3 reduce peak CPU below 35%, resize from 3 to 2 nodes.

Additional savings: $253/day ($92K annualized) beyond Phase 2.

### Phase 5: Full Decommission

**Prerequisites:** 0 active queries for 7 consecutive days. OpenAir cutover complete.

1. Terminate Redshift cluster
2. Delete snapshots
3. Clean up S3 buckets (ito-ds-redshift-us-east-1, audit log, itz-ds-redshift-us-east-1)
4. Remove IAM roles, security groups, VPC endpoints
5. Validate $0 Redshift in next billing cycle

---

## Savings Summary

| Phase | Action | Daily Savings | Annualized |
|-------|--------|-------------:|-----------:|
| Phase 1 | Quick wins (Fivetran + orphan MVs + inactive users) | ~$105 | ~$38K |
| Phase 2 | Resize 5 to 3 nodes | $507 | $185K |
| Phase 4 | Resize 3 to 2 nodes (after workload drop) | $253 | $92K |
| Phase 5 | Full shutdown | $601 (remaining) | $220K |
| | **Cumulative** | **$1,466 AWS + $90 Fivetran** | **$567K** |

---

## Monitoring

### Daily pipeline (built)

`./run.sh pipeline` extracts stl_scan + object inventory from Redshift, loads to Snowflake, runs dbt classification models.

- `GOLD_DEV.DATA_PLATFORM.RAW_REDSHIFT_SCANS` -- append-only scan data
- `GOLD_DEV.DATA_PLATFORM.RAW_REDSHIFT_OBJECTS` -- object inventory
- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY` -- classified objects
- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_MV_PRIORITIZATION` -- MVs ranked by compute cost

### CloudWatch (validated)

AWS CloudWatch API provides cluster-level metrics without Redshift connection:
- `CPUUtilization` -- resize trigger: peak hourly avg <35% enables 2-node resize
- `DatabaseConnections` -- trending to 0 confirms shutdown readiness
- `PercentageDiskSpaceUsed` -- not a constraint (10.5%)

### Resize decision rule

| Peak Hourly Avg CPU (5 nodes) | Safe Target | Savings |
|-------------------------------:|------------:|--------:|
| <50% (current: 43.5%) | 3 nodes | $185K/yr |
| <35% | 2 nodes | $277K/yr |
| ~0% for 7 days | Terminate | $535K/yr |

---

## Related Artifacts

- Scan inventory pipeline: `pipelines/redshift_scan_pipeline.py`
- dbt models: `dbt/models/` (staging, intermediate, marts)
- Workload analysis: `~/Documents/dna_ai_analyst/analyses/ad-hoc/2026-08-05-redshift-workloads/`
- Scream test: `~/Documents/dna_ai_analyst/analyses/ad-hoc/2026-08-11-redshift-scream-test/`
- Overlord retirement: `~/Documents/dna_ai_analyst/analyses/ad-hoc/2026-09-09-overlord-retirement/`
- OpenAir jobs: `github.com/Workiva/data_services_etl` (upload/openair, upload/salesforce)
- Cost data: `~/Documents/dna_ai_finops/reports/executive_summary_ytd_2026.md`
- Jira: DNA-5930, DNA-6072, DNA-6080, DNA-5454
