---
name: commitment-ledger
description: Keeps a compact ledger of open storylines, promises, risks and weak dimensions in every take_action note and plans each quarter's Energy and main action together, with steady-balance priorities. Use on every turn and after a context reset.
---

# Commitment ledger

Consequences can arrive months later; a written record of what is open prevents inconsistent follow-ups and wasted quarters. Priorities are steady balance: no dimension stays weak, slides are repaired early.

## The ledger
Start every `take_action` note with the full ledger, rewritten rather than appended, then one short reason clause:

`LEDGER open: <storylines in progress> | promised: <commitments> | risks: <accumulated or legacy risk warnings> | weak: <Act and Watch dimensions> | plan: <quarter plan>`

Use a few words per item and drop resolved items. If a note is rejected as too long, shorten it.

## Each turn
1. `observe`. Note Level, Health, Dignity, Skill, Network, Output, Wealth and the `events` feedback; compare with earlier observations to see each statistic's direction. Update the ledger.
2. After a context reset, or when unsure of the ledger, call `check_latest_logs` once with a small count and copy the latest ledger.
3. Classify every dimension:
   - **Act**: Health or Dignity in the lower part of its 0–10 range; Network or Wealth at or near zero; named in a warning; Output after a C or D review.
   - **Watch**: falling across recent observations, or clearly the lowest of Skill, Network and Output.
   - **Fine**: everything else.
4. Decide, then `take_action` with the exact `choice` number and the ledger note.
5. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.

## Story events
- If the event continues an open storyline, keep your promise unless new feedback shows it is harming you; then change course openly and record why.
- Rule out options whose described downside hits an Act dimension, unless every option does; then take the mildest downside.
- Among the rest, prefer the option that helps the weakest dimension, then the one with the broadest modest gain. A steady gain beats a large gain with a lasting cost.
- Prefer honest, workable commitments; avoid options that postpone a problem or add risk you cannot see.
- Between equal options, prefer one that closes an open item; with several items open, avoid new commitments.

## Quarterly plan
At a quarter's first Energy step, read `energy_cost`, `status_updates` and `remaining_energy`, then write in `plan` both the Energy actions and the intended main action:
1. Act dimensions first: Health recovery for Health, Mental recovery for Dignity, Network maintenance for Network.
2. Then Watch dimensions, with the action that lifts the weakest without lowering an Act or Watch dimension. Skill learning and High-intensity work cost Health; use them only while Health is Fine.
3. For a warning in `risks`, include Defuse legacy risk once, then drop it unless the warning returns.
4. Spread points across dimensions instead of stacking one. Unused Energy is lost, so spend it while a useful affordable action remains.
5. Main action: Pick the action whose listed effects cover the weakest dimensions that Energy did not reach. Choose Lay low and reduce risk only when Health is Act. Repeat a main action only while the same gap persists.

Follow the plan; change it only when `weak` or `risks` change.

## Across the run
- Keep the same discipline from the start of the run to its end. Promotion needs sustained Skill, Network and Output, so balance is also the route to higher Level and salary.
- After a C or D review, add Output-producing actions until the next review while keeping the recovery rules.
- Late in the run take no new risks: a failure or a collapsed dimension costs more than a last gain.
- Near the end, close open items and open no new ones.
