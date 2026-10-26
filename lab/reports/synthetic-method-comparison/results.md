# Synthetic method comparison (SynthCareer, known ground truth)

R = 100 replications per method, budget 4000 cost units (target episode 10, cheap episode 1; cheap actor `cheap_biased`, target actor `target`), seed 0. Truth: mean Y over 2000 games on fixed truth seeds (500 for rejected policies). Oracle best true Y = 67.50 (2617 candidates, 753,580 episodes). Common random numbers across methods. Wall time 320 s on 16 workers.

Cells: mean [95% interval over replications]; P(within 2) uses a Wilson interval; differences are paired by replication. Generation is emulated by parametric operators, so this tests allocation, selection and validation machinery under known mechanisms, not LLM-written policies or the real game.

| method | true Y of selected | regret vs oracle | P(within 2) | false-rejection rate (delta_t) | families explored | target / cheap / confirm share (%) | estimate bias | Δ true Y vs best_of_n |
|---|---|---|---|---|---|---|---|---|
| best_of_n | 55.1 [54.3, 56.0] | 12.4 [11.5, 13.2] | 0 [0, 4]% | n/a | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 2.4 [1.6, 3.2] (in_sample) | n/a |
| refine_leader | 53.4 [52.6, 54.3] | 14.1 [13.2, 14.9] | 0 [0, 4]% | n/a | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 6.2 [5.6, 6.7] (in_sample) | -1.7 [-2.7, -0.7] |
| racing | 57.1 [56.3, 57.8] | 10.4 [9.7, 11.2] | 0 [0, 4]% | 39 [37, 41]% | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 7.3 [6.5, 8.1] (in_sample) | 1.9 [0.9, 2.9] |
| full | 56.5 [55.8, 57.3] | 10.9 [10.2, 11.7] | 0 [0, 4]% | 10 [8, 12]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | -0.0 [-0.5, 0.5] (fresh) | 1.4 [0.5, 2.3] |
| no_diversity | 55.7 [54.9, 56.5] | 11.8 [11.0, 12.6] | 0 [0, 4]% | 10 [8, 12]% | 5.0 [4.8, 5.2] | 92 / 8 / 15 | 0.2 [-0.3, 0.7] (fresh) | 0.6 [-0.5, 1.6] |
| no_reopen | 56.4 [55.8, 57.1] | 11.1 [10.4, 11.7] | 0 [0, 4]% | 11 [9, 13]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | -0.1 [-0.7, 0.4] (fresh) | 1.3 [0.4, 2.2] |
| no_calibration | 56.9 [56.2, 57.7] | 10.6 [9.8, 11.3] | 0 [0, 4]% | 10 [8, 12]% | 7.0 [7.0, 7.0] | 90 / 10 / 15 | -0.1 [-0.6, 0.4] (fresh) | 1.8 [0.8, 2.8] |
| partial_screening | 54.6 [53.7, 55.4] | 12.9 [12.1, 13.8] | 0 [0, 4]% | 20 [17, 22]% | 7.0 [7.0, 7.0] | 100 / 0 / 15 | 0.1 [-0.4, 0.6] (fresh) | -0.6 [-1.7, 0.5] |
| no_specialization | 56.3 [55.5, 57.1] | 11.2 [10.4, 12.0] | 1 [0, 5]% | 10 [8, 12]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | -0.2 [-0.7, 0.3] (fresh) | 1.2 [0.2, 2.1] |
| target_only | 56.4 [55.6, 57.2] | 11.1 [10.3, 11.9] | 0 [0, 4]% | 10 [8, 11]% | 7.0 [7.0, 7.0] | 100 / 0 / 15 | -0.0 [-0.5, 0.4] (fresh) | 1.3 [0.3, 2.2] |

Ablations, paired by replication (ablation minus full; negative means the component helps):

| ablation | what changes | Δ true Y vs full | strict false-rejection rate (delta_s) | policies evaluated | pruning authority ever granted |
|---|---|---|---|---|---|
| no_diversity | all roots drawn from one random family (same root count); generation unchanged | -0.9 [-1.9, 0.2] | 4 [3, 5]% | 46 [45, 47] | 96% of runs |
| no_reopen | dormancy is permanent: no audits, no reopening on new child hypotheses | -0.1 [-0.9, 0.6] | 3 [2, 4]% | 47 [46, 48] | 99% of runs |
| no_calibration | cheap actor prunes from the start, without calibration or pruning authority | 0.4 [-0.5, 1.2] | 3 [2, 3]% | 53 [51, 54] | 100% of runs |
| partial_screening | successive halving on truncated (proxy_month) target episodes; no cheap actor | -2.0 [-3.1, -0.9] | 10 [8, 12]% | 78 [78, 78] | 0% of runs |
| no_specialization | no specialize operator (its weight goes to refine) | -0.3 [-1.0, 0.5] | 4 [2, 5]% | 45 [45, 46] | 96% of runs |
| target_only | no cheap actor: every evaluation on target | -0.1 [-1.0, 0.7] | 3 [2, 4]% | 43 [43, 43] | 0% of runs |
| (full itself) | | 0 | 3 [2, 4]% | 46 [45, 47] | 98% of runs |

Process diagnostics of the CareerLab variants (means over replications):

| variant | blocks | generation share after roots, mean / min over runs (%) | blocks without a new candidate | blocks flagged stagnant | cheap-pruned | proxy-pruned | audits | dormancies held back as inconclusive | specializations accepted / proposed | runs with a confirmed claim vs incumbent (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| full | 14.1 | 40 / 31 | 0.00 | 7.4 | 9.2 | 0.0 | 2.6 | 0.6 | 0.05 / 3.4 | 94 |
| no_diversity | 14.1 | 41 / 31 | 0.00 | 7.1 | 8.8 | 0.0 | 2.7 | 2.7 | 0.19 / 3.3 | 93 |
| no_reopen | 15.0 | 42 / 34 | 0.00 | 8.1 | 9.3 | 0.0 | 0.0 | 0.7 | 0.09 / 3.7 | 93 |
| no_calibration | 15.8 | 39 / 32 | 0.00 | 9.0 | 25.3 | 0.0 | 3.3 | 0.8 | 0.10 / 3.8 | 95 |
| partial_screening | 16.0 | 38 / 36 | 0.00 | 9.7 | 0.0 | 56.5 | 3.2 | 0.4 | 0.30 / 6.0 | 90 |
| no_specialization | 14.1 | 40 / 29 | 0.01 | 7.7 | 8.4 | 0.0 | 2.8 | 0.8 | 0.00 / 0.0 | 95 |
| target_only | 14.2 | 39 / 38 | 0.00 | 7.5 | 0.0 | 0.0 | 2.7 | 0.8 | 0.11 / 3.0 | 97 |

Reference policies (true Y): no_invest 27.1, early_invest 46.8, state_switch 47.1, calendar8 42.7, feedback_switch 44.6, overcommit 33.3, steady_networker 35.0, incumbent 43.4.

Oracle top 5 (true Y): 67.50, 67.48, 67.32, 67.16, 67.15.
