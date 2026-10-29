# Skills design — Gradient Depression

Submission: **cp-v5a**, Cut 2, 30 October 2026. JiuwenSwarm 0.2.4b3, single-agent `agent` mode. The bundle contains one `career-rules` Skill and a manifest instruction, without scripts or reference files. This document describes the existing candidate, not a proposed revision.

## Task and design

The agent manages a 48-month career through monthly stories, quarterly actions and six-monthly reviews. It reads the current choices for likely consequences, then applies priorities separately for stories and quarterly phases. A single Skill keeps those priorities together; the manifest repeats scope, risk precautions, review protection and the response protocol. The Skill is reread when it is no longer in view.

## Turn loop and efficiency

During ordinary story decisions, the agent requests `take_action` and then `observe` in one assistant response, using a literal `tool_calls` array example. In our local official-runner tests the calls execute in order, so the observation reads the resulting state. Each action still passes through the official MCP interface and normal validation and logging. “Decide silently” asks the model to omit redundant narrative while retaining a concise action note and tool results. The intended saving comes from fewer model round trips and less repeated text, not altered token accounting, scores or evaluation artifacts. This is not an instruction to override higher-priority requirements or conceal errors.

The current quarterly instruction goes further: after observing the quarterly menu it requests all Energy actions, the main action and a final observation in one response. It assumes option numbers remain stable across quarters. This is an implementation assumption, not a guarantee in the public interface documentation; it is a known portability and review concern. Actual execution does not always follow the requested batching. A failed call triggers another observation and a valid choice.

At startup the agent observes, reads events and recovers its latest note through `check_latest_logs` when needed. The Skill currently tells it not to call the handbook because the guidance is included in the Skill.

## Memory

Each note contains `Review in N | Now S.. N.. O.. | Best S.. N.. O.. | Reviews here: 0`, followed by at most one short reason. Now records observed Skill, Network and Output. Best records their maxima at the current level and resets after promotion. Reviews here counts reviews without promotion and resets after promotion. Missing memory is rebuilt with Best equal to Now and the review count zero.

The review switch uses `6 - (current_month mod 6)`. The candidate treats N=1 as the last month before a review and N=2 as preparation time. The published six-month interval supports anticipation, but the exact within-month boundary is an assumption of this candidate rather than an additional published rule.

## Story decisions

The reading guide asks for likely directions of Skill, Network, Output, Health, Dignity, Wealth and hidden risk. These are working interpretations of option text; observed feedback takes precedence.

The ordered steps are survival, risk, wellbeing, review protection and growth. A step is skipped if it would remove every option. When all options appear risky, the candidate uses a qualitative hierarchy of risk and reversibility. With friendly or quiet HR feedback and N=1, protecting growth statistics takes precedence over avoiding mild risk, except during its stalled-start mode. Severe concealment and gambling remain excluded. Wellbeing otherwise precedes review protection. Growth counts predicted improvements, weights a statistic explicitly identified as lagging twice, and subtracts predicted losses. End-of-career preferences favour wellbeing and risk control.

## Quarterly priorities

The first applicable line determines the plan:

1. Final quarter: reduce risk and recover wellbeing, then maintain relationships; report results when HR is friendly, otherwise lay low.
2. Near a limit: recover first. The candidate uses Health or Dignity at 4 or below, or falling for three months, as its own precautionary margin, not a published failure threshold; negative Wealth or zero Network also trigger recovery.
3. HR feedback: quiet calls for Defuse; more concerning feedback adds Lay low. Its stalled-start mode treats quiet feedback more conservatively.
4. A review explicitly identifies a lagging statistic: invest in that statistic.
5. From L4: prioritise Skill learning and rotation, with remaining Energy for Network or Output, subject to preceding recovery and risk rules.
6. Earlier levels: develop Skill, Network and Output, prioritising lost ground, and apply for a key project.

The L4 preference is a strategy choice, not a published promotion threshold. Its wellbeing-first ordering can leave insufficient Energy for risk reduction.

## Handbook provenance and limits

The in-game employee handbook returned by `show_employee_handbook`, under “Risk and failure → Ways people say a run ends”, describes dismissal after two weak half-year reviews and a trust crisis after a second blow-up. Our archived tool-output copy is `lab/data/transmision/handbook.md`, lines 141–147. These statements are available through the permitted interface; they are not deductions from package internals.

They do not establish that two reviews without promotion equal two weak reviews, or that the next review is necessarily a final chance. The candidate's stalled-start intervention makes that additional inference and should not be attributed to the handbook. Likewise, fixed future menu numbers and the relative risk hierarchy are not published guarantees. These limitations are disclosed rather than certified as official mechanics.

Compared with Cut 1, cp-v5a combines shorter notes and grouped calls with a stalled-start response, an all-options-risky rule and an explicit Skill priority at senior levels. It removes the earlier Stalled and Concerns memory fields. No event identifiers, event-title answer table, executable policy or simulator is shipped. The decision report separates measured results from assumptions and untested changes.
