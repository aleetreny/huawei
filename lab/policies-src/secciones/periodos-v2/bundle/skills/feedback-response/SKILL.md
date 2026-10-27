---
name: feedback-response
description: Core loop of the career. Turns risk warnings, Health or Dignity alarms and weak review grades into the next decision, and sets which skill leads when they disagree. Use on every turn, before choosing.
---

## Turn loop
1. `observe`; read `events` and your last action's result first.
2. Update the signal state, then `take_action` with the exact `choice` number and a short note: state, signal seen, response.
3. If `success` is false, pick an affordable option. Stop at `ending_score`.

## Signal state
Risk signal: warning, HR, compliance, complaint, audit or legacy-problem wording, a statistic warning, or a rising risk entry in `status_updates`.
- **Clear** (no recent risk signal): take the best visible trade-off. In quarterly phases follow the review-clock skill before your first promotion and the climb skill after it.
- **Raised** (one recent signal): Defuse legacy risk first in the next Energy phase. In story events prefer disclosing, fixing or closing a problem over postponing, hiding or shifting it.
- **Escalating** (repeated or stronger signals): as Raised, plus Defuse legacy risk every Energy phase, Lay low and reduce risk as main action unless a weak review plan is active, and no new story commitments.
- Step down one state after a whole quarter without a new risk signal.

## Weak review plan
After a C or D, or feedback that results fall short, until the next review: aim the main action at the factor named (results: Report results to your manager; capability: Build a mentorship; relationships: Repair a key relationship) and spend spare Energy on Prepare report materials.

## Priority when skills disagree
1. Recovery when Health or Dignity is low or named in a warning.
2. The risk state above.
3. The weak review plan.
4. Growth: review-clock before your first promotion, climb after it, closing at the end of the run.
