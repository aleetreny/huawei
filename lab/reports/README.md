# Índice de informes

Cada línea de trabajo tiene su carpeta con un `README.md` (o `resumen.md`) que empieza por las conclusiones y acaba en un Relevo. Lo aprendido de todas está resumido, por importancia, en [HALLAZGOS.md](../../HALLAZGOS.md).

**El proyecto está cerrado (1 nov 2026)** y todas las ramas están juntadas en `main`; las ramas que se citan abajo ya no existen y su historia está en `git log`. La historia completa está en el [README](../../README.md). Los candidatos de DeepSeek que quedaron sin probar están en [deepseek/pendientes.md](deepseek/pendientes.md).

## Líneas principales

| Carpeta | Línea | Empieza por |
|---|---|---|
| [ingenieria-inversa/](ingenieria-inversa/) | **Motor**: reglas exactas del juego, simulador, política óptima (rama `main-1nddsg`) | [README.md](ingenieria-inversa/README.md), después [motor-exacto.md](ingenieria-inversa/motor-exacto.md) |
| [question-bank/](question-bank/) | **Categorías**: tipos de respuesta que la IA reconoce (rama `alejandro/optimistic-gauss-edyw1j`) | [README.md](question-bank/README.md) |
| [transmision/](transmision/) | **Transmisión**: cómo escribir reglas que la IA obedezca (rama `alejandro/transmision`) | [resumen.md](transmision/resumen.md) |
| [palancas/](palancas/) | **Palancas**: cuánto vale cada pista o herramienta del juego (nota como memoria, techos, avisos, reputación, riesgo, tokens) y cómo hacer que la IA la use (rama `alejandro/palancas`) | [README.md](palancas/README.md) |

## Investigaciones cortas

- [mecanicas-emergentes/](mecanicas-emergentes/README.md): asignación conjunta del cierre, 600 partidas oficiales y corrección de liquidación terminal; [PR #20](https://github.com/aleetreny/huawei/pull/20). Subtrabajo de motor, no nueva línea activa.
- [fuentes-externas/](fuentes-externas/kingjinsight-v11.md): repo público de otro participante (v11, 73,1 en una partida), arquitectura, contraste con HALLAZGOS e ideas (C37–C41). 28 oct.
- [huevos-pascua/](huevos-pascua/README.md): búsqueda de combinaciones ocultas y atajos de ascenso (28 oct, sólo bots): no existen; mecánica nueva del trimestre (HALLAZGOS B28, B29). Rama `claude/hidden-combos-easter-eggs-eb0edx`. Investigación corta, no línea activa.
- [tramos/](tramos/README.md): **Tramos** (30 oct, activa): por qué el banco engaña y un arnés que juega el principio de la partida con la petición exacta de JiuwenSwarm contra el motor oficial; el razonamiento vuelve al historial (corrige C51); piloto v4 frente a v4-loop hasta el mes 6.
- [mejora/](mejora/README.md): **Mejora** (29 oct): un manual mejor que `t13-read-v4` a partir de sus reglas. Lectura de los costes ocultos en los meses de evaluación (C68); el bucle de ex-v1 no empareja con DeepInfra (C69); respuestas sin llamada y `max_continuations` (C70); réplica con el modelo de v4 (C71); 10 partidas reales (C72); mapa de pérdidas, riesgo, versiones corta y de calidad, `v4-loop` (C74–C79). Candidatos `mejora/mv-5r` y `mejora/v4-loop`. **Cerrada el 30 oct** (rama `alejandro/mejora-v4`, borrada al juntar).
- [exploracion/](exploracion/README.md): **Exploración** (29 oct): réplica calibrada con las 2.743 decisiones reales de DeepSeek (C61), dónde están los puntos (C62), scripts con estado medidos (C63), trimestre por tramos y freno de salud (C64), la trampa del mes previo de L1 (C65), calidad +8 (C66); candidatos `lab/policies-src/exploracion/` y [plan de pruebas con DeepSeek](exploracion/plan-deepseek.md). Rama `claude/gradient-depression-skills-k3b6u0`.
- [suelo/](suelo/README.md): **Suelo**: que ninguna de las 3 partidas se hunda (28 oct): rutas de hundimiento en la réplica con B30, reglas contra la trampa de L1 y la crisis de confianza, candidato `lab/policies-src/suelo/suelo-v1`. Subtrabajo de la línea DeepSeek, rama `claude/linea-suelo-hundimientos-5xjrnm`.

## Otros dueños (no se tocan aquí)

| Carpeta o archivo | Dueño |
|---|---|
| `matteo-*.md`, `matteo-observed-growth-haiku-pilot.json`, [first-review-search/](first-review-search/) | Matteo |
| [stat-perception/](stat-perception/README.md) | Leah: **percepción de indicadores**, el paso (c) de Categorías: qué forma de etiquetar entiende Haiku, cuánto vale en la réplica y si cambia las elecciones (rama `leah/workspace`; cerrada con Haiku) |
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

## Resto de carpetas y notas (cierre del 1 nov)

Líneas de Alejandro que se abrieron después del índice y estudios de Matteo y Leah que llegaron al juntar sus ramas.

| Carpeta o archivo | Qué es |
|---|---|
| [action-notes-study](action-notes-study/) | Note, contesto e cache — indagine approfondita |
| [bhr](bhr/) | BHR — Build, Hold, Repair |
| [calidad-skills](calidad-skills/) | Calidad de los SKILL.md (10 % de la nota automática) |
| [consistency-with-ale](consistency-with-ale/) | Confronto dei pattern con i risultati di Ale |
| [constrained-growth-study](constrained-growth-study/) | Crescita con vincoli di sostenibilità |
| [corte3](corte3/) | Línea Corte 3: superar 72,93 en la última entrega (1 nov) |
| [cut1-model-review](cut1-model-review/) | Scelta del manuale per il primo cutoff — 27 ottobre 2026 |
| [cut2-state-review](cut2-state-review/) | Assessment after cutoff 1 — 29 October 2026 |
| [easter-eggs](easter-eggs/) | Easter eggs: esistono scorciatoie per saltare livelli? |
| [financial-reserve-study](financial-reserve-study/) | Riserva economica dalla nuova partita |
| [first-review-transfer](first-review-transfer/) | First-review rule transfer: actor-controlled pilot |
| [formato](formato/) | Línea Formato: cambiar la forma de dar el manual a DeepSeek |
| [growth-gap-study](growth-gap-study/) | Sopravvivere senza seconda promozione: diagnosi e priorità di crescita |
| [known-catalogue-closure](known-catalogue-closure/) | Known six-month catalogue: 100% answer coverage |
| [luna-v4-loop](luna-v4-loop/) | Due partite Luna: t13-read-v4 con il solo nuovo ciclo di chiamate |
| [m1](m1/) | M1 — v10 strategy with factual memory |
| [manual-memory](manual-memory/) | Memoria nei manuali: inventario, canale e costo |
| [matteo-bhr-cooperate-1.md](matteo-bhr-cooperate-1.md) | bhr-cooperate-1: 4 partite Haiku |
| [matteo-bhr-cooperate.md](matteo-bhr-cooperate.md) | bhr-cooperate: 8 partite Haiku |
| [matteo-bhr-countdown.md](matteo-bhr-countdown.md) | bhr-countdown: 8 partite Haiku, fermate dopo la prima review |
| [matteo-bhr-haiku.md](matteo-bhr-haiku.md) | BHR: 8 partite Haiku |
| [matteo-m1-haiku.md](matteo-m1-haiku.md) | M1: una partita Haiku |
| [matteo-observed-growth-haiku-4.md](matteo-observed-growth-haiku-4.md) | observed-growth-v1: four Haiku episodes (origin `matteo`) |
| [matteo-observed-growth-haiku-pilot.json](matteo-observed-growth-haiku-pilot.json) | (datos) |
| [matteo-observed-growth-haiku-pilot.md](matteo-observed-growth-haiku-pilot.md) | observed-growth-v1: first autonomous Haiku pilot |
| [matteo-observed-growth-v10-v12.md](matteo-observed-growth-v10-v12.md) | observed-growth v10, v11 and v12 (27 Oct morning) |
| [matteo-observed-growth-v2.md](matteo-observed-growth-v2.md) | observed-growth-v2: design from trajectories and four Haiku episodes |
| [matteo-observed-growth-v3.md](matteo-observed-growth-v3.md) | observed-growth-v3: four Haiku episodes, all completed |
| [matteo-observed-growth-v4.md](matteo-observed-growth-v4.md) | observed-growth-v4: four Haiku episodes (worse than v3; keep v3) |
| [matteo-observed-growth-v5.md](matteo-observed-growth-v5.md) | observed-growth-v5 and four fresh v3 replicates: v3's first batch was lucky |
| [matteo-observed-growth-v6.md](matteo-observed-growth-v6.md) | observed-growth-v6: eight Haiku episodes |
| [matteo-observed-growth-v7.md](matteo-observed-growth-v7.md) | observed-growth-v7: eight Haiku episodes, 7 completed, mean Q 61.27 |
| [matteo-observed-growth-v8.md](matteo-observed-growth-v8.md) | observed-growth-v8: eight Haiku episodes, stopped after the month-12 review |
| [matteo-observed-growth-v9.md](matteo-observed-growth-v9.md) | observed-growth-v9: eight Haiku episodes to the month-12 review |
| [matteo-observed-growth.md](matteo-observed-growth.md) | Observed growth: explicit instructions informed by manual pilots |
| [matteo-promotion-study.md](matteo-promotion-study.md) | Promotion study: what decides the first promotion |
| [matteo-t4-value-conversion.md](matteo-t4-value-conversion.md) | Matteo T4: responsibility converted into career value |
| [matteo-v10-vs-bhr.md](matteo-v10-vs-bhr.md) | v10 contro BHR: replica alternata |
| [memory-pilot](memory-pilot/) | Singolo pilot Luna con memoria — completato |
| [promotion-strategy](promotion-strategy/) | Manuale di strategia e percorso di verifica |
| [research-dashboard](research-dashboard/) | Pannello visuale della ricerca |
| [scenario-patterns](scenario-patterns/) | Scenario families and first-promotion patterns |
| [second-review-search](second-review-search/) | Esplorazione dei mesi 7–12 e della seconda promozione |
| [techo](techo/) | Línea Techo: que las partidas que terminan no se queden en L5 con ~70 |
| [trust-risk-study](trust-risk-study/) | Fiducia, memoria degli incidenti e sopravvivenza nel primo anno |
