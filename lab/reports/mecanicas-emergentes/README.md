# Dos hallazgos nuevos sobre el cierre del juego

Investigación solicitada por Alejandro, 27 octubre 2026. Rama `alejandro/mecanicas-emergentes`. Base final: `main-1nddsg@da81e4a`, con catálogo v2 y política de referencia de 72,39 puntos reales. Se revisaron H1–H25, M1–M23 y las investigaciones por secciones/transmisión antes de contrastar siete hipótesis. La rama de revisión contiene sólo este trabajo encima de la investigación del motor.

**Resultado:** planificar conjuntamente el último trimestre mejora el cierre en **0,55 puntos** en el motor oficial (IC 95% **0,30–0,80**). Además, se identificó y corrigió una liquidación de nómina omitida en los dos generadores de la réplica. Las evidencias son distintas: una mejora de decisiones y una corrección de la representación del juego.

## 1. El cierre deja valor sin recoger: aún sirve mejorar la red

La fórmula de Q ya era conocida. Lo nuevo es comprobar que la política llamada «óptima» no la estaba aprovechando al cerrar:

- El cierre anulaba el valor de crecer **por debajo del umbral de ascenso**. Al terminar la carrera, eso también descartaba puntos de Network que todavía suman a la nota, aunque ya no permitan ascender.
- A veces gastaba energía en Defuse antes de elegir una acción principal que podía bajar ese mismo riesgo. Las dos decisiones se tomaban por separado.
- Seguía dando crédito a una reducción nominal de riesgo cuando el riesgo ya era cero.

En **568 estados oficiales de entrada al último trimestre**, la política anterior dejaba energía sin usar en **353**; el plan conjunto, en **52**. No hace falta gastar energía si ya nada mejora, pero sí aprovecharla cuando todavía queda una dimensión que puntúa.

Para cada estado se calcularon ambas secuencias completas: **406/568** admitían una mejora de Q, hasta **3 puntos** en un mismo estado. Este contraste es un **contrafactual calculado con la réplica**, no dos partidas oficiales clonadas. Las trayectorias elegidas sí se comprobaron contra el motor: **568/568 estados visibles finales encajan** una vez incluida la liquidación y permitida la fracción no visible del dinero.

Descomposición del beneficio contrafactual medio: red **+0,361**, salud+dignidad **+0,100**, habilidad **+0,007**, control de riesgo **−0,009**. La mayor parte viene de aprovechar la red; permitir algo de riesgo al final explica sólo una parte pequeña. No justifica jugar arriesgadamente durante la carrera.

### Ejemplo verificable

Estado de investigación: L6, Skill 145, Network 54, Output 38, Health 5, Dignity 5, riesgo 1, Wealth 40 y tres unidades de energía; ya no quedan evaluaciones.

| Plan | Energía | Acción principal | Salud / dignidad / riesgo al terminar | Q antes de nómina |
|---|---|---|---|---:|
| Anterior | Defuse + recuperar salud | Lay low | 8 / 5 / 0 | 71,75 |
| Conjunto | recuperar dignidad dos veces + recuperar salud | Lay low | 8 / 9 / 0 | **74,75** |

Ambos terminan con riesgo cero. El segundo evita pagar dos veces por la misma limpieza. Es una ilustración del mecanismo, no un estado oficial emparejado ni una receta numérica para una Skill.

### Confirmación separada de la exploración

| Prueba | Resultado |
|---|---|
| Réplica, 1.200 semillas nuevas por brazo, mismo flujo inicial | **+0,445 Q**, IC 95% emparejado **[0,419; 0,472]**; mismos niveles y derrotas |
| Motor oficial, 300 partidas por brazo, asignación aleatoria | Ganancia desde entrada al último trimestre: **3,059 frente a 2,507**; diferencia **+0,552**, IC 95% **[0,298; 0,805]** |
| Motor oficial, nota total sin ajustar | **72,97 frente a 72,52**; diferencia +0,448, IC 95% **[−1,303; 2,199]**: demasiado ruido para declarar un nuevo campeón global |

La medida primaria del motor se fijó antes de lanzarlo: Q final menos la Q del estado de entrada al último trimestre. La asignación se hizo al inicio de la partida, pero los brazos juegan **exactamente igual hasta ese trimestre**. Por tanto, llegar a ese punto es una condición anterior al tratamiento. Llegaron 283 controles y 285 tratamientos, todos terminaron. Se cuentan las 600 partidas en la comparación bruta; no se eliminan derrotas para mejorar la media. No hubo interrupciones ni acciones rechazadas.

Los IC son normales, calculados sobre partidas (diferencias por semilla en la réplica; grupos independientes en el motor). El estado de entrada usa dinero visible y el estimador de riesgo ya existente: es una variable anterior al tratamiento, no información futura. La validación de la liquidación se informa aparte.

## 2. La réplica se saltaba la última nómina

**El estado terminal de una carrera completa es el mes 49.** No hay un mes 49 jugable: después de la acción principal del mes 48, el motor avanza el mes, paga la nómina y liquida antes de puntuar. Son **48 nóminas**, no las 47 que abonaban los generadores.

Comprobación independiente con datos históricos ya publicados:

| Lote | Completadas | Mes terminal 49 | 48 nóminas | Dinero compatible con la nómina final | Duración en nivel +1 |
|---|---:|---:|---:|---:|---:|
| v03-validation | 471 | 471 | 471 | 471 | 471 |
| d01-planner2 | 380 | 380 | 380 | 380 | 380 |
| d02-planner2b | 154 | 154 | 154 | 154 | 154 |
| c02-planner-real | 151 | 151 | 151 | 151 | 151 |
| **Total histórico** | **1.156** | **1.156** | **1.156** | **1.156** | **1.156** |

Los 568 cierres del nuevo lote corroboran el estado tras esa liquidación. Los 4 smoke tests también. El motor muestra la parte entera del dinero: la comparación tolera únicamente la fracción compatible, no un error libre de ±1.

Para dinero bajo el tope de puntuación, el término omitido es **0,25 × salario del nivel final**: 0,175 Q en L4, 0,25 en L5 y 0,375 en L6. En el nuevo lote, la diferencia media entre Q oficial y predicción local de cierre baja de **0,452 a 0,103**, quedando principalmente la fracción monetaria no visible. Esto corrige la contabilidad, no demuestra por sí mismo una estrategia mejor.

Se corrigieron `replica.play` y `game.Game._advance`: las carreras completas liquidan una vez; los horizontes cortos y las partidas ya eliminadas conservan su comportamiento. `settle_completion=False` reproduce el criterio histórico. Los experimentos de esta investigación mantienen explícitamente ese criterio para reproducir sus resultados originales. En `terminal_q`, salario y nivel son iguales entre alternativas, así que la corrección no altera cuál es el mejor cierre ni su beneficio emparejado.

## 3. Lo que se probó y no se confirmó

Se ejecutaron **20.400 trayectorias en la réplica**, contando brazos y semillas compartidas, además de **600 partidas oficiales + 4 smoke tests**. No son 20.400 muestras independientes.

| Hipótesis | Qué ocurrió |
|---|---|
| No premiar reducción de riesgo por debajo de cero | +0,76 con la referencia antigua; sólo +0,13 con la actual. Señal pequeña, sin confirmación propia |
| Posponer el cierre para salvar el último ascenso | Prácticamente cero en nota; algunos ascensos extra no compensan el cierre peor |
| Optimizar juntos todos los trimestres | Piloto antiguo: mejora pequeña y más derrotas; no se promueve |
| Acumular más Skill por encima del mínimo | Mejora pequeña con la referencia antigua; casi nula con la actual |
| Cobrar el coste de oportunidad de historias largas | Parecía +0,85 en 400 semillas; **−0,50** en 2.000 nuevas. **Descartada** |
| Optimizar conjuntamente sólo el trimestre final | **Confirmada**, como se detalla arriba |
| Aumentar realmente el peso de Skill bajo umbral desde L4 | Algo más de L7, pero peor Q al insistir; no se confunde un récord de nivel con mejor estrategia |

Los pilotos `screen-01/02` usan catálogo v1 y referencia antigua, y quedan como exploración histórica. `screen-03` en adelante y las confirmaciones usan catálogo v2 y `politica_optima.json`. El campo `promotions48` de `screen-01` tenía una clave equivocada y **no se usa**; Q, nivel y supervivencia no estaban afectados. El hallazgo de nómina fue incidental durante la comprobación, y se contrastó con lotes históricos separados.

## 4. Traducción a un principio de Skill

Propuesta de texto general, **aún no probada con Haiku ni DeepSeek**:

> Once the final promotion assessment has passed, plan the remaining energy and main action together. If the main action will handle the remaining risk, use energy to restore wellbeing or improve another dimension that still contributes to the final result. Do not spend twice on the same cleanup, and do not leave useful energy idle merely because another promotion is no longer possible.

La prioridad debe depender de las mejoras que aún caben en el estado observado. No se copian a la Skill los números, fórmulas, umbrales ni respuestas del catálogo. No se ha cambiado ningún manual entregable, ni se ha usado IA/API de pago.

## 5. Evidencia y reproducción

- [Plan escrito antes de cada prueba](task_plan.md), [progreso](progress.md), [contexto](findings.md).
- [Resumen de todas las simulaciones](simulation-results.json) y carpetas `screen-*`, `confirm-*`, con una fila por trayectoria y manifiestos.
- [Resultado oficial](official-01/summary.json), [filas por partida](official-01/official-games.jsonl), [evidencia de los 568 cierres](official-01/quarter-evidence.jsonl.gz), [asignación aleatoria y versiones](official-01/manifest.json), [hashes de los logs completos](official-01/raw-hashes.json).
- [Auditoría de nómina](settlement/summary.json) y [filas históricas](settlement/games.jsonl).
- Código de intervención, análisis y auditoría en `scripts/mecanicas-emergentes/`. Los logs completos nuevos están en `~/careerlab-data/mecanicas-emergentes/official-01/`; la evidencia numérica de todos los cierres está también en Git.

```bash
# Análisis sin jugar partidas
python3 scripts/mecanicas-emergentes/analyze.py
python3 scripts/mecanicas-emergentes/settlement_audit.py

# Confirmación sintética reproducible; usar un destino nuevo
python3 scripts/mecanicas-emergentes/experiment.py \
  --variants base terminal_q terminal --games 1200 --seed 927000 \
  --out /tmp/mecanicas-confirm-reproduction

# Volver a analizar los logs oficiales existentes (no lanza partidas)
python3 scripts/mecanicas-emergentes/analyze.py \
  --official "$HOME/careerlab-data/mecanicas-emergentes/official-01"

# Comprobaciones
uv run pytest -q tests/test_replica_completion.py
uv run pytest -q
```

Para repetir partidas oficiales, `official.py` exige un directorio nuevo. El manifiesto conserva los argumentos exactos. Usa sólo las cinco herramientas oficiales, origen `emergentes`, servidores y carpetas propios; sin leer paquetes internos, sin fijar semillas del juego y sin tocar el registro de la carrera.

## Relevo

**Hecho y motivo.** Se revisó la investigación reciente, se descartaron mejoras que no sobrevivieron a semillas nuevas y se confirmó una intervención acotada de cierre. Se corrigió la liquidación terminal, descubierta al comparar predicción y observación. Todo está en la rama propia; la carrera y los manuales permanecen como estaban.

**Resultados.** +0,552 Q de ganancia de cierre en el motor, 600 partidas; réplica +0,445 en 1.200 pares. Nómina terminal verificada en 1.156 completadas históricas y 568 cierres nuevos. Evidencia y comandos arriba.

**Fallos/límites.** La ventaja global sin ajustar no es concluyente; no se afirma un nuevo campeón. El catálogo sólo es de desarrollo. Falta medir transferencia a texto. Los gzip históricos c02 están cortados como ya constaba en su informe: se conservaron sólo líneas JSON completas. Un glob inicial del analizador confundió las filas de auditoría con simulaciones; se corrigió y regeneró el resumen. No quedan procesos de partidas propios en marcha al cerrar.

**Siguiente paso concreto.** Integrar la corrección de liquidación en la rama de réplica y después en `main`; usar el texto general de cierre en una comparación independiente de manuales si el equipo lo decide. La mejora de bot no prueba obediencia ni transferencia del modelo de lenguaje. No hacen falta nuevas partidas para revisar este resultado: ejecutar los tres comandos de análisis anteriores.

**Validación de código.** 306 tests pasan en la rama final, incluidos cuatro de regresión para ambos generadores, no doble pago, horizonte corto, eliminación previa y el ejemplo de +3 puntos. `git diff --check` limpio.

**Coordinación.** Línea propia de `ESTADO.md` actualizada; commit, push y PR de revisión hacia `main`. [PR #20](https://github.com/aleetreny/huawei/pull/20). La investigación del motor `main-1nddsg@da81e4a` ya está incorporada en `main`; se sincronizó esta rama con `origin/main@e53b53f`, conservando la nueva estructura y resolviendo sólo el conflicto documental en ESTADO. Los commits exploratorios con la integración de T20 se preservan localmente en `alejandro/mecanicas-emergentes-exploracion`; la rama enviada excluye esos cambios ajenos.
