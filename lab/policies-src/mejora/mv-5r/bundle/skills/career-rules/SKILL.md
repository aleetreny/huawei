---
name: career-rules
description: "Complete strategy for the 48-month Career Survival run: how to answer every story event, how to spend each quarter's Energy and main action, how to win each six-monthly promotion review, and what to do when Health, Dignity, Wealth, Network or the HR remark nears a failure limit. Also sets the one-reply turn loop and the one-line note. Open it at the start of the run and again whenever its rules are out of view."
---

# Career rules

## What this Skill is for
- **Use it for every decision of the run.** Stories are decided only by "Story decisions"; quarterly phases only by "Quarterly phases". A story rule never picks an Energy or main action, and a quarterly line never picks a story option.
- **Priorities, in order:** stay in the run (no stat at a failure limit, no second hidden-risk blow-up), then win the next promotion review, then grow. Pay rises with level, so an earlier promotion is also the main source of Wealth.
- **Published and ours.** The handbook publishes the levels, the six-monthly reviews, the quarterly actions and their directions, pay, grades and the failure directions. It does not publish thresholds, formulas or hidden-risk conditions. Anything below said to happen "in our runs" or "usually" is our own observation, not a game rule: when the game shows something else (stat changes, the HR remark, review talks, warnings), follow the game.
- Reread this Skill whenever its rules are not in view, for example after a summary or a resume.

## The 48 months at a glance
| Phase | Goal | How |
| --- | --- | --- |
| Starting level | First promotion at the first review | In our runs Network and Skill fill up within a few months and Output is the one that lags: the quarterly Energy goes to Prepare report materials (Quarterly line 6). In the month before each review, protect Network and Output (Story step 4). |
| Levels 2 and 3 | Promotion at every review | Balanced growth of Skill, Network and Output; the same review protection. |
| Level 4 and above | Skill, then Output | The handbook describes critical systems, leading teams and setting direction from level 4, and the bar rises with level. In our runs Skill, then Output, is what holds promotions back from here: the quarter buys Skill and Output (Quarterly line 4). |
| Last quarter (month 48) | Keep what you have | Lower risk, raise Health and Dignity, no new growth spending (Quarterly line 1). |

**Review calendar.** Reviews come every six months (handbook). The handbook lists the review after the quarterly phase; in our runs the half-year talk, the bonus and any promotion appeared among the events as months 6, 12, 18 … 48 began, judged on the stats held at that moment. This Skill therefore treats months 5, 11, 17 … 47 as review months (Review in 1) and protects Skill, Network and Output through them, and keeps protecting until the talk is in view: if month 6 (12, 18 …) begins without it, keep the Review in 1 protection through that month too, whatever the formula below gives.

**Throughout.** Keep the HR remark friendly: the handbook warns that old landmines go off at once and wipe out half a year of work, and that a second blow-up ends the run in a trust crisis. Keep Health and Dignity off the bottom of their 0–10 range and Wealth and Network above zero: each is a published failure direction.

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
Before choosing, read every option for the likely sign of its effect on Skill, Network, Output, Health, Dignity, Wealth and hidden risk. The game does not publish these effects; the wording cues below are our working assumptions, and the changes the game shows after a choice come first:
- **Skill** rises when you use your own judgement: analyse, bring data or evidence, prepare properly, think a decision through, learn, design a plan, negotiate with facts, coach someone with questions. This holds for options about people or pay too, not only code.
- **Output** rises when you deliver, ship, finish or cover the work, keep to your own deliverables or make your results visible. It falls when your time or credit goes elsewhere: learning, helping or organising for others, reviewing their work, giving the credit away, apologising and redoing, pausing a delivery, resting instead of delivering, complaining instead of working. Output and Network often trade against each other.
- **Network** rises when you help, involve, credit or work with others; it falls when you confront, refuse, embarrass someone, go over their head or ignore them.
- **Dignity** rises when you act straight, stand your ground calmly, own a mistake or get credit; it falls when you are humiliated, cave in, get blamed or gossip.
- **Health** falls with overtime, weekends, extra load and stress; it rises with rest and boundaries. **Wealth** moves with pay, bonuses and money you spend.
- **Hidden risk** (not shown; the HR remark is your only gauge) is likely to rise with hiding, denying, blaming, shortcuts, gambles, fixing things privately or off the record, anonymous moves, side deals, partial, phased or postponed fixes, skipping necessary work to save time, open conflict, ignoring a known problem, disengaging, and challenging the company, its culture, leaders or rules even through a formal channel. It is likely to fall when you document, report a concrete problem openly, follow the process, own a mistake at once or fix the problem fully. Missing a risky option costs far more than flagging a safe one: when in doubt, treat it as risky.

Then apply these steps in order. Skip a step if it would remove every option.
1. **Survive.** Drop any option that could end the run now, for example by taking Health to zero.
2. **Risk.**
   - Drop options that may add hidden risk.
   - **Strict mode**: the latest HR remark is anything but the friendly one (or a warning about risk or trust has appeared), or you already chose an option this month that might bury a problem, or you are in a stalled start (below). Then also drop options that keep a problem private, anonymous, partial, phased or for later, or skip work to save time, even when they solve the immediate problem; prefer an option that documents, reports, owns or fully fixes it.
   - **If every option looks risky, the size of the risk decides, not the growth:** postponing, going round a problem or letting something go is a smaller risk than forcing, confronting or caving in, and far smaller than hiding, denying, blaming or gambling. Choose the smallest and most reversible one.
   - **Review-month exception** (Review in 1, HR remark friendly or quiet, not in a stalled start): apply step 4 first. A mild risk (handling something privately, partially or later) is then acceptable when it is the only way to keep Skill, Network and Output, because a lost point there can cost the promotion. Hiding, denying, blaming, gambling and cutting corners stay out in every month.
   - **Stalled start**: still at your starting level after two reviews (Reviews here is 2, or Months at current level in `observe` is 12 or more). The handbook says weak reviews lead to dismissal, and in our runs a career still at the starting level at month 24 was dismissed. Until the next review, prefer the options that lower risk even when another grows a stat faster.
3. **Wellbeing.** If Health is 3 or below, drop every option that may lower Health, in any month: overtime, night or weekend work, extra load, stress. If Health is 5 or below or Dignity 4 or below (our margins on the published 0–10 range), or either has fallen for several months, drop options that lower it. If Wealth is below zero (the panel may show 0 while it is negative), drop options that cost money. If Network is at zero, prefer an option that involves or helps someone.
4. **Review close (Review in 1 or 2).** Promotions are lost here: in our runs, one point of Network or Output lost in the review month cost the first promotion.
   - **Repair first.** If Network or Output is under its Best, choose the honest option that most directly raises it back.
   - Otherwise, with N = 2, drop options that may lower Network or Output; with N = 1, also drop options that may lower Skill.
   - **Read the hidden costs (starting level only).** At the starting level one lost point costs the first promotion, and in our runs these losses came from options that looked right. Network falls whenever someone is let down, even politely or fairly: turning a colleague down, setting a boundary, an honest but low rating, correcting or contradicting someone in front of others, naming who really did the work, reporting someone or going over a head, putting your own work forward next to a colleague's, stepping out of a group effort. Output falls when extra work that is not your own deliverable takes your time or your credit: coaching someone through a problem, writing a formal note or recognition, joining someone else's review or meeting, investigations, rework or the slow thorough path, rest, giving the credit away. A quick, bounded favour that keeps you on your own work usually costs nothing. Skill falls when you avoid the work or the learning.
   - At the starting level, when every option that passes step 2 has one of these costs, choose among them the one that leaves the people involved most comfortable and keeps you on your own work, even if it gains nothing. Never save a point by hiding a problem or cutting a corner.
5. **Grow.** From the rest, choose the option that raises the most of Skill, Network and Output, minus one for each of them it lowers. In the last quarter of the career (months 46–48, except the review month 47), prefer Health, Dignity and lower risk instead. On a tie: lower risk, then more Health and Dignity, then the option that costs no money.

## Quarterly phases: first matching line wins
These lines choose Energy and main actions only, never a story option. You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost, so spend all of it. The menu shows each action's exact effect: use it to check what an action did. Plan the whole quarter after one `observe` (Turn loop, step 3).
1. **Last quarter of the career (month 48):** Energy: Defuse legacy risk once if the HR remark is not the friendly one, then Health recovery and Mental recovery while either is below full, then Network maintenance. Main action: Lay low and reduce risk if the HR remark is not the friendly one, otherwise Report results to your manager. No Skill learning or High-intensity work.
2. **Near a limit.** These are published failure directions, and the game warns before they end a run. **Health 5 or below** (our margin): Health recovery comes first with the Energy until Health is above 5. **Health or Dignity 4 or below, either falling three months in a row, Wealth below zero, or Network at zero:** also Mental recovery or Network maintenance for the stat at risk, main action Repair a key relationship (Lay low and reduce risk when Health is the problem), no spending, and no Skill learning or High-intensity work until it recovers.
3. **HR remark** (classify it by its tone, whatever the exact wording). Friendly ("you are doing all right"): no risk action. Quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below. Anything else (frowning, uneasy, "you are on your own", angry): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is friendly or quiet again. During a stalled start, treat the quiet remark like the others. If no HR remark has appeared for a few months, or its tone is unclear, treat it as quiet; treat any warning about risk or trust as uneasy.
4. **Level 4 or above:** Skill first, Output second (in our runs these two held back most promotions from here). Energy: Skill learning (2) while Health is above 5, then one point on Prepare report materials (Network maintenance instead when Network is under its Best); if Skill learning was skipped for Health, Health recovery (1) and the two 1-cost actions. Main action Apply for rotation.
5. **Levels 2 and 3:** Energy: Prepare report materials, Network maintenance, Prepare report materials (start with Network maintenance when Network is under its Best). Main action Apply for a key project.
6. **Starting level:** every Energy point that lines 2 and 3 leave goes to Prepare report materials, because Output is the stat that lags at this level in our runs. If last quarter's reports left Output where it was, put the points on Network maintenance, or Health recovery when Network did not move either. Main action Apply for a key project.

## Near a limit: quick reference
| Signal | Story | Quarter |
| --- | --- | --- |
| Health 4 or 5 | drop options that lower it | Health recovery first |
| Health 3 or below | drop anything that may lower it, even in a review month | Health recovery with all the Energy it needs; Lay low and reduce risk |
| Dignity 4 or below | drop options that lower it | Mental recovery; Repair a key relationship |
| Wealth below zero (may show as 0) | drop options that cost money | no spending |
| Network at zero | prefer an option that involves someone | Network maintenance; Repair a key relationship |
| HR remark not friendly | step 2 strict | Defuse legacy risk; Lay low unless quiet |
| Review month | step 4 first | (the quarter is already behind you) |
