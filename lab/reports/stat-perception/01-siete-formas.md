# 01. Siete formas de pedir a Haiku qué indicador mueve cada respuesta

**Conclusión: pedir dirección en los 5 indicadores de cada opción sube la réplica de 49,1 a 53,3, y votar 5 formas de leer a 54,4 (sólo la categoría saca 46,7; las etiquetas perfectas, 58,1).**

27 oct, 15:15–15:50 UTC. Haiku por el CLI de Claude (`--model haiku`, sin herramientas), cuenta Pro de Leah: 147 llamadas, 1,6 M fichas, 0,62 USD a precio de lista.

## Método

- **Datos.** Las 936 respuestas de dev con su efecto exacto y su categoría: `answers.json`, construido con `scripts/question-bank/build_answers.py` desde la rama `main-1nddsg`. Lleva texto del juego y se queda fuera de Git.
- **Prueba justa.**
  - Antes de escribir ninguna instrucción, los eventos se partieron en dos mitades por título ([split.json](split.json)): 186 preguntas de diseño y 217 reservadas.
  - Sólo se miró la mitad de diseño para escribir los significados.
  - El acierto se da sobre la mitad reservada.
- **Etiquetado.**
  - Haiku ve una pregunta cada vez: la descripción del evento y las opciones, nunca los efectos.
  - Para cada opción da −1, 0 o +1 en Skill, Network, Output, Health y Dignity.
  - Va en lotes de 20 preguntas ([label.py](../../../scripts/stat-perception/label.py)).
- **Acierto** ([evaluate.py](../../../scripts/stat-perception/evaluate.py)): recall y precisión de subida y bajada por indicador, y **orden por pares**. El orden por pares mira, dentro de una pregunta, dos opciones cuyo efecto real en un indicador es distinto, y comprueba si las etiquetas las ordenan igual, que es lo que necesita una elección.
- **Valor** ([replica_eval.py](../../../scripts/stat-perception/replica_eval.py)):
  - sigue la lógica de `catbot.py` de Categorías: energía y acción principal con las 7 reglas del bot;
  - cada opción de historia se valora con el efecto medio de su categoría, corregido por las etiquetas;
  - el riesgo se juzga por la categoría, como lo haría un lector;
  - 1.000 partidas por brazo con las mismas semillas, así que las diferencias son pareadas.

## Las formas

| Forma | Qué se le dice a Haiku |
|---|---|
| plain | Nada sobre los indicadores; sólo dar dirección a los 5 en cada opción |
| defs | Un significado corto de cada indicador en este juego, escrito con la mitad de diseño. Skill = resolverlo de forma profesional (asumir, documentar, cuantificar, poner un proceso, enseñar, mantener la calidad); Output = la entrega propia; Network = la buena voluntad de las personas implicadas; Health; Dignity |
| cues | Los mismos significados como lista de pistas concretas |
| contrast | Significados, más comparar primero las opciones de la pregunta (cambian un indicador por otro) |
| reason | Significados, más hasta 12 palabras sobre qué gasta y qué gana la opción antes de las señales |
| trade | Significados, más UN indicador que se gana y UNO que se paga por opción |
| defs2 | defs con Output redefinido como impulso visible, "incluso venderte" ([03](03-errores-output.md)) |

Votaciones sin llamadas nuevas ([combine.py](../../../scripts/stat-perception/combine.py)): **vote5** = plain, defs, cues, contrast y reason; **vote5b** = lo mismo con defs2 en lugar de defs. Por indicador gana la señal más repetida, y los empates dan 0.

## Acierto en la mitad reservada

| Etiquetas | Acierto | Orden por pares | Skill: subidas detectadas | Output: orden por pares |
|---|---:|---:|---:|---:|
| prior (señal mayoritaria de la categoría, sin Haiku) | 0,640 | 0,700 | 0,64 | 0,50 |
| Etiquetas de Categorías | 0,723 | 0,731 | 0,30 | 0,71 |
| **plain** | **0,727** | **0,807** | 0,55 | **0,80** |
| defs | 0,684 | 0,793 | 0,73 | 0,72 |
| cues | 0,678 | 0,779 | 0,65 | 0,74 |
| contrast | 0,675 | 0,803 | 0,78 | 0,72 |
| reason | 0,670 | 0,802 | **0,79** | 0,74 |
| trade | 0,657 | 0,711 | 0,49 | 0,64 |
| vote5b | 0,703 | 0,803 | 0,73 | 0,77 |

## Valor en la réplica (1.000 partidas por brazo, mismas semillas)

| Percepción de las historias | Nota | Frente a sólo categoría | L6+ | Despidos | Crisis de confianza |
|---|---:|---:|---:|---:|---:|
| Oráculo (efectos y riesgo exactos) | 67,7 | — | 51 % | 66 | 34 |
| Categoría + señales perfectas | 58,1 | +11,4 ± 0,7 | 24 % | 101 | 215 |
| **vote5b** | **54,4** | **+7,7 ± 0,8** | 7 % | 203 | 81 |
| vote5 | 54,2 | +7,6 ± 0,8 | 5 % | 207 | 74 |
| reason | 53,5 | +6,8 ± 0,8 | 6 % | 219 | 92 |
| **plain** | 53,3 | +6,6 ± 0,7 | 8 % | 181 | 136 |
| defs | 53,2 | +6,5 ± 0,8 | 4 % | 213 | **73** |
| contrast | 52,8 | +6,1 ± 0,8 | 6 % | 212 | 111 |
| cues | 52,0 | +5,3 ± 0,7 | 4 % | 242 | 85 |
| Etiquetas de Categorías | 49,1 | +2,4 ± 0,8 | 5 % | 208 | 152 |
| defs2 | 48,1 | +1,5 ± 0,7 | 5 % | 240 | 174 |
| Sólo categoría | 46,7 | 0 | 2 % | 295 | 132 |
| prior | 44,2 | −2,5 ± 0,6 | 2 % | 252 | 169 |
| trade | 39,7 | −7,0 ± 0,8 | 1 % | 250 | 305 |

## Lectura

- Las cinco formas que mantienen los 5 indicadores quedan a menos de 1,5 puntos entre sí; las diferencias entre ellas son pequeñas.
- Hay dos saltos claros:
  - de las etiquetas de Categorías, que nombran sólo el indicador evidente, a cualquier etiquetado completo: +3 a +4;
  - de una forma sola a la votación: +1.
- **Los significados reducen a la mitad las crisis de confianza** (defs: 73 frente a 136 de plain), porque hacen visibles los costes. plain, en cambio, tiene menos despidos.
- **Una lista de pistas funciona peor que un significado corto** (52,0 frente a 53,2).
- **"Una ganancia y un coste" tira información** y queda por debajo de sólo la categoría.

Datos completos: [eval.json](eval.json), [replica.json](replica.json).
