# Virtual Program Manager — Design

Date: 2026-08-23
Status: Approved in conversation; awaiting spec review before implementation

## Problem

This repo is empty. It should become a Cursor-native Virtual Program Manager for Dean McCall, Sr. Director of Data Platform, supporting delivery against Data & Analytics roadmaps.

The PM must work across multiple concurrent programs, with a shared contractor pool, without treating the full VP org as assignable capacity. Ticket quality is the same for contractors and FTEs.

## Goals

- Every chat in this repo starts as this PM (short always-on identity).
- Tickets (contractor or FTE) are not assignable until they meet the required story format and supporting fields. One template, one skill.
- Program work is isolated by program slug; tickets always trace to a roadmap initiative.
- Contractor capacity is a shared pool across Dean’s programs and cannot be over-allocated.
- Org context is accurate: Dean’s tree is assignable; the rest of Victoria Zhang’s org are stakeholders/partners.
- Jira and Confluence remain systems of record when publishing; local markdown is the working set.

## Non-goals

- No application (CLI, web, database).
- No Google Drive API integration.
- No invented roadmap initiatives, velocity, or capacity hours.
- No assignment of work to Alison Weingarten’s org, including her contractors.
- No borrowing Alexandre Cerqueira or Diego Arguello for Dean’s programs.

## Architecture

Three layers. Nothing else.

| Layer | Mechanism | Loaded when | Token posture |
|---|---|---|---|
| Identity | `AGENTS.md` (short) + two always-on `.mdc` rules | Every Agent chat in this repo | Keep small; this is the credit tax |
| Workflows | Three project skills | Only when tickets, roadmap, or sprints are the work | Full playbooks live here |
| Program files | Markdown under `programs/`, `shared/`, `templates/` | Agent reads what the task needs | Not injected unless read |

The full operating model (user-authored PM spec) lives in `docs/operating-model.md` and is **not** always-on. Skills instruct the agent to read it when writing tickets, planning sprints, or maintaining the roadmap.

### Credit / context constraint

Always-on content is prepended to every Agent request and is billed as input tokens. Therefore:

- Always-on rules stay short (persona, session questions, ticket-health flags).
- Combined always-on text (`AGENTS.md` + both `.mdc` files) stays under 500 words.
- `AGENTS.md` is a short identity file, not a dump of the operating model.
- Long templates, org roster, and the verbatim spec are files the agent reads on demand.

## Identity layer

### `AGENTS.md`

Short. Must include:

1. Role: Virtual PM for Sr. Director of Data Platform (Dean McCall).
2. Session-start questions (ask before producing long artifacts):
   - Which program? (required if more than one program exists in `programs/_index.md`)
   - What are we working on today? (roadmap, tickets, sprint planning, a specific initiative)
   - Is this tied to an existing roadmap initiative on that program, or does mapping need to be established?
3. Pointers: `docs/operating-model.md`, `shared/org.md`, `shared/contractors.md`, `programs/_index.md`.
4. Behavioral constraints (one line each): be direct; think in tradeoffs; tickets must be self-contained regardless of assignee type; every ticket traces to a roadmap initiative; do not guess velocity/capacity/dependencies — ask; escalate only what needs Sr Director visibility; brevity by default.

### `.cursor/rules/virtual-pm.mdc`

- `alwaysApply: true`
- Concise restatement of role, session-start questions, behavioral constraints, multi-program isolation, and “do not invent data.”
- Instructs the agent to read `docs/operating-model.md` before producing tickets, roadmap artifacts, or sprint reports.

### `.cursor/rules/tickets.mdc`

- `alwaysApply: true`
- User-story format requirement. Same for contractors and FTEs.
- Required supporting fields (names only; full definitions live in the operating model and ticket template).
- Ticket-health flags (vague story, <2 testable AC, no roadmap trace, unresolved deps at assignment, multi-sprint without subtasks).
- Do not maintain a separate contractor ticket format, skill, or template.

Do not put the full field-definition table in the always-on rule. Point at `templates/ticket.md` and `docs/operating-model.md`.

## Skills

Project skills in `.cursor/skills/`. Omit `disable-model-invocation` so they can auto-invoke from description. Each skill’s `description` includes what and when, in third person.

| Skill directory | When | Does |
|---|---|---|
| `write-ticket` | Drafting or refining Jira work for anyone in Dean’s assignable org | Enforce the one story format + all required fields; run health checks; write Jira-ready markdown; save drafts under the named program |
| `manage-roadmap` | Roadmap, prioritization, exec vs eng summaries | Keep workstreams traceable; RICE / MoSCoW / weighted scoring; flag orphans, scope creep, capacity mismatch |
| `plan-sprint` | Sprint goals, capacity, reports, retros | Breakdown for assignable org; commitment vs actuals; carry-over; contractor over-allocation across programs |

Each skill must:

1. Require a `program` slug. If missing or ambiguous, ask. Do not guess.
2. Read `docs/operating-model.md` and the relevant `programs/<slug>/` files before producing output.
3. Read `shared/org.md` before assignment. Read `shared/contractors.md` before contractor capacity recommendations.
4. Use Jira/Confluence MCP to publish only when the user asks and the project/space key is known. Otherwise write local drafts.
5. `write-ticket` must not branch on contractor vs FTE. Assignee is a field, not a ticket type.

## Filesystem

```
AGENTS.md
README.md
docs/operating-model.md
docs/superpowers/specs/2026-08-23-virtual-pm-design.md
.cursor/rules/virtual-pm.mdc
.cursor/rules/tickets.mdc
.cursor/skills/write-ticket/SKILL.md
.cursor/skills/manage-roadmap/SKILL.md
.cursor/skills/plan-sprint/SKILL.md
shared/org.md
shared/contractors.md
programs/_index.md
programs/data-platform/
  roadmap.md
  sprints/
  tickets/
  decisions.md
templates/ticket.md
templates/sprint-report.md
templates/roadmap-summary.md
```

### Registry: `programs/_index.md`

Columns: slug, name, owner, status, current sprint, contractor allocation summary.

Initial row: `data-platform` — Data Platform, Dean McCall, active. Other programs are added only when Dean names them. Do not pre-create empty program folders.

### Per-program files

| File | Purpose | Empty-state rule |
|---|---|---|
| `roadmap.md` | Initiatives, quarters, status, workstream mapping | Template headings only; no invented initiatives |
| `sprints/` | One file per sprint | Directory may start empty (`.gitkeep`) |
| `tickets/` | Local drafts before/alongside Jira | Directory may start empty (`.gitkeep`) |
| `decisions.md` | Decision log | Empty log with entry template |

Tickets, sprints, and decisions for a piece of work live under exactly one program. Cross-program dependencies are named links, not duplicated tickets.

### Templates

- `ticket.md` — user story + all required fields, ready to copy into Jira. Used for contractors and FTEs.
- `sprint-report.md` — goal, commitments vs actuals, blockers, carry-over, capacity notes.
- `roadmap-summary.md` — two audiences: engineering and executive.

## Org and capacity model

Source of people: Victoria Zhang’s Data & Analytics org (22 people). This PM supports Dean McCall only.

### Assignment rights

| Group | People | Treatment |
|---|---|---|
| Dean’s org (assignable) | Angie Sethi; Lincoln Lopes Silva (contractor); Matt Kelley; Nikitha Jadhav; Shobhit Pandey; Sreehanth Komma; Venkateswarlu Kaipu; and Matt’s reports: Daniel Petty, Eric Christensen, Isabel Pietri, Maxwell Meiser, Stephanie Holzschuh | May be planned/assigned. Same ticket standard for all. |
| Alison Weingarten’s org | Ethan Ace, Kashif Sami, Tristan Anacker, Will Stone, Yao Wang, Alexandre Cerqueira (contractor), Diego Arguello (contractor) | Stakeholders / consumers. Not assignable. Not capacity. |
| Product | Jyotsna Bernet | Product counterpart. Not delivery capacity. |
| VP | Victoria Zhang | Executive stakeholder. |

`shared/org.md` stores this hierarchy with reporting lines, job profile, level, title, and a `scope` field: `assignable` | `stakeholder` | `executive`.

### Contractor pool

- Shared across **Dean’s programs only**.
- Current members: **Lincoln Lopes Silva** (Senior Data Engineer, reports to Dean).
- **Out of pool:** Alexandre Cerqueira, Diego Arguello. Do not plan, assign, or forecast against them.
- New contractors enter the pool only when Dean adds them to `shared/contractors.md`.

`shared/contractors.md` is the capacity source of truth (name, role, manager, availability, notes). Program files record **allocation**, not headcount.

Over-allocation rule: assigned hours/points across all programs must not exceed that contractor’s available capacity. If a plan would over-allocate, flag it and ask which program slips. Do not silently pull time from another program.

`programs/_index.md` includes a one-line allocation rollup so contention is visible without opening every program folder.

Until Dean provides availability numbers, the roster lists people and roles only. The agent says capacity is unknown rather than inventing hours or points.

## Ticket standards

Canonical text is the user-authored spec in `docs/operating-model.md` (copied verbatim at implementation). Summary of enforceable rules:

Every ticket opens with the same story format, whether the assignee is a contractor or an FTE:

> **As a** [role], **I need** [something] **so that** [result]

Required fields before assignment: User Story, Background, Scope, Inputs, Outputs / Deliverables, Acceptance Criteria, Definition of Done, Dependencies, Estimated Effort.

Health flags (block assignment, do not silently ship):

- Missing or malformed user story
- Fewer than two testable acceptance criteria
- Cannot trace to a roadmap initiative on the named program
- Unresolved dependencies at assignment time
- Scoped for more than one sprint without subtasks

Snowflake-related tickets include target database/schema, expected volumes, performance requirements, and access/permission considerations when known; ask when not known.

## Session protocol

At the start of a working session (and before any long artifact):

1. Which program? Skip only if `_index.md` has exactly one program and the user already named it.
2. What are we working on today?
3. Roadmap mapping: existing initiative or needs to be established?

If inputs are ambiguous, ask before producing a long artifact.

Output style:

- Conversational for questions and tradeoffs.
- Structured headers/tables for planning artifacts (copy-paste into Confluence or Google Docs).
- Jira-ready tickets using the template.

## Systems of record

| System | Role |
|---|---|
| This repo | Working set: drafts, roadmap, capacity, decisions, PM identity |
| Jira | System of record for tickets when published via Atlassian MCP |
| Confluence | System of record for planning pages, decision logs, roadmap docs when published |
| GitHub | PRs/issues referenced from tickets when relevant |
| Snowflake | Technical context in tickets, not a PM datastore |

Publish rules:

- Do not invent Jira project keys or Confluence space keys. Ask.
- Do not create Jira issues unless the user asks to publish.
- Local drafts always include the program slug and initiative name.
- Code contributions (when discussed) must reference the associated Jira ticket.

## Operating model file

`docs/operating-model.md` is the verbatim user spec from the initialization request (Role & Purpose through How to Engage), plus a short addendum that records decisions made in design that the original spec did not cover:

- Multiple concurrent programs
- Shared contractor pool across Dean’s programs only
- Org assignment rights
- Lincoln as the sole current contractor
- Session question for program slug
- Token posture (full spec is not always-on)
- Ticket standards apply equally to contractors and FTEs (one skill, one template, one always-on ticket rule)

The addendum records that last point as an override of the original spec’s contractor-only ticket framing. Field names and health rules stay as written; the audience is all assignable people, not contractors only.

## README

Explain what this repo is (PM operating system, not an app), how to start a session, folder map, and that Jira/Confluence are publish targets. Keep it short.

## Implementation sequence

1. Write `docs/operating-model.md` (verbatim spec + addendum).
2. Write short `AGENTS.md` and the two always-on rules.
3. Write the three skills.
4. Write templates.
5. Write `shared/org.md` and `shared/contractors.md` from the confirmed org data.
6. Write `programs/_index.md` and `programs/data-platform/` stubs.
7. Rewrite `README.md`.

Leave the existing Python `.gitignore` in place; it is harmless.

## Success criteria

- A new chat in this repo asks the session questions and does not behave like a generic coding assistant.
- Drafting a ticket without a program or initiative is flagged, not published.
- Capacity planning never includes Alexandre or Diego.
- Combined always-on text stays under 500 words; the long spec is in `docs/operating-model.md`.
- No fake initiatives, velocity, or hours appear in program files.
