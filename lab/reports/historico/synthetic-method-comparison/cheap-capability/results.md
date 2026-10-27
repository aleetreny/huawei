# Synthetic method comparison (SynthCareer, known ground truth)

R = 60 replications per method, budget 4000 cost units (target episode 10, cheap episode 1; cheap actor `cheap_capability`, target actor `target`), seed 0. Truth: mean Y over 2000 games on fixed truth seeds (500 for rejected policies). Oracle best true Y = 67.50 (2617 candidates, 753,580 episodes). Common random numbers across methods. Wall time 193 s on 16 workers.

Cells: mean [95% interval over replications]; P(within 2) uses a Wilson interval; differences are paired by replication. Generation is emulated by parametric operators, so this tests allocation, selection and validation machinery under known mechanisms, not LLM-written policies or the real game.

| method | true Y of selected | regret vs oracle | P(within 2) | false-rejection rate (delta_t) | families explored | target / cheap / confirm share (%) | estimate bias | Δ true Y vs best_of_n |
|---|---|---|---|---|---|---|---|---|
| best_of_n | 55.3 [54.3, 56.4] | 12.2 [11.1, 13.2] | 0 [0, 6]% | n/a | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 2.4 [1.4, 3.4] (in_sample) | n/a |
| refine_leader | 53.8 [52.6, 54.9] | 13.7 [12.6, 14.9] | 0 [0, 6]% | n/a | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 6.0 [5.3, 6.7] (in_sample) | -1.6 [-2.8, -0.3] |
| racing | 56.9 [55.9, 57.9] | 10.6 [9.6, 11.6] | 0 [0, 6]% | 40 [37, 43]% | 7.0 [7.0, 7.0] | 100 / 0 / 0 | 7.1 [6.0, 8.2] (in_sample) | 1.6 [0.4, 2.7] |
| full | 56.6 [55.5, 57.6] | 10.9 [9.9, 12.0] | 0 [0, 6]% | 10 [7, 12]% | 7.0 [7.0, 7.0] | 92 / 8 / 15 | -0.1 [-0.6, 0.4] (fresh) | 1.2 [0.2, 2.3] |
| no_diversity | 56.2 [55.2, 57.2] | 11.3 [10.3, 12.3] | 0 [0, 6]% | 10 [8, 12]% | 5.5 [5.1, 5.8] | 91 / 9 / 15 | 0.1 [-0.6, 0.8] (fresh) | 0.9 [-0.5, 2.2] |
| no_reopen | 56.3 [55.4, 57.2] | 11.2 [10.3, 12.1] | 0 [0, 6]% | 10 [7, 13]% | 7.0 [7.0, 7.0] | 91 / 9 / 15 | -0.6 [-1.2, -0.0] (fresh) | 1.0 [-0.5, 2.4] |
| no_calibration | 57.0 [56.2, 57.9] | 10.4 [9.6, 11.3] | 0 [0, 6]% | 9 [6, 11]% | 7.0 [7.0, 7.0] | 88 / 12 / 15 | -0.2 [-1.0, 0.5] (fresh) | 1.7 [0.6, 2.9] |
| partial_screening | 54.6 [53.5, 55.7] | 12.9 [11.8, 14.0] | 0 [0, 6]% | 20 [17, 23]% | 7.0 [7.0, 7.0] | 100 / 0 / 15 | 0.1 [-0.5, 0.7] (fresh) | -0.7 [-2.1, 0.6] |
| no_specialization | 56.2 [55.0, 57.4] | 11.3 [10.1, 12.5] | 0 [0, 6]% | 11 [9, 14]% | 7.0 [7.0, 7.0] | 91 / 9 / 15 | -0.6 [-1.2, 0.0] (fresh) | 0.9 [-0.4, 2.2] |
| target_only | 56.8 [55.8, 57.8] | 10.7 [9.7, 11.7] | 0 [0, 6]% | 9 [7, 11]% | 7.0 [7.0, 7.0] | 100 / 0 / 15 | -0.1 [-0.6, 0.5] (fresh) | 1.5 [0.2, 2.7] |

Ablations, paired by replication (ablation minus full; negative means the component helps):

| ablation | what changes | Δ true Y vs full | strict false-rejection rate (delta_s) | policies evaluated | pruning authority ever granted |
|---|---|---|---|---|---|
| no_diversity | all roots drawn from one random family (same root count); generation unchanged | -0.4 [-1.8, 1.0] | 2 [2, 3]% | 50 [48, 53] | 97% of runs |
| no_reopen | dormancy is permanent: no audits, no reopening on new child hypotheses | -0.3 [-1.6, 1.1] | 3 [1, 4]% | 51 [48, 53] | 97% of runs |
| no_calibration | cheap actor prunes from the start, without calibration or pruning authority | 0.5 [-0.6, 1.6] | 2 [1, 3]% | 63 [59, 66] | 100% of runs |
| partial_screening | successive halving on truncated (proxy_month) target episodes; no cheap actor | -1.9 [-3.4, -0.5] | 10 [8, 12]% | 78 [77, 78] | 0% of runs |
| no_specialization | no specialize operator (its weight goes to refine) | -0.3 [-1.5, 0.8] | 4 [2, 6]% | 50 [47, 53] | 97% of runs |
| target_only | no cheap actor: every evaluation on target | 0.2 [-1.0, 1.5] | 3 [2, 4]% | 43 [43, 43] | 0% of runs |
| (full itself) | | 0 | 3 [2, 4]% | 48 [46, 49] | 95% of runs |

Process diagnostics of the CareerLab variants (means over replications):

| variant | blocks | generation share after roots, mean / min over runs (%) | blocks without a new candidate | blocks flagged stagnant | cheap-pruned | proxy-pruned | audits | dormancies held back as inconclusive | specializations accepted / proposed | runs with a confirmed claim vs incumbent (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| full | 14.2 | 40 / 31 | 0.00 | 7.5 | 11.2 | 0.0 | 2.5 | 0.7 | 0.07 / 3.9 | 97 |
| no_diversity | 14.1 | 39 / 31 | 0.00 | 6.7 | 14.9 | 0.0 | 2.5 | 2.9 | 0.17 / 3.4 | 92 |
| no_reopen | 15.0 | 40 / 31 | 0.00 | 8.5 | 14.4 | 0.0 | 0.0 | 0.3 | 0.10 / 4.1 | 100 |
| no_calibration | 16.1 | 36 / 30 | 0.00 | 9.4 | 40.1 | 0.0 | 3.4 | 1.3 | 0.03 / 4.5 | 98 |
| partial_screening | 16.0 | 37 / 36 | 0.00 | 9.6 | 0.0 | 56.2 | 3.4 | 0.3 | 0.28 / 6.0 | 92 |
| no_specialization | 14.2 | 39 / 31 | 0.00 | 7.8 | 14.5 | 0.0 | 2.9 | 0.8 | 0.00 / 0.0 | 92 |
| target_only | 14.2 | 39 / 38 | 0.00 | 7.1 | 0.0 | 0.0 | 2.6 | 0.6 | 0.07 / 3.2 | 100 |

Reference policies (true Y): no_invest 27.1, early_invest 46.8, state_switch 47.1, calendar8 42.7, feedback_switch 44.6, overcommit 33.3, steady_networker 35.0, incumbent 43.4.

Oracle top 5 (true Y): 67.50, 67.48, 67.32, 67.16, 67.15.
