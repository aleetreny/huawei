# Percepción: qué ve DeepSeek en cada respuesta

**Conclusión.** DeepSeek ve bien el riesgo (detecta el 83 % de las respuestas que lo suben y el 90 % de las peligrosas) y los tipos de respuesta (mejor que Haiku), pero **se le escapa más de la mitad de lo que sube Skill y Output**. Equivocarse en los indicadores le cuesta unos 8 puntos en el simulador y equivocarse en el riesgo unos 4.

27 oct 2026, rama `alejandro/deepseek`. Script `scripts/deepseek/perceive.py`; prompt `scripts/deepseek/prompts/perceive-v1.md`.

## Qué se hizo

- A DeepSeek (`deepseek-v4-flash`, temperatura 0,95 como en JiuwenSwarm, razonamiento por defecto) se le enseña cada pregunta de historia **tal como sale en `observe`**: título, descripción y opciones numeradas. Una llamada por pregunta.
- El prompt v1 lleva sólo las definiciones de los indicadores del manual oficial y los 10 tipos de `scripts/question-bank/taxonomy.md`, sin pistas.
- Por cada opción pide: el tipo, el signo del efecto en Health, Dignity, Skill, Network, Output y Wealth (+, − o 0) y el signo del riesgo oculto.
- Se compara con el catálogo exacto (`catalog_v2.json`: efecto y paso de riesgo de cada respuesta).
- **Sólo títulos de diseño:** 289 preguntas y 669 respuestas. Los 50 títulos reservados del banco (114 preguntas) no se miran al diseñar.
- Dos repeticiones (r1, r2) para medir la estabilidad.
- Coste: 0,065 USD las dos pasadas (unos 0,0001 USD por pregunta).

## Resultados (r1; r2 sale casi igual)

Acierto por indicador. "Subidas vistas" es la parte de las respuestas que suben el indicador que DeepSeek marca con +; "falsas +" es la parte de las que no lo mueven que marca con +.

| Indicador | Suben | Subidas vistas | Bajan | Bajadas vistas | Falsas + | Falsas − | Haiku: subidas vistas | Haiku: bajadas vistas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Health | 43 | 72 % | 122 | 51 % | 6 % | 10 % | 63 % | 47 % |
| Dignity | 300 | 79 % | 178 | 79 % | 22 % | 30 % | 57 % | 64 % |
| **Skill** | 221 | **45 %** | 36 | 19 % | 1 % | 2 % | 24 % | 36 % |
| Network | 237 | 76 % | 197 | 61 % | 28 % | 15 % | 57 % | 70 % |
| **Output** | 148 | **49 %** | 93 | **34 %** | 7 % | 5 % | 47 % | 45 % |
| Wealth | 27 | 59 % | 22 | 45 % | 3 % | 2 % | 0 % | 0 % |

**Riesgo oculto:** ve el 83 % de las respuestas que lo suben (278), el **90 % de las de +2 o más**, y acierta el 74 % de las veces que avisa (21 % de falsas alarmas). Ve el 88 % de las que lo bajan. Acierto en "sube o no": 81 %. Con los 10 tipos de Haiku, el mismo acierto era del 78 %.

**Tipos:** coinciden con las etiquetas de Haiku en el 76 % de las respuestas y separan el riesgo igual de bien (FIX −0,11 de riesgo medio, OWN −0,35, HIDE +1,62, YIELD +1,00, ATTACK +1,09).

**Estabilidad** (misma respuesta en r1 y r2): tipo 85 %, riesgo 90 %, Health 88 %, Dignity 83 %, Skill 91 %, Network 81 %, Output 86 %, Wealth 96 %.

## Qué se le escapa (títulos de diseño)

- **Skill.** El juego da Skill a casi todo lo que exige pensar: analizar, aportar datos, preparar, sopesar una decisión, negociar con argumentos, enseñar con preguntas. DeepSeek sólo marca Skill cuando la opción es técnica o de aprender. 122 de las 221 subidas no las ve.
- **Output.** Baja cuando el tiempo se va en otra cosa que tu entrega: aprender, ayudar u organizar para otros, revisar su trabajo, pedir perdón y rehacer, parar una entrega. Sube al entregar o al centrarse en lo propio. DeepSeek ve una de cada tres bajadas.

## Lo que vale cada percepción en el simulador

Bot de 7 reglas (`scripts/deepseek/groupbot.py`, versión general de `catbot.py`) que elige las historias sólo con lo que ve de cada opción. 1.000 partidas con las mismas semillas. En los títulos reservados todos los brazos ven el efecto exacto, para que la diferencia salga sólo de los títulos de diseño.

| Lo que ve el bot | Nota |
|---|---:|
| Efecto y riesgo exactos (oráculo) | 67,7 |
| Signos perfectos de los 6 indicadores + signo perfecto del riesgo | 67,0 |
| Efecto exacto + aviso de riesgo de DeepSeek | 63,2 |
| Signos de DeepSeek + riesgo exacto | 58,9 |
| **Tipos de DeepSeek** (efecto y riesgo medios de su tipo) | **55,6** (r2: 56,8) |
| Signos de DeepSeek + su aviso de riesgo | 55,4 (r2: 55,0) |
| Tipos de Haiku, mismos títulos | 51,5 |

Techos de otras agrupaciones si se etiquetaran sin error (mismo montaje):

| Agrupación perfecta | Grupos | Nota |
|---|---:|---:|
| Sólo el signo del riesgo | 3 | 47–48 |
| Indicador que más sube | 7 | 42 (52 con el riesgo exacto aparte) |
| Indicador que más sube + riesgo | 21 | 53 |
| Indicadores de crecimiento que suben + riesgo | 22 | 58 |
| Tipo de DeepSeek + riesgo | 30 | 60 |
| Indicador que más sube + el que más baja + riesgo | 81 | 60–63 |
| Los 6 signos + riesgo | — | 67 |

**Lectura.** La forma de mirar una opción que más vale es la de los seis signos más el riesgo: con etiquetas perfectas casi iguala al oráculo. DeepSeek ya ve el riesgo bastante bien; lo que hay que arreglar son Skill y Output.
