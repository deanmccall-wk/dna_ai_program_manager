# Connect Atlan Fivetran connector

**Program:** `core-semantic-context-layer`  
**Initiative:** Strategy to increase coverage for additional Atlan connectors  
**Assignee:** Venkateswarlu Kaipu  
**Jira:** [DNA-6025](https://jira.atl.workiva.net/browse/DNA-6025) (Story)  
**Parent epic:** [DNA-6020](https://jira.atl.workiva.net/browse/DNA-6020)

## User Story

**As a** data platform engineer, **I need** the Atlan Fivetran connector connected **so that** Fivetran pipeline/connector metadata is visible in Atlan alongside destination assets.

## Background

Fifth connector in Dean’s sequence. Snowflake destinations may already be crawled (DNA-3504). This story is Fivetran *connector* metadata (sources, connectors, schemas), not a re-crawl of Snowflake. Do not start until the Salesforce pilot is accepted unless Dean reorders.

## Scope

**In scope**
- Configure Atlan Fivetran connector for a named Fivetran account
- Run crawl and confirm Fivetran connectors/pipelines appear in Atlan
- Record overlap with existing Snowflake assets (lineage if emitted)
- Record owner and schedule

**Out of scope**
- Building new Fivetran pipelines
- Replacing the Snowflake Atlan crawler
- DNA-4865

## Inputs

- Named Fivetran account and destination — **not provided**
- API credentials / Atlan Fivetran connector access — **not provided**
- Salesforce connector story accepted

## Outputs / Deliverables

- Live Atlan Fivetran connector for the named account
- Crawl evidence in Atlan
- Note: connectors in, destination, schedule, owner, overlap with Snowflake crawl

## Acceptance Criteria

1. Atlan Fivetran connector completes a crawl of the named account without a blocking error.
2. Named Fivetran connectors appear as Atlan assets and can be opened by the assignee.
3. Story notes whether destination Snowflake objects are already present from the Snowflake crawler.

## Definition of Done

- [ ] Connector configured
- [ ] Crawl verified
- [ ] Documented on the story
- [ ] Secrets in the approved path

## Dependencies

- Blocked by: Salesforce pilot; named Fivetran account; credentials (unresolved)
- Blocking: none

## Estimated Effort

Unknown until Venkateswarlu Kaipu provides it.

## Snowflake (if applicable)

- Target database/schema: Fivetran destination schemas — unknown until named
- Expected volumes: unknown
- Performance requirements: unknown
- Access / permissions: Fivetran API + existing Snowflake crawler — unknown
