# FedRAMP boundary change acceptance

**Program:** `snowflake-migration`
**Initiative:** Complete Snowflake Migration
**Assignee:** Dean McCall
**Jira:** draft

## User Story

**As a** data platform leader, **I need** Tennessee Valley Authority to accept the removal of Redshift from the FedRAMP boundary **so that** we are authorized to terminate the cluster.

## Background

Tennessee Valley Authority (Salesforce account: 0014000000UFXDUAA5) is Workiva's FedRAMP sponsor. The FedRAMP boundary currently includes Redshift. Removing it requires sponsor acceptance. This has not been received.

## Scope

**In scope**
- Coordinate with Security/Compliance team to submit boundary change request
- Track acceptance status
- Obtain written confirmation

**Out of scope**
- FedRAMP audit process changes

## Inputs

- Current FedRAMP boundary documentation
- Security/Compliance team contacts

## Outputs / Deliverables

- Written acceptance from Tennessee Valley Authority
- Updated FedRAMP boundary documentation

## Acceptance Criteria

1. Tennessee Valley Authority has formally accepted the removal of Redshift from the FedRAMP boundary
2. Security/Compliance confirms we are authorized to proceed with termination

## Definition of Done

- [ ] Acceptance received
- [ ] Documented
- [ ] Security/Compliance confirms authorization

## Dependencies

- Blocked by: Security/Compliance engagement
- Blocking: Phase 5 full cluster termination

## Estimated Effort

Unknown (external dependency)
