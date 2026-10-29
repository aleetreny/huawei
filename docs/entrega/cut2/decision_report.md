# Decision report — Gradient Depression

Submission: **cp-v5a**, Cut 2, 30 October 2026. Results below are development measurements with the official runner and designated DeepSeek model, not organiser-issued evaluation scores. They belong to the current cp-v5a bundle, not a future corrected revision.

## Why this candidate

Our work after Cut 1 separated decision quality from execution overhead. Every model call can resend a growing conversation, so reducing redundant narration and model round trips can improve efficiency without changing the game's state transitions. A fake-model runner probe established sequential execution of grouped calls; model probes showed that the literal tool_calls example elicited grouping more reliably than softer prose. These tests establish mechanics and instruction following, not improved career decisions.

cp-v5a combines that protocol with shorter status notes, a stalled-start response, a qualitative rule for all-risky options and Skill-focused quarterly actions from L4. The changes are bundled, so comparisons cannot identify the causal effect of each one. Three completed careers provide direct evidence for this candidate. They do not establish consistent performance across unknown evaluation careers.

## Verified career results

The figures were checked against the three original score_report.json files for the cp-v5a run group, rather than copied from estimates in the research narrative.

| Career | Quantitative score | Months | Final level | Total tokens | Tokens/month | Token efficiency |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 66.27 | 48 | L5 | 31,411,020 | 654,396.25 | 93.8242 |
| 2 | 65.10 | 48 | L5 | 29,509,546 | 614,782.21 | 95.4087 |
| 3 | 68.13 | 48 | L5 | 30,606,083 | 637,626.73 | 94.4949 |
| Mean | **66.50** | 48 | L5 | | **635,601.73** | **94.5759** |

All three completed with maximum Health and Dignity and zero final risk. Token efficiency is calculated using the published formula. The measured game and efficiency contributions sum to **62.6576** on the automated version scale; the full score would be `62.6576 + 0.1 × official design-quality score`. Quality 65 would imply approximately 69.16, but that is a scenario, not a measured official score. Claude quality judgements are proxies and are not substituted for the official judge.

The two completed Cut 1 v4 reference careers scored 71.67 and 70.22, with efficiency approximately 61.2 and 65.8. These are selected completed reference careers, not a matched estimate of overall superiority. Other family careers stalled or failed. At equal game performance, the efficiency difference is worth roughly three automated-score points; it does not establish that cp-v5a has higher expected total performance.

## Decision-bank warning

In 90 L1 review-preparation situations, cp-v5a had mean research loss 4.42 versus 3.31 and 3.68 in two v4 passes. Best-choice rates were 59% versus 61% and 60%; choices reducing Network or Output numbered 27 versus 24 and 25; risky choices numbered 8 versus 7 and 6. cp-v5a agreed with v4 in 84 of 90 choices; the two v4 passes agreed in 81.

Much of the excess loss concentrates in two copies of one situation. This limits independence and makes the average sensitive to rare costly disagreements. It does not prove the difference is noise, nor establish a reliable regression. Bank loss is not a change in full-career score. A v4-c5 hybrid with the new loop has no equivalent career evidence here, so we do not transfer v4 or cp-v5a results to it.

## What the evidence can and cannot establish

The local replica and recorded-situation banks were research tools for screening hypotheses. They are not shipped with the agent. Exact-effect research bots have information the deployed model lacks; their scores cannot forecast this model's performance. Repeated control readings reveal model variability, but not every candidate has repeated measurements.

The grouped-call protocol was observed in real careers, although compliance varied and some replies still contained one call. A later related variant also showed a career with almost no grouping, so the format is not guaranteed to work on every run. We retain tool outputs and actual token accounting; lower narration does not imply suppressed failures or rewritten evidence.

The current Skill assumes stable quarterly option numbers and a precise review boundary. Its stalled-start rule also goes beyond the handbook's statement about weak reviews by counting reviews without promotion. Those assumptions require review; the design document identifies their provenance and limits. The in-game handbook itself explicitly describes two weak reviews and a second trust blow-up, so those two statements should not be mislabelled as unpublished discoveries.

No evidence here establishes 75-point consistency. The candidate offers three completed careers and substantially lower measured token usage, with a remaining early-career decision risk. Any change to quarterly observation, policy or wording must be identified as a revision; these results remain evidence for its parent, not measurements of the revision.
