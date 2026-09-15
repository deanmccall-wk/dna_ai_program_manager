# Core Semantic Context Layer

**Slug:** `core-semantic-context-layer`  
**Period:** 2026 H2  
**Theme (H2 sheet):** Deliver a modernized Enterprise Data Platform  
**Owner:** Dean McCall  
**Source:** [DnA Roadmap_ongoingly_updated](https://docs.google.com/spreadsheets/d/1BUaL-iykYrJp_H1YxCwGAvJhin-bnf9BLho4Kt6VIk0/edit?gid=338395792#gid=338395792) · tab `DnA_H2'26` · method column. Pointer: `shared/roadmap-source.md`.

Do not add initiatives beyond what Dean names or what this source row already lists.

Sibling program `enterprise-agentic-personas` still owns ECM/C360 semantic views for the Q3 AI pilot. That target is not this method.

## Q3 owner

Venkateswarlu Kaipu (assignable). Capacity unknown. H2 sheet still shows Derek Veroff 0.05 — does not match this assignment.

## Initiatives

Named on the H2 row as Q3 method scope. Status is unknown until Dean confirms.

| Initiative | Quarter | Status | Workstreams | Notes |
|---|---|---|---|---|
| Catalog Integration Setup | 2026 Q3 | unknown | Atlan metadata → Snowflake Iceberg catalog | Sheet: Provision Snowflake Iceberg Catalog Integration. DNA-4863 (Closed) was Atlan↔Snowflake catalog pull — verify it is not this Iceberg catalog. |
| Granular RBAC Architecture | 2026 Q3 | unknown | Lakehouse DB + roles | Sheet: Establish dedicated database roles. Open: DNA-4864. |
| Strategy to increase coverage for additional Atlan connectors | 2026 Q3 | unknown | Ingestion epic; Salesforce connect-and-pilot first | Sheet spelling: `addtional`. Sequence: Salesforce, S3, Glue, Athena, Fivetran, Iceberg. Q3 Must: Salesforce connect-and-pilot. Later connectors are child stories, started after Salesforce. DNA-4865 parked. |

## H2 scope (verbatim from source)

**Q3 — Enable queryable, active metadata governance and native enterprise context within Snowflake by leveraging Atlan's Metadata Lakehouse features.**

- Catalog Integration Setup: Provision Snowflake Iceberg Catalog Integration
- Granular RBAC Architecture: Establish dedicated database roles
- Strategy to increase coverage for addtional Atlan connectors.

Targets:

- 100% of target production databases (ANALYTICS_PROD, RAW_PROD) integrated with Atlan’s Context Lakehouse via native SQL interface.

**Q4**

- Tag-Driven Policy Enforcement: Link Atlan-synced Snowflake Object Tags directly to Dynamic Data Masking and Row Access Policies for automated, query-time compliance.
- Atlan MCP & Snowflake Cortex Integration: Enable Snowflake Cortex AI agents and LLM tools to directly query Atlan’s Model Context Protocol (MCP) server for lineage, certification, and quality context at query time.

Targets:

- 100% coverage of core analytical tables with queryable governance views in Snowflake.

## Resource notes

Q3 delivery: Assigned to Critical River. Venkateswarlu Kaipu has churned. Critical River has been responsive but contractor churn frequency should be watched.

H2 resource grid still shows Derek Veroff 0.05. Derek is now on enterprise-agentic-personas (Data Room strategy).

### Status (as of 2026-08-31)

On Track, with risks.

### Risks

1. **Salesforce connector credentials:** Were created previously but need to be resurrected. DNA-6021 and downstream connector tickets remain blocked until credentials are restored.
2. **Atlan asset capacity:** Contract is constrained to 2 million assets. Current connector plan would add back ~673,432 assets. Unknown how many total assets the new connectors will create -- need to validate headroom before activating all connectors.
3. **Contractor churn:** Venkateswarlu Kaipu (Critical River) has already churned. Critical River replaced quickly but frequency is a pattern to watch.

## Mapping

Jira Initiative: [DNA-6019](https://jira.atl.workiva.net/browse/DNA-6019) — partly makes up [DNA-44](https://jira.atl.workiva.net/browse/DNA-44). H2 sheet cell `BA33`.

Tickets in `tickets/` must name an initiative from the table above.
