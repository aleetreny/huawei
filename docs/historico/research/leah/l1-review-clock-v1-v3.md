# l1-review-clock v1, v2 and v3: five Haiku games

Leah, 26 Oct 2026, 16:31–17:05 UTC, origin `leah` on Leah's Mac.
- **Player:** Claude Haiku, CLI 2.1.295 on a Pro account. The race uses 2.1.303 on Max.
- **Games:** run in parallel, 3 at a time; about 15 minutes each.
- **Status:** a rough read, not a race decision. All runs are in `lab/registry-origins/leah/` and in the panel under *Other machines*.

## Results

| Manual | Games | Scores | Mean | Completed | How the others ended |
|---|---:|---|---:|---:|---|
| **v1** | 3 | 60.9, 51.3, 44.0 | **52.1** | 2/3 | trust crisis at month 33 (two risk blow-ups) |
| v2 | 1 | 20.5 | 20.5 | 0/1 | dismissed at month 24, never left L1 |
| v3 | 1 | 21.8 | 21.8 | 0/1 | dismissed at month 24, never left L1 |
| Race leader F3 (race games) | 3 | 66.6, 59.7, 66.3 | **64.2** | 3/3 | — |
| Race, all Haiku games | 59 | — | 44.8 | 30/59 | — |

**v1 is above the race's average Haiku game (44.8) but clearly below F3 (64.2).** v2 and v3 made things worse; each was played once.

## Patterns found in the transcripts

These come from `scripts/leah/behaviour.py` and the trace scripts noted in the work log. All of them read only the worker's own transcripts.

1. **Skill stalls at L1.**
   - In every game, Skill sat around 8–9 while the player was at L1. In the stuck games that lasted a whole year or more, whatever was chosen.
   - In v3's stuck game, not one story event in months 4–11 raised Skill.
   - After the first promotion, good story options began paying +1 or +2 Skill each. The fast games gained about 34 Skill from story events in their first 18 months.
2. **The first promotion decides the game.**
   - Games promoted at the first review (Output 4–6 there) went on to L3 by month 12.
   - Games not promoted (Output 0–3) stayed at L1. Two were dismissed at month 24, and one scraped through to L2 at month 18.
   - So Output and Network at L1 look like the lever, not Skill. This is a pattern in 5 games, not a known rule.
3. **Early Defuse starves growth.** Defuse costs 2 of the 3 Energy points. v2 defused every quarter and stayed at L1.
4. **Late Defuse is still needed.** The fastest v1 game (L4 at month 18, Skill 72) defused only 4 times in 33 months and ended in a trust crisis. v1's completed games lost half their risk-control points.
5. **The quarterly plan was followed.** No High-intensity work appeared in any game; a key project was the main action in most quarters; and Health was kept high except for one game that dropped to Health 1 at month 6.

## What each version changed and why it failed

- **v2: risk-first** (Defuse on any non-relaxed remark and at least once per review period; Report results when Output stalls). This spent the early Energy on Defuse, and the game never got its first promotion. **Refuted**, in its current form, by the dismissal.
- **v3: story events as the growth engine** (own the problem and bring a plan; refuse comfortable options; Defuse after the first promotion). Its premise was wrong at L1, where story events stop paying Skill. It never got the first promotion either. **Not supported** (1 game).

## Next (not yet run)

A **v4** built on v1 should:
- target the first promotion through **Output and Network while at L1**: Prepare report materials and Network maintenance in every Energy phase, a key project as the main action, and story options that deliver visible results or win allies;
- keep v1's story judgement after that;
- add v3's **post-promotion Defuse** to prevent the trust crisis.

Run 2–3 games at once after the 5-hour quota resets (the window was at 70% at 17:05 UTC). One v1 game (`leah-scre-f1830961-614d6e-00004-a2`) is still queued and held.
