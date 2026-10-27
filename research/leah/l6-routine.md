# l6-routine-v1: the L6 bots' first-year routine, written the T20 way

Leah, 27 Oct 2026, branch `leah/workspace`. Manual: [lab/policies-src/l6-routine/l6-routine-v1/](../../lab/policies-src/l6-routine/l6-routine-v1/).

This is the optional idea in Alejandro's independent-chats plan (`research/careerlab/chats-independientes-2026-10-26.md`): "a first year like the bots that reached L6".

## Where the idea comes from

Of the 400 T10 energy bots, 4 reached L6 and finished with Q 67–76. No LLM game has passed L5 ([lessons.md](../../lab/fastloop/lessons.md), Frontier).
- **Promotions.** All four were promoted at each of the first three reviews (L2, L3, L4), despite a C at the first one.
- **Their play had no judgement:**
  - main action always Apply for a key project;
  - Energy on a fixed mix every quarter. Two used Health recovery, Mental recovery and Prepare report materials, one Defuse legacy risk and Health recovery, and one an adaptive mix;
  - stories took the first listed option, a lab device that must never be a Skill rule.

The lesson that can be passed on is the quarterly routine: the same allocation every quarter, a recovery point even when nothing looks wrong, and a key project every time.

## What the manual is

A copy of Alejandro's `t10-countdown` (T20, branch `alejandro/transmision`) with **one line changed**. t10 is the manual Haiku obeys best on his bank:
- Skill at L4: 77% obeyed;
- HR remark: 60%;
- final month: 83%;
- the review-month story rule sits behind a `Review in N` countdown, so it doesn't spill into other stories.

| Line | t10-countdown | l6-routine-v1 |
|---|---|---|
| 1–4 (final month, low Health or Dignity, HR remark, L4 and above) | as written | unchanged |
| 5 (everything else, in practice L1–L3) | Energy on whichever of Skill, Network and Output is furthest from the next review; main action key project | **Energy in a fixed order: Health recovery, Mental recovery, then Prepare report materials, every quarter; main action key project; no Skill learning, Network maintenance or High-intensity work at these levels** |
| Story countdown and `reference/review-month.md` | as written | unchanged |

The new line follows the T20 writing rules (`lab/reports/transmision/resumen.md`):
- it is imperative and names the exact game actions;
- the condition is visible on screen (the level);
- it is defined by exclusion ("when no line above matched"), so the first-match order stays the priority;
- it adds no story rule, so it can't change other story choices.

**Why this one change.** "Lift whatever is furthest from the next review" asks Haiku to judge which stat is behind. In the f3-lean-polish game, that judgement sent 26% of Energy to Skill learning, which stalls at L1, and the career never left L1. A fixed routine needs no judgement, and it is what the bots that reached L6 did.

## Checks

- `uv run careerlab lint lab/policies-src/l6-routine/l6-routine-v1`: no errors. Its 4 REVIEW notes ("final month", "4 or less", "multiple of 6", "last month") all come from t10's inherited lines, kept unchanged to stay one change away from t10.
- `uv run pytest -q`: 302 passed.
- SKILL.md is 447 words; the reference file 168.

## Smoke test: one Haiku game (27 Oct, 15:45–16:25 UTC)

Job `leah-pilo-32466d29-614d6e-00000-a1`: policy `32466d290c42d2f6`, actor `claude-cli:haiku`, origin `leah`, purpose `pilot`. It is outside every decision and only checks whether line 5 is obeyed. Checked with [scripts/leah/line5_check.py](../../scripts/leah/line5_check.py).

**Line 5 was obeyed every time it applied.**

| Month | Line that applied | Energy | Main action |
|---:|---|---|---|
| 3 | 2 (Health 3) and 3 (non-mild HR remark) | Health recovery, Defuse legacy risk | Lay low |
| 6 | 3 (uneasy HR remark) | Defuse legacy risk, Network maintenance | Lay low |
| 9 | **5** | Health, Mental, Report | key project |
| 12 | 3 (quiet "some risk" remark: Defuse, then main as below) | Defuse legacy risk, Report | key project |
| 15, 18, 21 | **5** | Health, Mental, Report | key project |

- **Line 5: 4 of 4 quarters exactly as written**, and no Skill learning at all. The other 3 quarters went to higher lines, which is correct under first match.
- Key project in 5 of 7 L1–L3 quarters (71%). That clears the refutation bar (70%) but misses the prediction (90%), and the 2 misses are Lay low from the risk line, not disobedience.
- After every quarterly routine the stats were back at the L1 ceiling: Skill 9, Network 3, Output 3.

**The game was lost anyway:** dismissed at month 24 at L1, grades C C C D, Q 23.0. At every review month one stat was a point short:
- month 6: Output 1;
- months 12 and 18: Network 2;
- month 24: Network 2 and Output 2.

Each time, the point was lost in a story event during the two months before the review, after the stats had been at the ceiling. That is the same failure Matteo found in v7.

**Why this test can't judge the manual.** The rule against that failure lives in `reference/review-month.md`. On this branch's actor Haiku can't open it. It wrote `Review in 1` correctly every time, then "Reference file unavailable, so judgement" in 12 notes. The game was missing the one rule that protects the review. That's why a fair test needs Alejandro's `#official` actor.

**Tokens.** 5.13 M over 24 months, about 214k a month (cache reads 5.0 M), 194 turns, list price 0.084 USD. That's below the polish game's 278k over the same 24 months.

## What to check in Alejandro's setup

- **What to measure** (also in `policy.json`):
  - share of key projects in L1–L3 quarters (prediction ≥ 90%);
  - Skill learning at L1–L3 (prediction under 5% of Energy actions);
  - promotion at the first review;
  - mean Q against t10-countdown.
- **Refuted if** there is no gain in first-review promotions and no better mean Q in the same batch, or if the routine isn't followed (key project in under 70% of L1–L3 quarters).

## Relevo

1. **Done.**
   - `l6-routine-v1` written as a one-line variant of t10-countdown; lint has no errors and the tests pass.
   - One Haiku smoke test: line 5 obeyed 4 of 4 times. The game was lost at month 24 on pre-review story losses, with the reference rule unreadable on this branch.
2. **Data.**
   - `lab/registry-origins/leah/` (exported);
   - live view in `lab/panel/live/game.json`;
   - transcript outside Git under `~/careerlab-data/huawei-leah/runs/leah-pilo-32466d29-614d6e-00000-a1/`.
3. **Open.** `parents` is empty because `t10-countdown` isn't registered on this machine. The lineage is in `idea_origin`. Set `parents: ["t10-countdown"]` once t10 is registered.
4. **Next.** Alejandro adds it to his T20 bank and his interleaved games, where the reference file is read:
   ```bash
   scripts/transmision/drive.sh <items> <ids> <slots> l6=lab/policies-src/l6-routine/l6-routine-v1/bundle
   ```
   Don't play more games of it from `leah/workspace`: without the reference rule they measure a different manual.
