# Skills design — Gradient Depression

**Draft for Cut 1, 27 October 2026. Intended package location: `design/skills_design.md`.**

**TODO(final):** reconcile this document with the frozen `t13-read-v2` Skill and reference files, record its version, and resolve every marker before packaging. The combined manual is being assembled; evidence below concerns its predecessors and components, not a validated final version.

## 1. Our understanding of the task

Career Survival asks a single agent to sustain a career while developing it. The public handbook describes a 48-month horizon, monthly story choices, quarterly Energy and main actions, and six-monthly reviews. Growth competes with wellbeing, working relationships and financial resilience. Story outcomes are uncertain before choosing, so professional-sounding language alone is insufficient evidence of a safe or useful consequence.

We separate three questions: what does this option probably change, what does the current career need, and which instruction applies in this phase? Our research found failures at all three layers. More detailed strategy did not automatically improve play: instructions could be followed in the wrong context, and correct priorities could be applied to misread options.

The agent uses the current run's observations, offered choices, handbook, review feedback, HR remarks, warnings and recent logs. Its memory consists of observations and labelled concerns, not supplied promotion requirements or a numerical model of hidden risk.

## 2. One Skill with explicit phase boundaries

The intended architecture has one discoverable `career-rules` Skill, used throughout the career. It contains the action loop, quarterly priorities, story-reading guide and note format. A small review-preparation reference isolates a narrower preference.

One Skill avoids selective loading: earlier multi-Skill experiments showed that the agent could retrieve one relevant-looking rule while missing another. In the Transmission and DeepSeek bank evaluations, the consolidated Skill was retrieved consistently. Consolidation does not remove interference, so the first decision is always which phase is active.

**TODO(final):** confirm whether `reference/review-month.md` remains separate and ensure its priorities agree with the main file. The design uses a single agent on JiuwenSwarm 0.2.4b3; reference retrieval is not delegation.

The intended turn loop is: observe, select the phase-specific procedure, choose one valid action, record a concise note, then observe again. A rejected action prompts inspection of the error and refreshed choices. Quarterly instructions must not decide a story answer.

## 3. Quarterly priorities: executable resource allocation

The public action menu gives costs and effects, making quarterly allocation more explicit than story interpretation. The priority list addresses threats to survival, depleted wellbeing and concerning feedback before growth. Growth targets a gap supported by review feedback rather than whichever raw stat is numerically smallest. Different stats have different scales.

Energy and the main action are separate decisions. The agent spends only affordable Energy, updates the remaining budget after each action, and then chooses a main action. It considers their combined benefits to avoid paying twice for the same repair.

This structure follows the strongest instruction-delivery result: concrete, ordered quarterly directions were followed much more reliably than loosely stated goals. DeepSeek's agreement with two tested allocation prescriptions rose from approximately 2% and 15% without the Skill to 65% with it. These are compliance measurements, not proof that every prescription maximises score.

**TODO(final):** match the exact priority order, affordable-action fallback, main-action routing and final-stage coordination to the implemented version. A separate randomised development experiment (600 careers) found a 0.552-point improvement in gain from entry to the closing stage, with a 95% confidence interval of 0.298–0.805. Its unadjusted whole-career difference was inconclusive; transfer into prose remains untested.

## 4. A self-computed review switch

The agent writes `Review in N`, calculated from the visible month and public review schedule. Our policy treats the preceding month as the preparation deadline. The counter activates the additional review-preparation check only in that window; it does not assert an unpublished rule about internal review execution.

This explicit switch addresses instruction leakage. In early proxy-model experiments, visible story rules changed approximately one in five unrelated choices. Computing and recording the switch confined the narrow review preference more successfully than simply writing “only before a review.” DeepSeek was less consistent, so we do not assume the switch isolates instructions perfectly across models.

The review check remains subordinate to survival and risk control. Protecting career progress must not become a reason to accept an immediately fatal choice or conceal an unresolved problem.

## 5. Read consequences before selecting benefits

The story guide asks for likely directions of change in Skill, Network, Output, Health, Dignity, Wealth and risk. It distinguishes capability development from completed delivery and relationships from mere agreement. It asks what action is actually proposed, including its costs, rather than rewarding a reassuring tone.

DeepSeek initially detected only about 45% of Skill-increasing and 49% of Output-increasing options in our perception tests. General reading cues raised Skill-increase detection to about 78%; Output remained difficult. That motivated a focused guide rather than further strategic detail. A six-stat reading also preserved more useful distinctions than broad behavioural categories in our conditional simulator benchmarks.

Risk is considered alongside benefits. We avoid teaching potentially hazardous conduct as an attractive route to growth. In a separate paired simulator experiment, such framing reduced average score from 53.2 to 48.1 and increased trust-crisis outcomes from 73 to 174 per 1,000 simulated careers. This supports caution about wording; it is not a prediction for the submitted manual.

**TODO(final):** confirm the guide's exact uncertainty notation and fallback order. The intended procedure protects immediate survival, considers unresolved risk, applies the scoped review preference, then compares useful growth. If all options have costs, it chooses a recoverable trade-off rather than silently dropping safety.

## 6. Notes as compact, revisable memory

The proposed status line contains `Review in N`, `Now`, `Expect`, `Stalled` and `Risky this month`.

`Now` records observed growth stats. `Expect` records the result implied by a chosen quarterly action's displayed updates. Comparing the next observation with that expectation can identify an investment that has not produced the anticipated gain. `Stalled` retains that observation for reconsideration; it is not proof of a permanent limit. A promotion prompts reassessment. The agent should not compare raw stat sizes as a ranking of need.

Palancas' proxy-model tests motivated this format. Writing an expectation improved mismatch detection from 16% to a reported range of 49–63%. Previously recorded information was carried forward in 97–100% of tested cases. Simulated benefits were promising, but the final DeepSeek combination has not inherited those scores merely by including the fields.

`Risky this month` counts choices the agent itself considered concerning. It does not measure hidden-risk units or establish that a calm remark has erased earlier concerns. This field's practical usefulness depends on recognising one's own risky decisions, which was weak in the proxy tests.

**TODO(final):** confirm which fields survive in the final manual and their reset/reassessment rules. Keep the status first and the entire note within 1,000 characters. On resumption, retrieve enough recent log entries to find the last valid status; a log-entry count is not a decision count.

## 7. Generalisation, scope and limits

The Skill ships guidance, not development-event mappings or executable research scripts. Any retained reference is short, scoped and in English. General decisions depend on current feedback and observed consequences; the submission does not supply hidden thresholds, scoring formulas or fixed event answers.

The main risks are misperception, rule leakage, stale memory and overreaction to an uncertain observation. These are reasons to preserve explicit phase boundaries, uncertainty and reassessment, not to add more unsupported rules. Token economy also favours concise notes and purposeful retrieval. The companion decision report distinguishes component evidence from whole-career validation.
