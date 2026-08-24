---
name: manage-roadmap
description: Maintains program roadmaps, traces tickets to initiatives, and writes engineering or executive summaries using RICE, MoSCoW, or weighted scoring. Use when working on roadmap, prioritization, quarterly planning, or exec vs eng summaries.
---

# Manage roadmap

## When

Roadmap edits, prioritization, orphan checks, or eng/exec summaries.

## Steps

1. Require `program` slug. Ask if missing or ambiguous. Read `programs/_index.md`.
2. Read `docs/operating-model.md`, `shared/roadmap-source.md`, and `programs/<slug>/roadmap.md`. For DnA H2 methods and capacity, read the Google Sheet (plugin: `get_values` on spreadsheet ID and tab in `shared/roadmap-source.md`). Do not use a local xlsx snapshot as current.
3. Do not invent initiatives. Add an initiative only when the user names it.
4. Keep tickets and workstreams mapped to an initiative. Flag orphans.
5. When prioritizing, use the framework the user names (RICE, MoSCoW, or weighted scoring). If they don't name one, ask. Do not fake scores.
6. Flag scope creep and capacity mismatch. For contractor contention, read `shared/org.md` (Employment type `Contractor`, scope `assignable`).
7. Summaries use `templates/roadmap-summary.md` (engineering view and executive view).
8. Publish to Confluence only when the user asks and the space key is known.
