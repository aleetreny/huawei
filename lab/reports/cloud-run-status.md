# CareerLab cloud run — status

Generated 26 Oct 16:57 UTC in the Claude Code cloud container, branch `cloud-lab-run`. All scores are Claude-proxy results on the dev split (`real-dev`), not official scores and not the target actor (deepseek-v4-flash in JiuwenSwarm). Under prereg-v1 section 8 they cannot prune or select by themselves.

## At a glance

- Jobs in the registry: done 303, interrupted 28, queued 37, running 3.
- Episodes finished in this container: 53. Batches completed: 1 (last at 2026-10-26 16:49:32 UTC).
- Five-hour quota (`careerlab.scheduler.latest_quota`): utilisation **0.26**, window resets 26 Oct 21:00 UTC; governor cap 0.8. The window is shared with every session on the account.
- Seven-day quota: utilisation **0.03**, window resets 02 Nov 16:00 UTC; weekly allowance now **0.105** (`weekly_allowance`: straight line from 0.10 at the window start to 0.90 at 2 Nov 00:00 UTC, about 0.126 a day). New episodes wait while either window is over its limit.
- Claude CLI pinned to 2.1.303 (the version frozen in the registry's actor records; the container ships 2.1.310), so new runs land in the existing Haiku (`08e9167a965ed82c`) and opus~100k (`eaaedd84f8f22e6d`) cells.
- **T13 Opus ceiling** (`claude-cli:opus@max~100k`, 2-slot lane, see `lab/reports/opus-ceiling/README.md`): jobs done 3, queued 2, running 1; finished games: Q 24.5/T 24, Q 53.6/T 48, Q 62.0/T 48.

## Latest pre-registered block decision (Haiku actor)

Registry decision #114, recorded 26 Oct 16:49 UTC (`careerlab.decisions.block_decision`, record=True).

Actor `08e9167a965ed82c` — robustness across noise models: True (robust: fits differ only inside the hysteresis band: 3207e8f585cbe240 dormant only in some fits, others inside the band (normal 0.089, student_t 0.104) | 663c8cd2a1cafe68 dormant only in some fits, others inside the band (normal 0.060, student_t 0.061) | cbc7402d11222ac7 dormant only in some fits, others inside the band (normal 0.090, student_t 0.140) | dd82cc1584e7370d dormant only in some fits, others inside the band (normal 0.093, student_t 0.097) | ed78f44ccd41adf8 dormant only in some fits, others inside the band (normal 0.053, student_t 0.068) | leader near-tie, not separated by any fit: normal=e373478ad46b58f6, student_t=e373478ad46b58f6, bayes_boot=954bf3788461f2d8; normal: P(e373478ad46b58f6 > 954bf3788461f2d8) = 0.739, student_t: P(e373478ad46b58f6 > 954bf3788461f2d8) = 0.635, bayes_boot: P(954bf3788461f2d8 > e373478ad46b58f6) = 0.569)

| Policy | runs in prefix | pending | posterior Y (sd) | P(best) | action | reason |
|---|---:|---:|---|---:|---|---|
| f7-three-skills-v1 | 5 | 0 | 55.21 (5.42) | 0.313 | **PROMOTE** | PROMOTE: top-2 posterior mean 55.2 with P(best) = 0.313 >= 0.2 |
| f3-balance-recombined-v1 | 4 | 0 | 50.9 (4.01) | 0.054 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.054, P(mu >= mu_L - 4) = 0.482, n=4) |
| f3-lean-v1 | 4 | 0 | 50.16 (4.01) | 0.039 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.039, P(mu >= mu_L - 4) = 0.438, n=4) |
| f3-distilled-prereview-defuse-v1 | 4 | 0 | 49.37 (4.01) | 0.027 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.027, P(mu >= mu_L - 4) = 0.393, n=4) |
| f1-steady-balance-v1 | 4 | 0 | 49.28 (7.08) | 0.102 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.102, P(mu >= mu_L - 4) = 0.414, n=4) |
| f3-feedback-reactive-v1 | 5 | 0 | 48.87 (3.89) | 0.019 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.019, P(mu >= mu_L - 4) = 0.363, n=5) |
| f8-secure-growth-v1 | 4 | 0 | 48.7 (8.78) | 0.133 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.133, P(mu >= mu_L - 4) = 0.404, n=4) |
| f1-review-risk-v1 | 3 | 0 | 48.65 (7.24) | 0.092 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f3-opus-distilled-v1 | 4 | 0 | 47.47 (4.01) | 0.01 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.010, P(mu >= mu_L - 4) = 0.290, n=4) |
| f2-convert-on-review-v1 | 3 | 0 | 47.24 (7.56) | 0.071 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f7-single-skill-v1 | 5 | 0 | 46.3 (5.42) | 0.019 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.019, P(mu >= mu_L - 4) = 0.261, n=5) |
| o1-promotion-gap-v1 | 4 | 0 | 42.67 (11.24) | 0.077 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.077, P(mu >= mu_L - 4) = 0.247, n=4) |
| p0-review-guard-v1 | 3 | 0 | 40.18 (5.27) | 0.001 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f4-review-first-v1 | 3 | 0 | 39.87 (7.59) | 0.009 | **REPEAT** | REPEAT: n=3 < n0=4 |
| p0-minimal-v1 | 5 | 0 | 39.42 (4.89) | 0.0 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.000, P(mu >= mu_L - 4) = 0.053, n=5) |
| f4-visible-delivery-v1 | 5 | 0 | 39.02 (7.31) | 0.005 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.005, P(mu >= mu_L - 4) = 0.090, n=5) |
| f6-commitment-ledger-v1 | 5 | 0 | 38.47 (7.96) | 0.007 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.007, P(mu >= mu_L - 4) = 0.093, n=5) |
| m3-subtracted-v1 | 3 | 0 | 38.42 (8.32) | 0.009 | **REPEAT** | REPEAT: n=3 < n0=4 |
| m3-sustainable-career-v0-1 | 4 | 0 | 38.01 (8.18) | 0.007 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.007, P(mu >= mu_L - 4) = 0.089, n=4) |
| o2-run-hot-v1 | 4 | 0 | 35.24 (8.69) | 0.004 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.004, P(mu >= mu_L - 4) = 0.060, n=4) |
| f5-relationship-capital-v1 | 5 | 0 | 29.43 (3.89) | 0.0 | **DORMANT** | DORMANT: n=5 >= n0=4 and P(mu >= mu_L - 4) = 0.001 < 0.05 (mean 29.4 vs leader e373478ad46b58f6 55.2) |
| f2-invest-early-v1 | 5 | 0 | 24.58 (5.97) | 0.0 | **DORMANT** | DORMANT: n=5 >= n0=4 and P(mu >= mu_L - 4) = 0.000 < 0.05 (mean 24.6 vs leader e373478ad46b58f6 55.2) |

Leader history (stall trigger: leader posterior mean not improved by 2 Y-points over 3 decisions):

| Decision | Time | Leader | Posterior Y |
|---:|---|---|---:|
| #78 | 26 Oct 13:26 UTC | f3-feedback-reactive-v1 | 61.34 |
| #83 | 26 Oct 13:39 UTC | f3-feedback-reactive-v1 | 61.34 |
| #88 | 26 Oct 14:07 UTC | f3-feedback-reactive-v1 | 60.21 |
| #114 | 26 Oct 16:49 UTC | f7-three-skills-v1 | 55.21 |

Gain over the last three decisions: -6.13 → stall trigger **fires**.

## Progressive widening (Haiku cell)

| Family | terminal Haiku episodes N_f | cap ⌈(1+N_f)^0.5⌉ | children so far |
|---|---:|---:|---:|
| f3-feedback-reactive | 21 | 5 | 4 |
| f7-one-vs-many | 10 | 4 | 0 |
| p0-minimal | 8 | 3 | 1 |
| f4-visible-delivery | 8 | 3 | 1 |
| f2-invest-early | 8 | 3 | 1 |
| m3-teammate | 7 | 3 | 1 |
| f1-steady-balance | 7 | 3 | 1 |
| f6-commitment-ledger | 5 | 3 | 0 |
| f5-relationship-capital | 5 | 3 | 0 |
| o2-run-hot | 4 | 3 | 0 |
| o1-promotion-gap | 4 | 3 | 0 |
| f8-secure-growth | 4 | 3 | 1 |
| matteo-value-conversion | 2 | 2 | 0 |

## Children created in this cloud run

### f8-secure-growth-v1 (`5f8c9648b6abd9b0`, family f8-secure-growth)

- Parents: f3-feedback-reactive-v1, f3-lean-v1; operator: new family seeded from the F3 core (cross-branch hypothesis under the stagnation rule); idea origin: playbook:P10 (less defensive family that keeps its response to warnings), chosen because the stall trigger fires and because of the score-gap finding in findings.md (strategy-session request, 26 Oct ~14:45 UTC).
- Hypothesis: Completed games already survive; the score they leave on the table is mostly career level and wealth (findings.md, 48 completed games, all actors), and every family so far optimises survival. F3's Clear state spends quiet quarters lifting the weakest statistic, which keeps the agent safe but does not compete for promotion. A policy that keeps F3's risk response (Secure) and weak-review plan (Repair) with higher precedence, and otherwise plays for promotion and pay (Grow: Apply for a key project, High-intensity work plus Prepare report materials while Health is comfortable, story options that raise Output, Skill, Wealth or standing at a bounded cost), will earn more A or S reviews, hence more promotions and salary, and end with higher level and wealth dimensions than F3 and f3-lean without more eliminations.
- Haiku runs so far: Q 55.8/T 48, Q 68.6/T 48, Q 23.5/T 24, Q 51.9/T 48.

### f3-opus-distilled-v1 (`c03a1bf3ca04c5e7`, family f3-feedback-reactive)

- Parents: f3-feedback-reactive-v1, f3-lean-v1; operator: distil (teacher); idea origin: user request 26 Oct: Opus teacher distillation (lab/reports/teacher-digests/distilled-rules.md).
- Hypothesis: Opus winners differed from Opus losers less in how they answered warnings (Defuse in the first phase after HR said risks had piled up or worse: 14 of 18 phases vs 11 of 15) than in where routine effort went: Prepare report materials in at least 3 of 4 quarters (8 of 8 winners, 2 of 6 losers); no chasing of the numerically smallest statistic (Network maintenance or Build a mentorship in two-thirds or more of quarters: 0 of 8 vs 3 of 6, exactly the three capability-dismissed games); Apply for a key project kept in both quarters after the first C (7 of 8 vs 1 of 6); Defuse in the last Energy phase before a review that follows a weak one (D 0 of 7 vs 7 of 22); and a blow-up handled as Escalating (both visible trust crises came 1 to 2 months after a blow-up followed by a formal escalation). f3-lean says the opposite on two points (lift the weakest statistic; switch the main action by factor after a C or D). Merging all five rules into f3-lean raises review grades after the opening C and so mean quantitative_score above f3-lean, F3 and f3-distilled-prereview-defuse-v1 in a 4-run Haiku screen, with completion no lower.
- Haiku runs so far: Q 27.8/T 24, Q 19.8/T 24, Q 47.4/T 48, Q 58.5/T 48.

### f3-distilled-prereview-defuse-v1 (`f41d6382cab6ec76`, family f3-feedback-reactive)

- Parents: f3-feedback-reactive-v1, f3-lean-v1; operator: distil (teacher, single-rule attribution); idea origin: user request 26 Oct: Opus teacher distillation (lab/reports/teacher-digests/distilled-rules.md).
- Hypothesis: Every Opus game opened with a C, and the most common Opus exit (3 of 6 losses, plus the eliminated Sonnet F3 run) is C, C, D, D. The D after a weak review followed risk that rebuilt once the agent stopped defusing: of 29 reviews that followed a C or D, none of the 7 preceded by Defuse legacy risk in the last Energy phase before the review was a D, against 7 of the 22 without it. In the decisive case (a third review after C, C) the split is 4 of 4 defused and no D versus 4 of 4 not defused and D, within every seed group and within P0 and M3. Adding one line to f3-lean that sets Defuse legacy risk and Prepare report materials in the second Energy phase after any C or D, whatever the signal state, removes that route for Haiku: no D after a weak review in a 4-run screen and mean quantitative_score at least f3-lean's and F3's.
- Haiku runs so far: Q 32.0/T 24, Q 61.8/T 48, Q 59.1/T 48, Q 56.7/T 48.

### x0-opus-ceiling-v1 (`47cbeec8b03ad2a0`, family ceiling)

- Parents: f3-feedback-reactive-v1; operator: synthesis of general knowledge (measurement arm, not a submission candidate); idea origin: T13 user request 26 Oct: Opus ceiling measurement with all general knowledge.
- Hypothesis: The current leader (F3 feedback-reactive, posterior Y about 60 with Haiku) is limited by two things: the player's reasoning and the policy's coverage (every family so far optimises survival only, and completed careers lose most of their missing ground on career level and wealth). Giving the strongest reasoner (Claude Opus at maximum effort) all our general knowledge in one Skill, namely F3's signal states and responses, f3-balance-recombined's strict precedence, an F8-style growth mode, the decision-relevant published handbook rules and the general form of distilled rules R1-R5, measures how far above the leader the game's ceiling lies when only legally usable, general knowledge is supplied. Expected: completion close to Opus's best observed rate and a mean quantitative_score clearly above F3's, with most of the gain on level and wealth.
- Haiku runs so far: no finished runs yet.

### o1-promotion-gap-v1 (`006571b3bb85b323`, family o1-promotion-gap)

- Parents: ; operator: new family (outside designer); idea origin: T4 outside ideas: agent without access to the team's Skills; sources: handbook, public rules, score structure.
- Hypothesis: Promotion is a multi-stat gate set by the weakest of Skill, Network and Output relative to level; diagnosing that binding gap from feedback, building it in the round after a review and harvesting visible Output in the round before the next one produces more promotions, hence higher final level and wealth, than balanced allocation, while recovering only on low or falling stats keeps survival intact.
- Haiku runs so far: Q 64.4/T 48, Q 15.7/T 24, Q 31.0/T 20, Q 64.7/T 48.

### o2-run-hot-v1 (`663c8cd2a1cafe68`, family o2-run-hot)

- Parents: ; operator: new family (outside designer); idea origin: T4 outside ideas: agent without access to the team's Skills; sources: handbook, public rules, score structure.
- Hypothesis: Survivors fall short on level and wealth because they hold Health and Dignity near full; treating them as fuel and switching between Full, Cruise and Cool modes on observed state and warnings converts the unused resilience margin into more Output and Skill, earlier promotions and more cash taken from events, without raising the early-elimination rate.
- Haiku runs so far: Q 24.7/T 24, Q 38.6/T 29, Q 61.9/T 48, Q 19.7/T 24.

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
| f3-opus-distilled-v1 | 4 | 27.8, 19.8, 47.4, 58.5 | 0 |
| f3-distilled-prereview-defuse-v1 | 4 | 32.0, 61.8, 59.1, 56.7 | 0 |

## Problem A check: Haiku vs opus~100k on shared policies

opus~100k decision computed with the same rule but **not recorded** (only the Haiku decision is the block decision).

| Policy | Haiku posterior Y (n) | opus~100k posterior Y (n) | opus~100k pending |
|---|---|---|---:|
| f1-steady-balance-v1 | 49.28 (4) | 65.56 (2) | 0 |
| p0-minimal-v1 | 39.42 (5) | 61.58 (2) | 0 |
| f3-feedback-reactive-v1 | 48.87 (5) | 39.05 (2) | 0 |
| f3-lean-v1 | 50.16 (4) | 39.04 (2) | 0 |
| m3-sustainable-career-v0-1 | 38.01 (4) | 38.99 (2) | 0 |
| f3-balance-recombined-v1 | 50.9 (4) | 38.24 (2) | 0 |

Shared policies with opus~100k data: 6. Spearman of posterior means -0.26; top policy Haiku `f3-balance-recombined-v1`, opus~100k `f1-steady-balance-v1` (disagree). Descriptive only: with this few shared policies and 2–4 runs per cell, agreement cannot certify transfer (pruning authority needs ≥ 8 shared policies spanning ≥ 16 Y-points).

## Actor comparison (all Claude-proxy episodes, `careerlab.analysis`)

Imported episodes from the Mac have no local `result.json`; their rows come from the registry evaluation (early-exit causes are blank for them).

| Actor | eps | interrupted | completion | mean Q (sd) | mean Y | mean months | rejected/ep | min/ep | min/month | cache-read M/month | list-USD/ep |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| haiku | 93 | 0 | 0.52 | 44.1 (18.0) | 42.8 | 37.5 | 0.01 | 9.4 | 0.25 | 0.518 | 0.75 |
| haiku@low | 6 | 0 | 0.33 | 39.2 (16.2) | 38.0 | 33.7 | 0 | 7.0 | 0.21 | 0.302 | 0.36 |
| opus | 6 | 0 | 0.33 | 37.3 (17.0) | 36.5 | 34.8 | 0 | 8.1 | 0.23 | 0.257 | 3.4 |
| opus@low | 6 | 0 | 0.33 | 42.5 (13.8) | 40.6 | 33.5 | 0 | 6.4 | 0.19 | 0.215 | 2.85 |
| opus~100k | 12 | 0 | 0.58 | 49.0 (19.9) | 47.1 | 36.6 | 0 | 10.2 | 0.28 | 0.119 | 2.71 |
| sonnet | 26 | 0 | 0.38 | 39.4 (20.0) | 38.4 | 35 | 0.04 | 8.2 | 0.23 | 0.258 | 1.66 |

| Actor | Policy | n | Q per episode | months | mean Y | early-exit causes |
|---|---|---:|---|---|---:|---|
| haiku | f1-review-risk-v1 | 3 | [51.8, 24.0, 61.0] | [48, 24, 48] | 44.8 |  |
| haiku | f1-steady-balance-v1 | 4 | [51.0, 66.6, 27.7, 71.8] | [48, 48, 24, 48] | 52.2 |  |
| haiku | f2-convert-on-review-v1 | 3 | [61.2, 30.0, 63.6] | [48, 24, 48] | 49.6 |  |
| haiku | f2-invest-early-v1 | 5 | [47.1, 18.3, 18.6, 15.0, 14.4] | [47, 18, 24, 19, 24] | 23.2 | ; ; ; Trust crisis — a second major blow-up. T; Dismissed for capability — a second weak |
| haiku | f3-balance-recombined-v1 | 4 | [63.0, 59.2, 65.7, 54.6] | [48, 48, 48, 48] | 58.5 |  |
| haiku | f3-distilled-prereview-defuse-v1 | 4 | [61.8, 32.0, 59.1, 56.7] | [48, 24, 48, 48] | 50.7 | Dismissed for capability — a second weak |
| haiku | f3-feedback-reactive-v1 | 5 | [59.7, 66.3, 66.6, 28.7, 22.4] | [48, 48, 48, 24, 24] | 47.0 | Dismissed for capability — a second weak; Dismissed for capability — a second weak |
| haiku | f3-lean-v1 | 4 | [50.1, 64.3, 46.7, 59.5] | [48, 48, 48, 48] | 54.1 |  |
| haiku | f3-opus-distilled-v1 | 4 | [27.8, 19.8, 47.4, 58.5] | [24, 24, 48, 48] | 38.2 | Dismissed for capability — a second weak; Dismissed for capability — a second weak |
| haiku | f4-review-first-v1 | 3 | [19.7, 60.3, 62.5] | [24, 48, 48] | 46.3 |  |
| haiku | f4-visible-delivery-v1 | 5 | [55.9, 59.1, 17.6, 18.8, 24.4] | [48, 48, 24, 17, 31] | 35.1 | ; Broke — months with an empty wallet. Som; Trust crisis — a second major blow-up. T |
| haiku | f5-relationship-capital-v1 | 5 | [21.8, 48.5, 23.1, 32.5, 26.9] | [24, 39, 24, 29, 24] | 29.4 | ; ; ; Trust crisis — a second major blow-up. T; Trust crisis — a second major blow-up. T |
| haiku | f6-commitment-ledger-v1 | 5 | [30.5, 25.8, 49.7, 23.0, 67.8] | [30, 8, 48, 24, 48] | 38.5 | ; ; Dismissed for capability — a second weak |
| haiku | f7-single-skill-v1 | 5 | [54.2, 63.9, 20.6, 60.1, 30.9] | [48, 48, 24, 48, 30] | 44.7 | ; Trust crisis — a second major blow-up. T |
| haiku | f7-three-skills-v1 | 5 | [50.4, 51.5, 67.1, 71.0, 58.5] | [48, 48, 48, 48, 48] | 57.8 |  |
| haiku | f8-secure-growth-v1 | 4 | [68.6, 55.8, 23.5, 51.9] | [48, 48, 24, 48] | 48.7 | Dismissed for capability — a second weak |
| haiku | m3-subtracted-v1 | 3 | [16.0, 60.6, 48.9] | [24, 48, 48] | 41.8 |  |
| haiku | m3-sustainable-career-v0-1 | 4 | [17.2, 70.2, 27.8, 30.9] | [24, 48, 24, 26] | 35.5 | ; ;  |
| haiku | o1-promotion-gap-v1 | 4 | [64.4, 15.7, 31.0, 64.7] | [48, 24, 20, 48] | 42.7 | Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T |
| haiku | o2-run-hot-v1 | 4 | [24.7, 38.6, 61.9, 19.7] | [24, 29, 48, 24] | 35.2 | Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T; Dismissed for capability — a second weak |
| haiku | p0-minimal-v1 | 5 | [53.9, 57.4, 31.6, 32.0, 18.5] | [48, 48, 22, 23, 24] | 37.9 | ; ;  |
| haiku | p0-review-guard-v1 | 3 | [41.9, 54.2, 45.1] | [33, 42, 47] | 42.6 | ; ;  |
| haiku | value-conversion-v1 | 2 | [37.1, 46.2] | [31, 40] | 38.3 | Trust crisis — a second major blow-up. T; Trust crisis — a second major blow-up. T |
| haiku@low | f1-steady-balance-v1 | 2 | [55.2, 62.1] | [48, 48] | 56.9 |  |
| haiku@low | m3-sustainable-career-v0-1 | 2 | [29.4, 21.5] | [23, 24] | 25.3 | ;  |
| haiku@low | p0-minimal-v1 | 2 | [28.4, 38.5] | [24, 35] | 31.7 | ;  |
| opus | f1-steady-balance-v1 | 2 | [56.2, 53.4] | [48, 48] | 53.8 |  |
| opus | m3-sustainable-career-v0-1 | 2 | [21.4, 48.2] | [24, 47] | 32.8 | ; Trust crisis — a second major blow-up. T |
| opus | p0-minimal-v1 | 2 | [24.2, 20.2] | [24, 18] | 22.8 | ; Trust crisis — a second major blow-up. T |
| opus@low | f1-steady-balance-v1 | 2 | [40.2, 30.2] | [24, 26] | 33.2 | ;  |
| opus@low | m3-sustainable-career-v0-1 | 2 | [51.8, 28.9] | [48, 20] | 39.8 |  |
| opus@low | p0-minimal-v1 | 2 | [65.0, 38.8] | [48, 35] | 49.0 | Trust crisis — a second major blow-up. T |
| opus~100k | f1-steady-balance-v1 | 2 | [69.8, 69.2] | [48, 48] | 65.6 |  |
| opus~100k | f3-balance-recombined-v1 | 2 | [25.8, 31.8] | [8, 24] | 28.0 | Broke — months with an empty wallet. Som; Dismissed for capability — a second weak |
| opus~100k | f3-feedback-reactive-v1 | 2 | [24.2, 67.8] | [24, 48] | 44.3 | Dismissed for capability — a second weak |
| opus~100k | f3-lean-v1 | 2 | [55.7, 35.6] | [48, 23] | 44.0 | Trust crisis — a second major blow-up. T |
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
| haiku | opus | 3 | True | 0.5 |
| haiku | opus@low | 3 | False | -0.5 |
| haiku | opus~100k | 6 | False | -0.26 |
| haiku | sonnet | 10 | False | 0.5 |
| haiku@low | opus | 3 | True | 0.5 |
| haiku@low | opus@low | 3 | False | -0.5 |
| haiku@low | opus~100k | 3 | True | 1.0 |
| haiku@low | sonnet | 3 | True | 0.5 |
| opus | opus@low | 3 | False | -1.0 |
| opus | opus~100k | 3 | True | 0.5 |
| opus | sonnet | 3 | True | 1.0 |
| opus@low | opus~100k | 3 | False | -0.5 |
| opus@low | sonnet | 3 | False | -1.0 |
| opus~100k | sonnet | 4 | True | 0.4 |

## What is next

- **Batch 1 done (16:49 UTC, 93.6 min).** It covered the pre-reset push (10 workers from 15:46) and the queue after the reset. The block decision is recorded above (registry #114).
  - New leader: **f7-three-skills-v1**, 55.2, labelled PROMOTE. The fits do not separate it from f3-balance-recombined (50.9).
  - f5-relationship-capital and f2-invest-early go DORMANT. P0 and M3 come back to REPEAT, because the lower leader puts them inside the band.
- **Stall rule fires:** the leader's posterior mean fell from 61.3 to 55.2 over three decisions. This block's contrarian or cross-branch slot is being written now and will cite a playbook card.
- **Dismissal pattern** (38 local games): every month-24 dismissal followed four weak reviews in a row (C C D D ×10, C C C C ×2, C C D C ×2). Every game with a B among its first four reviews got past month 24. Breaking the C streak early is the lever.
- **Batch 2** (running): Matteo's value-conversion-v1, 4 Haiku screens.
- **Block 3, allocated by prereg §6:** 24 repeat slots by top-two Thompson sampling, seed 20261140, recorded as an `allocate` decision.
  - Counts: F7 three-skills 5, F1 4, f8 3, f3-balance-recombined 3, f2-convert-on-review 3, f1-review-risk 2, and 1 each for o1, f7-single-skill, f3-lean and F6.
  - No dormant audit was drawn.
  - New candidates (≥ 20 %): 2 trace-driven children of F7 (cap 4 at N_f = 14) and the stall slot, 4 Haiku screens each, as soon as they lint clean.
- **T13 ceiling:** 3 of 4 games done (Q 24.5 dismissed at month 24, 53.6 completed, 62.0 completed). They mix completions and eliminations, so the pre-stated rule adds 2 games (6 in total, queued).
- **Problem A:** opus~100k does badly with the F3 family so far: one game went broke, three were dismissed or hit a trust crisis, and the best is 67.8. Earlier it reached 61–66 with F1 and P0. Haiku and Opus-compact rank these families differently. The report follows when the 6 runs finish.
- **Organiser round 2 (16:55 UTC):** merged `alejandro/explicacion-repo`, `matteo-t4-growth` (observed-growth-v1) and `leah/workspace` (l1-review-clock-v1, results panel).
  - Registered both new manuals with 4 Haiku screens each: Leah's `f1830961d168beb9` and Matteo's `f03981dac92f8b6c`.
  - Imported Leah's origin `leah` (10 jobs, 0 conflicts). Her runs used CLI 2.1.295, so they form their own actor cell and stay outside the race decisions.
  - The driver now filters on `origin=''` and waits for any running main-lane scheduler before starting a batch.

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
- **Authorship (user rule, 26 Oct 15:55 UTC):** every commit is made as Alejandro Treny Ortega <alejandrotreny100@gmail.com>, with no Claude co-author lines. The 14 earlier commits of this branch were rewritten to that identity and force-pushed with lease; the content is identical. `main` still holds 2 commits authored by Claude and 23 `Co-Authored-By` lines from earlier sessions. Rewriting those would need a force-push to `main`, which has not been done.
- **0.97 pre-reset cap.** First requested by the strategy session at 15:15, and blocked by this session's permission classifier because the request came from a peer. **The user then asked for it directly at 15:45 UTC.** From 15:46 the cap was 0.97, with 10 workers: 6 main lane, 2 extra lane for the o1 and o2 screens, 2 ceiling games. A detached script restored 0.80 at 16:00:05. Recorded as a `quota_cap` decision.
- 22 interrupted attempts from the Mac stay on record, never scored. Each slot already had a later attempt.

### 4. Next step and how to resume
- The loop scripts are committed in `scripts/cloud-run/` (README there). Copy `next.md`, `teacher.md` and `relevo.md` from the sections of this report into `$CLOUD_RUN_DIR` to keep the status file continuous.
- If this session is gone, start a new cloud session on branch `cloud-lab-run` with the prompt below.
- Leased or running jobs are released by `careerlab recover`. Interrupted ones get replacement attempts from `driver.py`'s requeue rule, or by hand with `Registry.requeue_interrupted`.

```text
Continue the CareerLab race on branch cloud-lab-run (repo aleetreny/huawei). Read lab/reports/cloud-run-status.md (section Relevo) and lab/CLOUD_RUNBOOK.md first. Setup: uv sync; uv run career-emulator-engine update --source distribution --split dev; npm install --prefix ~/claude-2.1.303 @anthropic-ai/claude-code@2.1.303 and export CAREERLAB_CLAUDE_EXE=~/claude-2.1.303/node_modules/.bin/claude (the actor records freeze CLI 2.1.303); uv run careerlab import; uv run careerlab recover; uv run careerlab status; write {"max_five_hour": 0.80} to ~/careerlab-data/huawei/quota_cap.json (never touch weekly_pace). Then start the loop with scripts/cloud-run/driver.py and scripts/cloud-run/ceiling.py (see scripts/cloud-run/README.md; the driver runs uv run careerlab run --kind claude-cli --slots 6 --max-five-hour 0.80 on non-pilot jobs, the ceiling lane runs purpose pilot with --slots 2); after each batch apply careerlab.decisions.block_decision for the Haiku actor 08e9167a965ed82c with record=True; generate children only within progressive widening and the stall rule; lint (careerlab lint), register, enqueue 4 Haiku screens; every hour careerlab export, update lab/reports/cloud-run-status.md, commit lab/registry, lab/reports, new lab/policies-src and push to cloud-lab-run. You are also the ORGANISER: every hour and after each batch, git fetch origin --prune; review finished collaborator branches (<persona>/<tarea>), merge them and origin/main into cloud-lab-run (keep their owners' lines in ESTADO.md; keep this side for lab/registry/*.jsonl), run uv run pytest -q, push cloud-lab-run, then push cloud-lab-run:main as a fast-forward (never force main); keep ESTADO.md (Spanish: section 2 results, the task table lines of the cloud and of merged branches, Relevo del organizador), findings.md, progress.md and task_plan.md in step. Push to main is authorised by the user (26 Oct 16:15 UTC); never submit, never use a competition key, never edit the prereg. Commit as the user: git config user.name "Alejandro Treny Ortega" and user.email alejandrotreny100@gmail.com, with no Co-Authored-By or Claude-Session lines (user rule, 26 Oct).
```

### 5. ESTADO.md
This session is the organiser and updates ESTADO.md on `main` itself (first at 16:20 UTC). The items below record the state at that time.
- **T1:** running in the cloud; batch 1 starts at the 16:00 UTC reset.
- **T2:** distilled-rules.md done; two F3 children registered and queued.
- **T3:** f8-secure-growth-v1 registered and queued.
- **T13:** README with pre-stated thresholds committed (a494d44) before registration. x0-opus-ceiling-v1 (47cbeec8b03ad2a0) registered; 4 games queued in their own 2-slot lane.
- **T4:** o1-promotion-gap and o2-run-hot registered and queued (4 Haiku each). o3-sponsor-lens held because it overlaps F4 and F5. o1's timing is cadence-relative, like R1, so the same compliance question applies.
- **T10:** done (`lab/reports/energy-bots/README.md`), 400 bot episodes, no quota. Health is the first constraint when stories ignore it: every mix without a Health point per quarter blacked out. Recovering only once Health is low is too late. Defuse + Health was the best mix. No mix fixes the first review. Surviving bots end at the same level and wealth as the LLM players.
- **T8:** not before 27 Oct; drafts start about 05:00 UTC.
- **Decision for the team:** whether R1's cadence-relative timing counts as a calendar trigger under prereg §10 (note at the end of distilled-rules.md).
