---
name: balanced-feedback
description: Balanced play by default, with specific responses when warnings, risk hints or weak reviews signal trouble. Use for every decision, after observe.
---

# Balanced play, feedback first

Read feedback first; it shows trouble before the statistics do.

## Each turn
1. `observe`. Read `events`, the event text and your last action's result, then each statistic's direction.
2. Set the signal state; apply the priorities in order.
3. `take_action` with the exact `choice` number and a short note: state, signal or weakest input with room, reason. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.
4. Use `check_latest_logs` only when a warning cites earlier decisions you cannot see.

## Signals
- **Risk**: warning, HR, compliance, complaint, audit or legacy-problem wording; a statistic warning; a rising risk entry in `status_updates`.
- **Weak review**: grade C or D, or comments that results fall short.
- State: **Clear** (no recent risk signal), **Raised** (one), **Escalating** (repeated or stronger). Step down one state only after a whole quarter without a new risk signal.

## Priorities
1. **Protect.** Health or Dignity in the lower part of its 0–10 range, or named in a warning: Health recovery or Mental recovery first. Keep Network and Wealth above zero.
2. **Risk.** Raised: Defuse legacy risk first in the next Energy phase. Escalating: Defuse legacy risk every Energy phase; main action Lay low and reduce risk or Repair a key relationship, whichever fits; no new commitments. In stories prefer disclosing, fixing or closing a problem over postponing, hiding or shifting it.
3. **Review.** After a weak review, aim the main action at the factor the feedback names until the next review: Report results to your manager or Showcase results for results; Build a mentorship or Apply for rotation for capability; Repair a key relationship for relationships. Spare Energy: Prepare report materials. If the next grade is still weak, change the factor.
4. **Balance** (default). Lift the weakest or falling of Skill, Network and Output, counting only those with room to grow.
   - **Room.** If an action aimed at an input leaves it unchanged, that input is full for your level: spend nothing more on it unless it drops, and test it again after a promotion. Judge the weakest by room left, not by size: at higher levels Output and Network often fill up while Skill is still climbing, and the next promotion then waits on Skill.
   - Story: avoid downsides on protected dimensions; prefer helping the weakest, and a modest gain over a large one with a lasting cost.
   - Energy: spread points; use Skill learning or High-intensity work only while Health is comfortable; spend all Energy.
   - Main action: cover gaps Energy missed; rotate rather than repeat. If Skill alone has room, take the main action listing the largest Skill gain, usually Apply for rotation, even if that repeats it.

Near the end, avoid choices that add unresolved risk.
