---
name: career-advisor
description: "Use on every Career Survival turn. You decide each story with the Story decisions below and write your reading of every option as short codes; the bundled script script/advisor.py checks your pick against your own reading (it replaces a pick you marked as risky, as costing a growth point in the review month, or as costing money with an empty wallet) and decides the quarterly Energy and main action with its memory of this run."
---

# Career advisor

You decide the stories: reading people and situations is your strength. The bundled script is a second pair of eyes with a memory: it checks every pick against your own reading of the options, remembers what it saw earlier in the run (which stats have stopped rising at this level, how worried HR has been), and decides the quarterly menus. Take the choice it prints.

## The loop (every decision)

1. `observe(session_id)`. Read `events` first: the monthly HR remark, the review talk, warnings.
2. If the event offers a single choice (Continue, a handbook, a notice), take it. No script call.
3. Story: read every option into codes (below), choose your `pick` with "Story decisions", and run the line with `phase=story pick=<n>`. Quarterly Energy menu: run the line with `phase=energy` (no options) and repeat after each pick until it prints `Reserve energy`. Main-action menu: `phase=main` once.

   ```
   python3 ../skills/career-advisor/script/advisor.py "sid=<session_id> m=<current_month> H=<health> D=<dignity> S=<skill> N=<network> O=<output> W=<wealth> L=<level number> E=<energy> hr=<0-4> phase=story pick=<n> | 1: <codes> | 2: <codes> | ..."
   ```

   The default working directory of `bash` is the agent's `projects` folder, next to `skills`. If the file is not found there, use the absolute path of `career-advisor/script/advisor.py` inside your agent skills directory, and keep using it.
4. `take_action(session_id, choice=<n from CHOOSE>, notes="<NOTE line> | <one short reason>")`. Keep notes short and in English. If the script printed `READ NEXT`, apply it to your next reading.

After a context reset nothing is lost: the script keeps its own memory for this session id. Observe and continue the loop.

## Filling the line

- Stats: copy them from `current_state.status` of the latest `observe`. `L` is the number of the level (L2 → `L=2`).
- `hr`: how worried the HR partner's most recent monthly remark sounds (it comes at the start of a month, in the `events` text): `0` relaxed or praising, `1` a quiet hint, `2` frowning or concerned, `3` uneasy or worried, `4` angry or alarmed. Keep the last value until a new remark appears.
- `phase`: `story` for story events, `energy` for the quarterly energy menu, `main` for the quarterly main-action menu.
- Options (story only): one block per option, `| <number>: <codes>`. Codes are a stat letter with a sign: `H` Health, `D` Dignity, `S` Skill, `N` Network, `O` Output, `W` Wealth; `+` rises, `++` rises a lot, `-` falls, `--` falls a lot. Add `R+` when the option may bury a problem (hidden risk rises) and `R-` when it clears one. Leave out what does not move. Example: `| 1: S+ N+ R- | 2: O+ N- | 3: H- O+ R+`.

## How to read an option (codes)

Write every stat you think moves, including the costs. Skill rises when you use your own judgement (analyse, investigate, prepare, learn, plan, negotiate with facts), even about people or pay. A proper fix often raises Skill and costs Output at the same time: write both. Output falls when your time or credit goes elsewhere (unplanned work, investigating or fixing properly, rework, the slow thorough path, meetings, someone else's problem). Network falls when you refuse, correct, report, embarrass or go over someone. `R+` for anything that may bury a problem (hiding, blaming, shortcuts, gambles, private or off-the-record handling, partial, phased, temporary or later fixes, skipping work to save time, open conflict, doing nothing about a known problem, challenging the company or its rules), even when it sounds pragmatic or kind; when in doubt, `R+`. `R-` only when the option documents, reports a concrete problem through the process, owns a mistake at once or fixes the problem fully.

## Story decisions (how you choose `pick`)
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

## What the script checks and decides
- **Your pick stands** unless your own codes mark it `R+`, or a Skill, Network or Output loss when the review is at the end of this month, or a money loss when the wallet shows almost nothing (the panel rounds Wealth down, so a small number may already be negative), or a Health drop near zero. Then it takes the best option you did not flag, and says why.
- **Quarterly menus:** risk first (Defuse legacy risk and Lay low and reduce risk while the HR remark is not relaxed); Health before it gets low; then Skill, Network and Output that still have room at this level, most the one with most room; once Network and Output have stalled (a published gain stopped registering), Skill first. In the last quarter of the career it clears risk and restores Health and Dignity.
