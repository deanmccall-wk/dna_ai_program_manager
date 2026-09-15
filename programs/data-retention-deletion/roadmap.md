# Data Retention & Deletion Framework

**Slug:** `data-retention-deletion`
**Period:** 2026 H2
**Goal:** Increase trust in data
**Owner:** Dean McCall
**RICE:** R=3, I=5, C=3, E=5 (SUM=16)
**Source:** `shared/data/dna-roadmap.xlsx` tab `DnA_H226` row 18

## Q3 Scope

Ensure regional data legal compliance (e.g., GDPR, CCPA) and eliminate compliance friction to accelerate the enterprise sales process.

* Asset Discovery & Tagging: Audit Snowflake storage objects and AWS S3 Inventory.
* S3 Lifecycle and Storage Integration Alignment
* TimeTravel and S3 Versioning Synchronization.

**Targets:**
* 100% of production tables tagged with data retention classification.

## Q4 Scope

* Automated Cascade Deletion Pipelines
* Legal Hold Enforcement
* Audit Transparency and Sales Defense Artifacts
* Automated Request to be Forgotten

**Targets:**
* 100% automated purge.
* < 14 days to apply request to be forgotten.
* 100% pass rate on InfoSec vendor security questionnaire.
* 0 impact to existing data pipelines.

## Resource Allocations

| Person | Allocation |
|--------|-----------|
| Staff Data Platform and AI Engineer (TBH) | 1.0 |

Note: This role is unfilled (TBH). No assignable capacity until position is filled.

## Stakeholders

Legal

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-31 | On Track | Q3 baseline: Lynn Peng has agreed to baseline all access to 10-year retention. Per-system rules require deeper analysis -- scoping a project with phData as a potential solution. Unfilled Sr Staff Data Operations role should be applied to this method in Q4. |

## Mapping

Jira: none linked on H2 sheet. Needs Jira epic or issue search.
