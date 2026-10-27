---
name: career-rules
description: "Use on every Career Survival turn. Keeps a one-line status note (review countdown, current Skill/Network/Output, expected result of each quarterly action, stats that did not take an announced gain, risky story choices this month) and sets the quarterly Energy and main action in priority order (end of career, Health and Dignity, HR risk remarks, senior levels, growth)."
---

# Career rules

## What this Skill decides
- **Every note:** a one-line status that carries what you have learned between turns (below).
- **Quarterly phases** (Energy actions, then one main action): fully, with the priority list below.
- **Story events:** you judge each story yourself. This Skill only adds the status line and, in the last month before a review, a check from `reference/review-month.md`.

## The 48 months at a glance
Reviews come every six months; promotion needs Skill, Network and Output high enough for your level, so growth matters most before each review. Hidden risk builds quietly and the monthly HR remark is the visible sign of it; a second blow-up ends the run. The handbook says higher levels set a higher bar; at senior levels watch which stat the review talks say is lagging, usually Skill. In the final month, the ending evaluation counts level, wealth, health and dignity, skill, risk control and network.

## Turn loop
1. `observe`. Read `events` first: the monthly HR remark, the review talk, warnings. If your last note is not in view (a new session, or after a summary), call `check_latest_logs` with count 3 and take `Stalled`, `Expect` and `Risky this month` (same month only) from the most recent note.
2. Quarterly phase: first the stall check below, then walk the list; the first matching line decides. Story event: write the status line, then choose.
3. `take_action` with the exact `choice` and a note that starts with the status line, then names the line used. If `success` is false, pick another option you can afford.

## Status line: your memory between turns
Start every note with this line:
`Review in N | Now S<Skill> N<Network> O<Output> | Stalled: none | Risky this month: 0`
In the quarterly phase, add what the chosen action should leave, from its `status_updates`:
`Review in N | Now S14 N5 O7 | Stalled: none | Risky this month: 0 | Expect S14 N5 O8`
- **Review in N:** the months left until the next review month, N = 6 - (current_month mod 6), and N = 6 when current_month is a multiple of 6.
- **Now:** Skill, Network and Output as `observe` shows them before this choice.
- **Stalled:** the stats that did not take an announced gain at your current level. Copy the list from your last note. When your `level` changes, reset to `Stalled: none` and let the stats show again whether they rise.
- **Stall check (quarterly phase, before choosing):** if your last note has `Expect` and was written in this same quarterly phase, compare it with Skill, Network and Output in `observe`. Any stat that is now below its `Expect` value did not take the gain: add it to Stalled. Example: last note `Expect S14 N5 O8`, observe shows Output 7, so write `Stalled: Output`.
- **Risky this month:** how many of this month's story choices may bury a problem: hiding or denying it, fixing it halfway or later, a quiet private deal, a gamble that it will not surface. Start each month at 0 and add 1 after such a choice. The HR remark only shows risk once a month, so this count is the risk it does not show yet: when it is 1 or more, in the rest of the month's stories prefer an option that brings the problem into the open or fixes it fully.
- **Using Stalled:** while a stat is in Stalled, more gains on it are not showing up in your stats, so treat them as wasted. In the quarterly phase, spend Energy and the main action on stats that are still rising. In stories, do not accept extra risk or a loss elsewhere to get it.
- **N = 1** (the last month before a review): open `reference/review-month.md` with `skill_tool` (relative_file_path) and apply it to this story choice. It is a short check that keeps the month's last choices from costing the promotion. For any other N there is no extra rule: choose the option you judge best for a long, healthy career, weighing what it likely does to Health, Dignity, Skill, Network, Output, Wealth and hidden risk.

## Quarterly phases: first matching line wins
You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost. Wherever a line names an action for a stat in Stalled, use the same line's choice for the next stat that is not in Stalled.
1. **Final month of the career (month 48):** main action Lay low and reduce risk. Energy: Defuse legacy risk if the HR remark is not the friendly one, then Health recovery and Mental recovery until both are full, then Network maintenance. Never Skill learning or High-intensity work: their gains come too late and their Health cost counts.
2. **Health or Dignity low.** Our safety margin, not a published limit: Health 4 or less, Dignity 3 or less, or either falling for several months. Health recovery (or Mental recovery) first; no Skill learning or High-intensity work until it recovers. Health at zero ends the run at once.
3. **HR remark shows high risk.** Read the latest monthly HR remark and place it in one of three bands:
   - friendly ("you are doing all right"): no risk action;
   - quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below;
   - anything else (frowning, uneasy, "you are on your own", angry, buried problems): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is back to friendly or quiet.
4. **After a weak review (C or D) or a talk that names a gap:** until the next review, spend Energy and the main action on the stat the talk names, or on the weakest of Skill, Network and Output that is not in Stalled (Prepare report materials, Network maintenance, Skill learning; main action Apply for a key project). A second weak review in a row is the dismissal path.
5. **L4 or above:** Skill learning (2 Energy) plus one point on the weakest of Health, Dignity or Network; main action Apply for rotation. If reviews stay strong while Output stalls, swap one quarter to Prepare report materials and Showcase results.
6. **Otherwise (L1 to L3):** spend Energy on whichever of Skill, Network and Output not in Stalled is furthest from what the next review needs: Prepare report materials for Output, Network maintenance for Network, Skill learning for Skill while Health is comfortable. Main action Apply for a key project, which lifts all three; if two of them are in Stalled, the main action that raises the third (Apply for rotation for Skill, Build a mentorship for Network, Showcase results for Output). If all three are in Stalled, Energy goes to Health and Dignity and the main action to Report results to your manager. If Network is near zero or Wealth is near zero for months, fix that first (Network maintenance or Repair a key relationship; avoid spending), since both are published failure paths.
