# Protocol fastloop-v2: champion and challengers (26 Oct 2026)

**Status.** Replaces prereg-v1's allocation and selection rules for the Haiku race from 26 Oct 2026, by Alejandro's decision (26 Oct, ~19:00 UTC): iterate faster, stop playing manuals that do not work, put games where there is value, and try bold ideas when the race is stuck. prereg-v1 is not edited and stays the record of what was decided before; its data stay valid and are reused here. Code: `careerlab/ladder.py`; driver: `scripts/fastloop/`; team page: `lab/fastloop/README.md`.

## Why

By 26 Oct 19:00 UTC the race had spread about 450 Haiku games over 40 manuals, most with 3–10 games, and the leader's estimate kept falling as games accumulated (61 → 55). New children were written from aggregate tables and none beat its parent. The single-designer loop (write, play a few games, read whole games, fix one thing) produced ideas faster, but four-game verdicts were often luck: Matteo's observed-growth-v3 went from 71.4 (4 games) to 51.0 (8 games). Both lessons shape this protocol: a designer that reads whole games, and verdicts that need 8–12 games before a manual can take the title.

## Rules

- **Actor and data.** The race actor is `claude-cli:haiku` with CLI 2.1.303 (`08e9167a965ed82c`), origin `` (the cloud race). Every terminal game of a manual with this actor counts, whatever its purpose. Interrupted games never count and are replaced.
- **Model of a manual.** Expected game score = p·μ + (1−p)·28.6, where p is the completion rate (posterior Beta(1+completed, 1+early exits)), μ the mean score of its completed games (posterior Normal(mean, 5/√completed); Normal(61, 8) before any completion), and 28.6 the mean score of the 75 race games that ended early. P(better) is the posterior probability that a challenger's expected score exceeds the champion's (Monte Carlo, 20,000 draws, deterministic seed).
- **Champion.** One manual. Initial champion: the best expected score among manuals with at least 8 race games. It plays control games: at least 8, plus one per 5 challenger games played since it took the title, at most 24.
- **Ladder.** A challenger plays 2 games (4 when it brings strong evidence from elsewhere), then:

| Games played | Stays if | Otherwise |
|---:|---|---|
| 2 | P(better) ≥ 0.05 | out |
| 4 | P(better) ≥ 0.15 | out |
| 8 | P(better) ≥ 0.60: **new champion**; 0.35–0.60: 4 more games | below 0.35: runner-up (stops playing) |
| 12 | P(better) ≥ 0.60: **new champion** | runner-up |

- **A new champion** drops the variants of the old champion that have not played yet; challengers already playing continue against the new champion.
- **Priorities.** 12-game rung 40, 8-game rung 30, champion control 25, 4-game rung 20, first games 10 (12 for bold and outside manuals). The continuous scheduler leases one job whenever a slot frees, so a priority set a minute ago applies to the next free slot.
- **Pipeline.** Four challengers in play at any time (active plus designs being written). Each missing slot asks for a design: one "stretch" (level and wealth in careers that already finish) whenever none is in play, otherwise "targeted" (the champion's costliest failure pattern).
- **Stuck.** Six challengers finished without a new champion, or three hours without one once three have finished: the next two designs are "bold" (a different premise, keeping the proven guardrails). The counter restarts once a bold manual enters.
- **Designers.** Headless Claude (Opus, effort max) with Read/Glob/Grep/Write/Edit only. They read the champion's Skills, digests of its latest race games (worst four, best two), `lab/fastloop/lessons.md` and `lab/fastloop/history.md`, and write one policy folder. The driver lints it with the known event titles, registers it and adds it to the ladder; one repair round, otherwise it is rejected.
- **Outside manuals** (team members' branches) enter as challengers once merged; with four or more games from another cell and a mean at least the champion's, they start with 4 games.

## Calibration

Simulated with the fitted race distributions: completed games Normal(μ, 4.5), early exits Normal(28.6, 11.2); champion with 12 games (`scripts/fastloop/calibrate.py`).

| Challenger vs champion (true expected score) | Becomes champion | Out after 2 | Out after 4 | Games used |
|---|---:|---:|---:|---:|
| much worse (44.8 vs 68.9) | 0.00 | 0.86 | 0.13 | 2.3 |
| worse (59.5 vs 68.9) | 0.02 | 0.43 | 0.33 | 4.3 |
| slightly worse (66.0 vs 68.9) | 0.13 | 0.15 | 0.26 | 7.0 |
| equal (68.9) | 0.42 | 0.06 | 0.11 | 8.5 |
| slightly better (71.7 vs 68.9) | 0.69 | 0.02 | 0.05 | 8.9 |
| better (75.1 vs 68.9) | 0.94 | 0.00 | 0.01 | 8.4 |

With the current champion (F1-like, 59.2), a v3-like challenger of true 68.9 is crowned 97 % of the time in about 8 games. The price of speed is accepted on purpose: a slightly worse challenger takes the title about one time in eight, and an equal one about two times in five (a coin flip with no loss).

## What it cannot do

It cannot make the game less random. The official tools offer no seed, so two manuals cannot be played on the same event draws; whether a career is promoted at its first window, which largely decides whether it survives, varies from game to game with the same manual. Differences of a few points need many games; the ladder detects large improvements quickly and small ones slowly or not at all.

## DeepSeek (target model, USD 50 key)

Never used for exploration. Gates, run from the Mac that holds the key (`careerlab/target.py`):
1. **Route and cost check:** one game of the confirmed champion (8+ race games), once, to prove the packaged manual plays end to end in the official runner and to measure the real cost per game.
2. **Before each cut:** two games of the champion if it changed since the last DeepSeek check, plus two of the previous submission when the choice is close.
3. **Divergence:** if DeepSeek ends early where Haiku completes, its trajectory is read and the lesson goes to `lessons.md`.
Budget guard: exact cost read from the key's usage before and after each game; a series stops if one game costs more than the cap; USD 15 stays in reserve for the last cut.
