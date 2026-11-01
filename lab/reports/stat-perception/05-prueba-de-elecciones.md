# 05. ¿Cambia la línea de Output lo que elige Haiku antes de una evaluación?

**Conclusión: no. Con la línea de percepción en la referencia del mes previo (t13-perc), Haiku no elige mejor que con t13-final; en el banco tiende a peor (pierde un punto necesario en el 30 % de las situaciones frente al 18 %) y cambia el 10 % de las historias de otros meses.**

27 oct, 16:15–16:45 UTC. Banco de obediencia de Transmisión (`lab/data/transmision/`), forma oficial de entrega del Skill (`scripts/transmision/runbench.py`), Haiku por el CLI 2.1.295 en la cuenta Pro de Leah. 164 situaciones; la ventana de 5 horas pasó del 34 % al 42 %.

## Qué se probó

`t13-final` (el manual recomendado de Transmisión) marca en su `reference/review-month.md`, que sólo se lee con `Review in 1`, que una opción "que quita tiempo a tu entrega (trabajo extra, investigaciones, rehacer, el camino lento…)" puede costar Output. Es justo la lectura de Output como "tiempo gastado" que falla al etiquetar ([03](03-errores-output.md)).

**t13-perc** ([lab/policies-src/stat-perception/t13-perc/](../../policies-src/stat-perception/t13-perc/)) es t13-final con un único cambio en esa referencia:
- añade "considera qué hace cada opción a cada uno de Skill, Network, Output, Health y Dignity";
- cambia la marca de Output: desentenderse, callar, tragar, esquivar, pasar tu trabajo a otro, pedir menos carga, descansar en vez de trabajar o quemarse "puede costar Output"; una charla corta, una revisión o un poco de ayuda no.

El lint no da errores, con los mismos avisos que t13-final.

## Cómo se midió

| Bloque | Situaciones | Brazos |
|---|---:|---|
| Mes previo a la evaluación (`pre_review` del conjunto A) | 69 (60 puntuables) | t13-perc frente a las respuestas guardadas de Alejandro con `t13-final` y sin manual (`control`) |
| Comprobación de versión del CLI | 25 de las anteriores | t13-final jugado de nuevo aquí (CLI 2.1.295; las de Alejandro son de 2.1.303) |
| Bloque general (otros meses, contaminación) | 70 del conjunto G1 | t13-perc frente a t13-final y control |

Puntuado con `scripts/transmision/score.py` y `fingerprint.py` de Alejandro. Las tablas completas están en [choice-test.out](choice-test.out), y las elecciones (sólo identificadores) en [choice-test-answers.json](choice-test-answers.json).

## Resultados

**Mes previo a la evaluación (60 situaciones puntuables, las mismas para los tres):**

| Brazo | Acierto (IC 95 %) | Pierde un punto necesario | Nota perdida por decisión |
|---|---|---:|---:|
| Sin manual | 62 % (49–73) | 28 % | 2,20 |
| **t13-final** | **67 % (54–77)** | **18 %** | **1,70** |
| t13-perc | 63 % (51–74) | 30 % | 2,28 |

**La versión del CLI no lo explica.** En 25 situaciones, t13-final jugado aquí coincide con el de Alejandro en 22 (88 %). t13-perc difiere de ese t13-final local en 3 de 25, tanto como repetir el mismo manual. En las 19 puntuables de ese subconjunto:
- t13-final de Alejandro: 11 % de puntos perdidos;
- t13-final local: 16 %;
- t13-perc: 26 %.

**Otros meses (70 historias):**
- t13-perc cambia el 10 % de las elecciones respecto a t13-final, justo en el umbral de alarma de Transmisión (1 de cada 10).
- No las empeora: acierta el 77 % frente al 74 %, y pierde 0,56 puntos por decisión frente a 0,82.
- Lleva menos Output: +0,04 por historia frente a +0,14.

## Lectura

- **Percibir mejor no es elegir mejor.** La misma idea que mejora el etiquetado (considerar los 5 indicadores y "desentenderse cuesta Output") no ayuda cuando Haiku elige con el manual delante.
- **La marca "tiempo de tu entrega" de t13-final es inexacta como descripción del juego, pero funciona como regla de elección.** Una explicación posible: en el mes previo a una evaluación lo que importa es no perder un punto, y desconfiar de las opciones que cuestan tiempo es una aproximación prudente.
- Con 60 situaciones los intervalos se solapan: "peor" no está demostrado. "Mejor" queda descartado con lo que hay.
- **Para el manual: se queda la redacción de t13-final.** La línea de percepción no entra en la referencia del mes previo.

## Límites

- Una sola pasada por brazo. El ruido de repetición del propio banco es de un 4–12 % de elecciones distintas (control frente a control-b de Transmisión: 96 % iguales; t13-final aquí frente a Alejandro: 88 %).
- Haiku hace de DeepSeek, y DeepSeek podría reaccionar distinto. La línea DeepSeek de Alejandro lo puede comprobar con su arnés.

Script para repetirlo: [scripts/stat-perception/run-choice.sh](../../../scripts/stat-perception/run-choice.sh).
