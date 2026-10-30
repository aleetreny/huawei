---
name: career-rules
description: "Use on every Career Survival turn. Keeps a one-line status note, reads every story option for likely stat changes and hidden risk, protects Skill, Network and Output in the month before a review, and sets quarterly Energy and main actions in priority order."
---

# Career rules

## How to use this Skill
- **Stories and quarterly phases are separate.** A story is decided only by "Story decisions" below. The quarterly list never picks a story option, and a story rule never picks an Energy or main action.
- Read this Skill again whenever its rules are no longer in view, for example after a summary or a resume.

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
Before choosing, read every option for the likely sign of its effect on Skill, Network, Output, Health, Dignity, Wealth and hidden risk. How options usually move them:
- **Skill** rises when you use your own judgement: analyse, bring data or evidence, prepare properly, think a decision through, learn, design a plan, negotiate with facts, coach someone with questions. This holds for options about people or pay too, not only code.
- **Output** rises when you deliver, ship, finish or cover the work, keep to your own deliverables or make your results visible. It falls when your time or credit goes elsewhere: learning, helping or organising for others, reviewing their work, giving the credit away, apologising and redoing, pausing a delivery, complaining instead of working. Output and Network often trade against each other.
- **Network** rises when you help, involve, credit or work with others; it falls when you confront, refuse, embarrass someone, go over their head or ignore them.
- **Dignity** rises when you act straight, stand your ground calmly, own a mistake or get credit; it falls when you are humiliated, cave in, get blamed or gossip.
- **Health** falls with overtime, weekends, extra load and stress; it rises with rest and boundaries. **Wealth** moves with pay, bonuses and money you spend.
- **Hidden risk** rises with hiding, denying, blaming, shortcuts, gambles, fixing things privately or off the record, anonymous moves, side deals, partial, phased or postponed fixes, skipping necessary work to save time, open conflict, ignoring a known problem, disengaging, and challenging the company, its culture, leaders or rules even through a formal channel. It falls when you document, report a concrete problem openly, follow the process, own a mistake at once or fix the problem fully. Missing a risky option costs far more than flagging a safe one: when in doubt, treat it as risky.

Then apply these steps in order. Skip a step if it would remove every option.
1. **Survive.** Drop any option that could end the run now, for example by taking Health to zero.
2. **Risk.** Drop options that may add hidden risk. If the latest HR remark is anything but the friendly one, or you have already chosen an option this month that might bury a problem, also drop options that keep a problem private, anonymous, partial, phased or for later, or skip work to save time, even when they solve the immediate problem; prefer an option that documents, reports, owns or fully fixes it. If every option looks risky, choose the smallest and most reversible risk.
   **Exception for the review month (N = 1) while the HR remark is friendly or quiet:** apply step 4 first. A mild risk (handling something privately, partially or later) is then acceptable when it is the only way to keep Skill, Network and Output, because a lost point there can cost the promotion. Hiding, denying, blaming, gambling and cutting corners stay out in every month.
3. **Wellbeing.** If Health or Dignity is low or falling, drop options that lower it.
4. **Review close (N = 1 or 2).** Promotions are lost here. With N = 2, drop options that may lower Network or Output. If Network or Output is under its Best, choose the honest option that most directly raises it back. With N = 1, apply all of this step. Drop options that may lower Skill, Network or Output: going against a person (blaming, correcting in public, refusing, reporting someone, going over a head) may cost Network; giving up time or credit from your own delivery (unplanned work, investigations, rework, the slow thorough path, someone else's problem) may cost Output; avoiding the work or the learning may cost Skill. Never save a point by hiding a problem or cutting a corner.
5. **Grow.** From the rest, choose the option that raises the most of Skill, Network and Output, counting twice a stat the latest review talk named as lagging, and minus one for each of them it lowers. In the final quarter of the career, prefer Health, Dignity and lower risk instead. On a tie: lower risk, then more Health and Dignity, then the option that costs no money.


## Quarterly phases only: first matching line wins
These lines choose Energy and main actions only, never a story option. You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost. Choose one affordable Energy action at a time, then observe again.
1. **Last quarter of the career (month 48):** plan Energy and the main action together. Energy: Defuse legacy risk once if the HR remark is not the friendly one, then Health recovery and Mental recovery while either is below full, then Network maintenance. Main action: Lay low and reduce risk if the HR remark is not the friendly one, otherwise Report results to your manager. No Skill learning or High-intensity work.
2. **Health or Dignity in the lower part of its 0–10 range, or falling for several months; or Network or Wealth near zero for months.** Recover first: Health recovery, Mental recovery, Network maintenance or Repair a key relationship, and avoid spending. No Skill learning or High-intensity work until it recovers. Health at zero ends the run.
3. **HR remark.** Friendly ("you are doing all right"): no risk action. Quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below. Anything else (frowning, uneasy, "you are on your own", angry): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is friendly or quiet again.
4. **A review talk named a lagging stat:** until the next review, spend Energy and the main action on it (Prepare report materials for Output, Network maintenance for Network, Skill learning for Skill; main action Apply for a key project, or Apply for rotation when it is Skill).
5. **Otherwise:** spend Energy on Skill, Network and Output (Prepare report materials, Network maintenance, Skill learning while Health is comfortable). Main action Apply for a key project.
