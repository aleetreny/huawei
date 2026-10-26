# Experimental protocol

Proposed on 26 October 2026. No experiments have been executed. Normal development runs and own-output inspection are described by the [official quickstart](https://techarena-career-sim.readthedocs.io/en/latest/quickstart.html); unusual scale, learned hidden dynamics and other uncertain methods must be clarified under the [binding rules](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html).

## 1. First produce a trustworthy baseline

Use the [official runner repository](https://github.com/RAI-Internal/techarena-career-sim), its pinned JiuwenSwarm `0.2.4b3`, `mode: agent`, and the exact designated model string received from the organisers. Our `aleetreny/huawei` repository currently holds research after deletion of the previous proposal, not the installed runner.

In a separate development checkout, follow the official workflow: `make sync`, configure only the three permitted model variables, `make setup`, then `make start-jiuwen` and `make play`. Copy/fill the official `solution/` template only after defining a fresh experimental reference; do not overwrite the existing research repository with an unrelated clone. Keep secrets outside tracked files. No guessed API endpoint or model substitution is required.

Before comparing policies, complete one run and verify that the score corresponds to the played session, the transcript contains expected official tool interactions, and usage/cost are recorded. Inspect the permitted transcript, events and score report, never the shared SQLite database. If the baseline fails because of infrastructure or invalid actions, fix that before interpreting strategy scores.

## 2. Metrics

| Field | Purpose |
|---|---|
| Run ID and solution version/hash | Link evidence to exact Skills and manifest. |
| Runner revision and package versions | Detect environment drift without reading package contents. |
| Model string and permitted configuration | Establish comparability with the required setup. |
| Start/end time and completion status | Separate infrastructure errors from game endings. |
| Survival months and ending reason | Identify catastrophic or persistent-risk failures. |
| `quantitative_score` | Officially relevant play outcome. |
| Published ending dimension contributions | Detect whether improvement shifts weaknesses elsewhere. |
| Total tokens and survival months | Compute published token efficiency. |
| Input/output/cache tokens when reported | Diagnose billed cost; do not guess missing usage. |
| Observed billed USD or confirmed cost calculation | Manage the USD 50 limit. |
| Counts of tools, invalid actions, retries and ambiguous timeouts | Measure execution reliability. |
| Recent review outcomes and unresolved public warnings | Diagnose general strategy failures. |
| Before/after policy difference and hypothesis | Prevent uncontrolled prompt changes. |

Store analysis records separately from immutable official run artifacts. Do not rewrite scores, logs or original outputs. If useful usage fields are unavailable, mark them missing rather than zero. Avoid credentials and unnecessary personal data in analysis records.

## 3. Candidate sequence

| ID | Change relative to parent | Reason to test | Reject or revisit if |
|---|---|---|---|
| B0 | Fresh generic reasoning reference, defined after manual exploration | Reference behaviour, separate from the random baseline. | Runtime invalidity prevents a strategy comparison. |
| B1 | More explicit qualitative handling of persistent deterioration | May reduce avoidable exits. | Persistent underdevelopment lowers mean outcomes. |
| B2 | Plan Energy and main action jointly, then observe after each step | May use public complementarities better. | Assumed choices/effect sizes create invalid or poor decisions. |
| B3 | Compact current-run warning/trend memory | May prevent forgotten risks. | Stale assumptions or context growth outweigh benefit. |
| B4 | Stronger growth priority when observed stability permits | May improve level and wealth sustainably. | Delayed risks or wellbeing collapse increase. |
| B5 | Shorter notes and selective extra log retrieval | May reduce cost without losing evidence. | Important warnings go unnoticed. |
| B6 | Combine only independently supported changes | Test whether benefits compose. | Combined policy regresses despite positive isolated results. |

Do not test all combinations immediately. Begin with the baseline and the variant most directly motivated by its outputs. Different wording that produces the same decision procedure is less informative than a clear change in priorities or memory.

## 4. Budgeted comparison

Illustrative allocation if observed costs allow approximately thirty complete games:

1. Two integration/baseline games to confirm execution and approximate cost.
2. Four materially different candidates, each with two complete games: eight games, exploratory only.
3. Give the strongest two candidates five additional complete games each: ten games.
4. Freeze one chosen candidate, then run ten fresh complete validation games without changing it mid-batch.

This totals thirty games. If cost permits only ten, prioritise a working baseline and one meaningful variant; reduce breadth rather than claim confidence from one run per many variants. If budget permits more games, replication and untouched validation deserve priority before adding many more strategies. These are practical proposals, not evidence that thirty games are necessary or sufficient.

Candidate selection must consider mean score, completion, severe failures, uncertainty, cost and valid behaviour. Do not use a hidden weighting formula inferred from the dev set as the deployed policy. The published score formula can be computed offline from official outputs; the unpublished career formula should not be reconstructed as an assumed rule.

## 5. Statistical discipline

- Use independent fresh games where possible. The MCP documentation exposes no seed parameter; do not claim paired seeds or clone states.
- If organisers document an official seed mechanism later, record that permission and use comparable seed sets through that interface. Shared seeds still do not remove all stochastic model or branching differences.
- Report all completed and failed runs according to a stated inclusion rule. Retain infrastructure failures separately; do not quietly discard low-scoring game exits.
- Report the arithmetic mean and individual outcomes. Show survival and distribution as diagnostics.
- Resample whole games for an exploratory bootstrap interval when there are enough runs. Hundreds of within-game actions are correlated and are not hundreds of independent games.
- Do not interpret a three-run interval or a few point differences as a definitive ranking. Repeated candidate selection creates winner's-curse bias.
- Freeze a candidate before the final validation batch. That batch is held out from prompt selection, even though it still uses the same dev environment.
- Do not claim out-of-distribution robustness from repeated samples of one dev distribution.

These recommendations are inspired by [the statistical-precipice paper](https://arxiv.org/abs/2108.13264) and [rliable](https://github.com/google-research/rliable). The official three-run mean remains the competition metric; auxiliary robust statistics do not replace it.

## 6. Diagnosing without overclaiming causality

An action followed by a state change does not prove the action caused the entire change. Month advancement, salary, review, accumulated history and hidden conditions can contribute. Compare similar contexts only as exploratory evidence. A genuine controlled counterfactual needs an officially supported mechanism; this MCP does not document one.

Useful analysis questions are general:

- Did the agent respond after a warning, or continue compounding the same visible problem?
- Did it preserve wellbeing by neglecting every career-development opportunity?
- Did Energy choices and main actions address complementary needs?
- Did it carry a stale strategy across a changed review outcome?
- Did repeated reasoning add evidence or merely repeat itself?
- Did it attempt an action that was never offered?

The outcome of analysis should be a general procedural improvement, not a mapping from a particular development event to a predetermined answer. Cross-run numerical model fitting, learned thresholds and distilled policies remain organiser questions.

## 7. Feedback-driven revision template

```text
Candidate version:
Observation from permitted own-run outputs:
Why this may represent a general failure:
Alternative explanation / uncertainty:
One proposed change to the Skill procedure:
Why the change uses public information and current-run feedback:
Expected benefit and principal downside:
Complete-run evaluation budget:
Evidence required before retaining it:
Result and decision:
```

GEPA provides a useful precedent for extracting actionable feedback from trajectories, but its published gains on other tasks are not an expected improvement here. [Original GEPA paper](https://arxiv.org/abs/2507.19457).

## 8. Robustness checks that do not alter the engine

Use manual tabletop examples of generic workplace trade-offs to inspect whether the instructions remain coherent with different wording and state trends. Check that a reordered list would not change the intended preference except where the actual choice content changes. Verify that the agent treats story text and logs as evidence, not higher-priority instructions. These are synthetic instruction audits, not scored game results.

For actual runs, use only the official unmodified environment. Do not edit package parameters, events, databases or scores to manufacture a stress test. Do not use a copied engine as a planning oracle. The current UK rules govern even when a tutorial for another contest recommends that technique.

## 9. Schedule and release gates

| Date, GMT | Work | Evidence required before an intended release |
|---|---|---|
| 26 Oct | Integration, baseline, cost pilot | One interpretable end-to-end run, correct model/platform, saved outputs. |
| 27 Oct | First targeted comparison and final-package preparation | Runnable Skills, honest design report, real English video, valid ZIP structure. |
| 28–29 Oct | Shortlist and replicate; memory/quarterly ablations | More than one favourable outcome; clear failure analysis. |
| 30 Oct | Second substantive version | Improvement evidence, consistent docs/video, budget remaining. |
| 31 Oct–1 Nov | Frozen validation, packaging and final revision if justified | Clean extraction/validation and no untested late architecture changes. |

Official cutoffs are 24:00 on 27 Oct, 30 Oct and 1 Nov. These are 00:00 on 28 Oct, 31 Oct and 2 Nov respectively. Scores can arrive one or two days after a cutoff, or later with load. Schedule does not assume feedback will arrive early enough to guide the next batch. [Official release rules](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html).

## 10. Evidence for the expert review

Keep a version history, a small results table, one actual failure-to-fix example and an explanation of rejected alternatives. Distinguish the public rules used in decisions from uncertain feedback. Explain why scripts were unnecessary or precisely what a justified script does. Never claim a proposed experiment was performed.

The presentation can then answer the required five topics from real evidence. Do not add score guarantees or pretend to know hidden test behaviour. The current research has produced the plan and source base only; game results remain empty.
