# Connect and pilot Atlan Salesforce connector

**Program:** `core-semantic-context-layer`  
**Initiative:** Strategy to increase coverage for additional Atlan connectors  
**Assignee:** Venkateswarlu Kaipu  
**Jira:** [DNA-6021](https://jira.atl.workiva.net/browse/DNA-6021) (Story)  
**Parent epic:** [DNA-6020](https://jira.atl.workiva.net/browse/DNA-6020)

## User Story

**As a** data platform engineer, **I need** the Atlan Salesforce connector connected and piloted **so that** Salesforce metadata is available in Atlan as the first non-Snowflake source.

## Background

Dean named Salesforce as the first connector on this program’s Q3 coverage work. Q3 bar is connect and pilot, not a full Salesforce object estate. Supports DNA-6019 / Strategy to increase coverage for additional Atlan connectors.

Do not treat this as completion of the separate H2 method `Ingest business system metadata into Atlan`.

## Scope

**In scope**
- Configure Atlan Salesforce connector against a named Salesforce org
- Run an initial crawl/pilot on a named object set
- Confirm pilot assets (and lineage if the connector emits it) are visible in Atlan
- Record connector owner, schedule, and failure path
- Unblock later connector stories once the pilot is accepted

**Out of scope**
- Crawling all Salesforce objects
- Amazon S3, Glue, Athena, Fivetran, Iceberg
- DNA-4865
- Glossary / data-product modeling
- Changing Salesforce as a system of record

## Inputs

- Named Salesforce org and environment (prod vs sandbox) — **not provided**
- Named pilot objects — **not provided**
- Salesforce + Atlan credentials and InfoSec approval — **not provided**
- Atlan workspace used for DNA-3504 / current Snowflake connector

## Outputs / Deliverables

- Live Atlan Salesforce connector for the pilot org
- Pilot crawl completed for the named object set
- Short pilot note: objects in, schedule, owner, errors
- Evidence (Atlan URLs or screenshots) attached to the Jira story

## Acceptance Criteria

1. Atlan Salesforce connector is connected to the named org and completes a crawl without a blocking error.
2. Named pilot Salesforce objects appear as Atlan assets and can be opened by the assignee.
3. Pilot note lists connector owner, crawl schedule, and at least one verified object key.

## Definition of Done

- [ ] Connector configured in the agreed Atlan workspace
- [ ] Pilot crawl verified
- [ ] Documented (pilot note on the story)
- [ ] Credentials stored in the approved secret path, not in Jira

## Dependencies

- Blocked by: named Salesforce org, pilot objects, credentials, InfoSec/app-owner approval (unresolved)
- Blocking: S3, Glue, Athena, Fivetran, Iceberg connector stories

## Estimated Effort

Unknown until Venkateswarlu Kaipu provides it.

## Snowflake (if applicable)

- Target database/schema: n/a (Atlan ← Salesforce)
- Expected volumes: unknown
- Performance requirements: unknown
- Access / permissions: Salesforce + Atlan connector roles — unknown
