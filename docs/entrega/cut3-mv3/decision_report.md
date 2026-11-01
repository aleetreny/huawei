# Decision report — Gradient Depression

**Submission `VERSION`, Cut 3 (1 November 2026).** All scores below come from our own development runs with the official runner and the designated model, or from our local tools. None is an organiser-issued evaluation.

## 1. Our decision process

We treated a Skill as a testable decision policy. A proposed change needed a predicted behavioural effect and a way it could fail: misreading an option, ignoring an instruction, applying it outside its scope, or damaging another objective. We used inexpensive local analysis to screen ideas, targeted model tests to examine interpretation, and development careers through the official tools to expose failures that isolated decisions missed.

These stages answer different questions:

- a simulator shows whether information would be useful;
- a perception test asks whether the model can recognise it;
- an obedience bank asks whether instructions change a choice;
- a complete career tests whether those choices work together.

We did not treat passing an earlier stage as proof of the next.

## 2. A local replica for screening

Our replica was built from recorded outputs of our own games through the official interfaces. On 600 new development careers it reproduced 99.3% of next steps exactly, agreed on 99.5% of promotions and had a mean absolute final-score error of about 0.33 points. These are research validation results, not guarantees about another event set.

The next-step test starts from observed states, so errors do not accumulate as they do in a free-running simulation. Some benchmarks also give research bots more accurate state information than a submitted agent has. We therefore used simulator comparisons to prioritise hypotheses, not to forecast DeepSeek's score.

The simulator is a research tool only. Nothing in the Skill is copied from it: no thresholds, formulas, event answers or schedules beyond the published review cycle.

## 3. Instruction delivery, obedience and leakage

We checked how a Skill reaches the agent rather than assuming its body is permanently visible. Consolidating related responsibilities into one Skill avoided selective retrieval. Concrete, ordered quarterly directions proved easier to follow than general ambitions: DeepSeek's agreement with two tested allocation prescriptions rose from about 2% and 15% without the Skill to 65% with it.

The obedience bank reused observed development situations and compared choices under different instructions. It included a general-choice block outside the intended intervention, and a repeated control to measure the model's own variability.

This exposed a major failure: an earlier combined manual changed about one in five unrelated story choices, and in proxy careers it scored about 13.7 points below the baseline (nine careers per arm). Logs suggested that protecting delivery was displacing useful learning outside the intended window. The response was narrower control: separate quarterly decisions from stories, and write a self-computed review switch (`Review in N`) before applying a scoped preference.

## 4. Perception tests changed our diagnosis

DeepSeek's isolated-option tests showed that it recognised risk better than Skill or Output effects. Initially it detected about 83% of risk increases, 45% of Skill increases and 49% of Output increases. A general reading guide raised Skill-increase recall to about 78% and risk-increase recall to about 86%; Output remained only partly recognised.

Broad categories lost information: a conditional simulator benchmark scored about 46.7 using categories and 56.0 using six stat directions plus a risk sign. These are bot scores with idealised context, not DeepSeek forecasts, but they motivated a reading guide instead of a category list.

Labels also varied between repeated readings of the same options (roughly 12–18% differed), so we compared versions on repeated readings and never on a single one.

## 5. From failing careers to complete ones

Our first DeepSeek development careers with earlier manuals ended early: 18.76 (dismissed at month 24), 14.98 (dismissed) and 42.51 (trust crisis at month 30). Their logs showed two failure routes:

1. **A missed early promotion.** Several reviews were lost because Network or Output fell by one point in the last story before the review.
2. **"Constructive" risk.** Options that sounded responsible (a private talk, an anonymous report, a phased fix) carried hidden risk the model did not see.

Each later version addressed one observed failure (see the design document, section 6). With `t13-read-v2` to `v7`, every career that the game itself ended reached month 48 at L5 with zero risk and full Health and Dignity:

| Manual | Development careers (quantitative score) |
|---|---|
| **`t13-read-v4` (submitted)** | **71.67 and 70.22** (48 months, L5) |
| `t13-read-v5` | 66.71 |
| `t13-read-v7` | 67.27 |

A third `t13-read-v4` career missed the first two promotions by one point each and was then terminated by an infrastructure fault on our machine (a port clash between two local instances), without a score. It shows the remaining weak point: the first review, where a single lost point matters. Some `t13-read-v2` and `v3` careers were stopped by our own budget guard or by the runner's continuation limit, not by the game; we do not count them.

A complete `t13-read-v4` career used about 65–70 million tokens, roughly 1.4 million per month. Token efficiency counts for 10% of the version score, but finishing the career matters far more.

## 5b. What we learned after Cut 1

**Where DeepSeek still loses value.** We compared 419 recorded story decisions from our development careers with what our research planner would have chosen. DeepSeek picked the planner's preferred option 66% of the time at the first level, 74–75% at the second and third and 86% at the fourth, and it rarely took a risky option. The costly choices concentrated in the first three levels, and in situations at the first level with a review close they cost about ten times more than an average story. In half of the costly cases where the better option was not riskier, the agent's own note rejected it as "a private or later fix that may bury the problem".

**Why we kept the cautious risk wording anyway.** We tested a version that told the agent that a private word or a written follow-up to the people concerned does not bury a problem. On review-close situations it improved by 0.46 points per decision, barely more than the gap between two runs of the unchanged Skill (0.37), while on situations with a genuinely risky private option it took more of them. DeepSeek cannot reliably tell a safe private step from a risky one, so a cautious list that sometimes discards a good option is the better trade for this model. Two other changes made no measurable difference: telling the agent that Health and Dignity stop at 10, and rewording the risk cues in the reading guide.

**How much headroom there is.** A research planner with full knowledge of every option's effect averages about 72 on development careers, and the best careers we have observed end at the sixth level. Our complete careers already reach the fifth level, so the remaining gains come from fewer early failures and a faster climb after the fourth level, not from a different overall approach.

## 5c. Evidence for `VERSION`

`VERSION` is the Skill behind our best development careers. Our Cut 2 version (`mv-5r`) differed from it in one paragraph: it named the hidden costs of polite or helpful options before the starting-level reviews only, because on a bank of recorded situations the text seemed to add risk before later reviews. In careers that restriction did not help: `mv-5r` scored 69.00, 22.65 and 24.51 in development and 45.44 officially.

**Tokens.** Token efficiency is 10% of the version score and is full at 500 thousand tokens per game month or fewer. `t13-read-v4` used 1.35–1.47 million, about 64 of 100. With one reply per decision and a one-line note, careers of this family used 0.46–0.70 million (efficiency 92–100).

**Reply format.** The two-call loop held with a provider that does not reason privately (18 of 18 replies in probes) and with one that does. One development career of this Skill stopped without a score after 21 replies carried no tool call, because the model wrote the call as text. A manifest line, "never end a reply with text only … put the decision in the take_action call, not in prose", brought such replies to 1–2 per career, but the same Skill with that line ended early more often (two trust crises and one dismissal in six careers, against none in the careers without it), plausibly because it also discouraged the short written reasoning the model uses when its provider does not reason privately. `VERSION` is the Skill without that line.

**Careers** (development game, official runner, DeepSeek):

| Date | Scores (end) |
|---|---|
| 29–30 October | 68.64, **77.78** (sixth level), 66.06, 63.35, 69.62, 63.27 (all complete); 37.06 (trust crisis at level 4); 18.98 (dismissed at the starting level); one stopped without a score |
| 1 November | TODO(manual: careers) |

Its complete careers averaged 68.1, the best of any family we tested; the starting level remains its weak point.

## 5d. What we learned after Cut 2, and two alternatives we did not promote

**The third review at the starting level is lost to hidden risk.** In our development careers, the first review at the starting level was won about half the time and the second about as often by careers that had lost the first, but the third by 1 of the 11 careers that reached it. Seven of those had Skill, Network and Output in place and received a weak review with a worried HR remark; the weak review itself then cost Network and Dignity, which at first made them look as if they had failed on Network.

**Replays of the first months over-promised.** We built faithful replays of the start of a career (the exact request JiuwenSwarm sends, against the official engine) to compare Skills cheaply. A rebuild of our Cut 1 rules with a stalled-start protocol left the starting level more often there (79% against 73%), and two independent reviewers scored its text highest. In five complete careers it scored 58.06, 52.32, 28.76, 24.90 and 28.34: three dismissals at the starting level and two slow climbs that the replays, which stop at the first promotion, could not see.

**Playing bolder did not raise the ceiling.** A variant of `VERSION` that accepted one mild risk a month while the HR remark was friendly, to climb faster, completed five careers at 60.62, 63.02, 61.53, 63.62 and 62.73, with blow-ups in two; all of them stalled at level 4 for 18–24 months. We went back to the Skill of our best careers.

## 6. Alternatives we did not promote

| Approach | Evidence and decision |
|---|---|
| Multiple independently loaded Skills | Selective retrieval weakened combined guidance; we consolidated responsibilities. |
| Broad category-only story policies | About 46.7 versus 56.0 for richer signs in the conditional benchmark; we kept a finer consequence reading. |
| Always-visible story restrictions | Some variants leaked into unrelated choices and lost heavily; we scope them with `Review in N`. |
| Unstructured log inspection | One variant raised log consultation to 96% without improving choices; logs are retrieved only to recover the status line. |
| More elaborate planning | Rollout improvement did not beat the reference planner (−0.27 ± 1.48 SE in 40 paired careers). |
| A numerical hidden-risk counter | A proxy test identified only 4 of 21 genuinely concerning earlier choices; the concern count stays a judgement, not an estimate. |
| A script that decides from model labels | A teammate's experiment reached our best single career (sixth level), but three of its seven careers ended early, and complete ones used about 1.6 times more tokens; not submitted. |
| Softer risk wording, "Health and Dignity stop at 10", reworded risk cues | No gain in our banks, and the softer wording made genuinely risky private options more likely (section 5b). |
| Hidden costs at the starting level only (Cut 2) | On recorded situations, naming them before every review seemed to add risk before later reviews (0.96 against 0.59); in careers the restriction did not help and Cut 2 scored 45.44 officially, so `VERSION` names them before every review (section 5c). |
| A Skill half as long, with the same loop | Chose like `mv-5r` but failed our risk control by one situation (2.00 against a limit of 1.3 fixed in advance); not promoted. |
| A rewrite for document quality only | Claude reviewers scored it 73.5 against 74.5; below the +3 we required. |
| v4's rules with only the new turn loop | The same token saving (302 and 432 thousand per month), but 23.23 and 58.95 in two careers; not enough to prefer it. |

## 7. Memory and measurement limitations

The status line came from a specific memory use: retain an expected quarterly result and compare it with the next observation. In proxy tests the recorded state was carried forward in 97–100% of cases. In DeepSeek careers the line was always written, but `Stalled` was almost never filled, so in `mv-5r` it was removed and the quarterly plan follows the level instead.

Our bank measurements have known caveats: some story continuations and the end-of-career settlement were missing from early versions, and "right answer" mixed rule compliance with estimated value. The replica was corrected afterwards, but not every historical bank figure was recomputed, so we treat decision-level regret as provisional. Holdout checks were useful but not perfectly isolated.

A handful of development careers cannot separate versions a few points apart, and the official score is the mean of only three careers. For the final cut we chose the Skill with the best record in complete careers, after two alternatives that looked better in cheaper tests (replays and reviewers) did worse in careers. It keeps what we could measure precisely: the one-reply loop that holds with the providers we tried, token use near 500 thousand per game month, and a modest rate of replies without a tool call (2–7 per career, once 21). It does not fix the starting level: DeepSeek still loses Network or Output in about one decision in five before the first review, and some careers end there.

## 8. What we learned about Skills

Skills can supply priority, scope and memory discipline, and they are very effective at changing how an agent works: the reply format alone cut DeepSeek's token use by two thirds. They cannot guarantee that a model understands an unfamiliar option, and a helpful rule can become harmful in another phase. What worked for us was a loop: find a concrete failure in the logs, write the narrowest general rule that addresses it, check that it does not change unrelated choices, and confirm it in a complete career.
