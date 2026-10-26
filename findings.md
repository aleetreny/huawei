# Findings — 26 October 2026

- Repository: https://github.com/aleetreny/huawei (private), cloned into the requested directory; existing preliminary/ preserved.
- Official docs: https://techarena-career-sim.readthedocs.io/en/latest/.
- Binding rules: competition-rules.html; final structure: submission.html.
- Required platform JiuwenSwarm 0.2.4b3 exactly, mode agent, English deliverables.
- Stage 1: 80% mean quantitative_score across three official runs, 10% mean Skill quality, 10% token efficiency. Top ten only: final = 70% Stage 1 + 30% expert review.
- Final ZIP needs an English presentation.mp4 (maximum ten minutes), including at first interim submission; preliminary does not.
- Cutoffs: 27 October, 30 October, 1 November 2026, each end of day in GMT.
- Five official tools only; own outputs and manual CLI testing permitted. No reading internal packages or simulation database.
- Prohibited submission knowledge includes unpublished formulas/thresholds presented as known rules, irrespective of how derived; fixed named-event answers also prohibited.
- Rule silence requires asking organisers in Discord before using an uncertain method. No bulk-call authorisation established.
- A search result exposed an issue discussing package-internal findings; excluded from evidence and strategy.
- All nine substantive official documentation pages reviewed: home, rules/fair play, API key, quickstart, packages, MCP, handbook, public rules, failure/endings and submission (ten including home).
- Official participation repository verified accessible and public: RAI-Internal/techarena-career-sim. User repository is a separate preliminary-design repository, not yet a configured runner.
- Existing preliminary files identify Gradient Depression and have two coherent English Skills; they are an untested initial design, not a final package.
- Search work: 19 Exa queries requesting 200 results; candidate index saved in research/search-audit.md. Search results are not 200 full-text verified sources.
- Strong relevant precedents: Huawei Ireland 2024 SA and CP-SAT/pattern-search author repositories; UK 2023 architecture predictors; UK 2025 Cangjie; same-family CareerSim-BDCI26 cannot establish UK permissions.
- Transferable methods: GEPA-style trace-driven prompt revision; Hyperband-style complete-run resource allocation; rliable-style uncertainty reporting; bounded quarterly public-action enumeration. Full MCTS needs a valid generative branching simulator, absent from documented MCP.
- Token-efficiency full mark plateau is 500,000 tokens/month, or 24 million total for a 48-month run; much lower token use can still matter to the USD 50 development budget.
- No game runs, API credits, messages or submissions performed.

## User reset and teammate evidence
- User revoked the two-Skill proposal and authorised ordinary exploratory gameplay and UI interaction. Four preliminary files deleted locally; teammate branch preserved.
- Refreshed origin/Matteo to 0eb0924. It contains a manual local browser adapter using only official MCP call_tool operations, and aggregate results from a uniform-random driver.
- Teammate reports 73,858 sessions, 1,563,578 actions, 5.9056 mean survival months, 11.7842 mean score, 0 completions and maximum survival 24. These are teammate-reported aggregates, not independently reproduced.
- Outcome counts show 40,496 Blackout and 30,559 Trust crisis. Competing risks mean their dominance does not establish a global priority ranking.
- Raw trajectories, per-run score variance, complete harness and provenance of organiser approval for bulk runs are not present in the tracked branch files reviewed.
- No dedicated game MCP tool is exposed in this Codex session. Attempting the teammate's reviewed stdio MCP adapter in an isolated local preview instead.
- Adapter works: played manually through official MCP in the browser to beginning of month 7, after two quarters; first review C, level L1, still alive. This is one incomplete manual session, not a scored agent benchmark.
- Current-run observations: story continuations cross months; action-log deltas and dashboard increments can differ; unaffordable two-cost actions can remain listed; first review feedback appeared before month-6 quarterly allocation.
- Modern source follow-up: GEPA and EvoTest (ICLR 2026), Meta-TTL and PACEvolve++ (2026), best-arm identification/top-two, TuRBO, quality-diversity, DreamerV3, Bayesian design. Seven additional searches requesting 54 result slots; selected originals fetched.
- Proposed experimental architecture: separate within-episode policy, candidate generation, adaptive evaluation allocation and frozen validation. No fixed Skill count selected and no learned hidden formula deployed.

## CareerLab build — 26 October 2026 (orchestrator integration log)

### Official interface facts verified by our own client (five tools only)
- `career-emulator-engine-mcp --help` documents `--transport stdio|http|sse|streamable-http`, `--host/--port/--path`, and `-c/--competition` ("only one new game session allowed").
- The official runner (RAI-Internal/techarena-career-sim@00b084a8, `career_sim_runner/setup.py`) launches the server with `--update skip` and env `CAREER_EMULATOR_DB`, `CAREER_EMULATOR_LOG_DIR`, `CAREER_EMULATOR_ACTIVE_LONG_CHAIN_LIMIT=1`, `CAREER_EMULATOR_MONTHLY_EVENT_LIMIT=3`, `CAREER_EMULATOR_MAX_NOTE_LENGTH=1000`. CareerLab uses the same values. Matteo's adapter set none of them, so his random batch may not match the runner's environment (equivalence unknown).
- The runner resets the JiuwenSwarm agent memory (`MEMORY.md`) and skills workspace on every install; IDENTITY.md (skill names + manifest instruction) stays in the system prompt across context compression.
- `observe` returns `ending_score` at termination: `outcome`, `survival_months`, `completed`, `quantitative_score`, `competition_partial_score`, and per-dimension `raw_value/normalized_score/weight`. Weights are observed dev-run output, not published rules: lab analysis may use them as auxiliary metrics; Skills must not embed them.
- Quarterly phases list `energy_cost` and `status_updates` (including `HiddenRisk`) in the current observation. An unaffordable choice returns `success: false` ("Insufficient energy ...") without advancing.
- Unknown session in `observe` returns a payload with `current_state.error`, not an MCP error flag; the client now raises on it.
- Isolation (diagnostics.check_isolation): separate `CAREER_EMULATOR_DB` paths are isolated across processes (Unknown session_id); the same path is shared; **without `CAREER_EMULATOR_DB`, processes started in different working directories share one default store** — changing folders does not isolate. Two sessions on one server do not affect each other; 8 concurrent `observe` calls on one connection return their own sessions; competition mode rejects a second `new_game` with an error payload.
- Timing on this Mac (18 cores): `new_game` ≈ 57 ms, `observe` ≈ 9 ms over stdio; a random 19-step episode took 0.4 s.
- **Session retention limit (verified through the five tools only):** one game database keeps about 20 sessions. Creating the 21st session made the 1st unknown; with 18 idle + 3 active sessions, creating 5 more evicted the active ones too. In one probe that observed every session after each creation, all 21 sessions became unknown at once. Consequence: an operational interruption that must never be scored; CareerLab rotates to a fresh database after at most 12 sessions per server process (`careerlab/pool.py`). The bench run with 48 episodes through one 16-way server lost 22 active sessions this way; all were classified `interrupted`, none scored.
- The first throughput figures (≈55–70 steps/s) were dominated by sequential server start-up (≈1.4 s per process); steady-state per-process latency is ≈6 ms `observe` + ≈14 ms `take_action` over stdio.
- **Account limits (checked 11:30 UTC):** the desktop session reports plan Max, 5-hour 7 %, weekly 2 % (reset 26 Oct 16:00 UTC), extra usage disabled. The `claude` CLI on this Mac is logged in as the same e-mail but reports `subscriptionType: pro`, and its rate-limit events show five-hour 46 % (reset 14:10 UTC) and seven-day **79 %** (reset 30 Oct 07:00 UTC), overage rejected. Headless `claude -p` workers therefore draw on a different, nearly exhausted quota unless the CLI is re-authenticated with the Max account (user action). Native subagents of this session use the Max quota.
- Worker isolation that keeps subscription auth: `--setting-sources "" --strict-mcp-config --mcp-config <file> --tools "" --allowedTools mcp__<server>__*` exposed only the configured MCP tool, no user plugins, hooks or skills (builtin plugins only). `--safe-mode` also disables `--mcp-config` servers, so it cannot be used for game workers. `--bare` needs an API key. Fast mode in `-p` reports `sdk_opt_in_required`.

### Pilot P1 — scripted policies on real dev through the full pipeline (26 Oct, 150 terminal episodes)
- Registry + rotating stdio pool + scheduler, 12 slots; interleaved launch order by replicate.
- Kill test: the scheduler was killed with `kill -9` mid-run (12 episodes in flight, 24 leased). `careerlab resume` reconciled: 12 interrupted (process gone, no result), 24 released to the queue; 10 interrupted episodes were continued in their own game session after observing first (`resumed=1`), 2 had no recorded session and got replacement attempts. Final: 150 terminal evaluations, 2 interrupted attempts kept on record and never scored.
- Per-cell results (Q = quantitative_score, n = 30 each): uniform 9.97 (SD 5.50), uniform-affordable 13.15 (5.48), quarterly-wellbeing 12.51 (4.74), quarterly-growth 12.47 (3.56), quarterly-risk 12.96 (5.11). Median survival 6–7.5 months; no completions; exits: Trust crisis 84, Blackout 53, Broke 11, resignation 2. Random story choices dominate early exits, so scripted quarterly rules cannot separate behaviour families: they are floors and infrastructure probes only.
- About 3.5 actions per survived month, so a full 48-month episode is about 170 actions; at the measured ~530 actions/s with 16 processes this Mac could run roughly 3 full scripted episodes per second (~11k per hour) if ever authorised.
- **Max-plan consumption measured (12:02 UTC):** after the 16-agent audit (3.43 M subagent tokens), the build workflow (in progress) and the playbook review (in progress) plus this orchestrator, the desktop Max plan shows 5-hour 14 % and weekly 4 % (both reset 26 Oct 16:00 UTC). Multi-agent work at this scale is far from the binding constraint; the scarce resources are target-actor episodes and the organiser authorisation.
- All ten Skill-policy bundles (P0, F1–F7, M3) pass the official `career_sim_runner validate` (structure, manifest `mode: agent`, team name, front matter) when wrapped in a temporary solution directory.
- Target slots (`careerlab/actors/official_runner.py`): a private runner clone, HOME and database per slot; `career_sim_runner setup` writes the instance MCP config with the slot's own `CAREER_EMULATOR_DB` and the official engine settings. A full target episode needs credentials.
- **deepseek-v4-flash price (OpenRouter public endpoint list, fetched 26 Oct 12:50 UTC):** model "DeepSeek V4 Flash 0423", 17 providers. Most endpoints charge USD 0.083–0.15 per M input tokens, 0.017–0.03 per M cache reads and 0.17–0.30 per M output, with fp8 or fp4 quantisation depending on the provider. Illustrative cost of one full JiuwenSwarm run: 12 M tokens with 80 % cache reads and 0.3 M output come to about USD 0.6; the 24 M-token full-mark ceiling comes to about USD 1.2. These are assumptions until a 2-episode pilot measures real usage. On this estimate, a team budget of USD 30 would buy roughly 25–50 target episodes. Routing is price-weighted and providers differ in quantisation, so a team-funded route must log the provider and cannot assume identity with organiser routing.

### User decision and real-game Claude workers (26 Oct, about 12:05 UTC onwards)
- User decision in chat: do not ask the organisers; methods not prohibited by the rules are approved by the team. Claude workers may play the real dev game before the key arrives, and the key's USD 50 must be managed carefully across three submissions. Recorded in `lab/gate.json` and as a registry decision. The rules text ("absence of an express prohibition is not permission") is unchanged, and the risk is accepted by the team.
- The CLI is now logged in to a Max account (`subscriptionType: max`). Its rate-limit windows match the desktop session (five-hour 19 %, seven-day 5 %, both reset 26 Oct 16:00 UTC), so headless workers and this orchestrator share one quota.
- Smoke test (Haiku, policy P0, real dev, isolated `claude -p` worker): the worker read the handbook once, created its own session and played at about 17 actions per minute. Its cached context grew by about 1k tokens per action (≈19k after 19 actions).
- **Playbook P01 interface check (scripted, real dev, 26 Oct):** a `take_action` note up to 1,000 characters comes back verbatim in `check_latest_logs`. Longer notes (1,001 and 3,000 characters) are accepted, with the action applied and `success: true`, but are **silently truncated to 1,000 characters**, which matches the runner's `CAREER_EMULATOR_MAX_NOTE_LENGTH=1000`. Consequence for ledger-style Skills (F6): keep the note under 1,000 characters and put the most important items first.
- **First real-game Claude episode (smoke test, about 12:10–12:24 UTC):** Haiku 5.5 with the minimal policy P0 **completed all 48 months**, quantitative_score 53.88. Dimension scores: level 40, wealth 33.75, resilience 95, skill 72.5, risk control 40, network 60. Run figures:
  - 197 actions and 378 turns, 0 rejected actions, 0 extra sessions, 0 non-game tool attempts;
  - 13.5 minutes of wall-clock time;
  - tokens: 31.35 M cache reads, 0.16 M cache writes, 52.6 k output;
  - list-price equivalent USD 1.24 (subscription, not billed);
  - five-hour window 19 % → 21 % (an upper bound: other agents were also running).

  For comparison, the scripted floors average 10–13 and exit around month 6. If cached tokens count in the official `total_tokens`, a history-accumulating agent would use about 650 k tokens per month, so `E` ≈ 94 rather than 100. Context management is therefore a small but real lever.
- **Incident (about 12:47 UTC), caught before any duplicate ran:** a second scheduler, started for Haiku screening while the E-W1 scheduler was running, called `recover()` at start-up. The heartbeat was refreshed only when an episode finished, so the live scheduler looked dead: its 22 leased-but-unstarted jobs were released and re-leased, and 4 of them started in the second process. The live scheduler still held those jobs in memory, which would have produced duplicate runs into the same directories. The orchestrator killed the second scheduler and its workers, then fixed the code:
  - an owner counts as alive if its PID exists on this host, otherwise if its own per-owner heartbeat (refreshed every 20 s) is fresh;
  - `recover()` never touches jobs whose owner is alive;
  - a job is claimed atomically before it starts (`status='leased' AND lease_owner=me`);
  - leasing can be filtered by purpose.

  Tests were added. The 4 killed calibrate attempts are re-run by the original scheduler, and 2 killed screen attempts were re-queued as new attempts. No interrupted run was scored.
- **Early Claude-worker diagnostics (first 13 real-game LLM episodes, 26 Oct about 12:50 UTC; n is tiny):** results are bimodal: either the 48 months are completed (Q ≈ 51–57) or the run is eliminated (Q ≈ 17–45). Early exits come from two published failure directions:
  - "Dismissed for capability — a second weak half-year review": 5 cases, all at month 24;
  - "Trust crisis — a second major blow-up": 4 cases, at months 23–39.

  The dismissed runs show weak review grades in the run's own feedback, for example C, C, then D at month 24 ("Half-year performance bonus (C)", "half-year review fell short… the next one has to be better"). That feedback is explicit and arrives during the run, so a policy can react to it legitimately, without any threshold. This is the main generation diagnostic for block 2: a review-recovery response to weak-review feedback, and risk defusing after blow-up warnings. Sonnet and Opus are not yet better than Haiku on these policies (n = 1–2 per cell; no conclusion).
- **Preliminary block-1 picture (31 Claude episodes on real dev, 13:05 UTC; not yet a protocol decision; 1–3 episodes per cell):**
  - F1 steady-balance leads with almost every actor: Haiku 51 and 66.6, Haiku@low 55.2, Opus 56.2, Opus~100k 69.8 (exceptions: Opus@low 40.2 and Sonnet 30.7, both trust crises).
  - P0 minimal, F4 visible-delivery and both F7 packagings follow (Haiku 50–57).
  - M3 (long, three Skills), F2 invest-early, F5 and F6 trail. They are mostly dismissed at month 24 after weak reviews, or end in a trust crisis. F2's late-benefit bet dies before it can pay off.
  - The actor matters a great deal (problem A). Sonnet completed 0 of 6 episodes (mean Q 26). Opus with low effort (52.3) or compact context (50.3) beat default Opus (33.9) on the same three policies. Haiku and default Opus order P0/F1/M3 the same way; Sonnet does not.
  - Context: Opus~100k used about 0.12 M cache-read tokens per survived month, Haiku about 0.41 M. Both are under the 500 k/month full-efficiency line, if cached tokens count the same way in the official total.
  - Speed: about 0.2–0.28 minutes per game month, so 10–13 minutes per full episode.
- **Quota throttling:** at 13:00 UTC, with 24 parallel workers, the shared five-hour window rose about 0.9 points per minute (30 % → 44 % in about 15 minutes). The orchestrator stopped the 12-slot scheduler and re-queued its 12 unfinished episodes. It also added a governor: `careerlab run --max-five-hour 0.55` holds new episodes above the cap until the 16:00 reset, because this orchestrator session shares the window.
- **First pre-registered block decision (Haiku actor, 13:25 UTC; `careerlab/decisions.py`, recorded in the registry):** prefix-complete runs, family-pooled posterior, robust across normal, Student-t and Bayesian-bootstrap fits.
  - Leader: F3 feedback-reactive, posterior Y 61.3 (SD 1.8), P(best) 0.57, 3 runs.
  - Second: F1 steady-balance, 58.0 (7.2).
  - Then F7 three-skills 50.0 and F7 single-skill 48.8.
  - P0 minimal goes **DORMANT** (4 runs, P(μ ≥ μ_leader − 4) = 0.008). This is reversible and stays subject to audits.
  - Every other cell repeats (fewer than 4 runs). The five block-2 children have 1–2 runs each and are not yet above their parents.
- **Block-2 children (Haiku, 3 runs each; second block decision at 13:36 UTC, robust across noise models):**

  | Child | Posterior Y | Parent | Parent Y |
  |---|---|---|---|
  | f2-convert-on-review | 45.9 | F2 | 31.1 |
  | f1-review-risk | 49.1 | F1 | 56.2 |
  | f4-review-first | 45.1 | F4 | 44.9 |
  | p0-review-guard | 41.2 | P0 | 40.8 |
  | m3-subtracted | 40.1 | M3 | 39.9 |

  Converting to visible delivery after the first weak review rescued the invest-early idea. Bolting extra rules onto an already good policy (F1) hurt it, which matches playbook P20. The other review guards did not help. F3 remains the leader at 61.3.

  Next generation, within the progressive-widening limit (2 children for the F3 family): an F3 subtraction (P20) and an F3 × F1 recombination (P14).
- **State at hand-off (14:15 UTC):** 99 Claude episodes on real dev, plus 150 scripted and the infrastructure tests.
  - Final Haiku block decision (robust): the F3 family leads. F3 60.2 (3 runs), f3-balance-recombined 58.9 (2), f3-lean 57.5 (2), then F7 three-skills 50.0, F1 49.3 (4) and the F7 single Skill 48.8.
  - **P0 and M3 are DORMANT.** Every other cell still repeats.
  - By actor (all policies): opus~100k completion 0.83, mean Q 57.8 (6 eps); Haiku 0.55 / 45.5 (53); opus@low 0.40 / 43.2 (5); Sonnet 0.38 / 39.4 (26); haiku@low 0.33 / 39.2 (6); opus 0.33 / 33.9 (3).
  - Compact context helps the strongest model; Sonnet is consistently weak in this game.
  - Synthetic method comparison (R = 100, `lab/reports/synthetic-method-comparison/`): racing and the full method beat best-of-N and refine-the-leader. The full method cuts false rejections 39 % → 10 % and gives unbiased confirmation. Truncated screening is the only clearly harmful ablation.
  - Cloud execution verified, and `lab/CLOUD_RUNBOOK.md` carries the lab on unattended.
  - Opus teacher digests (14:38 UTC, `careerlab digest --model opus`, `lab/reports/teacher-digests/opus/`): 14 Opus games, 8 completed. Every game opens with a C review. Eliminations at month 24 follow C C D D (second weak review) or a trust crisis after B grades; completed games climb from B to A after month 30. Opus never played F3, so distilled F3 children carry rules learned under F1, P0 and M3.
  - Install pitfall: in this iCloud folder the venv's `.pth` files carry the macOS `hidden` flag, which Python 3.13 skips, so `careerlab` stopped importing. Fix: `chflags nohidden .venv/lib/python3.13/site-packages/*.pth`. The flag comes back, so pytest now also sets `pythonpath = ["."]`. A venv outside iCloud (`UV_PROJECT_ENVIRONMENT`) avoids it for good.
  - Quota (14:42 UTC, app usage card): five-hour 86 %, weekly 15 %, and both reset 26 Oct 16:00 UTC. The new weekly window covers the rest of the competition. Today about 86 % of one five-hour window cost about 15 % of the week, so running at the five-hour cap in every window would empty the week in about two days. The governor now also paces the seven-day window: a straight line from 10 % at the window start to 90 % at 1 Nov 24:00 UK, about 12.6 % a day, keeping 10 % for the team's own chats.
  - Where completed games lose points (48 completed games, all actors): level 16.2 and wealth 13.1 of about 40 missing points; risk control 3.5, network 3.4, skill 3.3, resilience 0.2. Every family so far optimises survival, and none pushes promotion and wealth once survival is safe. This is the clearest coverage gap.

## Cloud race and organiser (26 Oct, 14:12–16:20 UTC, branch `cloud-lab-run`)
- The registry's actor records freeze Claude CLI 2.1.303, but the cloud container ships 2.1.310. Under prereg §1 a new CLI version would be a new actor cell, so the cloud pins 2.1.303 (`npm install --prefix ~/claude-2.1.303 …`, `CAREERLAB_CLAUDE_EXE`). With the pin, `claude-cli:haiku` and `claude-cli:opus~100k` resolve to the existing ids `08e9167a965ed82c` and `eaaedd84f8f22e6d`.
- The quota governor reads quota only from local worker streams. A fresh container has none and would launch above the cap, so a one-line probe stream in `runs/_quota-probe/` seeds it.
- Haiku games take 6–14 minutes in the cloud container.
- Reporting fixes:
  - `block_decision` had recorded `robust: null`;
  - `analysis.load_cells` dropped episodes without a local `result.json`, and now falls back to the evaluation row.
- New candidates on Haiku, provisional (3–4 games each, before the batch-1 decision), mean Q:

  | Policy | Mean Q | Completed |
  |---|---:|---:|
  | f3-balance-recombined | 60.6 | 4/4 |
  | F3 | 55.3 | 3/4 |
  | f3-lean | 55.1 | 4/4 |
  | f3-distilled-prereview-defuse (f3-lean + R1) | 51.0 | 2/3 |
  | f8-secure-growth | 49.3 | 2/3 |
  | o1-promotion-gap | 44.0 | 2/4 |
  | o2-run-hot | 36.2 | 1/4 |
  | f3-opus-distilled (f3-lean + R1–R5) | 31.7 | 1/3 |

  Most losses are still the month-24 dismissal. The full distilled child replaces F3's weak-review factor plan with "keep Apply for a key project" (R4), and is dismissed at month 24 in 2 of 3 games.
- T10 energy bots (400 scripted games, own data directory, no Claude quota; `lab/reports/energy-bots/`):
  - Health is the first constraint when story choices ignore it. Every Energy mix without a Health point per quarter blacked out.
  - Recovering only once Health is low is too late.
  - Defuse + Health recovery was the best mix.
  - No mix avoids the C at the first review.
  - Surviving bots end at the same level and wealth as the LLM players.
- T13 Opus ceiling (`opus@max~100k`, clean-room policy `x0-opus-ceiling-v1`, thresholds pre-stated in `lab/reports/opus-ceiling/README.md`): the first game was dismissed at month 24, with Q 24.5.
- Organiser actions:
  - merged `leah/workspace` (T11: origins; the registry migrated in place while the race ran) and `matteo-t4-growth` (T4 value-conversion, registered as `91b30e8096ff6766`). 230 tests pass.
  - At the user's request, commits are authored as Alejandro Treny Ortega, with no Claude co-author lines. The 14 earlier `cloud-lab-run` commits were rewritten and force-pushed (that branch only).
- Block-3 trace diagnosis (Haiku games with local digests; `lab/reports/cloud-run-diagnostics/block3-generation.md`):
  - The weak-review streak is about leaving Level 1. No game got a B while still at Level 1 after its first review (0 of 47 reviews). Mean Q by first promotion: at review 1, 57.3 (12/14 completed); at review 2, 47.0 (7/11); none by review 2, 22.0 (0/13).
  - Energy and main-action mixes do not separate the groups.
  - Output at its run high at the review does: all 14 games promoted at review 1 had it, against 12/24 others. When Output or Network dropped through story choices after the last quarterly phase, 14/60 reviews were good, against 34/66 otherwise.
  - New candidates: f7-trend-marking, f7-delivery-stories, and f7-promotion-drive (stall slot, playbook P12).
- Problem A (preliminary): Haiku and opus~100k rank the shared policies differently (6 shared policies, Spearman −0.26, different top). opus~100k does worse with the F3 family than with F1 and P0.
- T13 Opus ceiling, complete (`lab/reports/opus-ceiling/README.md`): 6 games on opus@max~100k with the clean-room all-general-knowledge Skill.
  - Mean Y 54.2 (90 % t interval 41.6–66.7), mean Q 56.2, 5 of 6 completed. The one loss was the C C D D dismissal at month 24.
  - Against the pre-stated thresholds (reference 60.21): **"near the ceiling"**, so effort should shift to reliability and token efficiency.
  - Completed games lose 16.2 points on level and 12.8 on wealth, identical to the 45 other completed cloud games (16.2 and 12.6). The level and wealth plateau does not move with the strongest player.
  - Tokens: 0.13–0.16 M per month.
- Problem A, complete (6 opus~100k runs on the Haiku top 3):
  - On the 6 shared policies, Spearman 0.20, with the same top (F1).
  - opus~100k completes 2 of 6 games with F3-family Skills (posterior about 38–39), against 4 of 4 with F1 and P0 (61.6–65.6). Haiku rates the F3 family mid-table.
  - The Haiku ranking does not transfer to a stronger model, which adds weight to the target pilot (T6).

- Block decision #142 (18:11 UTC): the three trace-driven F7 children (trend marking, delivery stories, promotion drive) score 42–45 after 4 Haiku games each. Family pooling pulls their parent f7-three-skills down to 51.5. New leader f1-steady-balance, 54.6 (n = 8). `careerlab digest` now skips imported games that have no local run folder.
- Block-5 diagnosis (18:29 UTC, `lab/reports/cloud-run-diagnostics/block5-generation.md`): F1's exposure is blow-ups. It took Defuse after only 11 of 22 non-reassuring risk remarks and never after a blow-up. Across 86 Haiku games, Defuse after a risk remark cut blow-ups within three months from 10 % to 2 % (mild) and from 20 % to 8 % (strong). All 37 D grades came with a risk remark in the review month. Three nested F1 children are queued: core (P20), risk-signal, and status-line (P22, stall slot).
- Decision #150 (19:03 UTC): the top posteriors converge around 50–52 as data accrue. Leader F1 52.2 (n = 12); none has P(best) ≥ 0.2. This is consistent with the T13 'near the ceiling' reading.
- **Representation effect, preliminary** (decision #157, 19:31 UTC): f1-status-line (P22 stall slot) completed 4/4 (Q 57, 66, 70, 65; posterior 56.1, P(best) 0.45, PROMOTE).
  - Its two siblings carry the same rules in prose: f1-core completed 1/4 and f1-risk-signal 1/4.
  - Status-line format: fill `Act | Risk | Weakest` before every choice, then serve the first need, with a fixed note shape.
  - Transfer test queued: f3-status-line-v1 (`688cc25c03bf6629`), f3-balance-recombined's exact rules in the same format.
  - Matteo's observed-growth-v3 in the race: 61, 19, 52, 64 (his own-origin 71.4 does not replicate).
- 19:41 UTC: race switched to fastloop-v2 by user decision. F1 is champion; challengers are observed-growth-v3, f3-lean, f3-balance-recombined, f1-risk-signal, f1-core, f1-status-line and f3-status-line. Energy-bot check: 4 of 400 bots reached **L6** (Q 66.9–75.6). Each was promoted at each of the first three reviews despite a first-review C, and ended with Skill 100. No LLM game has passed L5.
- Fastloop, first hour (20:40 UTC):
  - f3-balance-recombined crowned at 20:03 (10/12 completed, Q 54.6, P(better than F1) 0.74). f3-lean (11/12, 55.5) and observed-growth-v3 (10/12, 55.4) missed with P 0.55 and 0.59.
  - **The status-line representation effect is not confirmed:** f1-status-line 5/8 (Q 52.7), f3-status-line 3/8 (Q 39.5). The early 4/4 was luck.
  - Discarded: f1-core 1/4 and f1-risk-signal 1/4.
  - Merged Matteo's first-review-search: 38.8 MB of raw data, including a dev-event catalogue with choice outcomes. Research only, never for designers or Skills; warning added to ESTADO.md.
- Fastloop hour 2 (21:38 UTC): first designer-made champion, **targeted-1026-201334**, crowned at 21:29 (10/12 completed, Q 53.9, P(better than f3-balance-recombined) 0.61). It adds to f3-balance-recombined: until the first promotion, keep Output and Network in stories.
  - Failed: stretch-1026-200334, which replaced Lay low with results actions when risk escalates (4/8, 46.7); targeted-1026-202436, which protected Skill, Network and Output in every story (2/4, 42.8); observed-growth-v6 (5/8, 47.1).
