# First-review promotion: black-box branch investigation

26 October 2026. Matteo requested a search over the first six career months on his existing branch, including every encountered question, alternatives and delayed consequences. This report is private development research, not submission material.

The useful finding is a combination of **timing, balanced realised growth, dignity, and continued risk/health management**. There is a strong empirical promotion pattern, but no demonstrated universal policy for arbitrary agents or unseen histories.

## Results

There are **1,961 resolved six-month experiments**, plus **31 recorded technical interruptions**, in five archived batches. A resolved experiment either dies within the window or reaches the first observation of month 7 without taking a month-7 action. This is not 1,961 complete 48-month careers.

| Batch | Resolved | Technical interruptions | Promoted at first review | Alive after month 6 | Promoted AND alive |
|---|---:|---:|---:|---:|---:|
| Factorial discovery | 864 | 0 | 64 | 260 | 40 |
| Frozen learned research policy | 512 | 0 | 336 | 468 | 328 |
| Public quarterly action coverage | 293 | 31 | 8 | 84 | 5 |
| Reserve-energy confirmation | 36 | 0 | 2 | 10 | 0 |
| Targeted narrative frontier | 256 | 0 | 16 | 125 | 11 |

The learned research policy promoted **65.6%** of fresh episodes (Wilson 95% interval 61.4–69.6%) and both promoted and survived the window in **64.1%** (59.8–68.1%). Overall survival was 91.4%. These intervals describe this development policy and pool, not official competition performance. The policy uses an empirical action-effect lookup learned from discovery plus manually specified gap, health and concealment penalties. It is not the general prose rule and is unsuitable as a submitted event-answer manual. These are fresh histories from the same event pool, not held-out narrative families or actor-matched evaluations of a new Skill.

## Findings and their evidential limits

### 1. The operational deadline is earlier than a literal reading of the quarterly schedule suggests

All **1,379 recorded first-review transitions** occurred while the clock changed **5 → 6**. The month-6 energy and main actions came later. Every recorded first review had grade **C**, including promoted careers. Thus the first promotion does not require an observed B or A in this development configuration.

There were 108 factorial episodes and 107 learned-policy episodes still at L1 with Skill/Network/Output 9/3/3 at the final observation. End-of-window growth is too late to explain the earlier decision. Review timing must be read from transitions and logs, not inferred from final stats or from the name of the quarter.

### 2. Realised growth repeatedly stalls; nominal positive effects can be wasted

The factorial batch contains 720 quarterly positive Network investments with no realised gain while Network was 3, 485 positive Output investments with no realised gain while Output was 3, and 190 positive Skill investments with no realised gain while Skill was 9. These counts exclude level-changing transitions.

Earlier observations in the same runs can exceed Network 3 and Output 3. Therefore this is **not evidence of an unconditional, game-wide range limit**. The repeated plateaus are consistent with an early-career clamp or another settlement rule; its implementation was not inspected. The general response is to observe actual gains, fill another gap, and preserve health/risk capacity instead of repeatedly buying the same stalled increase.

### 3. A compact numerical separator describes the observed clean review transitions

For research only, the following **post-transition pattern** classified all 1,122 review transitions without a same-transition “Old landmines” or “Trust crisis” message:

> Skill ≥ 8, Network ≥ 3, Output ≥ 3, and Dignity ≥ 2.

There were **370 positive predictions, all promoted**, and 752 negative predictions, all unpromoted. This includes all five batches. The initial factorial pattern alone was not enough: learned-policy runs 78 and 186 reached 9/3/3 but did not promote, with dignity 1 and 0 respectively. They show why growth-only advice misses a relevant dimension. See `learned-v2/reviews.json` and the complete trajectories for those cases.

This is an empirical separator, **not a recovered promotion formula, an exact causal threshold, or an ex ante guarantee**. It uses observations after settlement. Hidden state may jointly affect those observations and the decision; the clean subset excludes difficult transitions. Do not put these unpublished numbers into submission Skills. The audit is in [numeric-hypothesis-audit.json](numeric-hypothesis-audit.json).

### 4. Review, promotion, risk settlement and death can share one action response

Across the archived batches, **426 episodes promoted; 42 of these died before the end of the window**. In 53 promoted episodes, the review transition also reported an old-risk explosion. Some promoted careers immediately displayed Output 0 after the explosion. That is not proof that zero output satisfies promotion: the notice and subsequent penalties are bundled into one public response.

The valid operational aim is “promoted and still able to continue”, not just seeing L2 once. Recover before capacity is exhausted, resolve accumulated exposure, and track delayed obligations. A single observed delta can include the chosen answer, automatic review, bonuses, clipping, risk penalties and failure checks. It must not all be attributed to the selected answer.

### 5. A named sponsor or special scenario has not been shown to be necessary

Promotions appear across different scenario histories, different quarterly actions and with different support narratives. The support-message classifier is intentionally incomplete: absence of a recognised phrase is not absence of hidden support. Mentor, peer, senior-colleague and manager interventions can be feedback about latent conditions, automatic help, or mechanics; observations do not establish which.

In the controlled learned-policy batch, the main-action arms were assigned before play and balanced across energy policies: mentorship promoted 89/128, key project 88/128, and no main action 78/128. These exploratory differences do not establish a single mandatory main action or a separate hidden sponsorship effect. The actor remained the same empirical bot; the game histories were unseeded and unpaired.

Likewise, recovery-heavy energy gave 92/128 promotions and 116/128 survivors; risk-heavy energy gave 76/128 promotions and 122/128 survivors. Recovery, growth and risk cleanup have opportunity costs. “Always defend” and “always produce” are both incomplete rules.

## Scenario catalogue and causal bookkeeping

The merged catalogue contains **89 narrative titles, 212 distinct narrative questions/stages**, and **503 exercised answers out of 508 encountered narrative alternatives** (99.0%). Including public quarterly/document nodes: 215 nodes and 521/526 answers. All encountered public quarterly action labels were exercised. This covers the action menu, not every energy-action order, every cross-quarter combination or every full narrative history.

- [Readable question/answer catalogue](catalogue.md): full question text, every displayed option, counts, observed changes, later same-title stages and evidence IDs.
- [Machine-readable catalogue](questions.json): observed delta distributions, immediate successors, possible delayed chains, example states, episode associations and explicit untried alternatives.
- [Coverage overview and remaining frontier](overview.json): the five untried narrative alternatives, spanning four rare stages. Targeted exploration reduced the frontier but did not close it.
- Each batch contains `observed-edges.csv`, `reviews.json`, `quarterly-effects.json`, `summary.json`, `manifest.json`, and a lossless `public-trajectories.jsonl.gz` archive with SHA-256.

An evidence ID is `batch/run/step`, using the zero-based `run` and step in the archived record. Every raw step retains the whole before-observation with **all available answers**, the chosen answer, action response, application flag and whole after-observation. Final public logs are retained. The catalogue includes episode promotion/failure associations but does not call them individual-answer causal effects.

`observed_next_question` edges include randomly drawn subsequent stories. `same_title_later_possible_chain` edges indicate likely narrative continuation. Neither is a proven counterfactual effect. Visible question identity intentionally does not identify the full hidden state. There is no cloning, rewind or simulator-seed parameter among the five public tools, so a genuinely exhaustive state-tree search is not available through this interface. Seeds here control only bot choices and shuffled policy schedules.

The causal working model is: choices change visible resources and possibly latent obligations/exposure; subsequent scenarios and automatic settlements respond to that history; the review uses its then-current inputs; risk and failure checks may subsequently change the same public response. The exact latent links remain hypotheses. We have policy-level interventions and detailed sequential evidence, not a complete causal identification of the engine.

## General rule to evaluate next

[general-rule-draft.md](general-rule-draft.md) contains the transferable prose version, with no event titles, answer indices, hidden numerical cutoffs or prescribed months:

> Build capability, collaboration and credited delivery together before the actual review boundary; keep dignity and health viable; close promises and emerging risks; verify realised gains and redirect effort when growth stalls.

The learned bot's 65.6% result must **not** be attached to this prose. Transfer to DeepSeek or another agent requires fresh actor-controlled tests with only the prose and official tools. No candidate was added to the policy race or registered in the cloud.

## Reproduction and isolation

Run from the repository root using its pinned virtual environment. Use a fresh output directory for every batch. Raw server storage is outside Git and outside the default/cloud registry. Do not read the server databases or emulator files. All engine data used in the analysis came from the five public tools.

```sh
.venv/bin/python scripts/first_review_search.py --output /absolute/isolated/path/discovery --runs 864 --workers 4 --seed 261026 --story first,uniform,coverage --energy balanced,reports,network,recovery,risk,skill --main project,report,mentor,none
.venv/bin/python scripts/first_review_search.py --output /absolute/isolated/path/learned --runs 512 --workers 4 --seed 270026 --story learned --energy adaptive,reports,recovery,risk --main adaptive,project,mentor,none --training /absolute/isolated/path/discovery
.venv/bin/python scripts/analyze_first_review.py /absolute/isolated/path/discovery /absolute/report/path/discovery
.venv/bin/python scripts/analyze_first_review.py /absolute/isolated/path/learned /absolute/report/path/learned
.venv/bin/python scripts/catalog_first_review.py /absolute/report/path
.venv/bin/python -m pytest -q
```

Environment: engine 1.0.6, development dataset 1.0.8, FastMCP 2.14.7, competition mode, monthly event limit 3, active long-chain limit 1, note-length limit 1000. Each experiment has its own server process and database because competition mode permits one new game per process. Four concurrent non-LLM workers were used. No model API, paid credits, Claude subscription or central queue was used by this investigation.

The learned model is archived in `learned-v2/frozen-effect-model.json`, SHA-256 `3b5473ee9c7c67c48160648064c58310d104623bd86543781243f5cbce6b8006`. It was frozen from the 864 discovery records before the 512 evaluation episodes. Source snapshots are retained for the later coverage/frontier launches; the first two launch snapshots were not saved separately, and the final script retains their decision rules. Exact game trajectories are not reproducible without simulator seeds. Use the archives for exact evidence.

## Relevo

Implemented `scripts/first_review_search.py`, `scripts/analyze_first_review.py`, and `scripts/catalog_first_review.py`, plus regression tests for the early review boundary, window stopping, interrupted/rejected actions, public skip labels and visible-question identity. Completed the five batches above and stopped all workers. The complete public-response evidence, catalogue, provisional numeric audit and general prose draft are in this directory. Central registries, frozen protocol, existing candidate Skills and other branches were not modified.

Validation: **232 tests passed** in 17.14 seconds, with the existing Authlib deprecation warning. Independently verified all five gzip archives against their SHA-256 files, parsed every archived record, reconciled batch counts, and checked the merged catalogue's 503 exercised narrative answers and five unanswered alternatives.

Technical failures are retained, not scored as failed games: the initial smoke attempted multiple games in one competition process; a 145-record exploratory batch was stopped after discovering an incorrect “No action” label; a four-record learned smoke preceded semantic/risk handling refinements. Those pilot records remain outside Git at `/Users/matteozabban/careerlab-data/matteo-first-review/` and are excluded from the five-batch totals. In the archived public-action batch, 31 reserve-energy attempts stopped on the incorrect skip label. The label was corrected, covered by a regression test, and a separate 36-episode confirmation batch completed without that error. Aborted sessions are not resumed or mistaken for zero scores.

Raw per-session JSON, server storage and pilot records remain under `/Users/matteozabban/careerlab-data/matteo-first-review/`; the public-tool trajectory archives in this report preserve the analysed evidence without engine internals. Rebuild the catalogue with the command above. The next concrete investigation is an actor-controlled evaluation of the prose rule, with distinct promotion and survival outcomes, followed by ablations of realised-gain checks, dignity protection and obligation tracking. A universal first-promotion guarantee is not established; the empirical frontier and hidden-state counterfactuals remain open.
