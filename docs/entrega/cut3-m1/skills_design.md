# Skills design — Gradient Depression

**Submission `VERSION`, Cut 3 (1 November 2026).** One Skill, `skills/career-rules/SKILL.md`, plus the manifest instruction. JiuwenSwarm 0.2.4b3, single-agent `agent` mode. No scripts and no reference files.

This version keeps the story judgement of our earlier submissions (the reading guide, the list of risky wording and the five ordered story steps) and the way of working introduced in Cut 2: each decision is one reply with two tool calls and a one-line note, and the quarterly plan follows the level. It is built on the Skill of our best development careers (one of them reached the sixth level), with three changes for Cut 3: a mild risk is accepted to climb faster while the HR remark is friendly, the starting level keeps Health without spending the last quarter before a review on it, and a stalled start (two reviews without a promotion) has its own protocol.

## 1. Our understanding of the task

Career Survival asks a single agent to sustain a career while developing it. The public handbook describes a 48-month horizon, monthly story choices, quarterly Energy and main actions, and six-monthly reviews. Growth competes with wellbeing, working relationships, money and hidden risk. Story outcomes are not shown before choosing, so the agent has to infer the likely consequence of each option from its wording.

We separate three questions: what does this option probably change, what does the career need now, and which instruction applies in this phase? Our research found failures at all three layers. More detailed strategy did not automatically improve play: instructions were sometimes followed in the wrong phase, and correct priorities were applied to misread options. The Skill is built around those three questions.

The agent decides only from the current run: `observe` (state, events, choices), review talks, the monthly HR remark, warnings and its own recent log entries. The Skill supplies priorities, a reading guide, a turn loop and a note format, not answers for named events, numerical thresholds or a model of hidden risk.

## 2. One Skill, with the key scope repeated in the manifest

The design has one discoverable `career-rules` Skill used on every turn. It contains the turn loop, the status line, the story procedure, the quarterly priority list and a quick reference for stats near a limit.

- **Why one Skill.** Earlier multi-Skill versions let the agent retrieve one relevant-looking rule while missing another. A single Skill was retrieved consistently in our DeepSeek and proxy-model tests.
- **Why the manifest repeats the scope.** In development careers, DeepSeek read the Skill early and then relied on its context; it did not reopen supporting files. The manifest instruction therefore states what matters most: the two-call turn loop and never ending a reply with text only; keeping stories and quarterly phases apart; dropping options that may bury a problem; protecting Skill, Network and Output in the two months before a review; and the quarterly plan from level 4. It also asks the agent to reread the Skill whenever its rules are no longer in view, for example after a summary.
- **No delegation.** Everything runs in one agent; there is no team mode and no sub-agent.

## 3. Turn loop and status line

Every model call resends the whole conversation, so the cost of a run grows with the number of replies. The turn loop makes each decision cost one reply.

- **The first three replies set the pattern:** `new_game`, then `observe`, then the opening screen answered already as the pair `take_action` + `observe`.
- **Story:** one reply with exactly two tool calls, `take_action` (the choice and a one-line note) and then `observe`, which returns the next situation together with the result. The agent decides silently, or with at most one short line of text, and sends both calls in the same reply.
- **Quarterly phase:** two replies in the first quarter (the Energy actions and `observe`, then the main action and `observe`), and from the second quarter on one reply with every action of the quarter and `observe`, because the menus are then known from the current run.
- **Recovery:** if the last note is not in view, the agent calls `check_latest_logs` with a small count and copies the status line. A rejected action leads to reading the error, observing again and choosing a valid option.

Every note is one line, the status line plus at most one short reason. It is the agent's compact memory:

`Review in N | Now S.. N.. O.. | Best S.. N.. O.. | Reviews here: 0`

- **Review in N** is computed from the visible month and the published six-month review schedule. It is a switch: the review-preparation steps apply only when N is 1 or 2, which keeps a narrow preference from leaking into the rest of the career. If a review month begins and the review talk is not yet in view, the agent keeps the review protection through that month.
- **Now** and **Best** record Skill, Network and Output as observed, and the best value of each seen at the current level. A stat below its Best has lost ground the agent should repair before a review. Best resets on promotion.
- **Reviews here** counts the review talks received at the current level without a promotion. At the starting level, 2 switches on the stalled-start protocol (section 4).

## 4. Stories: read consequences, then choose in a fixed order

The story section first asks for the likely sign of each option's effect on Skill, Network, Output, Health, Dignity, Wealth and hidden risk. The reading guide describes in general terms what tends to raise or lower each one: own judgement and preparation build Skill; delivering and making results visible builds Output, while time or credit given to others lowers it; helping and crediting others builds Network, while confronting or refusing lowers it; hiding, shortcuts, private or partial fixes, anonymous moves and open conflict add hidden risk. It also says that missing a risky option costs more than flagging a safe one, and that the changes the game shows after a choice come first.

The agent then applies five ordered steps, skipping a step only if it would remove every option:

1. **Survive:** drop options that could end the run now.
2. **Risk:** drop options that may add hidden risk. In strict mode (the HR remark is not the friendly one, a risky choice was already made this month, or a stalled start) also drop private, anonymous, partial or postponed fixes. If every option looks risky, the smallest and most reversible risk wins, not the largest gain. Three context rules adjust this step:
   - **Review month** (HR friendly or quiet, no stalled start): keeping Skill, Network and Output comes before avoiding a *mild* risk.
   - **Growth** (HR friendly, no risky choice yet this month, no blow-up, no stalled start): a mild risk is accepted when it gives clearly more Skill, Network or Output than every safe option. This is a deliberate bet on climbing faster: in our research planner, accepting a small risk while no risk is pending, instead of always playing safe, raised the average result by about five points and brought the fifth level earlier. The quarter's Defuse legacy risk and strict mode bring the remark back to friendly before the next such choice.
   - **Stalled start** (two reviews at the starting level without a promotion): until the next review, drop every option that may add risk, whatever it saves; then prefer the option that documents, reports, follows the process or fixes fully, because one that lowers risk covers one the agent misread; then keep Skill, Network and Output as in the review month. In our development careers, the third review at the starting level promoted only careers that reached it with the friendly HR remark.
   Hiding, denying, blaming, gambling and cutting corners stay excluded in every month.
3. **Wellbeing:** protect Health and Dignity when they are low or falling, avoid spending when Wealth is below zero, and prefer involving someone when Network is at zero.
4. **Review close (N = 1 or 2):** first repair Network or Output if it is under its Best. Otherwise avoid options that may lower Network or Output, and in the review month Skill as well. **At the starting level only**, the Skill names the hidden costs that looked right in our runs: Network falls when someone is let down, even politely or fairly; Output falls when extra work that is not your own deliverable takes your time or credit; a quick, bounded favour usually costs nothing. When every remaining option has such a cost, the agent chooses the one that leaves the people involved most comfortable and keeps it on its own work.
5. **Grow:** choose the option that raises most of Skill, Network and Output, minus one for each it lowers. In the final quarter, prefer Health, Dignity and lower risk. Ties go to lower risk, then Health and Dignity, then the option that costs no money.

## 5. Quarterly phases: first matching line wins

The quarterly list chooses Energy and main actions only, never a story option. The agent spends all its Energy, using the effects shown in the menu, and the first matching line wins:

1. **The final quarter of the career:** defuse risk if needed, recover Health and Dignity, report results; no new growth spending.
2. **Near a limit:** with low Health, Health recovery comes first (the Health brake), except at the starting level, where one point of Health is bought and the rest of the Energy still goes to the stats the next review needs; with low or falling Health or Dignity, Wealth below zero or Network at zero, recover the stat at risk and repair a relationship, with no spending.
3. **Stalled start:** defuse legacy risk first, one point on the stat under its Best, and lay low or report results.
4. **The HR remark:** if it is not friendly, defuse risk first, and lay low while it stays worrying.
5. **Level 4 and above:** Skill first, then Output: Skill learning while Health allows, one point on reports or on Network if Network lost ground, and Apply for rotation.
6. **Levels 2 and 3:** balanced reports and Network maintenance, and Apply for a key project.
7. **Starting level:** reports, because in our runs Output is the stat that lags at this level; if last quarter's reports left Output unchanged, Network maintenance or Health recovery instead. Apply for a key project.

Concrete, ordered quarterly directions were followed much more reliably than general goals in our obedience tests.

## 6. What changed from earlier versions, and why

| Version | Change | Reason, from our development careers |
|---|---|---|
| `t13-read-v1` | Reading guide for consequences and risk | DeepSeek recognised risk better than Skill or Output effects |
| `t13-read-v2` | Review protection moved into the Skill body and the manifest; strict story/quarter separation; stricter risk step | A quarterly rule leaked into stories; "constructive-sounding" private or phased fixes caused a trust crisis |
| `t13-read-v3` | In the review month, keeping Skill, Network and Output comes before a mild risk while HR is calm | Promotions were lost by one point in the last story before a review |
| `t13-read-v4` (Cut 1) | `Best` per level; protect Network and Output from two months before a review and repair losses at once | A career lost Output with two months to go while chasing Network it could no longer raise |
| **`mv-5r`** (Cut 2) | One reply per decision (`take_action` + `observe`); one-line note | v4 used 1.35–1.47 million tokens per game month: several replies per decision, each resending the whole history |
| **`mv-5r`** | A loop wording tested with two model providers | Another wording broke with a provider that does not reason privately: the agent narrated and sent the action alone |
| **`mv-5r`** | "Never end a reply with text only" in the manifest | One career stopped without a score after 21 replies carried no tool call |
| **`mv-5r`** | Hidden costs named before a review, at the starting level only | DeepSeek applied the review rule but misread costs (for example, that a polite refusal keeps Network); used at every level, the same text added risk before later reviews |
| **`mv-5r`** | Quarterly plan by level and a Health brake; `Stalled` and `Concerns` fields removed | DeepSeek rarely filled the stall field, so v4's stall-based quarterly lines seldom fired |
| **`VERSION`** (Cut 3) | A growth exception: one mild risk a month while the HR remark is friendly, when it grows Skill, Network or Output more than any safe option | Our research planner gained about five points over strict risk avoidance, mostly by reaching the fifth level earlier; Cut 2's careers that completed were held back by the pace of promotions, not by risk |
| **`VERSION`** | At the starting level, one point of Health in the quarter before a review instead of the whole quarter | In development careers whose last quarter before the first review went entirely to Health, the first review was won 6 times in 19; with one point and the rest on the review, 9 in 11 |
| **`VERSION`** | A stalled-start protocol: no added risk, prefer risk-lowering options, keep the review stats, defuse every quarter | In our careers the third starting-level review was lost to hidden risk in 7 of 11 cases with the review stats in place; in faithful replays, careers following this order were rescued 3 times in 8, against 0 in 6 without it |


## 7. Generalisation, scope and limits

The Skill contains no event titles, fixed answers, dataset references, months tied to specific events or unpublished thresholds. Every rule is phrased in terms of what the agent observes: the HR remark, review talks, the displayed effects of quarterly actions, the quarterly menus seen in the current run and its own notes. Health and Dignity margins are stated as our own margins on the published 0–10 range, and anything learned from our runs is marked as our observation, so the game's own signals come first. The same procedure applies if event wording or order changes.

The main limits we know of:

- **Perception.** DeepSeek still misreads part of the options that lower Output or Network. About one career in four still collapses, mostly by never leaving the starting level.
- **Review calendar.** The countdown assumes the published six-month review cycle. If the talk arrives later than expected, the Skill keeps protecting; a different calendar would shift the countdown.
- **Reply format.** The turn loop was verified with two model providers, not with all of them. Some providers occasionally write a tool call as text; the manifest line keeps this to a few replies per career.
- **Long context.** Each run accumulates a long history. One-reply decisions and one-line notes keep it to about a third of our Cut 1 version.

The companion decision report gives the evidence and its limits.
