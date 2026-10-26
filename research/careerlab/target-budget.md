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
