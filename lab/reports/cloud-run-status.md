# CareerLab cloud run — status

Generated 26 Oct 15:48 UTC in the Claude Code cloud container, branch `cloud-lab-run`. All scores are Claude-proxy results on the dev split (`real-dev`), not official scores and not the target actor (deepseek-v4-flash in JiuwenSwarm). Under prereg-v1 section 8 they cannot prune or select by themselves.

## At a glance

- Jobs in the registry: done 249, interrupted 22, leased 42, running 10.
- Episodes finished in this container: 0. Batches completed: 0.
- Five-hour quota (`careerlab.scheduler.latest_quota`): utilisation **0.89**, window resets 26 Oct 16:00 UTC; governor cap 0.97. The window is shared with every session on the account.
- Seven-day quota: utilisation **0.15**, window resets 26 Oct 16:00 UTC; weekly allowance now **0.899** (`weekly_allowance`: straight line from 0.10 at the window start to 0.90 at 2 Nov 00:00 UTC, about 0.126 a day). New episodes wait while either window is over its limit.
- Claude CLI pinned to 2.1.303 (the version frozen in the registry's actor records; the container ships 2.1.310), so new runs land in the existing Haiku (`08e9167a965ed82c`) and opus~100k (`eaaedd84f8f22e6d`) cells.
- **T13 Opus ceiling** (`claude-cli:opus@max~100k`, 2-slot lane, see `lab/reports/opus-ceiling/README.md`): jobs leased 2, running 2; finished games: none yet.

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
| f3-feedback-reactive | 7 | 3 | 4 |
| f1-steady-balance | 7 | 3 | 1 |
| f7-one-vs-many | 6 | 3 | 0 |
| f4-visible-delivery | 6 | 3 | 1 |
| f2-invest-early | 6 | 3 | 1 |
| f6-commitment-ledger | 3 | 2 | 0 |
| f5-relationship-capital | 3 | 2 | 0 |

## Children created in this cloud run

### f8-secure-growth-v1 (`5f8c9648b6abd9b0`, family f8-secure-growth)

- Parents: f3-feedback-reactive-v1, f3-lean-v1; operator: new family seeded from the F3 core (cross-branch hypothesis under the stagnation rule); idea origin: playbook:P10 (less defensive family that keeps its response to warnings), chosen because the stall trigger fires and because of the score-gap finding in findings.md (strategy-session request, 26 Oct ~14:45 UTC).
- Hypothesis: Completed games already survive; the score they leave on the table is mostly career level and wealth (findings.md, 48 completed games, all actors), and every family so far optimises survival. F3's Clear state spends quiet quarters lifting the weakest statistic, which keeps the agent safe but does not compete for promotion. A policy that keeps F3's risk response (Secure) and weak-review plan (Repair) with higher precedence, and otherwise plays for promotion and pay (Grow: Apply for a key project, High-intensity work plus Prepare report materials while Health is comfortable, story options that raise Output, Skill, Wealth or standing at a bounded cost), will earn more A or S reviews, hence more promotions and salary, and end with higher level and wealth dimensions than F3 and f3-lean without more eliminations.
- Haiku runs so far: no finished runs yet.

### f3-opus-distilled-v1 (`c03a1bf3ca04c5e7`, family f3-feedback-reactive)

- Parents: f3-feedback-reactive-v1, f3-lean-v1; operator: distil (teacher); idea origin: user request 26 Oct: Opus teacher distillation (lab/reports/teacher-digests/distilled-rules.md).
- Hypothesis: Opus winners differed from Opus losers less in how they answered warnings (Defuse in the first phase after HR said risks had piled up or worse: 14 of 18 phases vs 11 of 15) than in where routine effort went: Prepare report materials in at least 3 of 4 quarters (8 of 8 winners, 2 of 6 losers); no chasing of the numerically smallest statistic (Network maintenance or Build a mentorship in two-thirds or more of quarters: 0 of 8 vs 3 of 6, exactly the three capability-dismissed games); Apply for a key project kept in both quarters after the first C (7 of 8 vs 1 of 6); Defuse in the last Energy phase before a review that follows a weak one (D 0 of 7 vs 7 of 22); and a blow-up handled as Escalating (both visible trust crises came 1 to 2 months after a blow-up followed by a formal escalation). f3-lean says the opposite on two points (lift the weakest statistic; switch the main action by factor after a C or D). Merging all five rules into f3-lean raises review grades after the opening C and so mean quantitative_score above f3-lean, F3 and f3-distilled-prereview-defuse-v1 in a 4-run Haiku screen, with completion no lower.
- Haiku runs so far: no finished runs yet.

### f3-distilled-prereview-defuse-v1 (`f41d6382cab6ec76`, family f3-feedback-reactive)

- Parents: f3-feedback-reactive-v1, f3-lean-v1; operator: distil (teacher, single-rule attribution); idea origin: user request 26 Oct: Opus teacher distillation (lab/reports/teacher-digests/distilled-rules.md).
- Hypothesis: Every Opus game opened with a C, and the most common Opus exit (3 of 6 losses, plus the eliminated Sonnet F3 run) is C, C, D, D. The D after a weak review followed risk that rebuilt once the agent stopped defusing: of 29 reviews that followed a C or D, none of the 7 preceded by Defuse legacy risk in the last Energy phase before the review was a D, against 7 of the 22 without it. In the decisive case (a third review after C, C) the split is 4 of 4 defused and no D versus 4 of 4 not defused and D, within every seed group and within P0 and M3. Adding one line to f3-lean that sets Defuse legacy risk and Prepare report materials in the second Energy phase after any C or D, whatever the signal state, removes that route for Haiku: no D after a weak review in a 4-run screen and mean quantitative_score at least f3-lean's and F3's.
- Haiku runs so far: no finished runs yet.

### x0-opus-ceiling-v1 (`47cbeec8b03ad2a0`, family ceiling)

- Parents: f3-feedback-reactive-v1; operator: synthesis of general knowledge (measurement arm, not a submission candidate); idea origin: T13 user request 26 Oct: Opus ceiling measurement with all general knowledge.
- Hypothesis: The current leader (F3 feedback-reactive, posterior Y about 60 with Haiku) is limited by two things: the player's reasoning and the policy's coverage (every family so far optimises survival only, and completed careers lose most of their missing ground on career level and wealth). Giving the strongest reasoner (Claude Opus at maximum effort) all our general knowledge in one Skill, namely F3's signal states and responses, f3-balance-recombined's strict precedence, an F8-style growth mode, the decision-relevant published handbook rules and the general form of distilled rules R1-R5, measures how far above the leader the game's ceiling lies when only legally usable, general knowledge is supplied. Expected: completion close to Opus's best observed rate and a mean quantitative_score clearly above F3's, with most of the gain on level and wealth.
- Haiku runs so far: no finished runs yet.

### o1-promotion-gap-v1 (`006571b3bb85b323`, family o1-promotion-gap)

- Parents: ; operator: new family (outside designer); idea origin: T4 outside ideas: agent without access to the team's Skills; sources: handbook, public rules, score structure.
- Hypothesis: Promotion is a multi-stat gate set by the weakest of Skill, Network and Output relative to level; diagnosing that binding gap from feedback, building it in the round after a review and harvesting visible Output in the round before the next one produces more promotions, hence higher final level and wealth, than balanced allocation, while recovering only on low or falling stats keeps survival intact.
- Haiku runs so far: no finished runs yet.

### o2-run-hot-v1 (`663c8cd2a1cafe68`, family o2-run-hot)

- Parents: ; operator: new family (outside designer); idea origin: T4 outside ideas: agent without access to the team's Skills; sources: handbook, public rules, score structure.
- Hypothesis: Survivors fall short on level and wealth because they hold Health and Dignity near full; treating them as fuel and switching between Full, Cruise and Cool modes on observed state and warnings converts the unused resilience margin into more Output and Skill, earlier promotions and more cash taken from events, without raising the early-elimination rate.
- Haiku runs so far: no finished runs yet.

## Teacher distillation

User request relayed by the strategy session at about 14:25 UTC: distil Opus's winning games into new F3 children, with general rules only.

- **Analysis:** [`teacher-digests/distilled-rules.md`](teacher-digests/distilled-rules.md), written by one subagent from the 14 Opus digests (8 completed, 6 eliminated, under F1, P0 and M3; Opus never played F3). W = winners (completed), L = losers (eliminated).
  - **R1 (strongest):** after a C or D, take Defuse legacy risk + Prepare report materials in the last Energy phase before the next review. The next review was D in 0 of 7 such cases against 7 of 22 without it. At the third review after C C, all 4 games that defused avoided D, and all 4 that did not got D.
  - **R2:** Prepare report materials every quarter (8/8 W vs 2/6 L).
  - **R3:** lift a falling statistic or one named in feedback, not the smallest. Heavy Network maintenance or mentorship: 0/8 W vs 3/6 L, exactly the C C D D games.
  - **R4:** keep Apply for a key project after a weak review (7/8 W vs 1/6 L, weak link to later grades).
  - **R5:** a blow-up means Escalating at once (thin evidence).
  - Story style did not separate winners from losers (option 1 in 81 % vs 82 % of story decisions), so it is not a rule.
  - Main confound: actor and game overlap. opus~100k won 5 of 6, default opus and opus@low 3 of 8. All samples are small.
- **Children:** both are built on f3-lean's 250-word F3 core, so they stay under 400 words and are nested (f3-lean ⊂ attribution ⊂ full). F3 itself is 483 words, so "F3 + one rule" would break the limit.
  - `f3-distilled-prereview-defuse-v1`: f3-lean + R1 only, 278 words.
  - `f3-opus-distilled-v1`: f3-lean + R1–R5, 340 words.
  - Both are linted clean (0 findings) against 169 story-event titles from the digests. This container has no scripted trajectories, so `collect_titles` returns none here.
- **Registration** waits until the F3 family's Haiku N_f reaches 9, after round 1 of batch 1. Then the cap ⌈(1+N_f)^0.5⌉ = 4 allows both beside f3-lean and f3-balance-recombined. Children enqueued now could not run before batch 2 anyway.
- **Flag for the team:** R1's timing is anchored to the published review cadence. See the compliance note at the end of distilled-rules.md: under prereg §10 it may count as diagnostic-only.
- **Cloud digests:** new Opus games played here go to `lab/reports/teacher-digests/opus-cloud/`. `careerlab digest` skips games without a local run folder and rewrites `index.md`, so writing them into `opus/` would drop the 14 Mac games from that index.

| Distilled child | Haiku runs finished | Q per run | pending |
|---|---:|---|---:|
| f3-opus-distilled-v1 | 0 | — | 4 |
| f3-distilled-prereview-defuse-v1 | 0 | — | 4 |

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

## Relevo (hand-off)

_Kept current during the run and rewritten at the end. Last edit: 26 Oct 15:30 UTC._

### 1. What this session did, and why

**Setup (14:12–14:20 UTC)**
- Branch `cloud-lab-run` from `main` ad8c8f9. Ran `uv sync` and the dev dataset update, then `careerlab import`: 249 evaluations, 22 policies, 7 actors, 88 decisions.
- `careerlab recover` found nothing to release. Wrote `quota_cap.json` with `{"max_five_hour": 0.80}`.
- **Claude CLI pinned to 2.1.303** (`npm install --prefix ~/claude-2.1.303 @anthropic-ai/claude-code@2.1.303`, then `CAREERLAB_CLAUDE_EXE`).
  - Prereg §1 freezes the CLI version in every actor record. The container ships 2.1.310, which would have created new actor cells and cut the new runs off from the 99 Mac episodes.
  - Checked: `claude-cli:haiku` → `08e9167a965ed82c`, `claude-cli:opus~100k` → `eaaedd84f8f22e6d`, both the existing ids.
- **Quota seed:** the governor reads quota only from local worker streams, and there were none. A one-line probe stream in `runs/_quota-probe/` makes it hold correctly (five-hour 0.84 at 14:15, reset 16:00).
- **Two reporting fixes, no decision-rule change** (commit f1b1b5d):
  - `decisions.block_decision` recorded `robust: null` because it read attributes that `Robustness` does not have.
  - `analysis.load_cells` dropped every episode whose `result.json` is not on this machine; it now falls back to the evaluation row.

**Merges from `main`:** 7945fe4 (digests), 3db7af9 (seven-day pacing), d66911f (ESTADO.md, `careerlab lint`). Registry exports: kept this side, as asked.

**Scheduler**
- `scratchpad/driver.py`, detached: run the queue, then replacement attempts for interrupted slots, then the recorded Haiku block decision, then a marker file.
- It was restarted three times before any episode started, to load new code (14:47, pacing; 15:13, ceiling lane; 15:16, priorities). Each time `careerlab recover` released the leases; no episode ran twice.
- T13 ceiling lane: `scratchpad/ceiling.py`, `--purpose pilot --slots 2`. Ceiling jobs get priority −100, and the main lane uses `--limit` = queued non-pilot jobs, so it never leases them.

**Policies created**

| Policy | Id | Family | Parents | Hypothesis in one line |
|---|---|---|---|---|
| f8-secure-growth-v1 | 5f8c9648b6abd9b0 | f8-secure-growth (new) | F3, f3-lean (text) | Keep F3's risk and weak-review responses; when no signal is active, push for promotion and pay. That should lift level and wealth without more exits. T3, and the stall slot (playbook P10). |
| f3-opus-distilled-v1 | c03a1bf3ca04c5e7 | f3-feedback-reactive | F3, f3-lean | f3-lean + distilled R1–R5 from 14 Opus games (T2). |
| f3-distilled-prereview-defuse-v1 | f41d6382cab6ec76 | f3-feedback-reactive | F3, f3-lean | f3-lean + R1 only (attribution child, T2). |
| x0-opus-ceiling-v1 | 47cbeec8b03ad2a0 | ceiling | F3 | T13 measurement arm, written in a clean room (no digests) by a subagent, 599 words. Combines F3, the Protect > Risk > Review > Grow precedence, the handbook rules and R1–R3. 4 games on opus@max~100k, pilot lane. |
| o1-promotion-gap-v1 | 006571b3bb85b323 | o1-promotion-gap (new, T4) | none | Promotion is held shut by the stat lagging furthest behind the level. Name that one gap, build it after a review and make output visible before the next one. Outside designer, no access to our Skills. |
| o2-run-hot-v1 | 663c8cd2a1cafe68 | o2-run-hot (new, T4) | none | Health and Dignity are fuel: run Full growth quarters and throttle to Cruise or Cool only on falling stats or warnings. Outside designer. |
| o3-sponsor-lens-v1 | not registered (held) | o3-sponsor-lens (T4) | none | Held: it largely combines F4 and F5, both of which trail; only its role-based reading of events is new. Recorded as a `hold` decision. |

**Decisions recorded by this session**
- `enqueue`: Problem A, 2 × opus~100k each for F3, f3-balance-recombined and f3-lean.
- `enqueue`: 4 Haiku screens each for f8 and the two distilled children.
- `reprioritise`: 4 Mac-queued calibrate replacements (default opus, opus@low) to −10, because of the weekly pace.
- `reprioritise`: the 6 Problem-A opus~100k jobs to −5, behind the Haiku replicates.
- `enqueue`: 4 Haiku screens each for o1 and o2 (T4).
- `hold`: o3-sponsor-lens (overlaps F4 and F5).
- `recover`: several entries.
- Block decisions appear after each batch.

**Progressive widening.** Prereg §6 counts N_f as terminal episodes in the family subtree, all actors. For F3 that is 9 (F3 5, f3-balance-recombined 2, f3-lean 2), so the cap is 4: 2 children existed and both distilled children fit. The report table counts Haiku-only N_f, which is stricter.

### 2. Results so far
See the sections above: latest block decision, actor comparison, Problem A, T13. No cloud episode had finished at the time of this edit.

### 3. Failed or half done
- **0.97 pre-reset cap.** First requested by the strategy session at 15:15, and blocked by this session's permission classifier because the request came from a peer. **The user then asked for it directly at 15:45 UTC.** From 15:46 the cap was 0.97, with 10 workers: 6 main lane, 2 extra lane for the o1 and o2 screens, 2 ceiling games. A detached script restored 0.80 at 16:00:05. Recorded as a `quota_cap` decision.
- 22 interrupted attempts from the Mac stay on record, never scored. Each slot already had a later attempt.

### 4. Next step and how to resume
- The loop scripts are committed in `scripts/cloud-run/` (README there). Copy `next.md`, `teacher.md` and `relevo.md` from the sections of this report into `$CLOUD_RUN_DIR` to keep the status file continuous.
- If this session is gone, start a new cloud session on branch `cloud-lab-run` with the prompt below.
- Leased or running jobs are released by `careerlab recover`. Interrupted ones get replacement attempts from `driver.py`'s requeue rule, or by hand with `Registry.requeue_interrupted`.

```text
Continue the CareerLab race on branch cloud-lab-run (repo aleetreny/huawei). Read lab/reports/cloud-run-status.md (section Relevo) and lab/CLOUD_RUNBOOK.md first. Setup: uv sync; uv run career-emulator-engine update --source distribution --split dev; npm install --prefix ~/claude-2.1.303 @anthropic-ai/claude-code@2.1.303 and export CAREERLAB_CLAUDE_EXE=~/claude-2.1.303/node_modules/.bin/claude (the actor records freeze CLI 2.1.303); uv run careerlab import; uv run careerlab recover; uv run careerlab status; write {"max_five_hour": 0.80} to ~/careerlab-data/huawei/quota_cap.json (never touch weekly_pace). Then start the loop with scripts/cloud-run/driver.py and scripts/cloud-run/ceiling.py (see scripts/cloud-run/README.md; the driver runs uv run careerlab run --kind claude-cli --slots 6 --max-five-hour 0.80 on non-pilot jobs, the ceiling lane runs purpose pilot with --slots 2); after each batch apply careerlab.decisions.block_decision for the Haiku actor 08e9167a965ed82c with record=True; generate children only within progressive widening and the stall rule; lint (careerlab lint), register, enqueue 4 Haiku screens; every hour careerlab export, update lab/reports/cloud-run-status.md, commit lab/registry, lab/reports, new lab/policies-src and push to cloud-lab-run. Never push to main, never submit, never use a competition key, never edit ESTADO.md or the prereg.
```

### 5. Suggested ESTADO.md updates (for the organiser)
- **T1:** running in the cloud; batch 1 starts at the 16:00 UTC reset.
- **T2:** distilled-rules.md done; two F3 children registered and queued.
- **T3:** f8-secure-growth-v1 registered and queued.
- **T13:** README with pre-stated thresholds committed (a494d44) before registration. x0-opus-ceiling-v1 (47cbeec8b03ad2a0) registered; 4 games queued in their own 2-slot lane.
- **T4:** o1-promotion-gap and o2-run-hot registered and queued (4 Haiku each). o3-sponsor-lens held because it overlaps F4 and F5. o1's timing is cadence-relative, like R1, so the same compliance question applies.
- **T10:** done (`lab/reports/energy-bots/README.md`), 400 bot episodes, no quota. Health is the first constraint when stories ignore it: every mix without a Health point per quarter blacked out. Recovering only once Health is low is too late. Defuse + Health was the best mix. No mix fixes the first review. Surviving bots end at the same level and wealth as the LLM players.
- **T8:** not before 27 Oct; drafts start about 05:00 UTC.
- **Decision for the team:** whether R1's cadence-relative timing counts as a calendar trigger under prereg §10 (note at the end of distilled-rules.md).
