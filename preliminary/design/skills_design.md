# Preliminary Skills Design — Adaptive Career Planning Agent

## Objective and understanding of the simulation
We propose a single JiuwenSwarm agent (version `0.2.4b3`, mode `agent`) for the 48-month Career Survival Agent simulation. The agent acts as a newly hired engineer who must balance career progression, sustainable health and dignity, professional capability, relationships, output, wealth, and organisational risk. A run contains story decisions, three Energy points at quarterly action phases, one quarterly main action, and six-month performance reviews. Some effects and failure conditions are not publicly quantified, so the solution must respond to feedback without claiming knowledge of hidden rules.

## Architecture
There is one decision-making agent, not a team of agents. It uses the official MCP tools (`new_game`, `observe`, `take_action`, `check_latest_logs`, and `show_employee_handbook`) and two complementary Skills:

1. **career-planning:** structures event and quarterly decisions around progress across the full 48 months; takes into account upcoming reviews, development needs, public action effects, and observed longer-term trends.
2. **risk-management:** audits each contemplated decision for persistent or severe risks, such as deteriorating health, dignity, financial position, network, weak performance, or warnings in the logs; recommends a safer option or recovery action if needed.

The Skills are instructions used by the same agent, not separate cooperating JiuwenSwarm agents. At each choice, the agent produces a career-oriented recommendation, applies the risk audit, and selects one currently available action that balances expected benefits and downsides.

## Information the agent will use
- Official observed state and action choices, including visible Health, Dignity, Skill, Network, Output, Wealth, Level, Energy, and current time where returned.
- The public handbook and published rules on quarterly actions, six-month reviews, levels, and common failure directions.
- Legitimate within-run history and warning messages returned by the official interface.
- Qualitative trends across months and quarters; no guesses presented as hidden numerical thresholds.

## Decision process
1. Read the latest observation and identify whether this is a story event or a quarterly decision phase.
2. Review current statistics and any important recent warning or trend.
3. Compare only the actions currently offered, weighing near-term opportunity against long-term progression and sustainability.
4. Apply the risk-management Skill. If the preferred action may compound an existing severe risk, reconsider with more conservative priorities.
5. Choose an available action using the official MCP tool and record a concise rationale. Inspect subsequent feedback before making the next decision.
6. After a review or meaningful change in trend, adapt priorities rather than rigidly repeating a scripted response.

## Principal risks and mitigations
- **Premature termination:** protect deteriorating health and dignity and react to repeated weak performance, adverse finances, isolation, or risk warnings.
- **Myopic optimisation:** assess decisions with respect to 48 months, not only their immediate gains.
- **Overfitting development events:** avoid named-event answer tables and presumed secret mechanics; use general principles that apply to unseen scenarios.
- **Hallucinated actions and tool misuse:** use only the actions and interfaces returned by the official MCP server; inspect the state before acting.
- **Token inefficiency:** use concise context and decisions, calling logs as needed rather than repeatedly re-reading unchanging material.

## Development plan
First, verify the agent can complete end-to-end games. Next, review permitted run logs and quantitative results; compare broadly different public-rule-based priorities across repeated development runs. Revise the Skills in response to genuine failure patterns. Validate the final submission using the official tool and run it with the designated competition model. We will not inspect protected game internals or encode responses to named development events.

This is an initial good-faith design for API-key verification, not a claim of an implemented or tested final agent.
