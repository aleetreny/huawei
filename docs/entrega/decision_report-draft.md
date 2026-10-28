# Decision report — Gradient Depression

**Draft for Cut 1, 27 October 2026. Intended package location: `design/decision_report.md`.**

**TODO(final):** bind this report to the frozen `t13-read-v2` package, resolve the implementation markers in the design document, and add any completed final-version validation. Until then, no result below is a score for the combined manual or an organiser-issued evaluation.

## 1. Our decision process

We treated a Skill as a testable decision policy. A proposed change needed a predicted behavioural effect and a way it could fail: misread an option, ignore an instruction, apply it outside its scope, or damage another objective. We used inexpensive local analysis to screen ideas, targeted model tests to examine interpretation, and development careers through the official tools to expose failures that isolated decisions missed.

These stages answer different questions. A simulator can show that information would be useful. A perception test asks whether the model can recognise it. An obedience bank asks whether instructions change a choice. A complete career tests whether those choices work together. We did not treat passing an earlier stage as proof of the next.

## 2. A local replica for screening

Our replica was built from recorded outputs of our own games through the official interfaces. Validation on 600 new development careers reported 99.3% exact next-step predictions, 99.5% promotion agreement and approximately 0.33 points mean absolute final-score error. These are research validation results, not guarantees about another event set or a generated career.

The next-step test starts from observed states; errors do not accumulate as they do in a free-running simulation. Some benchmarks also provide research bots with more accurate state information than a submitted agent has. We therefore use simulator comparisons to prioritise hypotheses, not to forecast DeepSeek's score.

An independent audit also caught a missing final settlement in the generative driver. Correcting the representation changed accounting, not the strength of a Skill. Keeping such corrections separate from strategy improvements prevented us from calling a repaired prediction a new performance gain.

## 3. Instruction delivery, obedience and leakage

We checked how a Skill reaches the agent rather than assuming its body is permanently visible. Consolidating related responsibilities into one Skill avoided selective retrieval. Concrete, ordered quarterly directions proved easier to follow than general ambitions.

The obedience bank reused observed development situations and compared choices under different instructions. Crucially, we added a general-choice block outside the intended intervention. Its behavioural fingerprint measured both choice agreement and the mix of likely stat changes. A repeated control provided a reference for the model's own variability.

This exposed a major failure: an earlier combined manual changed approximately one in five unrelated story choices. Its final same-batch proxy comparison was about 13.7 career-score points below the baseline, with nine careers per arm. An earlier stopping snapshot was worse; it is not an independent replication. Logs supported the interpretation that protecting delivery was displacing useful learning outside the intended window.

The response was narrower control: separate quarterly decisions from stories and write a self-computed review switch before applying a scoped preference. Proxy results supported that mechanism; DeepSeek's less consistent scoping required renewed testing.

## 4. Perception tests changed our diagnosis

DeepSeek's isolated-option tests showed that risk recognition was stronger than recognition of Skill and Output effects. Initially it detected about 83% of risk increases, 45% of Skill increases and 49% of Output increases. A general reading guide raised Skill-increase recall to about 78% and risk-increase recall to about 86%; Output remained only partly recognised. Recall alone is insufficient, so false alarms and repeated readings also matter.

Broad categories were insufficient: a conditional simulator benchmark scored approximately 46.7 using categories, compared with 56.0 using six stat directions and a risk sign. These are bot scores with idealised contextual information, not DeepSeek career forecasts. The distinction motivated the guide while limiting what we claimed for it.

We repeated label readings because individual labels changed. Between two readings, roughly 12–18% of labels differed, and fixed label sets could move simulated averages by 5–7 points. Large numbers of simulated careers do not eliminate uncertainty arising from only a few model readings.

## 5. What the comparisons establish

The earlier `t13-final` manual averaged 57.2 points across 12 proxy careers, versus 50.5 across 43 pooled baseline careers. The estimated difference was **+6.7 points, SE 5.7** (often abbreviated +6.7 ±5.7 SE); the approximate 95% confidence interval is **−5.3 to +18.7**. It is not a confirmed improvement. Baselines were pooled across batches; the contemporaneous comparison was also inconclusive. Adaptive version selection and interrupted careers further limit causal interpretation.

For DeepSeek, `t13-read-v1` and `t13-final` were compared on 320 story decisions. The reading guide improved the targeted high-risk subset, but aggregate estimated regret changed by only −0.016 points per decision. A title-cluster confidence interval was approximately −0.30 to +0.33. We retained the risk signal as motivation, without claiming a whole-career gain or multiplying decision-level changes by the number of turns.

Two subsequent DeepSeek development careers through the official runner scored 14.98 and 42.51; both ended early, one by dismissal and one by trust crisis. These are local pilots, not official competition scores. They exposed unresolved risk perception and phase leakage despite apparently good bank performance. Their failure motivated clearer phase routing and safety precedence. **TODO(final):** report whether those repairs and the status line have been validated together; do not substitute predecessor results for that evidence.

## 6. Alternatives we did not promote

| Approach | Evidence and decision |
|---|---|
| Multiple independently loaded Skills | Selective retrieval weakened combined guidance; consolidate responsibilities. |
| Broad category-only story policies | Approximately 46.7 versus 56.0 for richer signs in the conditional benchmark; retain finer consequence reading. |
| Always-visible story restrictions | Some Transmission variants leaked and lost heavily; use scoped checks. Other experiments did not show the same loss, so this is a model/version-specific risk, not a universal ban. |
| Unstructured log inspection | A variant raised log consultation to 96% without improving choice accuracy; retrieve logs for a defined memory task. |
| More elaborate planning | Rollout improvement did not beat the reference planner: −0.27 ±1.48 SE in 40 paired development careers. A learned-value approach also failed to establish a better policy. |
| Extra warning and reputation rules | Simulator studies found approximately zero benefit for earlier warning reactions and about +0.1/−0.5 for two review-preparation variants; insufficient reason to add complexity. |
| A numerical hidden-risk counter from guessed choices | A proxy test identified only 4 of 21 genuinely concerning preceding choices. Keep a concern record provisional; do not claim an exact risk estimate. |

## 7. Memory and measurement limitations

Palancas supplied a more specific use for logs: retain an expected quarterly result and compare it with the next observation. Proxy tests carried recorded state in 97–100% of cases; expectation wording improved mismatch detection. This supports a compact status line, but does not establish its DeepSeek career benefit.

The audit identified four important bank caveats: pre-existing story continuations were lost, final settlement was omitted, an older catalogue differed from the later one, and “right answer” mixed prescription compliance with estimated value. Fixed-prefix replay also served saved observations after different agent actions, which could create false expectation mismatches. **TODO(final):** state which measurement fixes were completed and which results were recomputed. Until then, historical regret remains provisional.

Reserved-target checks were useful but not perfectly isolated: some design prefixes contained reserved stories. Label-bot missing-data handling and ideal state access also required qualification. We therefore do not claim a pristine, untouched final holdout. These limitations narrow the conclusions rather than being hidden behind a single accuracy percentage.

## 8. What we learned about Skills

Skills can supply priority, scope and memory discipline. They cannot guarantee that a model understands an unfamiliar option, and a helpful rule can become harmful in another phase. Our contribution is an evidence-linked process that distinguishes those failures and revises the instruction accordingly. The final package must preserve that distinction: measured predecessor results, a clearly specified submitted policy, and an honest account of what remains untested.
