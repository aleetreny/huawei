# Target-actor budget: USD 50 key and three submissions

Plan written on 26 October 2026, before the key arrived. It follows `lab/protocol/prereg-v1.md` §12, with one change the user asked for: before the key exists, Claude workers play the real dev game to find out what works. Their results stay in their own actor cells. Key spend goes only where Claude evidence cannot answer the question.

## What the key must buy

1. **Cost and fidelity pilot (about 6 % of the key).** Two complete episodes in the official runner:
   - the minimal policy P0;
   - the current Claude-screened leader.

   They measure tokens per month (the `E` term), USD per episode, wall-clock time and whether the agent finishes. They fix the real budget arithmetic. Without them the plan below is only an estimate.
2. **Transfer check (about 30 %).** Four to six policies that span the Claude-proxy ranking from best to worst, with two target episodes each, so we can see whether the Claude ranking transfers to deepseek-v4-flash. This deliberately buys a cheap, rough calibration, not pruning authority: the protocol needs at least 8 policies, which the key cannot afford. If the leader on Claude is clearly not the leader on the target, Claude screening loses its say for that family.
3. **Finalist confirmation (about 40 %).** At most two finalists plus the incumbent, run on fresh episodes after freezing. Selection never uses these data.
4. **Reserve (about 24 %).** Regression checks the day before each cutoff, recovery from operational failures, and the official-route variance the dev runner cannot see.

The per-episode price is an estimate from public OpenRouter rates for deepseek-v4-flash, before any measurement: USD 0.6–1.2 for a full 48-month run, less for early exits. On that estimate the key buys roughly 40–80 episodes, and the shares above are about 3 + 12 + 20 + 10 episodes at the conservative end. **Recompute after the pilot.**

## Submissions (Stage 1 = best of at most three scored versions)

| Cutoff (24:00 UK) | Basis for the choice | Rule |
|---|---|---|
| 27 Oct (R1) | Claude-worker screening on real dev, plus the pilot if the key arrives in time. | Posterior-best distinct policy among those screened; ties go to the simpler and cheaper policy. Label it an estimate. |
| 30 Oct (R2) | Transfer check on the target plus Claude racing. | Posterior-best under the target actor where it was measured; otherwise the Claude leader, corrected by the transfer check. |
| 1 Nov (R3) | Confirmation on the target. | Confirmed finalist, or the best posterior mean when confirmation cannot reach Δ. Design docs and video tell the evidence story. |

Each version must differ in content (identical content is not rescored). The official three-run evaluation is run by the organisers and does not use our key.

## Guardrails

- Every target episode is registered as a job: actor `jiuwenswarm-target`, route `competition-key`, one private slot per concurrent run. The scheduler refuses target work beyond the planned share unless the orchestrator records a decision.
- Token counts in `score_report.json` are summed after every episode, and the estimated spend is compared with the plan. If an episode costs more than twice the pilot estimate, target work pauses until the cause is understood.
- Interrupted target episodes are never scored. The runner gives an early exit a `quantitative_score`; that is a game result and is kept.

## How many families to race on the target (playbook P34 planner, `stats.budget_planner`)

Assumed episode SD σ = 12 Y-points (to be measured). The table gives the expected true mean of the chosen family relative to the average family, with the selection share of the budget split equally. Entries marked "infeasible" give fewer than 4 episodes per family, the protocol's dormancy minimum.

| Selection episodes | τ (between-family SD) | K=2 | K=3 | K=4 | K=5 | K=6 |
|---|---|---|---|---|---|---|
| 11 (B=20) | 8 | 3.8 | infeasible | infeasible | infeasible | infeasible |
| 22 (B=40) | 4 | 1.7 | 2.2 | 2.5 | 2.6 | infeasible |
| 22 (B=40) | 8 | 4.2 | 5.9 | 6.9 | 7.5 | infeasible |
| 44 (B=80) | 8 | 4.3 | 6.3 | 7.5 | 8.2 | 8.8 |

Decision: Claude screening narrows the ten initial policies to **4–5 families** for the target race. With fewer than about 40 affordable target episodes, race 2–3. Rerun the planner after the pilot with the measured σ and the first-block τ.
