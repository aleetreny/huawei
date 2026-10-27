# observed-growth-v8: eight Haiku episodes, stopped after the month-12 review

## What v8 changed from v7

Only the story-choice rules (policy `d3ed3600a5a0cbab`, parent `observed-growth-v7`, 562 words, lint clean), from the v7 analysis in [matteo-observed-growth-v7.md](matteo-observed-growth-v7.md): "honest and collaborative" (integrity never requires bluntness; pick the honest option that keeps the other person on side; flat refusal only when no collaborative option is honest), avoid options that slow one's own delivery before a review, repair a pre-review loss at once, never trade Health or Dignity heavily for appearances.

## Result

Same actor as v3/v6/v7 (`017798b931bc18f8`, CLI 2.1.310), origin `matteo`, purpose `pilot`, 8 slots, 26 Oct 22:45–22:55 UTC. Matteo stopped the batch after every episode had passed the month-12 review (episodes killed mid-game; recorded as interrupted, unscored). Weekly quota cap raised to 35 % for this batch and removed afterwards.

State just before each review (Skill/Network/Output) and outcome:

| Job | Month 6 | Month 12 |
|---|---|---|
| 00000 | 8/3/3 C | 9/3/2 C |
| 00001 | 9/3/2 C | 9/3/3 C, promoted |
| 00002 | 9/3/2 C | 9/3/3 C |
| 00003 | 9/3/3 C | 9/3/3 C, promoted |
| 00004 | 9/3/2 C | 9/2/3 C, promoted |
| 00005 | 9/3/3 C, promoted | (L2) |
| 00006 | 9/3/2 C | 9/3/3 C, promoted |
| 00007 | 9/3/3 C | 8/3/2 C |

| | v7 (9) | v8 (8) |
|---|---:|---:|
| Promoted at the first review | 5/9 | 1/8 |
| Out of L1 by month 12 | 8/9 | 5/8 |
| Network at the ceiling at the first review | — | 8/8 |
| Output at the ceiling at the first review | — | 4/8 |

## Interpretation

- The collaborative rule did what it said for Network: every episode held Network at the L1 ceiling at the first review.
- It moved the loss to Output: half the episodes reached the first review with Output one point short. Helping, pairing and talking things through appear to cost delivery.
- Net effect: worse than v7 at the two first windows. Two episodes at the full ceiling at month 6 were still not promoted (the chance part).

## Relevo

1. **Done:** wrote `observed-growth-v8` on branch `matteo/observed-growth-v8`; 8 Haiku pilots to month 12, then stopped at Matteo's request; exported (jobs interrupted, no scores).
2. **Data:** `lab/registry-origins/matteo/jobs.jsonl` (status of the 8 jobs); pre-review states above, read from the trajectories under `~/careerlab-data/huawei-matteo/runs/` in the sandbox.
3. **Unfinished:** the 8 episodes were deliberately not finished.
4. **Next:** `observed-growth-v9` = v7 plus a narrower collaborative rule that must not cost one's own delivery, with Output taking precedence before a review when it is below its best. Test to month 12 only.
5. **ESTADO.md:** T4 line updated.
