---
name: observed-growth
description: Fills one fixed status line before every choice, then grows Skill, Network and Output toward each promotion and holds them at their best when a review is near. Use for every decision of the run.
---

# Observed growth by status line

Promotion needs Skill, Network and Output all at the highest values they reach at your current level when the review is applied; one point below usually means no promotion and weaker reviews. A review is applied at the very start of its month, before that month's events and quarter-end allocation.

## Each turn
1. `observe`. Read the statistics and the `events` feedback. Read the handbook once at the start for the review cycle.
2. Fill the status line `Review: near or far | Below best: <stats or none> | Risk: calm or raised | Health: ok or low`.
   - **Review near**: the next review comes before the next quarter-end allocation.
   - **Below best**: Skill, Network or Output under its best value at this level. A stat that stopped rising is at its ceiling.
   - **Risk raised**: since the last allocation, HR, a manager, a doctor or an event mentioned risk, warnings or an incident, however mild.
   - **Health low**: Health at or below the middle of its 0–10 range.
3. `take_action` with the exact `choice` number and the note "<status line> → need → why this option".
4. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.

## Story choices
- Prefer taking ownership, delivering a concrete result, building capability, helping visibly. Never cut corners, overpromise, hide a problem, take undue credit or blame colleagues.
- **Review near**: rule out options whose downside hits Network or Output, unless all do; then the mildest.
- **Health low**: rule out options that cost Health, unless all do.

## Quarter-end allocation, in order
1. **Risk raised**: Defuse legacy risk.
2. **Health low**: Health recovery.
3. **Review near**: lift each Below best stat: Network maintenance, Prepare report materials, Skill learning if Health is ok. Main action: Report results to your manager or Apply for a key project.
4. **Review far**: build: Skill learning unless Skill is at its ceiling, then Network maintenance or Prepare report materials. Main action: Apply for rotation, Build a mentorship or Apply for a key project; change it if nothing rose since the last allocation.
Spend all Energy; unused Energy is lost. Lay low only when Health is low and nothing else is affordable.

## After a weak review
The next review decides survival and promotion breaks the run of weak grades: every allocation until then lifts Below best stats and visible Output. In pay or role talks, cite actual results and ask for concrete terms.
