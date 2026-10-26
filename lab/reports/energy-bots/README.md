# T10 — Energy bots: what the quarterly Energy mix does on its own

Run in the cloud container on 26 Oct 2026, 15:37–15:47 UTC. No Claude quota was used. Code: `scripts/energy-bots/run.py`.

The bots ran in their own data directory (`~/careerlab-data/energy-bots`), with their own server pool and run folders. Nothing entered the race's registry or its quota governor. Dev split, official engine settings, stdio, 2 workers at `nice 19`, 400 complete episodes, launches interleaved by replicate.

## Design

Ten scripted arms play identically except for the quarterly Energy:

- **Story events:** always the **first listed option**. This is a fixed rule so the arms are comparable. It is a lab device only, see the caveats.
- **Main action:** always Apply for a key project.
- **Energy:** each arm spends its 3 points in a fixed preference order. An action is not repeated within a phase. If none of its preferences is affordable, it falls back to a cheap action. The `reserve` arm spends nothing.
- **The `adaptive` arm** recovers when Health or Dignity is low and otherwise plays report + High-intensity work. Its "low" (4 of 10) is a lab parameter for this experiment, not a game threshold and not Skill content.

## Results (40 episodes per arm)

| Energy mix (preference order) | completed | mean months | blackouts | other exits | mean Q | grades over all reviews | completed Q |
|---|---:|---:|---:|---|---:|---|---|
| Defuse legacy risk + Health recovery | **10** | **20.5** | 22 | dismissed 6, broke 1, trust 1 | **32.8** | A 14, B 50, C 52, D 12 | 44–76 (mean 59.3) |
| Health + Mental recovery + Prepare report | 9 | 17.4 | 28 | dismissed 2, trust 1 | 30.4 | A 12, B 44, C 44, D 5 | 52–75 (mean 59.6) |
| Network maintenance + Health + Mental recovery | 4 | 14.0 | 30 | dismissed 5, trust 1 | 27.7 | A 5, B 19, C 48, D 9 | 52–68 |
| Prepare report + Network + Health recovery | 4 | 13.2 | 31 | dismissed 5 | 27.1 | A 8, B 23, C 38, D 7 | 50–70 |
| adaptive (recover only when low) | 1 | 8.8 | 36 | broke 2, trust 1 | 24.6 | A 1, B 14, C 28 | 67 |
| Prepare report + Defuse | 0 | 6.5 | 39 | broke 1 | 23.1 | B 1, C 21 | — |
| reserve (spend nothing) | 0 | 6.3 | 40 | — | 22.1 | B 1, C 22 | — |
| Prepare report + High-intensity work | 0 | 5.1 | 40 | — | 21.2 | B 1, C 17 | — |
| Prepare report + Skill learning | 0 | 4.9 | 40 | — | 22.1 | B 1, C 11 | — |
| High-intensity work + Network | 0 | 4.9 | 40 | — | 21.4 | C 18 | — |

The first review was C or D in **every** episode that reached one, in every arm.

## General lessons

These are behaviour lessons, not answers to events, and they contain no unpublished thresholds.

1. **Health is the first constraint whenever story choices do not look after it.** Every mix without a Health-recovery point in each quarter blacked out within the first months, all 40 of 40 runs. That includes spending nothing. Two-point growth actions (High-intensity work, Skill learning) make it come sooner. Any policy that plays stories aggressively needs a standing Health budget every quarter, not an occasional one.
2. **Recovering only once Health is already low is too late.** The adaptive arm blacked out in 36 of 40 runs. Health falls in steps from story events faster than one quarterly recovery restores it. Recovery has to be preventive: when Health is falling, or after a quarter with costly choices.
3. **Among mixes that protect Health, defusing risk adds the most.** Defuse legacy risk + Health recovery had the most completions (10/40), the longest careers and the most A grades. Recovery + report preparation was close behind (9/40). Network-heavy mixes completed less often (4/40).
4. **The Energy mix does not fix the first review.** All first reviews were C or D, as in every Claude and Opus game so far. Better grades (B, then A) appear only in careers that survive longer. Survival comes first, and grades follow time served and delivery.
5. **Surviving bots end at the same level and wealth as the LLM players.** The completed games ended at level 40–60 and wealth 21–49 (normalised), with Q 44–76. That is the same range as the completed Claude-proxy games. They did it with a fixed key-project main action and no judgement at all. The level and wealth gap therefore does not close through the Energy mix. What separates good from bad careers here is mostly whether they survive.

## Caveats

- **The first-option story rule is a lab device.** Option order is not a published rule and may differ in other datasets, so "take the first option" must never appear in a Skill. Its Health cost is specific to this rule. LLM players read the options and protect Health much better: Haiku's completed runs keep resilience near the top. So the blackout rates above say nothing about LLM players. The *ordering* of Energy mixes is the transferable part, and mostly for aggressive policies (o2-run-hot, f8's Grow mode).
- These are single scripted policies, one per arm, with 40 runs each. No uncertainty model was fitted, and a difference of 1–2 completions out of 40 is noise.

## Use in the race

- Lessons 1–2 support keeping preventive Health care in the growth-oriented families (f8 Grow, o2 run-hot), and they predict o2 is the most exposed.
- Lesson 3 is consistent with distilled rule R1 (Defuse before the next review).
- Lesson 5 says the remaining score is mostly about surviving more often and a little about what happens after promotion. It agrees with the score-gap finding, and shows a scripted bot reaches the same plateau.

Reproduce: `CAREERLAB_DATA=~/careerlab-data/energy-bots nice -n 19 uv run python scripts/energy-bots/run.py --n 40 --slots 2`.
