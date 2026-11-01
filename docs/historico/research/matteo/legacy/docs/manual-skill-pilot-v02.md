# Growth with a reserve: manual candidate v0.2

## Result and comparison

One Codex-assisted manual run completed all 48 months with **73.4/100**, **199 actions**, and final level **L5**. The candidate instructions stayed fixed; their recorded hashes still match the files at completion. Candidate source is commit `d5a7a51`. The helper submitted explicitly selected actions and recorded public MCP responses; it did not select actions or call a model.

| Measure | v0.1 pilot | v0.2 growth pilot |
|---|---:|---:|
| Completed months | 48 | 48 |
| Score | 69.4 | 73.4 |
| Final level | L5 | L5 |
| Health / dignity | 10 / 10 | 10 / 10 |
| Skill | 119 | 128 |
| Network | 43 | 54 |
| Output | 31 | 35 |
| Wealth in ending report | 29.5 | 37.5 |

Final visible wealth was 37; the ending report used 37.5. The reported score improved by **4.0 points**, principally through wealth and network. Local score contributions were level 15.0, wealth 9.4, wellbeing 15.0, skill 15.0, risk 10.0, network 9.0. These are observed local results, not a scoring formula to embed in submission Skills.

## Promotion hypothesis

Both runs reached L2 at month 6, L3 at month 12, L4 at month 24 and L5 at month 42. Review grades were also identical: C, B, B, B, B, A, A, B at months 6 through 48. **The growth-focused revision did not accelerate promotion in this run.** An A at month 36 did not immediately change the level. This does not establish a special L4 barrier, a minimum tenure, or any unpublished numerical requirement.

## What changed in the candidate

The three Skills explicitly allowed bounded wellbeing costs for useful learning and ownership, treated promotion readiness as an ongoing objective, discouraged unnecessary recovery, and required reassessment when nominal action benefits were not reflected in observed state. Candidate instructions were not edited mid-run.

## Observations worth carrying forward

- Growth and recovery need a budget. Health reached 1 before the month-12 allocation; two recovery actions restored it to 5. The run survived, but such a thin reserve was fragile. A bounded-looking opportunity can still consume meaningful health, so account for commitments and proximity to the next recovery opportunity.
- More investment did not always change visible statistics. For example, extra report preparation at month 33 left Output unchanged; subsequent relationship maintenance also left Network unchanged, while rotation increased Skill. Shift attention based on observed benefit without claiming an internal cap or a universal action schedule.
- Wider ownership, evidence-based communication, mentoring and follow-through supported a completed career with strong final relationships. These are qualitative interpretations of choices, not isolated measurements of each Skill's effect.
- Strong visible statistics did not remove explicit risk warnings. Cleanup was used when warnings appeared; the final local risk-control contribution was 10.0. There is no evidence that all cleanup actions were necessary.
- Terminal energy was directed toward useful relationship gains rather than topping up already full wellbeing. Final wellbeing still reached 10/10. This supports examining resource allocation, but does not prove the earlier run was universally too conservative.

## Limits and next experiment

These are two unpaired manual runs with different event trajectories, the same ongoing Codex conversation and prior experience. They do not isolate the effect of the Skill revision, establish an expected score, or validate automatic Skill discovery. There were **no competition-model API calls**, but manual reasoning consumed normal Codex usage. JiuwenSwarm and the designated model remain unevaluated.

Keep the present revision as a separate candidate. A useful next comparison would vary quarterly growth allocation while holding the decision-maker and evaluation setup fixed, recording review feedback and all promotion dates. Avoid memorized event-answer tables and inferred hidden thresholds. Confirm any improvement across multiple runs before calling it reliable.

The live panel now displays the completed result. Detailed current-run evidence remains local under `.career-lab/` and is excluded from Git; the tracked [summary](experiments/manual-skills-v02-summary.json) records final state, milestones, hashes and ending text without publishing an event-answer catalogue.

## Handoff

Both complete manual pilots are available on branch `Matteo`: this report and [v0.1](manual-skill-pilot-v01.md), with compact JSON evidence in `docs/experiments/`. Raw session histories stay local and are not part of a submission. The live monitor is development tooling only. The three v0.2 Skill hashes matched their run-start values at completion.

The growth hypothesis improved the observed score by 4.0 points but did not move any promotion date. Official-model evaluation and a controlled comparison remain pending. Do not pool these results with Haiku/M3 lab samples.

Next: use main's T4 workflow to propose an independent growth policy with a hypothesis, predicted behaviour and refutation criterion. Let the central cloud evaluate it; do not start local lab runs before T11. To retrieve this evidence without changing main, run `git fetch origin Matteo`, then `git show origin/Matteo:docs/manual-skill-pilot-v02.md` (or the corresponding v0.1 path). No new games are needed to inspect these results.
