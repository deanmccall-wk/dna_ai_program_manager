# Data Platform Performance Metrics

**Slug:** `platform-performance-metrics`
**Period:** 2026 H2
**Goal:** Deliver a modernized Enterprise Data Platform
**Owner:** Dean McCall
**RICE:** R=1, I=1, C=5, E=5 (SUM=12)
**Source:** `shared/data/dna-roadmap.xlsx` tab `DnA_H226` row 43

## Q3 Scope

* Metadata & Session Tagging Strategy: Enforce mandatory session-level and query-level tagging.
* Cost Extraction Pipeline: Build automated pipelines using Snowflake.
* Consumption Profiling: Segment platform spend into explicit categories: direct user queries, BI dashboard re-renders, background automated pipelines (dbt/Airflow), and platform overhead.
* Initial Cost-Per-User Model: Deploy an automated cost dashboard mapping total compute + storage spend divided by Active Monthly Users (MAU) and Daily Active Users (DAU) per department.

**Targets:**
* 100% automated daily ingestion into the cost-attribution data model.
* Total data platform costs visibility.
* Significant date (contract renewals) visibility.

## Q4 Scope

* Warehouse Right-Sizing & Auto-Suspend Tuning: Programmatically adjust Snowflake warehouse parameters.
* Resource Monitor Enforcement.
* Inefficient Query Mitigation: Build automated anomaly detection routines.
* Chargeback & Showback Reporting: Finalize the self-service "Cost Per User" executive matrix, allowing department managers to track individual user consumption trends month-over-month.

**Targets:**
* >= 20% reduction in average Snowflake credit cost per active user across the enterprise.

## Resource Allocations

No resources allocated on H2 sheet. Capacity unknown.

## Stakeholders

None listed on H2 sheet.

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-31 | unknown | Initial program creation. No Jira linked. No resources allocated. |

## Mapping

Jira: none linked on H2 sheet. Needs Jira epic or issue search.
