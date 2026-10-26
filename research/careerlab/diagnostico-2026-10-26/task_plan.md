# Plan del diagnóstico de cuellos de botella

Autor: Codex. Rama `alejandro/diagnostico-estrategias`. Base `origin/main` en `917565c`; estado de las 16:55 UTC del 26 de octubre. Plan propio: no modifica el plan global de la organizadora.

## Objetivo

Diagnosticar desde primeros principios qué limita aprender y conseguir mejores estrategias, contrastarlo con datos y código, y proponer una secuencia concreta de experimentos. Sólo análisis: no lanzar partidas ni cambiar la carrera, los manuales o el protocolo congelado.

## Fases

- [x] Leer ESTADO.md, actualizar referencias y crear rama/worktree propios.
- [x] Verificar objetivo y restricciones oficiales, evidencia metodológica y hallazgos ya existentes.
- [x] Analizar resultados exportados: supervivencia, puntuación, incertidumbre, diferencias entre actores y coste.
- [x] Revisar el bucle real de generación, ejecución, comparación y asignación para localizar pérdidas de información.
- [x] Derivar prioridades y experimentos falsables, distinguiendo hechos, hipótesis y propuestas.
- [x] Documentar Relevo y comprobar cálculos, hashes, enlaces y suite: 230 tests correctos.
- [x] Publicar commit/push y abrir [PR #4](https://github.com/aleetreny/huawei/pull/4) para la organizadora.

## Incidencias

- La ruta inicial de la skill Exa estaba mal transcrita; localizada la ruta correcta con `rg --files` y leída.
- El script de recuperación de planning-with-files no estaba en la ruta antigua de `.codex/skills`; localizado en `.agents/skills`.
- La primera ejecución del análisis asumía que toda evaluación exportada era terminal. Seis interrupciones importadas tienen puntuación nula: se excluyen expresamente del cálculo y se conservan en el recuento de exclusiones.

## Próximo paso

Diagnóstico terminado. Pendiente de la organizadora: revisar e integrar PR #4 y priorizar sus hallazgos. La evidencia numérica conserva la base 917565c; se ha contrastado el avance cualitativo de main a 3c1c993 sin mezclar cohortes.
