# Skills design — Gradient Depression

**Submission `c3-k3`, Cut 3 (1 November 2026).** One Skill, `skills/career-rules/SKILL.md`, plus the manifest instruction. JiuwenSwarm 0.2.4b3, single-agent `agent` mode. No scripts and no reference files.

This version keeps the story judgement of our Cut 1 submission (`t13-read-v4`): the reading guide, the list of risky wording and the five ordered story steps. It keeps the way of working introduced in Cut 2 (`mv-5r`): each decision is one reply with two tool calls and a one-line note. What is new targets the starting level, where most of our failed careers ended: the first two reviews and the third one need opposite attitudes to hidden risk, and the Skill now says so.

## 1. Our understanding of the task

Career Survival asks a single agent to sustain a career while developing it. The public handbook describes a 48-month horizon, monthly story choices, quarterly Energy and main actions, and six-monthly reviews. Growth competes with wellbeing, working relationships, money and hidden risk. Story outcomes are not shown before choosing, so the agent has to infer the likely consequence of each option from its wording.

We separate three questions: what does this option probably change, what does the career need now, and which instruction applies in this phase? Our research found failures at all three layers. More detailed strategy did not automatically improve play: instructions were sometimes followed in the wrong phase, and correct priorities were applied to misread options. The Skill is built around those three questions.

The agent decides only from the current run: `observe` (state, events, choices), review talks, the monthly HR remark, warnings and its own recent log entries. The Skill supplies priorities, a reading guide, a turn loop and a note format, not answers for named events, numerical thresholds of the game or a model of hidden risk. The few numbers it contains are our own safety margins on the published 0–10 ranges and are labelled as such.

## 2. One Skill, with the key scope repeated in the manifest

The design has one discoverable `career-rules` Skill used on every turn. It contains a 48-month plan, the turn loop, the status line, the story procedure, the quarterly priority list and a quick reference for stats near a limit.

- **Why one Skill.** Earlier multi-Skill versions let the agent retrieve one relevant-looking rule while missing another. A single Skill was retrieved consistently in our DeepSeek and proxy-model tests.
- **Why the manifest repeats the scope.** In development careers DeepSeek read the Skill once, at the start, and then relied on its context; the decisions that settle a career come 40 to 500 replies later. The manifest instruction is always in view, so it states what matters most: the two-call turn loop and never ending a reply with text only; keeping stories and quarterly phases apart; dropping options that may bury a problem; protecting Skill, Network and Output before a review; and the stalled-start protocol.
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
2. **Risk:** the first matching case applies.
   - **Stalled start** (two reviews at the starting level without a promotion): until the next review, first drop every option that may add risk, whatever it saves, including private, partial or temporary fixes; then keep Skill, Network and Output as in the review month; only then prefer the option that documents, reports, follows the process or fixes fully.
   - **Review exception** (not stalled, HR remark friendly or quiet, the month before any review, or either of the two months before a review at the starting level): keeping Skill, Network and Output comes before avoiding a *mild* risk. Hiding, denying, blaming, gambling and cutting corners stay excluded in every month.
   - **Strict mode** (the HR remark is not the friendly one, or a risky choice was already made this month): also drop private, anonymous, partial or postponed fixes, and prefer an option that documents, reports, owns or fully fixes the problem.
   - **Otherwise** drop options that may add risk. In every case, if every option looks risky, the smallest and most reversible risk wins.
3. **Wellbeing:** with Health at 3 or below (our margin), drop anything that may lower it, even before a review; with Health or Dignity low or falling, drop options that lower them; avoid spending when Wealth is below zero, and prefer involving someone when Network is at zero.
4. **Review close (N = 1 or 2):** first repair Network or Output if it is under its Best. Otherwise avoid options that may lower Network or Output, and in the review month Skill as well: going against a person may cost Network; giving up time or credit from one's own delivery may cost Output; avoiding the work or the learning may cost Skill.
5. **Grow:** choose the option that raises most of Skill, Network and Output, counting twice a stat the latest review talk named as lagging, minus one for each it lowers. In the last quarter of the career, prefer Health, Dignity and lower risk. Ties go to lower risk, then Health and Dignity, then the option that costs no money.

**Why the starting level has two risk attitudes.** The handbook says two weak half-year reviews end a run. In our development careers, the first two reviews at the starting level were weak in the same way whatever the HR remark said, so what decided them was keeping Network and Output; a mild risk that keeps them is the better trade, and the next quarters can defuse it. A career still at the starting level after those two reviews was promoted at the third only when it reached that review with the friendly HR remark, and otherwise dismissed six months later. From then on hidden risk is the one thing that cannot be traded.

## 5. Quarterly phases: first matching line wins

The quarterly list chooses Energy and main actions only, never a story option. The agent spends all its Energy, plans the whole quarter after one `observe`, and uses the effects shown in the menu. The first matching line wins:

1. **The final quarter of the career:** defuse risk if needed, recover Health and Dignity, report results; no new growth spending.
2. **Near a limit (the Health brake):** with Health at 5 or below (our margin), Health recovery comes first; with low or falling Health or Dignity, Wealth below zero or Network at zero, recover the stat at risk and repair a relationship, with no spending.
3. **Stalled start:** defuse legacy risk first, then one point on the stat under its Best; lay low when Network and Output are at their Best, otherwise report results.
4. **The HR remark,** classified by tone whatever its wording: if it is not friendly, defuse risk first, and lay low while it stays worrying.
5. **A review talk named a lagging stat:** spend on that stat until the next review.
6. **Level 4 and above:** Skill first: Skill learning while Health allows, one point on reports or on Network if Network lost ground, and Apply for rotation.
7. **Otherwise:** reports, Network maintenance and Skill learning, and Apply for a key project.

Concrete, ordered quarterly directions were followed much more reliably than general goals in our obedience tests.

## 6. What changed from earlier versions, and why

| Version | Change | Reason, from our development careers |
|---|---|---|
| `t13-read-v1` | Reading guide for consequences and risk | DeepSeek recognised risk better than Skill or Output effects |
| `t13-read-v2` | Review protection moved into the Skill body and the manifest; strict story/quarter separation; stricter risk step | A quarterly rule leaked into stories; "constructive-sounding" private or phased fixes caused a trust crisis |
| `t13-read-v3` | In the review month, keeping Skill, Network and Output comes before a mild risk while HR is calm | Promotions were lost by one point in the last story before a review |
| `t13-read-v4` (Cut 1) | `Best` per level; protect Network and Output from two months before a review and repair losses at once | A career lost Output with two months to go while chasing Network it could no longer raise |
| `mv-5r` (Cut 2) | One reply per decision (`take_action` + `observe`); one-line note; "never end a reply with text only"; Health brake; level-4 Skill quarter | v4 used 1.35–1.47 million tokens per game month; one career stopped after 21 replies without a tool call |
| `mv-5r` (Cut 2) | Hidden costs of polite or helpful options named at the starting level | DeepSeek misread some costs; in later checks this did not improve the first review in careers, and Cut 2 lost two of its three official careers at the starting level |
| **`c3-k3`** (Cut 3) | v4's story rules with the Cut 2 loop | In faithful replays of the first months, v4's rules with the one-reply loop won the first review far more often than without it |
| **`c3-k3`** | Mild-risk exception in both months before the first two reviews at the starting level | Those reviews were decided by one point of Network or Output, not by the HR remark |
| **`c3-k3`** | Stalled-start protocol: no added risk, defuse every quarter, keep Network and Output | Seven of the eleven careers that reached the third starting-level review lost it to hidden risk with all three stats in place |
| **`c3-k3`** | A 48-month table, a review calendar, margins labelled as ours, a quick reference near limits | Reviewers of our documents found a dangling reference, vague limits and a quarterly line that contradicted the one-reply loop |

## 7. Generalisation, scope and limits

The Skill contains no event titles, fixed answers, dataset references, months tied to specific events or unpublished thresholds. Every rule is phrased in terms of what the agent observes: the HR remark, review talks, the displayed effects of quarterly actions, the quarterly menus seen in the current run and its own notes. Health and Dignity margins are stated as our own margins on the published 0–10 range, and anything learned from our runs is marked as our observation, so the game's own signals come first. The same procedure applies if event wording or order changes.

The main limits we know of:

- **Perception.** DeepSeek still misreads part of the options that lower Output or Network, and some options that add risk read as responsible. A stalled start is only rescued if the agent also sees which options add risk.
- **Review calendar.** The countdown assumes the published six-month review cycle. If the talk arrives later than expected, the Skill keeps protecting; a different calendar would shift the countdown.
- **Reply format.** The turn loop was verified with several model providers, not with all of them. Some providers occasionally write a tool call as text; the manifest line keeps this to a few replies per career.
- **Long context.** Each run accumulates a long history. One-reply decisions and one-line notes keep it to about a third of our Cut 1 version.

The companion decision report gives the evidence and its limits.
