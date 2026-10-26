# Career Survival Agent: evidence and competitive strategy

Research date: 26 October 2026. Team: Gradient Depression. This is a development research document, not a tested solution or submission. Recommendations are hypotheses until evaluated. Public sources are linked beside the claims they support.

## 1. Recommendation and evidence standard

Build a reliable single decision-making agent with a small number of executable Skills, explicit handling of persistent risk, compact memory and public-rule-based quarterly planning. Spend development compute on comparing and improving general decision procedures. Prefer a repeatable improvement over an exceptional development run.

The investigation used 19 Exa search queries requesting 200 results, followed by direct reading of the official documentation and selected primary sources. Those are search-result slots, not 200 independent validated studies. The [search audit](search-audit.md) preserves candidate discovery, including irrelevant results. This is broad coverage, not a claim to have found every historical contest or every private solution.

Evidence categories used below:

- **Published requirement:** the current UK official documents.
- **Observed project fact:** the local repository and reviewed teammate branch.
- **External precedent:** a primary author account, competition page or original research paper.
- **Proposed hypothesis:** our own strategy or arithmetic, requiring validation.
- **Unresolved permission:** an approach for which the organisers must clarify the rules before use.

## 2. The actual optimisation target

For an evaluated version, let `Q1,Q2,Q3` be the three official `quantitative_score` values, `D` the mean Skill quality and `E` the mean token-efficiency score. All components use a 0–100 scale:

`A = 0.80 × mean(Q1,Q2,Q3) + 0.10 × D + 0.10 × E`.

A team's Stage 1 result is its highest valid issued automated version score. Only the ten highest Stage 1 teams advance. For those teams, `F = 0.70 × A + 0.30 × expert_review`. Effective final weights are therefore 56% play, 7% Skill quality, 7% token efficiency and 30% expert review. `competition_partial_score` already contains a separate 0.7 factor and is not the input to `A`. [Official evaluation](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html).

Consequences derived from that published formula:

1. A ten-point improvement in mean game outcome adds eight Stage 1 points and, for an advancing team, 5.6 final points.
2. A ten-point improvement in Skill quality adds one Stage 1 point and 0.7 final points.
3. A ten-point improvement in expert review adds three final points, conditional on qualifying.
4. Duplicating a scored submission does not buy new independent official rolls. Earlier unscored versions can be superseded by a later one before the same cutoff.
5. A strong three-run mean matters. One high local game does not estimate it reliably.

The expert component is large, but cannot rescue a team outside the top ten. Develop game reliability first while collecting evidence for the design report and video throughout the week. Do not leave the video until qualification: it is mandatory in every final ZIP. Reviewers have no published separate subweights for video versus design versus Skills. [Submission requirements](https://techarena-career-sim.readthedocs.io/en/latest/submission.html).

Survival is a strong proposed priority, not a mathematical substitute for the score: early exits still receive a quantitative outcome. An excessively defensive agent that completes with weak career outcomes can lose to a better-balanced policy. Compare actual mean outcomes and failure patterns rather than treating completion alone as proof of optimal play.

## 3. What the game makes public

A complete run spans 48 months. The default month has up to three story events. Quarterly phases provide three Energy points and an optional main action; unused Energy does not carry forward. Formal performance reviews and promotion windows occur every six months. Progression should be sustained; the exact promotion formula is not public. [Handbook](https://techarena-career-sim.readthedocs.io/en/latest/handbook.html), [public rules](https://techarena-career-sim.readthedocs.io/en/latest/rules.html).

Visible state includes Health and Dignity on 0–10 scales, Skill, Network, Output, Wealth, Level, Energy and CurrentLevelDuration. The public salary schedule increases with level, creating a plausible benefit to earlier sustainable promotion: a promotion can affect later monthly income as well as final level. That economic reasoning is our inference, not a claim that maximising promotion speed maximises the hidden final score. [Salary and reviews](https://techarena-career-sim.readthedocs.io/en/latest/rules.html).

Published failure directions include zero Health, persistent critically low Dignity, accumulated organisational risks, repeated weak performance, prolonged zero Network, prolonged negative Wealth and insufficient Skill relative to expectations. Except where explicitly public, exact counters and thresholds remain unknown. Ending dimensions include level, wealth, health/dignity, skill, risk control and network; the ending report exposes their contributions. [Failure and endings](https://techarena-career-sim.readthedocs.io/en/latest/failure-and-ending.html).

This makes the task naturally interpretable as sequential decision-making with partial information and resource constraints. That is an analytical description, not a published mathematical model of its internals. A good agent must manage both immediate resource depletion and delayed consequences.

## 4. The boundary around formula discovery

The official interface permits `new_game`, `observe`, `take_action`, `check_latest_logs`, `show_employee_handbook` and the exposed log resource. Manual public CLI testing and reading outputs of one's own runs are permitted. Direct inspection of engine/data packages, internal source, packaged data, local simulation databases or hidden evaluation state is prohibited. [Binding fair-play rules](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#official-interfaces-only).

The separate hard-coding prohibition matters even when access was legitimate. Submissions may not contain fixed named-event answers or unpublished formulas, thresholds, probabilities and trigger conditions presented as known rules. The rules explicitly say the prohibition does not depend on how the knowledge was obtained or described. The agent must decide from current-run public observations and feedback. Rewording an event, hiding a mapping in a reference file or calling a recovered constant a heuristic does not establish compliance. [Hard-coded knowledge](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#prohibited-hard-coded-answers-rules-and-thresholds).

Therefore there are three distinct questions:

| Activity | Status supported by the documents | Recommended treatment |
|---|---|---|
| Improve general priorities after reviewing permitted own-run outputs | Supported development activity | Start here; retain current-run reasoning and no event-answer tables. |
| Respond qualitatively to current-run deterioration or warnings | Explicitly aligned with public guidance | Core agent behaviour. |
| Enumerate affordable public action descriptions mentally or in a proposed planner | Public information is available | Evaluate actual available choices; any executable submitted script must satisfy environment rules. |
| Run millions of automated calls, concurrent sessions or non-LLM bulk experiments | Not expressly authorised by the pages reviewed | Obtain written organiser clarification first. |
| Fit numerical models of hidden dynamics, retain cross-run learned coefficients or distil them into the policy | Rules create substantial uncertainty; current-run basis is required | Clarify before using the method; do not package inferred internals. |
| Read a public post that reveals engine internals and incorporate its findings | Prohibited source cannot become permitted knowledge by republication | Exclude it. |
| Inspect or change the database or exploit restart behaviour | Outside permitted process | Do not use. |

The documentation requires asking organisers when a method is ambiguous or unaddressed. It does not make a million-call experiment lawful merely because the transport is MCP. This is a competition-rule assessment, not a legal opinion. [Interpretation process](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#interpretation-and-questions).

## 5. What brute force can and cannot do

Three different resources are often conflated:

1. **Search over prompts and policy designs:** generate alternatives offline, then test the promising few under the official environment. Potentially valuable; no hidden answers should be carried forward.
2. **Search over public quarterly combinations:** a small constrained decision problem. Potentially valuable even with qualitative effects, especially for avoiding inefficient Energy allocations.
3. **Search through actual game trajectories:** exponentially large, costly and not branchable through the documented interface. Mass experimentation also needs clarification.

Calling `observe` repeatedly on an unchanged session usually obtains no new transition evidence. Calling `take_action` advances the actual session. The documented tools do not provide state cloning, undo, arbitrary state initialisation or a seed parameter. Do not invent them or simulate their existence by copying the database. Another MCP client is permitted during development, but that does not make an alternative evaluation platform valid. [MCP interface](https://techarena-career-sim.readthedocs.io/en/latest/mcp.html).

POMCP and MCTS are attractive in partially observable games, but require a generative mechanism to sample hypothetical continuations from a belief state. A live irreversible session does not provide that capability. A surrogate model would add prediction error and permission questions. Full online MCTS is consequently a low-priority choice this week. Receding-horizon qualitative planning—plan, take one allowed action, observe and replan—is feasible without claiming numerical simulation accuracy. [POMCP original paper](https://proceedings.neurips.cc/paper/2010/hash/edfbe1afcf9246bb0d40eb4d8027d90f-Abstract.html).

The [search arithmetic document](budget-and-search.md) quantifies the trajectory explosion and the much smaller quarterly space. More compute helps only if its evaluator is informative and its result can be used under the rules.

## 6. Why recovering an equation is not the same as winning

Even ignoring permission, a numerical pattern in this dev environment need not identify the true mechanism:

- Visible state may omit accumulated risks and history.
- A change after an action can combine the action, month advancement, pay, review and other settling effects.
- Caps, rounding and nonlinearities can make different formulas indistinguishable on the states reached.
- The agent's own policy controls which states are observed, producing selection bias.
- One transition does not reveal the unchosen counterfactual.
- The official test can change parameters and event composition.

Symbolic regression searches expression space for compact empirical fits; it does not prove that the recovered expression is the environment's rule or that it extrapolates. PySR is an example of a real tool for this scientific task, not a recommendation to deploy recovered game formulas. [Original PySR paper](https://arxiv.org/html/2305.01582v3), [development/evaluation distinction](https://techarena-career-sim.readthedocs.io/en/latest/packages.html).

If the organisers approve a research-only modelling experiment, specify its exact use, dataset provenance, validation split and whether any fitted information reaches the submission. Prefer a modest predictive claim with uncertainty over an exact-rule claim. Until then, study broad strategy failures rather than fitting hidden thresholds.

## 7. Reset: no Skill architecture selected

The user withdrew the former proposal and requested starting from zero. Its manifest, design document and both Skill files have been deleted locally. The previous design is no longer the baseline or recommendation. Current work begins with manual gameplay, review of Matteo’s existing random-simulation evidence, and an experiment registry. Any decision procedures below are hypotheses, not a selected Skill implementation. See [the current lab plan](from-zero-lab.md).

## 8. Proposed decision procedure

Use the same single agent for planning and critique; a risk-checking Skill is an instruction module, not a separate teammate. The UK restriction is stricter than some older related examples. Do not enable team execution or assume an older `agent.plan` configuration is valid. [Platform requirements](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#required-jiuwenswarm-version-and-run-mode).

At each decision:

1. Read the current official observation. Identify the month, phase, exact available choices and relevant warnings.
2. Update a compact record of visible trends, unresolved warnings, recent reviews and the current strategic priority. Separate observed facts from uncertain interpretation.
3. Check immediate and persistent vulnerabilities. Avoid an option that compounds a serious existing problem when a credible alternative exists.
4. Identify the present growth bottleneck using public criteria and current-run outcomes. Weak review feedback with adequate wellbeing suggests rebalancing toward work capability, results or relationships; it does not identify a hidden promotion threshold.
5. Compare a few plausible available options by their documented/textual effects, reversibility and effect on future choices. Treat unspecified effects as uncertain.
6. Run a brief internal risk audit and select an option exactly as offered.
7. Act once with a short useful note. Observe the result and update the record.

If an action call times out, do not blindly repeat a mutating call: observe or check logs to determine whether it already happened. If parsing fails or the assumed option disappeared, refresh the official state and select again. Tool reliability is part of strategy because a perfect plan is irrelevant when actions are invalid.

## 9. Compact memory as an experiment

Proposed record, expressed only through permitted current-run information:

```text
Month / phase / level:
Current visible statistics and trend since last relevant observation:
Unresolved warnings, each linked to observed feedback:
Most recent review and whether the corrective action helped:
Current priority and alternative considered:
Remaining quarterly Energy and intended main-action complement:
Uncertainty to check on the next observation:
```

Do not preserve a transcript-sized history or reuse hidden empirical rules from previous games. A record of warnings and trends is more actionable than repeated long narrative reasoning. Within-run feedback can update priorities; certainty should not increase simply because the agent repeats a guess.

Reflexion and Voyager provide primary evidence that feedback and reusable skills can improve agent behaviour in their studied environments. They do not prove that an expanded memory or executable skill library improves this competition. Our test is whether a small record improves complete-run outcomes without bloating context or causing stale assumptions. [Reflexion](https://arxiv.org/abs/2303.11366), [Voyager](https://arxiv.org/html/2305.16291v2).

## 10. The quarterly phase is a high-value planning target

The public Energy budget is small and action costs are known. High-intensity work and skill learning use two points; defusing legacy risk also costs two. Network maintenance, mental recovery, health recovery and report preparation cost one. Public effects are directional; exact gains and hidden side effects are not given. [Quarterly rules](https://techarena-career-sim.readthedocs.io/en/latest/rules.html#quarterly-energy-actions).

Proposed method: compare whole-quarter packages rather than spending each point greedily in isolation. Use the current bottleneck to choose a shortlist, then re-evaluate after every actual action. Examples of general plans include recovery plus capability growth, relationship support plus review preparation, or explicit risk reduction plus recovery when current-run warnings support it. These are state-dependent categories, not fixed sequences keyed to events.

Coordinate Energy with the main action. If a main action can support results and relationships, Energy might be better spent on a neglected dimension. Conversely, a health-supporting main action may allow an otherwise appropriate learning investment. Actual outcomes must be observed before committing to the remainder.

Do not infer that an action with more published positive signs dominates another. Magnitudes, prerequisites, latent costs and future effects may differ. No direct statistic effect is published for defusing legacy risk, so a one-step visible-delta metric could systematically undervalue it.

## 11. Phase awareness without a rigid calendar policy

Three useful questions change over the career:

- Early: which capability investments and relationships can create durable options while maintaining stability?
- Around reviews: what does sustained recent feedback suggest is limiting progress?
- Late: which actions still have time to pay off, and which dimensions should be protected for the ending?

These are planning questions, not prescribed month-specific answers. Continuing development can matter late, and recovery can matter early. The public final score dimensions justify considering terminal balance; they do not publish the exchange rate between wealth, level or wellbeing. [Handbook](https://techarena-career-sim.readthedocs.io/en/latest/handbook.html), [ending dimensions](https://techarena-career-sim.readthedocs.io/en/latest/failure-and-ending.html#completing-the-run-and-ending-evaluation).

## 12. Use LLMs as candidate designers and failure analysts

The most relevant pattern from GEPA is to read execution traces, diagnose a concrete failure, propose a targeted instruction change and evaluate it. That is stronger than asking for a universally cleverer prompt. AlphaEvolve similarly depends on an objective evaluator that selects useful candidate changes. [GEPA paper](https://arxiv.org/abs/2507.19457), [AlphaEvolve research account](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/).

Apply the idea manually or with lightweight development tooling rather than replacing JiuwenSwarm with a different framework. Produce at most a few distinct hypotheses per iteration: e.g. earlier response to persistent deterioration, clearer prioritisation of Skill versus Output after reviews, or reduced repetitive log retrieval. Reject revisions that add hidden formulas, event-specific answers, unsupported actions or contradictions. Test the resulting English Skills with the required model and platform.

Competition credit is restricted to the designated model and competition activity. Do not use that key for other models. The reviewed documents do not settle every question about external, personally funded design assistance or offline policy training; clarify the exact proposed method before relying on it. Nothing about other contests' model ensembles overrides this track's requirements. [API-key restrictions](https://techarena-career-sim.readthedocs.io/en/latest/api-key.html).

## 13. Experiments before scale

First establish a complete valid baseline run and record cost, tool errors, survival length and all official outcome dimensions. Then compare materially different strategies while changing as little else as possible. Candidate families:

| Candidate | Single substantive difference | Main failure to watch |
|---|---|---|
| B0 | New documented generic reasoning reference, to be defined after exploration | Do not confuse it with random play or the removed proposal. |
| B1 | Explicit response to persistent deterioration | Excessive conservatism and missed progression. |
| B2 | Joint public quarterly planning | Planning with unavailable actions or assumed effect sizes. |
| B3 | Compact current-run trend/warning record | Stale memory and context cost. |
| B4 | Stronger balanced progression when stable | Ignoring delayed risk. |
| B5 | Concise reasoning and selective additional logs | Missing important feedback. |

Use complete games as the evaluation unit. A high score after twelve months is not necessarily a good proxy for surviving and scoring well at month 48. Borrow successive allocation from Hyperband, but eliminate *candidate budgets* rather than routinely truncating individual games: slow early strategies may perform well later. [Hyperband](https://jmlr.org/papers/v18/16-558.html).

The detailed protocol and recording schema are in [experiment-plan.md](experiment-plan.md). Batch sizes and counts there are budget proposals, not power calculations or official requirements.

## 14. Distinguish reliability from lucky evaluation

Always report the arithmetic mean game score because that matches official play scoring. Add survival fraction, distribution, worst outcomes, tokens, cost and tool failures. A robust auxiliary statistic may help debugging; it must not silently replace the organiser's metric.

If three independent games all complete, that is still weak evidence about the failure probability. With zero failures in `n` Bernoulli trials, the exact one-sided 95% upper bound is `1 − 0.05^(1/n)`: approximately 63.2% for three, 25.9% for ten and 9.5% for thirty. These are derived statistical illustrations, assuming independent comparable trials; dev games may not satisfy those assumptions and official parameter shift adds further uncertainty.

Bootstrap plots cannot create missing scenario diversity. More repeated dev games reduce sampling uncertainty under that environment but do not establish test-set generalisation. The statistical-precipice research and rliable are useful guides to interval estimates, score distributions and cautious claims. [Original paper](https://arxiv.org/abs/2108.13264), [authors' implementation](https://github.com/google-research/rliable).

## 15. Competitive positioning from past contests

Huawei Ireland 2024 offers unusually relevant evidence about the gap between algorithmic and final success. One team's repository reports first in algorithms but third overall after underinvesting in presentation. A separate second-place repository uses CP-SAT and pattern search. These are primary team accounts, not independently audited proof of every ranking claim. [Linan's team](https://github.com/linanwx/huawei2024), [second-place repository](https://github.com/acheong08/hwta-ireland-2024).

Sakana's AHC058 report demonstrates useful search diversity and evaluator-guided iteration, while also reporting roughly USD 1,300 of compute and thousands of calls. It does not show that our USD 50 credit can reproduce that process or that a single live game supports its local simulation technique. [Sakana report](https://sakana.ai/ahc058/).

Lux AI illustrates that both handcrafted policies and RL deserve consideration, but the RL authors' reports also show action-space, reward-shaping and debugging complexity. In a one-week Skills competition with hidden rules and a fixed platform, a new RL training stack is a poor first investment. The lesson is to simplify decisions and evaluate well, not to import a different bot architecture. [First-place author repository](https://github.com/ryandy/Lux-S2-neurips-public), [Deimos account](https://www.kaggle.com/competitions/lux-ai-season-2/writeups/deimos-10th-place-deimos-s-rl-approach).

See [precedents-and-reading.md](precedents-and-reading.md) for a wider comparison and a prioritised reading sequence.

## 16. Improving the scored Skill documents

The automatic document component is the mean of individual `SKILL.md` scores, not the count of Skills. Valid front matter, a useful discovery description, executable decision steps, priorities near limits and generalisation are explicitly valued. A Skill that contains prohibited conduct or contradicts the game can receive zero. [Document scoring rubric](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#official-evaluation-score-releases-and-final-score).

No Skill count or division of responsibilities is currently selected. Use experiments to identify useful decision procedures before packaging them. Compare a minimal coherent instruction with justified alternatives; do not let file structure determine the strategy. Clarity and completeness matter more than file count.

The design documents should describe what the tested Skills actually do and which outputs motivated changes. Preserve one concrete earlier/later example for the required presentation, but do not transform that case study into a fixed instruction for the named event. Discuss observations, uncertainty, revisions and measured limitations.

## 17. Packaging and submission strategy

All deliverables must be English and use JiuwenSwarm `0.2.4b3`, `mode: agent`. A final ZIP contains one top-level `solution/` with manifest, README, non-empty English presentation, the two required design documents and at least one valid Skill. The preliminary package is different and not scored. The former `preliminary/` proposal has been deleted; no final package is prepared. [Required structure](https://techarena-career-sim.readthedocs.io/en/latest/submission.html).

Cutoffs are end of 27 October, 30 October and 1 November 2026, all GMT. Submit a genuine tested revision before each cutoff when ready, rather than renaming unchanged work. Since the best issued valid score is retained, an already-scored stable version offers useful protection against a later lower score. The documents do not clearly settle which version's design is used for expert review when a different earlier version supplies the highest Stage 1 score; ask, and maintain coherent archived packages. [Version treatment](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#duplicate-and-superseded-submissions).

The video must answer the five official questions in order: design reasoning; what earlier logs taught and how a later version changed; why scripts/references were or were not used; robustness to changed settings; and the relationship between agents and Skills. It can be shorter than ten minutes and does not require slides. Use actual evidence, not invented ablations. [Video requirements](https://techarena-career-sim.readthedocs.io/en/latest/submission.html#required-contents).

## 18. What would count as a meaningful advantage

The strategy aims for six practical advantages, each needing evidence:

1. Fewer avoidable early exits from persistent issues the agent could observe.
2. Better use of quarterly action complementarities without hidden-rule assumptions.
3. More consistent sustained progression without sacrificing ending dimensions.
4. Correct tool calls and recovery from ambiguous execution outcomes.
5. Faster development through informative comparisons per dollar.
6. A defensible account of improvements, uncertainty and generalisation for expert review.

None guarantees first place, and there is no verified current leaderboard evidence here establishing the performance needed to beat other teams. The next evidence-producing step is the baseline run under the official runner and designated model. Large-scale experiments and recovered numerical dynamics remain conditional on organiser clarification.
