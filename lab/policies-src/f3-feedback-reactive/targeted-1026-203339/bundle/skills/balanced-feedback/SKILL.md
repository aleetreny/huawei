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

## Story costs
Promotion looks at Skill, Network and Output as they stand at each review; between Energy phases only stories move them. Each stops at a ceiling for your level until promotion, and is **full** once a choice that should raise it leaves it unchanged. At the entry level all three fill early, so a point a story takes is missing at the review unless a later story or Energy phase wins it back. Options that look free or useful often cost one:
- **Output** falls when work time goes anywhere but your own deliverables: rest while work waits, side reviews, notes for others, extra meetings, learning on the job, asking for less work. Finishing or showing your own work raises it.
- **Network** falls when you turn down, correct or go over the head of a colleague; helping, including or thanking one raises it.
- **Skill** falls when you pass up a chance to learn.

## Priorities
1. **Protect.** Health or Dignity in the lower part of its 0–10 range, or named in a warning: Health recovery or Mental recovery first. Keep Network and Wealth above zero.
2. **Risk.** Raised: Defuse legacy risk first in the next Energy phase. Escalating: Defuse legacy risk every Energy phase; main action Lay low and reduce risk or Repair a key relationship, whichever fits; no new commitments. In stories prefer disclosing, fixing or closing a problem over postponing, hiding or shifting it.
3. **Review.** After a weak review, aim the main action at the factor the feedback names until the next review: Report results to your manager or Showcase results for results; Build a mentorship or Apply for rotation for capability; Repair a key relationship for relationships. Spare Energy: Prepare report materials. If the next grade is still weak, change the factor.
4. **Balance** (default). Lift the weakest or falling of Skill, Network and Output that is not full; a full one is not weak, however small its number.
   - Story: avoid downsides on protected dimensions, Skill, Network and Output included (see Story costs); prefer helping the weakest, and a modest gain over a large one with a lasting cost. If the honest option costs one, take it and win the point back at the next chance; never hide or postpone a problem, cut a corner or bend a rule to keep one.
   - Energy: spread points; use Skill learning or High-intensity work only while Health is comfortable; spend all Energy.
   - Main action: cover gaps Energy missed; rotate rather than repeat.

Near the end, avoid choices that add unresolved risk.
