# CareerLab cloud run — status

Generated 26 Oct 19:04 UTC in the Claude Code cloud container, branch `cloud-lab-run`. All scores are Claude-proxy results on the dev split (`real-dev`), not official scores and not the target actor (deepseek-v4-flash in JiuwenSwarm). Under prereg-v1 section 8 they cannot prune or select by themselves.

## At a glance

- Jobs in the registry: done 404, interrupted 28, leased 10, queued 21, running 6.
- Episodes finished in this container: 140. Batches completed: 4 (last at 2026-10-26 19:03:01 UTC).
- Five-hour quota (`careerlab.scheduler.latest_quota`): utilisation **0.53**, window resets 26 Oct 21:00 UTC; governor cap 0.8. The window is shared with every session on the account.
- Seven-day quota: utilisation **0.07**, window resets 02 Nov 16:00 UTC; weekly allowance now **0.116** (`weekly_allowance`: straight line from 0.10 at the window start to 0.90 at 2 Nov 00:00 UTC, about 0.126 a day). New episodes wait while either window is over its limit.
- Claude CLI pinned to 2.1.303 (the version frozen in the registry's actor records; the container ships 2.1.310), so new runs land in the existing Haiku (`08e9167a965ed82c`) and opus~100k (`eaaedd84f8f22e6d`) cells.
- **T13 Opus ceiling** (`claude-cli:opus@max~100k`, 2-slot lane, see `lab/reports/opus-ceiling/README.md`): jobs done 6; finished games: Q 24.5/T 24, Q 53.6/T 48, Q 62.0/T 48, Q 69.2/T 48, Q 59.1/T 48, Q 69.0/T 48.

## Latest pre-registered block decision (Haiku actor)

Registry decision #150, recorded 26 Oct 19:03 UTC (`careerlab.decisions.block_decision`, record=True).

Actor `08e9167a965ed82c` — robustness across noise models: True (robust: fits differ only inside the hysteresis band: 663c8cd2a1cafe68 dormant only in some fits, others inside the band (normal 0.086, bayes_boot 0.053) | ed78f44ccd41adf8 dormant only in some fits, others inside the band (normal 0.104) | f03981dac92f8b6c dormant only in some fits, others inside the band (normal 0.085) | f2715987f0341ab2 dormant only in some fits, others inside the band (normal 0.073) | leader near-tie, not separated by any fit: normal=19618e7795be8da1, student_t=19618e7795be8da1, bayes_boot=cc098e54e25efc64; normal: P(19618e7795be8da1 > cc098e54e25efc64) = 0.581, student_t: P(19618e7795be8da1 > cc098e54e25efc64) = 0.705, bayes_boot: P(cc098e54e25efc64 > 19618e7795be8da1) = 0.619)

| Policy | runs in prefix | pending | posterior Y (sd) | P(best) | action | reason |
|---|---:|---:|---|---:|---|---|
| f1-steady-balance-v1 | 12 | 0 | 52.19 (3.73) | 0.174 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.174, P(mu >= mu_L - 4) = 1.000, n=12) |
| f3-balance-recombined-v1 | 7 | 0 | 51.19 (3.51) | 0.103 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.103, P(mu >= mu_L - 4) = 0.722, n=7) |
| f3-lean-v1 | 5 | 0 | 51.11 (3.7) | 0.109 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.109, P(mu >= mu_L - 4) = 0.711, n=5) |
| f1-review-risk-v1 | 7 | 0 | 50.42 (4.17) | 0.1 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.100, P(mu >= mu_L - 4) = 0.655, n=7) |
| f3-feedback-reactive-v1 | 6 | 0 | 50.1 (3.6) | 0.064 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.064, P(mu >= mu_L - 4) = 0.644, n=6) |
| f3-distilled-prereview-defuse-v1 | 4 | 0 | 50.04 (3.8) | 0.07 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.070, P(mu >= mu_L - 4) = 0.637, n=4) |
| f2-convert-on-review-v1 | 7 | 0 | 48.44 (5.65) | 0.092 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.092, P(mu >= mu_L - 4) = 0.515, n=7) |
| f3-opus-distilled-v1 | 4 | 0 | 48.32 (3.8) | 0.029 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.029, P(mu >= mu_L - 4) = 0.510, n=4) |
| f7-three-skills-v1 | 16 | 0 | 45.07 (3.57) | 0.003 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.003, P(mu >= mu_L - 4) = 0.273, n=16) |
| o1-promotion-gap-v1 | 7 | 0 | 44.63 (7.59) | 0.065 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.065, P(mu >= mu_L - 4) = 0.337, n=7) |
| f7-delivery-stories-v1 | 4 | 0 | 43.98 (4.32) | 0.004 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.004, P(mu >= mu_L - 4) = 0.231, n=4) |
| f7-promotion-drive-v1 | 4 | 0 | 43.98 (4.32) | 0.004 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.004, P(mu >= mu_L - 4) = 0.230, n=4) |
| l1-review-clock-v3 | 4 | 0 | 43.74 (5.93) | 0.021 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.021, P(mu >= mu_L - 4) = 0.263, n=4) |
| f7-single-skill-v1 | 6 | 0 | 43.43 (4.17) | 0.002 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.002, P(mu >= mu_L - 4) = 0.198, n=6) |
| l1-review-clock-v2 | 4 | 0 | 43.24 (5.93) | 0.017 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.017, P(mu >= mu_L - 4) = 0.240, n=4) |
| f7-trend-marking-v1 | 4 | 0 | 43.06 (4.32) | 0.002 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.002, P(mu >= mu_L - 4) = 0.185, n=4) |
| f8-secure-growth-v1 | 7 | 0 | 42.86 (6.79) | 0.027 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.027, P(mu >= mu_L - 4) = 0.246, n=7) |
| value-conversion-v1 | 7 | 0 | 42.6 (6.11) | 0.015 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.015, P(mu >= mu_L - 4) = 0.218, n=7) |
| l1-review-clock-v1 | 4 | 0 | 42.56 (5.93) | 0.013 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.013, P(mu >= mu_L - 4) = 0.211, n=4) |
| p0-review-guard-v1 | 3 | 0 | 40.7 (5.64) | 0.004 | **REPEAT** | REPEAT: n=3 < n0=4 |
| p0-minimal-v1 | 7 | 0 | 40.26 (5.06) | 0.001 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.001, P(mu >= mu_L - 4) = 0.104, n=7) |
| f6-commitment-ledger-v1 | 6 | 0 | 40.18 (6.72) | 0.01 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.010, P(mu >= mu_L - 4) = 0.149, n=6) |
| f4-review-first-v1 | 3 | 0 | 39.87 (7.59) | 0.017 | **REPEAT** | REPEAT: n=3 < n0=4 |
| f4-visible-delivery-v1 | 5 | 0 | 39.02 (7.31) | 0.01 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.010, P(mu >= mu_L - 4) = 0.132, n=5) |
| observed-growth-v1 | 9 | 0 | 38.75 (5.79) | 0.002 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.002, P(mu >= mu_L - 4) = 0.085, n=9) |
| m3-subtracted-v1 | 3 | 0 | 38.42 (8.32) | 0.017 | **REPEAT** | REPEAT: n=3 < n0=4 |
| m3-sustainable-career-v0-1 | 4 | 0 | 38.01 (8.18) | 0.014 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.014, P(mu >= mu_L - 4) = 0.129, n=4) |
| observed-growth-v2 | 4 | 0 | 37.57 (6.3) | 0.002 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.002, P(mu >= mu_L - 4) = 0.073, n=4) |
| o2-run-hot-v1 | 4 | 0 | 35.24 (8.69) | 0.008 | **REPEAT** | REPEAT: not separable yet (P(best) = 0.008, P(mu >= mu_L - 4) = 0.086, n=4) |
| f5-relationship-capital-v1 | 5 | 0 | 29.43 (3.89) | 0.0 | **DORMANT** | DORMANT: n=5 >= n0=4 and P(mu >= mu_L - 4) = 0.000 < 0.05 (mean 29.4 vs leader 19618e7795be8da1 52.2) |
| f2-invest-early-v1 | 5 | 0 | 24.92 (6.62) | 0.0 | **DORMANT** | DORMANT: n=5 >= n0=4 and P(mu >= mu_L - 4) = 0.001 < 0.05 (mean 24.9 vs leader 19618e7795be8da1 52.2) |

Leader history (stall trigger: leader posterior mean not improved by 2 Y-points over 3 decisions):

| Decision | Time | Leader | Posterior Y |
|---:|---|---|---:|
| #78 | 26 Oct 13:26 UTC | f3-feedback-reactive-v1 | 61.34 |
| #83 | 26 Oct 13:39 UTC | f3-feedback-reactive-v1 | 61.34 |
| #88 | 26 Oct 14:07 UTC | f3-feedback-reactive-v1 | 60.21 |
| #114 | 26 Oct 16:49 UTC | f7-three-skills-v1 | 55.21 |
| #128 | 26 Oct 17:50 UTC | f7-three-skills-v1 | 55.16 |
| #142 | 26 Oct 18:10 UTC | f1-steady-balance-v1 | 54.59 |
| #150 | 26 Oct 19:03 UTC | f1-steady-balance-v1 | 52.19 |

Gain over the last three decisions: -3.02 → stall trigger **fires**.

## Progressive widening (Haiku cell)

| Family | terminal Haiku episodes N_f | cap ⌈(1+N_f)^0.5⌉ | children so far |
|---|---:|---:|---:|
| f7-one-vs-many | 34 | 6 | 3 |
| f3-feedback-reactive | 26 | 6 | 4 |
| f1-steady-balance | 19 | 5 | 4 |
| matteo-feedback-growth | 13 | 4 | 3 |
| l1-review-clock | 12 | 4 | 2 |
| f2-invest-early | 12 | 4 | 1 |
| p0-minimal | 10 | 4 | 1 |
| f4-visible-delivery | 8 | 3 | 1 |
| o1-promotion-gap | 7 | 3 | 0 |
| matteo-value-conversion | 7 | 3 | 0 |
| m3-teammate | 7 | 3 | 1 |
| f8-secure-growth | 7 | 3 | 1 |
| f6-commitment-ledger | 6 | 3 | 0 |
| f5-relationship-capital | 5 | 3 | 0 |
| o2-run-hot | 4 | 3 | 0 |

## Children created in this cloud run

### f8-secure-growth-v1 (`5f8c9648b6abd9b0`, family f8-secure-growth)

- Parents: f3-feedback-reactive-v1, f3-lean-v1; operator: new family seeded from the F3 core (cross-branch hypothesis under the stagnation rule); idea origin: playbook:P10 (less defensive family that keeps its response to warnings), chosen because the stall trigger fires and because of the score-gap finding in findings.md (strategy-session request, 26 Oct ~14:45 UTC).
- Hypothesis: Completed games already survive; the score they leave on the table is mostly career level and wealth (findings.md, 48 completed games, all actors), and every family so far optimises survival. F3's Clear state spends quiet quarters lifting the weakest statistic, which keeps the agent safe but does not compete for promotion. A policy that keeps F3's risk response (Secure) and weak-review plan (Repair) with higher precedence, and otherwise plays for promotion and pay (Grow: Apply for a key project, High-intensity work plus Prepare report materials while Health is comfortable, story options that raise Output, Skill, Wealth or standing at a bounded cost), will earn more A or S reviews, hence more promotions and salary, and end with higher level and wealth dimensions than F3 and f3-lean without more eliminations.
- Haiku runs so far: Q 55.8/T 48, Q 68.6/T 48, Q 23.5/T 24, Q 51.9/T 48, Q 15.7/T 24, Q 55.9/T 48, Q 34.9/T 33.

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
- Haiku runs so far: Q 64.4/T 48, Q 15.7/T 24, Q 31.0/T 20, Q 64.7/T 48, Q 23.0/T 8, Q 64.9/T 48, Q 58.0/T 48.

### o2-run-hot-v1 (`663c8cd2a1cafe68`, family o2-run-hot)

- Parents: ; operator: new family (outside designer); idea origin: T4 outside ideas: agent without access to the team's Skills; sources: handbook, public rules, score structure.
- Hypothesis: Survivors fall short on level and wealth because they hold Health and Dignity near full; treating them as fuel and switching between Full, Cruise and Cool modes on observed state and warnings converts the unused resilience margin into more Output and Skill, earlier promotions and more cash taken from events, without raising the early-elimination rate.
- Haiku runs so far: Q 24.7/T 24, Q 38.6/T 29, Q 61.9/T 48, Q 19.7/T 24.

### f7-trend-marking-v1 (`188c7c484fa3519b`, family f7-one-vs-many)

- Parents: f7-three-skills-v1; operator: refine; idea origin: trace diagnosis of the 38 cloud Haiku digests (lab/reports/cloud-run-diagnostics/block3-generation.md, tables 2-4) and distilled Opus rule R3 'judge statistics by trend, not size' (lab/reports/teacher-digests/distilled-rules.md).
- Hypothesis: Reviews reward Output and Network being at their recent high when the review lands: across 127 reviews at Level 1-2, a B or a promotion followed 33 of 62 reviews with both at their high, 9 of 24 with Output only, 6 of 28 with Network only and 1 of 13 with neither; every one of the 14 first-review promotions had Output at its high (12 of 24 non-promoted games did not). The leader marks dimensions at risk by size and after any C or D, and every first review is a C, so the marks stop carrying information: in e373478a-04 Network was marked at risk in 62 of 88 story decisions below Level 3, 37 of them with Network at its high, and its two C reviews at Level 2 came with Network (review 2) and Output (review 3) below their high. Marking Skill, Network and Output at risk only when below their recent high makes the leader's own story rule 1 shield a stat that fell, its Energy rule restore it, and its main action default to a key project, so more reviews find Output and Network at their high.
- Haiku runs so far: Q 18.6/T 24, Q 51.6/T 48, Q 19.0/T 24, Q 54.0/T 45.

### f7-delivery-stories-v1 (`1d62c4e5121233e6`, family f7-one-vs-many)

- Parents: f7-three-skills-v1; operator: refine; idea origin: trace diagnosis of the 38 cloud Haiku digests (lab/reports/cloud-run-diagnostics/block3-generation.md, table 4: stats lost between the last quarterly phase and the review).
- Hypothesis: Output or Network lost in the story events between the last quarterly phase and a review cannot be restored by Energy before that review, and the loss costs the grade: at Level 1-2 a B or promotion followed 14 of 60 reviews with such a loss against 34 of 66 without (leader digests: 3 of 6 reviews had one, including both C reviews at Level 2 in e373478a-04). The losing story options share a visible pattern (delays, side duties, other people's processes, pauses), the gaining ones another (finishing, fixing or showing your own work), and Haiku's default choice in an event is the same across policies, so a rule that switches its preference while Output or Network is below its recent high will cut these losses and raise the share of good reviews without adding hidden risk.
- Haiku runs so far: Q 42.1/T 48, Q 63.2/T 48, Q 18.1/T 24, Q 62.7/T 48.

### f7-promotion-drive-v1 (`7ded9840c5c439d9`, family f7-one-vs-many)

- Parents: f7-three-skills-v1, f8-secure-growth-v1; operator: recombine (cross-family, stagnation slot); idea origin: playbook:P12 (stagnation rule, decision #114).
- Hypothesis: The weak-review streak is a promotion bottleneck, not a balance problem: no review after the first gave a B at Level 1 (0 of 47), every game still at Level 1 after its third review ended by month 24 (12 of 12), and the first promotion's timing sets the score (promoted at review 1: mean Q 57.3, 12 of 14 completed; at review 2: 47.0, 7 of 11; not by review 2: 22.0, 0 of 13). Balanced play spends quarters on statistics that have stopped rising, and the leader's notes mark most dimensions at risk on most turns. A temporary single priority (P12) - while the latest review did not promote you, take the story option that best shows delivered results or raises standing with decision makers at a bounded cost, with Apply for a key project as main action, and only Health, Dignity, Wealth and risk warnings as exceptions - brings the first promotion earlier than the leader's balanced rules. f8-secure-growth, whose Grow mode played this way before its first review, was promoted at review 1 in 3 of 4 Haiku games against 14 of 38 overall.
- Haiku runs so far: Q 19.5/T 24, Q 70.3/T 48, Q 53.8/T 47, Q 48.7/T 48.

### f1-core-v1 (`dbeb30d58b324510`, family f1-steady-balance)

- Parents: f1-steady-balance-v1; operator: refine (subtraction); idea origin: playbook:P20 + diagnostic:F1 trace audit (lab/reports/cloud-run-diagnostics/block5-generation.md).
- Hypothesis: F1's lead on Haiku comes from a small core that the actor actually executes: the Act test, repair the weakest, the story filter, Act-first Energy and a main action aimed at the weakest gap. The rest is either unused or works against that core. In 809 decisions of the 4 F1 digests, notes use the Watch and Fine labels 1% and 0% of the time, cite the Output-after-a-C-or-D rule 1% and 'spread' 0%, and Skill learning or High-intensity work appears in 0 of 64 Energy phases. The late-run caution is cited in 11% of notes from mid-run on and produced all 5 of F1's Lay-low main actions, every one at full Health, against F1's own rule 'Lay low only when Health is Act'; the weakest F1 game (Q 57.1, four Cs) took 4 of them. Keeping only the executed core (486 to 284 words) keeps F1's completion and score on Haiku, removes the contradiction a weaker reader resolves towards caution, and costs fewer tokens on every turn.
- Haiku runs so far: no finished runs yet.

### f1-risk-signal-v1 (`c9f41c4f60e41cc2`, family f1-steady-balance)

- Parents: f1-steady-balance-v1; operator: refine (single fix on the subtracted core); idea origin: diagnostic:unanswered risk signals in F1 traces (lab/reports/cloud-run-diagnostics/block5-generation.md) + playbook:P20 base (f1-core-v1 text).
- Hypothesis: F1 answers risk feedback by its strength, not its presence. In its 4 Haiku digests it took Defuse legacy risk after 11 of 22 risk-mentioning remarks (5 of 9 at 'piled up' or worse) and in none of the 6 Energy phases after its 3 blow-ups. 3 of the 4 games had a blow-up, one short of a trust crisis, which is how both of F1's Opus losses ended. Across the 86 Haiku digests, taking Defuse in the phase after a mild risk remark cut the rate of blow-ups within three months from 10% (9/93) to 2% (2/110); after a stronger remark it cut it from 20% (10/51) to 8% (13/154). After a calm remark it changed nothing (4% against 4%). The remark was calm again by the month's end in 86% of phases with Defuse against 34% without. Every D grade (37 of 37) came with a risk-mentioning remark in the review month. The new rule treats any non-reassuring risk feedback, or a blow-up since the last phase, as a signal that puts Defuse legacy risk right after Act recovery. It should cut blow-ups, risk-loaded reviews and D grades, and through them trust-crisis and dismissal exits, at a small cost in Prepare report materials.
- Haiku runs so far: no finished runs yet.

### f1-status-line-v1 (`30794daa53021d77`, family f1-steady-balance)

- Parents: f1-steady-balance-v1, f3-lean-v1; operator: recombine (cross-branch, stagnation slot): same rules, new intermediate representation; idea origin: playbook:P22 (stagnation rule, decision #142).
- Hypothesis: F1's losses come from execution, not from missing strategy. The rules exist, but the actor skips or reorders them: Defuse after 50% of risk signals, Lay low at full Health against the Lay-low guard, Watch and Fine labels never written. A status line filled every turn makes rule execution consistent for a small model. Its slots are the Act dimensions, Risk calm or raised (F3's named signal state, borrowed as a label only) and the Weakest. A strict need order (Act, then raised Risk, then Weakest), each need mapped to its Energy, story and main-action response, does the rest. The policy should lift completion and mean quantitative_score over F1 and match or beat f1-risk-signal-v1, which has the same rules in prose.
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
| f3-opus-distilled-v1 | 4 | 27.8, 19.8, 47.4, 58.5 | 2 |
| f3-distilled-prereview-defuse-v1 | 4 | 32.0, 61.8, 59.1, 56.7 | 0 |

## Problem A check: Haiku vs opus~100k on shared policies

opus~100k decision computed with the same rule but **not recorded** (only the Haiku decision is the block decision).

| Policy | Haiku posterior Y (n) | opus~100k posterior Y (n) | opus~100k pending |
|---|---|---|---:|
| f1-steady-balance-v1 | 52.19 (12) | 65.56 (2) | 0 |
| p0-minimal-v1 | 40.26 (7) | 61.58 (2) | 0 |
| f3-feedback-reactive-v1 | 50.1 (6) | 39.05 (2) | 0 |
| f3-lean-v1 | 51.11 (5) | 39.04 (2) | 0 |
| m3-sustainable-career-v0-1 | 38.01 (4) | 38.99 (2) | 0 |
| f3-balance-recombined-v1 | 51.19 (7) | 38.24 (2) | 0 |

Shared policies with opus~100k data: 6. Spearman of posterior means 0.20; top policy Haiku `f1-steady-balance-v1`, opus~100k `f1-steady-balance-v1` (agree). Descriptive only: with this few shared policies and 2–4 runs per cell, agreement cannot certify transfer (pruning authority needs ≥ 8 shared policies spanning ≥ 16 Y-points).

## Actor comparison (all Claude-proxy episodes, `careerlab.analysis`)

Imported episodes from the Mac have no local `result.json`; their rows come from the registry evaluation (early-exit causes are blank for them).

| Actor | eps | interrupted | completion | mean Q (sd) | mean Y | mean months | rejected/ep | min/ep | min/month | cache-read M/month | list-USD/ep |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| haiku | 175 | 0 | 0.54 | 44.9 (18.9) | 43.6 | 37.6 | 0.01 | 9.0 | 0.24 | 0.513 | 0.75 |
| haiku@low | 6 | 0 | 0.33 | 39.2 (16.2) | 38.0 | 33.7 | 0 | 7.0 | 0.21 | 0.302 | 0.36 |
| opus | 6 | 0 | 0.33 | 37.3 (17.0) | 36.5 | 34.8 | 0 | 8.1 | 0.23 | 0.257 | 3.4 |
| opus@low | 6 | 0 | 0.33 | 42.5 (13.8) | 40.6 | 33.5 | 0 | 6.4 | 0.19 | 0.215 | 2.85 |
| opus~100k | 12 | 0 | 0.58 | 49.0 (19.9) | 47.1 | 36.6 | 0 | 10.2 | 0.28 | 0.119 | 2.71 |
| sonnet | 26 | 0 | 0.38 | 39.4 (20.0) | 38.4 | 35 | 0.04 | 8.2 | 0.23 | 0.258 | 1.66 |

| Actor | Policy | n | Q per episode | months | mean Y | early-exit causes |
|---|---|---:|---|---|---:|---|
| haiku | f1-review-risk-v1 | 7 | [51.8, 24.0, 61.0, 54.8, 65.0, 20.2, 61.2] | [48, 24, 48, 48, 48, 24, 48] | 47.2 | ; Dismissed for capability — a second weak |
| haiku | f1-steady-balance-v1 | 12 | [51.0, 66.6, 27.7, 71.8, 68.1, 63.1, 66.1, 57.1, 62.3, 60.9, 24.8, 54.0] | [48, 48, 24, 48, 48, 48, 48, 48, 48, 48, 24, 48] | 54.1 | ; Dismissed for capability — a second weak |
| haiku | f2-convert-on-review-v1 | 7 | [61.2, 30.0, 63.6, 58.9, 65.2, 62.6, 18.4] | [48, 24, 48, 48, 48, 48, 24] | 49.7 | ; Dismissed for capability — a second weak |
| haiku | f2-invest-early-v1 | 5 | [47.1, 18.3, 18.6, 15.0, 14.4] | [47, 18, 24, 19, 24] | 23.2 | ; ; ; Trust crisis — a second major blow-up. T; Dismissed for capability — a second weak |
| haiku | f3-balance-recombined-v1 | 7 | [63.0, 59.2, 65.7, 54.6, 30.8, 55.6, 66.6] | [48, 48, 48, 48, 24, 48, 48] | 54.5 | Dismissed for capability — a second weak |
| haiku | f3-distilled-prereview-defuse-v1 | 4 | [61.8, 32.0, 59.1, 56.7] | [48, 24, 48, 48] | 50.7 | Dismissed for capability — a second weak |
| haiku | f3-feedback-reactive-v1 | 6 | [59.7, 66.3, 66.6, 28.7, 22.4, 68.1] | [48, 48, 48, 24, 24, 48] | 49.9 | Dismissed for capability — a second weak; Dismissed for capability — a second weak |
| haiku | f3-lean-v1 | 5 | [50.1, 64.3, 46.7, 59.5, 62.8] | [48, 48, 48, 48, 48] | 55.3 |  |
| haiku | f3-opus-distilled-v1 | 4 | [27.8, 19.8, 47.4, 58.5] | [24, 24, 48, 48] | 38.2 | Dismissed for capability — a second weak; Dismissed for capability — a second weak |
| haiku | f4-review-first-v1 | 3 | [19.7, 60.3, 62.5] | [24, 48, 48] | 46.3 |  |
| haiku | f4-visible-delivery-v1 | 5 | [55.9, 59.1, 17.6, 18.8, 24.4] | [48, 48, 24, 17, 31] | 35.1 | ; Broke — months with an empty wallet. Som; Trust crisis — a second major blow-up. T |
| haiku | f5-relationship-capital-v1 | 5 | [21.8, 48.5, 23.1, 32.5, 26.9] | [24, 39, 24, 29, 24] | 29.4 | ; ; ; Trust crisis — a second major blow-up. T; Trust crisis — a second major blow-up. T |
| haiku | f6-commitment-ledger-v1 | 6 | [30.5, 25.8, 49.7, 23.0, 67.8, 48.4] | [30, 8, 48, 24, 48, 48] | 40.2 | ; ; Dismissed for capability — a second weak |
| haiku | f7-delivery-stories-v1 | 4 | [63.2, 42.1, 62.7, 18.1] | [48, 48, 48, 24] | 46.0 | Dismissed for capability — a second weak |
| haiku | f7-promotion-drive-v1 | 4 | [19.5, 70.3, 53.8, 48.7] | [24, 48, 47, 48] | 46.0 | Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T |
| haiku | f7-single-skill-v1 | 6 | [54.2, 63.9, 20.6, 60.1, 30.9, 23.1] | [48, 48, 24, 48, 30, 24] | 41.2 | ; Trust crisis — a second major blow-up. T; Dismissed for capability — a second weak |
| haiku | f7-three-skills-v1 | 16 | [50.4, 51.5, 67.1, 71.0, 58.5, 70.4, 69.2, 20.1, 68.6, 61.9, 21.5, 44.9, 29.8, 19.0, 68.9, 16.5] | [48, 48, 48, 48, 48, 48, 48, 6, 48, 48, 24, 48, 24, 24, 48, 24] | 47.9 | Blackout — your health hits zero. The sc; Dismissed for capability — a second weak; Dismissed for capability — a second weak; Dismissed for capability — a second weak; Dismissed for capability — a second weak |
| haiku | f7-trend-marking-v1 | 4 | [18.6, 51.6, 19.0, 54.0] | [24, 48, 24, 45] | 34.9 | Dismissed for capability — a second weak; Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T |
| haiku | f8-secure-growth-v1 | 7 | [68.6, 55.8, 23.5, 51.9, 15.7, 55.9, 34.9] | [48, 48, 24, 48, 24, 48, 33] | 42.9 | Dismissed for capability — a second weak; Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T |
| haiku | l1-review-clock-v1 | 4 | [72.9, 29.2, 28.5, 20.3] | [48, 23, 9, 24] | 36.4 | Trust crisis — a second major blow-up. T; Blackout — your health hits zero. The sc; Dismissed for capability — a second weak |
| haiku | l1-review-clock-v2 | 4 | [23.8, 51.6, 39.5, 66.6] | [24, 48, 38, 48] | 43.8 | Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T |
| haiku | l1-review-clock-v3 | 4 | [28.3, 66.4, 46.1, 68.2] | [24, 48, 44, 48] | 49.3 | Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T |
| haiku | m3-subtracted-v1 | 3 | [16.0, 60.6, 48.9] | [24, 48, 48] | 41.8 |  |
| haiku | m3-sustainable-career-v0-1 | 4 | [17.2, 70.2, 27.8, 30.9] | [24, 48, 24, 26] | 35.5 | ; ;  |
| haiku | o1-promotion-gap-v1 | 7 | [64.4, 15.7, 31.0, 64.7, 23.0, 64.9, 58.0] | [48, 24, 20, 48, 8, 48, 48] | 44.6 | Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T; Broke — months with an empty wallet. Som |
| haiku | o2-run-hot-v1 | 4 | [24.7, 38.6, 61.9, 19.7] | [24, 29, 48, 24] | 35.2 | Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T; Dismissed for capability — a second weak |
| haiku | observed-growth-v1 | 9 | [52.4, 55.0, 24.4, 69.9, 18.8, 58.7, 20.1, 15.3, 68.2] | [48, 48, 24, 48, 24, 48, 24, 19, 48] | 41.8 | Dismissed for capability — a second weak; Dismissed for capability — a second weak; Dismissed for capability — a second weak; Trust crisis — a second major blow-up. T |
| haiku | observed-growth-v2 | 4 | [21.2, 23.0, 15.2, 62.8] | [9, 9, 24, 48] | 30.7 | Blackout — your health hits zero. The sc; Blackout — your health hits zero. The sc; Dismissed for capability — a second weak |
| haiku | p0-minimal-v1 | 5 | [53.9, 57.4, 31.6, 32.0, 18.5] | [48, 48, 22, 23, 24] | 37.9 | ; ;  |
| haiku | p0-review-guard-v1 | 3 | [41.9, 54.2, 45.1] | [33, 42, 47] | 42.6 | ; ;  |
| haiku | value-conversion-v1 | 7 | [65.1, 37.1, 46.2, 69.9, 28.1, 46.7, 23.5] | [48, 31, 40, 48, 22, 45, 24] | 42.6 | Trust crisis — a second major blow-up. T; Trust crisis — a second major blow-up. T; Trust crisis — a second major blow-up. T; Trust crisis — a second major blow-up. T; Dismissed for capability — a second weak |
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
| haiku | opus~100k | 6 | False | -0.14 |
| haiku | sonnet | 10 | False | 0.55 |
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
- **Block-3 generation (17:25 UTC)**, diagnosis in `lab/reports/cloud-run-diagnostics/block3-generation.md`.
  - The weak-review streak is about **promotion, not grades**. No game got a B while still at Level 1 after its first review (0 of 47 reviews). Games first promoted at review 1 averaged Q 57.3, with 12 of 14 completed. Games first promoted at review 2 averaged 47.0, with 7 of 11 completed. Games not promoted by review 2 averaged 22.0, and none of the 13 completed.
  - Output and Network falling through story choices before a review precede weak grades.
  - New candidates: f7-trend-marking, f7-delivery-stories, and the stall slot f7-promotion-drive (P12), with 4 Haiku screens each.
- **T13 complete (17:55 UTC):** mean Y 54.2 (90 % interval 41.6–66.7), 5 of 6 completed, reading **"near the ceiling"**. Level and wealth losses are identical to the other completed games, so effort goes to reliability and token efficiency (details in `lab/reports/opus-ceiling/README.md`).
- **Problem A complete:** Spearman 0.20 on 6 shared policies. opus~100k completes only 2 of 6 games with F3-family Skills, against 4 of 4 with F1 and P0.
- **Decision #128 (17:50):** f7-three-skills 55.2 (n = 10), F1 54.6, f2-convert-on-review 53.9. The stall rule still fires.
- **Block 4 allocated** (seed 20261154): F7 three-skills 6, observed-growth 5, F1 4, value-conversion 3, plus a dormant audit of P0 (2 games).
- **Next generation**, after the F7 children's screen: reliability-focused, i.e. leaving Level 1 by the first or second review.
- **Organiser round 3 (17:57 UTC):** merged `leah/workspace` (l1-review-clock v2 and v3) and `matteo/observed-growth-v2` (which includes `matteo-t4-growth`). Imported origins `leah` and `matteo` (0 conflicts). Registered and queued 4 Haiku screens each: l1-review-clock-v2 `6e26797afe52e4fd`, l1-review-clock-v3 `35576a667c2f3d53`, observed-growth-v2 `f2715987f0341ab2`.
- **Decision #142 (18:11 UTC):** the F7 children did not help (42–45). New leader **f1-steady-balance**, 54.6. Batch 4 (38 games) is running. Block-5 generation is in progress: F1 children aimed at reliability, plus the stall slot.
- **Block-5 generation (18:29 UTC)**, diagnosis in `lab/reports/cloud-run-diagnostics/block5-generation.md`. F1 loses to blow-ups that go unanswered, not to weak reviews: it took Defuse after only 11 of 22 non-reassuring risk remarks, and never after a blow-up. Across the 86 Haiku games, Defuse after a risk remark cut blow-ups from 10 % to 2 % (mild remark) and from 20 % to 8 % (strong remark). All 37 D grades came with a risk remark.
  - New F1 children, nested: f1-core (P20 subtraction), f1-risk-signal (core plus Defuse on any non-reassuring risk feedback), and the stall slot f1-status-line (P22: the same rules as a status line). 4 Haiku screens each.
- **Organiser round 4 (18:32 UTC):** restored ESTADO.md, which the block-5 commit had emptied for about 5 minutes on main (an edit script opened it for writing before reading). Merged `matteo/observed-growth-v3` (his own pilot: 4/4 completed, mean Q 71.4, a different actor cell, now being checked in the race) and `alejandro/investigacion-decisiones` (decision research that only analyses exports; PR #3). Imported origin `matteo` (0 conflicts).
- **Decision #150 (19:03 UTC):** F1 52.2 (n = 12), f3-balance-recombined 51.2, f3-lean 51.1, f1-review-risk 50.4, F3 50.1. With more data the top posteriors bunch around 50–52, and none has P(best) ≥ 0.2. **Block 6 allocated:** 18 slots (seed 20261176); its stall slot is 1 more game of f7-promotion-drive. Batch 5 (F1 children and observed-growth-v3) is running.

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
| value-conversion-v1 | 91b30e8096ff6766 | matteo-value-conversion (T4, Matteo) | none | Convert responsibility into career value inside story decisions (scope, resources, pay). Not blind: the author saw our broad conclusions. |
| observed-growth-v1 | f03981dac92f8b6c | matteo-feedback-growth (Matteo) | f8, value-conversion | A concise priority order with checks that each investment actually paid off. Matteo's isolated Haiku pilot scored 64.8. |
| l1-review-clock-v1 | f1830961d168beb9 | l1-review-clock (Leah) | none | Keep a Health reserve, read risk from feedback, and grow Output, Skill and Network together for each promotion window. Her own game (origin leah) scored 60.9. |
| f7-trend-marking-v1 | 188c7c484fa3519b | f7-one-vs-many | f7-three-skills | Mark Skill, Network and Output at risk by trend (below their recent high), not by size or grade. Trace-driven child of the leader. |
| f7-delivery-stories-v1 | 1d62c4e5121233e6 | f7-one-vs-many | f7-three-skills | While Output or Network is below its recent high, prefer finishing or showing your own work in stories. Traces show drops between the last quarterly phase and the review precede weak grades. |
| f7-promotion-drive-v1 | 7ded9840c5c439d9 | f7-one-vs-many | f7-three-skills, f8 | Stall slot, playbook P12 (decision #114): promotion drive until a review raises Level. Learning goal in its policy.json. |
| f1-core-v1 | (see registry) | f1-steady-balance | F1 | P20 subtraction: F1 without its unused and self-contradicting text. |
| f1-risk-signal-v1 | (see registry) | f1-steady-balance | F1 | Core plus Defuse right after recovery on any non-reassuring risk feedback or a blow-up. |
| f1-status-line-v1 | (see registry) | f1-steady-balance | F1, f3-lean | Stall slot P22 (decision #142): the same rules written as a fixed status line. |
| l1-review-clock-v2/v3, observed-growth-v2/v3 | 6e26797a…, 35576a66…, f2715987…, fe970f0d… | collaborators | their v1 | Leah's and Matteo's iterations, merged by the organiser. |

**Decisions recorded by this session**
- `enqueue`: Problem A, 2 × opus~100k each for F3, f3-balance-recombined and f3-lean.
- `enqueue`: 4 Haiku screens each for f8 and the two distilled children.
- `reprioritise`: 4 Mac-queued calibrate replacements (default opus, opus@low) to −10, because of the weekly pace.
- `reprioritise`: the 6 Problem-A opus~100k jobs to −5, behind the Haiku replicates.
- `enqueue`: 4 Haiku screens each for o1 and o2 (T4).
- `hold`: o3-sponsor-lens (overlaps F4 and F5).
- Block decision #114 after batch 1: leader f7-three-skills 55.2; stall rule fires; f5 and f2 dormant.
- `allocate`: 24 block-3 repeat slots by top-two Thompson sampling, seed 20261140, no audit.
- `enqueue`: 2 more T13 ceiling games (pre-stated rule for mixed results).
- `enqueue`: 4 Haiku screens each for value-conversion, observed-growth, l1-review-clock and the three F7 children.
- `recover`: several entries.
- Block decisions appear after each batch.

**Progressive widening.** Prereg §6 counts N_f as terminal episodes in the family subtree, all actors. For F3 that is 9 (F3 5, f3-balance-recombined 2, f3-lean 2), so the cap is 4: 2 children existed and both distilled children fit. The report table counts Haiku-only N_f, which is stricter.

### 2. Results so far
See the sections above: latest block decision, actor comparison, Problem A, T13. T13 is complete: mean Y 54.2, near the ceiling. Problem A is complete: the rankings disagree on the F3 family. Block decisions #114 and #128. For the numbers, see the sections above and `findings.md`.

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
