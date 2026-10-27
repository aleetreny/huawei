# Errata for the research package — verified 26 October 2026

Generated from `audit-2026-10-26.json`: eight independent auditors (one per dimension) and one adversarial verifier per dimension who tried to refute each serious finding. Only **critical/major findings upheld by the verifier** are listed. Refuted findings and minor notes stay in the JSON. Corrections marked "applied" are already implemented in CareerLab; the original research documents are kept unchanged as a record of what we believed earlier.

| Status | Count |
|---|---:|
| upheld | 43 |
| refuted | 11 |
| minor or unverified | 41 |


## Mathematics and statistics

- **[major, verifier confidence high]** `docs/historico/research/hierarchical-lab/lab-spec.json L74 (evaluation.primary_outcome); mathematics.md L9-11; experiment-registry.json primary_metric`

  Problem: Under the official formula the per-run objective also contains 0.1 x token efficiency. That term is computed per run and capped at 50 if the run ends before month 48, so completion and tokens per month change the version score directly. Two policies with equal mean Q but different completion rates (or different context growth) have different expected Stage-1 scores. Completing versus failing is worth up to 5 Stage-1 …

  Correction: Primary per-episode outcome Y = 0.8Q + 0.1E_run, where E_run = min(cap_T, clip(100(3e6 - tokens/T)/2.5e6, 0, 100)), cap_T = 50 if T<48 and 100 otherwise. 'tokens' is the quantity the official score report calls total_tokens; record it raw, because it is not certain that input+output+cached is the same thing. Y' for non-target actors must not erase token differences between policies: some candidates (for example …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/mathematics.md L46-56; docs/historico/research/from-zero-lab.md L77`

  Problem: The derivation is correct, but the rule cannot fire at budgets this lab can afford. The band ignores variance (it assumes the worst-case SD of 50 points for [0,100]). Half-widths at delta=0.05: n=10: 66 (K=1) / 77 (K=20) points; n=30: 43 / 48; n=100: 26 / 29. Two arms are separated only if their means differ by more than about 85 points at n=30. The docs admit the bands are 'muy anchas' but keep the rule as the only …

  Correction: Keep the Hoeffding band only as a labelled worst-case illustration. Define the working dormancy rule separately: a reversible Bayesian posterior rule whose thresholds are calibrated by simulation. Be explicit that even variance-adaptive betting CSs will rarely separate arms at feasible target sample sizes (hedged CS about ±24 points at n=10, ±11 at n=30, SD 15). Anytime-valid claims will therefore mostly be …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/mathematics.md L44-46 and L128-134; from-zero-lab.md L77`

  Problem: The time-uniform guarantee holds for each arm's outcome sequence only when the indexing order is independent of the outcomes (the 'stack of rewards' argument). With parallel workers, early failures finish first. If means or CS are updated in completion order, the running estimate of a fresh policy is biased low while its successful episodes are still running. The bias falls on late-benefit policies, which is problem …

  Correction: Replace the vague alternative in mathematics.md §10 with an explicit rule: estimators and CSs are computed only on launch-indexed, prefix-complete data, or on whole completed rounds. A prefix stalled by a censored launch is resolved by the censoring rule, not by skipping the launch. Severity: moderate. The hazard was identified; only the remedy was underspecified.

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/lab-spec.json L73; records.schema.json L217-225 (status 'censored'); mathematics.md L126`

  Problem: Labelling is correct, but no estimator or sensitivity analysis is defined. Complete-case analysis is biased whenever interruption risk grows with episode length. A 48-month run makes roughly 8x the tool and LLM calls of a 6-month failure, so rate limits and timeouts preferentially remove good episodes. That is informative censoring, and it biases means downward, most for the best policies.

  Correction: Keep resume-by-observe from protocol.md §9 and add a resumed flag. Note that a resumed LLM episode loses its in-episode memory, so it is a different execution policy. Note too that replacing censored episodes keeps the sample size up but does not remove length-biased selection. Use a tipping-point or delta-adjusted sensitivity analysis as the sensitivity layer, rather than Manski bounds at 0/90. Those bounds have …

- **[major, verifier confidence low]** `docs/historico/research/hierarchical-lab/counterexamples.json L57-74 (noisy_max); mathematics.md §3 L31-40; docs/historico/research/strategy-dossier.md L27-33, L213`

  Problem: For estimating mu this is right, but it misses how the official objective is built. Stage 1 = max over at most three scored versions (the latest unscored version at each of three cutoffs). Content-identical versions are not rescored, and a lower later score never reduces Stage 1. The version score has SD of about 0.8*sigma/sqrt(3) (6.9 Stage-1 points at sigma_Q=15). Then E[max of 2 equal-mean versions] = m + 0.564*s …

  Correction: Add a quantitative selection rule among unscored candidates at each cutoff, on top of the existing submit-each-cutoff practice. The predictive spread for EI relative to the issued score A* should include only the independent part: the 3-run sampling noise (0.64 sigma_v^2/3), the posterior variance, and any version-specific interaction with the environment. Leave out the dev-to-official shift common to all versions; …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/protocol.md L55-63 (fidelity pilot); design.md L136-140; mathematics.md L102-110`

  Problem: The design cannot measure the things it is asked to check. With K=6 policies, the Fisher 95% CI for an observed Pearson r=0.6 is [-0.41, 0.95] (K=10: [-0.05, 0.89]; K=20: [0.21, 0.82]). With n=3 episodes per cell, per-cell reliability tau^2/(tau^2+sigma^2/n) is about 0.46 (tau=8, sigma=15), so even a perfect true correlation is observed at roughly half its size. False-rejection audits built from a handful of target …

  Correction: State that the cheap actor has no pruning authority by default, and grant it only on pre-registered decision-focused criteria (top-k recall, regret of the cheap-selected policy, randomized-audit false-rejection rate). Acknowledge that with a USD 50 target budget these criteria will likely never be met. In that case the cheap actor screens only gross failures (invalid actions, early collapse) and never ranks close …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/records.schema.json L172-290 (evaluation record)`

  Problem: Fields required by any valid sequential analysis are missing: a launch index and block id (needed for prefix-complete analysis and paired differences), an analysis role (exploration / selection / audit / confirmation) with a pre-registration id (so held-out confirmation can be enforced), total_tokens and the per-run efficiency term (the primary outcome), a resumed flag, a provider/route identifier (epoch drift), and …

  Correction: Add analysis_role plus prereg_protocol_id, block_id, an explicit per-cell launch_index (more robust than timestamps), resumed, raw official total_tokens, the official efficiency term and dimension_contributions. Make the integrator enforce role separation. Severity: minor to moderate.


## Search and generation methods

- **[major, verifier confidence high]** `docs/historico/research/hierarchical-lab/mathematics.md §4 (also docs/historico/research/from-zero-lab.md §5A)`

  Problem: The rule is inoperative at any feasible sample size. On the 0-100 scale with delta=0.05, the half-width for the first candidate is ±68 at n=10, ±44 at n=30 and ±26 at n=100; the 10th candidate gets ±83, ±52 and ±30. The from-zero-lab K-version with K=4 gives ±71 at n=10 and ±45 at n=30. Two bands separate only when the true gap exceeds about twice the half-width, so with tens of episodes per candidate nothing is …

  Correction: Mark the Hoeffding/union-bound band as a non-operative illustration. Make the normative dormancy rule variance-adaptive and reversible. One option is a Bayesian soft elimination such as P(mu_i > mu_leader) < 0.10 under a Normal model with variance shrunk to the pooled estimate, reported with a whole-episode bootstrap because outcomes may be bimodal. Another is a fully sequential indifference-zone procedure (Kim & …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/bibliography.md (55 sources); design.md; mathematics.md; protocol.md; completion-audit.md row 1`

  Problem: A grep of docs/historico/research/*.md and docs/historico/research/hierarchical-lab/* finds no mention of racing, F-Race, irace, ParamILS, SMAC, LUCB or successive halving/rejects. Track-and-Stop occurs only in search-audit.json, as an unselected candidate. These fields exist precisely to choose among stochastic configurations that are expensive to evaluate, under repeated looks: iterated racing with elitism, incumbent intensification (a …

  Correction: Keep from-zero-lab's round-based racing as the starting point and ground it in the canonical sources. Add Maron & Moore 1993, Birattari et al. 2002 and López-Ibáñez et al. 2016 (irace: elitist iterated racing). Add Hutter et al. 2009 and 2011 (ParamILS/SMAC intensification, where a challenger must match the incumbent's run count). Add Kim & Nelson 2001 and Nelson et al. 2001 (indifference-zone and …

- **[major, verifier confidence high]** `docs/historico/research/hierarchical-lab/mathematics.md §1`

  Problem: (a) The automated version score is 0.8*mean Q + 0.1*D + 0.1*TE. TE is computed per run and capped at 50 when a run ends before month 48, so at equal Q a completed run can be worth up to 5 more automated points than an early exit. (b) Stage 1 is the highest valid version score over the two interim releases and the final release, with one scored version per cutoff, and a lower later score does not reduce it. The …

  Correction: Use a per-run primary estimand A = 0.8Q + 0.1·TE_run, computed only in target-harness cells, because Claude-worker token counts are not comparable to JiuwenSwarm+deepseek. Estimate 0.1·D per version from a rubric, and keep Q, P(month 48) and tokens/month as auxiliaries. On the cheap tier, rank on Q and completion only. At R2 and R3, choose the version that maximises a Monte Carlo estimate of E[max(S_banked, S_new)]. …


## Problem A

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/lab-spec.json roles (lines 13-33); design.md sections 12-13 (lines 134-148); README.md line 31; protocol.md section 2 table (lines …`

  Problem: Nobody priced or timed a target episode, so the premise was never checked. Per token, the designated model is as cheap as Haiku or cheaper. The OpenRouter endpoint list for deepseek/deepseek-v4-flash, fetched today, shows $0.05-0.60/M input (typically $0.09-0.14) and $0.17-1.32/M output, with cache reads around $0.02/M. Haiku 5.5 is $0.10/$0.50 per M for requests up to 100k input tokens and $0.50/$2.50 beyond that; …

  Correction: Price and time the target before designing anything else: measure tokens, $ and wall-clock for 1-2 target episodes. Replace the USD price table with three cost units: target $ per episode, Claude subscription usage per episode, and wall-clock. Make the ladder conditional. If team-funded target access (same OpenRouter slug, same JiuwenSwarm setup) is approved by both the user and the organisers, the target becomes …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/lab-spec.json target_actor (lines 26-32); protocol.md section 2 (line 27); records.schema.json evaluation.actor_model_id`

  Problem: The identity of the model actually served is underspecified and drifts between routes. OpenRouter's deepseek/deepseek-v4-flash currently resolves to 'DeepSeek V4 Flash 0423' and is served by 17 providers. Their quantization differs (fp4 at Relace and AtlasCloud, mxfp4 at Wafer, fp8 or unknown at the rest). Official scoring uses organiser-controlled routing, so the target is itself a mixture over providers. …

  Correction: Record the actor as a configuration: route/key class, slug as sent, served model name as returned, per-request provider and quantization where observable, harness and version, system-prompt hash, Skill-loading mode, reasoning/effort, context policy, MCP command and flags, split. For any team-funded target run, use OpenRouter with the organiser-equivalent slug. Note that OpenRouter's default routing is …

- **[major, verifier confidence high]** `docs/historico/research/hierarchical-lab/protocol.md section 5 (lines 53-65); design.md section 12 (lines 138-140); mathematics.md section 7 diagnostics (lines 102-110)`

  Problem: No threshold says what counts as sufficient or insufficient, and no estimator or decision rule is given. The pilot also lacks the power to inform the decision even in principle. Fisher-z 95% intervals for an observed correlation of 0.8 between perfectly measured policy means are [-0.03, 0.98] at K=6, [0.42, 0.94] at K=12 and [0.55, 0.92] at K=20. With 3 episodes per cell, the reliability of cell means is …

  Correction: Pre-register numeric license criteria and a default of no pruning. Before running the matrix, also simulate the probability of reaching the pruning license under plausible (s_b, sigma, rho) values. At s_b=5 and sigma=15, n* = 21, and even a perfectly measured r=0.8 at K=10 has an 80% lower bound of only about 0.55. If that probability is low, do not spend the target budget on a calibration matrix: run target-only …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/mathematics.md section 7 (lines 90-110); bibliography.md 'Contexto y transferencia' and R33-R35`

  Problem: The literature that actually governs this decision is missing, and so is the consequence that matters most. (1) Multi-fidelity best-arm identification (Kandasamy et al. 2016; Poiani et al. 2022, 2024) assumes a known maximum bias for each fidelity. The lab has no bias bound, so any pruning rule must estimate one and carry its uncertainty. (2) PPI, PPI++, active and stratified PPI, control variates, multi-fidelity …

  Correction: Add the multi-fidelity best-arm literature (Kandasamy 2016; Poiani 2022, 2024), stating that it assumes known per-fidelity bias bounds, so the lab must estimate an upper bound on tau and carry its uncertainty. Present the prior's calibration as a KOH / MISO-style policy-level model fitted with errors-in-variables, with pruning only through predictive intervals that include tau. State that episode-level control …

- **[critical, verifier confidence medium]** `docs/historico/research/hierarchical-lab/protocol.md section 7 'Contrato del trabajador' (lines 87-95) and section 4 (lines 47-51); lab-spec.json roles`

  Problem: Nothing technically enforces this for Claude Code workers. By default Claude Code has Bash, Read, Write, Web and other tools. It also loads user and project CLAUDE.md, plugins, skills, hooks and memory. --bare is unavailable without an API key. A worker started in the repo or next to .career_sim_runner/ could read career_emulator.sqlite3, run logs from other runs or package files, which the rules explicitly …

  Correction: Severity: major, not critical. Document the existing harness in protocol.md and lab-spec.json. Add a pre-flight attestation that parses the stream-json init event (tools, mcp_servers, skills/plugins) and marks the episode harness_invalid on any extra tool, server or skill. Verify experimentally that user CLAUDE.md and auto-memory are not loaded; one option is a clean CLAUDE_CONFIG_DIR. Do not add --safe-mode …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/design.md sections 12-13; mathematics.md section 7; protocol.md section 5`

  Problem: The harness is an uncontrolled second factor. Claude Code differs from JiuwenSwarm 0.2.4b3 in system prompt, how Skills are surfaced (progressive disclosure vs injection), context management (Claude Code auto-compaction vs JiuwenSwarm's policy), reasoning/effort defaults (Haiku 5.5 and Sonnet 5.5 cannot fully disable thinking), tool-call formatting and turn limits. A Claude-vs-target ranking difference therefore …

  Correction: Index cells by the full actor configuration (model x harness x Skill mode x context policy x MCP flags). Record that careerlab's Claude worker restarts a stopped episode as a fresh process with --no-session-persistence and the continuation prompt. That is a context reset, and it happens disproportionately in long episodes, so it is a harness factor confounded with problem B. Treat the OpenRouter-in-Claude-Code cell …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/protocol.md sections 2-3 (lines 13-43); lab-spec.json gates.external_spending_limit_usd and model_prices_as_checked`

  Problem: The planned Claude access is a Max subscription with extra usage disabled, so the binding constraints are rolling usage windows shared with the Opus orchestrator, not dollars. Workers that hit limits mid-episode are interrupted. Long, successful episodes are the most likely to hit a limit, so the censoring is informative (length-biased) and is not addressed beyond 'pending is not zero'. The 1M-token illustration is …

  Correction: Express Claude cost as measured subscription usage per episode: stream-json rate_limit events, total_cost_usd as an API-equivalent figure, and wall-clock. Add a subscription unit to the schema. On a rate-limit stop, wait for the window to reset and resume the same conversation instead of burning continuations. Record interruption_cause from the stream (rate_limit, timeout, context_reset, crash). Compare interruption …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/design.md line 140; lab-spec.json evaluation.sample_cheap_rejections_on_target; protocol.md section 11 'Falsos descartes'`

  Problem: There is no sampling design, inclusion probability, estimand, rate threshold or revocation rule. Auditing one candidate with 1-3 target episodes cannot classify it as a false rejection: the SE is about sigma/sqrt(n), i.e. 9-12 points for sigma=15-20 and n=3. Without known inclusion probabilities, any pooled false-rejection rate is biased by whichever candidates the orchestrator chose to audit.

  Correction: Pre-register the audit: random selection with logged probabilities (uniform is acceptable; non-uniform needs HT weights), episodes per audit, the pooled estimands (mean target gap and calibration z-scores against the predictive interval), and revocation thresholds that re-queue every cheap-pruned candidate in the stratum. State openly that single-candidate significance tests with 2 episodes have almost no power; …

- **[major, verifier confidence high]** `docs/historico/research/hierarchical-lab/records.schema.json $defs.evaluation and $defs.job (additionalProperties: false; actor_model_id only)`

  Problem: The actor is a single string and the schema forbids extra fields, so it cannot record harness, route/key, served version, provider mix, effort/reasoning, MCP server command/flags, dataset split, compliance metrics or interruption cause. Competition-key, team-funded and Claude-harness cells would be indistinguishable or squeezed into free text. execution_class also has no value for the official 3-run evaluation on …

  Correction: Add an actor_config object (or a reference with its hash) aligned with careerlab's actor.json and fingerprint() fields: route, key_class, served model, provider log reference, harness and version, system_prompt_sha256, skill_loading, effort, context policy, mcp_server_cmd_sha256, competition_mode, split. Also add a compliance block, an interruption_cause enum, a subscription-usage cost unit, and an …


## Problem B

- **[major, verifier confidence high]** `docs/historico/research/hierarchical-lab/lab-spec.json:74 (evaluation.primary_outcome); docs/historico/research/hierarchical-lab/mathematics.md §1 (Y = quantitative_score/100); …`

  Problem: This leaves out the part of the official per-run score that depends on survival. TE is computed from total_tokens / survival_months and is capped at 50 for any run ending before month 48. Reaching month 48 is therefore worth up to 0.1 x 50 = 5 automated points (6.25 quantitative_score points) beyond Q. A Q-only metric undervalues late-benefit policies that complete the run. It also overvalues long-surviving, …

  Correction: For target-runtime episodes, the primary per-run outcome is U = 0.8*Q + 0.1*TE. TE = clip(100*(3e6 - tokens/T)/2.5e6, 0, 100), capped at 50 when T < 48. Correction to the auditor: when the token count is missing because of our own instrumentation, mark U as missing and do not score TE as 0. The published zero rule applies to official runs, which will always have a runner-side count. Until organiser question C7 says …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/records.schema.json $defs.evaluation (terminal-only fields, additionalProperties:false) vs docs/historico/research/experiment-plan.md §2 lines 23 …`

  Problem: The evaluation record holds only terminal fields: terminal_score, survival_months, full_horizon_completion and a free-text termination_reason. It has no per-month trajectory of visible stats, level, CurrentLevelDuration, review grades, promotions, warnings, quarterly allocations or cumulative tokens. It also lacks ending-dimension contributions, a censoring month and a resumed flag. This contradicts the plan's own …

  Correction: Keep raw evidence as the single source of truth and make retaining it mandatory for every episode. Add a derived, deterministically regenerable 'trajectory' record: one row per month boundary, review and quarterly phase, with visible stats, level, CurrentLevelDuration, review grade, promotion, warnings, quarterly package and cumulative tokens when the runtime exposes them. Add terminal fields: ending_contributions …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/lab-spec.json:73; mathematics.md §9 last paragraph; records.schema.json status 'censored'`

  Problem: The label is right, but no estimator is specified, so the default becomes a complete-case mean. That is biased whenever interruption risk grows with episode length. Long episodes make more tool calls, run longer and are more exposed to rate limits, timeouts, context overflow and contention on the shared career_emulator.sqlite3. They are removed disproportionately, which pulls down the estimate for exactly the …

  Correction: Prefer resuming the same session_id through observe() after a live-handle check, as protocol.md §9 already says, and record resumed=true. Run sensitivity analyses with and without resumed episodes, because an LLM actor that loses its in-episode context is a different execution condition. Analyse censoring by month: KM for survival, Aalen-Johansen for causes, and an IPCW mean of U as a sensitivity estimate, noting …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/mathematics.md §10 (lines 128-134); protocol.md §6 ('El planificador puede ser asíncrono')`

  Problem: The diagnosis is correct but the remedy is optional. In asynchronous operation the first results to arrive are early exits, so a policy's interim mean is pessimistic precisely when its good episodes are long. An ASHA-style promotion or a dormancy decision taken on interim results is a hidden partial-episode screen. The clinical literature handles these 'pipeline' units explicitly (Hampson & Jennison 2013), and the …

  Correction: Make it binding through a per-policy launch-order prefix rule. A dormancy or rejection decision for policy i uses only the first n episodes launched for i, and only once all n are terminal or explicitly censored. This is equivalent to the auditor's round closure but avoids global barriers and idle workers when some episodes run long. Interim data may only reorder the launch queue. Pending episodes appear only as …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/protocol.md §7 line 95; records.schema.json termination_reason (free text)`

  Problem: The research does not separate truncation on the actor or runtime side from infrastructure interruption. Actor-side truncation covers max-turns, context overflow, compaction, the agent ending its turn, and any JiuwenSwarm iteration cap. In the target runtime, an agent that stops at month 20 is probably scored from the state at exit ('an early exit still receives one'). That is a real, policy-attributable late …

  Correction: Make termination_category an enum: completed_48 | game_elimination:<official label> | runtime_agent_stop | operational_interruption. For target-representative runs, keep the official runtime configuration; do not raise JiuwenSwarm or runner caps. Record runtime_agent_stop as a scored outcome if, and only if, a first target run (or an organiser reply to an extended C7/C9) shows that the runner scores it. For dev …


## Problem C

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/design.md:130 (section 11); mathematics.md:152 (section 12)`

  Problem: This treats within-episode randomization as uncertain or optional and never designs it, though it is the standard identification tool (SMART/MRT) and needs no cloning or seed. If the prefix policy is identical across arms and the switch Z is drawn at decision point d, the arms are exchangeable given the history at d. The conditional effect among episodes that reach d is then unbiased, with no survivorship bias, and …

  Correction: Add 'randomized mode switch at pre-registered decision points' as a lab action for mechanism studies. Draw Z from a sealed sequence the worker cannot see before d. Log p, Z, seed reference, stratum and the injected text hash. State Delta V_lab = P(T>=d)*E[Y(1)-Y(0)|T>=d, prefix P0, actor m] and label it the effect of the injected interactive regime. Say explicitly that the shippable regime's value must come from …

- **[major, verifier confidence high]** `docs/historico/research/hierarchical-lab/design.md:120 (section 10)`

  Problem: (1) There is no always-M arm, so a contextual win could just be the main effect of mode M, and the specialization would be unnecessary. (2) There is no sham-injection, yoked/random-timing or time-shift control, so contingency cannot be separated from timing, dose or a mid-episode reminder effect. (3) The decision rule has no metric, minimum effect, alpha, multiplicity rule or equivalence handling. With small n, …

  Correction: Arms: never-M, always-M, plus only shippable trigger families (feedback-graded and state/warning; a public-structure wording only if it differs from the calendar arm in firing time). On the cheap tier add a matched placebo clause for complete-policy runs, or a sham only in injection runs. Define aliasing for each operationalization pair as 'induces the same switch time in the episode'. Declare up front that triggers …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/design.md:124 (section 10)`

  Problem: This implies a dev-learned month or cutpoint may ship if it is labelled as a design preference. The binding rules make content prohibition independent of 'how it was arrived at, or how it is described'. They also require guidance to remain applicable when event order, parameter values or the dataset change, and warn against assuming a dev pattern persists. packages.rst says dev behaviour, thresholds and event …

  Correction: Ship no month index or statistic cutpoint whose value was searched or tuned on dev outcomes; such a value may encode dev composition or hidden thresholds. Thresholds the team fixes before seeing data, on published scales (for example Health 0-10), stated as team safety margins and not as simulation thresholds, are permitted general strategy. Calendar wording is allowed only when anchored in public structure (48 …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/design.md:118 (section 10 confound list)`

  Problem: Four important confounds are missing. (a) Actor-side time effects: month correlates with transcript length and position, and a mid-episode instruction can help simply by re-surfacing the Skill (a reminder effect), which is not a game mechanism. (b) Dev event-sequence artifacts: the benefit may come from which dev events cluster near month 8, which would also be a compliance problem. (c) Cutpoint selection: picking …

  Correction: Add to section 10 the following confounds: (a) actor attention or instruction drift over the episode, citing Li et al. 2024 COLM https://arxiv.org/abs/2402.10962 and Laban et al. 2025 https://arxiv.org/abs/2505.06120 instead of only Lost in the Middle; (b) dev event-composition artifacts; (c) cutpoint selection during discovery, with a pointer to the fresh-confirmation rule; (d) prefix dependence after …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/records.schema.json (policy.context_gate_description free string, line ~155; evaluation record lacks decision-point fields); …`

  Problem: No record can hold decision-point data: active mode, assignment Z, probability p, stratum, pre-treatment descriptors, would-have-fired flags for every candidate trigger, sham text hash, or the worker's declared mode. Problem C analyses (IPW, WCLS moderation, discordance, placebo balance) therefore cannot be run later. The gate is unstructured free text, so triggers cannot be pre-registered. protocol.md lists an …

  Correction: Add a decision_point record (evaluation_id, d_index, month, quarter, stratum, p, Z, assignment_seed_ref, injected_text_sha256, declared_mode_next, availability; descriptors and trigger flags optional, with a pointer to the trajectory span). Add a structured trigger object on policies (family, shippable wording, lab operationalization version, pre-registration decision id). Add an execution_class for segmented or …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/bibliography.md:325-341; references.json`

  Problem: A grep finds no causal-inference sources: nothing on Robins g-methods or the healthy-worker survivor effect, Murphy SMART or dynamic regimes, MRT/causal excursion effects, Hernán selection bias, principal stratification or negative controls. Problem C is exactly time-varying confounding plus selection on a post-treatment variable. Robins 1986 is literally about workers whose survival in employment confounds …

  Correction: Add the primary causal sources with notes on how they apply: Murphy 2005 SMART; Klasnja 2015 and Boruvka 2018 MRT; Qian 2022; Qian 2025 distal causal excursion effects (https://arxiv.org/abs/2502.13500), which fits a terminal outcome better than WCLS; Robins 1986 on the healthy-worker survivor effect; Hernán et al. 2004 on selection bias; Frangakis & Rubin 2002; Lipsitch 2010. Note that logged randomization makes …


## Rules and compliance

- **[critical, verifier confidence medium]** `docs/historico/research/organiser-questions.md L3, L28-34 (reply log 'Pending; not sent'); docs/historico/research/hierarchical-lab/protocol.md L9-11; README.md L46`

  Problem: It is 26 Oct (day 1 of 7). Organisers reply only in working hours (index.rst, api-key.rst, competition-rules 'Interpretation and questions'), the first score cutoff is 24:00 GMT on 27 Oct, and the key expires on 1 Nov. Every real-game part of the lab (problem A's cheap workers, calibration, false-rejection audits) is blocked until a reply arrives, and nothing has been sent. Each day of delay removes about one …

  Correction: Keep the status text as it is. Add a dated action, 'user sends the question on Discord during UK working hours on Mon 26 Oct', and a fallback plan that does not depend on the reply (official runner plus synthetic testbed). Only the user can send it; the assistant must not post. Record the link and date in the reply log. Expect no replies on Sat 31 Oct or Sun 1 Nov. The disclosure must also cover today's CareerLab …

- **[critical, verifier confidence medium]** `docs/historico/research/hierarchical-lab/protocol.md §13 milestone 1; docs/historico/research/hierarchical-lab/lab-spec.json 'gates'; docs/historico/research/RESUMEN_ES.md L49 ('comprobar clave y modelo …`

  Problem: No gate covers 'preliminary submission verified and key received'. The repo's preliminary/ files were deleted at 09:55 on 26 Oct (commit cf6116d; strategy-dossier L211), Matteo's plan says the key is not yet available, and protocol L25 says no key has been tested. The key is issued only after the organisers verify a genuine English preliminary submitted on techarena-uk.hydro.ac. Without it there is no target-actor …

  Correction: Add hard gates 'preliminary_upload_confirmed' and 'competition_key_received' to lab-spec.json and protocol §13, ahead of every target-actor and submission step. Today, ask the team whether anyone uploaded to techarena-uk.hydro.ac. If nobody did, upload a genuine English preliminary. It can be restored from commit 69bae27, or built from Matteo's Sustainable Career v0.1 Skills plus a manifest with a real team name and …

- **[major, verifier confidence medium]** `docs/historico/research/from-zero-lab.md L13, L55, L97, L182; docs/historico/research/matteo-branch-review.md L44-60; docs/historico/research/experiment-registry.json observation manual-ui-01 …`

  Problem: The session was played by an AI assistant (the text says 'He jugado personalmente', 'No aparece como herramienta nativa de este chat', 'La pestaña queda abierta') through Matteo's Starlette/FastMCP adapter. The docs allow manual testing through the public CLI, and they allow another MCP client to connect over stdio during development. They say nothing about whether an external LLM may play dev games, so this is …

  Correction: Relabel the session as 'AI-assistant (Codex) choices via browser UI -> local adapter -> official server over stdio'. Add an actor field to the registry and schema, and drop the word 'manual' for it. Remove 'user authorisation permits it' as a compliance basis; user authorisation is not organiser approval. Pause further AI-played sessions until the question is answered, and disclose this one in the question. Its …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/protocol.md L9; README.md L46; task_plan.md Phase 3 ('MCP client (stdio and HTTP)')`

  Problem: The paraphrase drops the qualifier. mcp.rst permits another client only through the server's standard input/output transport. The http/sse/streamable-http transports listed in the CLI --help are not sanctioned, and neither is running many sessions on one non-competition server that shares the runner's state database. The current plan builds an HTTP client anyway.

  Correction: Rewrite protocol L9 to quote the stdio qualifier. Stop using the streamable-http mode in careerlab, or ask about it explicitly. Use stdio with sequential sessions per process. For any parallelism, ask the organisers about multiple processes and about per-process CAREER_EMULATOR_DB (the variable the official runner sets) before relying on either. Disclose the HTTP and 16-way tests already run.

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/lab-spec.json evaluation.unit ('administrative interruption is censored, not a score'); protocol.md §7 L93, §9 L132`

  Problem: Correct for faults in the lab's own infrastructure, but wrong for the target actor under the official runner. Official scoring gives any early exit a quantitative_score from the state at exit, caps its token term at 50, and gives 0 on that term when token or survival counts are missing. The intent is to stop early exits from outscoring completed runs. If the agent stops calling tools, hits an iteration or context …

  Correction: Add a status 'actor_intrinsic_stop', scored under the policy x actor cell. For target runs, use Q at exit and TE at most 50, or 0 if counts are missing. If the local runner emits no score for such a stop, record Q as missing; do not impute 0 or censor. Keep lab-infrastructure faults (including the observed session eviction) as censored and re-run. Keep provider/key outages as a separate censored class whose …

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/lab-spec.json evaluation.primary_outcome; docs/historico/research/experiment-registry.json E01-E03 primary_metric`

  Problem: The scored quantity is 0.8·mean(Q) + 0.1·DQ + 0.1·TE, and TE depends on the policy (tokens per month survived, cap at 50 on early exit). For example, a change that adds 1 point of Q but moves usage from 500k to 1M tokens/month nets −1.2 Stage 1 points (+0.8, −2.0). TE can only be measured with deepseek-v4-flash in JiuwenSwarm; token counts from Claude workers say nothing about it.

  Correction: Pre-register A_hat = 0.8*mean(Q) + 0.1*mean(TE_r) + 0.1*DQ_fixed for target runs. TE_r follows the published piecewise rule, with a cap of 50 if survival < 48 and 0 if counts are missing. On cheap actors keep Q as the primary metric and model target tokens per month as a separate covariate. Report Q and TE alongside A_hat.

- **[major, verifier confidence medium]** `docs/historico/research/organiser-questions.md §A-C (10 questions, about 650 words); README.md L46`

  Problem: It is too long and open-ended to get a fast answer an organiser can approve. It asks organisers to invent limits instead of approving concrete caps, which contradicts protocol L11's own requirement for concrete limits. It leaves out the transport (stdio vs HTTP), self-funded deepseek-v4-flash, and retroactive disclosure of the 74k random batch and the AI-played session. It also calls the Claude route 'personally …

  Correction: Send a short question with concrete caps, but make the disclosure complete: Matteo's batch, the AI-played session, and today's CareerLab streamable-http, 16-way and scripted bench runs. Include a yes/no on per-process CAREER_EMULATOR_DB isolation. Keep B4 and B5 as yes/no items, or remove (b7) and (b8) from the list of methods needing a reply. Size the caps from measured need.

- **[major, verifier confidence medium]** `docs/historico/research/hierarchical-lab/protocol.md §13 and README.md 'Qué haría primero'; task_plan.md Phases 3-6`

  Problem: None of the milestones is tied to the three fixed cutoffs. Only the latest unscored version before each cutoff is evaluated, at most three scores are issued, results arrive one to two days after a cutoff, and Stage 1 is the maximum over issued scores. A lab result that is not frozen, rewritten into English Skills and tested with 0.2.4b3 before 24:00 GMT on 30 Oct gets no interim feedback. After 1 Nov the key expires …

  Correction: Merge the RESUMEN timeline into protocol §13 and task_plan.md. v1, built without the lab, is submitted by 24:00 GMT on Tue 27 Oct, conditional on the key arriving. Lab outputs feed v2 by Fri 30 Oct and v3 by Sun 1 Nov. Freeze each version before its cutoff with enough time for official-runner testing and the video. If the key has not arrived by 27 Oct, record that v1 cannot be properly tested, and decide explicitly …


## Teammate evidence and exploration claims

- **[major, verifier confidence high]** `docs/historico/research/organiser-questions.md:9-12 (A1-A2 and the paragraph 'We have specified this architecture but have not launched it')`

  Problem: A teammate has already run an automated uniform-random driver through the official MCP: 73,858 sessions and 1,563,578 actions over 4 h, via the Career Lab adapter. There have also been LLM-driven sessions through the browser and through Codex. The rules say that when the docs are silent on a method, teams must ask in Discord before using it, and that absence of a prohibition is not permission. mcp.rst permits a …

  Correction: Rewrite the section A preamble and A1/A2 as a disclosure plus a question. (i) On 26 Oct a teammate ran an automated uniform-random driver through a local stdio client of the unmodified career-emulator-engine-mcp 1.0.6 with the dev dataset 1.0.8: 73,858 sessions and 1,563,578 actions in about 4 h. It used no package, database or internal reads. (ii) Two LLM-assisted manual sessions were played: Codex via a browser UI …

- **[major, verifier confidence medium]** `origin/Matteo:docs/skill-evaluation-plan.md 'Proposed 100-run target'; docs/historico/research/experiment-plan.md:49 (~30 games); docs/historico/research/RESUMEN_ES.md:59 (USD …`

  Problem: There is one key, with at most USD 50, and the three plans have not been reconciled. The 100-run plan spends target-actor games on a single frozen candidate with no concurrent comparator ('Compare with a reasoned no-strategy baseline ... when resources permit'), so it estimates one arm and settles no selection question. For illustration with an assumed per-run SD of 15: 100 single-arm runs give an SE of about 1.5 on …

  Correction: Create one team ledger for the single key, recording spend per run in USD and tokens, and who is running what. Agree it with Matteo before anyone spends the key. In matteo-branch-review.md, state explicitly that a single-arm series of 100 runs estimates one mean but does not tell the team which version to submit. Replace it with an interleaved comparison of v0.1 against a same-actor reference, using variance-driven …

- **[major, verifier confidence medium]** `docs/historico/research/from-zero-lab.md:3; docs/historico/research/RESUMEN_ES.md:3,49,65; docs/historico/research/experiment-plan.md:115 (26 Oct 'Integration, baseline, cost pilot'); README.md ('No ... …`

  Problem: A key is issued only after the organisers verify a preliminary submission of preliminary/manifest.json, design/skills_design.md and skills/*/SKILL.md on techarena-uk.hydro.ac. The team's only preliminary package (commits 767387e-69bae27, 01:03 UTC on 26 Oct) was deleted in cf6116d. No file records whether it was submitted. The teammate states at 10:30 UTC that the key is not yet available. Deleting it from the repo …

  Correction: Add a status record to the registry: preliminary submitted (yes/no, date, which content), key requested or received (date), and who holds it. If nothing was submitted, the user should decide today which genuine English package to submit. One option is the deleted package (recoverable from 69bae27 and already complete). The other is Matteo's v0.1: its three SKILL.md files and skills_design.md moved into preliminary/, …

- **[major, verifier confidence medium]** `docs/historico/research/experiment-registry.json E01 (P00-P11) and E03 prerequisite; docs/historico/research/from-zero-lab.md:99-114; docs/historico/research/matteo-branch-review.md:36`

  Problem: The factors come from random-play terminal causes, which the review itself warns are not priorities. A reasoned target actor may rarely die of Blackout or Trust crisis early (unknown), which would make E01 a null experiment on scarce budget. Pushing growth to E03 screens growth-forward policies by early survival, which is exactly the late-benefit trap (problem B). It also contradicts experiment-plan.md:45 ('Begin …

  Correction: Mark E01-E03 as superseded by the hierarchical-lab design, or reconcile them with lab-spec.json. Choose the first factors only after B0 has run on the target actor. Base that choice on where B0 loses ending-score contributions and on its review and level trajectory, not on terminal-cause counts alone, because those counts are competing risks. Include at least one growth-forward family in round 1. Keep judging every …


## Orchestration and actor configuration with Claude Code

- **[major, verifier confidence medium]** `Task brief / user account statement ('Account: Claude Max plan (extra usage disabled)')`

  Problem: The local CLI reports a different plan. 'claude auth status' (no model call) returned authMethod claude.ai, apiProvider firstParty and subscriptionType 'pro'. Anthropic's pricing page describes Max as 5x or 20x Pro's usage per 5-hour session, so the budget and concurrency assumptions differ by up to a factor of 20 depending on which is true. The status-line field and /status can confirm it. I did not verify it in …

  Correction: Before any budget or concurrency plan, confirm the tier in /status or on the claude.ai account settings page. If it is Pro, plan for 1x windows, check in one interactive call that Opus 5.5 is usable in Claude Code on Pro, and record the observed tier and its source in the frozen lane record.

