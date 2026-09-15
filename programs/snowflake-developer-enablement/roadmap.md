# Snowflake Developer Persona Enablement

**Slug:** `snowflake-developer-enablement`
**Period:** 2026 H2
**Goal:** Deliver a modernized Enterprise Data Platform
**Owner:** Dean McCall
**RICE:** R=2.5, I=3, C=3, E=3 (SUM=11.5)
**Source:** `shared/data/dna-roadmap.xlsx` tab `DnA_H226` row 22

## Q3 Scope

* Configure provider SQL templates, differential privacy controls, and automated dataset linking for Iceberg and native tables.
* Audit long-running queries to identify high-spillover jobs.
* Model core business entities (Orders, Customers, Revenue) into Snowflake Native Semantic Views using standard DDL blocks (Tables, Relationships, Facts, Dimensions, Metrics).
* Snowflake agent design methodology.

**Targets:**
* Code Optimization: >= 25% reduction in overall compute credit spend on top-20 longest-running warehouse workloads.
* Semantic Views: >= 85% text-to-SQL query accuracy on initial Cortex Analyst benchmark test suite.

## Q4 Scope

* Expand Semantic Views across all business verticals.
* Integrate synonyms, verified query examples, and custom metrics for self-service business intelligence via Cortex Analyst.

**Targets:**
* 100% coverage of core enterprise KPIs defined inside governed Semantic Views with > 92% accuracy on natural-language Cortex Analyst queries.

## Resource Allocations

No resources allocated on H2 sheet. Capacity unknown.

## Stakeholders

Sales, Product, CPX, Marketing, Engineering, Growth

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-31 | On Track | Will be assigned to Derek Veroff. Related work in progress: DNA-5274 (ECM Semantic Views, Will Stone), DNA-6014 (architecture review, Sreehanth), DNA-6066 (dashboard vs semantic views, Yao Wang). |

## Mapping

Jira: none linked on H2 sheet. Needs Jira epic or issue search.
