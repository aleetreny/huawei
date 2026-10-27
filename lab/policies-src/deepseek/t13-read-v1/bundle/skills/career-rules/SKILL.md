---
name: career-rules
description: "Use on every Career Survival turn. Sets the quarterly Energy and main action in priority order (end of career, Health and Dignity, HR risk remarks, senior levels, growth), and how to read every story option and choose between them."
---

# Career rules

## What this Skill decides
- **Quarterly phases** (Energy actions, then one main action): fully, with the priority list below.
- **Story events:** read every option with the guide below, then choose with the story rule; in the last month before a review, also apply `reference/review-month.md`.

## The 48 months at a glance
Reviews come every six months; promotion needs Skill, Network and Output high enough for your level, so growth matters most before each review. Hidden risk builds quietly and the monthly HR remark is the visible sign of it; a second blow-up ends the run. The handbook says higher levels set a higher bar; at senior levels watch which stat the review talks say is lagging, usually Skill. In the final month, the ending evaluation counts level, wealth, health and dignity, skill, risk control and network.

## Turn loop
1. `observe`. Read `events` first: the monthly HR remark, the review talk, warnings. If you resumed after a break, call `check_latest_logs` for the last few decisions.
2. Quarterly phase: walk the list below; the first matching line decides. Story event: write the countdown and one reading per option, then choose.
3. `take_action` with the exact `choice` and a short note naming the line used. If `success` is false, pick another option you can afford.

## Quarterly phases: first matching line wins
You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost.
1. **Final month of the career (month 48):** main action Lay low and reduce risk. Energy: Defuse legacy risk if the HR remark is not the friendly one, then Health recovery and Mental recovery until both are full, then Network maintenance. Never Skill learning or High-intensity work: their gains come too late and their Health cost counts.
2. **Health or Dignity low.** Our safety margin, not a published limit: Health 4 or less, Dignity 3 or less, or either falling for several months. Health recovery (or Mental recovery) first; no Skill learning or High-intensity work until it recovers. Health at zero ends the run at once.
3. **HR remark shows high risk.** Read the latest monthly HR remark and place it in one of three bands:
   - friendly ("you are doing all right"): no risk action;
   - quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below;
   - anything else (frowning, uneasy, "you are on your own", angry, buried problems): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is back to friendly or quiet.
4. **After a weak review (C or D) or a talk that names a gap:** until the next review, spend Energy and the main action on the stat the talk names, or on the weakest of Skill, Network and Output (Prepare report materials, Network maintenance, Skill learning; main action Apply for a key project). A second weak review in a row is the dismissal path.
5. **L4 or above:** Skill learning (2 Energy) plus one point on the weakest of Health, Dignity or Network; main action Apply for rotation. If reviews stay strong while Output stalls, swap one quarter to Prepare report materials and Showcase results.
6. **Otherwise (L1 to L3):** spend Energy on whichever of Skill, Network and Output is furthest from what the next review needs: Prepare report materials for Output, Network maintenance for Network, Skill learning for Skill while Health is comfortable. Main action Apply for a key project, which lifts all three. If Network is near zero or Wealth is near zero for months, fix that first (Network maintenance or Repair a key relationship; avoid spending), since both are published failure paths.

## Story events: read every option, then choose
Start the note with `Review in N`: the months left until the next review month, N = 6 - (current_month mod 6), and N = 6 when current_month is a multiple of 6. With N = 1 (the last month before a review), also open `reference/review-month.md` with `skill_tool` (relative_file_path) and apply it to this choice.

Then write one reading per option, the sign of what it likely does to each stat and to hidden risk, for example `2: S+ N- O0 H0 D+ W0 R+` (Skill, Network, Output, Health, Dignity, Wealth, Risk). How options usually move them:
- **Skill** rises whenever you use your own judgement: analyse, bring data or evidence, prepare properly, think a decision through, learn, design a plan, negotiate with facts, coach someone with questions. This holds for options about people or pay too, not only code.
- **Output** rises when you deliver, ship, finish or cover the work, keep to your own deliverables or make your results visible. It falls when your time or credit goes elsewhere: learning, helping or organising for others, reviewing their work, giving the credit away, apologising and redoing, pausing a delivery, complaining instead of working. Output and Network often trade against each other.
- **Network** rises when you help, involve, credit or work with others; falls when you confront, refuse, embarrass someone, go over their head or ignore them.
- **Dignity** rises when you act straight and professionally, stand your ground calmly, own a mistake or get credit; falls when you are humiliated, cave in, get blamed or gossip.
- **Health** falls with overtime, weekends, extra load and stress; rises with rest and boundaries. **Wealth** moves with pay, bonuses and money you spend.
- **Risk** rises with hiding, denying, blaming, shortcuts, gambles, fixing things privately or off the record, side deals, partial, parallel or postponed fixes, open conflict, ignoring a known problem, disengaging, and challenging the company, its culture, leaders or rules, even through a formal channel. It falls when you document, report a concrete problem, follow the process, own a mistake at once or fix the problem fully. Missing a risky option costs far more than flagging a safe one: when in doubt, mark R+.

Story rule. Apply the filters in order; skip a filter if it would remove every option:
1. Drop options marked R+.
2. If Health or Dignity is low, drop options that lower it.
3. With N = 1, drop options that lower Skill, Network or Output.
4. From the rest, choose the option that raises the most of Skill, Network and Output, counting twice the one furthest from what the next review needs and minus one for each of them it lowers. In the final quarter of the career, prefer Health, Dignity and R- instead. On a tie: R-, then more Health and Dignity, then the one that costs no money.
