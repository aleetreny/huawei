# Precedents and reading guide

Checked on 26 October 2026. Primary sources are preferred. A claimed placing from a participant README is labelled as such. Similarity does not transfer permissions: many open-simulator contests permit practices forbidden in this UK track.

## 1. Historical Huawei landscape

| Competition / source | What is verified here | Transfer to our task | Important limitation |
|---|---|---|---|
| [UK 2023 official page](https://www.agorize.com/en/challenges/2023-tech-arena-uk?lang=en) | CPU branch/data/value prediction theme. | Understand objective and constraints before choosing algorithms. | A different systems problem, not this simulation. |
| [UK 2024 official page](https://huawei.agorize.com/en/challenges/uk-tech-arena-2024/pages/winning-teams?lang=en) | Architecture/fundamental software event. | Huawei's competition label covers different tasks. | Available text did not establish a detailed winner solution. |
| [UK 2024 public participant mirror](https://github.com/jason-blips/2024-uk-tech-arena) | Templates and guidebook repository found in search. | Historical problem materials if further study is needed. | A discovery lead, not verified winning code. Do not confuse with Ireland. |
| [Ireland 2024: Linan's team](https://github.com/linanwx/huawei2024) | Authors report algorithmic first, overall third; simulated annealing for deployment/pricing. | Local search over diverse candidate changes; presentation can change final ranking. | Public objective and input data differ fundamentally from hidden game dynamics. Ranking claim is the authors' account. |
| [Ireland 2024: acheong08](https://github.com/acheong08/hwta-ireland-2024) | Repository describes second place and CP-SAT plus pattern search. | Combine explicit constraints with optimisation where rules are known. | Does not supply a mathematical model of this career game. |
| [Ireland 2024 author retrospective](https://nansenli.com/post/2024/10/huawei2024/) | Related first-person retrospective surfaced. | Further reading alongside the team repository. | Search-level discovery; do not count as an independent full-text validation of the ranking. |
| [UK 2025 event](https://techarena-uk-2025.algotester.com/) | Cangjie challenge, systems focus, qualification and expert presentation. | Prepare a technical explanation, not just an algorithm. | Different objective and rules. |
| [Algotester UK 2025 results](https://techarena.algotester.com/en) | Official table shows Rookie Returns first, 1337 second and Rhapsody third. | Provisional versus final tables can change; validate beyond visible leaderboard cases. | Scores are specific to that task; no comparable career score or winning algorithm is established. |
| [Ireland 2025 winner's account](https://darasi.me/blog/2025/huawei-tech-arena/) and [CRT-AI institutional account](https://www.crt-ai.ie/huawei-ireland-tech-arena-2025/) | Dynamo A first in an LLM efficiency challenge; balancing answer quality, latency and cost. | Treat cost as a measured engineering variable. | Single-round QA differs from long-horizon decision-making. |
| [CareerSim-BDCI26 official-family repository](https://github.com/openJiuwen-ai/CareerSim-BDCI26) | Same-family 48-month career task with MCP and Skills. | Closest conceptual comparison; public interface vocabulary and long-horizon framing. | Same year, not a verified completed prior UK edition. Its mode examples and package names can conflict with current UK rules. No champion solution established here. |
| [Current UK participation repository](https://github.com/RAI-Internal/techarena-career-sim) | Public, accessible official runner identified. | Use its pinned setup and validation. | The runner is public; engine and dataset internals are not permitted reading material. |

There is no substantiated historical winning formula for the exact UK 2026 game in this investigation. The contest starts on the research date. Sources advertising a generic TechArena winner may refer to a different country, year or task.

## 2. Comparable optimisation and agent competitions

### AHC058: evaluator-guided diversity

[Sakana AI's account](https://sakana.ai/ahc058/) reports an ALE-Agent first place, with a diverse greedy constructor, simulated annealing and larger structural changes that helped escape local optima. It reports thousands of LLM calls and about USD 1,300 including infrastructure. The underlying contest was held in December 2025; the account was published in January 2026.

Transfer: preserve different strategic families and test substantive changes, not endless wording variants. Distinguish a cheap candidate-generation loop from the expensive evaluation loop.

Limit: the algorithm could simulate known mechanics locally. Our official MCP does not expose equivalent branching. Its use of multiple models is not permission for multiple evaluated JiuwenSwarm agents or use of another model with the competition key.

### AtCoder world final: the human winner's process

[Psyho's original approach](https://github.com/FakePsyho/cpcontests/blob/master/atcoder/awtf2025/approach.md) describes an optimisation contest with public generators, scoring tools, 50 provisional tests and 2,000 final tests. It is valuable for iterative problem solving and the distinction between provisional and final validation.

Transfer: make an early working solution, use local evidence, reserve enough focus and time to test. Limit: those contest rules and public simulation access do not apply here.

### Santa 2025: why exhaustive compute worked there

The [first-place author's writeup](https://www.kaggle.com/competitions/santa-2025/writeups/1st-place-genetic-algorithm-and-gpu-relaxation) describes a genetic algorithm, GPU relaxation, symmetry and population diversity for tree packing. The author reports substantial GPU time.

Transfer: reduce the degrees of freedom, keep a diverse pool and optimise a real evaluator. Limit: deterministic geometric validation and symmetry are available there; no analogous exact evaluator or symmetry is established in the career game. Renting GPUs is premature until we know the computation that would use them.

### Lux AI: heuristic and RL approaches

The [NeurIPS-edition first-place author repository](https://github.com/ryandy/Lux-S2-neurips-public) is a concrete high-performing game agent. The [Deimos tenth-place account](https://www.kaggle.com/competitions/lux-ai-season-2/writeups/deimos-10th-place-deimos-s-rl-approach) explains action-space simplification, staged rewards and debugging difficulties in an RL stack.

Transfer: constrain actions to what is legal, simplify the decision space and inspect why a policy fails. Limit: large-scale training, self-play, simulator rewrites and state initialisation belong to that open environment. They are not authorised in TechArena simply because Lux contestants used them. Also distinguish the original Lux S2 competition from its later NeurIPS edition.

### Selenia City: useful process, incompatible shortcuts

[Tom Delame's first-person account](https://virtual-atom.com/codingame/fall24/) starts from a simple complete greedy solution and improves it while building evaluation tooling. The author also discusses referee modifications and recognising specific levels.

Transfer only the baseline-first approach and focus on high-return development work. **Do not transfer referee inspection/modification or level-specific solutions**: the current UK rules prohibit corresponding engine access and fixed event answers. A tutorial can be valuable and still contain techniques that are disallowed here.

## 3. Research and manuals ranked by practical value

| Priority | Source | Read for | Application this week |
|---|---|---|---|
| 1 | [Current UK rules](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html) | Scoring, permitted interfaces, hidden-knowledge prohibition. | Requirements for every candidate. |
| 1 | [Quickstart](https://techarena-career-sim.readthedocs.io/en/latest/quickstart.html), [MCP](https://techarena-career-sim.readthedocs.io/en/latest/mcp.html), [submission](https://techarena-career-sim.readthedocs.io/en/latest/submission.html) | Reproducible runtime and valid deliverable. | One complete baseline before tuning. |
| 1 | [Public handbook](https://techarena-career-sim.readthedocs.io/en/latest/handbook.html), [rules](https://techarena-career-sim.readthedocs.io/en/latest/rules.html), [endings](https://techarena-career-sim.readthedocs.io/en/latest/failure-and-ending.html) | Public decision variables and cadence. | General strategy and quarter planning. |
| 2 | [GEPA original paper](https://arxiv.org/abs/2507.19457) | Diagnose traces, propose and test instruction changes. | A lightweight development cycle; no need to embed DSPy. |
| 2 | [Statistical precipice paper](https://arxiv.org/abs/2108.13264) and [rliable](https://github.com/google-research/rliable) | Uncertainty and score distributions. | Prevent overclaiming from one successful run. |
| 2 | [Hyperband](https://jmlr.org/papers/v18/16-558.html) | Resource allocation among candidates. | Progressively give more complete games to promising variants. |
| 2 | [Linan's Huawei solution](https://github.com/linanwx/huawei2024) | Algorithm/presentation trade-off. | Record evidence while developing, prepare video early. |
| 3 | [Project Vend phase two](https://www.anthropic.com/research/project-vend-2) | Long-run tool use, instructions and remaining social vulnerability. | Protect objective and memory from persuasive event text. |
| 3 | [Vending-Bench 2](https://andonlabs.com/evals/vending-bench-2) | Long-horizon coherence and resource management. | Monitor persistence and deterioration, not isolated decision eloquence. |
| 3 | [BalatroBench methodology](https://balatrobench.com/about.html) | Tool validity, game progress and cost as separate metrics. | Track invalid actions as well as score. |
| 3 | [ALE-Bench](https://arxiv.org/html/2506.09050) | Iterative score-based algorithm engineering. | Candidate diversity with real feedback. |
| 3 | [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) | Evaluator-guided program evolution. | Understand why a trustworthy evaluator matters more than proposal count. |
| 4 | [Reflexion](https://arxiv.org/abs/2303.11366) and [Voyager](https://arxiv.org/html/2305.16291v2) | Reflection and reusable skills. | Test a compact current-run memory; do not import remembered hidden answers. |
| 4 | [POMCP](https://proceedings.neurips.cc/paper/2010/hash/edfbe1afcf9246bb0d40eb4d8027d90f-Abstract.html) | Planning requirements under partial information. | Recognise why live MCP access alone is insufficient for search rollouts. |
| 5 | [PySR](https://arxiv.org/html/2305.01582v3) | Symbolic model discovery and empirical fits. | Background for a method requiring organiser clarification, not a submission recipe. |
| 5 | [AtCoder testing-tool author's guide](https://blog.terry-u16.net/entry/how-to-use-pahcer) | Avoid evaluating only one seed and compare score changes. | Methodological reading; current MCP has no documented seed input. This source was screened at search level. |

## 4. Sources deliberately not used as strategy

- An indexed CareerSim issue discussing installed-package observations: excluded because public availability does not legitimise internal knowledge.
- DeepWiki explanations of the simulator: excluded as a basis for game mechanics or hidden conditions.
- Generic second-hand articles that repeat primary winning reports: no extra evidentiary weight.
- Unverified models, benchmark leaderboards and numerical claims unrelated to the designated competition setup: not evidence for which agent wins here.
- A guessed `Deimos-BC/Deimos` source failed to yield a usable page; the actual author account and `RoboEden/lux2-deimos` discovery were used instead.

## 5. Coverage gaps

No private Discord clarifications, current participant strategies, hidden test distribution, official 2026 score releases or private winner materials were available in this research. We did not inspect engine packages, data files or databases, and did not run a competition game. The evidence supports a development strategy, not a performance prediction or a complete historical census.
