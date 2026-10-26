# observed-growth-v1: four Haiku episodes (origin `matteo`)

## Result

Matteo requested four Haiku episodes of `observed-growth-v1` (policy `f03981dac92f8b6c`, same content hash as the first pilot) on 26 October 2026, 16:47–17:05 UTC. They were played under origin `matteo` (T11), purpose `pilot`, four slots in parallel, with a five-hour quota stop at 0.9. They are outside the race's prereg-v1 decisions.

| Job | Outcome | Months | Q | Final level | Skill | Network | Output | Wealth |
|---|---|---:|---:|---|---:|---:|---:|---:|
| 00000 | dismissed (2nd weak review) | 24 | 28.45 | L1 | 9 | 0 | 3 | 6 |
| 00001 | completed | 48 | 70.94 | L5 (month 42) | 116 | 46 | 32 | 35 |
| 00002 | dismissed (2nd weak review) | 24 | 32.26 | L2 | 9 | 2 | 3 | 8 |
| 00003 | dismissed (2nd weak review) | 24 | 31.76 | L2 | 9 | 2 | 3 | 9 |

Mean Q **40.85**, mean Y 38.93 (anytime 95 % interval 7.7–78.0), **completion 1 of 4**. Zero rejected actions and zero interruptions. Including the first pilot (64.78, completed), the candidate has completed 2 of 5 Haiku careers.

## Interpretation

- **The completed career is strong.** At 70.94, with L5 at month 42 and every dimension high, it is above F3's posterior mean and the first pilot. The growth half of the manual works once the actor survives the first year.
- **The survival half fails.** All three losses are the month-24 capability dismissal with Health 9–10, so wellbeing is not the constraint. By month 24 Skill, Network and Output stay near their starting values (9 / 0–2 / 3).
- **Likely mechanism (from the action notes, not proven).** In the losing games, the main action is "Apply for a key project" almost every quarter while Output stays at 2–3. Energy goes mostly to Health recovery and Defuse legacy risk whenever HR or a doctor mentions accumulated risk, with at most one point on report materials. The realized-benefit check ("an investment that leaves its statistic unchanged is not repeated automatically") is never invoked. In the winning game the same main action raised Output by about 2 each time, so the loop was rewarded.
- So with Haiku, the bundle is high-variance: excellent when early investments pay, a C–C dismissal when they do not. That pattern resembles the full distilled F3 child, which also loses most often at month 24.

## Caveats

- Actor `017798b931bc18f8` is `claude-cli:haiku` on CLI 2.1.310 in a cloud sandbox, not the race actor `08e9167a965ed82c` (CLI 2.1.303). Do not pool with race cells.
- Four episodes; the interval is wide. Played on Matteo's own Claude account, not the team Max account.

## Relevo

1. **Done:** resolved the ESTADO.md conflict on PR #1 (commit `8d64afc`); registered `observed-growth-v1` locally under origin `matteo` after importing the race registry; played 4 Haiku pilots; exported to `lab/registry-origins/matteo/`.
2. **Data:** `lab/registry-origins/matteo/*.jsonl` (jobs, evaluations, scores, token use). Trajectories are outside Git under `~/careerlab-data/huawei-matteo/runs/` in the sandbox, referenced by SHA-256 in the evaluations.
3. **Unfinished:** nothing interrupted. The trajectories are not committed and will not survive the sandbox.
4. **Next:** keep v1 immutable. A `observed-growth-v2` should make the realized-benefit check executable for the first year: if Output has not risen after a review named results as the weakness, switch the main action and spend Energy on delivery evidence instead of repeated risk cleanup when Health is already high. Then play a small matched block. The organiser can import with `uv run careerlab import --dir lab/registry-origins/matteo` (expect `conflicts: 0`).
5. **ESTADO.md:** T4 line updated with these results.
