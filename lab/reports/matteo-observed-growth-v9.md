# observed-growth-v9: eight Haiku episodes to the month-12 review

## What v9 is

v7's text (status line, review timing, ceiling rule) with three story-choice lines learned from v7 and v8 (policy `9bb19b0bdfa06ae6`, parents `observed-growth-v7` and `observed-growth-v8`, 557 words, lint clean): honest without rigidity, but never at the cost of one's own delivery (brief or time-boxed help, raise privately, refuse only the improper part); before a review, if Output is below its best, prefer delivering or showing a result over a gesture of help; repair a pre-review loss at once.

## Result

Same actor as v3/v6/v7/v8 (`017798b931bc18f8`, CLI 2.1.310), origin `matteo`, purpose `pilot`, 8 slots, 26 Oct 22:50–23:00 UTC. At Matteo's request the batch was stopped once every episode had passed the month-12 review (episodes killed mid-game, recorded as interrupted, unscored). Weekly quota cap raised to 30 % for this batch and removed afterwards.

State just before each review (Skill/Network/Output), grade, promotion:

| Job | Month 6 | Month 12 |
|---|---|---|
| 00000 | L1 9/3/3 C, promoted | L2 21/7/6 B, promoted |
| 00001 | L1 9/3/3 C, promoted | L2 21/7/6 B, promoted |
| 00002 | L1 9/1/2 C | L1 9/3/3 C, promoted |
| 00003 | L1 9/3/3 C, promoted | L2 21/7/6 B, promoted |
| 00004 | L1 8/3/1 C | L1 9/3/3 C, promoted |
| 00005 | L1 9/3/3 C, promoted | L2 21/7/6 B, promoted |
| 00006 | L1 9/3/3 C | L1 9/3/3 C, promoted |
| 00007 | L1 9/3/3 C | L1 9/1/1 C |

| | v7 (9) | v8 (8) | **v9 (8)** |
|---|---:|---:|---:|
| At the full L1 ceiling at the first review | — | 3/8 | **6/8** |
| Promoted at the first review | 5/9 | 1/8 | 4/8 |
| Out of L1 by month 12 | 8/9 | 5/8 | **7/8** |
| At the L2 ceiling at month 12 (of those at L2) | — | — | **4/4, all promoted to L3** |

## Interpretation

- v9 reaches the ceiling at review time far more often than v8 and holds both Network and Output: 6/8 at the full L1 ceiling at the first review, and at month 12 every episode at the ceiling (7 of 7) was promoted. Every episode already at L2 sat exactly at 21/7/6 at month 12 and went to L3.
- The ceiling rule holds again: at month 6, 4 of 6 at the ceiling were promoted, 0 of 2 below it; at month 12, 7 of 7 at the ceiling, 0 of 1 below.
- The only episode still at L1 dropped to Network 1 and Output 1 just before the month-12 review.
- Against v7, out of L1 by month 12 is similar (7/8 vs 8/9); the gain is in how reliably the ceiling is held. Full careers were not played, so completion and Q are unknown.

## Relevo

1. **Done:** wrote `observed-growth-v9` on branch `matteo/observed-growth-v9` (built on `matteo/observed-growth-v8`); 8 Haiku pilots to month 12, then stopped; exported.
2. **Data:** `lab/registry-origins/matteo/jobs.jsonl`; pre-review states above, read from trajectories under `~/careerlab-data/huawei-matteo/runs/` in the sandbox.
3. **Unfinished:** the 8 episodes were deliberately not finished.
4. **Next:** if the team wants a score, put v9 in the fast race (T14) alongside v7, or play full careers. Possible next fix: the remaining loss pattern is a two-point drop of Network and Output in the months before a review in a minority of careers.
5. **ESTADO.md:** T4 line updated.

## At the ceiling but not promoted: is there a pattern? (26 Oct, 23:00 UTC)

Matteo asked whether careers at the L1 ceiling that were still not promoted share something, such as a person or an event. Data: 110 bot episodes from the promotion study at the full L1 ceiling at the first review (61 promoted), and 29 Haiku reviews at the L1 ceiling across v1–v9 (16 promoted).

- **People and events: no pattern beyond chance.** Comparing promotion rates with and without each event title seen in the first semester (titles seen at least 10 times), the largest gap was 0.31; in 71 % of datasets with the promotion labels shuffled, a gap at least that large appeared. Named people in event texts behave the same way. No individual event or colleague explains the misses.
- **HR tone and risk remarks**: no difference (risk remarks 0.9 vs 1.0 per episode, "doing all right" 1.5 vs 1.5).
- **Dignity matters for the bots**: promoted 62 % at Dignity 10, 57 % at 9, 53 % at 7–8, 29 % at 6 or below. Haiku keeps Dignity at 10 in almost every case, so this does not explain its misses.
- **Haiku at the ceiling**: 16/29 promoted (55 %, the same rate as the bots), with no difference in Dignity (all 10 among the misses) or Health.

So at the ceiling the promotion is close to a coin with about 55 % per review window. That makes holding the ceiling at every window the lever: three windows at the ceiling give roughly a 9 in 10 chance of leaving L1, one window about 1 in 2.
