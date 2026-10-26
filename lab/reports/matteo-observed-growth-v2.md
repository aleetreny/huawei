# observed-growth-v2: design from trajectories and four Haiku episodes

## Why v2

Matteo's hypothesis: Skill drives career level, and level drives wealth, so the strategy should build toward each promotion window and be phased around the review cycle. Evidence used: the five Haiku episodes of `observed-growth-v1` (origin `matteo`, see [matteo-observed-growth-haiku-4.md](matteo-observed-growth-haiku-4.md)), Matteo's manual pilots on branch `Matteo` and the public handbook returned by `show_employee_handbook`.

Findings from v1 trajectories:

- The handbook ties promotion to Skill, Network, Output and level, pays a base salary that rises with level, and pays review bonuses as a multiple of that salary. Level and wealth together are about half of the ending score.
- Story events, not quarterly actions, produced most stat gains. In the first 24 months of the completed v1 career, within-level changes after story choices were +44 Skill, +20 Network, +18 Output; after quarterly Energy, about +0/+4/+2. In the three losses, story choices gave roughly zero.
- Every completed career (this one, the first pilot and both manual pilots) was promoted at the first promotion window; every loss stayed at L1 until dismissal with Skill, Network and Output frozen from the first review on.
- The losses spent most Energy on Defuse legacy risk (no visible effect) and on Health recovery with Health already high. Skill learning was never used.

## What v2 changes

One Skill (525 words, v1 had 461): growth rationale from the published rules; story choices that take ownership and deliver; a quarter-end note with previous and current Skill/Network/Output and whether a review follows; build quarters (capability) alternating with review quarters (visible results); Skill learning; Defuse and Health recovery restricted to concrete need; a forced change of mix when stats did not rise; a survival plan after a weak review. Lint: no findings. Policy `f2715987f0341ab2`, parent `observed-growth-v1`.

## Result: four Haiku episodes

Same actor as the v1 pilots (`017798b931bc18f8`, `claude-cli:haiku`, CLI 2.1.310), origin `matteo`, purpose `pilot`, 26 Oct 17:35–18:05 UTC.

| Job | Outcome | Months | Q | Level path | Risk control dim |
|---|---|---:|---:|---|---:|
| 00000 | trust crisis (2nd blow-up) | 30 | 34.18 | L2 m6, L3, L4 | 0 |
| 00001 | completed | 48 | 59.32 | L2 m21, L3 m24, L4 | 40 |
| 00002 | trust crisis (2nd blow-up) | 19 | 24.28 | L2 m12, L3 m18 | 0 |
| 00003 | completed | 48 | 54.92 | L2 m6, L4 | 80 |

| | v1 (4 episodes) | v2 (4 episodes) |
|---|---:|---:|
| Mean Q | 40.85 | 43.18 |
| Completed | 1 | 2 |
| Promoted out of L1 by the first year | 1 | 3 |
| Capability dismissals | 3 | 0 |
| Trust crises | 0 | 2 |
| Defuse legacy risk per episode | 4–8 | 0–1 |
| Best completed Q | 70.94 (L5) | 59.32 (L4) |

## Interpretation

- **The review-cycle and growth changes worked.** No capability dismissals; three of four careers left L1 within the first year, including one that recovered at the fourth window. Quarter-end notes show the build/review flag, the before/after comparison and Skill learning, so the mechanism executed.
- **The Energy-discipline change backfired.** Restricting Defuse removed almost all cleanup, and both losses are trust crises from accumulated hidden risk. Defuse has no visible effect but is not useless. The rule "only for a concrete exposure" was wrong.
- **Level caps on stats.** In every episode (v1 and v2) Skill stopped at 9 while at L1 and at 21 while at L2, then resumed after promotion. Level unlocks Skill as much as Skill unlocks level. Skill learning at a stalled Skill wastes Energy; Output and Network are the inputs to push then. This is an observation from 9 episodes, not a published rule, so it must not be written as a number in a Skill.
- **Health ran thin.** Three of four v2 episodes touched Health 1–3 in the first year. None died of it, but the margin is small.
- Completed v2 careers scored below the v1 winner (L4 rather than L5, lower risk control). With four episodes per arm, none of these differences is reliable.

## Relevo

1. **Done:** analysed v1 trajectories and Matteo's pilots; wrote `observed-growth-v2` on branch `matteo/observed-growth-v2` (built on `matteo-t4-growth`); lint clean; played 4 Haiku pilots under origin `matteo`; exported to `lab/registry-origins/matteo/`.
2. **Data:** `lab/registry-origins/matteo/*.jsonl`. Trajectories stay outside Git under `~/careerlab-data/huawei-matteo/runs/` in the sandbox.
3. **Unfinished:** nothing interrupted. v2 is not proposed for the race yet.
4. **Next:** write `observed-growth-v3` from v2, keeping growth, review phasing and the quarter-end comparison, but restoring regular risk cleanup (Defuse whenever HR or management signals accumulated risk, as v1 did) and replacing Skill learning by Output/Network actions when Skill has stopped rising. Then play 4 matched Haiku episodes and compare with v1 and v2. Commands: `uv run careerlab lint lab/policies-src/matteo-feedback-growth/observed-growth-v3`, `uv run careerlab register …`, `uv run careerlab enqueue --policy <id> --actor claude-cli:haiku --n 4 --purpose pilot --why "…"`, `uv run careerlab run --kind claude-cli --slots 4 --max-five-hour 0.9`, `uv run careerlab export`.
5. **ESTADO.md:** T4 line updated.
