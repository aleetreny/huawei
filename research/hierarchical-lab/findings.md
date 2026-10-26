# Evidence notes — hierarchical research

Date/cutoff: 26 October 2026. These are research claims, not measured improvements in the game.

- Rechecked binding rules: official/evaluation-representative play is single-agent JiuwenSwarm 0.2.4b3 with designated model. External independent-episode orchestration requires interpretation, not an assumed exemption.
- Individual official Anthropic product pages confirm Opus 5.5, Sonnet 5.5 and Haiku 5.5; general model overview is stale. Availability in a particular account is unverified.
- MCTS-AHD (ICML 2025) closely matches the proposed outer policy tree, with progressive widening and temporarily poor candidates retained. Inner game-state MCTS is a different problem and needs branchable states.
- ShinkaEvolve uses parent/inspiration sampling, islands, novelty rejection and bandit model selection. Choosing mutation generators differs from validating cheap gameplay models as proxies.
- AdaEvolve (2026) adapts within-island intensity, across-island budget and meta-guidance. Its theory and results do not automatically transfer to noisy game episodes.
- Procrastinated Tree Search addresses delayed/noisy/multi-fidelity evaluations under assumptions, not arbitrary prompt-mutation guarantees.
- Multi-fidelity work includes unreliable sources and input-dependent fidelity. Cheap model score bias must be calibrated per policy/context.
- Unagi's primary ICFP 2025 report gives 320 ShinkaEvolve trials and about USD 60 for a focused SAT-encoding experiment, not the entire winning effort.
- arXiv API batches 01/02: 4/4 and 12/12 returned and parsed with bundled paper-lookup parser. Raw metadata remains in ignored local-runs/literature.
- Important correction to prior wording: lack of game-state cloning does not prevent MCTS over generated policy variants evaluated from fresh games.
- Patch error: attempted delete/add on one path was rejected atomically; corrected using an Update operation.
- arXiv batch 03 returned 13/13, but title checking caught one guessed FunSearch identifier that was actually a physics paper. Excluded it and resolved FunSearch via the original Nature DOI 10.1038/s41586-023-06924-6. Do not count a successful API result as correct identity.
- Batch 04 rechecked latest 2026 records: Meta-TTL current title differs from the older indexed page, and PACEvolve++ was updated 12 October 2026. Catalogue must follow verified current metadata, retaining aliases where useful.
- MCTS-AHD paper uses max-child backup and progressive widening. Copying max of noisy game scores would amplify selection bias; our proposed scheduler must separate own-policy estimates from search/descendant potential.
- Full episodes, mutant descendants and contextual specialists are different explanations for a seemingly bad branch becoming useful. Resurrection is not evidence that a fixed stationary policy's true mean changed.
- Statistical comparison cannot treat different actor models as IID replications. Calibrate policy ranking and audit cheaply rejected branches on the target model; reset epochs when model/environment/protocol changes.
- The first schema QA attempt exposed an environment issue: this jsonschema installation lacks its optional RFC 3339 date-time checker. The schema already declares date-time. QA now supplies an explicit ISO timestamp checker and the implementation protocol records the requirement; schema shape validation alone is not enough.
- Discovery audit for this goal: 23 Exa searches, 185 requested result slots, 185 exported entries and 184 distinct candidate URLs. The selected bibliography has 55 distinct primary sources. Exact Exa query strings were not retained in the export; topic IDs and returned candidate URLs were retained. Six exact arXiv metadata requests are preserved separately.
- Final remote verification found Matteo advanced from 0eb0924 to 27cd3c1. Reviewed all eight changed files read-only: new three-Skill candidate and an unstarted 100-run evaluation plan, not a new benchmark. Updated branch review; no teammate code/Skills merged or changed.
