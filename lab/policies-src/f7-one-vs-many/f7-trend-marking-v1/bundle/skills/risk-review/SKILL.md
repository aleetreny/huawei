---
name: risk-review
description: Marks the dimensions at risk. Use first on every turn, before story-decisions or quarterly-planning.
---

# Risk review

1. `observe`. Read Level, the statistics, the `events` feedback and the result of the last action.
2. Mark a dimension at risk when a warning names it; Health or Dignity when in the lower part of its 0–10 range or falling; Network or Wealth when near zero; Skill, Network or Output when below its recent high. Judge these three by trend, not by size or by a review grade.
3. Note any warning about accumulated or legacy risk.
4. Act with `take_action`, the exact `choice` number and a short note naming the dimensions at risk. If `success` is false, observe and pick a valid option. Stop when `ending_score` appears.
5. Use `check_latest_logs`, with a small count, only after a context reset.
