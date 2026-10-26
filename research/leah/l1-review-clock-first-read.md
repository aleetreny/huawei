# l1-review-clock-v1: first read (1 Haiku game)

Leah, 26 Oct 2026, origin `leah` on Leah's Mac.
- **Manual:** `lab/policies-src/l1-review-clock/l1-review-clock-v1/` (policy `f1830961d168beb9`).
- **Game:** `leah-scre-f1830961-614d6e-00000-a2`, played 16:31–16:46 UTC.
- **Player:** Claude Haiku through the lab's `claude-cli` worker. The settings match the race's Haiku cell, but this Mac runs CLI 2.1.295 on a Pro account; the race uses 2.1.303 on Max.

One game is an impression, not a result: the race's own Haiku games range from 49 to 72.

## Result

| | Score | Completed | Level | Wealth | Health & dignity | Skill | Risk control | Network |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **l1-review-clock-v1** (1 game) | **60.9** | 1/1 | **15.0** | **8.2** | 15.0 | 12.0 | 5.0 | 5.7 |
| Race leader F3 (3 Haiku games) | 64.2 | 3/3 | 15.0 | 7.5 | 14.8 | 13.0 | 6.7 | 7.2 |
| Race, all completed Haiku games (30) | 59.5 | — | 13.7 | 6.8 | 14.8 | 11.6 | 6.0 | 6.6 |

Points per dimension are averages over completed games, out of weights 30 / 20 / 15 / 15 / 10 / 10. F3's three games scored 66.6, 59.7 and 66.3.

The game ended at L5 with Health 10, Dignity 10, Skill 96, Network 34, Output 28 and Wealth 32.9. Its list-price cost was $1.28 for 204 actions in 15 minutes.

## Did Haiku follow the manual?

Counted by `scripts/leah/behaviour.py` from the worker's own transcript.

- **High-intensity work:** never used. ✔
- **Main action:** Apply for a key project in 13 of 15 quarters, with one Lay low and one Report results. ✔
- **Health reserve:** Health was 10 at 11 of 15 quarterly main actions and never below 7. ✔
- **Energy:** Prepare report materials 20, Network maintenance 10, Health recovery 7, Defuse legacy risk 5, Mental recovery 1, Reserve 1. Network maintenance isn't in the manual; Haiku used it as its catch-up for Network.
- **Promotions:** L2 at month 6, L3 at 12, L4 at 30, L5 at 48.

## What it says

1. **Promotion and pay are on par or better, but the game still lost.**
   - Level points matched F3's average (15.0) and wealth was higher than any comparison (8.2 against 7.5).
   - The score was 3.3 below F3's mean because of **risk control (5.0 against 6.7)** and **network (5.7 against 7.2)**.
2. **Risk control is the clearest gap.** The game ended with half the risk-control points. Defuse legacy risk ran only 5 times, because the manual triggers it only on a worried HR remark or a warning. F3 defuses whenever any risk signal appears and keeps doing so while signals repeat.
3. **L4 took 18 months (month 12 to 30).** That's the same stall Matteo's runs showed. Output stalled at about 26 from month 34 onward, while Skill kept rising.
4. **Network finished at 34**, with three drops in the final quarters, and earned under 60% of its points.

## Next ideas (not yet tested)

- **v2, risk:** Defuse at least once per half-year whenever the HR tone isn't relaxed, and in the last quarters before the end, so risk control closes clean.
- **v2, Output:** when Output stops growing for a quarter, switch the main action to Report results to your manager or Showcase results for a quarter.
- **More games of v1 first:** 3 games are queued and held (`leah-scre-f1830961-614d6e-0000{2,3,4}-a2`). Playing them would show whether 60.9 is typical.
