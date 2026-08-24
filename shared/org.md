# Data & Analytics org

Source: Victoria Zhang’s org. This PM supports Dean McCall only.

Employment type is `GOLD_PROD.MARTS.DIM_WORKERS.POSITION_TYPE` (latest row). Use it to identify contractors — do not infer contractor status from Profile.

`scope` values: `assignable` | `stakeholder` | `executive`

## Hierarchy

### Victoria Zhang — VP, Data & Analytics — Regular — `executive`

#### Alison Weingarten — Director of Decision Science — Data Science M5 — Regular — `stakeholder`

| Name | Profile | Employment type | Level | Title | Scope |
|---|---|---|---|---|---|
| Alexandre Cerqueira | Contractor | Contractor | — | Contractor | stakeholder |
| Diego Arguello | Contractor | Contractor | — | Contractor | stakeholder |
| Ethan Ace | Data Science | Regular | P4 | Staff Data Scientist | stakeholder |
| Kashif Sami | Business Intelligence | Regular | P5 | Senior Staff Decision Scientist | stakeholder |
| Tristan Anacker | Business Intelligence | Regular | P4 | Staff Business Intelligence Analyst | stakeholder |
| Will Stone | Data Science | Regular | P4 | Staff Data Scientist | stakeholder |
| Yao Wang | Business Intelligence | Regular | P4 | Staff Business Intelligence Analyst | stakeholder |

#### Dean McCall — Sr. Director, Data Platform — Data Engineering M6 — Regular — `assignable` (self; not a typical ticket assignee)

| Name | Profile | Employment type | Level | Title | Reports to | Scope |
|---|---|---|---|---|---|---|
| Angie Sethi | Product Management | Contractor | P2 | Associate Data Product Manager | Dean McCall | assignable |
| Lincoln Lopes Silva | Contractor | Contractor | — | Senior Data Engineer | Dean McCall | assignable |
| Matt Kelley | Data Engineering | Regular | M4 | Senior Manager of Analytics Engineering | Dean McCall | assignable |
| Nikitha Jadhav | Database Engineering | Contractor | P2 | Data Operations Engineer | Dean McCall | assignable |
| Shobhit Pandey | Database Engineering | Contractor | P2 | Data Operations Engineer | Dean McCall | assignable |
| Sreehanth Komma | Database Engineering | Contractor | P4 | Staff Data and AI Platform Engineer | Dean McCall | assignable |
| Venkateswarlu Kaipu | Data Engineering | Contractor | P3 | Sr Data Platform and AI Engineer | Dean McCall | assignable |

##### Matt Kelley’s reports

| Name | Profile | Employment type | Level | Title | Reports to | Scope |
|---|---|---|---|---|---|---|
| Daniel Petty | Data Engineering | Regular | P2 | Data Engineer | Matt Kelley | assignable |
| Eric Christensen | Data Analytics | Regular | P3 | Senior Analytics Engineer | Matt Kelley | assignable |
| Isabel Pietri | Data Analytics | Regular | P3 | Senior Analytics Engineer | Matt Kelley | assignable |
| Maxwell Meiser | Data Analytics | Regular | P2 | Data Analytics Engineer | Matt Kelley | assignable |
| Stephanie Holzschuh | Data Engineering | Regular | P3 | Senior Data Engineer | Matt Kelley | assignable |

#### Jyotsna Bernet — Lead Data Product Manager — Product Management P5 — Regular — `stakeholder`

## Rules

- This file is the complete roster. Do not maintain a separate contractor list.
- Do not assign tickets to `stakeholder` or `executive`.
- **Contractors** are rows with Employment type `Contractor`. Profile is job family and is not the contractor flag.
- **Dean’s contractor capacity** is Employment type `Contractor` and scope `assignable`: Angie Sethi, Lincoln Lopes Silva, Nikitha Jadhav, Shobhit Pandey, Sreehanth Komma, Venkateswarlu Kaipu.
- **Not capacity:** Employment type `Contractor` and scope `stakeholder` (Alexandre Cerqueira, Diego Arguello). Do not plan, assign, or forecast them on Dean’s programs.
- New people exist only when Dean adds them here. Refresh Employment type from `DIM_WORKERS` when the roster changes.
- Availability hours/points are unknown until Dean provides them. Do not invent numbers. Until then, say capacity is unknown.
- Program files record **allocation**, not headcount. Assigned hours/points for an assignable contractor across all programs must not exceed listed availability. If a plan would over-allocate, flag it and ask which program slips.
