# Connect Atlan AWS Athena connector

**Program:** `core-semantic-context-layer`  
**Initiative:** Strategy to increase coverage for additional Atlan connectors  
**Assignee:** Venkateswarlu Kaipu  
**Jira:** [DNA-6024](https://jira.atl.workiva.net/browse/DNA-6024) (Story)  
**Parent epic:** [DNA-6020](https://jira.atl.workiva.net/browse/DNA-6020)

## User Story

**As a** data platform engineer, **I need** the Atlan AWS Athena connector connected **so that** Athena-queryable datasets are cataloged in Atlan without duplicating Glue coverage.

## Background

Fourth connector in Dean’s sequence. Glue and Athena often share a catalog. This story starts after Salesforce, and should use the Glue story’s overlap note. Do not crawl the same tables twice without a recorded reason.

## Scope

**In scope**
- Configure Atlan Athena connector for named workgroups/catalogs, or document that Glue coverage is sufficient and close as not required
- If connected: crawl and confirm assets in Atlan
- Record owner, schedule, and relationship to Glue

**Out of scope**
- Replacing Glue as the catalog
- Cost-optimization of Athena queries
- DNA-4865

## Inputs

- Named Athena workgroups/catalogs — **not provided**
- Glue story overlap note
- Salesforce connector story accepted

## Outputs / Deliverables

- Either a live Atlan Athena connector with crawl evidence, or a written decision that Glue coverage is sufficient (Dean or Venkat recorded on the story)
- Note: workgroups, IAM, schedule, owner

## Acceptance Criteria

1. Either the Atlan Athena connector completes a crawl of the named workgroups without a blocking error, or the story records that Athena is not required because Glue already covers the same assets.
2. If connected, named Athena datasets appear as Atlan assets and can be opened by the assignee.
3. The story states whether Glue and Athena overlap and which connector is source of truth.

## Definition of Done

- [ ] Connector configured, or explicit not-required decision recorded
- [ ] Crawl verified if connected
- [ ] Documented on the story
- [ ] IAM/secrets in the approved path if connected

## Dependencies

- Blocked by: Salesforce pilot; Glue overlap decision; named workgroups; IAM (unresolved)
- Blocking: none

## Estimated Effort

Unknown until Venkateswarlu Kaipu provides it.

## Snowflake (if applicable)

- Target database/schema: n/a (Atlan ← Athena)
- Expected volumes: unknown
- Performance requirements: unknown
- Access / permissions: AWS IAM — unknown
