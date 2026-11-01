# Assessment after cutoff 1 — 29 October 2026

**Verdict: qualification is within reach, but not secured. The strongest new result is a more reliable efficient tool loop, not a demonstrated improvement in gameplay. Prefer isolating that loop on unchanged t13-read-v4 before spending on more rules.**

## Evidence inspected

Fetched all 27 current remote branches into separate refs, preserving the working checkout. Read current main ESTADO, NORMAS, HALLAZGOS, pending-candidate list, Comprobante experiments and cp-v12 bundle; inspected updated branches from DeepSeek, Formato, Leah, GPT principles and floor/ceiling research. Source SHAs are frozen in refs.json. Recomputed means from the main branch's exported partidas.csv: 35 recorded runs, 28 with terminal scores and seven without scores. These are local development runs, not the organiser's three evaluation games. Snapshot and computed grouped results accompany this report. No paid calls, games, simulator experiments or code changes.

The user screenshot gives Gradient Depression 13th, 64.75; 10th is 68.17; first is 75.99. The repo independently records those same leaderboard numbers. The live scoreboard was inaccessible via the web tool, so this is a screenshot/repo comparison, not independent live verification. The public runner upstream HEAD remains 00b084a8, matching the local official documentation.

## What 13th means

The gap to the displayed top-ten threshold is 3.42 overall points. With the 80/10/10 formula, that equals +4.275 average gameplay points if other components stay fixed. Alternatively +34.2 token-efficiency points has the same effect. Improving efficiency from around63 to100 would add3.7 overall points at fixed gameplay and Skill quality:64.75 becomes68.45. With a slightly lower Skill-quality score the result may be closer to68.1. This is only around the current boundary, which can move after cutoff2. Aim for a margin, roughly70 rather than68.2.

No actual official component breakdown or the three organiser-run trajectories was found in the material inspected. Quality65 and efficiency63 are assumptions used in repo discussions; they are not known official marks. Under those assumptions64.75 implies average gameplay64.69. That does not establish that one run collapsed: three middling completed careers could also produce it. HALLAZGOS C45 overstates what can be diagnosed from the aggregate alone.

The result neither validates our earlier selected-local-run average70.945 nor proves v4 failed badly. The interrupted third local career already warned that the two successful scores were an optimistic view. This was acknowledged in the cutoff1 review; the official result makes it more important to stop ranking by successful careers alone.

## What changed in the repo

- Cutoff1 really submitted t13-read-v4; documents say official structure validation passed and a6m22s video was included.
- Comprobante found that reducing model replies saves much more than just shortening notes. It pairs take_action and the following observe in one reply, and plans quarterly calls together.
- cp-v5a showed large token savings but did not keep pairing consistently across the hosting routes sampled in research. cp-v10 changed the startup pattern and separated pairing from whether visible text was produced.
- cp-v12 retains cp-v5a gameplay rules with that more reliable loop and learns action menus from the current run. Two complete games used roughly370k and492k total tokens/month, both meeting the maximum efficiency band. This supports improved transport/efficiency in the tested conditions, not universal reliability across every provider or restart.
- The rules also changed relative to v4: senior-level Skill priority, a stalled-start recovery mode and altered memory fields. cp-v12 is not simply v4 with fewer model replies.
- Repository C49 records organiser approval, according to the team, for multiple official tool calls per reply, current-run-only scripts and describing own observations as heuristics. The earlier concern that these methods were unapproved is superseded within that scope. Preserve the written approval with submission records.

## Gameplay evidence, including failures

| Candidate | Scored games | Completed | Mean game score | Individual scores |
|---|---:|---:|---:|---|
| t13-read-v4 |2, plus1 interrupted |2 |70.95 among scored |71.67,70.22; interrupted at L1/month22 |
| cp-v5a |3 |3 |66.50 |66.27,65.10,68.13 |
| cp-v7 |3 |2 |53.56 |62.25,69.88,28.56 |
| cp-v8 |2 |1 |48.24 |68.20,28.28 |
| cp-v10 |2 |1 |42.11 |22.98,61.24 |
| cp-v11 |1 |0 |25.75 |25.75 |
| cp-v12 |2 |2 |59.82 |56.80,62.83 |
| script-v1 |2 |1 |45.05 |13.23,76.87 |
| script-v3 |3 |2 |53.20 |66.55,32.59,60.45 |

These samples are small and noncontemporaneous; they cannot rank true gameplay means reliably. cp-v12's lower mean is a regression signal to investigate, not proof the loop caused damage. Conversely its100% pairing is not proof gameplay was preserved.

An illustrative calculation: cp-v12's two game scores, quality65 and efficiency100 would give64.35 overall, not68–70. cp-v5a's three games with quality65 and efficiency94.6 give69.16. Neither projection is an official result or a reliable prediction from so few games. Pooling cp-v5a and cp-v12 produces five successful games averaging63.83, but these are not identical bundles and pooling does not remove the uncertainty about changed loop behaviour.

Token gains of3.3–3.7 overall points can be cancelled by only4.1–4.6 fewer average gameplay points. A single game falling from68 to20 among the official three costs12.8 overall points before any efficiency penalty. Early exits also cap their efficiency term at50. This is why preventing collapses and promotion delays still matters more than polishing the judge score.

Leah's v4-lean-q has useful supporting research but no target full-game confirmation and a predicted efficiency gain smaller than the one already demonstrated by Comprobante. It is no longer the leading efficiency candidate. Matteo's prior Haiku designs and rare-option experiments do not currently provide a demonstrated stronger DeepSeek candidate. The script route still has upside but no reliable winner: do not choose it merely for76.87.

## Where the next gameplay points probably are

The current traces describe two recurring problems: early choices repeatedly pursue a stat that no longer visibly rises while Output remains weak; later careers reach higher levels too late. A stalled-start rescue was actually observed in cp-v12, which is meaningful evidence for that mechanism, but the saved career finished at L4/56.80. Avoiding elimination alone is not sufficient.

The missing capability is maintaining and acting on evidence of progress across turns, rather than reading more generic advice. Stalled was not maintained reliably in v4; removing it does not solve wasteful investment. A history-rich probe should check whether the model can recognise lack of progress, distinguish an uncertain prediction from a real displayed effect and prioritise the currently lagging dimension. Any script should use current-run observations, not supplied hidden caps or event answer tables.

The report's comparison of a noisy simulator score around42 with successful real careers around65 requires care: compare identical policy definitions and the same denominator, including failures, before calibrating. Matching a mean alone can hide a wrong balance of early exits, promotion delays and late growth. Test intervention rankings on held-out runs, not only fit historical outcomes. The model-based planner average72.4 is a benchmark, not a mathematical upper bound on all possible strategies or the leaderboard's overall score.

## Recommended decision for cutoff2

1. **Keep cp-v12 as the current delivery fallback**, with its known full-game efficiency, exact frozen bytes and complete package. Do not describe it as proven superior gameplay.
2. **Use the next authorised target tests to isolate the gain:** unchanged t13-read-v4 gameplay plus only the robust startup/pairing loop versus cp-v12, same runner settings and interleaved runs where feasible. A small4–6-game block can check execution and major regressions; it cannot establish a4-point gameplay advantage. Write the decision criteria before testing and include every terminal failure.
3. **For a new gameplay intervention, use history-rich failure probes first**, targeted to wasted investment, Output and review preservation, with held-out cases. Do not spend the remaining window on another broad prose rewrite or an unbounded simulator recalibration project. Calibrate only what the imminent decision needs.
4. **Freeze and validate the actual chosen candidate before cutoff2**, 30October24:00 UK, with design documents describing its actual memory and tool loop. Counts of calls, menu learning and recovery exceptions must match the final files. No claim that the review report is the final submission.

If forced to decide immediately without further evidence, cp-v12 is a defensible next-cutoff candidate because efficiency is improved and the prior valid cutoff1 score remains in contention. It is not a qualification guarantee. With maximum efficiency and illustrative quality65, mean gameplay67 produces70.1 overall: that is a plausible, useful target. The immediate need is to retain gameplay in the mid-to-high60s while banking the efficiency improvement.

## Sources pinned to reviewed commits

- [Current project status](https://github.com/aleetreny/huawei/blob/e17b1f09f7ab7515c132b5e127b31cd606e8885b/ESTADO.md)
- [Current candidate queue and next steps](https://github.com/aleetreny/huawei/blob/e17b1f09f7ab7515c132b5e127b31cd606e8885b/lab/reports/deepseek/pendientes.md)
- [Comprobante experiments (read latest update and §6.17, not only stale opening recommendation)](https://github.com/aleetreny/huawei/blob/e17b1f09f7ab7515c132b5e127b31cd606e8885b/lab/reports/deepseek/comprobante.md)
- [Exported game data](https://github.com/aleetreny/huawei/blob/e17b1f09f7ab7515c132b5e127b31cd606e8885b/lab/data/deepseek/partidas.csv)
- [Findings, including official result C45 and permissions C49](https://github.com/aleetreny/huawei/blob/e17b1f09f7ab7515c132b5e127b31cd606e8885b/HALLAZGOS.md)
- [Leah lean variants](https://github.com/aleetreny/huawei/blob/532d672b8dda25a1e85b19849f8e19aa6533d8f6/lab/reports/stat-perception/09-v4-lean.md)

## Relevo

Read-only review requested by Matteo after the13th-place screenshot. Current candidates and evidence fetched without merging other people's branches or changing manuals. Generated score summaries and conditional projections, identified the lack of official per-run decomposition, and recommended isolating the loop improvement before further gameplay edits. No API spend, games or code tests were required. Saved all source refs and a small CSV snapshot; no narrative event data added here. Integrate only this report and its attachments into main as support for the existing DeepSeek/Comprobante work; this does not open a new experimental line.

## Submission plan and video clarification — follow-up, 29 October

Remote main/DeepSeek/Comprobante SHAs were rechecked and are unchanged from refs.json. Official rules were reopened online at the public upstream source.

**Tomorrow's objective:** retain the measured loop saving while keeping mean gameplay around67 or better, rather than trying to discover a new high-variance controller before the cutoff. Illustrative67 gameplay,65 Skill quality and100 efficiency gives70.1 overall. A competitor scoring75.99 need not average75.99 in gameplay:72 gameplay,85 Skill quality and100 efficiency gives76.1. These are examples, not reconstructed marks for any team. The leaderboard establishes achievable overall performance, not which implementation produced it or its repeatability.

**Time-limited plan:** prepare an isolated unchanged-v4-plus-robust-loop candidate and compare it with frozen cp-v12 in a predeclared small screen (for example three complete runs each, interleaved, same runner and routing configuration, within the team's already authorised spending). Include every terminal failure and all token counts; do not stop or omit a disappointing run. Six runs can identify execution problems and gross regressions, not establish a small true mean advantage. Check action rejection, recovery, menu transitions, ending behaviour, first promotions and stalled investments as well as weighted score. A history-rich probe is appropriate for a targeted new idea; another unvalidated prose/controller rewrite is not. This review does not launch or authorise paid tests itself.

Keep cp-v12 ready as the existing delivery fallback. Freeze the selected exact bytes tomorrow with enough time to validate and upload; target an internal22:00 UK upload buffer for the official30October24:00 cutoff. Update Skill design documents and the video only as necessary to accurately describe the final memory and paired tool loop. Verify the extracted ZIP in a clean directory. No stale TODOs or claims that changed bytes inherit the parent's test results.

**Video:** published process is Stage1 automated scoring (80% mean gameplay,10% SKILL.md quality,10% token efficiency). Video and design documents are used for Stage2 expert review, after Stage1 ends, for the top ten only. Thus64.75 is not a video/expert-review grade. No viewer telemetry, organiser acknowledgement of watching, or Stage2 score was available. Do not assert no organiser has opened the video: administrative/compliance inspection is distinct from scored expert review. The video is still mandatory in each final ZIP. Stage2 expert review accounts for30% of the advancing team's combined final score.

**Where we lack:** (1) previously expensive execution, now substantially improved; (2) gameplay with late promotion and wasteful investment in stats that stop visibly rising; (3) low-tail reliability, where one early collapse can erase the token gain; (4) evidence discipline: separate local successful-run averages, all-terminal averages and official scores. Repo simulator benchmarks are not proven hard ceilings on all attainable policies. We cannot infer another team's technique from its aggregate score.

**Relevo:** clarified tomorrow's decision sequence and checked video timing against primary rules. No paid calls, games, candidate changes or third-party messages. Next action belongs to the existing Comprobante/DeepSeek line; integrate this follow-up with the report.

Official sources: [competition rules](https://raw.githubusercontent.com/RAI-Internal/techarena-career-sim/main/docs/competition-rules.rst), [submission requirements](https://raw.githubusercontent.com/RAI-Internal/techarena-career-sim/main/docs/submission.rst).
