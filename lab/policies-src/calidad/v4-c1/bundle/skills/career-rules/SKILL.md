---
name: career-rules
description: "Career Survival strategy for every turn of the 48-month run: how to choose story options and quarterly Energy and main actions, keep a one-line status note, protect the next promotion review, and recover when a stat nears a failure limit. Open it at the start of the run and whenever its rules are no longer in view."
---

# Career rules

## How to use this Skill
- **Stories and quarterly phases are separate.** A story is decided only by "Story decisions" below. The quarterly list never picks a story option, and a story rule never picks an Energy or main action.
- Read this Skill again whenever its rules are no longer in view, for example after a summary or a resume.
- **What is published and what is ours.** The handbook publishes the levels, the six-monthly promotion reviews, the quarterly actions and their directions, pay and the failure directions; it does not publish formulas, thresholds or hidden-risk conditions. Lines below that say how options "usually" move a stat are our working assumptions for reading option text, not game rules. Trust what the game shows you (stat changes, the HR remark, review talks and warnings) over them.

## The 48 months at a glance
- **Every review (every six months).** Promotion is decided at the half-year review from Skill, Network and Output, and it is easy to lose by a point in the last month before it. Prepare from two months out and protect the three stats in the last month (Story step 4).
- **Throughout.** Keep the HR remark friendly: hidden risk that builds up blows up and costs half a year of results; a second blow-up ends the run. Keep Health and Dignity away from the bottom of their range, Wealth above zero and Network above zero: each is a published failure direction.
- **Growing.** Between review deadlines, grow the stats the next review needs, and stop paying for a stat whose expected rise no longer shows (Stalled).
- **Final quarter (month 46 on).** No promotion review is left to prepare. The ending evaluation counts level, wealth, health and dignity, skill, risk control and network, so lower risk and raise Health and Dignity instead of chasing growth.

## Turn loop
1. `observe`. Read `events` first: the monthly HR remark, the review talk, warnings. If your last note is not in view, call `check_latest_logs` with enough entries to find your most recent note and copy its status line.
2. Decide with the section for the current phase: a story offers options about a situation; a quarterly phase offers Energy actions (with their Energy cost) or main actions.
3. `take_action` with the exact `choice` and a note that starts with the status line, then one short reason. Keep the note well under 1,000 characters. If `success` is false, read the error, observe again and choose a valid option.

## Status line
The note is your memory: it survives summaries and comes back through `check_latest_logs`. Start every note with:
`Review in N | Now S<Skill> N<Network> O<Output> | Best S<..> N<..> O<..> | Stalled: none | Concerns this month: 0`
- **Review in N:** N = 6 - (current_month mod 6), and N = 6 when current_month is a multiple of 6. Reviews come every six months (handbook); N = 1 is the last month before a review, the deadline for review preparation in our plan.
- **Now:** Skill, Network and Output as `observe` shows them before this choice. If you cannot find your last note, rebuild the line from `observe`: Best = Now, Stalled: none.
- **Best:** the highest value of each of the three you have seen at your current level (copy it from your last note and raise it when Now is higher). Reset it to Now when your level changes. A stat under its Best has lost ground since you last held it.
- **Stalled:** a provisional record of an expected gain that did not show up in this run. In a quarterly phase, add `Expect S<..> N<..> O<..>`: the values the chosen action should leave, from its displayed changes. At the next quarterly choice, if the previous note describes that action and nothing else intervened, a stat still below its `Expect` value goes into Stalled. While a stat is in Stalled, prefer another useful investment over paying again for it. The same check works in stories: if your last story choice was one you read as raising a stat and Now shows no rise in it, add that stat to Stalled. Clear the list when your level changes, or when later observations show the stat rising again.
- **Concerns this month:** how many of this month's story choices you judged might bury a problem. Start each month at 0. It records your judgement, not the hidden risk itself.

## Story decisions
Before choosing, read every option for the likely sign of its effect on Skill, Network, Output, Health, Dignity, Wealth and hidden risk. The game does not publish these effects; these are our working assumptions for reading option text, and the changes the game shows after a choice come first:
- **Skill** rises when you use your own judgement: analyse, bring data or evidence, prepare properly, think a decision through, learn, design a plan, negotiate with facts, coach someone with questions. This holds for options about people or pay too, not only code.
- **Output** rises when you deliver, ship, finish or cover the work, keep to your own deliverables or make your results visible. It falls when your time or credit goes elsewhere: learning, helping or organising for others, reviewing their work, giving the credit away, apologising and redoing, pausing a delivery, complaining instead of working. Output and Network often trade against each other.
- **Network** rises when you help, involve, credit or work with others; it falls when you confront, refuse, embarrass someone, go over their head or ignore them.
- **Dignity** rises when you act straight, stand your ground calmly, own a mistake or get credit; it falls when you are humiliated, cave in, get blamed or gossip.
- **Health** falls with overtime, weekends, extra load and stress; it rises with rest and boundaries. **Wealth** moves with pay, bonuses and money you spend.
- **Hidden risk** (not shown; the HR remark is your only gauge) is likely to rise with hiding, denying, blaming, shortcuts, gambles, fixing things privately or off the record, anonymous moves, side deals, partial, phased or postponed fixes, skipping necessary work to save time, open conflict, ignoring a known problem, disengaging, and challenging the company, its culture, leaders or rules even through a formal channel. It is likely to fall when you document, report a concrete problem openly, follow the process, own a mistake at once or fix the problem fully. Missing a risky option costs far more than flagging a safe one: when in doubt, treat it as risky.

Then apply these steps in order. Skip a step if it would remove every option.
1. **Survive.** Drop any option that could end the run now, for example by taking Health to zero.
2. **Risk.** Drop options that may add hidden risk. If the latest HR remark is anything but the friendly one, or Concerns this month is 1 or more, also drop options that keep a problem private, anonymous, partial, phased or for later, or skip work to save time, even when they solve the immediate problem; prefer an option that documents, reports, owns or fully fixes it. If every option looks risky, choose the smallest and most reversible risk.
   **Exception for the last month before a review (N = 1) while the HR remark is friendly or quiet:** apply step 4 first. A mild risk (handling something privately, partially or later) is then acceptable when it is the only way to keep Skill, Network and Output, because a lost point there can cost the promotion. Hiding, denying, blaming, gambling and cutting corners stay out in every month.
3. **Wellbeing.** If Health or Dignity is low or falling, drop options that lower it.
4. **Review close (N = 1 or 2).** Promotions are lost here. With N = 2, drop options that may lower Network or Output. If Network or Output is under its Best, choose the honest option that most directly raises it back. With N = 1, apply all of this step. Drop options that may lower Skill, Network or Output: going against a person (blaming, correcting in public, refusing, reporting someone, going over a head) may cost Network; giving up time or credit from your own delivery (unplanned work, investigations, rework, the slow thorough path, someone else's problem) may cost Output; avoiding the work or the learning may cost Skill. Never save a point by hiding a problem or cutting a corner.
5. **Grow.** From the rest, choose the option that raises the most of Skill, Network and Output that are not in Stalled, counting twice a stat the latest review talk named as lagging, and minus one for each of them it lowers. In the final quarter of the career, prefer Health, Dignity and lower risk instead. On a tie: lower risk, then more Health and Dignity, then the option that costs no money.

After choosing, add 1 to Concerns this month if the chosen option might bury a problem.

## Quarterly phases only: first matching line wins
These lines choose Energy and main actions only, never a story option. You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost. Choose one affordable Energy action at a time, then observe again.
1. **Last quarter of the career (month 48):** plan Energy and the main action together. Energy: Defuse legacy risk once if the HR remark is not the friendly one, then, with the Energy left, Health recovery and Mental recovery while either is below full, then Network maintenance. Main action: Lay low and reduce risk if the HR remark is not the friendly one, otherwise Report results to your manager. No Skill learning or High-intensity work.
2. **Health or Dignity in the lower part of its 0–10 range, or falling for several months; or Network or Wealth near zero for months.** Recover first: Energy on Health recovery, Mental recovery or Network maintenance, main action Repair a key relationship (or Lay low and reduce risk for Health), and avoid spending. No Skill learning or High-intensity work until it recovers. Health at zero ends the run.
3. **HR remark.** Friendly ("you are doing all right"): no risk action. Quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below. Anything else (frowning, uneasy, "you are on your own", angry): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is friendly or quiet again.
4. **A review talk named a lagging stat:** until the next review, spend Energy and the main action on it (Prepare report materials for Output, Network maintenance for Network, Skill learning for Skill; main action Apply for a key project, or Apply for rotation when it is Skill).
5. **Network and Output both in Stalled:** Skill learning plus one point on the weakest of Health, Dignity or Network; main action Apply for rotation.
6. **Otherwise:** spend Energy on Skill, Network and Output that are not in Stalled (Prepare report materials, Network maintenance, Skill learning while Health is comfortable). Main action Apply for a key project; if two of the three are in Stalled, the main action that raises the third (Apply for rotation for Skill, Build a mentorship for Network, Showcase results for Output); if all three are, Energy on Health and Dignity and the main action Report results to your manager.
