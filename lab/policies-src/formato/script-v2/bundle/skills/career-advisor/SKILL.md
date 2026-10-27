---
name: career-advisor
description: "Use on every Career Survival turn. Decide each story yourself with the Story decisions below; at the start of every month and at every quarterly menu run the bundled script script/advisor.py, which keeps the status line (best values, stalled stats, review countdown) and plans the quarter's Energy and main action."
---

# Career advisor

You decide the stories: reading people and situations is your strength. The bundled script does what is easy to get wrong over 48 months: comparing numbers across months (which stat has stopped rising at this level, which one has slipped below its best) and planning the quarterly Energy and main action from that record. It keeps its own memory for this game, so nothing is lost after a summary or a resume.

## How to use this Skill
- **Stories and quarterly phases are separate.** A story is decided only by "Story decisions" below. The quarterly plan comes only from the script and never picks a story option.
- Read this Skill again whenever its rules are no longer in view, for example after a summary or a resume.

## The script
Run it with the `bash` tool (its default folder is next to the skills folder; if the file is not found, use the absolute path of `career-advisor/script/advisor.py` inside your agent skills directory):

```
python3 ../skills/career-advisor/script/advisor.py "sid=<session_id> m=<current_month> H=<health> D=<dignity> S=<skill> N=<network> O=<output> W=<wealth> L=<level number> E=<energy> hr=<0-4> phase=<status|quarter>"
```
- Copy the stats from `current_state.status` of the latest `observe` (`L=2` for L2).
- `hr` is how worried the latest monthly HR remark sounds: `0` friendly ("doing all right"), `1` quiet, `2` frowning, `3` uneasy or "on your own", `4` angry.
- `phase=status` at the **first decision of every month** and after any resume. It prints `STATUS: Review in N | Now ... | Best ... | Stalled: ...`. Use that line as the start of every note this month (update `Now` from `observe` as it changes).
- `phase=quarter` **once, at the quarterly Energy menu**. It prints the Energy picks in order and the main action. Take them exactly, one pick per `take_action` (by name if a number differs), then the main action. Do not run it again for the same quarter.

## Turn loop
1. `observe`. Read `events` first: the monthly HR remark, the review talk, warnings.
2. First decision of the month (or after a resume): run the script with `phase=status`.
3. Story: decide with "Story decisions". Quarterly menu: follow the script's plan.
4. `take_action` with the exact `choice` and a short note that starts with the status line, then one short reason, in English. Keep notes short. If `success` is false, read the error, observe again and choose a valid option.

## Status line
- **Review in N:** months left until the next review month. With N = 1 the review comes at the end of this month.
- **Now / Best:** Skill, Network and Output now, and the highest value of each seen at your current level. A stat below its Best has lost ground since you last held it.
- **Stalled:** stats whose published gain stopped registering at this level (the script checks it after each quarter). While a stat is Stalled, gains in it are wasted: do not pay for it, but do not lose it either.
- **Concerns this month:** add `| Concerns this month: <count>` yourself: how many of this month's story choices you judged might bury a problem. Start each month at 0.

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
2. **Risk.** Drop options that may add hidden risk. If the latest HR remark is anything but the friendly one, or Concerns this month is 1 or more, also drop options that keep a problem private, anonymous, partial, phased or for later, or skip work to save time, even when they solve the immediate problem; prefer an option that documents, reports, owns or fully fixes it. If every option looks risky, choose the smallest and most reversible risk.
   **Exception for the review month (N = 1) while the HR remark is friendly or quiet:** apply step 4 first. A mild risk (handling something privately, partially or later) is then acceptable when it is the only way to keep Skill, Network and Output, because a lost point there can cost the promotion. Hiding, denying, blaming, gambling and cutting corners stay out in every month.
3. **Wellbeing.** If Health or Dignity is low or falling, drop options that lower it.
4. **Review close (N = 1 or 2).** Promotions are lost here. With N = 2, drop options that may lower Network or Output. If Network or Output is under its Best, choose the honest option that most directly raises it back. With N = 1, apply all of this step. Drop options that may lower Skill, Network or Output: going against a person (blaming, correcting in public, refusing, reporting someone, going over a head) may cost Network; giving up time or credit from your own delivery (unplanned work, investigations, rework, the slow thorough path, someone else's problem) may cost Output; avoiding the work or the learning may cost Skill. Never save a point by hiding a problem or cutting a corner.
5. **Grow.** From the rest, choose the option that raises the most of Skill, Network and Output that are not Stalled, counting twice a stat the latest review talk named as lagging, and minus one for each of them it lowers. In the final quarter of the career, prefer Health, Dignity and lower risk instead. On a tie: lower risk, then more Health and Dignity, then the option that costs no money.

After choosing, add 1 to Concerns this month if the chosen option might bury a problem.

## What the quarterly plan weighs
- Risk first: when the HR remark is not friendly, Defuse legacy risk and Lay low and reduce risk until it is friendly again.
- Health: recover before Health gets low; a run ends at zero Health.
- Growth: Energy and the main action go to Skill, Network and Output that still have room at this level, most to the one with most room; once Network and Output are Stalled, Skill comes first.
- Last quarter of the career: clear risk, then restore Health and Dignity.
