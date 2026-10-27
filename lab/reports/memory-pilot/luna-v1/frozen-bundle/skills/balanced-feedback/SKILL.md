---
name: balanced-feedback
description: Balanced play by default, with specific responses when warnings, risk hints or weak reviews signal trouble. Use for every decision, after observe.
---

# Balanced play, feedback first

Read feedback first; it shows trouble before the statistics do.

## Each turn
1. `observe`. Read `events`, the event text and your last action's result, then each statistic's direction.
2. Set the signal state; apply the priorities in order.
3. `take_action` with the exact `choice` number and a short note: state, signal or weakest dimension, reason. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.
4. Use `check_latest_logs` only when a warning cites earlier decisions you cannot see.

## Signals
- **Risk**: warning, HR, compliance, complaint, audit or legacy-problem wording; a statistic warning; a rising risk entry in `status_updates`.
- **Weak review**: grade C or D, or comments that results fall short.
- State: **Clear** (no recent risk signal), **Raised** (one), **Escalating** (repeated or stronger). Step down one state only after a whole quarter without a new risk signal.

## Priorities
1. **Protect.** Health or Dignity in the lower part of its 0–10 range, or named in a warning: Health recovery or Mental recovery first. Keep Network and Wealth above zero.
2. **Risk.** Raised: Defuse legacy risk first in the next Energy phase. Escalating: Defuse legacy risk every Energy phase; main action Lay low and reduce risk or Repair a key relationship, whichever fits; no new commitments. In stories prefer disclosing, fixing or closing a problem over postponing, hiding or shifting it.
3. **First promotion.** Until you are first promoted, keep Output and Network in stories: promotion depends on them as well as Skill, and a point given away is hard to win back before the review. Do not trade them for what you are not short of: putting work off for rest or exercise while Health is comfortable, or slowing delivery to learn once Skill has stopped rising. If Health slips, recover it in the next Energy phase. Never hide or postpone a problem to keep them.
4. **Review.** After a weak review, aim the main action at the factor the feedback names until the next review: Report results to your manager or Showcase results for results; Build a mentorship or Apply for rotation for capability; Repair a key relationship for relationships. Spare Energy: Prepare report materials. If the next grade is still weak, change the factor.
5. **Balance** (default). Lift the weakest or falling of Skill, Network and Output.
   - Story: avoid downsides on protected dimensions; prefer helping the weakest, and a modest gain over a large one with a lasting cost.
   - Energy: spread points; use Skill learning or High-intensity work only while Health is comfortable; spend all Energy.
   - Main action: cover gaps Energy missed; rotate rather than repeat.

Near the end, avoid choices that add unresolved risk.

## Compact current-run memory
Keep a short record in the existing action note alongside the state and reason: past serious incidents; open commitment and next step; latest review weakness; last investment and observed payoff. A calmer warning does not erase incident history. Close commitments only on evidence. If context is missing, recover the latest available record from a few public logs; mark missing facts unknown. Rewrite the current summary, not a diary. Do not carry information between games.
