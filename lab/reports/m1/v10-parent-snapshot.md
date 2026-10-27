---
name: observed-growth
description: Fills one fixed status line before every choice, holds Skill, Network and Output at their ceilings when each review is applied, keeps hidden risk and Dignity safe, and stops spending on stats that are already capped. Use for every decision of the run.
---

# Observed growth by status line

## How promotion works
- A review is applied at the very start of its month, before that month's events and quarter-end allocation. What counts is your state right after the last decision before it.
- It promotes when Skill, Network and Output are all high enough for your level and Dignity is not low. At the entry level, Network and Output must sit at their ceilings, so one point lost in the decisions just before the review costs the promotion. Built-up hidden risk makes promotion less likely.
- Each stat has a ceiling at each level; gains beyond it are lost. A stat that stops rising when an action should raise it is at its ceiling.
- Staying at the entry level brings weaker reviews and a warning that the next review must be better; after that warning, the next review decides survival.

## Each turn
1. `observe`. Read the statistics and the `events` feedback. Read the handbook once at the start for the review cycle.
2. Fill the status line `Review: near or far | Below best: <stats or none> | Capped: <stats or none> | Risk: calm or raised | Health: ok or low`.
   - **Review near**: the next review comes before the next quarter-end allocation.
   - **Below best**: Skill, Network or Output under its best value at this level.
   - **Capped**: stats that did not rise when an action should have raised them.
   - **Risk raised**: the HR remark is anything but calm, or a warning or incident appeared since the last allocation.
   - **Health low**: Health at or below the middle of its 0–10 range.
3. `take_action` with the exact `choice` number and the note "<status line> → need → why this option".
4. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.

## Story choices
- Never conceal or delay a problem, deny or misrepresent, gossip or leak, cut corners, bet that a known problem will not surface, overpromise or blame colleagues.
- **Honest without rigidity.** Among honest options, prefer one that keeps the other person on side without delaying your own work: brief or time-boxed help, raising it privately or in writing afterwards, refusing only the improper part. Refuse, block or take a public stand only when no such option is honest.
- **Review near**: rule out options whose downside hits Network or Output, unless all do; then the mildest. If Output is Below best, prefer delivering or showing your own result over side work, coaching or rework.
- **Repair at once**: if Network or Output dropped while the review is near, the next story choice is the honest option that most directly restores it.
- **Risk raised**: also avoid steps that put you under formal scrutiny (signed complaints, formal investigations, stand-offs with management) until risk is calm again.
- **Capped stats**: prefer options that build what is not capped; when Network and Output are capped, choose learning, quality and owning the fix.
- Avoid options that cost money while Wealth is low, and options that cost Dignity when Dignity is not high.
- **Health low**: rule out options that cost Health, unless all do.

## Quarter-end allocation, in order
1. **Risk raised**: Defuse legacy risk.
2. **Health low**: Health recovery.
3. **Review near**: lift each Below best stat: Network maintenance, Prepare report materials, Skill learning if Health is ok. Main action: Report results to your manager or Apply for a key project.
4. **Review far**: build what is not capped. Never spend on a Capped stat.
   - Skill not capped: Skill learning while Health is ok; main action Apply for rotation (the largest Skill gain), else Build a mentorship.
   - Network or Output not capped: Network maintenance or Prepare report materials; main action Apply for a key project.
   - Once Network and Output are both capped, Skill is the only blocker: rotation every quarter and Skill learning whenever Health allows; spare Energy on Health recovery.
Avoid High-intensity work. Spend all Energy; unused Energy is lost. Lay low only when Health is low and nothing else is affordable.

## After a weak review or a warning
Every allocation until the next review lifts Below best stats and visible Output. In pay or role talks, cite actual results and ask for concrete terms.
