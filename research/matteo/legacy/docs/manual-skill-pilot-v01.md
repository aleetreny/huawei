# Sustainable Career v0.1: first complete manual Skill exercise

## Result

One manual Codex-assisted session completed all **48 months**, making **200 actions** including initialization and quarterly choices. The local simulator reported **69.4/100**, ending at **L5** with **Health 10**, **Dignity 10**, **Skill 119**, **Network 43** and **Output 31**.

The ending score report used **Wealth 29.5**; the final observation's status field displayed 29. Both are preserved in the [summary evidence](experiments/manual-skills-v01-summary.json), rather than silently changing one to match the other.

## Method and scope

The exercise used the three candidate Skills at commit `27cd3c1`: risk review, event decisions and quarterly planning. The instructions stayed unchanged. Codex read the candidate and selected each action manually from the currently available choices through the official MCP interface, checking consequences before the next decision. A small local helper only submitted the explicitly selected action and recorded tool responses; it contained no autonomous decision policy.

This continued the separate pilot previously started through month 2, not the user's browser game. All 200 actions are included in the count. Detailed current-run observations and reasons were retained locally; only a compact summary is tracked here to avoid turning the research into an event-answer catalogue.

There were **no competition-model API calls**. This exercise used the ongoing Codex session and its normal usage. It did not run JiuwenSwarm, test automatic Skill discovery, or use the designated competition model.

## Career milestones

| Month | Observed milestone |
|---:|---|
| 6 | L1 to L2; performance C |
| 12 | L2 to L3; performance B |
| 18 | Remained L3; performance B |
| 24 | L3 to L4; performance B |
| 30 | Remained L4; performance B |
| 36 | Remained L4; performance A |
| 42 | L4 to L5; performance A |
| 48 | Completed the career at L5; performance B |

## Ending contributions returned by this session

| Dimension | Contribution to local score |
|---|---:|
| Career level | 15.0 |
| Wealth | 7.4 |
| Health and dignity | 15.0 |
| Professional skill | 14.9 |
| Risk control | 10.0 |
| Workplace network | 7.2 |

The simulator reported a total of 69.4; the displayed contributions are rounded individually and should not be used to reconstruct a more precise total. These are results of one local session, not guaranteed official weights or a scoring formula for the Skills.

## What was useful in the instructions

- **Dynamic recovery:** health losses were corrected at available opportunities without making every quarter defensive. Wellbeing was full at the end.
- **Warning-driven risk handling:** explicit risk warnings prompted legacy cleanup and, when warranted, a risk-reducing main action. High visible statistics were not treated as proof that organizational liabilities were resolved.
- **Consequences and follow-through:** the next decision considered commitments and observed outcomes, including the need to repair relationships after boundaries or escalation.
- **Bounded commitments:** several choices balanced delivery and collaboration through scope, timing, handovers or a realistic plan rather than unlimited extra work.
- **End-of-run priorities:** the final allocation restored health and strengthened relationships instead of pursuing output solely for a review that had already happened.

These are descriptions of how the manual interpreter used the guidance, not measured causal effects of individual Skills.

## Weaknesses and questions exposed

1. **Some reasonable compromises still produced adverse consequences.** Temporary technical mitigation did not eliminate a later incident in this session. The interpreter adapted to the new evidence, but the original judgment was not optimal in hindsight. Do not convert this into a fixed answer for that event; test broader guidance about severity, unresolved liabilities and the limits of mitigation.
2. **Career progress stalled for a long period.** L4 lasted from month 24 until month 42. A completed career and full wellbeing did not maximize level or wealth. A useful next hypothesis is whether more explicit review-driven growth planning improves progression without compromising survival.
3. **Nominal logged gains sometimes differed from displayed state changes.** The interpreter noticed this and avoided assuming that repeating a growth action guaranteed further visible improvement. We did not inspect internals or derive hidden caps, thresholds or formulas.
4. **The narrative sometimes indicated strain while the health panel was high.** Decisions considered those explicit signals, not just numeric status. A simpler agent may miss this unless the risk Skill is actually loaded and followed.
5. **Risk management may have been conservative.** Cleanup and recovery consumed opportunities for other actions. The result supports testing this balance, not assuming every protective action was necessary.

## Comparison with the random baseline

The historical random batch had 0 completions in 73,858 sessions, mean survival 5.91 months and mean score 11.78. This manual run completed 48 months with 69.4. The difference is encouraging evidence that purposeful play can succeed in the local environment.

It is **not** an estimate of the effect of these Skills. The decision-maker, reasoning process, event trajectories and behavior differ, there is no matched no-Skill Codex baseline, and this is a single trial. The ongoing conversation also contained previous development context. We cannot infer an expected score, completion probability or designated-model result from it.

## Terminal-state handling

After the final action, the observation advanced its bookkeeping month to 49, with no choices and the reason `Completed the 48-month simulation.` The ending report explicitly stated 48-month completion and survival of 48 months. The raw flags nevertheless contained `alive: false` and `failed: true`. For this record, completion is classified from the explicit ending and report, rather than incorrectly labeling it an early failure from that flag alone. No engine data or flags were modified.

## Next step

Keep v0.1 as a reference candidate. Before changing instructions, run additional independent manual exercises if useful for clarity, and later use the required JiuwenSwarm setup and designated model for actual candidate evaluation. Record any revised candidate separately. Test a review-driven growth change or an alternative risk balance one at a time; do not build a memorized response map from this transcript.

See the [evaluation plan](skill-evaluation-plan.md) for the proposed 100-run target and its API-key, identity and budget prerequisites. This completed exercise is **one manual run**, not one completed official-model run in that batch.
