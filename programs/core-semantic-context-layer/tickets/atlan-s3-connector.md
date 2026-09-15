# Connect Atlan Amazon S3 connector

**Program:** `core-semantic-context-layer`  
**Initiative:** Strategy to increase coverage for additional Atlan connectors  
**Assignee:** Venkateswarlu Kaipu  
**Jira:** [DNA-6022](https://jira.atl.workiva.net/browse/DNA-6022) (Story)  
**Parent epic:** [DNA-6020](https://jira.atl.workiva.net/browse/DNA-6020)

## User Story

**As a** data platform engineer, **I need** the Atlan Amazon S3 connector connected **so that** selected bucket metadata is cataloged in Atlan after the Salesforce pilot.

## Background

Second connector in Dean’s sequence. Child of the Atlan connector ingestion epic. Do not start until the Salesforce pilot is accepted unless Dean reorders.

## Scope

**In scope**
- Configure Atlan Amazon S3 connector for named buckets/prefixes
- Run crawl and confirm assets in Atlan
- Record owner, schedule, and IAM pattern used

**Out of scope**
- Crawling all org buckets
- File-content PII classification beyond what the connector emits
- Glue/Athena catalog work (separate stories)
- DNA-4865

## Inputs

- Named buckets/prefixes — **not provided**
- AWS account and IAM role for Atlan — **not provided**
- Salesforce connector story accepted

## Outputs / Deliverables

- Live Atlan S3 connector for the named scope
- Crawl evidence in Atlan
- Note: buckets, IAM role, schedule, owner

## Acceptance Criteria

1. Atlan S3 connector completes a crawl of the named buckets/prefixes without a blocking error.
2. Named prefixes appear as Atlan assets and can be opened by the assignee.

## Definition of Done

- [ ] Connector configured
- [ ] Crawl verified
- [ ] Documented on the story
- [ ] IAM/secrets in the approved path

## Dependencies

- Blocked by: Salesforce pilot story; named buckets; IAM (unresolved)
- Blocking: none required; Glue/Athena may reuse the same AWS account

## Estimated Effort

Unknown until Venkateswarlu Kaipu provides it.

## Snowflake (if applicable)

- Target database/schema: n/a unless a named bucket is a Snowflake external stage — unknown
- Expected volumes: unknown
- Performance requirements: unknown
- Access / permissions: AWS IAM for Atlan — unknown
