# observed-growth-v7: eight Haiku episodes, 7 completed, mean Q 61.27

## What v7 is

v6's rules (from the promotion study, [matteo-promotion-study.md](matteo-promotion-study.md)) rewritten in the status-line format of `f1-status-line-v1`, and shorter: 455 words against v6's 711. Policy `ce54d3c2f15b3179`, parents `observed-growth-v6` and `f1-status-line-v1`, lint clean. Before every choice the actor fills `Review: near or far | Below best: <stats or none> | Risk: calm or raised | Health: ok or low`, where "Review near" means the next review comes before the next quarter-end allocation (reviews are applied at the start of their month), and "Below best" lists Skill, Network or Output under their best value at the current level. Story choices guard Network and Output when a review is near; the quarter-end allocation is ordered: Defuse on any risk signal, Health recovery at or below mid-range, then top-up of the Below-best stats before a review or capability building otherwise.

## Result

Same actor as v1–v6 (`017798b931bc18f8`, `claude-cli:haiku`, CLI 2.1.310), origin `matteo`, purpose `pilot`, 8 parallel slots, 26 Oct 22:06–22:20 UTC. The sandbox CLI had updated itself to 2.1.311 after an environment restart; the first 8 jobs (actor `b949e41e0434071a`) were cancelled before playing and requeued with a local install of 2.1.310 so the actor matches v3 and v6 exactly.

| Job | Outcome | Months | Q | Final level | Wealth dim |
|---|---|---:|---:|---|---:|
| 00000 | completed | 48 | 62.85 | L5 | 46.8 |
| 00001 | completed | 48 | 64.28 | L5 | 38.9 |
| 00002 | completed | 48 | 67.08 | L5 | 40.4 |
| 00003 | completed | 48 | 52.95 | L4 | 32.9 |
| 00004 | completed | 48 | 61.98 | L5 | 35.8 |
| 00005 | trust crisis | 47 | 44.90 | L4 | 27.0 |
| 00006 | completed | 48 | 64.80 | L5 | 40.3 |
| 00007 | completed | 48 | 71.32 | L5 | 55.8 |

| | v3 (8) | v6 (8) | **v7 (8)** |
|---|---:|---:|---:|
| Mean Q | 51.04 | 50.08 | **61.27** |
| Completed | 5/8 | 6/8 | **7/8** |
| Out of L1 within the first year | 5/8 | 6/8 | **8/8** |
| Promoted at the first review | 4/8 | 4/8 | 5/8 |
| Finished at L5 | — | 4/8 | **6/8** |

## Interpretation

- **No career stayed at L1**, which was the cause of nearly every loss in v1–v6 and in the race. The three not promoted at the first review were all promoted at the second.
- The only loss is a trust crisis at month 47 at L4 (Q 44.9).
- Every action note carries the status line; before reviews, notes cite Network and Output protection.
- For reference: the race champion is at 53.9 (12 games) and the Opus ceiling measurement at Q 56.2. This is the first manual we have seen above 60 over eight episodes, but these are pilots outside the race with a fixed actor; v3's 71.4 over four pilot episodes did not survive replication. The race measurement is what counts.
- The status-line format did not help `f3-status-line-v1` in the race (3/8); here it carries different rules, so the format alone is not the explanation.

## Relevo

1. **Done:** wrote `observed-growth-v7` on branch `matteo/observed-growth-v7` (built on `main`); lint clean; 8 Haiku pilots under origin `matteo`, actor matched to v3/v6; exported.
2. **Data:** `lab/registry-origins/matteo/*.jsonl` (40 evaluations across v1–v7). Trajectories outside Git under `~/careerlab-data/huawei-matteo/runs/` in the sandbox.
3. **Unfinished:** nothing interrupted. The 8 cancelled 2.1.311 jobs remain in the registry as cancelled, never played.
4. **Next:** organiser to `ladder add` `lab/policies-src/matteo-feedback-growth/observed-growth-v7` in the fast race (T14) with the race actor; if it holds up, it is a candidate for the cut-1 submission. To reproduce the pilot actor: `npm install @anthropic-ai/claude-code@2.1.310` and `CAREERLAB_CLAUDE_EXE=<that>/node_modules/.bin/claude`.
5. **ESTADO.md:** T4 line updated.
