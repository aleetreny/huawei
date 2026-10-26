# Promotion study: what decides the first promotion

Matteo asked what drives the first promotion, since it decides most careers (see [matteo-observed-growth-v5.md](matteo-observed-growth-v5.md) and the organiser's diagnosis in `lab/reports/cloud-run-diagnostics/block3-generation.md`). This study used scripted bots (no Claude quota) plus the 24 Haiku pilots of origin `matteo`. Only the five official tools were used.

## Method

`scripts/promotion-study/run.py`: one scripted bot per episode, own seed, own data directory (`~/careerlab-data/promotion-study`), nothing in the race registry. Each episode draws one of the three most survivable Energy mixes of T10, then picks story options and quarterly main actions uniformly at random. Random choices give variation where we need it; the Energy mix keeps enough episodes alive to reach the first review. `scripts/promotion-study/analyse.py` extracts per-episode features and the event pool. Batch of 26 Oct, 19:50–21:00 UTC, about 3,600 episodes, 2 slots.

## Findings

1. **Timing of the review (the key correction).** In every episode (2,511 at the first review, 252 at the second), the formal half-year review and the promotion decision are applied at the **start** of the review month, before that month's story events and before its quarter-end allocation. The allocation that precedes a review is the previous quarter-end, and the story events of the months in between also count. The handbook's numbered list reads as if the quarter-end allocation came first; it does not. Our v2–v5 manuals told the actor to treat the allocation of the review month as the one before the review, so their "review quarter" was mistimed.

2. **Being at the visible ceiling of the current level at review time is what promotes.** Measured on the state just before the review:

   | | episodes | promoted at the first review |
   |---|---:|---:|
   | Bots at the L1 visible ceiling (Skill, Network, Output all at their highest observed L1 values) | 103 | **55 %** |
   | Bots below it on any one of them | 2,408 | **3.5 %** |
   | Haiku pilots at the ceiling | 13 | **9 (69 %)** |
   | Haiku pilots below it | 11 | **0** |

   Promotion probability rises monotonically with each of Skill, Network and Output; Dignity is also higher in promoted bot episodes (8.9 vs 6.7). The earlier claim in `matteo-observed-growth-v5.md` that all Haiku careers reached the ceiling before the review was wrong: it measured peaks over the month, including after the review. At review time, 11 of the 15 non-promoted Haiku careers had dropped below the ceiling on Network or Output (to 1–2) or Skill (to 8), mostly through story outcomes in the months just before the review.

3. **What remains is partly chance.** Even at the ceiling about a third to a half of careers are not promoted. Among ceiling episodes, no story-choice category or main action separated promoted from not with any stability as the sample grew.

4. **Story choices.** Across all bots, options that confront or blame colleagues, or cut corners, were associated with lower promotion odds; ownership-type options with higher. This is consistent with v3's story rules.

5. **Event pool.** 132 distinct event titles over about 67,000 story decisions. Every title can appear from the first month; 934 of 955 episodes in an early check had distinct opening sequences. About 44 % of titles return within an episode as follow-ups of a chain. There is no fixed order to exploit, and titles must never appear in a Skill anyway.

## What this means for the manual

General, lint-safe rules that follow:
- A review judges the state at the moment it is applied, which is before the review month's own events and allocation.
- Promotion needs every visible input at the highest value it can reach at the current level; a stat that has stopped rising is at that ceiling and must be kept there, not merely reached once.
- In the run-up to a review, avoid story options that cost Network or Output (small ceilings make a single point decisive) and use the quarter-end before the review to top up whichever input is below its recent best.

## Relevo

1. **Done:** wrote the bot runner and analysis on branch `matteo/promotion-study`; ran about 3,600 bot episodes; checked the Haiku pilots at review time.
2. **Data:** `~/careerlab-data/promotion-study/` in the sandbox (`episodes.csv`, `events.csv`, `prereview.csv`, run folders). Not committed: they contain development-dataset text. Re-run with the commands below.
3. **Unfinished:** the bot batch was stopped before 6,000 episodes; the numbers above were stable between 950 and 3,600 episodes.
4. **Next:** write `observed-growth-v6` = v3 with the corrected review timing and the hold-the-ceiling rule; test with 8 Haiku episodes against the 8 v3 episodes. Commands: `CAREERLAB_DATA=~/careerlab-data/promotion-study nice -n 19 uv run python scripts/promotion-study/run.py --n 6000 --slots 2`, then `python3 scripts/promotion-study/analyse.py`.
5. **ESTADO.md:** not changed on this branch (findings for the organiser to fold in).
