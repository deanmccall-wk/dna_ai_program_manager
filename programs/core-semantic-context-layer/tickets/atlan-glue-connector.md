# Connect Atlan AWS Glue connector

**Program:** `core-semantic-context-layer`  
**Initiative:** Strategy to increase coverage for additional Atlan connectors  
**Assignee:** Venkateswarlu Kaipu  
**Jira:** [DNA-6023](https://jira.atl.workiva.net/browse/DNA-6023) (Story)  
**Parent epic:** [DNA-6020](https://jira.atl.workiva.net/browse/DNA-6020)

## User Story

**As a** data platform engineer, **I need** the Atlan AWS Glue connector connected **so that** Glue catalog databases/tables are visible in Atlan.

## Background

Third connector in Dean’s sequence. Glue often feeds Athena; keep this story on Glue catalog metadata only. Athena is a separate child story. Do not start until the Salesforce pilot is accepted unless Dean reorders.

## Scope

**In scope**
- Configure Atlan AWS Glue connector for a named AWS account and Glue databases
- Run crawl and confirm Glue databases/tables in Atlan
- Record owner, schedule, and IAM pattern
- Note overlap with the Athena story (shared catalog vs duplicate crawl)

**Out of scope**
- Athena workgroup/query metadata (Athena story)
- Migrating Glue jobs
- DNA-4865

## Inputs

- Named AWS account and Glue databases — **not provided**
- IAM role for Atlan — **not provided**
- Salesforce connector story accepted

## Outputs / Deliverables

- Live Atlan Glue connector for the named databases
- Crawl evidence in Atlan
- Note: databases in, IAM, schedule, owner, overlap with Athena

## Acceptance Criteria

1. Atlan Glue connector completes a crawl of the named Glue databases without a blocking error.
2. Named Glue databases/tables appear as Atlan assets and can be opened by the assignee.
3. Story comments whether Athena should reuse this crawl or needs a separate connector.

## Definition of Done

- [ ] Connector configured
- [ ] Crawl verified
- [ ] Documented on the story
- [ ] IAM/secrets in the approved path

## Dependencies

- Blocked by: Salesforce pilot story; named Glue databases; IAM (unresolved)
- Blocking: Athena story may depend on this decision

## Estimated Effort

Unknown until Venkateswarlu Kaipu provides it.

## Snowflake (if applicable)

- Target database/schema: n/a (Atlan ← Glue)
- Expected volumes: unknown
- Performance requirements: unknown
- Access / permissions: AWS IAM — unknown
