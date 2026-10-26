# CareerLab cloud run — status

Generated 26 Oct 14:48 UTC in the Claude Code cloud container, branch `cloud-lab-run`. All scores are Claude-proxy results on the dev split (`real-dev`), not official scores and not the target actor (deepseek-v4-flash in JiuwenSwarm). Under prereg-v1 section 8 they cannot prune or select by themselves.

## At a glance

- Jobs in the registry: done 249, interrupted 22, leased 28.
- Episodes finished in this container: 0. Batches completed: 0.
- Five-hour quota (`careerlab.scheduler.latest_quota`): utilisation **0.84**, window resets 26 Oct 16:00 UTC; governor cap 0.8. The window is shared with every session on the account.
- Seven-day quota: utilisation **0.14**, window resets 26 Oct 16:00 UTC; weekly allowance now **0.894** (`weekly_allowance`: straight line from 0.10 at the window start to 0.90 at 2 Nov 00:00 UTC, about 0.126 a day). New episodes wait while either window is over its limit.
- Claude CLI pinned to 2.1.303 (the version frozen in the registry's actor records; the container ships 2.1.310), so new runs land in the existing Haiku (`08e9167a965ed82c`) and opus~100k (`eaaedd84f8f22e6d`) cells.

## Latest pre-registered block decision (Haiku actor)

Registry decision #88, recorded 26 Oct 14:07 UTC (`careerlab.decisions.block_decision`, record=True).

Actor `08e9167a965ed82c` — robustness across noise models: True (robust: leader dd49c06cd04e433e and dormant set ['3207e8f585cbe240', 'ed78f44ccd41adf8'] agree across normal, student_t, bayes_boot)

| Policy | runs in prefix | pending | posterior Y (sd) | P(best) | action | reason |
|---|---:|---:|---|---:|---|---|
| f3-feedback-reactive-v1 | 3 | 2 | 60.21 (2.31) | 0.421 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f3-balance-recombined-v1 | 2 | 2 | 58.85 (2.63) | 0.221 | **REPEAT** | REPEAT: n=2 < n0=4 |
| f3-lean-v1 | 2 | 2 | 57.47 (2.63) | 0.101 | **REPEAT** | REPEAT: n=2 < n0=4 |
| f7-three-skills-v1 | 3 | 2 | 49.95 (6.54) | 0.041 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f1-steady-balance-v1 | 4 | 0 | 49.28 (7.08) | 0.043 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.043, P(mu >= mu_L - 4) = 0.176, n=4) |
| f7-single-skill-v1 | 3 | 2 | 48.76 (6.54) | 0.027 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f1-review-risk-v1 | 3 | 0 | 48.65 (7.24) | 0.039 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f2-convert-on-review-v1 | 3 | 0 | 45.89 (8.3) | 0.03 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f4-review-first-v1 | 3 | 0 | 45.09 (9.12) | 0.036 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f4-visible-delivery-v1 | 3 | 2 | 44.94 (9.12) | 0.035 | **REPEAT** | REPEAT: n=3 < n0=4 |
| p0-review-guard-v1 | 3 | 0 | 40.18 (5.27) | 0.0 | **REPEAT** | REPEAT: n=3 < n0=4 |
| p0-minimal-v1 | 5 | 0 | 39.42 (4.89) | 0.0 | **DORMANT** | DORMANT: n=5 >= n0=4 and P(mu >= mu_L - 4) = 0.001 < 0.05 (mean 39.4 vs leader dd49c06cd04e433e 60.2) |
| m3-subtracted-v1 | 3 | 0 | 38.42 (8.32) | 0.003 | **REPEAT** | REPEAT: n=3 < n0=4 |
| m3-sustainable-career-v0-1 | 4 | 0 | 38.01 (8.18) | 0.002 | **DORMANT** | DORMANT: n=4 >= n0=4 and P(mu >= mu_L - 4) = 0.016 < 0.05 (mean 38.0 vs leader dd49c06cd04e433e 60.2) |
| f6-commitment-ledger-v1 | 3 | 2 | 34.91 (7.49) | 0.0 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f2-invest-early-v1 | 3 | 2 | 31.14 (8.3) | 0.0 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f5-relationship-capital-v1 | 3 | 2 | 29.88 (6.96) | 0.0 | **REPEAT** | REPEAT: n=3 < n0=4 |

Leader history (stall trigger: leader posterior mean not improved by 2 Y-points over 3 decisions):

| Decision | Time | Leader | Posterior Y |
|---:|---|---|---:|
| #78 | 26 Oct 13:26 UTC | f3-feedback-reactive-v1 | 61.34 |
| #83 | 26 Oct 13:39 UTC | f3-feedback-reactive-v1 | 61.34 |
| #88 | 26 Oct 14:07 UTC | f3-feedback-reactive-v1 | 60.21 |

## Progressive widening (Haiku cell)

| Family | terminal Haiku episodes N_f | cap ⌈(1+N_f)^0.5⌉ | children so far |
|---|---:|---:|---:|
| p0-minimal | 8 | 3 | 1 |
| m3-teammate | 7 | 3 | 1 |
| f3-feedback-reactive | 7 | 3 | 2 |
| f1-steady-balance | 7 | 3 | 1 |
| f7-one-vs-many | 6 | 3 | 0 |
| f4-visible-delivery | 6 | 3 | 1 |
| f2-invest-early | 6 | 3 | 1 |
| f6-commitment-ledger | 3 | 2 | 0 |
| f5-relationship-capital | 3 | 2 | 0 |

## Children created in this cloud run

None yet.

## Teacher distillation

User request relayed by the strategy session at about 14:25 UTC: distil Opus's winning games into new F3 children, with general rules only.

- Input: the 14 Opus game digests made on the Mac (`lab/reports/teacher-digests/opus/`, merged from `main` 7945fe4): 8 completed, 6 eliminated, under F1, P0 and M3. Opus never played F3.
- Design: both children are built on f3-lean's 250-word F3 core, so they stay under the 400-word limit and are nested. f3-lean ⊂ attribution child (adds only the strongest rule) ⊂ full distilled child (adds all rules). F3 itself is 483 words, so "F3 + one rule" would break the limit. Parents are recorded as F3, with f3-lean as the text base.
- Status: analysis and draft bundles in progress (one subagent). Registration waits until the F3 family's Haiku N_f reaches 9, so the cap ⌈(1+N_f)^0.5⌉ allows 2 more children beside f3-lean and f3-balance-recombined. Children enqueued now could not run before batch 2 anyway.
- Digests of new Opus games played here will go to `lab/reports/teacher-digests/opus-cloud/`. `careerlab digest` skips games without a local run folder and rewrites `index.md`, so writing into `opus/` would drop the 14 Mac games from that index.

## Problem A check: Haiku vs opus~100k on shared policies

opus~100k decision computed with the same rule but **not recorded** (only the Haiku decision is the block decision).

| Policy | Haiku posterior Y (n) | opus~100k posterior Y (n) | opus~100k pending |
|---|---|---|---:|
| f1-steady-balance-v1 | 49.28 (4) | 65.56 (2) | 0 |
| p0-minimal-v1 | 39.42 (5) | 61.58 (2) | 0 |
| m3-sustainable-career-v0-1 | 38.01 (4) | 38.99 (2) | 0 |

Shared policies with opus~100k data: 3. Spearman of posterior means 1.00; top policy Haiku `f1-steady-balance-v1`, opus~100k `f1-steady-balance-v1` (agree). Descriptive only: with this few shared policies and 2–4 runs per cell, agreement cannot certify transfer (pruning authority needs ≥ 8 shared policies spanning ≥ 16 Y-points).

## Actor comparison (all Claude-proxy episodes, `careerlab.analysis`)

Imported episodes from the Mac have no local `result.json`; their rows come from the registry evaluation (early-exit causes are blank for them).

| Actor | eps | interrupted | completion | mean Q (sd) | mean Y | mean months | rejected/ep | min/ep | min/month | cache-read M/month | list-USD/ep |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| haiku | 53 | 0 | 0.55 | 45.5 (17.8) | 44.1 | 38.5 | 0.02 | 10.1 | 0.26 | 0.52 | 0.79 |
| haiku@low | 6 | 0 | 0.33 | 39.2 (16.2) | 38.0 | 33.7 | 0 | 7.0 | 0.21 | 0.302 | 0.36 |
| opus | 3 | 0 | 0.33 | 33.9 (19.3) | 33.8 | 32 | 0 | 7.1 | 0.22 | 0.238 | 3.01 |
| opus@low | 5 | 0 | 0.4 | 43.2 (15.3) | 41.6 | 33.2 | 0 | 6.5 | 0.2 | 0.222 | 2.88 |
| opus~100k | 6 | 0 | 0.83 | 57.8 (19.4) | 55.4 | 44 | 0 | 12.6 | 0.29 | 0.123 | 3.27 |
| sonnet | 26 | 0 | 0.38 | 39.4 (20.0) | 38.4 | 35 | 0.04 | 8.2 | 0.23 | 0.258 | 1.66 |

| Actor | Policy | n | Q per episode | months | mean Y | early-exit causes |
|---|---|---:|---|---|---:|---|
| haiku | f1-review-risk-v1 | 3 | [51.8, 24.0, 61.0] | [48, 24, 48] | 44.8 |  |
| haiku | f1-steady-balance-v1 | 4 | [51.0, 66.6, 27.7, 71.8] | [48, 48, 24, 48] | 52.2 |  |
| haiku | f2-convert-on-review-v1 | 3 | [61.2, 30.0, 63.6] | [48, 24, 48] | 49.6 |  |
| haiku | f2-invest-early-v1 | 3 | [47.1, 18.3, 18.6] | [47, 18, 24] | 27.4 | ; ;  |
| haiku | f3-balance-recombined-v1 | 2 | [63.0, 59.2] | [48, 48] | 58.9 |  |
| haiku | f3-feedback-reactive-v1 | 3 | [59.7, 66.3, 66.6] | [48, 48, 48] | 61.3 |  |
| haiku | f3-lean-v1 | 2 | [50.1, 64.3] | [48, 48] | 55.8 |  |
| haiku | f4-review-first-v1 | 3 | [19.7, 60.3, 62.5] | [24, 48, 48] | 46.3 |  |
| haiku | f4-visible-delivery-v1 | 3 | [55.9, 59.1, 17.6] | [48, 48, 24] | 43.7 |  |
| haiku | f5-relationship-capital-v1 | 3 | [21.8, 48.5, 23.1] | [24, 39, 24] | 29.9 | ; ;  |
| haiku | f6-commitment-ledger-v1 | 3 | [30.5, 25.8, 49.7] | [30, 8, 48] | 34.9 | ;  |
| haiku | f7-single-skill-v1 | 3 | [54.2, 63.9, 20.6] | [48, 48, 24] | 45.3 |  |
| haiku | f7-three-skills-v1 | 3 | [50.4, 51.5, 67.1] | [48, 48, 48] | 55.1 |  |
| haiku | m3-subtracted-v1 | 3 | [16.0, 60.6, 48.9] | [24, 48, 48] | 41.8 |  |
| haiku | m3-sustainable-career-v0-1 | 4 | [17.2, 70.2, 27.8, 30.9] | [24, 48, 24, 26] | 35.5 | ; ;  |
| haiku | p0-minimal-v1 | 5 | [53.9, 57.4, 31.6, 32.0, 18.5] | [48, 48, 22, 23, 24] | 37.9 | ; ;  |
| haiku | p0-review-guard-v1 | 3 | [41.9, 54.2, 45.1] | [33, 42, 47] | 42.6 | ; ;  |
| haiku@low | f1-steady-balance-v1 | 2 | [55.2, 62.1] | [48, 48] | 56.9 |  |
| haiku@low | m3-sustainable-career-v0-1 | 2 | [29.4, 21.5] | [23, 24] | 25.3 | ;  |
| haiku@low | p0-minimal-v1 | 2 | [28.4, 38.5] | [24, 35] | 31.7 | ;  |
| opus | f1-steady-balance-v1 | 1 | [56.2] | [48] | 54.9 |  |
| opus | m3-sustainable-career-v0-1 | 1 | [21.4] | [24] | 22.1 |  |
| opus | p0-minimal-v1 | 1 | [24.2] | [24] | 24.4 |  |
| opus@low | f1-steady-balance-v1 | 2 | [40.2, 30.2] | [24, 26] | 33.2 | ;  |
| opus@low | m3-sustainable-career-v0-1 | 2 | [51.8, 28.9] | [48, 20] | 39.8 |  |
| opus@low | p0-minimal-v1 | 1 | [65.0] | [48] | 62.0 |  |
| opus~100k | f1-steady-balance-v1 | 2 | [69.8, 69.2] | [48, 48] | 65.6 |  |
| opus~100k | m3-sustainable-career-v0-1 | 2 | [19.1, 59.6] | [24, 48] | 39.0 |  |
| opus~100k | p0-minimal-v1 | 2 | [62.0, 67.0] | [48, 48] | 61.6 |  |
| sonnet | f1-steady-balance-v1 | 4 | [30.7, 57.8, 42.0, 53.3] | [32, 48, 45, 48] | 44.2 | ;  |
| sonnet | f2-invest-early-v1 | 2 | [35.9, 17.2] | [30, 24] | 26.3 | ;  |
| sonnet | f3-feedback-reactive-v1 | 2 | [64.4, 20.5] | [48, 24] | 41.5 |  |
| sonnet | f4-visible-delivery-v1 | 2 | [15.0, 19.0] | [24, 24] | 18.6 | ;  |
| sonnet | f5-relationship-capital-v1 | 2 | [20.9, 64.3] | [18, 48] | 41.6 |  |
| sonnet | f6-commitment-ledger-v1 | 2 | [60.6, 44.9] | [48, 35] | 49.7 |  |
| sonnet | f7-single-skill-v1 | 2 | [71.4, 59.2] | [48, 48] | 62.2 |  |
| sonnet | f7-three-skills-v1 | 2 | [48.4, 28.3] | [48, 24] | 38.2 |  |
| sonnet | m3-sustainable-career-v0-1 | 4 | [45.5, 15.9, 16.7, 73.1] | [39, 24, 24, 48] | 36.5 | ; ;  |
| sonnet | p0-minimal-v1 | 4 | [20.1, 25.5, 59.1, 14.2] | [24, 18, 48, 21] | 30.0 | ; ;  |

| Actor A | Actor B | shared policies | same top | Spearman |
|---|---|---:|---|---:|
| haiku | haiku@low | 3 | True | 1.0 |
| haiku | opus | 3 | True | 1.0 |
| haiku | opus@low | 3 | False | -0.5 |
| haiku | opus~100k | 3 | True | 1.0 |
| haiku | sonnet | 10 | False | 0.2 |
| haiku@low | opus | 3 | True | 1.0 |
| haiku@low | opus@low | 3 | False | -0.5 |
| haiku@low | opus~100k | 3 | True | 1.0 |
| haiku@low | sonnet | 3 | True | 0.5 |
| opus | opus@low | 3 | False | -0.5 |
| opus | opus~100k | 3 | True | 1.0 |
| opus | sonnet | 3 | True | 0.5 |
| opus@low | opus~100k | 3 | False | -0.5 |
| opus@low | sonnet | 3 | False | -1.0 |
| opus~100k | sonnet | 3 | True | 0.5 |

## What is next

- **Batch 1** has 28 jobs, held by the quota governor until the 16:00 UTC reset:
  - 18 Haiku screens, F3 children first;
  - 6 opus~100k Problem-A runs;
  - 4 calibrate replacements queued on the Mac, at priority −10.
- **14:47 UTC: merged `main` 3db7af9 and restarted the scheduler before the reset.** The merge adds seven-day pacing to `wait_for_quota`. The 28 leased jobs were released and re-leased; none had started. The 4 calibrate replacements on default opus and opus@low now run last (recorded as a `reprioritise` decision). They were not cancelled: both actors are weak and no decision depends on them.
- **Weekly pacing caps the lab.** After the reset, the account may use about 0.126 of the week per day, starting from a 0.10 allowance. Before the pacing change, one five-hour window at the cap cost about 15 % of the week. Expect roughly one five-hour window of episodes before the weekly line binds, then a trickle overnight. Orchestration counts against the same budget.
- **After batch 1:** record the Haiku block decision. The stall trigger is expected to fire (leader 61.34 → 60.21 over the first three decisions).
- **New candidates, all screened on Haiku with n = 4 and priority 20:**
  1. Two F3 children from the Opus teacher distillation: the full distilled bundle and an attribution child with only the strongest rule. The F3 cap ⌈(1+N_f)^0.5⌉ allows these two once N_f ≥ 9 terminal Haiku episodes.
  2. A new family, **secure-then-grow**, requested by the strategy session after the score-gap finding. Completed games miss about 40 points, mostly level and wealth. The family keeps F3's survival and review-recovery rules and adds a growth mode that seeks promotion and wealth when reviews are solid and no risk warning is active. It is the stall response for this block: playbook P10, "less defensive family with response to warnings".
