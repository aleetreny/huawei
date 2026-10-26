---
name: career-decisions
description: Makes every decision of the run in three parts - a risk review before each decision, story-event choices, and quarterly Energy and main-action planning. Use on every turn from the start of the run to the ending.
---

# Career decisions

## Risk review
Do this before every decision.
1. `observe`. Read Level, the statistics, the `events` feedback and the result of the last action.
2. Mark a dimension at risk when Health or Dignity is in the lower part of its 0–10 range or falling, when Network or Wealth is near zero, when a warning names it, or, for Output, after a C or D review.
3. Note any warning about accumulated or legacy risk.
4. Act with `take_action`, the exact `choice` number and a short note naming the dimensions at risk. If `success` is false, observe and pick a valid option. Stop when `ending_score` appears.
5. Call `check_latest_logs` with a small count only after a context reset, or when a warning refers to a decision you cannot see.

## Story decisions
1. Rule out options whose described downside worsens a dimension at risk, unless all do; then take the mildest downside.
2. Prefer options that keep commitments honest and workable and that help the weakest dimension.
3. Between similar options, prefer the one that builds Skill, Network or visible Output without a lasting cost.

## Quarterly planning
1. Read `energy_cost`, `status_updates` and `remaining_energy` in the current observation.
2. Energy: first the recovery action for each dimension at risk (Health recovery, Mental recovery, Network maintenance); Defuse legacy risk after a risk warning; then growth, such as Prepare report materials, or Skill learning while Health is comfortable. Spend all Energy while a useful affordable action remains.
3. Main action: cover the weakest dimension that Energy did not reach. After a C or D review prefer Report results to your manager or Showcase results. Choose Lay low and reduce risk only when Health is at risk.
4. Keep the same rules all run; near the end, avoid new risks.
