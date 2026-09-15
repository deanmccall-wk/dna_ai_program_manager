# Tickets — core-semantic-context-layer

Jira is the system of record. This file is the local map.

Initiative: [DNA-6019](https://jira.atl.workiva.net/browse/DNA-6019) — partly makes up [DNA-44](https://jira.atl.workiva.net/browse/DNA-44).

## Linked to DNA-6019 (Contents)

Prior Metadata Lakehouse work. Mapped by Dean to this H2 method.

| Key | Summary | Type | Status | Notes |
|---|---|---|---|---|
| [DNA-4862](https://jira.atl.workiva.net/browse/DNA-4862) | Creating a Metadata Lakehouse in Snowflake | Epic | Closed | Contents → DNA-6019 |
| [DNA-4863](https://jira.atl.workiva.net/browse/DNA-4863) | Metadata Lakehouse - Integration Catalog | Story | Closed | Contents → DNA-6019. Also Related to DNA-4862. |
| [DNA-4864](https://jira.atl.workiva.net/browse/DNA-4864) | Metadata Lakehouse - Database Creation and Role Creation | Story | Open | Contents → DNA-6019. Maps to Granular RBAC Architecture. Unassigned. |

## Related, not Contents-linked

Still Related to DNA-4862. Not linked to DNA-6019 unless Dean says so.

| Key | Summary | Status |
|---|---|---|
| [DNA-4865](https://jira.atl.workiva.net/browse/DNA-4865) | Metadata Lakehouse - Gold Layer | Open |
| [DNA-4866](https://jira.atl.workiva.net/browse/DNA-4866) | Understand Metadata Sync between DBT, Snowflake, Atlan and Metadata Lakehouse | Open |

DNA-4865 stays parked (Dean 2026-08-23).

DNA-5962 / DNA-5963 (Atlan certification for Master Agent) stay on `enterprise-agentic-personas` (parked under DNA-5933).

## Atlan connector ingestion (DNA-6020)

Initiative: Strategy to increase coverage for additional Atlan connectors. Assignee: Venkateswarlu Kaipu. Epic Contents → DNA-6019. Stories on Epic Link DNA-6020. Still not assignable until source scope and credentials are named.

| Key | Summary | Type | Q3 | Assignable now? |
|---|---|---|---|---|
| [DNA-6020](https://jira.atl.workiva.net/browse/DNA-6020) | Atlan connector ingestion | Epic | Parent | No — container only |
| [DNA-6021](https://jira.atl.workiva.net/browse/DNA-6021) | Connect and pilot Atlan Salesforce connector | Story | Connect and pilot | **No** — org, objects, credentials missing |
| [DNA-6022](https://jira.atl.workiva.net/browse/DNA-6022) | Connect Atlan Amazon S3 connector | Story | After Salesforce | **No** — blocked by DNA-6021 + named buckets |
| [DNA-6023](https://jira.atl.workiva.net/browse/DNA-6023) | Connect Atlan AWS Glue connector | Story | After Salesforce | **No** — blocked by DNA-6021 + named Glue DBs |
| [DNA-6024](https://jira.atl.workiva.net/browse/DNA-6024) | Connect Atlan AWS Athena connector | Story | After Salesforce / Glue | **No** — blocked by DNA-6021 and DNA-6023 |
| [DNA-6025](https://jira.atl.workiva.net/browse/DNA-6025) | Connect Atlan Fivetran connector | Story | After Salesforce | **No** — blocked by DNA-6021 + named Fivetran account |
| [DNA-6026](https://jira.atl.workiva.net/browse/DNA-6026) | Connect Atlan Iceberg source connector | Story | After Salesforce | **No** — blocked by DNA-6021; not lakehouse Iceberg catalog |
