# BHR — Build, Hold, Repair

Matteo requested an explicit preservation mode after discussing readiness lost before reviews. We first inspected existing public trajectories without launching careers or calling a gameplay model, then wrote an English candidate at `lab/policies-src/matteo-memory/bhr/`. M1 is unchanged. BHR is not registered or queued.

Parent: M1 at commit `18b8685`; parent Skill SHA256 `3b71da85f7dd7885428150204d87268f24a128abf82d9b38f20869e45ca53a4e`. It retains M1's memory and safety duties while making mode selection and transitions explicit. BHR is a manual, not a trained model or an executable action filter.

## Offline verification

Scope chosen before counting: the entire learned-v2 first-review collection (512 careers) and the entire financial light-reserve calibration collection (512 different careers). These are existing bot archives, not v10/M1/BHR episodes. Collections use different controllers and must not be pooled into an efficacy estimate.

`archive-audit/results.json` records source SHA256s and counts. `witnesses.jsonl` retains the per-career snapshot, running best and observed loss steps, without copying event answers into the Skill. Reproduce with:

```sh
.venv/bin/python scripts/audit_bhr_archives.py --output lab/reports/bhr/archive-audit lab/reports/first-review-search/learned-v2/public-trajectories.jsonl.gz lab/reports/financial-reserve-study/calibration-v1/public-trajectories.jsonl.gz
```

| Collection | First review observed | Promoted | Non-promoted | Non-promoted with an earlier N/O loss | Non-promoted with no earlier N/O loss |
|---|---:|---:|---:|---:|---:|
| Learned-v2 | 496/512 | 336 | 160 | 157 | 3 |
| Light-reserve calibration | 512/512 | 385 | 127 | 123 | 4 |

Loss means an applied non-review transition with visible Network or Output falling at the same level. Losses also occur in **314/336** and **367/385** promoted careers, respectively. An earlier loss therefore does not establish the cause of non-promotion or that preserving everything is optimal.

The last input snapshot before the review-bearing action is below the running best of Network or Output in **130/160** and **92/127** non-promoted careers; it is also below best in **197/336** and **211/385** promoted careers. A personal best is not a proven promotion requirement. This snapshot is before the final action, not a view inside the review gate: the subsequent response may combine the choice, settlement and review. To avoid false action attribution, the audit excludes that mixed transition from its loss counts. Sixteen learned-v2 careers have no first-review message and are reported separately, not silently scored as unpromoted reviews.

Promotion is reconstructed from level change at the first public review message, not from an archive-wide promoted flag: the twelve-month calibration schema does not supply the same flag as learned-v2. Source collections and first-review outcome totals were checked against the public transitions; regression tests cover this schema difference and the mixed review boundary.

**Conclusion:** losses deserve attention, but the claim "all failures reached the cap early and then lost it" is not established. The seven no-earlier-loss failures also show why a no-loss record cannot certify readiness; they do not rule out an effect of the excluded final action or other requirements. We cannot identify true caps, universally classify readiness, infer the effects of unchosen options, or evaluate whether BHR will be followed from these archives.

Ale's already archived findings provide another caution: preserving all three stats throughout the career was unsuccessful in a small trial (2/4 completion). BHR therefore allows necessary safety trade-offs and invalidates unsupported HOLD assumptions after non-promotion. It does not impose an absolute preservation veto or a fixed month schedule.

## Candidate decisions

- BUILD is the default, with protection of already strong dimensions.
- HOLD requires a stated target and public support. Personal best alone and one zero delta are insufficient. A plateau permits only explicitly provisional HOLD with repeated comparable no-gain evidence in all three growth dimensions and no outstanding review weakness. This conservative trigger may rarely fire; its availability needs measurement.
- REPAIR records a protected deficit and targets its restoration. Restoration must be observed before returning to HOLD.
- Safety and weak-review recovery override unsupported HOLD. Non-promotion ends HOLD and triggers diagnosis; promotion resets level-specific targets.
- Each note includes MODE, TARGET with source/time, GAP and an option-specific WHY. The next observation checks what actually happened. A required lossy choice must carry an explicit exception.

The Skill is 889 whitespace-separated words versus M1's 845: the mode rules replace some dispersed wording rather than appending an extensive second manual. Word count is not a tokenizer or cost invoice.

## Adherence is not yet demonstrated

A future actor assessment must score execution separately from outcomes. The proposed rubric is in `adherence-rubric.md`; no decisions have been scored under it and no model was called. Static lint only checks submission format/content constraints; software tests validate the archive analysis. Neither proves an actor will follow BHR or obtain a promotion.

Validation: lint reports no findings. Full software suite: 302 passed with the existing Authlib deprecation warning. No simulator internals were inspected.

## Relevo

Completed: read-only audit of 1,024 existing public careers, reproducible counters and per-career witnesses, separate BHR candidate and prospective adherence rubric. M1, v10, older bundles and frozen research protocols remain unchanged. No games, model calls, registry writes or automation. Only Matteo's T4 row is updated; commit/push and existing PR #12 request integration into main.

Next step, if authorised: freeze BHR and M1 hashes, actor/runtime and a new case set before testing. Use an initial no-game archived-prefix actor assessment to measure mode entry/exit, source correctness, note length, exceptions, ambiguous cases and choice/reason consistency. Calls still consume model quota. Then an independently scheduled matched full-career comparison is needed for promotion/survival and cost effects; static preservation claims are not counterfactual proof. Do not restart the paused Haiku study or register BHR automatically.
