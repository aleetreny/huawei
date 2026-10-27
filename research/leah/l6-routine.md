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

## Not done, and what to check

- **No game played yet.**
- `reference/review-month.md` is only read by the `#official` mode of the Claude CLI actor, which is on `alejandro/transmision` and not yet on `main`. A game from `leah/workspace` would not see it. The fair test is Alejandro's setup: his obedience bank and his interleaved games against t10-countdown and f3-lean-v1.
- **What to measure** (also in `policy.json`):
  - share of key projects in L1–L3 quarters (prediction ≥ 90%);
  - Skill learning at L1–L3 (prediction under 5% of Energy actions);
  - promotion at the first review;
  - mean Q against t10-countdown.
- **Refuted if** there is no gain in first-review promotions and no better mean Q in the same batch, or if the routine isn't followed (key project in under 70% of L1–L3 quarters).

## Relevo

1. **Done.** `l6-routine-v1` written as a one-line variant of t10-countdown; lint has no errors and the tests pass.
2. **Data.** None yet.
3. **Open.**
   - The manual depends on t10-countdown, which is on `alejandro/transmision`.
   - Its `parents` field names `t10-countdown`, which has to be registered first.
4. **Next.** Alejandro adds it to his T20 bank and games:
   ```bash
   scripts/transmision/drive.sh <items> <ids> <slots> l6=lab/policies-src/l6-routine/l6-routine-v1/bundle
   ```
   For a quick check from this branch that Haiku follows line 5, one game under origin `leah` is enough; the review-month reference won't be read there.
