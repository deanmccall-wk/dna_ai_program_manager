# Core Semantic Context Layer

**Slug:** `core-semantic-context-layer`  
**Period:** 2026 H2  
**Theme (H2 sheet):** Deliver a modernized Enterprise Data Platform  
**Owner:** Dean McCall  
**Source:** [DnA Roadmap_ongoingly_updated](https://docs.google.com/spreadsheets/d/1BUaL-iykYrJp_H1YxCwGAvJhin-bnf9BLho4Kt6VIk0/edit?gid=338395792#gid=338395792) · tab `DnA_H2'26` · method column. Pointer: `shared/roadmap-source.md`.

Do not add initiatives beyond what Dean names or what this source row already lists.

Sibling program `enterprise-agentic-personas` still owns ECM/C360 semantic views for the Q3 AI pilot. That target is not this method.

## Initiatives

Named on the H2 row as Q3 method scope. Status is unknown until Dean confirms.

| Initiative | Quarter | Status | Workstreams | Notes |
|---|---|---|---|---|
| Catalog Integration Setup | 2026 Q3 | unknown | | Sheet: Provision Snowflake Iceberg Catalog Integration |
| Granular RBAC Architecture | 2026 Q3 | unknown | | Sheet: Establish dedicated database roles |
| Strategy to increase coverage for additional Atlan connectors | 2026 Q3 | unknown | | Sheet spelling: `addtional` |

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

H2 resource grid: Derek Veroff 0.05. No Lincoln Lopes Silva allocation on this row. Capacity otherwise unknown.

Derek Veroff is on the H2 sheet and is not in `shared/org.md`. Do not assign until Dean adds him to the roster or names an assignable owner.

## Mapping

Tickets in `tickets/` must name an initiative from the table above.

No H2 Jira initiative key is on the sheet row. Do not invent one.
