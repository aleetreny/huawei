# Synthetic method comparison (SynthCareer, known ground truth)

R = 60 replications per method, budget 2000 cost units (target episode 10, cheap episode 1; cheap actor `cheap_biased`, target actor `target`), seed 0. Truth: mean Y over 2000 games on fixed truth seeds (500 for rejected policies). Oracle best true Y = 67.50 (2617 candidates, 753,580 episodes). Common random numbers across methods. Wall time 113 s on 16 workers.

Cells: mean [95% interval over replications]; P(within 2) uses a Wilson interval; differences are paired by replication. Generation is emulated by parametric operators, so this tests allocation, selection and validation machinery under known mechanisms, not LLM-written policies or the real game.

| method | true Y of selected | regret vs oracle | P(within 2) | false-rejection rate (delta_t) | families explored | target / cheap / confirm share (%) | estimate bias | Δ true Y vs best_of_n |
|---|---|---|---|---|---|---|---|---|
| best_of_n | 53.4 [52.1, 54.7] | 14.1 [12.8, 15.4] | 0 [0, 6]% | n/a | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 1.7 [0.7, 2.7] (in_sample) | n/a |
| refine_leader | 52.2 [50.9, 53.5] | 15.3 [14.0, 16.6] | 0 [0, 6]% | n/a | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 4.2 [3.5, 4.9] (in_sample) | -1.2 [-2.8, 0.4] |
| racing | 56.2 [55.1, 57.2] | 11.3 [10.3, 12.4] | 0 [0, 6]% | 38 [35, 41]% | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 7.4 [6.2, 8.6] (in_sample) | 2.8 [1.4, 4.2] |
| full | 54.5 [53.3, 55.6] | 13.0 [11.9, 14.2] | 0 [0, 6]% | 8 [5, 11]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | 0.5 [-0.3, 1.3] (fresh) | 1.1 [-0.1, 2.2] |
| no_diversity | 52.6 [51.0, 54.2] | 14.9 [13.3, 16.5] | 0 [0, 6]% | 13 [9, 16]% | 3.0 [2.7, 3.2] | 92 / 8 / 15 | -0.2 [-1.0, 0.6] (fresh) | -0.8 [-2.8, 1.2] |
| no_reopen | 54.0 [52.8, 55.2] | 13.5 [12.3, 14.7] | 0 [0, 6]% | 7 [5, 9]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | 0.5 [-0.2, 1.2] (fresh) | 0.6 [-0.4, 1.6] |
| no_calibration | 54.8 [53.8, 55.9] | 12.6 [11.6, 13.7] | 0 [0, 6]% | 10 [7, 12]% | 7.0 [7.0, 7.0] | 88 / 12 / 15 | -0.4 [-1.3, 0.6] (fresh) | 1.5 [0.3, 2.6] |
| partial_screening | 52.4 [51.1, 53.7] | 15.1 [13.8, 16.4] | 0 [0, 6]% | 30 [26, 35]% | 7.0 [7.0, 7.0] | 100 / 0 / 15 | 0.4 [-0.5, 1.3] (fresh) | -1.0 [-2.7, 0.6] |
| no_specialization | 53.9 [52.9, 55.0] | 13.6 [12.5, 14.6] | 0 [0, 6]% | 7 [5, 9]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | 0.6 [-0.3, 1.5] (fresh) | 0.5 [-0.7, 1.7] |
| target_only | 54.5 [53.4, 55.5] | 13.0 [12.0, 14.1] | 0 [0, 6]% | 8 [5, 10]% | 7.0 [7.0, 7.0] | 100 / 0 / 15 | 0.1 [-0.9, 1.0] (fresh) | 1.1 [-0.1, 2.3] |

Ablations, paired by replication (ablation minus full; negative means the component helps):

| ablation | what changes | Δ true Y vs full | strict false-rejection rate (delta_s) | policies evaluated | pruning authority ever granted |
|---|---|---|---|---|---|
| no_diversity | all roots drawn from one random family (same root count); generation unchanged | -1.9 [-3.8, 0.1] | 5 [3, 8]% | 26 [26, 27] | 83% of runs |
| no_reopen | dormancy is permanent: no audits, no reopening on new child hypotheses | -0.5 [-1.6, 0.7] | 2 [1, 3]% | 27 [27, 27] | 87% of runs |
| no_calibration | cheap actor prunes from the start, without calibration or pruning authority | 0.4 [-0.7, 1.5] | 4 [2, 5]% | 30 [30, 31] | 100% of runs |
| partial_screening | successive halving on truncated (proxy_month) target episodes; no cheap actor | -2.1 [-3.9, -0.3] | 18 [15, 22]% | 43 [43, 43] | 0% of runs |
| no_specialization | no specialize operator (its weight goes to refine) | -0.5 [-1.7, 0.6] | 2 [1, 2]% | 26 [26, 27] | 95% of runs |
| target_only | no cheap actor: every evaluation on target | -0.0 [-1.1, 1.1] | 3 [1, 5]% | 26 [26, 26] | 0% of runs |
| (full itself) | | 0 | 3 [1, 5]% | 26 [26, 27] | 92% of runs |

Process diagnostics of the CareerLab variants (means over replications):

| variant | blocks | generation share after roots, mean / min over runs (%) | blocks without a new candidate | blocks flagged stagnant | cheap-pruned | proxy-pruned | audits | dormancies held back as inconclusive | specializations accepted / proposed | runs with a confirmed claim vs incumbent (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| full | 6.0 | 44 / 30 | 0.00 | 2.1 | 2.0 | 0.0 | 0.8 | 0.2 | 0.03 / 1.6 | 78 |
| no_diversity | 6.0 | 44 / 29 | 0.00 | 1.8 | 1.9 | 0.0 | 0.9 | 1.9 | 0.08 / 1.2 | 67 |
| no_reopen | 6.0 | 45 / 35 | 0.00 | 2.3 | 2.2 | 0.0 | 0.0 | 0.1 | 0.00 / 1.6 | 70 |
| no_calibration | 7.2 | 43 / 34 | 0.00 | 2.9 | 13.5 | 0.0 | 1.2 | 0.5 | 0.05 / 2.0 | 77 |
| partial_screening | 7.5 | 39 / 38 | 0.00 | 3.1 | 0.0 | 30.5 | 1.5 | 0.2 | 0.18 / 3.9 | 65 |
| no_specialization | 6.0 | 43 / 32 | 0.02 | 2.2 | 2.0 | 0.0 | 1.1 | 0.2 | 0.00 / 0.0 | 70 |
| target_only | 6.0 | 39 / 39 | 0.00 | 1.8 | 0.0 | 0.0 | 1.0 | 0.2 | 0.02 / 1.4 | 80 |

Reference policies (true Y): no_invest 27.1, early_invest 46.8, state_switch 47.1, calendar8 42.7, feedback_switch 44.6, overcommit 33.3, steady_networker 35.0, incumbent 43.4.

Oracle top 5 (true Y): 67.50, 67.48, 67.32, 67.16, 67.15.
