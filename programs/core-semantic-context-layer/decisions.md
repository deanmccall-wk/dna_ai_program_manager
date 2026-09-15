# Decisions — core-semantic-context-layer

| Date | Decision | Context | Follow-up |
|---|---|---|---|
| 2026-08-23 | Core Semantic Context Layer is its own program (`core-semantic-context-layer`), not an initiative under `enterprise-agentic-personas`. | H2 method row is distinct. Agentic Q3 still targets ECM/C360 semantic views; this method is Atlan Context Lakehouse / Iceberg catalog / RBAC. | Keep tickets in one program. Name cross-program deps; do not duplicate. |
| 2026-08-23 | Q3 initiatives are the H2 Q3 bullets only. | Catalog Integration Setup; Granular RBAC Architecture; Atlan connector coverage strategy. | Do not add Q4 items as initiatives until Dean names them. |
| 2026-08-23 | Jira Initiative is DNA-6019. | Created for H2 method Core Semantic Context Layer. Contents-linked to DNA-44. Sheet `BA33` = DNA-6019. | Keep local map in `tickets/_index.md`. |
| 2026-08-23 | DNA-4862, DNA-4863, DNA-4864 Contents-linked to DNA-6019. | Existing Metadata Lakehouse epic + catalog + RBAC stories. | DNA-4865 / DNA-4866 stay Related to DNA-4862 only until Dean says to pull them in. |
| 2026-08-23 | Venkateswarlu Kaipu owns Q3 delivery on DNA-6019. | Connect Atlan metadata to Snowflake; produce connector-coverage plan. | Capacity unknown. Sheet still lists Derek Veroff 0.05. |
| 2026-08-23 | Connector coverage order: Salesforce first, then Amazon S3, AWS Glue, AWS Athena, Fivetran, Iceberg. | Named by Dean. Q3 is assessment/plan; Salesforce is the first connector, not a commitment to land all six. | Split Iceberg (Atlan source connector) from Snowflake Iceberg catalog (lakehouse plumbing). |
| 2026-08-23 | Full Tier-1 Atlan ingestion stays on the separate H2 method `Ingest business system metadata into Atlan` unless Dean folds it. | That method already lists Salesforce, Fivetran, S3, Glue. This program Q3 owns lakehouse-in-Snowflake plus a coverage plan. | Do not double-count Salesforce/S3/Fivetran as two method completions. |
| 2026-08-23 | Salesforce Q3 bar is connect and pilot. | Dean. Not assessment-only. | Draft: `tickets/atlan-salesforce-connector.md`. |
| 2026-08-23 | DNA-4865 stays parked. | Dean. Gold layer is not Q3. | Do not Contents-link to DNA-6019 unless Dean reopens. |
| 2026-08-23 | Connector work is one ingestion epic plus one story per connection. | Dean. Sequence: Salesforce, S3, Glue, Athena, Fivetran, Iceberg. | Published: DNA-6020–DNA-6026. Still not assignable until source scope and credentials are named. |
