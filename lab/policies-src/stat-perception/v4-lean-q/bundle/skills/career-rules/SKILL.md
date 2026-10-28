---
name: career-rules
description: "Use on every Career Survival turn. Keeps a one-line status note, reads every story option for likely stat changes and hidden risk, protects Skill, Network and Output in the month before a review, and sets quarterly Energy and main actions in priority order."
---

# Career rules

## How to use this Skill
- **Stories and quarterly phases are separate.** A story is decided only by "Story decisions" below. The quarterly list never picks a story option, and a story rule never picks an Energy or main action.
- Read this Skill again whenever its rules are no longer in view, for example after a summary or a resume.

## Plan for the 48 months
- Promotion needs Skill, Network and Output high enough for your level at a review; reviews come every six months. Early levels: keep all three at their best for each review. The handbook says higher levels set a higher bar; in this plan, from level 4 most quarterly Energy goes to Skill.
- Pay rises with level, so promotions are also the main source of Wealth. Avoid options that cost money, more so at higher levels.
- Hidden risk ends careers: keep the HR remark friendly. In the final quarter, recover Health and Dignity and lower risk.

## Turn loop
1. `observe` (once per story; once per quarterly phase, see below). Read `events` first: the monthly HR remark, the review talk, warnings. If your last note is not in view, call `check_latest_logs` with enough entries to find your most recent note and copy its status line.
2. Decide with the section for the current phase.
3. `take_action` with the exact `choice` and a short note: the status line, then at most one short reason. Do not write analysis outside the note; call the tools directly. If `success` is false, read the error, observe again and choose a valid option.

## Status line
Start every note with:
`Review in N | Now S<Skill> N<Network> O<Output> | Best S<..> N<..> O<..>`
- **Review in N:** months left until the next review month, N = 6 - (current_month mod 6), and N = 6 when current_month is a multiple of 6. Reviews come every six months; our plan treats the month with N = 1 as the deadline for review preparation.
- **Now:** Skill, Network and Output as `observe` shows them before this choice.
- **Best:** the highest value of each of the three you have seen at your current level (copy it from your last note and raise it when Now is higher). Reset it to Now when your level changes. A stat under its Best has lost ground since you last held it.

## Story decisions
Before choosing, read every option for the likely sign of its effect on Skill, Network, Output, Health, Dignity, Wealth and hidden risk. How options usually move them:
- **Skill** rises when you use your own judgement: analyse, bring data or evidence, prepare properly, think a decision through, learn, design a plan, negotiate with facts, coach someone with questions. This holds for options about people or pay too, not only code.
- **Output** rises when you deliver, ship, finish or cover the work, keep to your own deliverables or make your results visible. It falls when your time or credit goes elsewhere: learning, helping or organising for others, reviewing their work, giving the credit away, apologising and redoing, pausing a delivery, complaining instead of working. Output and Network often trade against each other.
- **Network** rises when you help, involve, credit or work with others; it falls when you confront, refuse, embarrass someone, go over their head or ignore them.
- **Dignity** rises when you act straight, stand your ground calmly, own a mistake or get credit; it falls when you are humiliated, cave in, get blamed or gossip.
- **Health** falls with overtime, weekends, extra load and stress; it rises with rest and boundaries. **Wealth** moves with pay, bonuses and money you spend.
- **Hidden risk** rises with hiding, denying, blaming, shortcuts, gambles, fixing things privately or off the record, anonymous moves, side deals, partial, phased or postponed fixes, skipping necessary work to save time, open conflict, ignoring a known problem, disengaging, and challenging the company, its culture, leaders or rules even through a formal channel. It falls when you document, report a concrete problem openly, follow the process, own a mistake at once or fix the problem fully. Our rule: when in doubt, treat an option as risky.

Then apply these steps in order. Skip a step if it would remove every option.
1. **Survive.** Drop any option that could end the run now, for example by taking Health to zero.
2. **Risk.** Drop options that may add hidden risk. If the latest HR remark is anything but the friendly one, or you have already chosen an option this month that might bury a problem, also drop options that keep a problem private, anonymous, partial, phased or for later, or skip work to save time, even when they solve the immediate problem; prefer an option that documents, reports, owns or fully fixes it. If every option looks risky, choose the smallest and most reversible risk.
   **Exception for the review month (N = 1) while the HR remark is friendly or quiet:** apply step 4 first. A mild risk (handling something privately, partially or later) is then acceptable when it is the only way to keep Skill, Network and Output, because a lost point there can cost the promotion. Hiding, denying, blaming, gambling and cutting corners stay out in every month.
3. **Wellbeing.** If Health or Dignity is low or falling, drop options that lower it.
4. **Review close (N = 1 or 2).** Promotions are lost here. With N = 2, drop options that may lower Network or Output. If Network or Output is under its Best, choose the honest option that most directly raises it back. With N = 1, apply all of this step. Drop options that may lower Skill, Network or Output: going against a person (blaming, correcting in public, refusing, reporting someone, going over a head) may cost Network; giving up time or credit from your own delivery (unplanned work, investigations, rework, the slow thorough path, someone else's problem) may cost Output; avoiding the work or the learning may cost Skill. Never save a point by hiding a problem or cutting a corner.
5. **Grow.** From the rest, choose the option that raises the most of Skill, Network and Output, counting twice a stat the latest review talk named as lagging, and minus one for each of them it lowers. In the final quarter of the career, prefer Health, Dignity and lower risk instead. On a tie: lower risk, then more Health and Dignity, then the option that costs no money.


## Quarterly phases only: first matching line wins
These lines choose Energy and main actions only, never a story option. You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost. Plan the whole quarter after one `observe`: the Energy choices and the main-action choices keep the same numbers every quarter. Call `take_action` for each Energy action in turn (a typical quarter is one 2-Energy action plus one 1-Energy action, or three 1-Energy actions), then for the main action, without observing in between. Observe again only if a call returns `success` false.
1. **Last quarter of the career (month 48):** plan Energy and the main action together. Energy: Defuse legacy risk once if the HR remark is not the friendly one, then Health recovery and Mental recovery while either is below full, then Network maintenance. Main action: Lay low and reduce risk if the HR remark is not the friendly one, otherwise Report results to your manager. No Skill learning or High-intensity work.
2. **Health or Dignity at 4 or below; or Network or Wealth near zero for months.** Recover first: Health recovery, Mental recovery, Network maintenance or Repair a key relationship, and avoid spending. No Skill learning or High-intensity work until it recovers. Health at zero ends the run.
3. **HR remark.** Friendly ("you are doing all right"): no risk action. Quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below. Anything else (frowning, uneasy, "you are on your own", angry): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is friendly or quiet again.
4. **A review talk named a lagging stat:** until the next review, spend Energy and the main action on it (Prepare report materials for Output, Network maintenance for Network, Skill learning for Skill; main action Apply for a key project, or Apply for rotation when it is Skill).
5. **Level 4 or above:** Skill learning plus one point on the weakest of Health, Dignity or Network; main action Apply for rotation.
6. **Otherwise:** spend Energy on Skill, Network and Output (Prepare report materials, Network maintenance, Skill learning while Health is above 4). Main action Apply for a key project, which raises all three.
