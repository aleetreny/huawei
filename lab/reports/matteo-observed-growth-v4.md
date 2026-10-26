# observed-growth-v4: four Haiku episodes (worse than v3; keep v3)

## What v4 changed from v3

Matteo chose three changes after the v3 pilots ([matteo-observed-growth-v3.md](matteo-observed-growth-v3.md)), because v3 saturated health, skill and risk control but finished at L5 with wealth 41–52 and a slow late promotion:

1. **Bottleneck rule.** v3's build/review allocation was replaced by "push whichever of Skill, Network, Output rose least", with action lists per input and High-intensity work allowed for Output when Health is near full.
2. **Trimmed risk cleanup.** Defuse skipped after a mild risk remark if Defuse was spent at the previous quarter-end and nothing else happened.
3. **Explicit wealth.** Story preference for concrete pay, bonus or recognised roles; aim for strong grades.

Policy `5fdf30b08c86d678`, parent `observed-growth-v3`, 590 words, lint clean.

## Result

Same actor as v1–v3 (`017798b931bc18f8`, `claude-cli:haiku`, CLI 2.1.310), origin `matteo`, purpose `pilot`, 26 Oct 18:37–19:05 UTC.

| Job | Outcome | Months | Q | Final level |
|---|---|---:|---:|---|
| 00000 | completed | 48 | 66.72 | L5 |
| 00001 | blackout (Health 0) | 9 | 19.75 | L1 |
| 00002 | dismissed (2nd weak review) | 24 | 20.73 | L1 |
| 00003 | dismissed (2nd weak review) | 24 | 23.82 | L1 |

| | v1 | v2 | v3 | v4 |
|---|---:|---:|---:|---:|
| Mean Q | 40.85 | 43.18 | **71.43** | 32.76 |
| Completed | 1/4 | 2/4 | **4/4** | 1/4 |
| Promoted at the first window | 1 | 2 | 4 | 1 |

## Interpretation

- **The rules executed, the outcome got worse.** Quarter-end notes name the input that "rose least" and spend on it, and Defuse is skipped as specified. But three careers never left L1, the v1 failure pattern.
- **Likely cause: the bottleneck rule at the starting level.** At L1 Skill stalls early, and Network and Output barely move from quarterly actions, so the rule keeps redirecting Energy between flat inputs. v3's fixed alternation (Skill learning and Network in build quarters, visible Output before reviews) gave a steadier push into the first promotion window.
- **Health.** The blackout started at a quarter-end with Health exactly at mid-range: "lower half" did not trigger recovery, 3 Energy went to Defuse and report materials, and story events drained Health to 0 within the quarter. The Health reserve rule is too tight.
- **Noise.** v3's 4/4 first-window promotions may be partly luck; four episodes per arm cannot separate a real effect of a few points. The size of the drop here (about 39 points) is still large enough to keep v3.

## Relevo

1. **Done:** wrote `observed-growth-v4` on branch `matteo/observed-growth-v4` (built on `matteo/observed-growth-v3`); lint clean; 4 Haiku pilots under origin `matteo`; exported.
2. **Data:** `lab/registry-origins/matteo/*.jsonl` (16 jobs and evaluations: v1–v4). Trajectories stay outside Git under `~/careerlab-data/huawei-matteo/runs/` in the sandbox.
3. **Unfinished:** nothing interrupted. v4 is not proposed for the race.
4. **Next:** keep v3 as Matteo's candidate (already merged and queued by the organiser). If another revision is tried, start again from v3 and change one thing at a time: e.g. v3 plus "recover Health when it is at or below mid-range", or v3 plus the wealth preference only; and use 8 episodes to compare with v3.
5. **ESTADO.md:** T4 line updated.
