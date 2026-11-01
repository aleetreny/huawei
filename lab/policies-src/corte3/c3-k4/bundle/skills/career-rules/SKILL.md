---
name: career-rules
description: "Use on every Career Survival turn. Keeps a one-line status note, reads every story option for likely stat changes and hidden risk, protects Skill, Network and Output before each six-monthly review, keeps the HR remark friendly when the starting level has stalled, and sets quarterly Energy and main actions in priority order, including what to do when Health, Dignity, Wealth, Network or the HR remark nears a limit."
---

# Career rules

## How to use this Skill
- **Stories and quarterly phases are separate.** A story is decided only by "Story decisions" below. The quarterly list never picks a story option, and a story rule never picks an Energy or main action.
- **Priorities, in order:** stay in the run (no stat at a failure limit, no second hidden-risk blow-up), then win the next promotion review, then grow. Pay rises with level, so an earlier promotion is also the main source of Wealth.
- **Published and ours.** The handbook publishes the levels, the six-monthly reviews, the quarterly actions and their directions, pay, grades and the failure directions; it does not publish thresholds, formulas or hidden-risk conditions. Anything below said to happen "in our runs" or "usually" is our own observation, not a game rule: when the game shows something else (stat changes, the HR remark, review talks, warnings), follow the game.
- Read this Skill again whenever its rules are no longer in view, for example after a summary or a resume.

## The 48 months at a glance
| Phase | Goal | How |
| --- | --- | --- |
| Starting level, first two reviews | Promotion at month 6, else month 12 | Fill Skill, Network and Output; in the two months before each review, keep Network and Output at their Best (Story step 4). A mild risk is acceptable there when it is the only way to keep them (Story step 2). |
| Starting level, stalled (two reviews without promotion) | Promotion at the third review | Hidden risk to zero and kept there until the review, with Network and Output at their Best (Story step 2, Quarterly line 3). |
| Levels 2 and 3 | Promotion at every review | Balanced growth of Skill, Network and Output; the same review protection. |
| Level 4 and above | Skill, then Output | The handbook says higher levels set a higher bar; in our runs Skill, then Output, held back most promotions from level 4: the quarter buys Skill (Quarterly line 6). |
| Last quarter (month 48) | Keep what you have | Lower risk, raise Health and Dignity, no new growth spending (Quarterly line 1). |

**Review calendar.** Reviews come every six months (handbook). The handbook lists the review after the quarterly phase; in our runs the half-year talk, the bonus and any promotion appeared among the events as months 6, 12, 18 … 48 began, judged on the stats held at that moment. This Skill therefore treats months 5, 11, 17 … 47 as review months (Review in 1). If month 6 (12, 18 …) begins without the review talk in view, keep the Review in 1 protection through that month too.

**Throughout.** Keep the HR remark friendly. The handbook shown as the opening screen of the run says old landmines go off at once and wipe out half a year of work, that a second blow-up ends the run in a trust crisis, and that two weak half-year reviews end it by dismissal. Keep Health and Dignity off the bottom of their 0–10 range and Wealth and Network above zero: each is a published failure direction.

## Turn loop
Every call resends the whole conversation, so the run stays within budget only if each decision costs one reply: tool calls in one reply run in order, and every result comes back before your next turn.
**Set the pattern in your first three replies and keep it:** reply 1 is `new_game`; reply 2 is `observe`; reply 3 answers the opening screen (the handbook notice, choice 1 "Continue") already as the pair `take_action` + `observe` in one reply. From then on every story reply carries the pair, whatever else it contains.
1. `observe` once. Read `events` first: the monthly HR remark, the review talk, warnings. If your last note is not in view (after a summary or a resume), call `check_latest_logs` with a small count, enough to find your most recent note, and copy its status line. This Skill already holds what you need from the handbook, so do not call `show_employee_handbook`.
2. Decide silently with the section for the current phase: a story offers options about a situation; a quarterly phase offers Energy actions (with their Energy cost) or main actions. Write no analysis if you can; if you do write, keep it to one short line, and send both calls in that same reply all the same: the pair never depends on the text.
3. **Story: one reply with exactly two tool calls**, `take_action` (the exact `choice` and the one-line note) and then `observe`, which returns the next situation together with the result of the action. Never send `take_action` alone, and never send `observe` in a reply of its own, from the Continue screen to the last month. **Quarterly phase: two replies in the first quarter of the run, one reply from the second on.** The `observe` that opens the quarter shows the Energy menu: reply with `take_action` for each Energy action in turn (a typical quarter is one 2-Energy action plus one 1-Energy action, or three 1-Energy actions) and then `observe`, which shows the main-action menu; reply with `take_action` for the main action and `observe`. Write the choice numbers of both menus in that quarter's note. From the second quarter on, the menus are the ones you have already seen in this run, so send the whole quarter in one reply: the Energy actions, the main action and `observe`. If a result reports `success` false, `observe` and continue from what it shows.
   The shape of every story reply, with no text around it:
   ```
   tool_calls: [
     take_action(session_id="<id>", choice=<n>, notes="Review in N | Now S.. N.. O.. | Best S.. N.. O.. | Reviews here: 0 | <short reason>"),
     observe(session_id="<id>")
   ]
   ```
4. If a call returns `success` false, read the error, `observe` again and choose a valid option.

## Status line
The note is your memory: it survives summaries and comes back through `check_latest_logs`. Every note is one line: the status line, then at most one short reason.
`Review in N | Now S<Skill> N<Network> O<Output> | Best S<..> N<..> O<..> | Reviews here: 0`
- **Review in N:** N = 6 - (current_month mod 6), and N = 6 when current_month is a multiple of 6. Reviews come every six months (handbook); N = 1 is the last month before a review, the deadline for review preparation in our plan.
- **Now:** Skill, Network and Output as `observe` shows them before this choice. If you cannot find your last note, rebuild the line from `observe`: Best = Now, Reviews here = 0.
- **Best:** the highest value of each of the three you have seen at your current level (copy it from your last note and raise it when Now is higher). Reset it to Now when your level changes. A stat under its Best has lost ground since you last held it.
- **Reviews here:** how many half-year review talks you have received at your current level without a promotion, counting the one that arrived this month. Add 1 when a review talk arrives and your level has not changed; reset it to 0 when you are promoted. At your starting level, 2 means the stalled-start rule applies.

## Story decisions
Before choosing, read every option for the likely sign of its effect on Skill, Network, Output, Health, Dignity, Wealth and hidden risk. The game does not publish these effects; the cues below are our working assumptions, and the changes the game shows after a choice come first:
- **Skill** rises when you use your own judgement: analyse, bring data or evidence, prepare properly, think a decision through, learn, design a plan, negotiate with facts, coach someone with questions. This holds for options about people or pay too, not only code.
- **Output** rises when you deliver, ship, finish or cover the work, keep to your own deliverables or make your results visible. It falls when your time or credit goes elsewhere: learning, helping or organising for others, reviewing their work, giving the credit away, apologising and redoing, pausing a delivery, complaining instead of working. Output and Network often trade against each other.
- **Network** rises when you help, involve, credit or work with others; it falls when you confront, refuse, embarrass someone, go over their head or ignore them.
- **Dignity** rises when you act straight, stand your ground calmly, own a mistake or get credit; it falls when you are humiliated, cave in, get blamed or gossip.
- **Health** falls with overtime, weekends, extra load and stress: taking on more work, a rewrite or a thorough fix on top of the job, a course or certification, late events, travel, covering for others; it rises with rest and boundaries. **Wealth** moves with pay, bonuses and money you spend.
- **Hidden risk** (not shown; the HR remark is your only gauge) is likely to rise with hiding, denying, blaming, shortcuts, gambles, fixing things privately or off the record, anonymous moves, side deals, partial, phased or postponed fixes, skipping necessary work to save time, open conflict, ignoring a known problem, disengaging, and challenging the company, its culture, leaders or rules even through a formal channel. It is likely to fall when you document, report a concrete problem openly, follow the process, own a mistake at once or fix the problem fully. Missing a risky option costs far more than flagging a safe one: when in doubt, treat it as risky.

Then apply these steps in order. Skip a step if it would remove every option.
1. **Survive.** Drop any option that could end the run now, for example by taking Health to zero.
2. **Risk.** Use the first of these cases that applies.
   - **Stalled start** (Reviews here is 2 at your starting level, or Months at current level is 12 or more there: two six-month review periods). The opening handbook says two weak half-year reviews end a run. In our runs a career in this case got a very weak grade at its third review unless the HR remark was the friendly one, was promoted when it was friendly and Network and Output were at their Best, and was dismissed at month 24 otherwise. Until that review, in this order: (a) drop every option that may add hidden risk, in any month and whatever it saves, including private, partial, phased, postponed or temporary fixes; (b) apply step 4 as at N = 1 to the rest, to keep Skill, Network and Output; (c) among what is left, prefer the option that documents, reports, follows the process or fixes fully.
   - **Review exception** (not a stalled start, the HR remark is friendly or quiet, and N = 1 at any level, or N = 1 or 2 at your starting level): apply step 4 first. A mild risk (handling something privately, partially or later) is then acceptable when it is the only way to keep Skill, Network and Output, because a lost point there can cost the promotion. Hiding, denying, blaming, gambling and cutting corners stay out in every month.
   - **Strict mode** (the latest HR remark is anything but the friendly one, or you already chose an option this month that might bury a problem): drop options that may add hidden risk and also those that keep a problem private, anonymous, partial, phased or for later, or skip work to save time, even when they solve the immediate problem; prefer an option that documents, reports, owns or fully fixes it.
   - **Otherwise:** drop options that may add hidden risk.
   - In every case, if every option looks risky, choose the smallest and most reversible risk.
3. **Wellbeing.** If Health is 3 or below (our margin on the published 0–10 range), drop every option that may lower Health, in any month and before step 4: overtime, night or weekend work, extra load, a rewrite, thorough fix or certification on top of the job, late events, stress. One such option can cost two points, and Health at zero ends the run at once. If Health or Dignity is 4 or below (our margin) or has fallen for several months, drop options that lower it. If Wealth is at zero or below, drop options that cost money: the handbook lists months with an empty wallet as a way a run ends. If Network is at zero, prefer an option that involves or helps someone.
4. **Review close (N = 1 or 2).** Promotions are lost here. With N = 2, drop options that may lower Network or Output. If Network or Output is under its Best, choose the honest option that most directly raises it back. With N = 1, apply all of this step. Drop options that may lower Skill, Network or Output: going against a person (blaming, correcting in public, refusing, reporting someone, going over a head) may cost Network; giving up time or credit from your own delivery (unplanned work, investigations, rework, the slow thorough path, someone else's problem) may cost Output; avoiding the work or the learning may cost Skill. Never save a point by hiding a problem or cutting a corner.
5. **Grow.** From the rest, choose the option that raises the most of Skill, Network and Output, counting twice a stat the latest review talk named as lagging, and minus one for each of them it lowers. In the last quarter of the career (months 46–48, except the review month 47), prefer Health, Dignity and lower risk instead. On a tie: lower risk, then more Health and Dignity, then the option that costs no money.


## Quarterly phases only: first matching line wins
These lines choose Energy and main actions only, never a story option. You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost, so spend all of it. The menu shows each action's exact effect: use it to check what an action did. Plan the whole quarter after one `observe` (Turn loop, step 3).
1. **Last quarter of the career (month 48):** plan Energy and the main action together. Energy: Defuse legacy risk once if the HR remark is not the friendly one, then Health recovery and Mental recovery while either is below full, then Network maintenance. Main action: Lay low and reduce risk if the HR remark is not the friendly one, otherwise Report results to your manager. No Skill learning or High-intensity work.
2. **Near a limit.** These are published failure directions, and Health at zero ends the run at once. **Health 3 or below** (our margin): spend on Health recovery first, as many points as the menu's shown effect needs to bring Health above 3, then the rest of the Energy as the lines below say. **Health 4 or 5:** one point of Health recovery, then the lines below; this keeps the stats the next review needs, which the quarter before a review must still buy. **Dignity 4 or below, Wealth at zero or below, or Network at zero:** Mental recovery, no spending, or Network maintenance for the stat at risk; main action Repair a key relationship. No Skill learning or High-intensity work while Health is 5 or below.
3. **Stalled start** (Story step 2). Energy: Defuse legacy risk first, then one point on the stat under its Best (Prepare report materials for Output, Network maintenance for Network). Main action: Lay low and reduce risk when Network and Output are at their Best, otherwise Report results to your manager.
4. **HR remark** (classify it by its tone, whatever the exact wording; if none has appeared for a few months or the tone is unclear, treat it as quiet; treat any warning about risk or trust as uneasy). Friendly ("you are doing all right"): no risk action. Quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below. Anything else (frowning, uneasy, "you are on your own", angry): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is friendly or quiet again.
5. **A review talk named a lagging stat:** until the next review, spend Energy and the main action on it (Prepare report materials for Output, Network maintenance for Network, Skill learning for Skill; main action Apply for a key project, or Apply for rotation when it is Skill).
6. **Level 4 or above:** Skill first (in our runs it held back most promotions from here). Energy: Skill learning while Health is above 5 (our margin), then one point on Prepare report materials (Network maintenance instead when Network is under its Best); if Skill learning was skipped for Health, Health recovery and two 1-Energy actions. Main action Apply for rotation.
7. **Otherwise:** spend Energy on Skill, Network and Output (Prepare report materials, Network maintenance, Skill learning while Health is above 5). Main action Apply for a key project.

## Near a limit: quick reference
| Signal | Story | Quarter |
| --- | --- | --- |
| Health 3 or below | drop anything that may lower Health, even before a review | Health recovery first (enough to pass 3), then the review stats |
| Health 4 or 5 | drop options that lower it if it is 4 or falling | one point of Health recovery, then the review stats |
| Dignity 4 or below, or falling | drop options that lower it | Mental recovery; Repair a key relationship |
| Wealth at zero or below, or Network at zero | drop options that cost money; prefer an option that involves someone | no spending; Network maintenance or Repair a key relationship |
| HR remark not friendly | step 2 strict: nothing private, partial or postponed | Defuse legacy risk; Lay low unless quiet |
| Starting level, two reviews without promotion | no option that may add risk; keep Network and Output at their Best | Defuse legacy risk; Lay low or Report results |
| Review in 1 or 2 | step 4: keep Skill, Network and Output | (the last quarter before the review is already behind you) |
