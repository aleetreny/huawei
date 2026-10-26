# Sustainable Career — candidate v0.1

This is an initial English-language Skill bundle for the TechArena Career Survival simulator. It is a design hypothesis, not an experimentally established best strategy.

The bundle contains three Skills for one agent:

- `career-risk-review`: identify the current sustainability concern from visible state and feedback.
- `career-event-decisions`: compare the offered story choices in context and update after consequences.
- `career-quarterly-planning`: allocate quarterly resources and select a main action according to current needs.

Read the risk Skill first, then the Skill relevant to the current phase. Responsibilities are sequential reasoning steps within a single agent, not separate agents or JiuwenSwarm team mode.

## Readiness

The Skills and design documents can be reviewed and manually exercised before the competition key arrives. A manifest with the team's confirmed registered identity is still needed for the official runner. No team identity has been invented here. The final submission also needs the team's real English `presentation.mp4`; no empty video is supplied.

Manual tests with Codex interpreting these Skills are useful for finding unclear instructions. They are not official-model benchmarks and do not consume competition model API credits; they do use the current Codex session. Genuine end-to-end Skill testing requires JiuwenSwarm 0.2.4b3 in `agent` mode and the designated competition model. Do not compare Codex-assisted results as though only the Skills changed from a random or official-model baseline.

See [the design](design/skills_design.md), [the decision report](design/decision_report.md) and [the evaluation plan](../docs/skill-evaluation-plan.md).
