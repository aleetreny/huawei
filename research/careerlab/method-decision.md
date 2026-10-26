# CareerLab — method decision after the critical audit

26 October 2026. This document replaces the "Recomendación" of `research/hierarchical-lab/README.md` as the team's working decision. The earlier package stays as a record. Its verified errors are listed in [errata.md](errata.md), and the full audit with verifier verdicts is in [audit-2026-10-26.json](audit-2026-10-26.json). The pre-registered statistics are in [`lab/protocol/prereg-v1.md`](../../lab/protocol/prereg-v1.md); measured infrastructure facts are in [`findings.md`](../../findings.md).

## 0. Status at a glance

| Area | State on 26 October |
|---|---|
| Official MCP client | Built and tested (`careerlab/`). Only stdio is used, only the five official tools are called, and the engine settings match the official runner. |
| Isolation, retention and recovery | Measured through the official tools only (section 5). |
| Registry, planner, resume after kill | Built and tested on real dev: 150 scripted episodes, one `kill -9` mid-run, 10 episodes resumed in their own sessions, no interruption scored. |
| Pre-registered statistics | Frozen (v1, hashes in the registry) before any policy-selection data. |
| Synthetic testbed and method comparison | Being built by the build workflow (`careerlab/synthetic`, `careerlab/search`); results go in `lab/reports/`. |
| Initial behaviour families (Skill bundles) | Being written with a compliance linter (`lab/policies-src`). |
| Target actor (deepseek-v4-flash in JiuwenSwarm 0.2.4b3) | **Blocked.** No competition key; the preliminary package that earns it was deleted in `cf6116d`. A self-funded route needs a user budget and an organiser answer. |
| Claude workers on the real game | **Gated** (`lab/gate.json`). The rules do not address them, and the organiser message is drafted but not sent. The CLI on this Mac is logged in to a Pro account at 79 % of its weekly limit, not the Max x20 plan. |

No strategy has been shown to win. Everything below is a procedure, measured infrastructure, or a claim that is explicitly pending.

## 1. What the audit changed

Eight auditors checked the previous research against primary sources and the official docs. An adversarial verifier then tried to refute each serious finding: 43 were upheld and 11 refuted. These upheld findings change what we do:

1. **The objective was wrong.** Each run contributes `0.8 Q + 0.1 E` to the official score. `E`, the token-efficiency term, is capped at 50 when a run ends before month 48. Finishing is therefore worth up to 5 automated points on top of any effect on `Q`, and a policy that bloats context loses points even when `Q` is equal. The primary outcome is now `Y = 0.8 Q + 0.1 E`.
2. **The only formal decision rule was inoperative.** The Hoeffding union band is ±43 points at n = 30, so it could never separate realistic policies. We replaced it with Bayesian partial pooling for reversible decisions, betting confidence sequences for anytime-valid statements, and fresh confirmation for claims.
3. **Asynchronous results bias against late benefits.** Early failures come back first, so interim means of long, successful policies start low. Decisions now use only prefix-complete data at block boundaries.
4. **Cheap workers may not be cheap, and calibration was underpowered.** Per token, deepseek-v4-flash costs about the same as Haiku 5.5 or less. Six policies × three episodes cannot measure rank agreement: the 95 % CI for r = 0.6 runs from −0.41 to 0.95. Selection is now **anchored on the target actor**. Cheap actors only screen gross execution failures and supply traces until they earn pruning authority under the pre-registered rule.
5. **The best-matched literature was missing.** Racing for algorithm configuration (F-Race, irace), best-arm identification and noisy selection fit expensive stochastic evaluations. MCTS-AHD, AB-MCTS, ShinkaEvolve and AdaEvolve score each candidate once with a deterministic evaluator. AB-MCTS's own results also show best-of-N matching it at its main budget. We use those papers for generation, not for allocation.
6. **Problem C had warnings but no design.** We added within-episode randomisation of mode switches with logged probabilities (micro-randomised / SMART designs), `never` and `always` comparison arms, and a time-shift placebo. We also flagged aliasing: in most episodes, month 8, eight months at the current level and two months after the first review are the same moment.
7. **Rules.** The docs describe development clients over **stdio** only, so HTTP transport and many sessions on one shared server are not sanctioned. Our first diagnostics did use HTTP locally; all real-game runs now use stdio. The organiser message was too long and named no caps; it has been replaced by a four-item yes/no message. The plan was not tied to the three score cutoffs; it now is (section 7).
8. **Compliance precedents.** The 73,858-game random batch and the AI-driven "manual" session are not evidence that such methods are authorised. The message discloses both.
9. **The worker harness was not enforced.** Claude Code loads user plugins, hooks and memory by default, and the desktop app exports variables such as `CLAUDE_CODE_EFFORT_LEVEL` that override CLI flags. Workers now run with no setting sources, strict MCP configuration, only the game tools and a scrubbed environment.
10. **Records lacked fields** needed for valid analysis: launch index, block, analysis role, resumed flag, per-month trajectory, decision-point data and full actor configuration. The registry and trajectories now store them.

## 2. The decision: target-anchored racing over LLM-proposed policies with a reversible archive

### 2.1 Three loops, three kinds of agent

| Role | What it is | Never does |
|---|---|---|
| **Builders and analysts** | Opus 5.5 orchestrator and native Claude Code subagents or workflows. They write code, audit, diagnose traces and propose policies. | Play evaluated episodes; edit a frozen policy. |
| **Policy workers** | One actor per episode: scripted executor, isolated `claude -p` worker, or the official runner (JiuwenSwarm + designated model). Each plays one complete game from a frozen bundle. | Change their own policy; see other episodes; call tools other than the five game tools. |
| **Programmatic planner** | `careerlab.scheduler` with the registry and the gate. It leases jobs, runs workers on isolated servers, integrates results as the single writer, and applies the pre-registered rules at block boundaries. | Rely on an LLM to remember budgets, leases or protocol rules. |

### 2.2 Generation: policies are complete, testable hypotheses

A policy is a frozen Skill bundle, either `manifest.json` instruction plus `skills/*/SKILL.md`, or a scripted rule set. Its identity is the SHA-256 of its exact bytes. Each policy records its parents (a multi-parent graph), the hypothesis, the predicted observable behaviour and what would refute it. Before any spend, the compliance linter checks for named events, unpublished thresholds or weights, calendar triggers, non-English text and injection phrases.

The orchestrator chooses among these operators:

- **New family:** a substantively different behaviour.
- **Refine:** a targeted fix driven by trace diagnostics, as in GEPA/EvoTest reflective mutation.
- **Recombine:** modules from different branches.
- **Specialise:** a mode with entry and exit conditions on observable state or feedback (the options framework).
- **Wild:** a contrarian or large change, used on stagnation, with a written learning goal.

The archive keeps behaviourally distinct policies. Duplicates are rejected by hash, and near-duplicates are rejected when their predicted behaviour does not differ (the ShinkaEvolve novelty-rejection idea).

The initial families are deliberately distinct: minimal baseline, steady balance, invest early (late-benefit hypothesis), feedback-reactive, visible delivery, relationship capital, commitment ledger, and the same content packaged as one Skill versus three. Matteo's three-Skill candidate enters as an external frozen policy. The number of Skills is a factor to test, not an assumption.

### 2.3 Allocation: racing on complete episodes

- **Blocks** interleave all active arms. A block gives each arm one complete episode by default; top-two Thompson sampling assigns any extra slots. At least 20 % of slots go to new candidates, and the number of children per family grows as ⌈(1 + N_f)^0.5⌉.
- **Decisions** are taken at block boundaries, on prefix-complete data. They use normal–normal partial pooling within families (τ² floor 9) and a Bayesian-bootstrap robustness refit; a decision that flips is recorded as inconclusive and gets another block.
- **Dormancy is reversible.** A policy goes dormant after at least 4 terminal episodes if `P(μ ≥ μ_leader − 4) < 0.05`. Its reason and review trigger are recorded. Audits draw dormant policies with logged probability 0.2 per block, so we can estimate false rejections and reopen candidates. Only invalid, duplicate or non-compliant artefacts are retired.
- **Sample sizes follow the observed variance** (`n ≈ 9 σ_U² / Δ²` with an upper-bound σ re-estimated each block), not a fixed number. When the budget cannot reach the precision target, the result is labelled an estimate.

### 2.4 Validation and submission

Finalists are frozen and evaluated on fresh episodes in the official runner. A confirmation batch never feeds selection. Claims to the jury come only from confirmation data (one look, one-sided Welch bound, Bonferroni over at most two claims). Otherwise we present estimates with intervals.

Stage 1 is the maximum over at most three scored versions, and identical content is not rescored. At each cutoff we therefore submit the distinct valid version with the highest posterior predicted version score, and break ties in favour of the simpler, cheaper policy.

### 2.4b Stall handling with the competition playbook

The teammate library in `research/competition-playbook/` (36 cards from 17 competition cases) is the idea bank for stalls. A stall is detected from evidence, never from impatience. The pre-registered triggers are: stagnation (no leader gain of Δ/2 over three blocks), recurrent execution failures, a cheap–target rank reversal, a suspicious calendar pattern, or coordination cost growing faster than useful episodes. The orchestrator matches the symptom to the diagnostic table in `playbook.md` §1 and writes at least one alternative explanation. It then selects a few cards and turns each into a candidate with a frozen comparator under the protocol.

Every candidate records its **idea origin** separately from the **experiment run**: `idea_origin: playbook:<card>/<case>` in the policy metadata, with registry experiment and job identifiers for what was actually executed. Cards that have not been run stay hypotheses with their trigger. A champion's mechanism is never presented as a validated improvement for this game. The card-by-card decisions from today's source review are in `research/careerlab/playbook-decisions.md`.

### 2.5 Why not the alternatives

| Alternative | Why not as the backbone |
|---|---|
| MCTS-AHD / AB-MCTS trees as allocators | They score each node once with deterministic or surrogate evaluators. Our evaluation is stochastic, expensive and actor-dependent. AB-MCTS's own main-budget results show best-of-N matching it. We keep the generate-versus-refine choice; allocation uses racing. |
| ShinkaEvolve / AdaEvolve controllers | They use single evaluations, and the reported ablations are on deterministic tasks (circle packing). We reuse the archive, novelty rejection and stagnation response, not the fitness signal. |
| Successive halving / Hyperband on truncated episodes | Score curves can cross (problem B), and a rank cut on 2 noisy episodes misranks about 25–37 % of pairs. It is allowed only after the pre-registered proxy validation. |
| Hoeffding union bands | They cannot fire at feasible n. |
| Pure best-of-N or refine-the-leader | Kept as equal-budget baselines. If they win in the testbed, we say so. |
| Cheap-worker pruning from the start | Pruning would rest on actor bias (problem A) without a measured bound. It is allowed only with pruning authority. |

### 2.6 Known mechanisms, our adaptation, demonstrated results

| Level | Content |
|---|---|
| Known mechanisms (cited) | Racing / irace; best-arm identification and top-two Thompson sampling; hierarchical partial pooling; betting confidence sequences; GEPA/EvoTest reflective prompt evolution; quality-diversity archives; options; micro-randomised trials and SMART designs; prefix-complete analysis of asynchronous sampling. |
| Team adaptation | Objective `Y` that reproduces the official per-run contribution, including the early-exit token cap. A gate that ties actor use to written authorisation. Target-anchored selection with cheap actors restricted to execution screening and traces. A reversible archive with audited dormancy. Specialisation accepted only against both the `never` and `always` arms with a placebo. A submission rule for a maximum over three versions. Infrastructure that respects the measured retention limit and resumes in-session after observing first. |
| Demonstrated so far | The infrastructure facts in section 5 and the kill / resume test. Synthetic comparisons are pending (they show behaviour under known mechanisms, not real-game gains). **No real-game policy improvement has been demonstrated yet.** |

## 3. The three problems

| | A. Worker capability and bias | B. Late benefits | C. Deceptive specialisation |
|---|---|---|---|
| **Risk** | A good policy fails because the worker cannot execute it; or a worker's own judgement fills gaps and inflates weak policies; rankings differ between models. | A policy that invests early looks bad at months 6–12 and wins at 48; interim data and truncated proxies discard it. | A "month 8 rule" really reflects accumulated state, feedback, level duration or which games survived. |
| **Detection** | Separate statistics per actor. Execution audits on trajectories: invalid actions, tool errors, rule adherence on sampled decisions. Decision-level probes: the same logged observation given to several actors. Rank comparison on shared policies when affordable. Logged-probability audits of dormant candidates on the target. | Per-month trajectories. Kaplan–Meier and RMST by policy. Crossing survival or score curves. Rank correlation between month-k proxies and final `Y` on completed episodes. Interruption rate by episode length. Audits of dormant candidates. | Within-episode randomised switch with logged probability and visible state. `never` / `always` arms. Time-shift placebo on a random month in 5–12. Aliasing check between month, level duration and review cadence. Effects among survivors versus fresh games. |
| **Reduction** | Selection only on the target actor. Cheap actors screen execution failures only. Actor configuration frozen and hashed. Worker harness isolated and run with the official prompts. Policies written so the actor can execute them. | Complete episodes only. Prefix-complete, block-synchronous decisions. Timeouts ≥ 3 × the median completed duration. No truncated screening without validation. | Compare complete policies from fresh games. Ship only qualitative state- or feedback-based modes. Calendar arms are diagnostic and never shipped. Accept only if the policy beats `max(never, always)` by Δ with probability ≥ 0.8. |
| **Assumptions** | The dev target actor approximates the official one (provider routing may differ, so we log it). Behaviour is stationary within an epoch. | Episodes are independent within a cell. Interruptions are not caused by the outcome (we check this). | Positivity at decision points. No carry-over between episodes. The visible state captures what the mode condition needs. |
| **Evidence it is failing** | Rank reversals between cheap and target actors on shared policies; any audited false rejection; compliance rates that differ by actor; official scores far from predictions (`|z| > 2`). | Interruptions concentrated in long episodes; interim-versus-final rank flips; dormant policies reactivated by audits; KM curves diverging late. | The placebo reproduces the effect; the gain exists only conditional on survival; it vanishes in fresh games; triggers fire at the same decision point. |

## 4. Orchestration and models

- **Account.** This desktop session runs on the Max plan (5-hour 7 %, weekly 2 %, extra usage off). The `claude` CLI on this Mac is logged in as `subscriptionType: pro`: its own rate-limit events show 46 % of the five-hour window and **79 % of the seven-day window**, which resets 30 Oct 07:00 UTC, with overage rejected. Headless workers therefore use a different, nearly exhausted quota until the user runs `claude auth login` with the Max account. Native subagents use the Max quota.
- **Builders and analysts.** The critical audit used 16 Opus agents: 3.43 M subagent tokens, 676 tool calls, 30 minutes of wall-clock. It produced 43 upheld corrections, 11 refutations and a rules-and-statistics redesign that one context could not have produced with the same independence. Coordination stops paying when agents need each other's intermediate state; implementation was therefore split into components with disjoint files and adversarial review per component.
- **Workers.** `careerlab/actors/claude_cli.py` freezes model, effort, skills mode (inline or Claude Code plugin), autocompact window, CLI version, prompts (verbatim from the official runner), isolation flags and the server command. Each episode gets its own stdio server in competition mode with a fresh database. The planner verifies the end state with its own client and re-prompts with the official continuation prompt if the worker stops early.
- **What we will compare across Haiku / Sonnet / Opus (default and low effort, and Opus with a compact autocompact window):**
  - strategy quality: `Y` on shared policies;
  - instruction following: rule-adherence audits;
  - tool errors and invalid actions;
  - speed: wall-clock and API time;
  - tokens: input, cache, output;
  - list-price-equivalent cost and quota consumption per episode, from the rate-limit deltas.

  Fast mode is not available headless (`sdk_opt_in_required`). This comparison needs authorisation on the real game. On the synthetic testbed it measures only harness behaviour.

## 5. Fast, safe game execution (measured)

- **Latency:** `observe` ≈ 6 ms and `take_action` ≈ 14 ms over stdio; server start-up ≈ 1.4 s.
- **Throughput:** one process per concurrent session, scaled by processes. Sixteen processes reach ≈ 530 actions/s, ≈ 22 short episodes/s and an estimated ≈ 3 full 48-month episodes/s (≈ 170 actions each). Concurrency inside one process adds latency without adding throughput.
- **Isolation:** separate `CAREER_EMULATOR_DB` paths are isolated across processes. The same path is shared. **Without the variable, processes in different folders share one default store.**
- **Retention limit:** a database keeps about 20 sessions, and creating more evicts sessions, including active ones. The pool rotates to a fresh database every ≤ 12 sessions. One early benchmark that ignored this lost 22 active sessions; all were classified `interrupted` and none was scored.
- **Ambiguous replies:** observe before any retry. A lost reply after the action was applied is inferred from the state change; a lost request is retried exactly once (tested).
- **Recovery:** after `kill -9`, jobs are reconciled against real processes and result files; episodes are resumed in their own session (flagged `resumed`) or replaced.
- **Scale-out:** the same code runs on cloud workers. Paths are configurable (`CAREERLAB_DATA`, `CAREERLAB_LAB_DIR`, `CAREERLAB_RUNNER_DIR`), and planners can be sharded per machine because each pool owns its databases. Millions of scripted episodes would take ~100 machine-hours, **if ever authorised**. Infinite repetitions would not reveal the hidden test set.

## 6. Rules and gates

The gate (`lab/gate.json`) is checked by the planner before any job is queued:

- **Allowed now:** scripted development clients over stdio on real dev, capped at 1,500 sessions in total pending an answer (≈ 900 used); anything on the synthetic testbed.
- **Closed:** Claude actors on the real game, and the self-funded target route.
- **Not yet available:** the competition key, which requires a verified preliminary submission.

The four-item organiser message is in `research/organiser-questions.md` §0 and must be posted by the team. Nothing in this lab changes what a submission may contain: no named-event answers, no learned thresholds or weights presented as rules, single-agent JiuwenSwarm 0.2.4b3 in `agent` mode, and only the designated model.

## 7. Timeline tied to the score cutoffs (24:00 UK)

| When | Lab output | Submission |
|---|---|---|
| 26 Oct (today) | Infrastructure, protocol, families, synthetic validation. **Team:** preliminary package for the key, the organiser message, a decision on a self-funded target budget, CLI login to Max. | — |
| 27 Oct (R1) | 2-episode target cost pilot as soon as a target route exists; families pass the linter. | Best-justified family as an **estimate**, with presentation.mp4 (required in the first final ZIP). |
| 28–30 Oct (R2) | Racing among 6–8 families on the target in blocks; trace-driven children; audits. | Posterior-best distinct version. |
| 31 Oct–1 Nov (R3) | Freeze, then confirmation versus the incumbent; refinement only on development data. | Distinct version chosen by the submission rule; design docs and video tell the evidence story. |

## 8. Next most useful experiment

The **target cost-and-fidelity pilot**: two complete episodes of the minimal baseline and two of one reasoned family in the official runner with the designated model. It measures tokens per month, the `E` term, wall-clock and cost per episode, and so sets the whole target budget. These are the numbers every later sample size depends on. It needs a key or an approved self-funded route. Until then, the most useful work is the synthetic method comparison and the compliance review of the family bundles.
