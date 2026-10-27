# Bibliografía anotada y procedencia

Corte y consulta: **26 de octubre de 2026**. Son 55 fuentes seleccionadas: artículos, preprints, relatos de autores y documentación oficial. No son 55 lecturas completas. Cada entrada indica su alcance; la selección más profunda incluye métodos y discusiones de MCTS-AHD, AB-MCTS, ShinkaEvolve, AdaEvolve, AIDE, DGM y TreeFlex. Los resultados publicados se atribuyen a sus autores y no se han reproducido en CareerSim.

El [catálogo JSON](references.json) conserva autores, versiones comprobadas y consultas de metadatos. El [registro de búsqueda](search-audit.json) contiene candidatos de descubrimiento, incluidos resultados no seleccionados. Los preprints recientes aportan ideas y no se equiparan a resultados establecidos o garantías generales.

La referencia R55 se incluye para documentar el uso material de **paper-lookup** y su artículo de procedencia; no es evidencia de rendimiento de una política ni un resultado de CareerSim.

## Árboles y evolución de sistemas

### R01 — MCTS-AHD

[Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design](https://proceedings.mlr.press/v267/zheng25o.html). Zhi Zheng, Zhuoliang Xie, Zhenkun Wang et al.; 2025. ICML 2025.
Alcance comprobado: `methods_and_ablations`.

**Utilidad:** Outer tree of generated heuristics, progressive widening and retention of weak ancestors.
**Límite:** Its max backup and benchmark evaluation are not a calibrated estimator for noisy game episodes.

### R02 — AB-MCTS

[Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search](https://arxiv.org/abs/2503.04412). Yuichi Inoue, Kou Misaki, Yuki Imajuku et al.; 2025. NeurIPS 2025.
Alcance comprobado: `methods_read`.

**Utilidad:** Explicit generation action decides whether to branch wider or refine deeper.
**Límite:** Bayesian node model is an assumption; a GEN node is not an ordinary fixed arm.

### R03 — ShinkaEvolve

[ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution](https://arxiv.org/abs/2509.19349). Robert Tjarko Lange, Yuki Imajuku, Edoardo Cetin; 2025. ICLR 2026.
Alcance comprobado: `methods_and_ablations`.

**Utilidad:** Archive, island populations, novelty screening and adaptive mutation-model selection.
**Límite:** Mutation-model selection is distinct from fidelity of a model playing the game.

### R04 — AdaEvolve

[AdaEvolve: Adaptive LLM Driven Zeroth-Order Optimization](https://arxiv.org/abs/2602.20133). Mert Cemri, Shubham Agrawal, Akshat Gupta et al.; 2026. arXiv preprint.
Alcance comprobado: `methods_and_experiments`.

**Utilidad:** Local exploration intensity, global allocation across islands and meta-guidance.
**Límite:** Reported gains on algorithm tasks do not establish robustness on this game's noisy objective.

### R05 — GEPA

[GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457). Lakshya A Agrawal, Shangyin Tan, Dilara Soylu et al.; 2026. ICLR 2026.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Use execution traces to propose targeted instruction revisions and maintain a candidate frontier.
**Límite:** No transfer of its percentage gains or rollout savings is assumed for CareerSim.

### R06 — ReEvo

[ReEvo: Large Language Models as Hyper-Heuristics with Reflective Evolution](https://arxiv.org/abs/2402.01145). Haoran Ye, Jiarui Wang, Zhiguang Cao et al.; 2024. NeurIPS 2024.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Reflective evolution provides language feedback for heuristic improvement.
**Límite:** Verbal gradients are feedback heuristics, not derivatives of the true game score.

### R07 — FunSearch

[Mathematical discoveries from program search with large language models](https://www.nature.com/articles/s41586-023-06924-6). Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov et al.; 2024. Nature 625 (2024); first online 14 December 2023.
Alcance comprobado: `primary_abstract_intro`.

**Utilidad:** A trusted evaluator can filter LLM-generated candidates; islands retain diversity.
**Límite:** Needs a valid evaluator; the original maths/code setting differs from an agent game.

### R08 — AlphaEvolve

[AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131). Alexander Novikov, Ngân Vũ, Marvin Eisenberger et al.; 2025. arXiv preprint.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Evaluator-guided evolution separates proposal generation from objective assessment.
**Límite:** A cheap model generating code is not evidence that a cheap actor preserves policy rankings.

### R09 — Darwin Godel Machine

[Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954). Jenny Zhang, Shengran Hu, Cong Lu et al.; 2026. ICLR 2026 listing.
Alcance comprobado: `selected_methods`.

**Utilidad:** Archive of agent designs supports open-ended descendants rather than one greedy lineage.
**Límite:** Self-modification and code/tool changes cannot simply be imported into the competition submission.

### R10 — Automated Design of Agentic Systems

[Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435). Shengran Hu, Cong Lu, Jeff Clune; 2025. arXiv preprint.
Alcance comprobado: `abstract_intro`.

**Utilidad:** Meta-agent search over an archive of agent designs.
**Límite:** Broad agent architecture search exceeds the track's fixed runtime permissions.

### R11 — AIDE

[AIDE: AI-Driven Exploration in the Space of Code](https://arxiv.org/abs/2502.13138). Zhengyao Jiang, Dominik Schmidt, Dhruv Srikanth et al.; 2025. arXiv preprint.
Alcance comprobado: `selected_methods`.

**Utilidad:** Separate drafting, debugging and atomic improvements; preserve concise search summaries.
**Límite:** Its simple best-node improvement rule is a baseline, not proof that greedy search is sufficient.

### R12 — EvoTest

[EvoTest: Evolutionary Test-Time Learning for Self-Improving Agentic Systems](https://arxiv.org/abs/2510.13220). Yufei He, Juncheng Liu, Yue Liu et al.; 2026. ICLR 2026.
Alcance comprobado: `primary_abstract_and_metadata`.

**Utilidad:** Actor/evolver loop revises agent configuration between game episodes.
**Límite:** Its cross-episode state-action memory may conflict with this track's fixed-answer prohibition.

### R13 — Meta-TTL

[Meta-TTL: Meta-Learning Self-Improvement Policies for Language Agents](https://arxiv.org/abs/2604.00830). Zhanzhi Lou, Hui Chen, Yibo Li et al.; 2026. arXiv preprint.
Alcance comprobado: `latest_metadata_and_abstract`.

**Utilidad:** Optimise the rule for improving a policy, not only the policy itself.
**Límite:** Current API title differs from an older indexed version; requires broader tasks/meta-training.

### R14 — PACEvolve++

[PACEvolve++: Improving Test-time Learning for Evolutionary Search Agents](https://arxiv.org/abs/2605.07039). Minghao Yan, Bo Peng, Benjamin Coleman et al.; 2026. arXiv preprint.
Alcance comprobado: `latest_metadata_and_abstract`.

**Utilidad:** Adapts evolutionary-search guidance by training an advisor as search progresses.
**Límite:** Training an advisor and using a separate implementation model is not the fixed official setup.

### R15 — TreeFlex

[TreeFlex: Agents Navigating Their Own Search Trees](https://arxiv.org/abs/2610.20334). Dongzhuo Li, Fangzhou Cheng, Weiwei Li et al.; 2026. arXiv preprint.
Alcance comprobado: `selected_methods`.

**Utilidad:** Branch cards and path-specific context support deliberate revisit and clean execution context.
**Límite:** 14 October preprint; trained navigation and restored task state do not imply game-state rollback.

### R16 — TreeSeeker

[TreeSeeker: Tree-Structured Trial, Error, and Return in Deep Search](https://arxiv.org/abs/2606.11662). Zhuofan Shi, Mingzhe Ma, Lu Wang et al.; 2026. arXiv preprint.
Alcance comprobado: `abstract_intro`.

**Utilidad:** Branch-attached evidence, uncertainty and failure cues support return decisions.
**Límite:** Deep-search benchmark and textual UCB are not calibrated career-policy confidence bounds.

### R17 — Empirical-MCTS

[Empirical-MCTS: Continuous Agent Evolution via Dual-Experience Monte Carlo Tree Search](https://arxiv.org/abs/2602.04248). Hao Lu, Haoyuan Huang, Yulin Zhou et al.; 2026. arXiv preprint.
Alcance comprobado: `abstract_intro`.

**Utilidad:** Couples local search with cross-problem memory management.
**Límite:** Reasoning benchmarks and retained experience differ from permitted current-run game information.

### R18 — SPARK

[SPARK: Strategic Policy-Aware Exploration via Dynamic Branching for Long-Horizon Agentic Learning](https://aclanthology.org/2026.acl-long.1100/). Jinyang Wu, Shuo Yang, Yuhao Shen et al.; 2026. ACL 2026.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Concentrates branching at informative decision states during long-horizon agent training.
**Límite:** Depends on training/branching capabilities absent from the documented live MCP interface.

## Fundamentos, archivos, recursos y estadística

### R19 — HOO

[X-Armed Bandits](https://www.jmlr.org/papers/v12/bubeck11a.html). Sébastien Bubeck, Rémi Munos, Gilles Stoltz et al.; 2011. JMLR 12 (2011).
Alcance comprobado: `primary_abstract`.

**Utilidad:** Formal hierarchical optimistic search over a structured space of actions.
**Límite:** Locally Lipschitz/similarity assumptions are not established for prompt mutations.

### R20 — StoSOO

[Stochastic Simultaneous Optimistic Optimization](https://proceedings.mlr.press/v28/valko13.html). Michal Valko, Alexandra Carpentier, Rémi Munos; 2013. ICML 2013.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Noisy coarse-to-fine optimisation with hierarchical partitions and unknown smoothness.
**Límite:** Does not remove all regularity assumptions or guarantee arbitrary semantic-tree search.

### R21 — Procrastinated Tree Search

[Procrastinated Tree Search: Black-Box Optimization with Delayed, Noisy, and Multi-Fidelity Feedback](https://doi.org/10.1609/aaai.v36i9.21280). Junxiong Wang, Debabrota Basu, Immanuel Trummer; 2022. AAAI 2022.
Alcance comprobado: `abstract_intro`.

**Utilidad:** Hierarchical optimisation with delayed, noisy and multi-fidelity feedback.
**Límite:** Its bias/smoothness/delay assumptions must be checked; successful long games have informative duration.

### R22 — BAST

[Bandit Algorithms for Tree Search](https://arxiv.org/abs/cs/0703062). Pierre-Arnaud Coquelin, Rémi Munos; 2007. INRIA technical report / arXiv.
Alcance comprobado: `abstract_intro`.

**Utilidad:** Shows pathological UCT behaviour and motivates smooth-tree confidence-based pruning.
**Límite:** Unknown descendants cannot be safely bounded by one parent's observed score without assumptions.

### R23 — MAP-Elites

[Illuminating search spaces by mapping elites](https://arxiv.org/abs/1504.04909). Jean-Baptiste Mouret, Jeff Clune; 2015. arXiv preprint.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Keep good policies in different behavioural niches rather than only the global best.
**Límite:** Descriptors and niche estimates must be reliable; diversity is not itself the competition score.

### R24 — QD populations

[Evolving Populations of Diverse RL Agents with MAP-Elites](https://arxiv.org/abs/2303.12803). Thomas Pierrot, Arthur Flajolet; 2023. arXiv preprint.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Evolve diverse populations with separate hyperparameters/learnable components.
**Límite:** RL population training differs from frozen LLM policy testing.

### R25 — Go-Explore

[First return, then explore](https://arxiv.org/abs/2004.12919). Adrien Ecoffet, Joost Huizinga, Joel Lehman et al.; 2021. Nature (2021).
Alcance comprobado: `abstract_intro`.

**Utilidad:** Archives preserve useful stepping stones and support return before new exploration.
**Límite:** Do not assume its environment-state restoration is allowed or available here.

### R26 — POET

[Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions](https://arxiv.org/abs/1901.01753). Rui Wang, Joel Lehman, Jeff Clune et al.; 2019. GECCO 2019.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Alternative paths and transferred stepping stones can solve deceptive tasks.
**Límite:** Generating or modifying game environments is not authorised by the official MCP tools.

### R27 — PBT

[Population Based Training of Neural Networks](https://arxiv.org/abs/1711.09846). Max Jaderberg, Valentin Dalibard, Simon Osindero et al.; 2017. arXiv preprint.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Asynchronous exploit/explore across a population; schedules can outperform a fixed setting.
**Límite:** Training checkpoint inheritance is not cloning a valid game state.

### R28 — PB2

[Provably Efficient Online Hyperparameter Optimization with Population-Based Bandits](https://arxiv.org/abs/2002.02518). Jack Parker-Holder, Vu Nguyen, Stephen Roberts; 2020. NeurIPS 2020.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Model-guided adaptation of population hyperparameters.
**Límite:** Theoretical efficiency concerns its model and assumptions, not arbitrary prompt workers.

### R29 — Hyperband

[Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization](https://jmlr.org/papers/v18/16-558.html). Lisha Li, Kevin Jamieson, Giulia DeSalvo et al.; 2018. JMLR 18 (2018).
Alcance comprobado: `primary_abstract_and_metadata`.

**Utilidad:** Allocate more evaluation resource to promising candidates in staged comparisons.
**Límite:** Use episode count as resource; a shorter game horizon can reverse strategy ranking.

### R30 — ASHA

[A System for Massively Parallel Hyperparameter Tuning](https://arxiv.org/abs/1810.05934). Liam Li, Kevin Jamieson, Afshin Rostamizadeh et al.; 2020. MLSys 2020.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Practical asynchronous allocation among many jobs.
**Límite:** Fast early failures and slow successful episodes require careful handling of pending work.

### R31 — BOHB

[BOHB: Robust and Efficient Hyperparameter Optimization at Scale](https://proceedings.mlr.press/v80/falkner18a.html). Stefan Falkner, Aaron Klein, Frank Hutter; 2018. ICML 2018.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Combines model-guided proposals with staged resource allocation.
**Límite:** Low-resource estimates must be informative about the real target.

### R32 — TuRBO

[Scalable Global Optimization via Local Bayesian Optimization](https://arxiv.org/abs/1910.01739). David Eriksson, Michael Pearce, Jacob R Gardner et al.; 2019. NeurIPS 2019.
Alcance comprobado: `abstract_and_verified_metadata`.

**Utilidad:** Local Bayesian search is useful for bounded numeric design knobs.
**Límite:** Prompt-text proximity does not automatically define a smooth numeric objective.

### R33 — Robust MFBO

[Multi-Fidelity Bayesian Optimization with Unreliable Information Sources](https://arxiv.org/abs/2210.13937). Petrus Mikkola, Julien Martinelli, Louis Filstroff et al.; 2023. AISTATS 2023, acceptance reported in author record.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Unreliable cheap sources can increase cost; robust source handling matters.
**Límite:** No guarantee cheap and target gameplay models are positively correlated in this task.

### R34 — Multi-information source optimisation

[Multi-Information Source Optimization](https://arxiv.org/abs/1603.00389). Matthias Poloczek, Jialei Wang, Peter I. Frazier; 2017. NeurIPS 2017.
Alcance comprobado: `verified_metadata_abstract`.

**Utilidad:** Choose both an input/candidate and the information source used to measure it.
**Límite:** Source-specific bias/noise must not be hidden in a pooled average.

### R35 — Input-dependent fidelity

[Multi-fidelity Bayesian Optimization with Multiple Information Sources of Input-dependent Fidelity](https://proceedings.mlr.press/v244/fan24a.html). Mingzhou Fan, Byung-Jun Yoon, Edward Dougherty et al.; 2024. UAI 2024.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Source fidelity can change across regions of the input space.
**Límite:** A global Haiku-to-target correlation does not validate every new policy family.

### R36 — Top-two best-arm identification

[Simple Bayesian Algorithms for Best Arm Identification](https://proceedings.mlr.press/v49/russo16.html). Daniel Russo; 2016. COLT 2016.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Allocate measurement effort to distinguish credible contenders for final selection.
**Límite:** Fixed-alternative statistical guarantees differ from generation of unobserved descendants.

### R37 — Modern top-two analysis

[Optimal Top-Two Method for Best Arm Identification and Fluid Analysis](https://arxiv.org/abs/2403.09123). Agniv Bandyopadhyay, Sandeep Juneja, Shubhada Agrawal; 2024. arXiv preprint.
Alcance comprobado: `verified_metadata_abstract`.

**Utilidad:** A modern theoretical reference on optimal top-two selection under its setting.
**Límite:** No universal finite-budget optimality is inferred for this open-ended search.

### R38 — Confidence sequences

[Time-uniform, nonparametric, nonasymptotic confidence sequences](https://doi.org/10.1214/20-AOS1991). Steven R. Howard, Aaditya Ramdas, Jon McAuliffe et al.; 2021. Annals of Statistics 49 (2021).
Alcance comprobado: `primary_abstract_and_metadata`.

**Utilidad:** Time-uniform intervals support repeated looks and optional stopping under assumptions.
**Límite:** Adaptive policy changes, actor changes and environment drift define new estimands/epochs.

### R39 — Statistical precipice

[Deep Reinforcement Learning at the Edge of the Statistical Precipice](https://arxiv.org/abs/2108.13264). Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro et al.; 2021. NeurIPS 2021.
Alcance comprobado: `primary_abstract_and_metadata`.

**Utilidad:** Show distributions and uncertainty rather than only top scores.
**Límite:** Auxiliary robust summaries do not replace the official arithmetic mean.

## Contexto y transferencia entre modelos

### R40 — Options

[Between MDPs and semi-MDPs: A framework for temporal abstraction in reinforcement learning](https://all.cs.umass.edu/pubs/1999/sutton_ps_AI99.pdf). Richard S. Sutton, Doina Precup, Satinder Singh; 1999. Artificial Intelligence 112 (1999).
Alcance comprobado: `primary_abstract`.

**Utilidad:** Initiation, subpolicy and termination formalise context-dependent modes over time.
**Límite:** A discovered month index is not proof of a causal regime change.

### R41 — policytree

[policytree: Policy learning via doubly robust empirical welfare maximization over trees](https://joss.theoj.org/papers/10.21105/joss.02232). Erik Sverdrup, Ayush Kanodia, Zhengyuan Zhou et al.; 2020. JOSS 5(50), 2232 (2020).
Alcance comprobado: `publisher_record`.

**Utilidad:** Interpretable policy trees provide an alternative to opaque routing.
**Límite:** Offline causal estimators need assumptions/data not supplied by the current aggregate logs.

### R42 — MAPO

[MAPO: Boosting Large Language Model Performance with Model-Adaptive Prompt Optimization](https://arxiv.org/abs/2407.04118). Yuyan Chen, Zhihao Wen, Ge Fan et al.; 2024. arXiv 2024; record reports Findings EMNLP 2023.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Prompt effectiveness depends on the actor model.
**Límite:** The preprint reports earlier EMNLP acceptance; use explicit source dates rather than conflating them.

### R43 — S2LPP

[S2LPP: Small-to-Large Prompt Prediction across LLMs](https://arxiv.org/abs/2505.20097). Liang Cheng, Tianyi LI, Zhaowei Wang et al.; 2025. arXiv preprint.
Alcance comprobado: `primary_abstract`.

**Utilidad:** Some task families support useful small-to-large prompt preference transfer.
**Límite:** Useful transfer in QA/NLI does not guarantee transfer in long-horizon gameplay.

### R44 — Concept distillation

[Concept Distillation from Strong to Weak Models via Hypotheses-to-Theories Prompting](https://aclanthology.org/2025.naacl-industry.52/). Emmanuel Aboah Boateng, Cassiano O Becker, Nabiha Asghar et al.; 2025. NAACL 2025 Industry Track.
Alcance comprobado: `primary_abstract`.

**Utilidad:** A strong model can diagnose weak-model mistakes and propose general concepts.
**Límite:** Rules distilled from named game answers or hidden formulas cannot be imported into the submission.

### R45 — Research-agent search comparison

[AI Research Agents for Machine Learning: Search, Exploration, and Generalization in MLE-bench](https://arxiv.org/abs/2507.02554). Edan Toledo, Karen Hambardzumyan, Martin Josifoski et al.; 2025. arXiv preprint.
Alcance comprobado: `abstract_intro`.

**Utilidad:** Study search policies/operators/evaluators in a common research-agent environment.
**Límite:** This is AIRA-dojo's comparative paper, not the original AIDE paper.

## Practicantes

### R46 — Unagi ICFP 2025

[ShinkaEvolve in Action: How a Human-AI Partnership Conquered a Coding Challenge](https://sakana.ai/icfp-2025/). Takuya Akiba; 2025. Primary practitioner account.
Alcance comprobado: `primary_practitioner_report`.

**Utilidad:** Winning team focused AI search on a measurable bottleneck and reused resulting insights.
**Límite:** 320 trials/about USD 60 describe that subexperiment, not total winning cost or an LLM-only win.

### R47 — ALE-Agent AHC058

[Sakana AI Agent Wins AtCoder Heuristic Contest (First AI to Place 1st)](https://sakana.ai/ahc058/). Sakana AI; 2026. Primary practitioner account.
Alcance comprobado: `primary_practitioner_report`.

**Utilidad:** Diverse construction and structural mutations can outperform narrow local tweaks.
**Límite:** Known simulator and roughly USD 1300 setup differ from the current key/budget constraints.

### R48 — Anthropic multi-agent research

[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system). Anthropic; 2025. Primary practitioner account.
Alcance comprobado: `primary_engineering_report`.

**Utilidad:** Independent contexts, clear delegation and controlled summaries fit parallel independent episodes.
**Límite:** Vendor research evaluation is not evidence of a game advantage; coordination increases token consumption.

## Reglas y modelos comprobados

### R49 — Competition rules

[Competition rules and fair play](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html). TechArena Career Survival Agent organisers; 2026. Official documentation.
Alcance comprobado: `official_page`.

**Utilidad:** Binding platform/model/interface/fair-play requirements and scoring.
**Límite:** Research architecture is not organiser approval for external models, concurrency or bulk experimentation.

### R50 — Official MCP

[Configuring the track MCP server](https://techarena-career-sim.readthedocs.io/en/latest/mcp.html). TechArena Career Survival Agent organisers; 2026. Official documentation.
Alcance comprobado: `official_page`.

**Utilidad:** Five tools and stdio transport define the available interface.
**Límite:** No documented state clone, undo, arbitrary initial state or simulator seed parameter.

### R51 — Submission requirements

[Submission requirements](https://techarena-career-sim.readthedocs.io/en/latest/submission.html). TechArena Career Survival Agent organisers; 2026. Official documentation.
Alcance comprobado: `official_page`.

**Utilidad:** English deliverables, real video, consistent design evidence and valid structure.
**Límite:** A research laboratory is not the final ZIP; keep Spanish research and runtime data out of it.

### R52 — Opus 5.5

[Claude Opus 5.5 availability and pricing](https://www.anthropic.com/claude/opus). Anthropic; 2026. Official documentation.
Alcance comprobado: `official_product_page`.

**Utilidad:** Confirms requested orchestrator model and published API ID/base pricing.
**Límite:** Availability in the user's API account and fitness for this game were not tested.

### R53 — Haiku 5.5

[Claude Haiku 5.5 availability and pricing](https://www.anthropic.com/claude/haiku). Anthropic; 2026. Official documentation.
Alcance comprobado: `official_product_page`.

**Utilidad:** Confirms requested cheap worker and prompt-length-dependent base pricing.
**Límite:** Low price or generic subagent capability does not establish reliable strategy ranking.

### R54 — Sonnet 5.5

[Claude Sonnet 5.5 availability and pricing](https://www.anthropic.com/claude/sonnet). Anthropic; 2026. Official documentation.
Alcance comprobado: `official_product_page`.

**Utilidad:** Confirms requested escalation worker and published API ID/base pricing.
**Límite:** Treat model escalation as a changed experimental condition.

## Procedencia de la herramienta de consulta

### R55 — Scientific Agent Skills

[Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents](https://arxiv.org/abs/2609.00065). Timothy Kassis, Vinayak Agarwal, Yuhuan He et al.; 2026. arXiv preprint.
Alcance comprobado: `tool_provenance`.

**Utilidad:** Procedural literature lookup skill used to check metadata and identifier shape.
**Límite:** This supports retrieval provenance, not any claim about the proposed game strategy.

## Auditoría de identidad y versiones

Se hicieron seis consultas acotadas a la API de arXiv, sin clave y con solicitudes serializadas. Se comprobó la estructura Atom, el número devuelto y los títulos con el parser de la habilidad `paper-lookup`. Un identificador inicialmente supuesto para FunSearch devolvió un artículo real de física: se rechazó y se resolvió el original por la editorial. La verificación también detectó el cambio de título de la versión actual de Meta-TTL respecto a una página indexada antigua.

La herramienta de consulta procedimental contribuyó a esa verificación y se cita en R55; no es evidencia de eficacia de la estrategia. Las respuestas y textos recuperados completos permanecen en `local-runs/literature/`, ignorado por Git. No se consultaron paquetes internos ni bases de datos del simulador.
