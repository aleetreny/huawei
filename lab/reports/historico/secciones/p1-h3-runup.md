# P1, ronda 3: reloj frente a reloj + respuestas discretas (`review-run-up`)

**Hipótesis (profundizar H-P1a).** Qué cambia: un solo Skill que junta el reloj de evaluación con alternativas discretas y honestas a las posturas firmes en público (en privado, por escrito después, preguntar, abstenerse, ayudar una vez y fijar un límite). Por qué: tras el reloj, las pérdidas que quedaban eran de ese tipo. Medida: ascenso en la 1.ª evaluación.

**Diseño.** 25 partidas cortas (6 meses) por brazo, intercaladas, 27 oct 02:10–05:08 UTC (intercaladas a su vez con la prueba final), lote [`batches/p1-h3-runup.json`](batches/p1-h3-runup.json).

## Resultado

| Brazo | Partidas | Ascienden en la 1.ª (IC 95 %) | Pérdidas en el mes 5 / en el 4 |
|---|---:|---:|---:|
| f3-lean-v1 (referencia) | 24 | 12 = 50 % (31–69) | 9 / 5 |
| + review-clock (`f3-lean-clock-v2`) | 24 | 9 = 38 % (21–57) | 14 / 2 |
| + review-run-up (`f3-lean-runup-v1`) | 24 | 11 = 46 % (28–65) | 12 / 2 |

**El reloj, en las tres rondas sobre f3-lean** (cada una con su referencia intercalada):

| Ronda | Referencia | Reloj |
|---|---:|---:|
| 1 | 9/24 | 12/25 |
| 2 | 10/25 | 15/25 |
| 3 | 12/24 | 9/24 |
| **Total** | **31/73 = 42 %** | **36/74 = 49 %** |

- La ventaja de las dos primeras rondas **no se repite**: en la tercera el reloj va por debajo, y la bajada de las pérdidas del mes 5 tampoco se repite (14 frente a 9). En total, +7 puntos con un error típico de unos 8: indistinguible de cero.
- Juntarlo con las respuestas discretas (`review-run-up`) tampoco gana (46 % frente a 50 %).

## Decisión

**H-P1a descartada como palanca del P1** (no se confirma con 74 partidas). Se mantiene en el manual compuesto sólo porque no empeora, ordena las notas y es la parte del manual que da el calendario (la rúbrica pide mirar a los 48 meses). Lección: el ascenso de la 1.ª evaluación depende de unas pocas respuestas del mes 5 que ni el calendario ni las reglas generales de tono consiguen cambiar en Haiku; dos lotes de 25 a favor fueron suerte.
