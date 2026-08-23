---
name: write-ticket
description: Drafts or refines Jira-ready tickets for anyone in Dean McCall's assignable org using one story format and required fields. Use when writing, editing, splitting, or reviewing tickets, stories, or Jira work.
---

# Write ticket

## When

User asks to write, refine, split, or review a ticket or Jira story.

## Do not

- Do not branch on contractor vs FTE. Assignee is a field.
- Do not create `write-contractor-ticket` behavior or a second template.
- Do not invent a program slug, initiative, Jira project key, or assignee outside `shared/org.md` `scope: assignable`.
- Do not publish to Jira unless the user asks and the project key is known.

## Steps

1. If `program` is missing, read `programs/_index.md`. If more than one program, ask which. If exactly one, use it and confirm.
2. Read `docs/operating-model.md` and `templates/ticket.md`.
3. Confirm the roadmap initiative on `programs/<slug>/roadmap.md`. If none, stop and ask to establish mapping. Do not invent an initiative.
4. If assigning, read `shared/org.md`. Assignee must have `scope: assignable`. If the named person is not assignable, refuse and explain.
5. Fill every required field. Acceptance Criteria needs at least two testable conditions.
6. Run health checks from `.cursor/rules/tickets.mdc`. If any fail, say the ticket is not assignable and list the gaps. Still save a draft if the user wants it.
7. Snowflake work: include database/schema, volumes, performance, access when known; ask when not.
8. Save to `programs/<slug>/tickets/<short-slug>.md` unless the user only wants chat output.
9. Publish via Jira MCP only on explicit request with a known project key.
