# Índice de informes

Cada línea de trabajo tiene su carpeta con un `README.md` (o `resumen.md`) que empieza por las conclusiones y acaba en un Relevo. Lo aprendido de todas está resumido, por importancia, en [HALLAZGOS.md](../../HALLAZGOS.md).

**Para mejorar el manual de DeepSeek, empieza por [deepseek/pendientes.md](deepseek/pendientes.md)**: todos los candidatos y lo que falta confirmar con la clave.

## Líneas activas

| Carpeta | Línea | Empieza por |
|---|---|---|
| [ingenieria-inversa/](ingenieria-inversa/) | **Motor**: reglas exactas del juego, simulador, política óptima (rama `main-1nddsg`) | [README.md](ingenieria-inversa/README.md), después [motor-exacto.md](ingenieria-inversa/motor-exacto.md) |
| [question-bank/](question-bank/) | **Categorías**: tipos de respuesta que la IA reconoce (rama `alejandro/optimistic-gauss-edyw1j`) | [README.md](question-bank/README.md) |
| [transmision/](transmision/) | **Transmisión**: cómo escribir reglas que la IA obedezca (rama `alejandro/transmision`) | [resumen.md](transmision/resumen.md) |
| [palancas/](palancas/) | **Palancas**: cuánto vale cada pista o herramienta del juego (nota como memoria, techos, avisos, reputación, riesgo, tokens) y cómo hacer que la IA la use (rama `alejandro/palancas`) | [README.md](palancas/README.md) |

## Investigación terminada, pendiente de integración

- [mecanicas-emergentes/](mecanicas-emergentes/README.md): asignación conjunta del cierre, 600 partidas oficiales y corrección de liquidación terminal; [PR #20](https://github.com/aleetreny/huawei/pull/20). Subtrabajo de motor, no nueva línea activa.
- [fuentes-externas/](fuentes-externas/kingjinsight-v11.md): repo público de otro participante (v11, 73,1 en una partida), arquitectura, contraste con HALLAZGOS e ideas (C37–C41). 28 oct.
- [huevos-pascua/](huevos-pascua/README.md): búsqueda de combinaciones ocultas y atajos de ascenso (28 oct, sólo bots): no existen; mecánica nueva del trimestre (HALLAZGOS B28, B29). Rama `claude/hidden-combos-easter-eggs-eb0edx`. Investigación corta, no línea activa.
- [mejora/](mejora/README.md): **Mejora** (29 oct): un manual mejor que `t13-read-v4` a partir de sus reglas. Lectura de los costes ocultos en los meses de evaluación (C68); el bucle de ex-v1 no empareja con DeepInfra (C69); respuestas sin llamada y `max_continuations` (C70); réplica con el modelo de v4 (C71); 10 partidas reales (C72); mapa de pérdidas, riesgo, versiones corta y de calidad, `v4-loop` (C74–C79). Candidatos `mejora/mv-5r` y `mejora/v4-loop`. **Cerrada el 30 oct** (rama `alejandro/mejora-v4`, borrada al juntar).
- [exploracion/](exploracion/README.md): **Exploración** (29 oct): réplica calibrada con las 2.743 decisiones reales de DeepSeek (C61), dónde están los puntos (C62), scripts con estado medidos (C63), trimestre por tramos y freno de salud (C64), la trampa del mes previo de L1 (C65), calidad +8 (C66); candidatos `lab/policies-src/exploracion/` y [plan de pruebas con DeepSeek](exploracion/plan-deepseek.md). Rama `claude/gradient-depression-skills-k3b6u0`.
- [suelo/](suelo/README.md): **Suelo**: que ninguna de las 3 partidas se hunda (28 oct): rutas de hundimiento en la réplica con B30, reglas contra la trampa de L1 y la crisis de confianza, candidato `lab/policies-src/suelo/suelo-v1`. Subtrabajo de la línea DeepSeek, rama `claude/linea-suelo-hundimientos-5xjrnm`.

## Otros dueños (no se tocan aquí)

| Carpeta o archivo | Dueño |
|---|---|
| `matteo-*.md`, `matteo-observed-growth-haiku-pilot.json`, [first-review-search/](first-review-search/) | Matteo |
| [t11-multi-machine/](t11-multi-machine/) | Leah |

## Históricos que se quedan aquí porque el código los usa

| Carpeta o archivo | Qué es | Quién lo usa |
|---|---|---|
| [teacher-digests/](teacher-digests/) | Resúmenes de partidas de Opus y Haiku del 26 oct (llevan texto del juego; no se copian a un manual) | `careerlab lint` (títulos conocidos) |
| [decision-research/](decision-research/) | Análisis de decisiones del 26 oct (Codex) | `scripts/explore_decisions.py` |
| [carrera-rapida.md](carrera-rapida.md) | Última página de estado de la carrera rápida (parada el 26 oct) | `careerlab ladder status --write` |

## Histórico (26 oct y noche del 26 al 27)

En [historico/](historico/). Ninguno es una línea abierta.

| Carpeta o archivo | Conclusión |
|---|---|
| [historico/cloud-run-status.md](historico/cloud-run-status.md) | Diario y relevo de la carrera de manuales en la nube (sustituida por las líneas actuales) |
| [historico/cloud-run-diagnostics/](historico/cloud-run-diagnostics/) | Cómo se pierde en el mes 24: rachas de C sin ascender |
| [historico/energy-bots/](historico/energy-bots/) | Bots de energía: la salud es el primer límite; ninguna mezcla evita la C de la primera evaluación |
| [historico/opus-ceiling/](historico/opus-ceiling/) | Techo con Opus: 54,2 de media; ni Opus asciende más |
| [historico/secciones/](historico/secciones/) | Laboratorio por periodos (T18): ninguna táctica por periodo gana con claridad |
| [historico/synthetic-method-comparison/](historico/synthetic-method-comparison/) | Prueba del método de elección en un juego de juguete |
| [historico/cloud-portability-2026-10-26.md](historico/cloud-portability-2026-10-26.md) | Prueba de que el laboratorio corre en la nube |
