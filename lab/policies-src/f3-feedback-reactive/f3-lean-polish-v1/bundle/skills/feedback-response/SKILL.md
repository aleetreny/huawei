---
name: feedback-response
description: Chooses every story option, Energy action and quarterly main action from risk warnings and review grades. Use on every turn, right after observe and before take_action.
---

## Turn loop
1. Call `observe` once; read `events` and your last action's result first.
2. Set the risk state, then `take_action` with the exact `choice` number and a note of a few words: state, signal, response.
3. If `success` is false, pick an affordable option. Stop at `ending_score`.

## Risk state
Judge by meaning, not wording. A risk signal is any warning or HR, compliance, complaint, audit or legacy-problem wording, a statistic warning, or a rising risk entry in `status_updates`.
- **Clear**: no recent signal. **Raised**: one recent signal. **Escalating**: repeated or stronger signals.
- Step down one state after a whole quarter without a new signal.

## Decide by turn type
**Always first:** when Health or Dignity is low or named in a warning, recovery overrides growth.

**Story event**
- Clear: the best visible trade-off.
- Raised or Escalating: disclose, fix or close a problem rather than postpone, hide or shift it. Escalating: take no new commitments.

**Energy phase**
- Raised: Defuse legacy risk first. Escalating: Defuse legacy risk every phase.
- Weak review plan active: spare Energy on Prepare report materials.
- Otherwise lift the weakest statistic.

**Main action**
1. Weak review plan active: the factor named. Results: Report results to your manager. Capability: Build a mentorship. Relationships: Repair a key relationship.
2. Escalating: Lay low and reduce risk.
3. Otherwise lift the weakest statistic.

## Weak review plan
Starts after a C or D, or feedback that results fall short; lasts until the next review. These rules apply for the whole career.
