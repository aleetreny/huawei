# Synthetic method comparison (SynthCareer, known ground truth)

R = 60 replications per method, budget 8000 cost units (target episode 10, cheap episode 1; cheap actor `cheap_biased`, target actor `target`), seed 0. Truth: mean Y over 2000 games on fixed truth seeds (500 for rejected policies). Oracle best true Y = 67.50 (2617 candidates, 753,580 episodes). Common random numbers across methods. Wall time 391 s on 16 workers.

Cells: mean [95% interval over replications]; P(within 2) uses a Wilson interval; differences are paired by replication. Generation is emulated by parametric operators, so this tests allocation, selection and validation machinery under known mechanisms, not LLM-written policies or the real game.

| method | true Y of selected | regret vs oracle | P(within 2) | false-rejection rate (delta_t) | families explored | target / cheap / confirm share (%) | estimate bias | Δ true Y vs best_of_n |
|---|---|---|---|---|---|---|---|---|
| best_of_n | 56.6 [55.6, 57.6] | 10.9 [9.9, 11.9] | 0 [0, 6]% | n/a | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 3.6 [2.7, 4.4] (in_sample) | n/a |
| refine_leader | 55.2 [54.2, 56.3] | 12.3 [11.2, 13.3] | 0 [0, 6]% | n/a | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 7.5 [6.8, 8.1] (in_sample) | -1.4 [-2.8, 0.0] |
| racing | 57.9 [57.0, 58.7] | 9.6 [8.8, 10.5] | 0 [0, 6]% | 40 [37, 42]% | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 4.3 [3.8, 4.7] (in_sample) | 1.2 [0.0, 2.4] |
| full | 58.5 [57.4, 59.5] | 9.0 [8.0, 10.1] | 0 [0, 6]% | 8 [6, 10]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | -0.0 [-0.5, 0.5] (fresh) | 1.8 [0.5, 3.2] |
| no_diversity | 58.2 [57.3, 59.0] | 9.3 [8.5, 10.2] | 0 [0, 6]% | 9 [7, 11]% | 6.8 [6.7, 6.9] | 92 / 8 / 15 | 0.5 [0.0, 0.9] (fresh) | 1.6 [0.4, 2.8] |
| no_reopen | 58.1 [57.2, 59.0] | 9.4 [8.5, 10.3] | 0 [0, 6]% | 10 [7, 12]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | -0.0 [-0.5, 0.4] (fresh) | 1.5 [0.3, 2.7] |
| no_calibration | 58.9 [58.2, 59.6] | 8.6 [7.9, 9.3] | 0 [0, 6]% | 6 [5, 8]% | 7.0 [7.0, 7.0] | 89 / 11 / 15 | 0.0 [-0.5, 0.5] (fresh) | 2.3 [1.2, 3.4] |
| partial_screening | 57.4 [56.6, 58.2] | 10.1 [9.3, 10.9] | 0 [0, 6]% | 11 [9, 13]% | 7.0 [7.0, 7.0] | 100 / 0 / 15 | 0.3 [-0.2, 0.8] (fresh) | 0.8 [-0.5, 2.1] |
| no_specialization | 58.4 [57.5, 59.3] | 9.1 [8.2, 10.0] | 3 [1, 11]% | 8 [6, 9]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | 0.0 [-0.5, 0.5] (fresh) | 1.8 [0.5, 3.1] |
| target_only | 58.8 [57.9, 59.7] | 8.7 [7.8, 9.6] | 3 [1, 11]% | 7 [6, 9]% | 7.0 [7.0, 7.0] | 100 / 0 / 15 | -0.3 [-0.8, 0.2] (fresh) | 2.2 [1.0, 3.4] |

Ablations, paired by replication (ablation minus full; negative means the component helps):

| ablation | what changes | Δ true Y vs full | strict false-rejection rate (delta_s) | policies evaluated | pruning authority ever granted |
|---|---|---|---|---|---|
| no_diversity | all roots drawn from one random family (same root count); generation unchanged | -0.3 [-1.5, 1.0] | 3 [2, 3]% | 93 [88, 98] | 97% of runs |
| no_reopen | dormancy is permanent: no audits, no reopening on new child hypotheses | -0.4 [-1.7, 1.0] | 3 [2, 4]% | 96 [91, 101] | 100% of runs |
| no_calibration | cheap actor prunes from the start, without calibration or pruning authority | 0.5 [-0.6, 1.5] | 2 [1, 2]% | 115 [108, 122] | 100% of runs |
| partial_screening | successive halving on truncated (proxy_month) target episodes; no cheap actor | -1.1 [-2.4, 0.3] | 5 [3, 6]% | 143 [143, 144] | 0% of runs |
| no_specialization | no specialize operator (its weight goes to refine) | -0.1 [-1.2, 1.1] | 2 [1, 3]% | 95 [90, 100] | 98% of runs |
| target_only | no cheap actor: every evaluation on target | 0.4 [-1.0, 1.8] | 2 [1, 3]% | 76 [76, 76] | 0% of runs |
| (full itself) | | 0 | 3 [1, 4]% | 94 [89, 98] | 98% of runs |

Process diagnostics of the CareerLab variants (means over replications):

| variant | blocks | generation share after roots, mean / min over runs (%) | blocks without a new candidate | blocks flagged stagnant | cheap-pruned | proxy-pruned | audits | dormancies held back as inconclusive | specializations accepted / proposed | runs with a confirmed claim vs incumbent (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| full | 31.5 | 40 / 33 | 0.00 | 22.3 | 31.6 | 0.0 | 6.0 | 2.4 | 0.25 / 7.5 | 98 |
| no_diversity | 31.5 | 39 / 32 | 0.00 | 21.0 | 31.9 | 0.0 | 6.1 | 5.1 | 0.32 / 6.3 | 100 |
| no_reopen | 32.0 | 41 / 33 | 0.00 | 22.4 | 32.5 | 0.0 | 0.0 | 2.6 | 0.23 / 7.0 | 100 |
| no_calibration | 32.8 | 36 / 32 | 0.00 | 24.3 | 71.4 | 0.0 | 6.6 | 1.5 | 0.13 / 6.0 | 100 |
| partial_screening | 32.4 | 36 / 35 | 0.00 | 23.5 | 0.0 | 105.0 | 6.9 | 1.8 | 0.33 / 7.8 | 100 |
| no_specialization | 31.4 | 39 / 32 | 0.02 | 21.9 | 34.1 | 0.0 | 6.2 | 2.9 | 0.00 / 0.0 | 100 |
| target_only | 31.0 | 39 / 38 | 0.00 | 21.0 | 0.0 | 0.0 | 5.8 | 2.5 | 0.20 / 6.1 | 98 |

Reference policies (true Y): no_invest 27.1, early_invest 46.8, state_switch 47.1, calendar8 42.7, feedback_switch 44.6, overcommit 33.3, steady_networker 35.0, incumbent 43.4.

Oracle top 5 (true Y): 67.50, 67.48, 67.32, 67.16, 67.15.
