# Laboratorio nocturno por periodos (T18): resumen de la noche

Rama `alejandro/lab-secciones`, origen de registro `secciones`, actor Haiku de siempre (`claude-cli:haiku`, CLI 2.1.303). Empezó el 27 oct 2026 a las 00:27 UTC.

**Cómo leer las tablas.** Una partida corta se corta al llegar a un mes dado (actor `claude-cli:haiku^M`, herramienta en `careerlab/truncate.py`); nunca cuenta como terminada ni como eliminada y no tiene nota. La nota (Q) sólo sale de partidas completas. Error estándar (SE) de la media; intervalos de Wilson al 95 % para porcentajes. Cada comparación es contra una referencia jugada en el mismo lote, intercalada.

## Mejor estrategia por periodo

Referencia en todos los periodos: **f3-lean-v1** (el manual de referencia del plan). P1 y P2 se miden con partidas cortas; P3 y P4, con las partidas completas de la prueba final (mismo lote, intercaladas). Nota (Q) media ± error estándar; sólo las partidas completas tienen nota.

| Periodo | Medida | Mejor estrategia probada | Partidas por brazo | Resultado (mejor / referencia) | Nota Q de esas partidas (mejor / referencia) | ¿Gana con claridad? |
|---|---|---|---:|---|---|---|
| **P1** meses 1–5 | % que asciende en la 1.ª evaluación | `review-clock` sobre f3-lean (cuenta atrás con el calendario publicado, no ceder N/O el mes previo) | 74 / 73 (3 rondas, 6 meses) | 49 % / 42 % | – (cortas) | **No** (+7 ± 8; las dos primeras rondas daban +15 y la tercera se dio la vuelta) |
| **P2** meses 6–17 | nivel en el mes 18 | `climb` (reparto al indicador que bloquea tras cada ascenso) | 24 / 24 (18 meses) | 2,25 / 2,29 | – (cortas) | **No** |
| **P3** meses 18–35 | nivel en el mes 36 · meses en L4 | manual compuesto `periodos-v1` (climb v2 dentro) | 37 / 37 (completas) | nivel en el mes 36: 3,3 / 3,1; meses en L4: 18,0 / 17,7 | 51,5 ± 3,0 / 50,4 ± 2,8 | **No** (en L4 casi nadie invierte en Skill: 0–2 % de las acciones) |
| **P4** meses 36–48 | terminadas · dimensiones finales | manual compuesto `periodos-v1` (closing dentro) | 37 / 37 (completas) | terminadas 28/37 / 26/37; nivel final 3,8 / 3,8; control de riesgo 81 / 74 | 51,5 ± 3,0 / 50,4 ± 2,8 | **No** (más terminadas y mejor control de riesgo, sin significación) |
| Riesgo (todos) | eliminaciones por crisis de confianza · control de riesgo final | `periodos-v1` | 37 / 37 (completas) | crisis de confianza 3 / 2; ruina 0 / 3; control de riesgo final 81 ± 5 / 74 ± 5 | – | No |

**En una frase:** ninguna táctica por periodo ganó con claridad en su propia medida. El manual compuesto `periodos-v1` empata con la referencia en 37 partidas completas por brazo (51,5 ± 3,0 frente a 50,4 ± 2,8); sólo mejora, sin llegar a prueba, el control de riesgo final y las ruinas.

## Tabla viva de hipótesis

| Id | Periodo | Qué cambia | Partidas por brazo | Resultado | Decisión |
|---|---|---|---|---|---|
| [P1-base](p1-base.md) | P1 | 4 manuales: f3-lean (ref.), bb-mechanics-lean, bb-mechanics, observed-growth-v7 | 30 (6 meses) | 47 %, 50 %, 37 %, 40 % ascienden en la 1.ª; 52/52 en el umbral ascienden | ninguno distinto; f3-lean y bb-mechanics-lean a 15 completas |
| [H-P1a](p1-h1-clock.md) | P1 | + `review-clock` (calendario publicado, techos, no ceder N/O el mes previo) | 25 (2×2) + 25 (réplica) | sobre f3-lean: 54 % frente a 39 % (50 y 49 partidas); pérdidas en el mes 5: 0,34 frente a 0,63 por partida; sobre bb-mechanics: 44 % frente a 60 % | **prometedora**; se profundiza |
| [H-P1d](p1-h2.md) | P1 | + `cap-trade` (no comprar Dignidad llena a cambio de Network) | 25 | 40 % frente a 40 % | descartada |
| [H-P1c](p1-h2.md) | P1 | + `log-check` (leer el registro de efectos) | 25 | 36 % frente a 40 %; ~2 llamadas por partida | descartada |
| [P4-bots](p4-bots-cierre.md) | P4 | Defuse + recuperación en el último año (bots) | 200 bots | control de riesgo 65 ± 6 frente a 67 ± 5; nota igual | descartada |
| [H-P1a ronda 3](p1-h3-runup.md) | P1 | reloj (réplica) y reloj + respuestas discretas (`review-run-up`) | 24 | 38 % y 46 % frente a 50 % | reloj **descartado** (total 49 % frente a 42 %, no se confirma); run-up descartado |
| [H-P2a](p2-h1-climb.md) | P2 | + `climb` (reparto al indicador que bloquea tras cada ascenso) | 24 (18 meses) | nivel en el mes 18: 2,25 frente a 2,29 | descartada |
| [Final](#manual-compuesto-recomendado) | P1–P4 | `periodos-v1` (núcleo f3-lean + review-clock + climb v2 + closing) | 37 completas | 51,5 ± 3,0 frente a 50,4 ± 2,8 | **no gana** (+1,1 ± 4,1) |
| Comprobación v2 | P1–P2 | `periodos-v2` (redacción para la rúbrica) frente a `periodos-v1` | 0 | no se llegó a jugar | pendiente |
| [H-P3a](#relevo) | P3 | `periodos-v3` (climb v3: cuello de botella por la charla de evaluación; Skill tras una evaluación fallida) | 19 / 19 (30 meses, de 20) | nivel en el mes 30: 3,26 (v3) frente a 3,32 (v1); Skill learning en L4: 0 % en ambos | sin conclusión (menos de 20 por brazo); la regla no se ejecuta |

## Revisión de las 2 horas (02:10 UTC)

**Qué he aprendido de la mecánica.**
- El ascenso de la 1.ª evaluación es un interruptor: 143 de 143 partidas que empezaron el mes 6 en el umbral ascendieron, y ninguna por debajo. Toda la varianza del P1 está en llegar al mes 6 sin perder un punto.
- Los puntos se pierden en el mes 5 (y algo en el 4) por respuestas de principios firmes o públicas que suben Dignidad (ya en 10) y cuestan Network, o que quitan tiempo a la entrega propia (Output). Siempre había otra respuesta que conservaba el punto.
- Haiku no sabe cuándo llega la evaluación ni reconoce el techo; si se le enseña a contar con el calendario publicado, lo hace y pierde la mitad de puntos en el mes 5. Las reglas generales sobre "ser discreto" (cap-trade) no cambian su elección.
- `check_latest_logs` enseña el efecto exacto de cada respuesta, pero Haiku apenas lo usa aunque se le pida.
- Con bots: limpiar riesgo "por si acaso" al final no sube el control de riesgo; lo que pesa es lo que crean las respuestas.

**Líneas que mato:** cap-trade, log-check, limpieza preventiva del último año.

**Dos ideas nuevas muy distintas:**
1. *Manual mínimo (G1)*: sólo f3-lean + el reloj en 150 palabras, para ver si DeepSeek (más débil) lo sigue mejor y ahorrar tokens.
2. *Proteger Skill desde L4 con el reloj de 6 meses*: en L4 la evaluación sólo mira la Skill; usar el mismo reloj para planear la Skill por semestre (cuántos meses quedan, cuánto falta por subir).

## Revisión de las 4 horas (04:30 UTC)

- **La mecánica que más pesa es la que menos se deja mover.** El P1 depende de 1–3 respuestas del mes 5; Haiku las juzga "por principios" y ni el calendario, ni el tono, ni el registro de efectos cambian esa elección de forma estable. Las réplicas lo confirman: las rachas de 25 partidas engañan (el reloj pasó de +15 a −12 en la tercera ronda).
- **Donde un manual sí manda es en el reparto trimestral.** Las notas muestran que Haiku sigue al pie de la letra las reglas de energía (`blocker:` y Prepare report materials en L3). Por eso la palanca prometedora es de reparto: en L4 la Skill bloquea durante ~19 meses y nadie invierte en ella.
- **Líneas que mato:** reloj como palanca del P1, cap-trade, log-check, climb v1 a 18 meses, limpieza preventiva del último año.
- **Dos ideas nuevas muy distintas:** (1) `climb-v3`: identificar el cuello de botella por lo que dice la charla de evaluación y por una evaluación fallida con Network y Output aún subiendo (entonces Skill), y volcar Skill learning + rotación ahí; (2) manual mínimo (G1) para DeepSeek y tokens: núcleo f3-lean + una línea de calendario, ~150 palabras.

## Hipótesis descartadas

| Hipótesis | Periodo | Motivo |
|---|---|---|
| Otro manual general (bb-mechanics, bb-mechanics-lean, observed-growth-v7) | P1 | 37–50 % frente a 47 % de f3-lean con 30 partidas; ninguno distinto. bb-mechanics además provoca agotamientos (3 en 6 meses) |
| H-P1a `review-clock` (calendario + no ceder N/O el mes previo) | P1 | Se ejecuta, pero 36/74 (49 %) frente a 31/73 (42 %) en tres rondas; la bajada de pérdidas del mes 5 no se repitió. Sobre bb-mechanics, peor (44 % frente a 60 %) porque duplica su regla |
| H-P1d `cap-trade` (no comprar Dignidad llena a cambio de Network) | P1 | 40 % frente a 40 %; las pérdidas se desplazan del mes 5 al 4 |
| H-P1c `log-check` (leer `check_latest_logs`) | P1 | 36 % frente a 40 %; Haiku lo llama unas 2 veces por partida aunque se le pida |
| `review-run-up` (reloj + respuestas discretas) | P1 | 46 % frente a 50 % (ronda 3) |
| H-P2a `climb` v1 | P2 | nivel en el mes 18 2,25 frente a 2,29; el P2 sigue dominado por salir de L1 |
| Limpieza preventiva del último año (bots) | P4 | sin efecto en el control de riesgo final ni en la nota; quitar la recuperación de salud provoca agotamientos |

## Manual compuesto recomendado

**`periodos-v1`** ([carpeta](../../policies-src/secciones/periodos-v1/)), un Skill por responsabilidad, 1.187 palabras:

| Skill | Periodo | Qué hace |
|---|---|---|
| `feedback-response` | siempre | núcleo de f3-lean: estados de riesgo (Defuse tras cualquier aviso), recuperación, plan tras una evaluación floja |
| `review-clock` | P1 (y cada evaluación) | cuenta atrás con el calendario publicado; no ceder Network/Output el mes previo |
| `climb` (v2) | P2–P3 | tras el primer ascenso, energía y acción principal al indicador que bloquea |
| `closing` | P4 | ningún riesgo enterrado, salud y dignidad altas, Network y Skill conservadas |

**Resultado en partidas completas** (lotes `final-periodos-v1` + `final-periodos-v1-ext`, intercalados, mismo actor):

| Manual | Partidas | P1: ascienden en la 1.ª | P2: nivel en el mes 18 | P3: nivel en el mes 36 | P4: terminadas | Nivel final | Q media ± SE | Riesgo · Salud+Dig. · Red · Skill · Dinero (terminadas) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| f3-lean-v1 (referencia) | 37 | 20/37 = 54 % | 2,5 ± 0,2 | 3,1 ± 0,2 | 26/37 | 3,8 ± 0,3 | **50,4 ± 2,8** | 74 ± 5 · 96 ± 1 · 60 ± 2 · 77 ± 3 · 36 ± 1 |
| periodos-v1 | 37 | 15/37 = 41 % | 2,4 ± 0,1 | 3,3 ± 0,2 | 28/37 | 3,8 ± 0,3 | **51,5 ± 3,0** | 81 ± 5 · 99 ± 1 · 63 ± 2 · 77 ± 2 · 34 ± 1 |

| Manual | Meses en L2 | Meses en L3 | Meses en L4 | Llegan a L5 | Eliminaciones |
|---|---:|---:|---:|---:|---|
| f3-lean-v1 | 9,1 | 12,0 | 17,7 | 18/37 | 6 despidos, 3 ruinas, 2 crisis de confianza |
| periodos-v1 | 7,4 | 11,4 | 18,0 | 17/37 | 6 despidos, 3 crisis de confianza |

(Meses en cada nivel entre las partidas que llegan a él; las que no salen de un nivel cuentan hasta su final.)

- **No gana.** Diferencia de nota +1,1 ± 4,1 (z = 0,26). Con 18 partidas por brazo parecía +5 y con 10, +10: la misma regresión hacia la media que en la carrera. Las partidas terminadas puntúan igual (61,3 ± 1,0 frente a 60,6 ± 1,3).
- Lo que sí cambia, sin llegar a ser prueba: ninguna ruina (0 frente a 3), algo más de partidas terminadas (28 frente a 26), mejor control de riesgo al final (81 frente a 74) y salida más rápida de L2 (7,4 frente a 9,1 meses). Lo que no cambia: el ascenso de la 1.ª evaluación (41 % frente a 54 %, peor sin ser significativo), el tiempo en L3 y L4, y el nivel final.
- Los Skills nuevos se ejecutan (cuenta atrás y `blocker:` en las notas), pero en L4 el reparto sigue sin ir a la Skill (0–2 % de las acciones), que es justo lo que frena a ambos brazos 18 meses en L4
- **Recomendación para el chat de entregas (T15):** por rendimiento, `periodos-v1` **no** justifica sustituir al manual elegido: empata con f3-lean. Puede usarse si interesa su estructura por periodos para la rúbrica y el jurado (un Skill por responsabilidad), sabiendo que juega igual. Para entregar, la versión con redacción para la rúbrica es **`periodos-v2`** (mismas reglas; prioridad explícita entre Skills; "estancado" en vez de techos no publicados; momento de la evaluación sin contradecir el orden publicado del mes). Un revisor Sonnet con la rúbrica oficial puntuó v1 en 71,5 de media (núcleo 80, reloj 66, climb 72, cierre 68); las correcciones de v2 son las que propuso.

## Relevo

**Actualizado: 27 oct 2026, 07:30 UTC.** El runner está parado (archivo `~/careerlab-data/huawei-secciones/STOP`) y la cola cancelada; no queda nada jugando. Rama `alejandro/lab-secciones`, origen `secciones`.

1. **Qué he hecho y por qué.**
   - Herramienta: corte de partidas de Claude en un mes (`careerlab/truncate.py`, actor `claude-cli:haiku^M`, resultado `truncated` que nunca cuenta como terminada ni eliminada) con instantánea de cada evaluación (estado antes y después, nota, ascenso, tono de RR. HH., explosiones). Pruebas en `tests/test_truncate.py` (309 tests OK).
   - Scripts en `scripts/secciones/`: `batch.py` (lotes intercalados por prioridad), `compose.py` (manual = base + módulos), `periods.py`, `fail_r1.py`, `reviews.py`, `period_table.py`, `alloc_by_level.py`, `avoidable.py` (catálogo de bots, sólo laboratorio), `close_bots.py` (bots del P4).
   - Experimentos en el orden de la tabla viva; un informe por hipótesis en `lab/reports/secciones/`.
2. **Resultados con números:** tablas de arriba. Datos: `lab/registry-origins/secciones/` (exportado) y `~/careerlab-data/huawei-secciones/runs/*/result.json` (campo `periods`; fuera de Git). Bots en `~/careerlab-data/secciones-bots/` (fuera de Git; contienen texto del juego).
3. **Lo que falló o quedó a medias.**
   - La prueba del P3 (`p3-h1-skill`, periodos-v3 frente a periodos-v1, cortes en el mes 30) quedó en 19 y 19 partidas (de 20) cuando terminaron las que estaban en juego (07:30): nivel en el mes 30 de 3,32 (v1) frente a 3,26 (v3), sin conclusión. Lo importante: **tampoco con climb-v3 elige Haiku Skill learning en L4** (0 % de las acciones trimestrales en L4), así que la regla no se ejecuta. Antes de repetir, hay que entender por qué Haiku la evita (cuesta 2 de energía y salud; quizá prefiere la recuperación o el Defuse que manda el núcleo).
   - La comprobación de `periodos-v2` no llegó a jugarse (20 + 20 partidas de 18 meses en cola, canceladas al cerrar); v2 sólo cambia la redacción, pero conviene comprobarla antes de entregarla.
   - Del lote `full-base` sólo se jugaron 2 completas (1 por brazo); las 14 de f3-lean se cancelaron porque las sustituyen las de la prueba final, y las de bb-mechanics-lean quedaron en cola (14, canceladas al cerrar).
   - Cuota: la semana pasó del 19 % (00:30) a 23 % a las 07:12 (unas 551 partidas de Haiku: 455 cortas y 96 completas); nunca saltó el freno.
4. **Siguiente paso concreto.**
   - **P3 es la palanca con más margen y mecánica clara:** en L4 la Skill bloquea ~19 meses y Haiku dedica 0–2 % de las acciones trimestrales a Skill learning o rotación. Terminar `p3-h1-skill` (20 por brazo, cortes en el mes 30) y, si la Skill en L4 sube y el tiempo en L4 baja, jugar periodos-v3 con 25 completas frente a f3-lean.
   - Repetir la prueba final con más partidas (hace falta ~80 por brazo para detectar 5 puntos).
   - Comandos:

     ```bash
     cd /home/user/huawei   # o tu copia del repo, en la rama alejandro/lab-secciones
     uv run careerlab origin set secciones
     export CAREERLAB_CLAUDE_EXE=~/claude-2.1.303/node_modules/.bin/claude
     uv run careerlab run --kind claude-cli --continuous --slots 4 --max-five-hour 0.65 --stop-file ~/careerlab-data/huawei-secciones/STOP &
     uv run python scripts/secciones/periods.py --batch p3-h1-skill
     uv run python scripts/secciones/alloc_by_level.py --batch p3-h1-skill
     uv run python scripts/secciones/period_table.py --batch final-periodos-v1,final-periodos-v1-ext
     # nuevo lote: scripts/secciones/batch.py --name <id> --cut <mes> --n 25 --arms <ref> <carpeta o nombre>
     ```
5. **Línea T18 de ESTADO.md:** actualizada.
