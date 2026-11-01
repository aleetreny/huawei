# Known six-month catalogue: 100% answer coverage

Matteo requested closure of the known answer frontier on 26 October 2026. **Every answer currently present in the encountered six-month catalogue now has a verified successful execution.** This closes the original five missing answers and the additional gap exposed during the search.

| Coverage | Before | After |
|---|---:|---:|
| Narrative question stages | 212 | 213 |
| Narrative answers executed / encountered | 503 / 508 | **510 / 510** |
| All answers, including document and quarterly menus | 521 / 526 | **528 / 528** |
| Untried known answers | 5 | **0** |
| Narrative titles | 89 | 89 |

The 100% denominator is the **currently encountered question/answer catalogue**, not all random histories, hidden states, action orders, causal effects or unseen scenarios. Each answer has been exercised at least once in a particular state; different states can still change its effects. Consequences after the six-month boundary remain outside this experiment.

## Search and evidence

The original input catalogue was copied and hashed before the search, so closing its five holes cannot be confused with changing the denominator. A targeted controller followed observed same-title narrative routes, selected each missing answer explicitly, and otherwise used a public-response-trained survival fallback. A separate exploratory cohort intentionally lowered dignity while preserving health to reach rare retention scenarios. These are research interventions, not recommended playing policies or submission Skills.

Batch `known-closure-1` completed **592 fresh six-month episodes**, closing all five original gaps. It also encountered a previously unseen stage of an existing expense-claim story. Batch `known-closure-2` completed **5 episodes** and exercised its remaining alternative. No further question stages were encountered in that second batch. Both stopped launching games as soon as their frozen targets were closed; already-started games finished their window.

There were **597 new resolved experiments, zero technical interruptions**, comprising 459 survivors through month 6 and 138 game eliminations. No LLM, model quota, API credit, cloud registry, simulator internals, state cloning or simulator-seed control was used. The queued prose-versus-manual Haiku comparison remains separately prepared for manual resumption; this work did not start it.

| Gap closed | Evidence ID (`batch/run/step`) |
|---|---|
| Graduate mentoring: decline | `known-closure-1/83/20` |
| Retention package: accept the rise immediately | `known-closure-1/97/21` |
| Retention package: stay while quietly continuing the search | `known-closure-1/588/20` |
| Redundancy leak follow-up: deny the disclosure | `known-closure-1/246/21` |
| Recurring palpitations follow-up: continue working | `known-closure-1/485/22` |
| Newly encountered expense-audit follow-up: defend the claim as team custom | `known-closure-2/2/22` |

All six were accepted by the official `take_action` tool with `success: true`, without an ambiguous reply, and with a recorded after-observation. Their exact public texts, visible states, feedback and episode outcomes are in each batch's `closed-targets.json` and lossless archive. Some alternatives are intentionally harmful: execution is coverage, not endorsement. For example, the recurring-palpitations witness ended in a trust crisis in the same response, which also included other settlement effects; that is not an isolated estimate of the answer's causal effect.

## Independent audit

[coverage-audit.json](coverage-audit.json) independently reads and hashes all **seven lossless public-response archives**, covering **2,589 retained records**. This total includes the 31 previously documented technical interruptions; there are **2,558 resolved experiments** overall. The audit reconstructs question identities from raw before-observations and demands a successful, non-ambiguous, applied action inside months 1–6 for every displayed option in the current catalogue. Merely seeing an option, attempting it, or recording a rejected action cannot satisfy the audit.

The audit found **528/528 witnesses**, including **510/510 narrative witnesses**, and zero missing pairs. It includes a batch/run/step witness and before/after states for every answer. The current catalogue SHA-256 is `929a322de590cb04578abdbf06fb54bee49e891acb0aab27257ed6013dabcd1b`.

Current readable catalogue: [catalogue.md](../first-review-search/catalogue.md). Current coverage and empty frontier: [overview.json](../first-review-search/overview.json). Machine-readable question graph: [questions.json](../first-review-search/questions.json). The previous promotion-pattern statistics remain results of their original frozen batches; closure runs deliberately explore poor actions and are not a comparable policy-performance sample.

## Relevo

Implemented `scripts/close_known_frontier.py` for state-aware targeted closure and `scripts/audit_known_catalogue.py` for independent verification from public-tool archives. Added tests proving that unexecuted or rejected choices cannot close a target, new nodes do not silently change the frozen denominator, narrative routes use same-title evidence, and corrupted archives fail verification. Updated the merged catalogue and Matteo's T4 line. The simulation workers have stopped; no automatic exploration is running.

Validation: **249 tests passed** in 17.50 seconds, with the existing Authlib deprecation warning. Independent archive audit passed with 528 successful non-ambiguous witnesses and zero missing answers.

Exact input catalogues, runner snapshots, environment settings, coverage status, closure witnesses, edges, review extracts and lossless public trajectories are archived under `lab/reports/first-review-search/known-closure-1/` and `known-closure-2/`. Full per-session public-response JSON and server storage remain outside Git at `/Users/matteozabban/careerlab-data/matteo-known-closure/`. No engine database was read by the research code.

Rebuild and verify from the repository root:

```sh
.venv/bin/python scripts/catalog_first_review.py lab/reports/first-review-search
.venv/bin/python scripts/audit_known_catalogue.py lab/reports/first-review-search lab/reports/known-catalogue-closure/coverage-audit.json
.venv/bin/python -m pytest -q
```

The requested known-catalogue closure is complete. Further work would test the general rule with an actual reasoning agent, or separately search for previously unseen stages; neither is required to claim the narrowly defined answer coverage above.
