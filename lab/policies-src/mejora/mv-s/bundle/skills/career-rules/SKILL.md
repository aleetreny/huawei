---
name: career-rules
description: "Strategy for every turn of the 48-month Career Survival run: the one-reply turn loop and one-line note, how to pick each story option, and how to spend each quarter. Open it at the start of the run and again whenever its rules are out of view."
---

# Career rules

Use this Skill for every decision. Stories are decided only by "Story decisions" and quarterly phases only by "Quarterly phases". Goals, in order: stay in the run, win the next six-monthly review, then grow. Lines marked "in our runs" are our observations, not game rules; when the game shows something else, follow the game. Reread this Skill whenever it is out of view.

**Plan.** Starting level: first promotion at the first review. Levels 2 and 3: a promotion at every review. Level 4 and above: Skill first. Months 46–48: keep Health, Dignity and low risk. **HR remark** (the monthly gauge of hidden risk), read by its tone: friendly ("you are doing all right"), quiet ("some risk, nothing serious yet"), or worse (frowning, uneasy, "you are on your own", angry); an unclear tone or a warning about risk counts as quiet or worse.

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
**Read each option first** for its likely effect (our working cues; the changes the game shows come first):
- **Skill** rises with your own judgement: analyse, bring data, prepare, learn, plan, negotiate with facts.
- **Output** rises when you deliver your own work and make it visible; it falls when your time or credit goes to others or to process.
- **Network** rises when you help, involve or credit others; it falls when you confront, refuse, embarrass someone or go over their head.
- **Hidden risk** (the HR remark is your only gauge) rises with hiding, denying, blaming, shortcuts, gambles, private or off-the-record fixes, anonymous moves, side deals, partial or postponed fixes, ignoring a problem, open conflict and challenging the company. It falls when you document, report openly, follow the process, own a mistake or fix it fully. When in doubt, treat an option as risky.

**Then the first rule that applies decides:**
1. **Never** pick an option that could end the run, or that hides, denies, blames, gambles or leaks.
2. **Caution:** the HR remark is not the friendly one, or you already took a risky option this month, or you are in a stalled start (two reviews at your starting level without promotion). Pick the lowest-risk option; on a tie, the one that grows most.
3. **Health 3 or below:** drop every option that lowers Health.
4. **Review in 1 or 2:** drop risky options and options that lower Network or Output (with Review in 1, also Skill). If Network or Output is under its Best, pick the honest option that raises it back.
   - **At your starting level** one lost point costs the first promotion. Network falls whenever someone is let down, even politely or fairly (turning someone down, a boundary, an honest low rating, correcting someone in front of others, naming who really did the work, putting your work next to a colleague's). Output falls when extra work that is not your own deliverable takes your time or credit (coaching, formal notes or recognition, other people's meetings, investigations, rework, rest); a quick, bounded favour usually costs nothing. If no option is free of these costs, pick the one that leaves people most comfortable and keeps you on your own work.
   - **With Review in 1 and the HR remark friendly or quiet**, a mild risk (handling something privately, partially or later) is acceptable when it is the only way to keep Skill, Network and Output.
5. **Otherwise:** drop risky options and pick the one that raises most of Skill, Network and Output, minus one for each it lowers. In months 46 and 48, prefer Health, Dignity and lower risk. If every option is risky, pick the smallest and most reversible risk.
   Ties: lower risk, then more Health and Dignity, then no money spent.

## Quarterly phases
You have 3 Energy (Skill learning, High-intensity work and Defuse legacy risk cost 2, the rest 1); unused Energy is lost, so spend all 3, repeating an action when a line names fewer. Check the numbers you send against the menu in view. The first line that applies decides:
1. **Month 48:** Defuse legacy risk if the HR remark is not friendly, then Health recovery and Mental recovery while below full, then Network maintenance. Main action: Lay low and reduce risk if the HR remark is not friendly, otherwise Report results to your manager.
2. **Health 5 or below:** Health recovery first until Health is above 5. **Health or Dignity 4 or below, Wealth below zero or Network at zero:** recover that stat (Health recovery, Mental recovery or Network maintenance), main action Repair a key relationship (Lay low and reduce risk for Health), no Skill learning or High-intensity work.
3. **HR remark quiet:** first Energy action Defuse legacy risk. **Worse than quiet** (or quiet during a stalled start): Defuse legacy risk and main action Lay low and reduce risk, until it is friendly or quiet again.
4. **By level**, with the Energy left:

| Level | Energy | Main action |
| --- | --- | --- |
| Starting level | Prepare report materials (Network maintenance when Network is under its Best or reports stopped raising Output) | Apply for a key project |
| 2 and 3 | Prepare report materials, Network maintenance, Prepare report materials (Network first when under its Best) | Apply for a key project |
| 4 and above | Skill learning while Health is above 5, then Prepare report materials (Network maintenance when under its Best) | Apply for rotation |

In our runs Output lagged at the starting level and Skill held back promotions from level 4; pay rises with level, so early promotions are also the main source of Wealth.
