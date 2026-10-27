# Free tests planned after phases 1 and 2

Research only; no proposed Skill files and no model/API calls. Use the team's replica and saved full DeepSeek label sets, not official engine packages. All outcome numbers are conditional simulator results.

1. Information intervention: compare frozen noisy predictions, exact risk signs, exact growth signs and exact all signs with a common decision rule/context. If repairing perception cannot close the gap even with perfect execution, the assumed bottleneck is incomplete. Compare full growth preference with a loss-only controller that removes anticipated positive growth benefits; this can refute a robust-to-unknown-benefits strategy.
2. Feedback versus maintenance: compare lagged-HR controllers with a fixed quarterly cleanup schedule, using the same saved story perception. Repeat with risk recognition blinded to test whether maintenance can substitute for classification. Preserve health recovery and do not use actual within-month risk to trigger the observed-controller actions.
3. Within-run learning: calibrate broad group/predicted-stat associations from one's own subsequent visible outcomes only; skip month/level transitions and ambiguous capped zeros. No training across careers, future/unchosen labels, event-identity lookup or exact hidden-risk feedback. Compare against the same fixed label baseline. This is a cheap implementation of one narrow learning mechanism, not a test of all possible language-based learning.

Initial screen: 800 seeds per arm from 831000, two saved label readings selected as a whole per encounter using a stable hash. Every arm uses the same initial seed list; event streams may diverge after choices. Report paired mean differences, SE, completion, failure types and first promotion by reviews. Report ideal-context versus observed-context assumptions separately. No choosing weights by looking at evaluation outcomes.

A possible confirmation uses new seeds only if an initial screen justifies another run. Never infer paid-model obedience from a scripted controller.

## Confirmation plan after screen, before new seeds

Screen suggests the missing control boundary may matter as much as labels. Confirm on 2,000 fresh seeds from 951000 with fixed arms: observed, loss_only, scheduled, online, hard_risk, true_all_hard, true_all, live_risk, exact_caps, true_all_ideal. New hard-risk arms remove predicted positive-risk options when a predicted survivable/nonpositive-risk option exists, before value ranking. They retain the same label predictions and tie breaks; perfect-sign versions are diagnostic ceilings. Context factors isolate exact current risk versus exact caps. No weight fitting or new labels. This is an additional hypothesis from the screen, not a preregistered initial result.

## Combined mechanism check

After the confirmation, test the combined contract (hard predicted-risk admission before ranking, with positive growth rewards omitted) against observed/hard-risk/loss-only on 1,000 new seeds from 1011000. No new weights. This tests whether the two mechanisms combine; report the new result separately rather than attaching it to the earlier confirmation.
