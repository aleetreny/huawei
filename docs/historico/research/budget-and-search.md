# Credits, brute force and useful search

All numerical examples below are derived illustrations, not observed performance or provider price quotes. Official credit and model restrictions are in [Competition API key](https://techarena-career-sim.readthedocs.io/en/latest/api-key.html); scoring is in [Competition rules](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html).

## 1. Four budgets, not one

| Resource | What consumes it | How to measure it |
|---|---|---|
| LLM credit | Input/output, reasoning and cached tokens according to the actual designated route | Provider-reported billed usage; confirm which token fields count. |
| Game calls | MCP observations, actions and logs | Per-tool counts, latency, errors. No quota established here. |
| Local compute | Candidate analysis, permitted own-output processing | Wall time, CPU/memory and any infrastructure charge. |
| Human time | Debugging, reviewing evidence, video and submission preparation | Remaining work before the three cutoffs. |

MCP transport is not itself an LLM inference. A million MCP calls need not mean a million model calls, but automating the game outside the representative single-agent path or at unusual scale still needs organiser clarification. Conversely, one tool call can cause large model costs when a growing conversation is repeatedly sent to the model.

The issued key has at most USD 50 and only works during 26 October–1 November 2026 for the designated competition model and competition purposes. No price table is specified in the reviewed rules. Use the exact model name provided by email; do not guess a substitute or select a provider. There is no verified cost per game yet.

## 2. Budget allocation proposal

| Phase | Cap, USD | Purpose |
|---|---:|---|
| Integration pilot | 5 | Verify one complete path and estimate cost. |
| Exploration | 15 | Compare a small number of distinct general policies. |
| Confirmation | 15 | Replicate the strongest candidates. |
| Final validation | 10 | Fresh complete games after freezing the candidate. |
| Reserve | 5 | Failed infrastructure, final check or unexpected token growth. |
| Total | 50 | Reallocate after measuring the pilot. |

These caps are a starting proposal. If one game costs more than the pilot cap, stop and reassess before launching a batch. Track cost after each run and estimate remaining full games. Do not assume unused or wasted credit will be restored.

Illustrative capacity after reserving USD 5:

| Measured complete-game cost | Approximate games within USD 45 |
|---|---:|
| USD 0.25 | 180 |
| USD 0.50 | 90 |
| USD 1.00 | 45 |
| USD 2.00 | 22 |
| USD 5.00 | 9 |
| USD 10.00 | 4 |

Round down; additional design calls, failed runs, uncaptured usage and changing context sizes reduce capacity. These are scenarios, not claims about DeepSeek pricing or the actual competition route.

Where the organiser provides applicable prices, estimate:

`cost = uncached_input_tokens × input_price / 1e6 + cached_input_tokens × cache_price / 1e6 + billed_output_tokens × output_price / 1e6`.

Do not subtract cached tokens twice if a reported input field already excludes them. Reasoning tokens may already be part of billed output. Prefer measured provider billing over an incomplete estimate.

## 3. The unusual token-efficiency plateau

The published rule uses `t = total_tokens / survival_months`:

- `t ≤ 500,000`: efficiency score 100.
- `t ≥ 3,000,000`: score 0.
- Otherwise: `100 × (3,000,000 − t) / 2,500,000`.
- Early exits are capped at 50; missing token or survival counts score zero.

For a 48-month completion, the full-mark boundary is **24 million total tokens** and the zero boundary is **144 million total tokens**. At one million tokens per month the score is 80, so Stage 1 loses two points versus the maximum efficiency component. This is arithmetic from the published rubric, not a claim that such usage is affordable.

Below the plateau, fewer tokens do not earn extra efficiency points. They can still improve development economics and reduce context noise. Do not remove important observation or risk checks for a nonexistent bonus below the plateau. Clarify accounting of caching/reasoning if reported usage is ambiguous.

## 4. How many trajectories exist?

Toy illustration: if 144 story decisions each had exactly three choices, there would be `3^144 ≈ 5.08 × 10^68` story-choice strings. The default handbook says up to three events per month; it does not guarantee 144 decisions or three choices per event. The illustration shows the exponential structure, not the actual reachable tree size.

Even choosing only among eight main actions plus none for sixteen quarters gives `9^16 = 1,853,020,188,851,841` abstract sequences before adding story or Energy decisions. Not all such paths need be reachable or sensible. A million trials cannot exhaust this space.

An optimal fixed sequence would also be the wrong abstraction for changing events and states. We want a policy that reacts to observations. Policy search can be much smaller than enumerating trajectories if its representation captures useful general priorities.

## 5. Why the quarterly space is manageable

Public action costs are four one-Energy categories and three two-Energy categories. With budget three, an illustrative enumeration **allowing repeats** has:

| Ordered Energy sequence type | Count |
|---|---:|
| Empty | 1 |
| One action | 4 + 3 = 7 |
| Two one-cost actions | 4² = 16 |
| One one-cost plus one two-cost, either order | 2 × 4 × 3 = 24 |
| Three one-cost actions | 4³ = 64 |
| Total | 112 |

Multiplying by nine main-action categories yields 1,008 abstract packages for a quarter. If order is ignored, stars-and-bars gives 35 all-one-cost multisets with total cost at most three, plus `3 × (1+4) = 15` multisets containing a two-cost action: 50 Energy multisets or 450 packages with main actions.

**These counts do not establish that repeats, every category or every order is available in a real state.** Runtime choices govern legality. Order can matter because observations change between actions; do not collapse ordered actions when their consequences differ. This is a public-cost counting exercise, not a recovered game formula.

Even this tiny space does not have a known exact numerical evaluator. Start by comparing a short list of plausible packages using public directional effects and current-run needs. Exhaustive arithmetic over made-up effect sizes would merely optimise the wrong model.

## 6. What a million calls would mean

One million calls over seven full days requires an average of approximately **1.65 calls per second**, continuously. This is arithmetic, not a recommended rate or authorised load. It ignores latency, serial dependencies, failures, server limits and any organiser restrictions. At one call per second it takes 11.57 days; at ten it takes 27.78 hours.

For scale only: up to 144 default story decisions, up to 48 one-point Energy actions and 16 main selections give about 208 action selections in a full run. One observation and one action per selection, plus new game and handbook, gives about **418 MCP calls** before extra logs, retries or other variation. One million such calls correspond to roughly **2,392 hypothetical full runs**, not one million independent full games. This is an approximate default accounting model, not a documented bound on all possible runs.

If each full run cost USD 0.50 in model usage, 2,392 would cost about USD 1,196; at USD 2 it would cost USD 4,784. Actual cost is unknown. Increasing local call rate cannot make unaffordable model usage fit the USD 50 key.

Bulk `observe` calls on the same state do not create transitions; `take_action` changes the actual game. A valid experimental question matters more than call count. Any high-volume proposal must specify purpose, interface, model path, rate, concurrency, stop conditions and whether learned information reaches the submission, then obtain organiser clarification.

## 7. Where local brute force is useful

| Search idea | Expected value now | Reason |
|---|---|---|
| Generate a handful of distinct policy/Skill revisions | High | Cheap to propose, relatively easy to inspect and test. |
| Compare public quarterly plans before acting | High | Small budget and meaningful complementarities. |
| Reanalyse already generated own outputs | High | Can find procedural mistakes without new game/model expense. |
| Give promising candidates progressively more full games | High | Spend evaluation budget where evidence is most useful. |
| Generate thousands of near-identical prompts | Low | Expensive to evaluate and prone to selection overfit. |
| Online MCTS through repeated live actions | Low / unsupported mechanism | No documented arbitrary state cloning or rollback. |
| Fit hidden formulas and transfer coefficients into Skills | Unresolved / do not use without clarification | Hard-coding prohibition and generalisation risk. |
| Train a new RL policy from millions of transitions | Low this week; permission unresolved | Sample, platform, credit and deployment constraints. |
| Rent GPUs before identifying a permitted CPU bottleneck | Low | No useful GPU computation has yet been established. |

## 8. Spending discipline

After each batch, answer: which uncertainty was reduced; what general behaviour improved; whether the effect was repeated; and what the next batch can distinguish. Prefer one informative full-game comparison to thousands of redundant observations. Wall-clock time is not a score component, but development deadlines and cost still matter. No credit was spent during this research.
