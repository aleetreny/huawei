# 07. El camino a L6: dónde se pierde el tiempo y qué regla ayuda

**Conclusión: llegar a L6 vale +7 puntos por partida, pero se llega tarde a L5 (mes ~43) porque se pasan 17–18 meses en L4 ganando Skill casi sólo con historias. La única regla de manual que ayuda es poner Skill learning y Apply for rotation en el trimestre a partir de L4, sin condiciones (+0,6 de nota y L6 del 1 % al 5 % con lectura de Haiku). Empezar en L3 empeora.**

28 oct, 10:40–11:40 UTC. Sólo la réplica de la línea Motor: sin cuota y sin DeepSeek. 2.000 partidas por brazo con las mismas semillas.

## Montaje

- Historias con las reglas de `t13-read-v4` (el `TrapBot` de [06](06-trampa-l1.md)), con lectura perfecta o de Haiku (dos pasadas de `plain`).
- Sólo cambia el trimestre ([l6.py](../../../scripts/stat-perception/l6.py)):
  - **blind:** DeepSeek tal como juega: informe, Network y proyecto clave, sin Skill learning. La línea 5 de v4, "Skill cuando Network y Output están en Stalled", no se activa nunca porque DeepSeek no rellena Stalled (0 de 160 notas, [mejora-nota.md](../deepseek/mejora-nota.md)).
  - **sk\<L\>[r]:** a partir del nivel L, Skill learning primero y un punto en Network u Output; acción principal proyecto clave o, con `r`, Apply for rotation.
  - **ref:** el trimestre del bot de 7 reglas, que conoce los techos. Es la referencia.
- **Corrección de un dato:** para pasar de L5 a L6 hacen falta **Skill 130**, Network 45 y Output 32 en una evaluación (`THRESH[5]` de la réplica). Los 170 de Skill son para L7. La partida de 76,87 llegó a L6 con Skill 147.

## Dónde se pierde el tiempo

**Mes medio de cada ascenso** (lectura perfecta, 300 partidas):

| | L2 | L3 | L4 | L5 | L6 (llegan) |
|---|---:|---:|---:|---:|---:|
| v4 (blind) | 7 | 15 | 25 | **43** | 48 (7 %) |
| Oráculo (7 reglas, efectos exactos) | 7 | 13 | **21** | 38 | 47 (55 %) |

- **18 meses en L4.** Las evaluaciones de L4 fallan por Skill (502 veces, frente a 116 por Network): hay que pasar de ≤42 (el techo de L3) a 90.
- **El Skill de L4 sale de las historias:** 39 de los 44 puntos ganados con v4, y 46 de 56 con el oráculo.
- **El oráculo también pasa ~17 meses en L4, pero llega 4 meses antes**: tarda menos en L2 y L3, cuyas evaluaciones fallan sobre todo por Network. Llega a L5 en el mes 38 y tiene dos evaluaciones para L6.

**Lo que vale L6:** las partidas completas acaban con una media de 57,2 en L4, 66,2 en L5 y **73,1 en L6**: +7 puntos por partida que llega a L6.

## Lo que se probó

**Lectura perfecta:**

| Trimestre / regla | Nota | Llega a L6 | Llega a L5 en el mes |
|---|---:|---:|---:|
| blind (v4 hoy) | 55,7 | 5,9 % | 43,1 |
| + Network primero en L3 (mantenimiento y Build a mentorship) | 55,0 | 4,0 % | 43,7 |
| + historias: una opción segura que suba Skill, desde L4 (o L3) | 55,7 | 6,0–6,3 % | 43,1 |
| sk4r + las dos anteriores | 55,7 | **9,9 %** | 42,4 |
| ref | 57,6 | 13,5 % | 41,8 |

**Lectura de Haiku:**

| Trimestre | Nota | Llega a L6 | Llega a L5 | Skill al final (completas) |
|---|---:|---:|---:|---:|
| blind (v4 hoy) | 49,7 | 1,2 % | 48,4 % | 105 |
| sk4 | 50,0 | 4,0 % | 51,8 % | 110 |
| **sk4r** | **50,3** | **4,9 %** | 51,3 % | **115** |
| sk3r | 47,9 | 1,6 % | 37,5 % | 101 |
| ref | 51,4 | 4,7 % | 54,4 % | 112 |

Error típico de cada nota: ~0,4.

## Lectura

- **Skill learning y rotation en el trimestre a partir de L4 es la única regla que ayuda:**
  - +0,6 de nota con lectura de Haiku;
  - L6 del 1 % al 5 %;
  - un 3 % más de partidas en L5;
  - +10 de Skill al final.

  Es una regla de trimestre, que es lo que mejor obedece DeepSeek: en el banco de la línea DeepSeek, "Skill en L4" pasa del 2 % al 65 % con t13-final ([obediencia.md](../deepseek/obediencia.md)).
- **Tiene que ser a partir de L4, no de L3:** en L3 hace falta Network para ascender, y empezar antes cuesta 1,8 puntos.
- **Las reglas de historias para Skill no cambian nada** con lectura perfecta: el bot ya coge Skill cuando la ve. La prioridad de Network en L3 empeora.
- **Llegar a L6 de forma fiable no está al alcance de una regla.** El oráculo llega en el 55 % porque llega a L4 cuatro meses antes, y eso depende de elegir mejor las historias (percepción y riesgo exactos), no del trimestre.

## Para el manual

En `t13-read-v4`, la línea 5 del trimestre ("Network y Output en Stalled → Skill learning y rotation") depende de un registro que DeepSeek no rellena, así que no se aplica nunca. **Propuesta: volver a la condición visible de `t13-final`** (su línea 5): "L4 or above: Skill learning (2 Energy) plus one point on the weakest of Health, Dignity or Network; main action Apply for rotation", detrás de las líneas de salud y de RR. HH.

Ganancia esperada pequeña (+0,3 a +0,6 por partida en la réplica), pero es un cambio de una línea, de trimestre y fácil de obedecer.

Una advertencia: en el banco de la línea DeepSeek, las decisiones de "Skill en L4" con t13-final pierden algo más por decisión que sin manual (0,12 → 0,22; +0,10, con un intervalo que incluye el 0). Ese banco mide la pérdida de cada decisión suelta; la réplica mide la carrera entera, donde la ganancia está en llegar antes a L5. Antes de entregarlo habría que comprobar en el banco de DeepSeek que no se cuela en las historias.

## Límites

- El bot no es DeepSeek: con lectura de Haiku las notas absolutas son ~50, no los ~70 de las partidas reales. Las conclusiones son comparaciones con las mismas semillas.
- La réplica no conoce los techos por nivel de forma distinta a la del juego dev. Si la evaluación oficial cambia los parámetros, la condición "L4 or above" sigue siendo visible.

Datos: [l6.json](l6.json).
