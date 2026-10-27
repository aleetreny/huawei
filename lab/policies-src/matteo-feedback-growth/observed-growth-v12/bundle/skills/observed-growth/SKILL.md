---
name: observed-growth
description: Fills one fixed status line before every choice, reads the HR remark as the hidden-risk gauge, holds Skill, Network and Output at their level's requirements when each review is applied, and keeps the slow failure conditions away. Use for every decision of the run.
---

# Observed growth by status line

## How the game works
- **Promotion.** A review is applied at the very start of its month; what counts is your state after the last decision before it. It promotes when Skill, Network and Output are all high enough for your level and Dignity is not low. At the entry level Network and Output must sit at their ceilings, so one point lost just before the review costs the promotion. Staying at the entry level brings a warning, then dismissal.
- **Ceilings.** Each stat has a ceiling at each level; gains beyond it are lost. At higher levels Skill is what keeps you from the next promotion, so Skill gained early matters most.
- **Hidden risk.** The HR partner's monthly remark is the risk gauge: smiling is clear, then quiet, frowning, uneasy, angry. Each step up is closer to an explosion. An explosion costs Dignity, Wealth and the results built over the last half-year; a second one ends the run. Answers add or remove risk; a warning in a review talk adds some too.
- **Slow failures.** Wealth below zero, Network at zero or Dignity exhausted for several months ends the run. Escaping the condition once resets it.

## Each turn
1. `observe`. Read the statistics and the `events` feedback. Read the handbook once at the start for the review cycle.
2. Fill `Review: near or far | Below best: <stats or none> | HR: smiling, quiet, frowning, uneasy or angry | Health: ok or low | Wealth: ok or low`.
   - **Review near**: the next review comes before the next quarter-end allocation.
   - **Below best**: Skill, Network or Output under its best value at this level.
   - **Health low**: at or below the middle of its 0–10 range.
3. `take_action` with the exact `choice` number and the note "<status line> → need → why this option".
4. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.

## Story choices
- Never conceal or delay a problem, deny or misrepresent, gossip or leak, cut corners, bet that a known problem will not surface, overpromise or blame colleagues.
- **Honest without rigidity.** Among honest options, prefer one that keeps the other person on side without delaying your own work: brief help, raising it privately or in writing afterwards, refusing only the improper part.
- **HR not smiling**: also avoid steps that put you under formal scrutiny (signed complaints, formal investigations, stand-offs with management).
- **Review near**: rule out options that cost Network or Output, unless all do. If Output is Below best, prefer delivering your own result over side work.
- **Repair at once**: after losing Network or Output with the review near, the next choice restores it.
- Otherwise prefer options that build Skill (learning, quality, owning the fix) once Network and Output are at their best.
- **Wealth low**, or any level above the first two: avoid options that cost money; losses grow with level.
- Avoid options that cost Dignity when it is not high, and Health when Health is low.

## Quarter-end allocation
Energy, in order:
1. HR frowning or worse: Defuse legacy risk.
2. Health low: Health recovery.
3. Review near: Network maintenance or Prepare report materials for each Below best stat.
4. Otherwise Skill learning while Health is ok, then Health recovery.
Never High-intensity work. Spend all Energy.

Main action, never none:
- HR quiet or worse: Lay low and reduce risk (it lowers hidden risk).
- Review near with Network or Output Below best: Report results to your manager or Apply for a key project.
- Otherwise: Apply for rotation (Skill and lower risk); Repair a key relationship if Network is Below best.

## Endgame and warnings
- After a review warning, every choice until the next review serves the stats Below best.
- In the last half-year, bring HR back to smiling and Health and Dignity high: the ending counts them.
