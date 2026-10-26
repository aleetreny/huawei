---
name: feedback-response
description: Turns risk warnings and review grades into the next decision. Use on every turn, before choosing.
---

## Turn loop
1. `observe`; read `events` and your last action's result first.
2. Update the signal state, then `take_action` with the exact `choice` number and a short note: state, signal seen, response.
3. If `success` is false, pick an affordable option. Stop at `ending_score`.

## Signal state
Risk signal: warning, HR, compliance, complaint, audit or legacy-problem wording, a statistic warning, or a rising risk entry in `status_updates`.
- **Clear** (no recent risk signal): take the best visible trade-off; in quarterly phases lift a statistic that is falling or named in feedback, not simply the smallest number.
- **Raised** (one recent signal): Defuse legacy risk first in the next Energy phase. In story events prefer disclosing, fixing or closing a problem over postponing, hiding or shifting it.
- **Escalating** (repeated or stronger signals, or buried problems blowing up): as Raised, plus Defuse legacy risk every Energy phase, Lay low and reduce risk as main action unless a weak review plan is active, and no new story commitments, formal complaints or open escalations.
- Step down one state after a whole quarter without a new risk signal; a reassuring remark does not shorten that quarter.

## Weak review plan
After a C or D, or feedback that results fall short, until the next review: keep Apply for a key project as the main action (Repair a key relationship if the feedback names relationships) and spend spare Energy on Prepare report materials.
In the second Energy phase after a C or D, the last before the next review, take Defuse legacy risk and Prepare report materials whatever the signal state.

## Every quarter
Put at least one Energy point into Prepare report materials. Default main action: Apply for a key project. Use Network maintenance or Build a mentorship only when Network is falling or feedback names relationships.

Recovery overrides growth when Health or Dignity is low or named in a warning.
