---
name: career-advisor
description: Required for every Career Survival decision (story events, quarterly energy, quarterly main action). You read the turn and describe each option in a short code; the bundled script script/advisor.py weighs the codes against your stats, the HR tone and what it has learned this run, and prints the choice to take. Use it on every turn of the 48 months.
---

# Career advisor

You are good at reading situations; arithmetic over 48 months is where agents slip. So the work is split:

- **You read.** Each turn you turn what you see into one line: your stats, how worried the HR partner sounds, and, for a story, how each option is likely to move each stat and whether it may bury a problem.
- **The script decides.** `script/advisor.py` scores every option the same way every time, remembers what it saw earlier in this run, and prints `CHOOSE n` and a `NOTE` line.
- **You act.** Take exactly the printed choice and put the NOTE line at the start of your `notes`.

The script never sees event text. Its choice is only as good as your reading, so read each option carefully.

## The loop (every decision)

1. `observe(session_id)`.
2. If the event offers a single choice (Continue, a handbook, a notice), take it. No script call.
3. Otherwise build the advisor line (format below) and run it with the `bash` tool:

   ```
   python3 ../skills/career-advisor/script/advisor.py "sid=<session_id> m=<current_month> H=<health> D=<dignity> S=<skill> N=<network> O=<output> W=<wealth> L=<level number> E=<energy> hr=<0-4> phase=<story|energy|main> | 1: <codes> | 2: <codes> | ..."
   ```

   The default working directory of `bash` is the agent's `projects` folder, next to `skills`. If the file is not found there, use the absolute path of `career-advisor/script/advisor.py` inside your agent skills directory (shown in your system prompt), and keep using that path.
4. `take_action(session_id, choice=<n from CHOOSE>, notes="<NOTE line> | <one short reason>")`.

Quarterly phases: for the energy menu run the line with `phase=energy` (no options) and take the printed choice; repeat after each pick until the script prints `Reserve energy`, then take that. For the main-action menu run it once with `phase=main`. The script prints the action name: if the number in the menu differs, pick by name.

After a context reset, nothing is lost: the script keeps its own memory for this session id. Just observe and continue the loop.

## Filling the line

- Stats: copy them from `current_state.status` of the latest `observe`. `L` is the number of the level (L2 → `L=2`).
- `hr`: how worried the HR partner's most recent monthly remark sounds (it comes at the start of a month, in the `events` text): `0` relaxed or praising, `1` a quiet hint, `2` frowning or concerned, `3` uneasy or worried, `4` angry or alarmed. Keep the last value until a new remark appears.
- `phase`: `story` for story events, `energy` for the quarterly energy menu, `main` for the quarterly main-action menu.
- Options (story only): one block per option, `| <number>: <codes>`. Codes are a stat letter with a sign: `H` Health, `D` Dignity, `S` Skill, `N` Network, `O` Output, `W` Wealth; `+` rises, `++` rises a lot, `-` falls, `--` falls a lot. Add `R+` when the option may bury a problem (hidden risk rises) and `R-` when it clears one. Leave out what does not move. Example: `| 1: S+ N+ R- | 2: O+ N- | 3: H- O+ R+`.

## How to read an option

Most options move two or three stats. Judge from the option's wording and the situation.

- **Health** falls with overtime, weekends, late nights, extra load, stress; rises with rest, going home, boundaries.
- **Dignity** rises when you act straight and professionally, stand your ground calmly, own a mistake or get credit; falls when you are humiliated, cave in, get blamed, gossip or put up with unfair treatment.
- **Skill** rises whenever you use your own judgement: analyse, investigate, bring data, think a decision through, prepare properly, learn, design a plan, negotiate with facts, coach with questions. This is the one readers miss most: it rises even when the topic is people or pay.
- **Network** rises when you help, involve, credit or work with others; falls when you confront, refuse, embarrass someone, go over their head or ignore them.
- **Output** rises when you deliver, ship, finish, keep focus on your own deliverables or make your results visible; falls when your time or credit goes elsewhere (learning, helping or organising for others, reviewing their work, extra meetings, redoing work, pausing a delivery, complaining instead of working). Output and Network often trade against each other.
- **Wealth** rises with a pay rise, bonus or payment; falls when you pay or give up money.
- **Hidden risk (`R+`)** rises with hiding, denying, blaming, shortcuts, gambles, fixing things privately or off the record, side deals, partial, parallel or postponed fixes, doing less than the proper job to save time, open conflict, doing nothing about a known problem, disengaging or eyeing the exit, and challenging the company, its culture, leaders or rules, even through a formal channel. It falls (`R-`) when you document, report a concrete problem, follow the process, own a mistake at once or fix the problem fully. Missing a risky option costs far more than flagging a safe one: when in doubt, write `R+`.

## What the script weighs (so you know why it chose)

- Hidden risk first. A blow-up erases months of results and a second one ends the career. The script refuses options you marked `R+` as soon as the HR remark is not relaxed, and spends the quarter on clearing risk (Defuse legacy risk, Lay low) until the remark is relaxed again.
- Health and Dignity: it avoids options that push Health low and recovers Health in the quarter before it gets low; low Dignity blocks promotion.
- Growth: it prefers options that raise Skill, Network and Output, most the one with most room. When a published gain stops registering ("stalled"), it stops spending on that stat at this level and moves on; in the month before each review (months 5, 11, 17, ...) it refuses to give up any growth point.
- Money: losses grow with level, so it avoids paying at higher levels.
- Last quarter of the career: it clears risk and restores Health and Dignity, which count at the end.
