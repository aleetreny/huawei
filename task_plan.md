# Task Plan: CareerLab — strategy laboratory for Career Survival

Global plan owned by the orchestrator (main Claude Code session, Opus 5.5). Workers and builder agents never edit this file; they write in their own run or report directories and the orchestrator integrates. The previous research-phase plan is archived at `research/archive/task_plan-2026-10-26-research-phase.md`.

## Goal

A tested, resumable laboratory that generates, evaluates and archives Career Survival policies through the official MCP server, with pre-registered statistics that handle worker bias (A), late benefits (B) and deceptive specialization (C), and evidence the team can show the jury.

## Next Step

Integrate build-workflow components (synthetic, stats, policies, search); run synthetic method comparison and harness smoke test.

## Current Phase

Phase 4

## Phases

### Phase 1: Context, rules and branch check

- [x] Active branch is `main` (user's branch); `origin/Matteo` untouched at 27cd3c1
- [x] Read prior research package, teammate review, organiser questions, from-zero lab
- [x] Download official docs sources (scratchpad) and record binding constraints
- [x] Install planning-with-files 3.25.2 from OthmanAdi/planning-with-files (plugin, user scope)
- **Status:** complete

### Phase 2: Critical audit and method decision

- [x] Eight-dimension audit with adversarial verification (workflow wf_aaa6465f-69d): 43 upheld, 11 refuted
- [x] Decide generation / allocation / validation procedure and justify against alternatives (`research/careerlab/method-decision.md`)
- [x] Pre-register statistical protocol before any policy results are analysed (`lab/protocol/prereg-v1.*`, hashes in registry)
- **Status:** complete

### Phase 3: Reproducible install and official MCP client

- [x] uv project with pinned engine/dataset versions and configurable paths
- [x] Persistent-connection MCP client (stdio only for the real game), observe-before-retry
- [x] Isolation, concurrency, retention-limit and throughput checks through the official interface only
- **Status:** complete

### Phase 4: Planner, store, statistics and actors

- [x] Immutable policy store (hash, parents, hypothesis, change), registry, job leases, resume
- [ ] Scripted actors [x], Claude CLI worker actor [x], synthetic testbed (build workflow wf_dfeb9d9a-a0f)
- [ ] Statistics module implementing the pre-registered rules (build workflow)
- **Status:** in_progress

### Phase 5: Pilot, fixes and scale-up by evidence

- [ ] Dev-scale pilot on the real game within the authorisation gate
- [ ] Synthetic-testbed validation of method vs baselines and ablations
- [ ] Fix problems found; record what failed
- **Status:** pending

### Phase 6: Commit and report

- [ ] Commit to `main` without secrets or simulator internals
- [ ] Report results, decisions, uncertainties and the next most useful experiment
- **Status:** pending

## Key Questions

1. Do organisers allow (a) automated dev batches at scale, (b) Claude models as development actors, (c) many concurrent sessions? Not answered in docs; query drafted in `research/organiser-questions.md`. Until answered, the authorisation gate in `lab/config` limits real-game use.
2. Does the team have the competition key? Required for any target-actor (deepseek-v4-flash, JiuwenSwarm) evidence. Preliminary submission is the prerequisite.
3. Are separate `career-emulator-engine-mcp` processes isolated or sharing storage? Must be tested through the five tools only.

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Work on `main` | It is the user's branch; teammate work lives on `origin/Matteo` and is read-only. |
| Root planning files are the global plan; workers write elsewhere | User requirement; single integrator avoids conflicting writes. |
| Claude workers run as isolated `claude -p` processes driven by the programmatic planner | Frozen, logged actor config and token accounting per episode; native subagents stay for building/analysis. |
| Real-game Claude actors and large batches gated on written organiser clarification | Rules: silence is not permission; user instruction to check clarifications first. |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| `claude plugin marketplace add` refused (source already declared in user settings) | 1 | Marketplace already known from `extraKnownMarketplaces` pointing at the original repo; install succeeded. |
| Old root `task_plan.md` failed native plan validation | 1 | Archived with `git mv`; new plan uses native phase/status markers. |
