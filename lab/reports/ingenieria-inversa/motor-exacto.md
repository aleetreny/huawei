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

**Los datos están en el repo privado:** partidas, catálogo, riesgo, modelos y scripts de análisis, en [`lab/data/ingenieria-inversa/`](../../data/ingenieria-inversa/README.md). Para usarlos, `export BB_DATA=$PWD/lab/data/ingenieria-inversa`. Llevan texto del juego de desarrollo: son para estudiar y no se copian a un manual.

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


## Fase 3 (27 oct, 09:40–10:50 UTC): parte alta, sorteo, política óptima y reglas generales

**Lotes nuevos, todos de bots y sin cuota de Claude** (datos en `lab/data/ingenieria-inversa/`):

| Lote | Partidas | Para qué |
|---|---:|---|
| `h01-l6hunt` | 400 | planificador ajustado para llegar a L6 en el mes 42 |
| `v03-validation` | 600 | validación nueva |
| `d01-planner2` | 400 | 2 brazos de la nueva política |
| `d02-planner2b` | 160 | más partidas del brazo 1 |

### Tabla final

| Punto | Resultado | Datos |
|---|---|---|
| **(a) Nota S** | **Descartada en 48 meses.** Ninguna S en **24.525 evaluaciones**. Cada nivel tiene una nota máxima:<br>• L1: C (9.913 C, 152 D)<br>• L2 y L3: B<br>• L4 y L5: A (4.346 A)<br>• L6: A en 4 de 243 casos, todas con Network de 69–71, cerca de su techo<br>Ni con todo en el techo, Dignity 10 y riesgo 0 se pasa de esa nota (M19). La S exigiría el techo de L6 o un nivel superior, inalcanzable en 48 meses (punto b) | 24.525 evaluaciones de 7 lotes |
| **(b) Umbral de L6 → L7** | Skill **169–170** (estado justo antes de la evaluación):<br>• ascienden con 170 y 175<br>• no ascienden con 168/65/50 ni con 168/64/51<br>Network ≤ 65 y Output ≤ 48 no frenan; los umbrales exactos de esos dos no se pueden medir. Techos de L6 vistos: Skill ≥ 175, Network ≥ 72, Output ≥ 54 | **243 evaluaciones de L6** (87 de `h01`); 2 ascensos a L7 |
| **(b) L8–L10** | **No alcanzables.** El primer ascenso posible a L7 es en el mes 48:<br>• L5 no puede llegar antes del 30: desde el techo de L3 (42 en el mes 18), 6 meses a ~4,3 no llegan a 90<br>• por la misma razón, L6 no llega antes del 42<br>• en el mes 47 se llega como mucho a ~167 de Skill, justo el umbral<br>L8 exigiría L7 en el mes 42, es decir, 130 de Skill en el mes 35, y el máximo es ~115. **Nota máxima por nivel final** (resto al máximo, sueldo y bonus del mejor calendario): **L5 75,8 · L6 79,6 · L7 82,6** | M9, M16 y cálculo del presupuesto de Skill |
| **(c) Validación del simulador** | En **600 partidas nuevas** (`v03`), con el catálogo construido sin ellas:<br>• **99,3 % de pasos exactos** (eventos 99,2 %, energía 100 %, acción principal 97,6 %)<br>• **99,5 % de ascensos**<br>• **error medio de la nota final de 0,33 puntos**<br>**Sorteo real frente a generado** (misma política, 362 partidas terminadas por lado):<br>• frecuencia por título y partida: correlación **0,961**, diferencia media 0,029<br>• 99,0 frente a 98,2 títulos distintos por partida<br>• reparto por bloques de desbloqueo igual semestre a semestre (abajo) | `validation_v03.txt`, `analisis/cmpdraw.py` |
| **(d) Política óptima** | **72,39 ± 0,51 en 360 partidas reales** (mediana 74,9, máximo 80,8). 72 % terminan en L6; 2 crisis de confianza, 5 ruinas y 7 despidos. Antes: 70,5 | `d01` brazo 1 + `d02`; parámetros en `politica_optima.json` |
| **(e) Reglas generales** | 7 reglas sin números ni eventos; 88–89 % de acuerdo con la política óptima en las dos mitades de títulos. Aportación de cada una con parámetros cambiados un 20 %: ver M23 | `analisis/rulestest.py`, `rules_scen.log` |

### M18. El sorteo de eventos: bloques por mes, no por nivel

- **Los eventos se desbloquean al empezar cada semestre, sea cual sea el nivel:**

  | Mes | Títulos nuevos |
  |---:|---:|
  | 1 | 64 |
  | 6 | 25 |
  | 12 | 37 |
  | 18 | 13 |
  | 24 | 23 |
  | 30 | 6 |

  En total son 168.
  - Prueba: desde el semestre 3, la proporción de eventos tardíos es igual en L1, L2, L3 y L4 (0,25 en todos).
  - **No hay eventos exclusivos de niveles altos.**
  - Tampoco hay eventos que dependan de la salud, el dinero, el riesgo, la dignidad o el tiempo en el nivel: desviaciones ≤ 0,15 una vez fijado el mes.
- **El sorteo es casi uniforme** entre los títulos desbloqueados y no usados (no se repiten).
  - Las historias que pasan al mes siguiente pesan ~0,6, frente a ~1,1 de las de un solo paso (correlación peso–duración de −0,61): no puede haber dos historias largas abiertas a la vez.
- Reparto real frente a generado (proporción de títulos de cada bloque en cada semestre, real/simulado):

  | Semestre | Bloque 1 | Bloque 6 | Bloque 12 | Bloque 18 | Bloque 24 | Bloque 30 |
  |---|---|---|---|---|---|---|
  | S2 | 0,66/0,64 | 0,29/0,30 | 0,04/0,06 | – | – | – |
  | S4 | 0,37/0,38 | 0,19/0,18 | 0,30/0,29 | 0,12/0,12 | 0,02/0,03 | – |
  | S6 | 0,28/0,30 | 0,15/0,15 | 0,24/0,24 | 0,09/0,09 | 0,18/0,18 | 0,05/0,05 |
  | S8 | 0,30/0,29 | 0,15/0,15 | 0,23/0,24 | 0,09/0,10 | 0,18/0,17 | 0,05/0,04 |

### M19. Huevos de Pascua: lo que hay y lo que no

- **Nota máxima por nivel.** Con Skill, Network y Output en el techo, Dignity 10 y riesgo 0:

  | Nivel | Nota máxima |
  |---|---|
  | L1 | C |
  | L2–L3 | B |
  | L4–L5 | A |

  La nota mide el rendimiento frente a lo que se espera del nivel. **No hay S en 24.525 evaluaciones.**
- **Ningún ascenso fuera de la evaluación** (10.659 de 10.659 en una evaluación) y ninguna bajada de nivel. No hay atajos.
- **Mayores efectos de una sola respuesta** (suma de |efecto|): 11, en "Volunteer for the incident team" (Network +3, Skill +2, Health −3, Output −2, Dignity +1). Las historias que más Skill dan en total: 12 y 11 puntos.
- **Skill al mes:** en algún mes suelto se ganan hasta 11 puntos, pero el ritmo sostenido máximo sigue siendo ~4,3 al mes. Ninguna vía permite ascender más deprisa.

### M20. Correcciones del simulador en esta fase

1. **Dinero.** Se sigue un intervalo del dinero real compatible con todos los valores vistos; el juego muestra el dinero redondeado hacia abajo y lo guarda con 1 decimal.
2. **Dignity en la evaluación.** Primero el +1 de la charla neutra (o el +2 de la de elogio), hasta 10. Después el −1 de "too fast".
3. **Charla de elogio:** Network +1, antes de restar el coste del ascenso.
4. **"Too fast" en todos los niveles:** Network −3. Coste base del ascenso de L6: −4.
5. **Umbral de L6** con Skill 170.
6. **Sorteo por bloques de mes** (M18).
7. **Catálogo v2** construido con 11.732 partidas (b00, b01, c01, c02, v02 y h01). El riesgo encaja exactamente en el 89 % de esas partidas.

Lo que sigue fallando, por orden de peso:
- dinero ±1 cuando el intervalo cruza un entero;
- nota A frente a B (un modelo de árbol con riesgo y medias acierta el 88 %; queda una parte oculta);
- acción principal (97,6 %).

### M21. La política óptima y qué hace en cada etapa

Búsqueda de pesos del planificador:
- primero 150 configuraciones × 250 partidas con semillas comunes en el simulador;
- después, las 8 mejores con 1.000 partidas nuevas;
- por último, las 2 mejores en el juego real.

La mejora por simulación ("rollouts") **no mejoró** al planificador: −0,27 ± 1,48 en 40 partidas emparejadas, porque el ruido del sorteo de eventos tapa las diferencias.

Pesos ganadores (`politica_optima.json`):
- mucho peso a cumplir los umbrales;
- protección fuerte en el mes previo a la evaluación;
- tope de riesgo de 2–3;
- **Defuse desde riesgo 2 y Lay low desde 3**;
- limpieza final a partir del mes 46.

**Qué hace en cada momento** (360 partidas reales):

| Semestre | Riesgo medio | Nivel antes de evaluar | S / N / O en el mes 5 del semestre | Energía más usada | Acción principal |
|---|---:|---|---|---|---|
| 1 | 0,3 | L1 | 9 / 3 / 3 (techo) | Health recovery, Report | Lay low, Rotation |
| 2 | 0,4 | L2 (83 %) | 19 / 6 / 5 | Report, Health | Lay low, Key project |
| 3 | 0,5 | L3 (79 %) | 35 / 16 / 13 | Report, Network | Key project |
| 4 | 0,5 | L4 (66 %) | 52 / 26 / 20 | Report, Network | Rotation |
| 5 | 0,4 | L4 | 75 / 33 / 24 | Health, Skill learning | Rotation |
| 6 | 0,35 | L4 → L5 | 98 / 38 / 27 | Report, Skill learning | Rotation |
| 7 | 0,4 | L5 | 120 / 45 / 32 | Report, Skill learning | Rotation |
| 8 | 0,4 | L5 → L6 | 142 / 53 / 38 | Health, limpieza | Lay low |

**Valor de cada respuesta en nota final esperada.** En 229 puntos de decisión, cada respuesta se valoró con 24 continuaciones de la política. La tabla completa (609 respuestas) está en `answer_values.csv`; es investigación y nunca va a una Skill.
- La política elige la mejor en el **73 %** de los casos, con una pérdida media de **0,16 puntos** por decisión, en buena parte ruido.
- Lo que cuesta elegir mal, según el riesgo de la respuesta:

  | Riesgo de la respuesta | Pérdida media |
  |---|---:|
  | −1 | 0,08 |
  | 0 | 0,43 |
  | +1 | 0,52 |
  | +2 | 1,07 |
  | +3 | 3,39 |

### M22. Reglas generales (sin números ni eventos)

Un bot que sólo ve:
- el efecto anunciado de cada opción;
- el **signo** de su riesgo (arriesgada o prudente), no la cantidad;
- el comentario de RR. HH.;
- el techo visible del nivel.

No conoce los umbrales. Juega con 7 reglas (`rules.py`):

| Regla | Enunciado general |
|---|---|
| R1 | Mantén tranquilo el comentario de RR. HH. Si deja de estarlo, rechaza las opciones arriesgadas y usa el trimestre para bajar el riesgo |
| R2 | En el mes previo a una evaluación, no cedas ni un punto de Skill, Network u Output |
| R3 | Haz crecer primero el indicador más lejos de su techo visible. Lo que pasa del techo no vale nada |
| R4 | Cuando Network y Output estén en su techo, todo a Skill |
| R5 | En el último trimestre, riesgo a cero y salud y dignidad al máximo |
| R6 | En niveles altos, evita las opciones que cuestan dinero |
| R7 | Que la salud nunca baje cerca de cero; recupera en el trimestre |

- Saca **68,1** en el simulador. El planificador, que lo sabe todo, saca ~73.
- **Prueba con títulos reservados.** Coincide con las decisiones del planificador en el **88,9 %** y el **88,1 %** de las dos mitades de títulos sorteadas al azar. Las reglas no dependen de qué eventos salgan.

### M23. ¿Aguantan las reglas si cambian los parámetros? (300 partidas por celda)

Diferencia de nota al quitar cada regla (negativo = la regla ayuda):

| Escenario | Con todas | −R1 riesgo | −R2 mes previo | −R3 techo | −R4 Skill | −R5 final | −R6 dinero | −R7 salud | Sin reglas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base | 68,1 | −45,8 | −2,6 | −7,3 | +0,6 | −2,2 | −0,5 | −12,6 | 19,2 |
| Techos −20 % | 22,7* | −6,5 | +0,7 | −1,6 | +0,1 | 0,0 | 0,0 | −0,3 | 14,9 |
| Techos +20 % | 74,3 | −50,9 | +0,5 | −2,5 | 0,0 | −2,6 | −0,6 | −22,2 | 20,8 |
| Umbrales −20 % | 78,1 | −54,4 | +0,7 | −2,3 | −0,2 | −2,9 | −0,7 | −18,7 | 20,6 |
| Umbrales +20 % | 23,3* | −7,0 | +0,6 | −1,8 | +0,1 | 0,0 | 0,0 | −0,3 | 15,2 |
| Sorteo alterado | 68,0 | −45,0 | −4,8 | −4,4 | +0,2 | −2,1 | −0,3 | −12,6 | 18,7 |
| Explota con 4 | 60,2 | −40,2 | −0,9 | −6,4 | +1,0 | −1,7 | −0,3 | −10,0 | 17,5 |
| Explota con 6 | 69,9 | −45,4 | −3,0 | −7,1 | +0,4 | −2,1 | −0,4 | −13,2 | 20,4 |

\* Con los techos por debajo de los umbrales nadie puede ascender, y todas las políticas acaban despedidas en el mes 24.

**Veredicto:**
- **Aguantan en todos los escenarios: R1 (riesgo), R7 (salud), R3 (techo) y R5 (limpieza final).** R1 vale 40–54 puntos.
- **R2 (mes previo)** ayuda cuando el juego es el de dev o el sorteo cambia (−2,6 y −4,8), pero estorba un poco cuando los umbrales o los techos se mueven (+0,5 a +0,7). Conviene formularla como "no cedas lo que te hace falta para la evaluación", no como "nunca cedas nada".
- **R6 (dinero)** aporta poco pero nunca resta.
- **R4 ("todo a Skill"), tal como está escrita, no ayuda** (+0,6). El planificador sí gana guardando Skill desde L4, pero lo hace con los umbrales en la mano. Una regla sin números que lo capture está por encontrar.

## Relevo (27 oct, 10:50 UTC)

**1. Qué se ha hecho.** La Fase 3 completa (tabla final arriba):
- **(a) Nota S:** descartada, con 24.525 evaluaciones.
- **(b) Umbral de L6 → L7:** Skill 169–170, con 243 evaluaciones de L6. L8–L10 no son alcanzables.
- **(c) Simulador:** 99,3 % en 600 partidas nuevas y sorteo real frente a generado reproducido.
- **(d) Política óptima:** 72,39 en 360 partidas reales.
- **(e) Reglas generales:** 7, probadas con parámetros alterados un 20 %.

**2. Dónde está todo.**
- Código en `scripts/ingenieria-inversa/`:
  - `replica.py`: simulador;
  - `game.py`: partida paso a paso y mejora por simulación;
  - `planner.py`: planificador;
  - `rules.py`: bot de reglas generales;
  - `replica_bot.py`: adaptador al juego real.
- Datos y artefactos en `lab/data/ingenieria-inversa/`: `catalog_v2.json`, `riskd_v2.json`, `sampler_v1.json`, `politica_optima.json`, `answer_values.csv`, `validation_v03.txt`, `rules_scen.log` y los lotes.

**3. Lo que falló o quedó a medias.**
- La mejora por simulación no superó al planificador; haría falta mucho más cómputo por decisión.
- R4 ("todo a Skill") no se ha conseguido formular sin números de forma que ayude.
- Los umbrales exactos de Network y Output de L6 → L7 no se pueden medir: casi nadie llega a la Skill necesaria.

**4. Siguiente paso.** Llevar a una Skill sólo R1, R7, R3, R5 y R2 (en su forma "no cedas lo que necesitas para la evaluación") y R6, sin números ni eventos, y jugarla con Haiku o DeepSeek. Comandos:

```bash
export BB_DATA=$PWD/lab/data/ingenieria-inversa
python3 scripts/ingenieria-inversa/replica.py validate --catalog $BB_DATA/catalog_v2.json --batches v03-validation
python3 lab/data/ingenieria-inversa/analisis/rulestest.py base,thr+20 300 2
```

**5. Línea de ESTADO.md:** actualizada (fase 3).
