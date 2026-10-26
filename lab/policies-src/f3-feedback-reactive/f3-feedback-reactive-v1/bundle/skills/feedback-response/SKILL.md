---
name: feedback-response
description: Turns warnings, HR or risk hints, review grades and the outcomes of earlier actions into the next decisions, including defusing accumulated risk and a corrective plan after a weak review. Use on every turn, right after observe and before choosing.
---

# Feedback response

The run's own feedback can reveal risk before the statistics show it. Treat feedback as the primary signal.

## Turn loop
1. `observe`. Read `events`, the event description and the result of your last action before reading the choices.
2. Update the signal state below, then decide.
3. `take_action` with the exact `choice` number and a note: signal state, signal seen, response. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.
4. Call `check_latest_logs` with a small count only when a warning refers to earlier decisions you cannot see, to find which choice caused it.

## Signals
- **Risk**: warning, HR, compliance, complaint, audit or legacy-problem wording; a statistic warning; a quarterly option whose `status_updates` shows a risk entry increasing.
- **Performance**: the review grade and its comments. S, A and B are acceptable; C and D are weak.
- **Outcome**: what your last choice actually changed, compared with what you expected.

Signal state: **Clear** (no recent risk signal), **Raised** (one recent signal), **Escalating** (repeated or stronger signals, or a statistic warning together with another signal).

## Responses
- **Clear**: play balanced. In story events take the option with the best visible trade-off; in quarterly phases lift the weakest of Health, Dignity, Skill, Network and Output.
- **Raised**: in the next Energy phase spend on Defuse legacy risk first. In story events prefer options that disclose, fix or close a problem over options that postpone, hide or shift it.
- **Escalating**: Defuse legacy risk in every Energy phase; choose Lay low and reduce risk or Repair a key relationship as the main action, whichever matches the signal; take no new commitments in story events.
- Step down one state only after a whole quarter without a new risk signal.

## Weak review plan
After a C or D, or comments that results fall short:
1. Name the factor the feedback points to: results, capability or relationships.
2. Until the next review aim the main action at it: Report results to your manager or Showcase results for results; Build a mentorship or Apply for rotation for capability; Repair a key relationship for relationships.
3. Spend spare Energy on Prepare report materials, keeping recovery first when Health or Dignity is low.
4. If the next grade is still weak, change the factor instead of repeating the plan.

## Limits
Recovery overrides growth when Health or Dignity is in the lower part of its 0–10 range or a warning names it. Keep Network and Wealth above zero. Apply the same rules all run; near the end, avoid any choice that adds unresolved risk.
