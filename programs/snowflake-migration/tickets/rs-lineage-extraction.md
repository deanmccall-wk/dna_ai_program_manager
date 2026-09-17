# Run Atlan lineage extraction for all active landing tables

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Dean McCall
**Jira:** draft

## User Story

**As a** data platform engineer, **I need** to extract Atlan lineage for all 970 active landing tables **so that** we have the full dependency map required to assign consumer cutover work by team.

## Background

The lineage pipeline is built and demonstrated on mv_spectrum.workiva_workspace (462 edges, 234 dependents). It needs to be run for all active landing tables to produce the complete redshift_dependency_graph. Expected runtime: 5-14 hours depending on API response times.

## Scope

**In scope**
- Run `./run.sh pipeline --include-lineage` for all active landing tables
- Review and validate output in `REDSHIFT_DEPENDENCY_GRAPH`
- Group consumers by owning team for cutover ticket creation

**Out of scope**
- Executing the actual consumer cutover (separate tickets)

## Inputs

- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_ORPHAN_INVENTORY` (landing tables)
- Atlan API (lineage endpoint)

## Outputs / Deliverables

- `GOLD_DEV.DATA_PLATFORM.RAW_ATLAN_LINEAGE` populated for all landing tables
- `GOLD_DEV.DATA_PLATFORM.REDSHIFT_DEPENDENCY_GRAPH` with complete edges
- Summary report: consumers grouped by owning team

## Acceptance Criteria

1. Lineage extracted for >90% of active landing tables (some may not be in Atlan)
2. `REDSHIFT_DEPENDENCY_GRAPH` contains edges for all major schemas (salesforce, staging_coupa, mv_spectrum, product_operations, etc.)
3. Consumer-by-team grouping produced and reviewed

## Definition of Done

- [ ] Pipeline run completed
- [ ] Data validated
- [ ] Consumer grouping documented

## Dependencies

- Blocked by: none (pipeline is built)
- Blocking: Consumer cutover ticket creation

## Estimated Effort

Unknown

## Snowflake (if applicable)

- Target database/schema: GOLD_DEV.DATA_PLATFORM
- Expected volumes: ~50K-200K lineage edges
