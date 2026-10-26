# Draft questions for the organisers

Prepared 26 October 2026. **Not sent.** Intended channel: [official Discord](https://discord.gg/Ds4JC3gJjj). The [rules](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#interpretation-and-questions) require clarification before an ambiguous method is used. Record the organiser's actual reply and date; an unanswered question is not approval.

## A. Ask before any unusual-scale experiment

Hello, we are team Gradient Depression. We want to improve general decision procedures while following the five official MCP tools and the current-run-information requirement. Could you clarify the following before we implement any bulk experiments?

1. Are automated development batches through the unmodified official MCP server permitted beyond ordinary JiuwenSwarm development runs? If so, what limits apply to total games/tool calls, request rate, parallel sessions and concurrent LLM requests?
2. May a deterministic non-LLM development driver select ordinary game actions through those five tools to compare general strategies, or must every such development game also be controlled by the required JiuwenSwarm single-agent setup?
3. Is there an officially supported way to choose/reuse a seed or replay an action sequence for comparative testing? We will not clone or edit a database or call engine internals.

For A1–A2, our precise proposed architecture is an **external development laboratory**: a personally funded Claude orchestrator proposes generic policy revisions between games; several Haiku or Sonnet workers each play a separate complete episode through the five official tools. There is one actor per episode and no leader/teammate cooperation inside it. Results remain tagged by actor, and any official/evaluation-representative run uses the required single-agent platform and designated model. Is this development workflow allowed at all, and if so, under what model, concurrency, rate and retention limits? We understand that the submitted policy cannot depend on the external orchestrator, event-answer tables or hidden formulas. We have specified this architecture but have not launched it.

## B. Clarify learning scope, not a loophole

4. We understand that hidden thresholds/formulas and named-event answers may not be embedded in submissions, regardless of how obtained. Is quantitative research on our own MCP-returned transitions permitted solely for development analysis? If so, what restrictions apply to retaining results, using fitted predictive models or allowing such models to influence a final policy? We will not use this method until clarified.
5. Are qualitative procedural improvements derived from comparing our own completed runs permitted when the submitted agent itself uses only public information and feedback from its current run? Are persistent cross-game memories disabled or required to be cleared in official evaluation?
6. May a team use personally funded external LLMs for offline literature research, English editing or proposing generic Skill revisions, while using only the designated competition model/key and JiuwenSwarm `0.2.4b3` for all representative games? Are there restrictions on automated prompt optimisation or training/distillation even if no hidden formulas or event-answer tables are included?

## C. Lower-priority evaluation details

7. Which reported token fields count toward `total_tokens` for efficiency: cached input, reasoning/output and retries? Does official evaluation have any context, request or runtime caps beyond the published score rule?
8. If a team's highest Stage 1 score comes from an earlier version but its latest submitted ZIP differs, which version's Skills, design documents and presentation are used for expert review? Should the latest design explain earlier scored versions as well?
9. How should valid infrastructure/model failures be reported and distinguished from game failure during local comparison or official scoring?
10. Is there a published maximum ZIP size and required MP4 codec/resolution? We will keep normal playback speed and answer the five questions in order.

## Reply log

| Question | Organiser/date/link | Exact scope of clarification | Consequence for plan |
|---|---|---|---|
| A1–A3 | Pending; not sent | No permission established | No bulk-call or controlled-seed assumption. |
| B4–B6 | Pending; not sent | No permission established | No numerical hidden-rule learning, external-model development pipeline or persistent cross-game policy memory assumed permitted. |
| C7–C10 | Pending; not sent | No further details established | Use published scoring and conservative packaging; do not invent missing limits. |
