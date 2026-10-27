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
