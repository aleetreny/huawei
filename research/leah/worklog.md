# Leah's work log

Everything done on branch `leah/workspace`, newest first. Each entry links to the full report.

## 27 Oct 2026, 15:30 UTC: l6-routine-v1, the L6 bots' routine in Alejandro's T20 format

- **What.** Alejandro's `t10-countdown` with one line changed. At L1–L3, Energy follows the fixed routine of the energy bots that reached L6: Health recovery, Mental recovery, then Prepare report materials, every quarter. The main action is a key project, with no Skill learning. It replaces "lift whichever stat is furthest from the review".
- **Why.** The idea is in Alejandro's independent-chats plan. A fixed routine needs no judgement; t10's judgement line is the kind that sent the polish game's Energy to Skill learning at L1.
- **Checks.** Lint has no errors; its 4 REVIEW notes are inherited from t10's lines. 302 tests pass.
- **Not done.** No games. The fair test is Alejandro's T20 bank and interleaved games. Details in [l6-routine.md](l6-routine.md).

## 27 Oct 2026, 10:00 UTC: one Haiku game of f3-lean-polish-v1, live game page

- **Result.** 28.5, dismissed at month 24, never left L1.
  - The rewrite changed behaviour: the explicit main-action order meant **no key projects at all** (f3-lean: 49%) and 26% Skill learning.
  - The token lines worked: notes 60% shorter, about 13% fewer tokens per month.
  - Recommendation: submit **f3-lean-v1 as written** tonight. Details in [f3-lean-polish.md](f3-lean-polish.md).
- **Live game page.** `lab/panel/live.html`, fed by `scripts/panel/live.py`, follows a running game every 4 seconds: stats after each decision, reviews, promotions and the latest decisions with notes.
- **Panel.**
  - It now builds from `origin/main`, where the race ended: 521 race games, plus the origins `leah` (6), `matteo` (30) and `deepseek` (1).
  - Games imported from other machines are no longer double-counted as race games.
  - The page reloads `data.js` fresh every time.

## 27 Oct 2026: f3-lean-polish-v1, the R1 candidate rewritten for the rubric and tokens

- **What.** A copy of f3-lean-v1 (the cloud's R1 recommendation) with the **same rules**, regrouped by turn type to fit the official document-quality rubric, plus token instructions (one `observe` per decision, notes of a few words). 287 words; lint-clean.
- **Why.** Telling the tied top manuals apart would need about 130 games each, so the text-only 20% of the automated score (document quality and tokens) is what can still move today. Token gains are small: DeepSeek's one game used about 670k tokens a month, about 93 if completed.
- **Not done.** No game has been played with it. Submitting it is the team's call (T9).
- **Write-up.** [f3-lean-polish.md](f3-lean-polish.md).

## 26 Oct 2026, 17:05 UTC: v1 ×3, v2 and v3 (5 Haiku games)

- **Results.**
  - v1 scored 60.9, 51.3 and 44.0 (mean 52.1; 2 of 3 completed, one trust crisis at month 33).
  - v2 scored 20.5 and v3 scored 21.8; both were dismissed at month 24 still at L1.
  - The race leader F3 averages 64.2.
- **Learned.**
  - Skill stalls at L1, and story events only pay Skill after the first promotion.
  - The first promotion (Output and Network at L1) decides the game.
  - Early Defuse starves growth, but too little Defuse later causes a trust crisis.
- **Speed.** Games ran 3 at a time, about 15 minutes each. One game uses about 15% of the 5-hour window on Leah's Pro account.
- **Write-up.** [l1-review-clock-v1-v3.md](l1-review-clock-v1-v3.md), with the v4 plan.

## 26 Oct 2026, 16:50 UTC: first game of l1-review-clock-v1

- **Result.** 60.9, all 48 months completed, finished at L5 (promotions at months 6, 12, 30 and 48).
  - The race leader F3 averages 64.2 over 3 Haiku games; all completed race Haiku games average 59.5.
  - Level points matched F3 and wealth was higher. Points were lost on risk control (5.0 vs 6.7) and network (5.7 vs 7.2).
- **Manual followed.** No High-intensity work; a key project in 13 of 15 quarters; Health never below 7 at quarter end.
- **One game only, at Leah's request.**
  - The second game started in parallel was stopped and recorded as interrupted, so it is never scored.
  - The other 3 stay queued and held.
- **Earlier.** The CLI sign-in had expired, so the first 5 attempts never started (now recorded as interrupted). Leah signed in again with `claude auth login`.
- **Where.**
  - Write-up: [l1-review-clock-first-read.md](l1-review-clock-first-read.md).
  - Panel: *Other machines*, "Same player, different manual".
  - Export: `lab/registry-origins/leah/`.

## 26 Oct 2026, 16:30 UTC: Leah's manual, l1-review-clock-v1 (first read blocked)

- **What.** A new single-Skill manual, `lab/policies-src/l1-review-clock/l1-review-clock-v1/` (lint: no findings). It plans each quarter around the published review and promotion cadence:
  - a preventive Health reserve in every Energy phase;
  - the HR remark and warnings as a risk gauge, driving Defuse legacy risk and Lay low;
  - Apply for a key project as the default main action, with a catch-up action for whichever of Skill, Network or Output trails;
  - Prepare report materials for spare Energy, and never High-intensity work;
  - story options judged on honest, scoped delivery.
- **Why.** The race's gap is in level and wealth, and my local bot sweep found that this quarterly pattern was the best scripted plan. The hypothesis, predicted behaviour and refutation are in `policy.json`.
- **Comparison set up.**
  - Registered as `f1830961d168beb9` under origin `leah`.
  - 5 Haiku games queued: `leah-scre-f1830961-614d6e-0000{0..4}-a1`.
  - Same Haiku settings as the race cell, but Claude CLI 2.1.295 on a Pro account against the cloud's 2.1.303 on Max, so it's a rough read rather than a race decision.
  - The panel's *Other machines* section now draws a game-by-game head-to-head against the race leader and the race average for the same model.
- **Blocked.**
  - All 5 attempts stopped before creating a game: "OAuth session expired and could not be refreshed", and `claude auth status` now shows `loggedIn: false`.
  - No game was played and no quota was used. The attempts are kept on record as interrupted and are never scored.
- **Resume after signing in** (`claude auth login`):

  ```sh
  uv run python -c "from careerlab.config import load_settings; r=load_settings().registry(); [r.requeue_interrupted(j[0], 'replacement after CLI sign-in') for j in r.db.execute(\"SELECT job_id FROM jobs WHERE origin='leah' AND purpose='screen' AND status='interrupted'\")]"
  uv run careerlab run --kind claude-cli --slots 2 --max-five-hour 0.6
  uv run careerlab export && uv run python scripts/panel/build.py
  ```

## 26 Oct 2026, 16:20 UTC: results panel

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
- **v4 after the quota reset**: target the first promotion through Output and Network at L1, keep v1's story judgement, add Defuse after the first promotion. See [l1-review-clock-v1-v3.md](l1-review-clock-v1-v3.md).
- **Register Matteo's v0.2 Skills** as a race policy and test them under origin `leah`.
- **A rule-safe scripted strategy bot**, to probe the level and wealth gap without Claude quota.
- **After T11 merges,** the organiser updates ESTADO §6 *Partidas* and adds an origin filter to `scripts/cloud-run/driver.py`, as the T11 report explains.
