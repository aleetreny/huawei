# observed-growth v10, v11 and v12 (27 Oct morning)

Same actor as v7–v9 (`017798b931bc18f8`, Haiku, CLI 2.1.310), origin `matteo`, purpose `pilot`.

## v10: L4 capped-stat rule plus Alejandro's mechanics (8 full games)

Policy `c8b245267e72ae13`. Added a "Capped" field (stats that stop rising), rotation and Skill learning once Network and Output are capped, and the promotion, Dignity, risk-trigger, money and High-intensity rules from PR #16.

- 7/8 completed, **mean Q 59.56** (v7: 57.56 over 9); scores 21.9, 51.58, 54.12, 67.04, 68.76, 70.6, 71.25, 71.25; 5 finished at L5.
- First review: 4/4 at the L1 threshold promoted, 0/4 below (Network lost just before the review).
- **The L4 rule was not executed**: Haiku always wrote "Capped: none" and "Output below best" (Output oscillates at its L4 ceiling), and kept choosing key project, report and network maintenance; at L4 Skill learning once, rotation never.

## v11: review-based Skill blocker (stopped)

Policy `4cea12436627e387`. "Capped" replaced by "Blocker: Skill" after an unpromoted review with Network and Output at their best. A stop watcher cut games that could no longer inform the L4 test (wrapper CLI refusing continuations when `STOP` exists in the run folder): four games still at L1 after the month-12 review were stopped at months 13–14. Matteo then stopped the whole batch at 09:48 UTC as not informative enough for the quota; all 8 recorded as interrupted, unscored.

## v12: exact engine rules (1 exploratory game)

Policy `e54eb82cf1bbd1b4`, from Alejandro's `motor-exacto.md` (branch `main-1nddsg`): HR remark read as the five-step hidden-risk gauge, Lay low as main action whenever HR is not smiling, never no main action, rotation as default, never High-intensity work, money guard above the first two levels, slow-failure conditions, endgame cleanup.

- Promotions at months 6, 12, 24 and 42 (L5 with an A), the fastest early career we have seen; **trust crisis at month 43, Q 50.2**.
- Rules executed only in part: rotation once, Lay low twice; key project chosen at L4 with Output already at its ceiling ("review near"); at month 42 HR was quiet and the main action was key project instead of Lay low, and HR went to uneasy in month 43 just before the second explosion; the endgame rule was applied from month 33.
- One game says nothing about performance; it shows that the allocation rules competing with "review near" are resolved towards "review near".

## Quota

Matteo's weekly window reached about 35 % on 27 Oct morning, above the lab's pace (25 %); the cap was raised temporarily for each batch and removed after.
