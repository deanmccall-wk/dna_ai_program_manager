# Connect Atlan Iceberg source connector

**Program:** `core-semantic-context-layer`  
**Initiative:** Strategy to increase coverage for additional Atlan connectors  
**Assignee:** Venkateswarlu Kaipu  
**Jira:** [DNA-6026](https://jira.atl.workiva.net/browse/DNA-6026) (Story)  
**Parent epic:** [DNA-6020](https://jira.atl.workiva.net/browse/DNA-6020)

## User Story

**As a** data platform engineer, **I need** the Atlan Iceberg source connector connected **so that** Iceberg table metadata from named catalogs is visible in Atlan.

## Background

Sixth connector in Dean’s sequence. This is the Atlan *source* connector for Iceberg tables. It is not the Snowflake Iceberg *catalog integration* on Catalog Integration Setup / lakehouse plumbing. Do not start until the Salesforce pilot is accepted unless Dean reorders.

## Scope

**In scope**
- Configure Atlan Iceberg connector for a named catalog (Glue, Snowflake Iceberg, or other — must be named)
- Run crawl and confirm Iceberg tables in Atlan
- Record owner, schedule, and which catalog implementation was used
- Explicitly distinguish this work from lakehouse Iceberg catalog tickets

**Out of scope**
- Provisioning Snowflake Iceberg Catalog Integration (Catalog Integration Setup)
- DNA-4864 roles and lakehouse database
- DNA-4865
- Creating new Iceberg tables

## Inputs

- Named Iceberg catalog and table set — **not provided**
- Catalog credentials / IAM — **not provided**
- Salesforce connector story accepted

## Outputs / Deliverables

- Live Atlan Iceberg source connector for the named catalog
- Crawl evidence in Atlan
- Note: catalog type, tables in, schedule, owner, and a one-line distinction from lakehouse Iceberg catalog work

## Acceptance Criteria

1. Atlan Iceberg source connector completes a crawl of the named catalog without a blocking error.
2. Named Iceberg tables appear as Atlan assets and can be opened by the assignee.
3. Story states the catalog implementation used and that this is not the DNA-6019 Snowflake Iceberg catalog integration.

## Definition of Done

- [ ] Connector configured
- [ ] Crawl verified
- [ ] Documented on the story
- [ ] Secrets in the approved path

## Dependencies

- Blocked by: Salesforce pilot; named Iceberg catalog; credentials (unresolved)
- Blocking: none

## Estimated Effort

Unknown until Venkateswarlu Kaipu provides it.

## Snowflake (if applicable)

- Target database/schema: unknown until the Iceberg catalog is named (may be Glue-only)
- Expected volumes: unknown
- Performance requirements: unknown
- Access / permissions: unknown
