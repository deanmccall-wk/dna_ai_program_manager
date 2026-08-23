---
name: plan-sprint
description: Plans sprints for Dean McCall's assignable org, tracks commitment vs actuals, and flags contractor over-allocation across programs. Use when setting sprint goals, doing capacity planning, writing sprint reports, or running retros.
---

# Plan sprint

## When

Sprint goals, capacity, reports, retros, carry-over.

## Steps

1. Require `program` slug. Ask if missing. Read `programs/_index.md`.
2. Read `docs/operating-model.md`, `programs/<slug>/roadmap.md`, and `shared/org.md`.
3. Break work for the assignable org using `templates/ticket.md` quality rules via `write-ticket` behavior (same ticket standard).
4. Before recommending contractor load, read `shared/contractors.md`. Pool member is Lincoln Lopes Silva only. Never plan Alexandre Cerqueira or Diego Arguello.
5. If contractor assignment would exceed listed availability across all programs, stop and ask which program slips. Do not silently move time.
6. If availability numbers are missing, say capacity is unknown. Do not invent hours or points.
7. Reports use `templates/sprint-report.md`. Save under `programs/<slug>/sprints/` when producing a durable artifact.
8. Publish to Jira/Confluence only on request with known keys.
