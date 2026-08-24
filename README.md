# DNA AI Program Manager

Cursor-native Virtual Program Manager for Dean McCall, Sr. Director of Data Platform.

This is a PM operating system (rules, skills, markdown), not an application.

## Start a session

Open Agent chat in this repo. The PM should ask:

1. Which program?
2. What are we working on today?
3. Which roadmap initiative does it map to?

If that does not happen, `@AGENTS.md` and continue.

## Layout

| Path | What |
|---|---|
| `docs/operating-model.md` | Full PM spec |
| `.cursor/rules/` | Always-on identity and ticket health |
| `.cursor/skills/` | Ticket, roadmap, sprint playbooks |
| `programs/` | One folder per program |
| `shared/org.md` | Roster: assignable vs stakeholder; contractors = Employment type from `DIM_WORKERS` |
| `shared/roadmap-source.md` | Live DnA roadmap (Google Sheet ID + H2 tab) |
| `templates/` | Ticket / sprint / roadmap skeletons |

## Publish

Jira and Confluence are systems of record. Local markdown is the working set. Do not publish unless you ask and the project/space key is known.

## Ticket standard

One format for contractors and FTEs. Template: `templates/ticket.md`.
