# observed-growth-v3: four Haiku episodes, all completed

## What v3 changes from v2

Design and v1/v2 evidence are in [matteo-observed-growth-v2.md](matteo-observed-growth-v2.md). v3 (policy `fe970f0dc37fa905`, parent `observed-growth-v2`, 542 words, lint clean) keeps v2's growth story choices, review-cycle phasing, quarter-end before/after note and weak-review plan, and fixes its two failures:

- **Risk cleanup restored.** At every quarter-end, Defuse legacy risk comes first whenever HR, the manager, a doctor or an event mentioned risk, warnings or an incident since the previous quarter-end, even when the remark says it is not serious. v2 used Defuse 0–1 times per episode and lost two careers to trust crises.
- **Health reserve.** Health recovery when Health is in the lower half of its range or the planned spending would put it there.
- **Stalled-Skill rule.** If Skill did not rise since the previous quarter-end, skip Skill learning until the next promotion and spend on Output or Network instead.
- **Story choices.** Explicit ban on cutting corners, overpromising, hiding problems, undue credit and bending rules.

## Result

Same actor as the v1 and v2 pilots (`017798b931bc18f8`, `claude-cli:haiku`, CLI 2.1.310), origin `matteo`, purpose `pilot`, 26 Oct 17:56–18:15 UTC.

| Job | Outcome | Q | Level | Wealth dim | Skill dim | Network dim | Risk control dim |
|---|---|---:|---|---:|---:|---:|---:|
| 00000 | completed | 69.38 | L5 | 48.1 | 93.3 | 65.0 | 100 |
| 00001 | completed | 73.62 | L5 | 51.9 | 100.0 | 90.0 | 100 |
| 00002 | completed | 72.78 | L5 | 48.5 | 100.0 | 88.3 | 100 |
| 00003 | completed | 69.92 | L5 | 40.6 | 90.8 | 81.7 | 100 |

| | v1 | v2 | v3 |
|---|---:|---:|---:|
| Mean Q | 40.85 | 43.18 | **71.43** |
| Completed | 1/4 | 2/4 | **4/4** |
| Capability dismissals | 3 | 0 | 0 |
| Trust crises | 0 | 2 | 0 |
| Promoted at the first window | 1 | 2 | 4 |
| Defuse per episode (whole career) | 4–8 | 0–1 | 13–15 |

All four reached L2 by the first promotion window, survived the month-24 review at L3 or L4 and finished at L5. One episode touched Health 2 late in the career and recovered to 9. List-price-equivalent token cost was about USD 4.8 for the four episodes, run on Matteo's Claude subscription (usage quota, not a bill).

## Interpretation and caveats

- Mean Q 71.4 is above the race's Haiku leaders (F3 posterior about 60, f3 recombined 60.6 provisional) and above Opus with an almost empty manual (62–67). This is the strongest observed result so far, but it comes from 4 pilot episodes outside prereg-v1, so no superiority claim is made.
- The actor is not the race actor (`08e9167a965ed82c`, CLI 2.1.303); do not pool with race cells. The target is DeepSeek, not Haiku.
- v3 bundles several changes over v2. The v1/v2/v3 sequence suggests that regular risk cleanup and growth-oriented play are both needed, but which v3 change mattered most is not isolated.

## Relevo

1. **Done:** wrote `observed-growth-v3` on branch `matteo/observed-growth-v3` (built on `matteo/observed-growth-v2`, which is built on `matteo-t4-growth`); lint clean; 230 tests pass; played 4 Haiku pilots under origin `matteo`; exported.
2. **Data:** `lab/registry-origins/matteo/*.jsonl` (12 jobs and evaluations: v1, v2, v3). Trajectories stay outside Git under `~/careerlab-data/huawei-matteo/runs/` in the sandbox.
3. **Unfinished:** nothing interrupted.
4. **Next:** ask the organiser to register `lab/policies-src/matteo-feedback-growth/observed-growth-v3` and screen it against the incumbent with the race actor under prereg-v1, and to import `lab/registry-origins/matteo` (`uv run careerlab import --dir lab/registry-origins/matteo`, expect `conflicts: 0`). If it holds up, it is a candidate for the cut-1 submission (T9). Commands to register locally: `uv run careerlab lint lab/policies-src/matteo-feedback-growth/observed-growth-v3` then `uv run careerlab register lab/policies-src/matteo-feedback-growth/observed-growth-v3`.
5. **ESTADO.md:** T4 line updated.
