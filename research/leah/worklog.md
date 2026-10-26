# Leah's work log

Everything done on branch `leah/workspace`, newest first. Each entry links to the full report.

## 26 Oct 2026, 16:30 UTC: results panel

- **What.** A static results panel at `lab/panel/index.html`, generated from committed results by `scripts/panel/build.py`. It shows the race leaderboard per decision snapshot, every AI game over time, where the points go per scoring dimension, survival by month, the T10 energy bots, my local 1,562-game bot sweep and other machines' exports.
- **Why.** The race's results were spread over JSONL files and Markdown reports. One page makes progress and the remaining gap visible to the whole team.
- **Key numbers** (race at `b0f348f`):
  - the leader is f3-feedback-reactive-v1 at 60.2;
  - completed games miss about 40 points, mostly level (13.8/30) and wealth (6.9/20);
  - 27 of 51 eliminations are the month-24 dismissal;
  - the best single AI game is 73.1 (Matteo's M3 with Sonnet).
- **Report.** [lab/panel/README.md](../../lab/panel/README.md)

## 26 Oct 2026, 16:08 UTC: T11, several machines without overwriting results

- **What.** Each machine other than the cloud race sets an origin (`careerlab origin set leah`). Its job ids, replicate numbers, data folder and export folder become its own. Leasing, recovery and the pre-registered decisions only see the registry's own origin. Every `export` refuses to delete rows that the local registry lacks.
- **Why.** Two machines numbered games identically, so merges dropped results, and a stale `export` could wipe the race's rows in Git.
- **Evidence.** 230 tests pass (5 new). Two real scripted games ran as `leah` and left the race's 249 finished and 22 queued games untouched.
- **Commit.** `30856ee`.
- **Report.** [lab/reports/t11-multi-machine/README.md](../../lab/reports/t11-multi-machine/README.md)

## 26 Oct 2026, 15:55 UTC: branch, tasks and starting point

- **Branch.** Created `leah/workspace` from `main` (`42440a0`) and pushed it. No PR yet; it waits for review.
- **Tasks for Leah.** `ESTADO.md` assigned none. I picked T11 because playing from this Mac needs it; T4, T7 and this panel were the other good fits.
- **Matteo's branch.**
  - It forked from the first commit, so it has none of CareerLab, and merging it whole would be a step back.
  - Its value is the v0.2 "growth" Skills. They scored 73.4 in one manual Codex-played game, but they have never been entered in the race.
  - The v0.1 version (M3) is dormant at 38 with Haiku. Yet it produced the race's best single game, 73.1, with Sonnet.
- **Starting point.** `main`, with results read from `cloud-lab-run`.

## Open threads

- **PR from `leah/workspace` to `main`** for T11 and the panel. Leah asked to hold it for now.
- **Register Matteo's v0.2 Skills** as a race policy and test them under origin `leah`.
- **A rule-safe scripted strategy bot**, to probe the level and wealth gap without Claude quota.
- **After T11 merges,** the organiser updates ESTADO §6 *Partidas* and adds an origin filter to `scripts/cloud-run/driver.py`, as the T11 report explains.
