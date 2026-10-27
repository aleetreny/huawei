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

## Interpretation (written by hand after reading the numbers; a rerun of the CLI overwrites this file)

**Revision after review.** An earlier version of `no_diversity` changed three things at once: it limited every
operator to the one root family, moved the `new_family` weight to `refine`, and, when progressive widening left no
parent with room, returned no proposal. That left generation stalled in many blocks: at budget 8000 its generation
share was 16% against 35% for full, below the prereg minimum of 20% in 60 of 60 runs. The ablation now changes only
the root, drawing all 14 roots from one random family. Generation is exactly full's.

A second fix came out of the same check. In full, the reopen episodes that a new child triggers on a dormant parent
were charged against the block's generation quota. In one cheap_capability run this pushed the generation share down
to 18.6%. The quota now counts only spend on new candidates (`methods.GEN_PURPOSES`). Every number below comes from
a full rerun after both fixes. As a determinism check, best_of_n, refine_leader, racing, no_reopen and
partial_screening reproduced their earlier results exactly in all four settings. Neither fix changes their code paths.

Sensitivity runs reuse the same oracle. They are in `budget-2000/`, `budget-8000/` (R = 60 each, cheap_biased) and
`cheap-capability/` (R = 60, budget 4000). `decomposition.json` splits regret on replications 0-29 of this run into
two parts, using 500 truth games per policy:

- exploration: oracle minus the best policy the method ever proposed;
- selection: best proposed minus selected.

Paired true-Y differences (95% intervals over replications):

| setting | full − best_of_n | full − refine_leader | racing − full | no_diversity − full | partial_screening − full | no_reopen − full | no_specialization − full | no_calibration − full | target_only − full |
|---|---|---|---|---|---|---|---|---|---|
| budget 4000, R=100 | +1.4 [0.5, 2.3] | +3.1 [2.1, 4.2] | +0.5 [-0.4, 1.4] | -0.9 [-1.9, 0.2] | -2.0 [-3.1, -0.9] | -0.1 [-0.9, 0.6] | -0.3 [-1.0, 0.5] | +0.4 [-0.5, 1.2] | -0.1 [-1.0, 0.7] |
| budget 2000, R=60 | +1.1 [-0.1, 2.2] | +2.3 [0.7, 3.9] | +1.7 [0.3, 3.1] | -1.9 [-3.8, 0.1] | -2.1 [-3.9, -0.3] | -0.5 [-1.6, 0.7] | -0.5 [-1.7, 0.6] | +0.4 [-0.7, 1.5] | 0.0 [-1.1, 1.1] |
| budget 8000, R=60 | +1.8 [0.5, 3.2] | +3.2 [1.8, 4.7] | -0.6 [-1.8, 0.6] | -0.3 [-1.5, 1.0] | -1.1 [-2.4, 0.3] | -0.4 [-1.7, 1.0] | -0.1 [-1.2, 1.1] | +0.5 [-0.6, 1.5] | +0.4 [-1.0, 1.8] |
| cheap_capability, 4000, R=60 | +1.2 [0.2, 2.3] | +2.8 [1.3, 4.3] | +0.3 [-0.9, 1.5] | -0.4 [-1.8, 1.0] | -1.9 [-3.4, -0.5] | -0.3 [-1.6, 1.1] | -0.3 [-1.5, 0.8] | +0.5 [-0.6, 1.6] | +0.2 [-1.0, 1.5] |

What the evidence supports:

1. **Full beats the two simple baselines, by a small margin.**
   - Against best_of_n it gains +1.1 to +1.8 Y-points. The interval excludes 0 in three of four settings; at budget
     2000 it is +1.1 [-0.1, 2.2].
   - Against refine_leader it gains +2.3 to +3.2 in every setting.
   - It does this while spending 15% of its budget on confirmation that never helps selection.
   - Noisy hill climbing (refine_leader) is the worst method everywhere. It replaces the leader with lucky children,
     and its in-sample estimate overstates the truth by 4.2 to 7.5 points.
2. **Full does not beat racing.**
   - irace-style racing is level with full at budgets 4000 and 8000 and in cheap_capability. At budget 2000 it is
     ahead: +1.7 [0.3, 3.1].
   - Racing has no confirmation cost and explores more: 84 policies per run against 46 at budget 4000, and an
     exploration gap of 8.4 against 10.2.
   - The extra machinery in full does not pay for itself in the selected policy's true Y on this landscape.
3. **One component clearly helps: deciding on complete episodes instead of truncated proxies.**
   - Successive halving on month-12 truncated target episodes loses 1.1 to 2.1 points. The interval excludes 0 in
     three of four settings.
   - The decomposition shows why. partial_screening *proposes* policies as good as full's: best proposed 58.3
     against 57.3. But the proxy discards them, and the best policy that reached complete-episode evaluation had only
     54.9. Its selection gap of 4.4 is the largest of any method.
   - This is problem B (late benefits) reproduced in the testbed.
4. **Diverse roots: a small benefit that is not significant, and it shrinks with budget.** The earlier claim that
   removing diversity costs 1.2-2.4 points came mostly from the confounded ablation. Isolated, root diversity is
   worth:
   - +0.9 [-0.2, 1.9] at budget 4000;
   - +1.9 [-0.1, 3.8] at 2000;
   - +0.3 [-1.0, 1.5] at 8000;
   - +0.4 [-1.0, 1.8] with cheap_capability.

   Every point estimate favours diversity, but no interval excludes 0. The `new_family` operator rebuilds diversity
   during the search: no_diversity explores 3.0, 5.0 and 6.8 families on average at budgets 2000, 4000 and 8000.
   That is why the gap closes as the budget grows.

   Without diverse roots, the robustness refit also holds back more dormancies as inconclusive: 2.7 against 0.6 per
   run at budget 4000. Single-family cells are closer to each other, so the fits disagree more often.
5. **Reopening/audits, specialization and cheap-actor calibration show no detectable effect on the selected
   policy's true Y.** All their paired differences straddle 0. Concretely:
   - The audits are few (about 2.6 per run at budget 4000), and dormant policies rarely deserved better. Full's
     strict false-rejection rate is 3%.
   - The specialization gate (P(mu_spec > mu_parent + 4) >= 0.8) accepted 0.03-0.25 of 1.6-7.5 proposals per run,
     so it almost never ships a specialization.
   - Calibration granted pruning authority in 92-98% of runs, even with the biased cheap actor, so full behaves
     almost like no_calibration (+0.4 to +0.5, not significant). The calibration set is the diverse roots, where rank
     agreement is easy. Pruning acts on children near the leader, a different population. That violates the
     exchangeability assumption in `stats.calibration`'s docstring. The testbed shows no harm from it only because
     the cheap actors here preserve the rankings of good policies well enough.
   - Cheap screening as a whole (full against target_only) gains nothing: -0.4 to +0.1 for full.
6. **The clearest win is honest estimation.**
   - Full's fresh confirmation estimate is unbiased: bias -0.1 to +0.5, with every interval covering 0.
   - Every method that reports its selection data is optimistic: best_of_n by +1.7 to +3.6, refine_leader by +4.2
     to +7.5, and racing by +4.3 to +7.4.
   - Full also rejects fewer good policies. 8-10% of its dormant policies were within delta_t = 8 of the selected
     one, against 38-40% for racing. Racing's count includes irace's routine discard of non-elites at the end of each
     iteration.
7. **No method gets near the oracle at these budgets.**
   - P(within 2 of the oracle best, 67.5) is 0-3% for every method at every budget, and regret is 8.6-15.3 points.
   - The decomposition shows the gap is mostly **exploration**: oracle minus best proposed is 8.4-12.0 points, while
     selection loses 0.9-3.0 (4.4 for partial_screening). Selection losses at budget 4000 were 1.4 for full, 1.7 for best_of_n, 1.9 for
     refine_leader and 3.0 for racing.
   - Generation is the part this testbed emulates, so this result says the most about the operators and the least
     about an LLM orchestrator.
8. **Protocol observations for the protocol owner:**
   - After both fixes, the generation share after roots is 36-45% on average. Its minimum over all runs is 29%, and
     it never falls below the prereg 20% in any variant or setting.
   - A block can still fail to produce a new candidate if six proposals in a row are duplicates. That happened about
     once in 100 no_specialization runs and is now logged as `generation_stalled`.
   - The stagnation rule fired in 35-71% of blocks (52% at budget 4000), because a leader's posterior mean regresses
     downwards as it collects data. As written, it is close to "always on" at larger budgets.
   - The claim "finalist beats the incumbent" was confirmed in 78-98% of runs, because the incumbent (default theta,
     true Y 43.4) is weak.

Bottom line for the lab: keep complete-episode decisions and fresh confirmation, which delivers the unbiased estimate
and the honest claim. Keep diverse roots as a cheap default, but this testbed does not show they matter once
generation can draw new families. Racing on target alone would select as well at this cost ratio. The cheap actor,
audits and specialization machinery are not shown to help on SynthCareer. Treat them as safeguards whose value was
not demonstrated here, not as performance features. Generation quality, not allocation, limits every method.
