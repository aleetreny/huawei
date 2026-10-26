# observed-growth-v5 and four fresh v3 replicates: v3's first batch was lucky

## What was run

After v4 (three changes at once) lost to v3 ([matteo-observed-growth-v4.md](matteo-observed-growth-v4.md)), two arms were played in the same batch, 26 Oct 18:58–19:35 UTC, 8 parallel slots, same actor as v1–v4 (`017798b931bc18f8`, `claude-cli:haiku`, CLI 2.1.310), origin `matteo`, purpose `pilot`:

- **v3 replicates** (policy `fe970f0dc37fa905`, jobs 00004–00007): does v3's 4/4 completion hold?
- **v5** (policy `fc33794755955007`, parent `observed-growth-v3`): v3 plus two sentences only: prefer story options that secure concrete pay, bonuses, raises or recognised roles on fair terms; aim for strong review grades. Lint clean.

## Results

| Arm | Job | Outcome | Months | Q | Final level | Wealth dim |
|---|---|---|---:|---:|---|---:|
| v3 | 00004 | completed | 48 | 60.62 | L4 | 40.0 |
| v3 | 00005 | dismissed | 24 | 19.15 | L1 | 10.1 |
| v3 | 00006 | blackout | 12 | 19.75 | L1 | 5.6 |
| v3 | 00007 | dismissed | 24 | 23.07 | L1 | 8.9 |
| v5 | 00000 | dismissed | 24 | 14.57 | L1 | 6.4 |
| v5 | 00001 | dismissed | 24 | 23.90 | L1 | 8.9 |
| v5 | 00002 | completed | 48 | 52.82 | L4 | 27.9 |
| v5 | 00003 | trust crisis | 24 | 29.98 | L3 | 1.8 |

All Haiku pilots of the family so far (origin `matteo`):

| Version | Episodes | Mean Q | Completed |
|---|---:|---:|---:|
| v1 | 4 | 40.85 | 1/4 |
| v2 | 4 | 43.17 | 2/4 |
| **v3** | **8** | **51.04** | **5/8** |
| v4 | 4 | 32.76 | 1/4 |
| v5 | 4 | 30.32 | 1/4 |

## Interpretation

- **v3's first batch (4/4, mean 71.43) was largely luck.** The four fresh replicates gave 1/4 completed and mean 30.65. Over eight episodes v3 is 5/8 and mean 51.04: still the best version of the family, but below the race's Haiku leaders (about 60) rather than above them. The earlier claim that v3 beats the leaders does not hold.
- **The first promotion decides the career.** Across all 24 episodes, every career that stayed at L1 into the second year was dismissed at the month-24 review or died earlier; careers promoted in the first year mostly finished. In the replicates, 0/4 v3 careers were promoted at the first window, against 4/4 in the first batch, with the same manual and actor. This looks driven by event draws and hidden factors more than by the manual, and no version has found a reliable way to force it.
- **v5's wealth preference did not help.** One completion in four, with low wealth even in the completed career. With four episodes this is not evidence that it hurts, but it gives no reason to adopt it.
- **Health and hidden risk remain live failure modes even in v3** (one blackout in the replicates; a trust crisis in v5).

## Relevo

1. **Done:** wrote `observed-growth-v5` on branch `matteo/observed-growth-v5` (built on `matteo/observed-growth-v3`); lint clean; played 4 v5 and 4 v3 episodes in one batch under origin `matteo`; exported.
2. **Data:** `lab/registry-origins/matteo/*.jsonl` (24 jobs and evaluations, v1–v5). Trajectories outside Git under `~/careerlab-data/huawei-matteo/runs/` in the sandbox.
3. **Unfinished:** nothing interrupted. v5 is not proposed.
4. **Next:** treat v3 as a mean-51 candidate, not 71; the race's own measurement with the race actor is what counts. The open problem is getting out of L1 in the first year; a useful next step is to compare the first-year decisions of promoted and non-promoted careers (24 trajectories available) before writing any new version, and to compare with how F3/f3-recombined handle the first year.
5. **ESTADO.md:** T4 line updated; PR #5 commented with the corrected v3 figure.
