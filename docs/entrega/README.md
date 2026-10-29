# Entrega

Material para los cortes de entrega (no es la entrega en sí).

| Archivo | Para |
|---|---|
| [jury-story.md](jury-story.md) | Guion base del vídeo `presentation.mp4` y la historia para el jurado |
| [target-budget.md](target-budget.md) | Cómo gastar los 50 USD de DeepSeek |
| [skills_design-draft.md](skills_design-draft.md) | English draft for final design/skills_design.md; reconcile with frozen t13-read-v2 |
| [decision_report-draft.md](decision_report-draft.md) | English draft for final design/decision_report.md; evidence, uncertainty and limitations |
| [t19-compliance.md](t19-compliance.md) | Internal status-line wording review; do not package as a design deliverable |
| [cut2/](cut2/PREPARAR.md) | Corte 2: borradores en inglés (`README.md`, `skills_design.md`, `decision_report.md`) con `TODO(manual)` y los pasos para cerrarlo; empaquetar con `scripts/entrega/build_cut.py` |

## Evidence map for the design drafts (internal; not for the submission ZIP)

The drafts are standalone accounts for human reviewers. Do not package raw research reports or this map as supporting explanations: their content has not been redacted for submission. Outcome numbers are experimental results, not hidden game rules. The drafts use no event titles, option text, supplied hidden limits or hidden scoring formulas.

| Draft claim | Owning evidence |
|---|---|
| Official document responsibilities, information sources, principal risks; Stage 2 consistency with submitted Skills | `local-runs/official-runner/docs/api-key.rst` lines 30–50 and `competition-rules.rst`, Stage 2, video, scope and hard-coded-rules sections |
| One Skill, retrieval, ordered quarterly instructions, review switch and leakage | [HALLAZGOS B10–B14](../../HALLAZGOS.md); [Transmission summary](../../lab/reports/transmision/resumen.md); [delivery study](../../lab/reports/transmision/fase0-carga-skills.md) |
| Replica 99.3% next-step accuracy, 99.5% promotion agreement, ~0.33 error on 600 new careers | [HALLAZGOS B1](../../HALLAZGOS.md); [motor validation](../../lab/reports/ingenieria-inversa/motor-exacto.md), M17/M20; distinguishes observed-state validation from generated trajectories |
| Perception recall, repeated readings and conditional label-bot comparisons | [DeepSeek README](../../lab/reports/deepseek/README.md); [categorisation](../../lab/reports/deepseek/categorizacion.md); [perception](../../lab/reports/deepseek/percepcion.md); HALLAZGOS B17–B21/C16 |
| Targeted bank result and no aggregate improvement | [masticado](../../lab/reports/deepseek/masticado.md); [review 2](../../lab/reports/deepseek/independent-designs/review-2.md), sections 2–3; title-cluster interval, not a whole-career effect |
| +6.7 points with SE 5.7; 95% CI −5.3 to +18.7; final same-batch leakage comparison | [Transmission summary](../../lab/reports/transmision/resumen.md); [review 2](../../lab/reports/deepseek/independent-designs/review-2.md), section 3; distinguishes pooled, same-batch and early stopping snapshots |
| Two t13-read-v1 target-model pilots scored 14.98 and 42.51 and ended early | Updated [ESTADO](../../ESTADO.md), DeepSeek row, and [HALLAZGOS C3](../../HALLAZGOS.md); detailed [pilot report](../../lab/reports/deepseek/partidas-oficiales.md) in this main revision still documents only the first pilot, so it is not used as proof of the second |
| Expect/Stalled detection 16% versus 49–63%; carry 97–100%; concern-count recognition 4/21 | [Palancas README](../../lab/reports/palancas/README.md); [notes](../../lab/reports/palancas/nota-memoria.md); [stalled-gain experiment](../../lab/reports/palancas/techos.md); [risk memory](../../lab/reports/palancas/riesgo.md); HALLAZGOS B22–B23/C9 |
| Status first, 1,000-character bound, log entries versus decisions | HALLAZGOS B25; draft uses only interface/memory observations and no hidden numeric mechanic |
| Risk-promoting wording: scores 53.2→48.1; crises 73→174 per 1,000 | HALLAZGOS B24 (source line report on Leah's branch); clearly labelled simulator evidence, not target-manual performance |
| Closing gain +0.552 [0.298,0.805], 600 randomised development careers; whole-career comparison inconclusive | [closing experiment README](../../lab/reports/mecanicas-emergentes/README.md), section 1 |
| Rejected planning, warning, reputation and generic-log strategies | HALLAZGOS X; [motor M21](../../lab/reports/ingenieria-inversa/motor-exacto.md); [Palancas README](../../lab/reports/palancas/README.md); [rubric/log study](../../lab/reports/transmision/fase3-rubrica.md) |

The historical jury outline is a narrative prompt, not current evidence. These drafts do not repeat its unverified blanket claims about preregistration, untouched holdouts, completed-only scoring or automated compliance guarantees.

## Relevo — Cut 1 design drafts

**27 October 2026, branch `alejandro/entrega`, base main `1044a8b`.** Drafted both required English design documents and a focused t19 compliance note. The documents distinguish predecessor/component results from the intended t13-read-v2 and mark final-package dependencies with `TODO(final)`. Safer status wording records a reversible observation, not a fixed limit; the concern count is not a hidden-risk total.

No candidate/source/data changes, model/API calls or games. Checks and word counts are recorded in `.planning/design-drafts/progress.md`. Remaining work: inspect the frozen t13-read-v2, resolve markers, ensure wording and validation status match it, then copy the approved drafts to `design/skills_design.md` and `design/decision_report.md` in the final submission. Do not copy this README, the planning notes or the internal t19 note into the submission. Commit/push these drafts and request integration with main.
