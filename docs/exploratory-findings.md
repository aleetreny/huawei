# Career Survival Simulator: exploratory findings and contributor handoff

Experiment date: 26 October 2026. Status: the four-hour batch finished at its configured time limit, with no error recorded by the harness.

## Executive summary

We completed **73,858 local sessions and 1,563,578 actions** using uniformly random available choices. None reached the full 48-month horizon. Average survival was **5.91 months**, and the average quantitative score was **11.78/100**.

Health exhaustion caused **54.83%** of recorded terminal outcomes and trust crises caused **41.38%**. Together they accounted for **96.2%**. These findings make health preservation and warning-driven risk assessment good initial hypotheses for Skill design. They do not establish an optimal strategy or a fixed ranking of decision priorities.

The experiment did **not** use a reasoning model, run submitted Skills, consume competition API credit, or measure official competition performance. More random runs are now lower priority than testing a compact reasoned strategy.

## 1. Purpose and scope

Before the competition key was available, we wanted a concrete baseline answering:

- How long does indiscriminate play tend to survive in the installed development configuration?
- Which terminal outcomes occur most often under that behavior?
- Which aspects of a future strategy deserve explicit testing?
- What can we learn through the supported interface without inspecting internal package data?

We did not attempt to recover hidden formulas, promotion thresholds, failure counters or event probabilities. We did not build a catalogue of event-specific answers.

This document is research context for contributors. It is not an agent Skill and should not be copied wholesale into a competition submission.

## 2. Method

### Environment and interface

The installed environment used Python 3.13, `career-emulator-engine` 1.0.6, `career-emulator-techarena` 1.0.8 and FastMCP 4.1.3. The development dataset was loaded using the engine's public update command.

The experiment sent requests through the local Career Lab adapter, which called the official MCP server. For each session it used `new_game`, `observe`, `take_action` and `check_latest_logs`. The UI also supports the public `show_employee_handbook` tool. No direct package internals or simulator database were used to make decisions or retrieve results.

This was a random interface-exploration harness, not a JiuwenSwarm submission. A future benchmark of competition Skills must use JiuwenSwarm **0.2.4b3**, single-agent mode and the designated model under the official setup. This standalone environment does not replace that setup.

### Decision procedure

For each fresh session:

1. Observe the state and currently available choices.
2. Sample one available choice uniformly at random.
3. Submit it with a note identifying the action as random exploration.
4. Repeat until no choices remain.
5. Read the terminal state and recent official logs, including the ending score.
6. Update aggregate results.

Every available choice was eligible, including poor options and any finish/skip choices exposed by the simulator. Uniform sampling of individual choices does not imply equal exploration of whole strategies or career paths. The procedure did not interpret event wording, respond intelligently to warnings or optimize quarterly resources.

Choice sampling used a separate Python random seed of `7_000_000 + run_index` for each session, with zero-based indexing. This controlled choice sampling only. Simulator event generation was neither seeded nor paired by the harness; identical future trajectories are not guaranteed.

### Duration and accounting

The initial request was one million sessions. It was changed to a time budget, first three and then four hours. The process was stopped and resumed to apply those changes while preserving aggregate counters. The final measured experiment elapsed time was **14,400.19 seconds**; brief configuration pauses were outside that accumulated runtime.

The main batch contains **73,858 sessions**, not one million. A separate **30-session pilot** preceded it and is excluded from all main-batch totals below. Do not add pilot results to the main summary without treating them as a distinct batch.

The harness recorded no execution error, and all recorded terminal labels were failures. This is not an independent audit of every engine transition. Survival months were parsed from the ending-score message, with current-month state as a fallback; the aggregate does not retain a fallback-use count. Scores were parsed from the reported quantitative score, and the score count equals the completed-session count.

## 3. Main results

| Metric | Result |
|---|---:|
| Finished sessions | 73,858 |
| Submitted actions | 1,563,578 |
| Accumulated elapsed time | 14,400.19 seconds |
| Mean throughput | 5.129 sessions/second |
| Sessions reaching month 48 | 0 |
| Mean reported survival | 5.9056 months |
| Minimum reported survival | 1 month |
| Maximum reported survival | 24 months |
| Sessions with a parsed score | 73,858 |
| Mean quantitative score | 11.7842/100 |
| Minimum quantitative score | 3.1/100 |
| Maximum quantitative score | 28.9/100 |

The maximum score and maximum survival are separate aggregate statistics; we cannot claim they came from the same session.

### Terminal outcomes

| Recorded outcome | Sessions | Share |
|---|---:|---:|
| Blackout: health exhaustion | 40,496 | 54.830% |
| Trust crisis | 30,559 | 41.375% |
| Broke | 2,430 | 3.290% |
| Relationship-related resignation | 359 | 0.486% |
| Obsolete | 12 | 0.016% |
| Dismissed for capability | 1 | 0.001% |
| Breakdown | 1 | 0.001% |
| **Total** | **73,858** | **100% before rounding** |

The outcome categories use the terminal reason supplied by the simulator. Each session contributes one final label; this does not measure every contributing weakness or warning that preceded elimination.

## 4. What the evidence supports

### Health and trust failures dominate random play

These categories account for 71,055 of 73,858 outcomes. A first reasoned strategy should explicitly assess workload sustainability and organizational risk feedback. This is a prioritized experiment hypothesis, not proof that protecting these dimensions always dominates career growth.

### The random baseline is weak

No run reached 48 months, and the longest reached 24. Random sampling routinely selects choices that a reasoning agent might reject immediately. Therefore these numbers cannot stand in for the performance of a model without Skills.

### Surviving and scoring are distinct goals

The simulator assigns a quantitative score even to early exits. In the separate pilot, the highest score came from an early exit at month 3. That observation motivates reporting survival alongside score; it does not establish the relationship between those metrics across the main batch, whose trajectories were not retained.

### Rare failure labels do not establish low importance

Most sessions ended early from health or trust problems. Other weaknesses may need longer to produce a terminal outcome. This competing-risk effect means the observed failure frequency is not a ranking of how much each statistic matters to a successful four-year career.

## 5. Local scoring information and its boundaries

The published documentation lists career level, wealth, health and dignity, skill, risk control and network as ending dimensions. During the separate 30-session pilot, official ending-score log entries consistently exposed the following local weights:

| Dimension | Weight observed in pilot ending reports |
|---|---:|
| Career level | 30% |
| Total wealth | 20% |
| Health and dignity | 15% |
| Professional skill | 15% |
| Risk control | 10% |
| Workplace network | 10% |

These are observations of that installed development configuration. We did not retain per-dimension weight data for the main batch, so do not describe this as a 73,858-run verification of the weights. They do not establish official evaluation weights, hidden scoring formulas or marginal value per statistic point.

For example, a dimension weight of 30% does not tell us the benefit of one promotion: that would require knowing its score transformation and other consequences. Output is not listed as a separate ending dimension, but the public rules describe its role in performance and promotion, so it can still matter indirectly.

Do not encode these development observations as guaranteed rules in submitted Skills. Prefer public guidance and current-run feedback.

## 6. Candidate Skill responsibilities

Start with a compact, coherent Skill. The following responsibilities can initially be sections rather than separate files:

| Responsibility | Intended behavior | Evidence needed next |
|---|---|---|
| State assessment and risk triage | Read visible state and warning feedback; identify urgent deterioration before discretionary growth | Fewer avoidable early failures under a reasoned policy |
| Event decision-making | Compare immediate benefits, future liabilities and available alternatives in context | Better survival and career outcomes across changing events |
| Quarterly planning | Allocate available Energy and the main action according to weaknesses and goals | Improved outcomes versus the same strategy without explicit planning |
| Review and adaptation | Use performance reviews and observed consequences to revise priorities over time | Recovery after setbacks and progress over later career stages |

Avoid invented numeric safety thresholds presented as engine rules. Decisions should be based on the public handbook, current state, available options and current-run feedback. A successful approach must adapt when wording, event order and parameters change.

## 7. Limitations and unanswered questions

- **No reasoned comparison:** we have not measured an AI baseline, a Skill improvement or a winning strategy.
- **One development configuration:** the official dataset and parameters may differ.
- **No paired scenarios:** different runs may encounter different events, so differences cannot be attributed to a specific policy change here.
- **Limited late-game exposure:** early elimination prevents useful conclusions about sustained high-level careers.
- **Aggregate-only main batch:** no per-run histogram, score variance, median survival, trajectory reconstruction or survival/score correlation is available from the committed summary.
- **No causal action analysis:** we cannot say which individual choices caused aggregate changes or were best.
- **No official efficiency benchmark:** zero competition API use means model token efficiency was not measured; local throughput is not the scored token-efficiency component.
- **No guaranteed transfer:** large sample size reduces uncertainty about this random behavior in this setup; it does not fix the mismatch with a reasoned competition agent.

## 8. Recommended next experiments

Once the competition key is available:

1. Set up the official participation repository with its exact dependency pin and designated model. Keep single-agent mode.
2. Define a reproducible reasoning baseline, then a compact Skill version. Record the exact manifest, instructions and version used.
3. Run multiple independent sessions per version. Three is a practical initial check, not evidence of statistical certainty.
4. Compare the baseline with one change at a time: health guidance, warning interpretation, or quarterly planning.
5. Track quantitative score, survival months, ending contributions, failure reasons, reviews and token usage. Preserve enough permitted run output to explain failures.
6. Report mean and variability, not only the best run. Keep the model and environment constant where possible.
7. Expand testing only when it answers an unresolved question. Do not spend the key budget on another large random batch.

Useful hypotheses include whether warning-driven risk assessment improves survival, whether explicit quarterly planning reduces avoidable resource waste, and whether growth becomes more effective after early survival problems are controlled. None has been established by this experiment.

## 9. Evidence and repository navigation

- [Main aggregate summary](experiments/random-baseline-summary.json): the final checkpoint, including exact counters and outcome labels.
- [Experiment plan](experiment-plan.md): proposed workflow for testing Skills.
- [Career Lab setup](../tools/local-game/README.md): the manual browser interface.

Detailed pilot outputs and local runtime data are not committed. The main batch retained aggregate checkpoints rather than a separate exported trajectory for each run. The summary permits checking counts and reported aggregates, but it is not sufficient to independently replay the experiment. Do not claim a full reproducibility package exists.

When joining the project, read this report, reproduce the manual interface if useful, and implement the next controlled experiment. Do not treat the random baseline as a validated decision policy.

## 10. Official references

- [Public handbook](https://techarena-career-sim.readthedocs.io/en/latest/handbook.html)
- [Public rules](https://techarena-career-sim.readthedocs.io/en/latest/rules.html)
- [Failure and ending evaluation](https://techarena-career-sim.readthedocs.io/en/latest/failure-and-ending.html)
- [Competition rules and fair play](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html)
- [Submission requirements](https://techarena-career-sim.readthedocs.io/en/latest/submission.html)

Read the current rules before development. These notes do not certify that any future automation or submission is compliant. Do not inspect internal datasets, memorize event-to-answer mappings, manipulate run artifacts or present unpublished thresholds as known rules.
