# observed-growth-v6: eight Haiku episodes

## What v6 changes from v3

Built from the promotion study ([matteo-promotion-study.md](matteo-promotion-study.md)): reviews are applied at the start of the review month, and promotion needs Skill, Network and Output at the current level's ceiling at that moment. v6 (policy `fbf47dab7a60f99f`, parent `observed-growth-v3`, 711 words, lint clean) adds to v3: a review-timing section; a quarter-end note that tracks best values at this level and whether the next review comes before the next quarter-end; a top-up of any input below its best in the allocation before a review; a guard on Network and Output in story choices before a review; an explicit ban on confronting or blaming colleagues; Health recovery at or below mid-range.

## Result

Same actor as v1–v5 (`017798b931bc18f8`, `claude-cli:haiku`, CLI 2.1.310), origin `matteo`, purpose `pilot`, 8 parallel slots, 26 Oct 20:20–20:33 UTC.

| Job | Outcome | Months | Q | Final level | First review |
|---|---|---:|---:|---|---|
| 00000 | completed | 48 | 53.90 | L4 | not promoted (Output below best), promoted at the second |
| 00001 | trust crisis | 22 | 18.62 | L1 | not promoted (Skill below best) |
| 00002 | completed | 48 | 55.35 | L4 | not promoted (Skill below best), promoted at the second |
| 00003 | completed | 48 | 56.98 | L5 | promoted (at ceiling) |
| 00004 | completed (resumed) | 48 | 54.91 | L5 | promoted (at ceiling) |
| 00005 | dismissed | 24 | 23.48 | L1 | not promoted (Output below best) |
| 00006 | completed (resumed) | 48 | 71.72 | L5 | promoted (Skill one below best) |
| 00007 | completed | 48 | 65.67 | L5 | promoted (at ceiling) |

The two interrupted episodes stopped at month 42, alive at L4 and L5, when Matteo's Claude account hit its session limit (usage_limit_reached, reset 21:20 UTC). At 22:00 UTC, after the reset, both were continued in place with the official continuation prompt (same session, same server database; `resumed` = 1 in the registry) and completed.

| | v3 (8) | v6 (8) |
|---|---:|---:|
| Out of L1 within the first year | 5/8 | 6/8 |
| Promoted at the first review | 4/8 | 4/8 |
| Mean Q | 51.04 | 50.08 |
| Completed | 5/8 | 6/8 |

## Interpretation

- **The ceiling rule held again**: at the first review, the 3 episodes at the full ceiling were all promoted; 1 of 5 below it was. v6 did not yet make the actor reach and hold the ceiling more often than v3 (4/8 promoted at the first review in both).
- **The second window helped**: two of the four not promoted at the first review were promoted at the second; v3 had 1 of 4.
- Both losses are careers that never left L1, as in every version.
- Completed v6 careers scored 54–72 with final level L4–L5. v6 completes more often (6/8 vs 5/8) at a similar mean Q (50.1 vs 51.0); with eight episodes each the two are not distinguishable.
- v6 is 711 words, the longest in the family; token cost counts for 10 % of the grade.

## Relevo

1. **Done:** wrote `observed-growth-v6` on branch `matteo/observed-growth-v6` (built on `main`); lint clean; played 8 Haiku pilots under origin `matteo`; exported.
2. **Data:** `lab/registry-origins/matteo/*.jsonl`. Trajectories outside Git under `~/careerlab-data/huawei-matteo/runs/` in the sandbox.
3. **Unfinished:** nothing. Jobs 00004 and 00006 were interrupted at month 42 by the account limit and resumed in place after the reset with a small script that reuses the lab's continuation prompt and `Registry.ingest`.
4. **Next:** if v6 is pursued, the open problem is getting the actor to the ceiling at the first review (Output and Skill dips), and shortening the Skill for token cost. The race (T14) now favours a fixed status-line format (`f1 línea de estado`); a v7 could use that format with v6's review-timing rule.
5. **ESTADO.md:** T4 line updated.
