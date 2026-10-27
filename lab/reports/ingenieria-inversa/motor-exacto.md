# Reglas exactas del motor (caja negra, dev 1.0.8)

Segunda fase de la ingeniería inversa (27 oct 2026, sesión de la nube, rama `main-1nddsg`). El objetivo es **recrear el juego entero en un simulador propio** que reproduzca paso a paso las partidas reales, para buscar en él la jugada óptima.

Las reglas salen sólo de lo que devuelven las 5 herramientas oficiales en nuestras partidas: `observe`, `take_action` y `check_latest_logs`. No se lee el motor. Igual que en [hallazgos.md](hallazgos.md), **nada de esto se copia a una Skill** como número o umbral.

**Datos:**
- Lotes regenerados en la nube (los del Mac no estaban): `b00-random-safe` (2.657 partidas al azar con energía segura) y `b01-oracle-eps` (oráculo con un 15 % de decisiones al azar, en curso).
- Los datos brutos están en `/home/user/bbdata/` del contenedor, fuera de git.
- Scripts en `scripts/ingenieria-inversa/` (`tl.py`, `replay.py`, `monthtr.py`, `tags.py`).

**Validador.** `replay.py` predice el estado tras cada decisión a partir del estado anterior, con las reglas de abajo, y cuenta las diferencias.
- Dentro de un mes cuadran **64.001 de 64.508 transiciones (99,2 %)**.
- Las diferencias que quedan son, sobre todo, el dinero, que el juego muestra redondeado.

## M1. Orden de un mes

1. Tres decisiones de evento cada mes, siempre (12.390 de 12.390 meses).
2. En los meses 3, 6, 9… se juega después la fase trimestral: varias acciones de energía y una acción principal.
3. Se cambia de mes. Se cobra el sueldo, llega el comentario de RR. HH. y los avisos y, en los meses 6, 12, 18…, la evaluación semestral (charla, nota, bonus y ascenso).

En el registro oficial, el sueldo y la evaluación aparecen antes de la tercera decisión del mes, pero es sólo el orden de escritura: **la evaluación cuenta el efecto de las tres decisiones del mes 5.**

| Estado tras la 3.ª decisión | ¿Asciende? |
|---|---|
| La 3.ª decisión completa los mínimos | 80 de 87 sí |
| La 3.ª decisión rompe unos mínimos que se cumplían | 0 de 74 |

## M2. Historias

- Las continuaciones pendientes salen primero el mes siguiente, y luego eventos nuevos hasta llenar las tres plazas.
- Algunas continuaciones salen en el mismo mes, justo detrás. El hueco entre pasos de una misma historia es de 0 meses en 3.791 casos y de 1 mes en 8.508; más de un mes es raro.

## M3. Efecto de una respuesta

El efecto es el que anuncia el registro (H12), aplicado indicador a indicador:
- **Health y Dignity**: entre 0 y 10.
- **Skill, Network y Output**: no pueden superar el techo de su nivel (H1, H6). Si ya están por encima, una subida no los baja.
- **Mínimos**: Skill 1, Network 0 y Output −1.
- **Regla nueva (M3a).** Si una respuesta quita Skill estando ya en el mínimo (1), en su lugar se pierden **1 de Dignity y 1 de Output**. Pasa en 437 de 470 casos; el resto se explica porque Dignity u Output ya estaban en su mínimo.
- **Rareza del servidor (M3b).** La primera partida que juega un proceso de servidor recién arrancado no aplica los techos durante los meses 1–2. Se comprobó con servidores nuevos: sólo la primera partida, y el exceso se recorta solo antes del mes 3. No influye en ningún ascenso. Si la evaluación oficial arranca un servidor por partida, cada partida oficial tendrá esa ventana, que no cambia nada.

## M4. Explosión de riesgo ("Old landmines…")

| Efecto | Detalle |
|---|---|
| Dignity | −2 |
| Wealth | −2 |
| **Output** | **vuelve al valor que tenía al empezar el mes de hace cinco meses** (570 de 590 casos). Es decir, se pierde exactamente lo ganado en el último medio año. En L1 eso suele dejarlo en 0; en L4 lo baja de ~26 a ~22 |
| Riesgo final | cada explosión suma **5** al valor de riesgo que puntúa la nota final (M5) |

## M5. El riesgo de la nota final = riesgo oculto + 5 × explosiones

El valor `risk_control` del desglose final (2.657 partidas):

| Explosiones | Valor final | Partidas |
|---|---|---:|
| 0 | entre 0 y 7 | ~550 |
| 1 | entre 5 y 12 | ~770 |
| 2 (crisis de confianza) | siempre 10 | 1.501 |

- La nota de riesgo es (10 − valor) × 10, con mínimo 0. **Una sola explosión cuesta 5 puntos de nota final** solo por esta vía, más la dignidad, el dinero y el Output perdidos.
- El comentario de RR. HH. sigue al riesgo oculto: con el comentario tranquilo, el valor final va de 0 a 2; con el enfadado, de 4 a 6.
- Primer ajuste lineal del riesgo por respuesta: cuadra el 99 % de las partidas sin explosión, pero aún tiene más parámetros que partidas. Se rehará con b01.
- Lo que sí se ve ya en las acciones trimestrales:

  | Acción | Riesgo |
  |---|---|
  | Repair a key relationship | −0,7 |
  | Apply for rotation | −0,5 |
  | Lay low | −0,4 |
  | Defuse | −0,3 |
  | No hacer acción principal | **+1** |

## M6. Penalizaciones al cambiar de mes (avisos)

Avisos que aparecen en el texto del mes y lo que hacen (transiciones de b00 y b01, sin explosión ni ascenso):

| Aviso (texto resumido) | Cuándo | Efecto |
|---|---|---|
| "Payday just means paying off debts…" | dinero bajo cero | Dignity −1 (635 de 664) |
| "nobody asks you to lunch…" | Network en 0 durante varios meses | Health −1, Dignity −1, Output −2 |
| "do I really need this job?" | Dignity agotada | Health −2, Network −1 |
| "This half-year review fell short…" | evaluación con aviso en L1 | Health −1, **Dignity −5**, Network −1 |
| "jargon you cannot keep up with…" | Skill baja para lo esperado | ningún efecto inmediato visible |

Sin avisos, el 99 % de los cambios de mes no tocan los indicadores, salvo el sueldo.

## M7. Evaluación semestral: charla, nota y efectos

**La charla tiene tres tonos, con tres textos cada uno:**

| Tono | Textos (inicio) | Nota | Efecto |
|---|---|---|---|
| Aviso | "I had hopes…", "The room feels tense…", "HR marks the note…" | C o D | Health −1, Dignity −2 |
| Neutro | "Acceptable overall…", "This half was neither good nor bad…", "The feedback covers schedule…" | B o C | ninguno o Dignity +1 |
| Elogio | "Your manager closes their notebook…", "To be honest, I worried…", "The talk is shorter…" | A | ninguno |

- **Primer año (meses 6 y 12, como recién llegado):** un compañero te cubre ("A senior colleague…", "Your mentor texts…", "The team's old hand…", "a diligent peer…", "After standup your manager…"). Acompaña a la nota C de L1 y no tiene efecto propio.
- **Coste en Network de cada ascenso:**

  | Ascenso | Network |
  |---|---:|
  | L1 → L2 | 0 |
  | L2 → L3 | 0 |
  | L3 → L4 | −2 |
  | L4 → L5 | −2 (a veces −1) |
  | L5 → L6 | −3 (a veces −2) |

  Además, **ascender en la primera ocasión dentro del nivel** (6 meses en él) trae el aviso "You climbed too fast…" y **3 de Network más** en L2 → L3 y L3 → L4.

## M8. Acciones trimestrales: iguales en todos los niveles

El efecto de las acciones principales y de energía es el mismo de L1 a L6 (miles de casos por nivel):
- Rotation: Skill +2, Network +1.
- Skill learning: Skill +1, Health −1.
- Key project: Output +2, Skill +1, Network +1.

Lo mismo para las demás. **No escalan con el nivel**, así que en los niveles altos el crecimiento sale casi todo de los eventos.

## M9. Cuánta Skill puede dar el juego, y el techo de nota que eso impone

**Skill que ofrecen los eventos.** Para cada evento que salió, se tomó la mayor subida de Skill entre sus respuestas (367 preguntas exploradas del todo, 102.000 eventos):

| Nivel | Skill máxima media por decisión | Reparto (0 / +1 / +2 / +3) |
|---|---:|---|
| L1 | 1,09 | 25 % / 46 % / 27 % / 3 % |
| L4 | 1,07 | 26 % / 44 % / 28 % / 2 % |
| L5 | 1,04 | 27 % / 43 % / 28 % / 2 % |

Con 3 eventos al mes y +3 por trimestre de acciones (rotación y aprendizaje), **el máximo de Skill es de unos 4,3 al mes**, y eso eligiendo siempre lo que más Skill da.

**Calendario más rápido posible** con los umbrales medidos (H6, H14):

| Ascenso | Mes | Por qué |
|---|---:|---|
| L2, L3, L4 | 6, 12, 18 | |
| L5 | 30 | De ~42 (techo de L3) a 90 hace falta +48, unos 11 meses |
| L6 | 42 | De ~90 a 130 hace falta +40, unos 9 meses, y la evaluación siguiente llega a los 12 |
| L7 | ? | Umbral desconocido. Con L6 en el mes 42 se llegaría al 48 con unos 165 de Skill |

**Techo de nota sin L7:**

| Dimensión | Puntos |
|---|---:|
| Nivel 6 | 18 |
| Dinero (sueldos ~38 + 1 inicial + bonus ~8 = ~46, sobre 80) | 11,5 |
| Habilidad, red, salud+dignidad y riesgo al máximo | 50 |
| **Total** | **~80** |

Coincide con la mejor partida observada (79,3). **El margen entre los mejores manuales (~60) y 80 está en jugar bien:** no explotar y ascender en cada ventana. Para pasar de 80 hace falta L7.

## M10. Riesgo oculto: entero, visible y con explosión determinista (hallazgo central)

1. **El comentario mensual de RR. HH. es el riesgo oculto**, con 0 = sonriente, 1 = en voz baja, 2 = ceño fruncido, 3 = inquieto y 4 = enfadado, que también significa 4 o más.
   - Ajuste lineal sobre 22.156 cambios de mes: Defuse −1,06, High-intensity +1,18 y **Lay low −1,07**, que el juego no anuncia. Las demás acciones, ~0.
2. **Cada respuesta suma un entero fijo** al riesgo, sin bajar de 0.
   - Ajuste secuencial entero (`riskseq.py`) sobre 3.228 partidas: el 91 % cuadra exactamente en todos los meses y en el valor final.
   - Reparto de los valores: 0 (431 respuestas), +1 (216), +2 (117), +3 (29), −1 (114), −2 (12), −3 (10).
3. **Al llegar a 5 explota en el acto.** Pasa tras una respuesta, una acción de energía o el aviso de la evaluación:

   | Riesgo tras la decisión | Explosiones |
   |---|---|
   | 4 o menos | ~1 % (errores del ajuste) |
   | 5 | 1.200 de 1.208 |
   | 6 o más | todas |

   - Al empezar el mes, con riesgo 5 explota en 526 de 527 casos.
   - Tras la explosión el riesgo vuelve a 0 (M4).
   - La segunda explosión es la crisis de confianza.
4. **Un aviso en la charla de la evaluación suma +1 de riesgo**, además de Health −1 y Dignity −2 (607 de 609 casos).
5. **Consecuencia:** aparte del sorteo de eventos, **el juego es determinista**. Con el riesgo en 4, cualquier respuesta con riesgo positivo hace explotar; con el riesgo en 0, se pueden encajar respuestas de +3 o +4 sin explotar. Los "detonantes" de H20 son esto mismo: respuestas de riesgo alto con el contador ya cargado.

## M11. Nota y tono de la evaluación

- **La nota sale del estado justo antes de la evaluación**, sobre todo de Skill, Network y Output frente al techo y al umbral del nivel, y del tiempo en el nivel. Un modelo logístico por nivel la acierta:

  | Nivel | Acierto |
  |---|---:|
  | L1 | 100 % |
  | L2 | 96 % |
  | L3 | 99 % |
  | L4 | 93 % |
  | L5 | 98 % |

  - La D en L1 llega por quedarse: con 17 meses en el nivel.
  - **No se ha visto ninguna S** en 4.436 evaluaciones.
- **Bonus** = factor × sueldo mensual (S 3; A 2; B 1; C 0,25; D 0). El dinero se guarda redondeado a un decimal, así que el 0,075 de una C en L1 entra como 0,1.
- **Efecto de la charla:**

  | Charla | Efecto |
  |---|---|
  | Aviso | Health −1, Dignity −2, riesgo +1 |
  | Neutra | Dignity +1 |
  | D en L1 ("fell short") | además, Dignity −3 y Network −1 |
  | Ascenso en la primera ocasión ("too fast") | Dignity −1 y sin el +1 de la neutra |

## M12. Regla de ascenso

Se asciende si se cumplen las tres condiciones:
- Skill, Network y Output están en el umbral del nivel o por encima;
- Dignity es 4 o más;
- la nota no es D.

Acierta el **99,5 %** de 4.436 evaluaciones. Las excepciones son D en el mes 18, con 17 meses todavía en L1.

## M13. Pérdidas de dinero que escalan con el nivel

Lo que una respuesta quita de dinero se multiplica según el nivel (2.060 casos, sin excepciones):

| Niveles | Multiplicador |
|---|---:|
| L1–L2 | ×1 |
| L3–L4 | ×2 |
| L5–L6 | ×3 |

- **Las ganancias no se multiplican**, y la explosión cuesta siempre −2.
- Con un "−1" anunciado en L5 se pierden 3 de dinero, o 0,75 puntos de nota final.

## M14. El simulador `replica.py` y su validación

`scripts/ingenieria-inversa/replica.py` reúne M1–M13:
- catálogo de respuestas con sus efectos, su riesgo y su continuación;
- acciones trimestrales, techos, mínimos, sueldo, bonus, nota, tono, ascenso, avisos, explosiones, derrotas y nota final.

Con `validate`, el simulador recibe el estado observado y la decisión de cada paso y predice el estado siguiente. También predice el ascenso de cada evaluación y la nota final.

**Dentro de la muestra** (b01, 571 partidas, 67.839 pasos):

| Medida | Resultado |
|---|---:|
| Estado exacto tras cada paso | **98,7 %** |
| Ascenso sí o no | **99,2 %** |
| Error medio de la nota final | **0,43 puntos** |

**Validación en un lote nuevo** (`v02-validation`: 600 partidas del oráculo con un 5 % de decisiones al azar, jugadas el 27 oct después de fijar las reglas). Ninguna partida suya se usó para descubrir reglas: el catálogo `catalog_v1` sale sólo de b00 + b01. Salida completa en [validacion-v02.txt](validacion-v02.txt).

| Medida | Resultado | Objetivo |
|---|---:|---:|
| Estado exacto tras cada paso (todos) | **98,5 %** de 107.698 pasos | ≥ 95 % |
| … tras respuestas a eventos | 98,2 % de 77.410 | |
| … tras acciones de energía | 100,0 % de 22.234 | |
| … tras la acción principal | 97,0 % de 8.054 | |
| Ascenso sí o no en cada evaluación | **99,8 %** de 4.246 evaluaciones (8 ascensos no previstos, 1 previsto de más) | ≥ 95 % |
| Error medio de la nota final | **0,35 puntos** (máximo 1,43; el 100 % por debajo de 2) | ≤ 2 |

Qué falla todavía, en orden de peso:
1. **Dinero ±1 al cambiar de mes.** El juego muestra el dinero redondeado hacia abajo y una parte de los cambios no se puede reconstruir del todo.
2. **Nota A frente a B en L4.** Cambia el bonus y el +1 de Network. El modelo acierta un 87 %, porque la nota depende también de la media del semestre.
3. **Explosiones no previstas.** Se deben a respuestas poco observadas cuyo riesgo está mal medido.

**Cómo se reproduce:**

```bash
BB_DATA=~/careerlab-data/ingenieria-inversa python3 scripts/ingenieria-inversa/riskseq.py b00-random-safe,b01-oracle-eps  # riesgo -> riskd.json
python3 scripts/ingenieria-inversa/replica.py build --batches b00-random-safe,b01-oracle-eps --risk riskd.json --out catalog_v1.json
python3 scripts/ingenieria-inversa/replica.py validate --catalog catalog_v1.json --batches v02-validation
python3 scripts/ingenieria-inversa/replica.py play --catalog catalog_v1.json --games 500
```

El catálogo lleva títulos de eventos de dev. Por eso se queda fuera de Git, en la carpeta de datos, igual que las partidas.

## M15. Derrotas por condición persistente

| Derrota | Aviso (una sola vez por partida) | Condición | Partidas (b00+b01) |
|---|---|---|---:|
| Broke | "Payday just means paying off debts…" | dinero bajo cero antes de cobrar | 755 |
| You resign | "nobody asks you to lunch…" | Network en 0 | 160 |
| Breakdown | "do I really need this job?" | Dignity agotada (≤1) | 6 |
| Dismissed for capability | "This half-year review fell short…" | sigue en L1 | 25 |

- **El aviso sale a los 3 meses seguidos de la condición, y la derrota llega a los 6** si sigue.
  - De 755 ruinas, 680 llegan exactamente 3 meses después del aviso.
  - En el aislamiento es igual, aunque con más dispersión: 86 de 160 a los 3 meses.
- El despido llega 6 meses después de la evaluación con "fell short", en el mes 24 si sigues en L1.
- Ruina y aislamiento se evitan saliendo de la condición una sola vez antes del 6.º mes.
- Las demás derrotas:
  - **Blackout**: Health llega a 0, en el acto.
  - **Trust crisis**: la 2.ª explosión.
  - **Obsolete**: Skill muy por debajo de lo esperado; 1 caso.

## M16. L7 es alcanzable, por muy poco: el umbral de L6 → L7

**Una partida real llegó a L7** (lote `c01-greedy-real`, `p1-000282`, nota 74,55):

| Mes | Ascenso | Skill / Network / Output |
|---:|---|---|
| 6 | L2 | |
| 12 | L3 | |
| 18 | L4 | |
| 30 | L5 | |
| 42 | L6 | |
| 48 | L7 | 167 / 68 / 50 (nota B) |

- **Las 16 evaluaciones de L6 que no ascendieron tenían Skill de 163 o menos**, aunque algunas tenían Network 63–67 y Output 46–52. El umbral de Skill de L6 → L7 está **entre 164 y 167** y cuadra con la serie 8, 18, 35, 90, 130, ~165. Los de Network y Output quedan por debajo de 68 y 50; en el simulador se usan, provisionalmente, 60 y 45.
- **Techos de L6:** como mínimo 174 de Skill, 68 de Network y 52 de Output (valores vistos).
- **Lo que pide L7.** Hay que ascender en todas las ventanas posibles (6, 12, 18, 30, 42 y 48) y sumar unos 125 de Skill entre el mes 18 (techo de L3: 42) y el 47, es decir, **~4,2 de Skill al mes durante 30 meses, frente a un máximo teórico de ~4,3** (M9). Además hay que guardar Skill en L5 hasta cerca de su techo (154), para llegar a L6 en el mes 42 con ~150.
- En el simulador lo consigue el 0,5 % de las partidas voraces (3 de 600, con una nota máxima de 83,1). Hace falta suerte con los eventos: que sigan saliendo preguntas con +2 o +3 de Skill.

## M17. Estrategia óptima según el simulador

Búsqueda aleatoria de los pesos del planificador por etapas (`planner.py`, 60 configuraciones × 150 partidas, misma semilla) y comprobación de las 3 mejores con 600 semillas nuevas:

| Política (en el simulador) | Nota media | L6 | Crisis de confianza | Despidos |
|---|---:|---:|---:|---:|
| Voraz de un paso | 68,9 | 58 % | 0,5 % | 4 % |
| **Planificador ajustado** | **71,8** | 66 % | 1,7 % | 1,2 % |

Lo que eligió la búsqueda:
1. **Mucho peso a cumplir los umbrales de la próxima evaluación**, unas 7 veces lo que pesa crecer por encima de ellos, y aún más en el mes previo.
2. **Presupuesto de riesgo bajo:** tope de 2–3, con un coste por cada punto. Hay que dejar sitio al +1 del aviso de la evaluación.
3. **Lay low** en cuanto el riesgo llega a 2; Defuse sólo con riesgo alto.
4. **Final de partida (meses 46–48):** cambiar de objetivo a la nota en sí, con riesgo a 0 y salud y dignidad a 10.
5. **No elegir respuestas que cuestan dinero en los niveles altos** (pierden ×2 o ×3).

**Techo práctico.** Para L6 en el mes 42 con limpieza final, unos 80 puntos (M9); para L7, unos 82,5. **Nota óptima esperada, unos 72**, con la variación que pone el sorteo de eventos.

**Comprobado en el juego real** (lote `c02-planner-real`, 162 partidas antes de que se reiniciara el contenedor):

| Brazo | Partidas | Nota media | L6 | Crisis de confianza |
|---|---:|---:|---:|---:|
| Planificador ajustado | 82 | **70,5** | 72 % | 4 % |
| Igual, con cautela ante respuestas poco observadas | 80 | 70,0 | 65 % | 4 % |

**Es el mejor bot hasta ahora:** el oráculo anterior sacaba 67,9 y la política voraz real 63,9. El simulador predecía 71,8, así que **la estrategia encontrada sin jugar se traslada al juego real** con una diferencia de ~1,3 puntos.

**Diferencia con el juego real.** La política voraz saca 63,9 en el juego real (300 partidas) y 69,5 en el simulador. Casi toda la diferencia son crisis de confianza: 19 % en el juego real y 0 % en el simulador. Se debe a que los riesgos de las respuestas poco observadas están mal medidos (M14), y una política que apura el riesgo hasta 4 las paga. En el juego real conviene **más margen de riesgo** del que pide el simulador.


## Relevo (27 oct, ~02:40 UTC)

**1. Qué se ha hecho y por qué.**
- Los datos del Mac no estaban en la nube, así que se regeneraron. Lotes:

  | Lote | Partidas | Para qué |
  |---|---:|---|
  | b00 | ~9.700 | al azar |
  | b01 | 571 | oráculo con un 15 % al azar |
  | c01 | 300 | política voraz del simulador, en el juego real |
  | c02 | 162 | planificador ajustado, en el juego real |
  | v02 | 600 | validación |

- Se fijaron las reglas exactas M1–M17 y se escribió `replica.py`, el simulador completo, con el validador y el modo generativo. También `planner.py` (planificador), `replica_bot.py` (adaptador al juego real), `riskseq.py` (riesgo) y `gzrobust.py` (lector tolerante a gzip cortados).
- El objetivo de Alejandro era recrear el juego y validarlo en un lote nuevo. Está cumplido (tabla de M14).

**2. Resultados clave.**
- El juego es **determinista salvo el sorteo de eventos**. El riesgo oculto es el comentario de RR. HH. y explota exactamente al llegar a 5.
- Se puede llegar a L7 (umbral de Skill de 164–167), pero sólo en ~0,5 % de las partidas.
- **El planificador ajustado en el simulador saca 70,5 en el juego real**, el mejor bot hasta ahora.

**3. Lo que falló.**
- El primer lote de validación (v01) se corrompió porque se lanzó dos veces sobre los mismos archivos; se repitió como v02.
- El reinicio del contenedor cortó c02 en 162 partidas.

**4. Siguiente paso.**
1. Medir mejor el riesgo de las respuestas poco observadas, con más exploración dirigida.
2. Planificador con más profundidad (MCTS en el simulador) y búsqueda de una política para L7.
3. **Traducir a la Skill sólo principios generales**:
   - el contador de riesgo es el comentario de RR. HH. y nunca debe llegar a "angry" más una respuesta arriesgada;
   - cumplir los umbrales antes de cada evaluación;
   - guardar Skill desde L4;
   - limpieza final;
   - en niveles altos, las respuestas que cuestan dinero cuestan el doble o el triple.

   Nada de números ni de eventos.

Comandos en M14. Los datos están en `/home/user/bbdata/` de este contenedor y no están en Git; si el contenedor se pierde, se regeneran con `run.py`.
