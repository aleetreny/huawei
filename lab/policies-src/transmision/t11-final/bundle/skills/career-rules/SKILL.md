---
name: career-rules
description: "Use on every Career Survival turn. Sets the quarterly Energy and main action in priority order (end of career, Health and Dignity, HR risk remarks, senior levels, growth) and the review countdown to write before every story choice."
---

# Career rules

## What this Skill decides
- **Quarterly phases** (Energy actions, then one main action): fully, with the priority list below.
- **Story events:** you judge each story yourself. This Skill only adds a review countdown and, in the last month before a review, a check from `reference/review-month.md`.

## The 48 months at a glance
Reviews come every six months; promotion needs Skill, Network and Output high enough for your level, so growth matters most before each review. Hidden risk builds quietly and the monthly HR remark is its only gauge; a second blow-up ends the run. From L4 the bar rises fastest for Skill. In the final month, the ending evaluation counts level, wealth, health and dignity, skill, risk control and network.

## Turn loop
1. `observe`. Read `events` first: the monthly HR remark, the review talk, warnings. If you resumed after a break, call `check_latest_logs` for the last few decisions.
2. Quarterly phase: walk the list below; the first matching line decides. Story event: write the countdown, then choose.
3. `take_action` with the exact `choice` and a short note naming the line used. If `success` is false, pick another option you can afford.

## Quarterly phases: first matching line wins
You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost.
1. **Final month of the career (month 48):** main action Lay low and reduce risk. Energy: Defuse legacy risk if the HR remark is not the friendly one, then Health recovery and Mental recovery until both are full, then Network maintenance. Never Skill learning or High-intensity work: their gains come too late and their Health cost counts.
2. **Health or Dignity low.** Our safety margin, not a published limit: Health 4 or less, Dignity 3 or less, or either falling for several months. Health recovery (or Mental recovery) first; no Skill learning or High-intensity work until it recovers. Health at zero ends the run at once.
3. **HR remark shows high risk.** Read the latest monthly HR remark and place it in one of three bands:
   - friendly ("you are doing all right"): no risk action;
   - quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below;
   - anything else (frowning, uneasy, "you are on your own", angry, buried problems): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is back to friendly or quiet.
4. **L4 or above:** Skill learning (2 Energy) plus one point on the weakest of Health, Dignity or Network; main action Apply for rotation.
5. **Otherwise (L1 to L3):** spend Energy on whichever of Skill, Network and Output is furthest from what the next review needs: Prepare report materials for Output, Network maintenance for Network, Skill learning for Skill while Health is comfortable. Main action Apply for a key project, which lifts all three. If Network is near zero or Wealth is near zero for months, fix that first (Network maintenance or Repair a key relationship; avoid spending), since both are published failure paths.

## Story events: review countdown
Before every story choice, start the note with `Review in N`: the months left until the next review month, N = 6 - (current_month mod 6), and N = 6 when current_month is a multiple of 6.
- **N = 1** (the last month before a review): open `reference/review-month.md` with `skill_tool` (relative_file_path) and apply it to this choice.
- **Any other N:** no extra rule. Choose the option you judge best for a long, healthy career, weighing what it likely does to Health, Dignity, Skill, Network, Output, Wealth and hidden risk.
