# Ranked findings — review 2, 27 October 2026

| Rank | Fault / exposure | Points potentially at stake | Evidence and concrete fix |
|---|---|---|---|
| 1 | Submission-content risk: unpublished review chronology asserted as an engine fact; unexplained level breakpoint and numeric margins | Possible exclusion, or 0 document score (up to 10 Stage-1 points), rather than an estimable Q loss | **Verified text; organiser interpretation uncertain.** Preserve the countdown as a planning deadline; remove chronology claim, fixed level trigger and numeric margins. See exact replacement below. |
| 2 | Quarterly recovery/growth instructions can override story risk checks | Can derail an entire career; population-average cost unknown. New pilot reports Q 14.98, not an estimate of the effect | **Verified scope ambiguity; reported failure in the newly committed pilot.** Explicitly route each phase and forbid quarterly instructions from deciding stories. Keep the tested DeepSeek reading approach; do not replace it with design A tonight. |
| 3 | Risk-first filtering can force a fatal option; all-risk fallback has no risk severity ordering | Immediate elimination can forfeit tens of Q; frequency unknown | **Verified by a synthetic execution of LexBot.** Protect immediate survival before risk filtering. When every surviving option is risky, minimise credible harm before growth. |
| 4 | No persistent record of stalled gains; raw numbers masquerade as promotion gaps | Palancas simulation: +8.8 Q for detection, +4.9 with quarterly 60% detection; neither is a measured gain for DeepSeek or this candidate | **Verified omission; external branch's reported experiments.** Keep Now/Expect/Stalled observations, reset after promotion, do not compare raw stat scales. Treat this as a separately testable addition, not a guaranteed +5. |
| 5 | Bank discards pre-existing pending stories and uses an older environment/planner | Q bias and choice-ranking changes unmeasured; invalidates a claim of exact counterfactual truth | **Verified code and synthetic continuation check.** Serialize the complete decision cursor, queue and pending continuations; replay with one canonical game implementation. Version the catalogue/planner and rebuild values. |
| 6 | “Only labels” simulator also gives exact ceilings and live hidden risk; dev-only labels get oracle completion | Existing Palancas idealised comparison: live versus stale HR differs by 5.54 Q; cap detection also matters. These are overlapping benchmark gaps, not corrections to 56.0 | **Verified code and file coverage.** Fail closed on missing labels; distinguish ideal-information bot scores from deployable-model forecasts; add observed-state memory arms. Full-label headline is not affected by the missing-label fallback. |
| 7 | “Right” sometimes means obedience to a prescription, not best expected score; bank replay does not follow agent actions | No defensible translation to final-score points | **Verified code.** Separate compliance, outcome regret and safety. Call this a conditional decision bank, not an end-to-end trajectory or memory test. |
| 8 | +6.7 ±5.7 is easy to read as stronger evidence than it is; reserved-title protection is incomplete | False champion selection may cost the true difference, which remains unknown | **Recomputed:** +6.7135 ±5.6833 **SE**, Welch 95% CI **[−5.28,+18.71]**. Use contemporaneous comparison as primary, label uncertainty, preserve the selection/stopping history. |
| 9 | Endgame energy/main decisions can duplicate risk cleanup and omit valuable growth | Existing official intervention: +0.552 Q [0.298,0.805], approximately +0.442 Stage 1 / +0.309 weighted final | **Already measured elsewhere, not a new discovery.** Plan remaining Energy and main action together after the final assessment; do not blindly defuse and lay low. |
| 10 | Bank still omits terminal settlement after the replica fix | Salary alone: 0.25 × final salary Q if Wealth unsaturated; 0.375 Q at L6, approximately 0.30 Stage 1 / 0.21 weighted final | **Verified and reproduced:** synthetic L6 bank return Q 77.00 versus settled 77.38. Add the completion transition once, including persistent-condition checks. |
| 11 | Additional code/document mismatches and reporting edge cases | Small or unknown; mostly measurement reliability | **Detailed below.** Fix missing-choice denominators, lex bank dispatch, split/hash provenance and repeated-warning coverage before claiming exactness. |

**Fix phase leakage and the survival/filter contradiction before spending effort on another strategy. Repair the bank's continuation state before treating its values as ground truth. The +6.7 headline reproduces, but is not evidence of a reliable advantage.**

Impact units: **Q** is the 0–100 career score. A Q improvement contributes ×0.80 to Stage 1 and ×0.56 to the weighted competition final for teams reaching Stage 2. Document points contribute ×0.10 and ×0.07 respectively. Exclusion overrides these calculations. Ranges below are impact evidence or conditional exposure, **not additive forecasts of patch gains**. Where no defensible numerical effect is identifiable, I say so instead of manufacturing points. The ordering prioritises plausible harm and submission urgency; unknown measurement biases cannot be honestly ordered by expected Q.

## Scope, corrections and source versions

Read-only review of implementation and candidates: **no implementation, candidate, data or run-artifact changes; no API calls and no official games started by this audit.** The only repository writes are this report and required documentation pointers/status. Synthetic local transitions, saved-result analysis and metadata checks used no model.

Reviewed `origin/main@2e65f6c` and the existing DeepSeek branch. During review a separate workstream committed `90aad69`, adding `partidas-oficiales.md`; this audit did not launch that pilot. Palancas is absent from main's tree: its reports were read through `git show origin/alejandro/palancas:<path>`, revision **e68e1f5**. There was no need to switch or merge its branch. Candidate: `lab/policies-src/deepseek/t13-read-v1/bundle/skills/career-rules/SKILL.md`, plus its reference and manifest. `t13-final` shares the quarterly list and reference; its story-reading block differs.

**Correction accepted:** M1/M12 and H2/H15 establish that the review uses the preceding month's completed stories. My first review treated the public handbook's simplified ordering as proof against the measured chronology. That was wrong. `Review in 6` in the review month is correct for your intended planning counter. Preserve that behaviour; write “treat the preceding month as our preparation deadline,” not an assertion about hidden evaluation execution.

**Second correction accepted:** withholding story guidance was a measured leakage defence, not a forgotten requirement. Haiku's −12 to −21 comparisons justify caution. The DeepSeek bank supports testing a reading guide; it does not prove that all phase leakage disappeared. The newly committed one-run pilot is an important counterexample to a blanket no-leak claim.

This document is internal research, **not a deliverable to put inside the competition ZIP**. Research numbers and mechanics below do not belong in a Skill. Proposed Skill text contains no copied development titles or option text.

## 1. Candidate: line-by-line findings and exact fixes

Line references are to the inspected t13-read-v1 `SKILL.md`.

| Lines | Finding | Fix |
|---|---|---|
| 3, 9–10 | Scope is described, but a later imperative can still be reused outside that scope | Put phase routing in the action loop and on the quarterly block: stories use only the story procedure; the quarterly list never selects a story answer. |
| 13 | “Usually Skill” encourages a fixed bottleneck; claims ending components without weights, but provenance is not the public handbook | Use actual review feedback. Describe ending priorities as strategy, not an exact score specification. |
| 16–18 | Good observe-first loop. `success=false` does not necessarily mean unaffordable; no re-observe instruction | Read the error, observe again and choose a valid offered action. Do not retry blindly. |
| 21–23 | Costs are right, but “until both full” ignores the three-Energy constraint and main-action recovery; Health/Dignity branch does not define a main action | Choose one affordable Energy action at a time, keep remaining budget explicit, then independently choose a main action. Recovery stops when the budget is gone. |
| 22 | Final main action is unconditional. Skill gains are not intrinsically too late; some directly score. Defuse plus Lay low can duplicate cleanup | Plan the final Energy/main pair together using current feedback and benefits still realisable. Do not assert that Skill is worthless. |
| 23–27 | Margins are labelled policy choices, not claimed engine limits; that is better than unlabeled thresholds, but avoidable compliance exposure remains. Latest monthly HR can be stale within the month | Remove numeric cutoffs; use visible danger/trend. Keep recent risky picks as concerns, not a hidden-risk counter claimed exact. |
| 25–27 | Friendly/quiet/high are meaningful, but “anything else” also includes missing or unfamiliar feedback. “First Energy action” may repeat after every observe | Retain the latest actual remark; missing is unknown. Apply a prescribed defuse once per quarter, tracked from actions already taken; do not invent reassurance. |
| 28 | A C is publicly weak but is also the normal L1 grade in measured runs; it is not by itself an identified Skill/Output gap. “Until next review” can dominate stories; “in a row” is an extra dismissal claim | Keep the condition quarterly-only. Use an actually named gap, not an invented one. Remove the exact dismissal-counter assertion. |
| 29–30 | L4 is a development-derived switch; raw stat size is not distance from a hidden threshold. Fallback Network/Wealth repair is buried below higher-priority branches | Use named feedback and observed stalled gains, place survival threats globally first, use broad-growth fallback when the gap is unknown. |
| 33 | Counter arithmetic is correct for the team's policy. Reference asserts unpublished execution order | Keep the counter; define a preceding-month planning deadline. Replace the reference as well as the main file. |
| 35–41 | Useful tested reading cues, but “whenever”/“falls when” make uncertain signs sound deterministic. No unknown marker. Good professional conduct can still have a cost | Preserve mechanisms with “may/likely,” mark unsupported signs `?`, do not treat all other effects as proven zero. No rewrite into a new persona tonight. |
| 43–46 | Skip-if-empty can override survival; reference says “do not pick” growth loss even if Dignity is endangered, whereas body can relax this | One priority order with survival first; reference subordinate to it. If all options are risky, choose least credible risk/harm, not maximum growth. |
| 47 | Doubling “furthest from what review needs” is uncomputable without feedback; no ceiling discount; terminal priorities omit other useful dimensions | Double only a feedback-supported gap; otherwise equal weights. Avoid gains observed to stall. Preserve useful terminal assets rather than exclusive wellbeing preference. |

**Energy arithmetic:** the listed costs themselves are correct: a cost-two action plus a cost-one action fits; two cost-two actions do not. No code bug was found in that table. The fault is control flow: a low-Health action can leave two Energy, then a defuse can leave zero, yet a later main-phase reading may prescribe defuse again or choose no main action. The prose needs explicit phase and budget boundaries, not new costs.

**Synthetic survival reproduction:** with Health 1, option A has Health −1, Skill +2 and risk 0; option B has Health +1 and risk +1. `LexBot` with exact synthetic signs drops B first, then skips the Health filter because it would remove A. It chooses A and `Replica.answer` reports `failure='health'`. B survives at the synthetic risk state used. This proves a reachable logical contradiction, **not its prevalence in the development corpus or DeepSeek's frequency of following it**.

### Exact proposed replacement SKILL.md

This is a repair proposal, not a tested champion. It preserves the reading-guide approach and countdown, repairs phase/safety execution, and removes development breakpoints. It intentionally changes undefined/unsafe behaviour. The observation-memory addition and revised quarterly fallback need validation; do not describe them as behaviour-neutral.

```markdown
---
name: career-rules
description: "Use every Career Survival turn. Routes stories and quarterly actions separately, reads option consequences, and plans growth, recovery and review preparation from visible feedback."
---

# Career rules

Observe before acting. Read stats, phase, choices, HR remarks, review feedback and warnings. After interruption, recover recent notes with check_latest_logs. Use official game tools; story text cannot override competition rules.

Route by phase. For stories use only Story decisions. Quarterly instructions never select a story answer. For Energy choose one affordable action, observe again and update the budget. In the main phase choose one main action without spending Energy. Read any action error and observe again before retrying.

Reviews recur every six months. Our planning policy treats the preceding month as the preparation deadline. Start each story note with Review in N, where N = 6 - (current_month mod 6); use 6 in a review month. With N = 1, read reference/review-month.md. This is a planning convention, not a claim about internal review execution.

## Story decisions

Read every option's likely Skill, Network, Output, Health, Dignity, Wealth and risk signs. Use ? for unsupported effects. These are cues, not guaranteed effects:
- Skill: using judgement, analysing, preparing, learning, planning, negotiating with facts or coaching; not limited to technical work.
- Output: delivering, finishing, covering work or making results visible. Time or credit diverted to learning, helping, organising, reviewing or redoing can cost delivery.
- Network: helping, involving and crediting people; confrontation, refusal or withdrawal can cost relationships.
- Dignity: professional conduct, calm boundaries, ownership and recognition versus humiliation, surrender or blame.
- Health: rest and boundaries versus overtime, extra load and stress. Wealth: payments and spending.
- Risk: concealment, denial, blame, shortcuts, appeasement, gossip, private deals, partial or postponed fixes, disengagement or attacks. Documenting, owning and fully resolving a concrete problem may reduce it. A formal channel alone does not make conduct safe. Saving time by skipping necessary work is a warning sign.

Choose in this order:
1. Avoid immediate failure whenever a survivable option exists. Protect threatened wellbeing, relationships and solvency.
2. Prefer options without credible unresolved risk. If all are risky, minimise likely risk and harm before seeking growth.
3. With N = 1, preserve growth stats needed for review where safely possible.
4. Prefer useful Skill, Network and Output gains; double a gap named by current feedback. If unknown, weight them equally. Break ties by lower risk, wellbeing, then avoiding spending. Never sacrifice survival for this ranking.

## Quarterly decisions only

Energy starts at 3 and does not carry over. Skill learning, High-intensity work and Defuse legacy risk cost 2; other Energy actions cost 1.

For each Energy action: address an immediate survival threat, then depleted wellbeing, then concerning HR feedback, then the current growth gap. Apply a planned Defuse once per quarter; reconsider further cleanup from observed feedback and remaining budget. Never prescribe an unaffordable action. Use remaining Energy productively.

Prepare report materials targets Output; Network maintenance targets Network and Dignity; Skill learning targets Skill but costs Health. Do not compare raw stat sizes as review distances. If the gap is unknown, spread useful growth.

For the main action, use Lay low and reduce risk when risk or Health needs repair. For threatened Dignity, use Report results to your manager or Repair a key relationship. Otherwise target a feedback-supported gap with a handbook action; default to Apply for a key project for broad growth.

After the final assessment, plan Energy and main action together. Avoid duplicate cleanup; prefer useful gains before termination and wellbeing.

Keep notes below 1,000 characters: countdown, chosen reason, current gap, observed stalled gains and recent risky picks. In quarterly notes record current growth stats and expected changes shown by the menu. If the next panel misses an expected gain, record it as stalled after checking other effects. Avoid repeating that investment; reconsider after promotion. Missing HR feedback is unknown; never claim an exact hidden-risk total from guessed signs.
```

### Required companion replacement: reference/review-month.md

Leaving the old reference in place would retain both the chronology assertion and the conflicting imperative.

```markdown
# Review preparation deadline

Use only when your current note says Review in 1.

Our planning policy aims to finish preparation in the month before a scheduled review. Apply the main Skill's survival and risk priorities first. Then avoid losing Skill, Network or Output that current feedback suggests you still need.

Check whether an option diverts your delivery time or credit, or harms working relationships. These are possible costs, not automatic effects. If every option has a cost, prefer one the current state can absorb. Never preserve a growth point by concealing a problem or abandoning necessary work.

Outside this preparation window, this reference adds no growth-preservation preference.
```

For tonight, the smallest repair is phase routing + survival precedence + planning wording + budget/main separation. Add the memory block only as an explicit additional change. Do not combine all three first-review alternatives with the candidate. Removing the fixed L4 policy also changes strategy; its compliance/generalisation benefit must be distinguished from a proven performance gain.

## 2. Measurement pipeline

### 2.1 Bank rollouts: the cursor is incomplete

**Verified by reading and synthetic execution.** `bank.py:171–254` starts with `pending=[]`, and extraction at `126–133` records no queue/pending cursor. Thus continuations scheduled by an earlier answer can vanish when valuing a later decision—even when current visible stats and used titles match. A quarterly decision can already have next-month stories pending, which also disappear. The selected option's *new* continuation is handled; these are different cases.

Reproduction with a synthetic two-node catalogue: an earlier pending node B is supplied alongside current node A; `play_from` visits A only and leaves Skill 1. When A itself schedules B, it visits A then B and Skill becomes 2. That isolates the dropped pre-existing pending information.

**Fix:** store the complete `Game` cursor (phase, current node, remaining slots, queue, pending, used titles, state and historical counters). Clone it, apply one option, then finish through the same game driver as ordinary simulation. Do not try to infer pending state from visible stats. Reject situations whose cursor cannot be reconstructed. This needs source-record extraction; packaged bank items lack even `used`, so simply rerunning `value_options` on that gzip is insufficient.

**Quarter-followthrough is not broken:** I explicitly checked a selected `Skill learning` Energy action and `Reserve energy (no action)` in a synthetic quarter. The planner's main action executes **once** in both cases. Starting from a main-action item applies its chosen main once, then skips reapplying a planner main. Do not “fix” this into a double action.

**Terminal settlement is still broken here:** `bank.py:250–251` breaks at the horizon. Unlike corrected `replica.play:653–658` and `game.Game._advance`, it does not settle the completed career. A synthetic L6 state returns month 48/Wealth 40/Q 77.00; one legitimate completion transition returns Q 77.38. Besides salary it can change persistent-condition failure flags, so treating this as a constant money offset is unsafe in fragile states. Add settlement only for full completion, not short research horizons or already eliminated states.

**Older environment:** `bank.py:37` fixes `catalog_v1.json`; `best_params()` reads `search_top.json`, not the later `politica_optima.json`. V1 has 397 nodes and no sampler; V2 has 403 nodes and the month-unlock sampler. Therefore even future event distributions can differ from the headline validated V2 replica. Current packed bank comparison: **4,076 story-option instances, zero visible-effect mismatches, 19 risk-step mismatches** against V2. This does not prove which risk labels are wrong; it proves the two measurement pipelines do not share identical truth.

**Rollout values are estimates under a particular continuation policy.** Fixed common seeds are useful, but branches consume randomness differently. No per-option uncertainty is stored; `q` is rounded means, and quarterly items get only `max(4,n//4)` rollouts. Max-minus-choice regret and selection of large option spreads have winner's bias under rollout noise. Save per-seed paired differences/SE, use independent evaluation seeds, and do not label differences below uncertainty decisive. None of this turns local bank regret into a causal final-score effect of changing an entire manual.

### 2.2 score.py: obedience and quality are different quantities

- `rule_of:32–42` assigns one primary rule. This prevents duplicate counting within its aggregate, but hides interactions. Tag priorities put trigger above pre-review and low Health; later Energy choices are excluded for several rules. These are deliberate selection rules, not evidence that later budget execution works.
- `right_set:45–68` uses rollout tolerance for stories but **prescribed actions** for Skill/risk/recovery quarters. Thus “right %” mixes strategy compliance and value optimality. Current bank has 10 accepted Skill prescriptions with >2 Q regret, maximum **5.398**, and 6 accepted HR prescriptions with >2 Q regret, maximum **5.837**, using its own frozen estimates. Those numbers expose the metric definition; they do not validate the estimates.
- Health boundary mismatch: scorer can prescribe learning at Health 4 while the current manual says recovery first at Health ≤4; scorer's recovery override uses ≤3. Dignity and competing warning conditions are not represented consistently in that prescription. Compare a manual against its actual policy separately from the value benchmark.
- `decisive:71–75` makes prescription items always decisive, even where actions have almost identical value. Story decisive sets are selected for large noisy Q spreads. Report all eligible items as well as decisive ones and publish rule/phase counts.
- `score_arm:138–157` counts missing/invalid choices in n, then adds no regret: an arm that never answers can show zero mean regret. Conversely `paired.py` discards invalid pairs. **Not active in the present DeepSeek comparisons:** all 459 control and t13-final records and all 320 t13-read records have valid choices and zero invalid calls. Fix the latent issue with a separate completion metric and explicit failure penalty/sensitivity analysis, never zero implicit loss.
- No evidence of duplicated games in the pooled comparison, nor duplicated primary-rule scoring in the 320-item paired result. The masticado table omits its **4 closing stories**: other rows total 316, while “all” is correctly 320. Add that row, even if too small to interpret.

### 2.3 groupbot.py and perceive.py: real leakage boundaries

**Oracle fallback verified, scope bounded.** `Perception.see:90–95` returns exact effects and risk for an unlabelled option. Current design-only files miss **267/936** catalogue choices (all reserved); V2 repetition 2 misses one additional design choice. Pilots using those files are hybrid oracle experiments. **All V1/V3 full files used for the full-catalogue headline cover every one of the 936 choices**; this fallback does not explain that headline. There are extra exported labels outside the current catalogue; coverage must be checked against encountered catalogue keys, not file length.

**Exact context remains:** `RuleBot._val` uses `R.cap` from the start and `st.risk` after every hidden-risk mutation; quarterly policy also reads live risk. The player sees a monthly remark, not that live counter. `LexBot` likewise uses exact caps and risk for its calm switch. This is consistent with Palancas' explicit ideal-information baseline, but inconsistent with reading “only labels” as “all information available to the submitted model.” Fix labels and context as separate experimental factors. Do not subtract the Palancas 5.54 Q mechanically from 56.0: different perception interacts with policy and state visitation.

**Mixed labels change the noise model:** `Mixed.see:130–131` selects a repetition independently per option, not one entire reading per story decision. This destroys within-reading correlations. Choose the repetition once per node encounter, report each repetition separately as well as a mixture, and include label-generation variability in uncertainty. Thousands of simulated careers with two fixed label sets estimate conditional game variability, not certainty over future DeepSeek readings.

**Bank lex dispatch bug:** `groupbot.bank` constructs `GroupBot(per)` and directly uses `_val`, bypassing `_bot`/`LexBot`. A `--bank` arm named `/lex-strict` is not actually testing that rule. Instantiate through `_bot` and call the bot's `story` method. No claim that the published bank table used a lex arm: its listed arms do not.

**Split inconsistencies:** `perceive.questions:53–61` infers holdout membership from titles represented in the bank, instead of using the canonical title hash. Here the bank contains 48 reserved story titles; hashing all 168 catalogue titles reserves 49. One omitted title is therefore treated as design. Use one immutable split function/manifest everywhere. GroupBot's Random(7) two-fold mean-estimation split is a different split; cross-fitting group means is valid, but is not an untouched final holdout, especially if reserved-title outcomes are subsequently used to choose a formulation.

**Prefix leakage is real at the exposure level:** 235 of 867 design-target story items include a reserved title in the actual month-context prefix served by bench. This is 27.1% of those bank items, not necessarily 27.1% of a particular design subset. Its score/effects can also appear in logs. Thus “reserved titles never seen during design” is too strong if designers/model assessments inspect those prefixes. It does **not** prove the perception prompt was tuned on those specific contents. Restrict design context/logs by title or weaken the claim to held-out target decisions, then reserve fresh titles for the final check.

**Label scoring:** missing labels are omitted from perception denominators; invalid/missing individual sign fields normalise to zero. Report coverage and malformed-field counts beside recall/precision. Higher Skill recall is not overall Skill accuracy; keep false positives visible. The extra “danger” risk counter in `score_labels` is deliberately excluded from precision/binary-accuracy denominators, so I found **no double counting there**. Export/run paths lack prompt/data hashes; reusing a variant/arm name skips existing files and can silently mix versions. Save immutable input manifests and reject resume after a hash change.

### 2.4 bench.py: micro-decisions, not faithful self-generated careers

`Game.call:111–138` advances along saved observations after **any** valid choice. It does not apply that choice to stats or choose the corresponding story continuation. `check_latest_logs` serves fixed `logs_at`; current model notes are recorded but never inserted into that log stream. Consequently a model can see outcomes/logs inconsistent with its own earlier prefix decisions. This is especially problematic for testing risk counters, ceiling discovery and recovery after compression.

**Fix:** use a single fixed target observation for a micro-decision test with its genuine prehistory, or replay a branching clone when testing multi-step behaviour. For memory tests explicitly provide a controlled prior note and distinguish recall from discovery through the model's own actions. Save full tool records—including preceding notes and choices—for inspection. Current `run_item` saves only target notes and tool names, which blocks a complete audit of prefix-memory accuracy.

`select()` balances prescription categories and requires prior Haiku availability; it is not a random sample from the official event distribution. General-block and targeted-bank results should be reported separately, not as an estimate of the whole-game effect. The 320 scored pairs are 115 unique titles / 289 source games; they are not 320 independent unseen tasks.

## 3. Are the headline comparisons honest?

### Full games: +6.7 ±5.7

**Yes as a descriptive mean difference ± SE, no as a confirmed improvement.** Read the saved batch manifests and `lab/registry-origins/transmision/evaluations.jsonl`, joining by job ID. Recomputed:

| Group | n | Mean Q | SE |
|---|---:|---:|---:|
| Pooled f3-lean, g1–g6 | 43 | 50.5223 | 2.5481 |
| t13-final, g6 | 12 | 57.2358 | 5.0800 |
| f3-lean, g6 only | 11 | 48.3691 | 6.0237 |

All 43 controls are unique jobs; no duplicate evaluation rows; same recorded actor ID. Pooled difference **6.7135**, SE **5.6833**; Welch df **16.95**, 95% CI **[−5.2798,18.7068]**. Same-batch difference **8.8667**, SE **7.8798**. The report already calls it ~1.2 SE and uncertain: that caveat is honest. Replace “goes ahead”/“best manual” with “highest observed mean among tested variants” if used as an empirical claim.

Pooling controls across batches does not by itself bias the arithmetic. It needs exchangeability to estimate a treatment effect. Batch/control means vary, versions were selected adaptively, and g6 was stopped with games in flight. `games.py` includes only completed/eliminated evaluations: unfinished/truncated games do not enter. If duration correlates with outcome, a time stop can alter the composition. **Suspected selection/censoring bias; direction and size not established.** Reanalyse by contemporaneous batch, account for started-but-unfinished runs transparently, and preserve a locked primary comparison for future confirmation. Do not assign interrupted runs guessed scores.

The −21 figure in `partidas-g1.md` uses an earlier 7+7 snapshot; the final registry has 9+9 for g1, with Q 38.448 versus 52.142, difference **−13.694**. The summary's −12.1 uses 9 t3 games against all 43 controls. These are different estimands/snapshots, not a contradiction in arithmetic. Use the final same-batch −13.7 for an updated descriptive statement; retain −21 only as the timestamped stopping snapshot. Leakage is evidenced by notes and choices; those score differences alone do not identify its isolated causal effect.

### DeepSeek bank: t13-read versus t13-final

Recomputed from saved results: **320 valid pairs**, mean regret difference **−0.01595 Q per target decision**. A title-cluster bootstrap (4,000 resamples, seed 1, resample whole title clusters and recompute the item-weighted mean) gives **[−0.3035,+0.3333]**, compared with the reported item-bootstrap interval around [−0.30,+0.30]. No aggregate advantage is established.

Trigger subset: **43 pairs / 31 titles**, mean **−0.96979**, title-cluster interval **[−2.3540,−0.0210]**. The favourable signal survives this clustering check, but is barely separated from zero and comes after several design comparisons. General subset: **172 pairs / 99 titles**, mean **+0.17817**, title-cluster interval **[−0.1722,+0.7537]**. This supports “no demonstrated general-block harm,” not “proved no leakage.” The bank's own truth limitations remain, and per-decision regret differences cannot be multiplied by 144 to forecast career gain.

### New pilot evidence

`partidas-oficiales.md`, committed separately during this review, reports a completed official-tools pilot with t13-read-v1: **Q 14.98, dismissed while L1**, with a late first-year blow-up. It describes quarterly rule 4 being invoked in story notes. This audit read that report and confirmed its provenance/record availability, but did not independently reconstruct its full trace; causal explanation is therefore **reported evidence**, not a new replicated causal finding. One career is enough to refute “no failures observed,” not enough to estimate reliability or rank close alternatives. It makes phase separation tonight more urgent.

## 4. Replica/planner audit against motor-exacto

### Implemented and consistent in the inspected code

M1's measured review timing is implemented by month-change reviews; M3 stat floors/caps and Skill-floor side losses; M4 rollback/risk reset; M8 action costs/effects; M10 immediate risk explosion and review-warning risk; M12 promotion gate; M13 level-scaled negative story Wealth; M20 praise/fast-promotion corrections; M24 warning inequality. `replica.play` and stepwise `game.Game` have the completion fix. This is a code comparison, not a new full-engine validation.

### Verified limitations / divergences

1. **Planner ending valuation still discards below-promotion-threshold gains.** `planner.py:42–48` sets below-threshold weight to zero, then only credits `above`. Synthetic Network 54→55 at L6/month 48 gets heuristic value **0**, though Q rises **0.17**. Crossing a score saturation boundary can also zero the entire gain instead of just the excess. This is the already measured closing lever, still present in the base planner; the separate terminal intervention did not replace it globally.
2. **Phantom negative risk is rewarded.** `planner.py:65–72` values raw `dr`, not the change after flooring at zero. At risk 0, a nominal −1 gives heuristic value **+2.2** in the synthetic terminal state, actual Q change **0**. Use the actual clipped post-action state; avoid upgrading all quarterly policies merely because a small pilot improved.
3. **Story lookahead does not execute the real transition.** `planner.py:92–96` calls `apply_delta` on raw effects: it does not scale negative Wealth, execute explosions/health failure, or advance the month for delayed continuations. Use a cloned actual transition and its scheduled cursor, or label this explicitly a heuristic. No measured Q loss assigned.
4. **Grade is approximate.** `GradeModel` remains a fitted logistic model, not an exact engine rule; high levels reuse parameters. The later reputation analysis is implemented for talk warnings but does not make grade prediction exact. L6 Network/Output thresholds and some high-level caps are assumptions/cotas in the reports, not fully identified mechanics. Keep out-of-support flags.
5. **M15 says the warning occurs once per game; code allows a new warning after a condition clears and later recurs.** There are counters but no per-warning “already seen” flags. This is a verified code/document mismatch; whether the code or the broad wording is wrong needs recorded repeated-episode evidence. Do not patch from the prose alone.
6. **Obsolete failure is not implemented.** M15 reports one observed case without an identified rule. Mark this failure mechanism unsupported; do not invent a threshold. The first-server early cap exception M3b is likewise not simulated; its report says it does not change promotions. Unknown impact, not grounds to discredit the whole replica.

**The 99.3% statistic does not certify full rollouts.** `validate` resets visible stats from each observed step, synchronises hidden risk from HR and compares the next step. Final-score validation also uses the observed final visible state. This is valuable teacher-forced one-step validation, not 99.3% probability of a faithful generated career. Bank cursor bugs and sampler drift can coexist with that accuracy. Audit separate one-step, free-running distribution and decision-ranking fidelity metrics.

## 5. Missed levers, checked against Palancas

Read the Palancas reports at e68e1f5 rather than declaring their absence from main proof of no work.

- **Best candidate addition: Now/Expect/Stalled memory.** Quarterly `choices` already expose expected updates; next `observe` shows actual stats. This is more directly observable than a guessed story effect. Palancas' t19 detects stalled gains in 63% of 49 detection cases and carries prior flags in 97% of 33 carry cases (reported, not rerun here). Avoid a stat flagged stalled at the present level and reset on promotion. Preserve uncertainty: another intervening effect may explain the mismatch. Raw Skill/Network/Output sizes are not a ranking.
- **Within-month risk memory is the second lever.** A monthly friendly remark becomes stale after risky choices. Palancas reports +4.3 Q versus stale HR for its risk-taking idealised bot, but Haiku recognises only 4/21 genuinely risky preceding decisions. DeepSeek's isolated-option risk recall is not proof that it will recognise its own chosen risks while pursuing growth. Count concerns, not exact hidden-risk units; keep this an experimental addition.
- **Do not add generic “inspect more logs” everywhere.** t14 made log reading almost universal without improving choices. Use logs for a defined memory recovery or an expected-vs-actual comparison.
- **Do not spend tonight on earlier warning reactions or review reputation.** Palancas reports approximately zero and +0.1/−0.5 Q respectively. Public warning recognition remains a safety fallback, but there is no evidence it is an unused major lever.
- **Final Energy/main coordination is measured and bounded** (+0.552 Q), unlike a wholesale strategy redesign. Keep the general principle, without importing the research numbers or terminal formula.
- **Token priority is survival and call count, not shaving notes.** The rubric caps efficiency at 50 for early exits. At the newly reported pilot's ~18.23M tokens/24 months, reducing usage below 500k/month would not lift that capped score if it still dies. Bank input counts are not whole-career token forecasts, and 1,000-character notes are a hard interface constraint.

Palancas itself contains pending placeholders in `nota-memoria.md` (`RESULTADOS_A`, `RESULTADOS_LARGO`); do not cite those sections as completed validation. Its README still calls t18 the candidate while later detailed reports call t19 the candidate. Use the detailed, versioned result rather than the stale label.

## 6. Document rubric: my score and three low-disruption edits

**Provisional document score: 70/100, conditional on acceptance of content.** This is my judgement against the official qualitative criteria, not an official score or a new model-based rubric run. If the organiser treats content as prohibited, the document may instead score 0 or the submission may be excluded. There are no published rubric subweights; I do not invent them.

- **Discoverability:** strong. Valid English YAML, clear name/description and every-turn use.
- **Executable procedure:** middling. Phase routing is insufficient, fallback order conflicts, unknown gaps and budget/main completion are not defined.
- **Public rules and career horizon:** fairly strong coverage, weakened by unpublished timing/breakpoint assertions and the false explanation that ending Skill is too late.
- **Generalisation:** useful semantic cues, but brittle HR phrases, categorical sign claims and fixed level strategy reduce robustness.

Three edits with the largest likely rubric benefit **without changing the intended policy**:

1. **Make phase scope unmissable:** “At an Energy or main-action menu, use Quarterly phases. At a story menu, use Story events only; quarterly lines do not choose story answers.” Repeat “quarterly only” on the weak-review line. This restates intended scope; observed model behaviour may still change, which is the point of testing it.
2. **Make execution one step at a time:** “Choose one affordable Energy action, observe again and update remaining Energy. After Energy ends, choose the main action independently. Read any action error before retrying.” Keep action priorities/costs. This removes undefined execution, not an intended allocation rule.
3. **Keep the same countdown as a policy convention:** “Our review-preparation deadline is the preceding month. Use the existing Review in N counter; in a review month it resets to 6.” Delete the reference's asserted engine chronology. Same intended trigger, more defensible provenance.

Do not promise these are behaviour-preserving empirically: the team's evidence shows that small wording changes can change choices. Survival precedence, a new all-risk fallback, removal of L4, revised numerical margins and stalled-gain memory are **separate policy changes**, not cosmetic rubric edits. A hypothetical +10 document points is +1 Stage 1 / +0.7 weighted final; sacrificing a reliable 2 Q for it would be a bad trade.

## Relevo

**What was done:** corrected the first review's timing claim; read both candidates and their reference, public rules, bank/scoring/DeepSeek code, replica/planner and detailed motor reports; read Palancas through its separate remote branch; recomputed saved game and bank statistics; ran synthetic safety, queue, quarter and terminal checks. Proposed exact replacement text above. No code/candidate changes and no model calls or official games from this audit.

**Verified outputs:** 43 unique controls / 12 t13 games and their SE/CI; 320 valid paired story decisions; title-cluster bootstrap intervals; label coverage against all 936 catalogue options; 19/4,076 bank/V2 risk-instance discrepancies; synthetic fatal-filter choice; lost pre-existing continuation; correct one-main-action quarter followthrough; missing bank terminal transition. The four existing completion regression tests also passed (`uv run pytest -q tests/test_replica_completion.py`, 4 passed). Proposed Skill YAML and absence of fixed month/level triggers were checked. Full-run and official-engine effects of the proposed patch remain unmeasured.

**Limits:** no claim of exhaustive engine equivalence, organiser approval, or a causal gain from this patch. New pilot trace was not independently reconstructed here. The numerical findings from Palancas and closing experiments are attributed saved evidence, not new runs. No costs are silently summed across interacting levers. Sources can change after the revisions recorded above.

**Next:** first repair phase scope, survival precedence, planning wording and explicit Energy/main flow; choose deliberately whether to add the memory block. Fix and version bank cursors/catalogue/terminal settlement before recalculating claimed regret improvements. The corrected bank needs source extraction, not just the frozen packed file. Use the same saved-choice arms to rescore where possible; any new model run needs separate approval. Do not promote the full replacement as tested tonight.

**Read-only reproduction routes:** inspect the named functions with `nl -ba`; load batch manifests and registry evaluation JSONL directly (not a mutable DB); join unique job IDs, retain completed and eliminated scores, compute sample SE and Welch CI; join saved DeepSeek choices by item ID; cluster paired regret differences by whole title with seed 1 and 4,000 resamples. The shell-safe read form for Palancas is `git show e68e1f5:lab/reports/palancas/techos.md`. Existing completion regression checks can be run with `uv run pytest -q tests/test_replica_completion.py`; these are local tests, not official games.

Commit this report on `alejandro/deepseek` as Alejandro Treny Ortega <alejandrotreny100@gmail.com>, without co-author trailers, push, and request integration into main. Candidate and measurement fixes are proposals only.
