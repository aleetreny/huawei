# Skills design — Gradient Depression

**Submission `TODO(manual: version name)`, Cut 2 (30 October 2026).** One Skill, `skills/career-rules/SKILL.md`, plus the manifest instruction. JiuwenSwarm 0.2.4b3, single-agent `agent` mode. No scripts and no reference files. TODO(manual: confirm the Skill name and that there is still one Skill and no script.)

This version keeps the structure of our Cut 1 submission (`t13-read-v4`) and changes TODO(manual: one sentence on what changes and where).

## 1. Our understanding of the task

Career Survival asks a single agent to sustain a career while developing it. The public handbook describes a 48-month horizon, monthly story choices, quarterly Energy and main actions, and six-monthly reviews. Growth competes with wellbeing, working relationships, money and hidden risk. Story outcomes are not shown before choosing, so the agent has to infer the likely consequence of each option from its wording.

We separate three questions: what does this option probably change, what does the career need now, and which instruction applies in this phase? Our research found failures at all three layers. More detailed strategy did not automatically improve play: instructions were sometimes followed in the wrong phase, and correct priorities were applied to misread options. The Skill is built around those three questions.

The agent decides only from the current run: `observe` (state, events, choices), the handbook, review talks, the monthly HR remark, warnings and its own recent log entries. The Skill supplies priorities, a reading guide and a note format, not answers for named events, numerical thresholds or a model of hidden risk.

## 2. One Skill, with the key scope repeated in the manifest

The design has one discoverable `career-rules` Skill used on every turn. It contains the turn loop, the status line, the story procedure and the quarterly priority list.

- **Why one Skill.** Earlier multi-Skill versions let the agent retrieve one relevant-looking rule while missing another. A single Skill was retrieved consistently in our DeepSeek and proxy-model tests.
- **Why the manifest repeats the scope.** In development careers, DeepSeek read the Skill early and then relied on its context; it did not reopen supporting files. The manifest instruction therefore states the three behaviours that matter most: keep stories and quarterly phases apart, drop options that may bury a problem, and protect Skill, Network and Output just before a review. It also asks the agent to reread the Skill whenever its rules are no longer in view, for example after a summary.
- **No delegation.** Everything runs in one agent; there is no team mode and no sub-agent.

## 3. Turn loop and status line

Each turn is: `observe`, read `events` first, decide with the section for the current phase, then `take_action` with a note. If the last note is not in view, the agent calls `check_latest_logs` to recover it. A rejected action leads to reading the error, observing again and choosing a valid option.

Every note starts with one status line, which is the agent's compact memory:

`Review in N | Now S N O | Best S N O | Stalled: none | Concerns this month: 0`

- **Review in N** is computed from the visible month and the published six-month review schedule. It is a switch: the review-preparation steps apply only when N is 1 or 2, which keeps a narrow preference from leaking into the rest of the career.
- **Now** and **Best** record Skill, Network and Output as observed, and the best value of each seen at the current level. A stat below its Best has lost ground the agent should repair before a review. Best resets on promotion.
- **Stalled** records an expected gain that did not appear in this run. In quarterly phases the agent writes `Expect …` from the displayed effects of its action and compares it with the next observation. It is provisional and is cleared on promotion or when the stat rises again. It is not a claim about a hidden limit.
- **Concerns this month** counts story choices the agent itself judged might bury a problem. It records the agent's judgement, not a hidden-risk value.

The note stays well under 1,000 characters, which also limits token use.

## 4. Stories: read consequences, then choose in a fixed order

The story section first asks for the likely sign of each option's effect on Skill, Network, Output, Health, Dignity, Wealth and hidden risk. The reading guide describes in general terms what tends to raise or lower each one: own judgement and preparation build Skill; delivering and making results visible builds Output; helping and crediting others builds Network; hiding, shortcuts, private or partial fixes and open conflict add hidden risk. It also says that missing a risky option costs more than flagging a safe one.

The agent then applies five ordered steps, skipping a step only if it would remove every option:

1. **Survive:** drop options that could end the run now.
2. **Risk:** drop options that may add hidden risk; when the HR remark is not the friendly one, or a concern was already recorded this month, also drop private, anonymous, partial or postponed fixes.
3. **Wellbeing:** protect Health and Dignity when they are low or falling.
4. **Review close (N = 1 or 2):** avoid options that may lower Network or Output, and in the review month Skill as well. Repair a stat that fell below its Best. While the HR remark is friendly or quiet, this step comes before avoiding a *mild* risk in the review month. Hiding, denying, blaming, gambling and cutting corners stay excluded in every month.
5. **Grow:** choose the option that raises most of Skill, Network and Output that are not stalled, weighting a stat the latest review talk named as lagging. In the final quarter, prefer Health, Dignity and lower risk.

## 5. Quarterly phases: first matching line wins

The quarterly list chooses Energy and main actions only, never a story option. The agent spends affordable Energy one action at a time and observes again. The first matching line wins:

1. the final quarter of the career (recover, defuse risk, report results);
2. low or falling Health or Dignity, or Network or Wealth near zero for months (recover first);
3. an HR remark that is not friendly (defuse risk; lay low while it stays worrying);
4. a lagging stat named in a review talk (invest in it until the next review);
5. Network and Output both stalled (turn to Skill);
6. otherwise, invest in the growth stats that are not stalled, with a main action that matches what is still rising.

Concrete, ordered quarterly directions were followed much more reliably than general goals in our obedience tests.

## 6. What changed from earlier versions, and why

| Version | Change | Reason, from our development careers |
|---|---|---|
| `t13-read-v1` | Reading guide for consequences and risk | DeepSeek recognised risk better than Skill or Output effects |
| `t13-read-v2` | Review protection moved into the Skill body and the manifest; strict story/quarter separation; stricter risk step | A quarterly rule leaked into stories; "constructive-sounding" private or phased fixes caused a trust crisis |
| `t13-read-v3` | In the review month, keeping Skill, Network and Output comes before a mild risk while HR is calm | Promotions were lost by one point in the last story before a review |
| `t13-read-v4` (Cut 1) | `Best` per level; protect Network and Output from two months before a review and repair losses at once | A career lost Output with two months to go while chasing Network it could no longer raise |
| **TODO(manual: version name)** | TODO(manual: change) | TODO(manual: the log finding behind it) |

## 7. Generalisation, scope and limits

TODO(manual: if sections 2–5 changed, update them to match the submitted Skill word for word before packaging; the reviewers compare this document with the Skill.)


The Skill contains no event titles, fixed answers, dataset references, months tied to specific events or unpublished thresholds. Every rule is phrased in terms of what the agent observes: the HR remark, review talks, the displayed effects of quarterly actions and its own notes. The same procedure applies if event wording or order changes.

The main limits we know of:

- **Perception.** DeepSeek still misses part of the options that lower Output or Network. A single lost point before an early review can delay a promotion.
- **Memory fields.** DeepSeek fills the status line reliably but rarely marks a stat as Stalled, so the stall-based quarterly lines seldom fire. TODO(manual: if this version adds a quarterly rule for later levels, say how it avoids depending on Stalled.)
- **Long context.** Each run accumulates a long history. Short notes keep token use down, but late in a run some model calls returned a generic refusal instead of an action.

The companion decision report gives the evidence and its limits.
