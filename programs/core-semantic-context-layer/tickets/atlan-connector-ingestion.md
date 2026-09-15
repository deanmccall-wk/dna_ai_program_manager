# Atlan connector ingestion

**Program:** `core-semantic-context-layer`  
**Initiative:** Strategy to increase coverage for additional Atlan connectors  
**Assignee:** Venkateswarlu Kaipu  
**Jira:** [DNA-6020](https://jira.atl.workiva.net/browse/DNA-6020) (Epic)  
**Parent:** [DNA-6019](https://jira.atl.workiva.net/browse/DNA-6019)

## User Story

**As a** data platform engineer, **I need** source-system metadata ingested into Atlan through governed connectors **so that** enterprise context extends beyond Snowflake-crawled assets.

## Background

Q3 work on DNA-6019 includes a strategy to increase Atlan connector coverage. Dean named the sequence: Salesforce first (connect and pilot), then Amazon S3, AWS Glue, AWS Athena, Fivetran, Iceberg.

This epic is the ingestion vehicle. Child stories are one connection each. Full Tier-1 ingestion still exists as a separate H2 method (`Ingest business system metadata into Atlan`); these tickets are the delivery backlog on this program so the work is not double-counted as two method completions.

DNA-4865 (Metadata Lakehouse Gold Layer) stays parked.

This epic is multi-sprint. Do not assign the epic as execution work. Assign child stories.

## Scope

**In scope**
- Child stories for Salesforce, Amazon S3, AWS Glue, AWS Athena, Fivetran, and Iceberg connectors
- Salesforce connect-and-pilot in Q3
- Sequence, dependencies, and Contents-link to DNA-6019
- Connector config, crawl, and evidence that assets appear in Atlan

**Out of scope**
- DNA-4865 Gold Layer
- Snowflake Iceberg catalog / lakehouse RBAC (Catalog Integration Setup, Granular RBAC Architecture, DNA-4864)
- Q4 tag-driven policies and Atlan MCP / Cortex
- Glossary term mapping and data-product models from the other H2 method, unless Dean folds that method

## Inputs

- Atlan workspace and connector admin access
- Source credentials per child story (Salesforce org, S3 buckets, Glue/Athena accounts, Fivetran, Iceberg catalogs)
- DNA-6019; Closed DNA-3504 / DNA-4863 as prior Snowflake↔Atlan context only

## Outputs / Deliverables

- Jira Epic with six child stories, Contents-linked to DNA-6019
- Working Salesforce pilot in Atlan
- Remaining connectors connected in named sequence, or a recorded block with owner

## Acceptance Criteria

1. Epic is Contents-linked to DNA-6019 and contains exactly one child story per named connector: Salesforce, Amazon S3, AWS Glue, AWS Athena, Fivetran, Iceberg.
2. Salesforce child is the first started; later children stay blocked until the Salesforce pilot meets its acceptance criteria, unless Dean reorders.
3. DNA-4865 remains parked (not a child of this epic).

## Definition of Done

- [ ] Epic published and Contents-linked to DNA-6019
- [ ] Child stories published and linked to this epic
- [ ] Sequence documented on the epic
- [ ] Q3 Salesforce pilot accepted or a named block recorded

## Dependencies

- Blocked by: source credentials and InfoSec/app-owner approval per connector (unresolved until named)
- Blocking: Q4 tag/MCP work that needs broader Atlan coverage

## Estimated Effort

Unknown until Venkateswarlu Kaipu provides it.

## Snowflake (if applicable)

- Target database/schema: not this epic (Atlan ingestion). Iceberg child must distinguish Atlan Iceberg *source* connector from Snowflake Iceberg *catalog* on Catalog Integration Setup.
- Expected volumes: unknown
- Performance requirements: unknown
- Access / permissions: unknown
