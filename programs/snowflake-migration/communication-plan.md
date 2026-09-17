# Redshift Shutdown -- Communication & Meeting Plan

**Program:** snowflake-migration
**Owner:** Dean McCall
**Duration:** September 15 - November 1, 2026

---

## Stakeholder Communication Matrix

| Audience | Forum | Cadence | Day | Content | Owner |
|----------|-------|---------|-----|---------|-------|
| VP of Data & Analytics | 1:1 or staff meeting | Weekly | Monday | VP Scorecard: % complete, savings, blockers, next week | Dean McCall |
| Data Platform Team | Team standup / Slack #data-platform | 2x weekly | Tue / Thu | Execution status, task assignments, blockers, daily scan results | Dean McCall |
| Alison Weingarten (ECM) | Slack DM + weekly sync | Weekly | Wednesday | ECM QuickSight migration status (DNA-6080), dataset re-pointing progress | Dean McCall |
| CPX / BizTech (OpenAir) | Shared standup | Weekly | Thursday | OpenAir non-prod env, Fivetran connector setup, parity testing, SOX timeline | Dean McCall + CPX lead |
| Finance (OpenAir SOX) | Meeting | Biweekly or as needed | -- | OpenAir data validation results, sign-off request, cutover date | Dean McCall + CPX lead |
| Security / Compliance (FedRAMP) | Meeting + email | As needed | -- | FedRAMP boundary change status, Tennessee Valley Authority acceptance | Dean McCall + Security lead |

---

## Weekly Rhythm

### Monday
- Update VP weekly scorecard with latest data from Snowflake
- Present to VP in 1:1 or staff meeting
- Identify any blockers requiring escalation

### Tuesday
- Data Platform team sync: review task board, assign work for the week
- Run scan pipeline to update orphan inventory (if not automated)

### Wednesday
- Sync with Alison Weingarten on ECM QuickSight progress
- Review any new consumers discovered in daily scan data

### Thursday
- Data Platform team sync: mid-week progress check
- CPX/OpenAir standup: non-prod env, connector status

### Friday
- Review weekly metrics for scorecard update
- Update Jira issue statuses
- Prep Monday scorecard

---

## Escalation Path

| Issue | First Escalation | Second Escalation |
|-------|-----------------|-------------------|
| OpenAir SOX sign-off delayed | CPX lead -> Finance Director | VP of Data & Analytics |
| FedRAMP acceptance not received | Security lead | VP of Data & Analytics -> Legal |
| ECM QuickSight migration stalled | Alison Weingarten | VP of Data & Analytics |
| Resource constraint on Data Platform | Dean McCall | VP of Data & Analytics |

---

## Communication Artifacts

| Artifact | Location | Update Cadence |
|----------|----------|---------------|
| VP Weekly Scorecard | `programs/snowflake-migration/vp-weekly-scorecard.md` | Weekly (Monday) |
| Detailed Completion Scorecard | `programs/snowflake-migration/shutdown-completion-scorecard.md` | After each milestone |
| Timeline | `programs/snowflake-migration/shutdown-timeline.md` | As dates change |
| Shutdown Plan (full assessment) | `programs/snowflake-migration/redshift-shutdown-plan.md` | As findings change |
| PPTX Presentation | `programs/snowflake-migration/redshift-shutdown-presentation.pptx` | As needed (regenerate with build_presentation.py) |
| Jira Epic | DNA project: "Redshift Shutdown - Consumer Cutover" | Continuous |
