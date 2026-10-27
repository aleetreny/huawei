# Categorización: la forma de agrupar las respuestas que DeepSeek entiende y que discrimina

**Conclusión.** La mejor agrupación no son los 10 tipos sino **leer cada opción como seis signos (Health, Dignity, Skill, Network, Output, Wealth) más el signo del riesgo**, con definiciones que digan cómo suele moverse cada indicador (prompt v3). Un bot que elige sólo con esa lectura de DeepSeek saca **56,0** en el simulador, frente a 46,7 con los 10 tipos de Haiku y 67,7 el oráculo. Con una regla escrita sencilla saca 53,7.

27 oct 2026, rama `alejandro/deepseek`. Scripts `scripts/deepseek/perceive.py` (etiquetado) y `scripts/deepseek/groupbot.py` (medida). Prompts en `scripts/deepseek/prompts/`.

## La medida

`groupbot.py` es la versión general de `scripts/question-bank/catbot.py`: el bot de 7 reglas juega 1.000–2.000 partidas del simulador con las mismas semillas, y en las historias **sólo ve lo que DeepSeek ha puesto** a cada opción. Hay tres formas de usar esa lectura:
- **tipo:** efecto y riesgo medios del grupo, calculados en la otra mitad de los títulos;
- **signos + riesgo:** el signo que DeepSeek pone a cada indicador (tamaño 1) y su aviso de riesgo;
- **tipo + signos + riesgo:** la media del tipo, corregida por los signos.

Con las etiquetas de Haiku, `groupbot.py` reproduce exactamente los números publicados (46,7 y 49,1), así que las cifras se pueden comparar.

**Ruido de las etiquetas.** Una sola pasada de etiquetas da notas que varían 5–7 puntos entre repeticiones: un riesgo que no se ve en un evento frecuente basta para muchas crisis de confianza. En la partida real DeepSeek lee la opción cada vez que la encuentra. Por eso la medida final usa **dos pasadas, y en cada encuentro el bot toma una al azar**.

## Las agrupaciones probadas

**Techos (etiquetas perfectas, títulos de diseño).** Sirven para saber qué merece la pena pedir:

| Agrupación perfecta | Grupos | Nota |
|---|---:|---:|
| Sólo el signo del riesgo | 3 | 47–48 |
| Indicador que más sube + riesgo | 21 | 53 |
| Indicadores de crecimiento que suben + riesgo | 22 | 58 |
| Tipo + riesgo | 30 | 60 |
| Indicador que más sube + el que más baja + riesgo | 81 | 60–63 |
| **Los 6 signos + riesgo** | — | **67** |

Las agrupaciones gruesas pierden demasiado. Pedir los seis signos y el riesgo es lo único que, bien leído, casi iguala al oráculo.

**Redacción de las definiciones** (lo que lee DeepSeek también es parte de la categorización):
- **v1:** definiciones del manual oficial y los 10 tipos, sin pistas.
- **v2:** con cómo suele moverse cada indicador. Skill sube al usar el propio juicio (analizar, aportar datos, preparar, aprender, negociar con argumentos); Output baja cuando el tiempo se va en otra cosa que la entrega propia.
- **v3:** v2 más dos pistas, el intercambio Output/Network (centrarse en lo propio sube Output y cuesta Network) y las señales de riesgo que se escapaban (quejarse de la empresa, su cultura o sus reglas aunque sea por el canal formal; arreglos privados o en paralelo; desengancharse), con la regla "ante la duda, marca riesgo".

Todas se escribieron mirando sólo los títulos de diseño, son principios generales y no citan ningún evento.

## Resultados

**Percepción** (subidas vistas / bajadas vistas; títulos reservados entre paréntesis):

| Indicador | v1 | v2 | v3 |
|---|---|---|---|
| Skill | 45 % / 19 % (37 % / 17 %) | 77 % / 17 % | 78 % / 28 % (73 % / 17 %) |
| Output | 49 % / 34 % (49 % / 39 %) | 33 % / 42 % | 47 % / 47 % (54 % / 55 %) |
| Network | 76 % / 61 % (80 % / 66 %) | 76 % / 72 % | 78 % / 79 % (84 % / 82 %) |
| Riesgo que sube | 83 % (91 %) | 81 % | 86 % (92 %) |

Estabilidad de v3 entre dos pasadas: tipo 86 %, riesgo 88 %, indicadores 82–97 %.

**Cuánto vale cada error** (v2, cambiando un indicador cada vez por el correcto; base 57,7 en títulos de diseño):
- riesgo, +3,3 (corregir sólo los riesgos que no ve: +2,3; corregir las falsas alarmas: nada);
- Output, +2,0;
- Skill y Network, +0,4;
- Health, Dignity y Wealth, nada.

**La medida única, todo el catálogo** (todos los títulos etiquetados por DeepSeek; dos pasadas mezcladas, 2.000 partidas; error típico ±0,45):

| Lo que ve el bot | Nota | Nivel 6 o más | Despidos | Crisis de confianza |
|---|---:|---:|---:|---:|
| Oráculo (efecto y riesgo exactos) | 67,7 | 51 % | 7 % | 3 % |
| **v3: tipo + 6 signos + riesgo** | **56,2** | 15 % | 21 % | 8 % |
| **v3: 6 signos + riesgo** | **56,0** | 14 % | 20 % | 8 % |
| v3: 6 signos + riesgo, **regla escrita** | 53,7 | 13 % | 26 % | 6 % |
| v1: tipo + 6 signos + riesgo | 51,8 | 9 % | 25 % | 12 % |
| v1: 6 signos + riesgo | 50,5 | 8 % | 28 % | 12 % |
| v1: sólo los 10 tipos | 49,4 | 7 % | 27 % | 12 % |
| v3: sólo los 10 tipos | 48,5 | 8 % | 29 % | 10 % |
| Haiku: tipos + indicadores | 49,1 | 5 % | 21 % | 15 % |
| Haiku: sólo los 10 tipos (lo que había que superar) | 46,7 | 2 % | 30 % | 13 % |

**Pérdida por decisión en el banco** (historias de ids-V2 y G1, una pasada; oráculo 0,77 y 0,82):

| Lectura | Títulos de diseño | Títulos reservados |
|---|---:|---:|
| v3: tipo + signos + riesgo | 1,14 | 1,50 |
| v1: tipo + signos + riesgo | 1,11 | 1,44 |
| Haiku: tipos + indicadores | 1,55 | 1,57 |
| Haiku: tipos | 1,75 | 2,04 |

En el banco v1 y v3 empatan: la pérdida por decisión pesa igual todos los errores, mientras que el simulador castiga sobre todo los riesgos no vistos que llevan a la crisis de confianza.

## La regla de grupo escrita

Para que DeepSeek la pueda seguir, la regla es una lista por orden (`LexBot` en `groupbot.py`). Sólo usa la lectura de la opción y lo que se ve: el comentario de RR. HH., Health, Dignity, el mes de la evaluación y lo lejos que está cada indicador de su techo.

1. Descarta las opciones marcadas como arriesgadas (siempre: probado también "sólo si RR. HH. no está tranquilo", que da lo mismo o menos).
2. Descarta las que bajan Health si Health está baja, o Dignity si Dignity está baja.
3. En el mes previo a la evaluación, descarta las que bajan Skill, Network u Output.
4. Si un paso dejaría sin opciones, se salta.
5. De las que quedan, prefiere la que sube más indicadores de crecimiento (Skill, Network, Output) que aún no estén en su techo, contando doble el que está más lejos, y restando uno por cada uno que baja. Al final de la carrera, prefiere Health, Dignity y bajar el riesgo. En caso de empate: la que baja el riesgo, después la que más Health y Dignity da, después la que no cuesta dinero.

Con las lecturas de DeepSeek v3 saca 53,7, a 2,3 puntos de la fórmula completa (56,0). Con etiquetas perfectas la regla escrita se queda en 60,5–61,3 (la fórmula, 67): cuando la lectura tiene ruido, la regla sencilla casi no cuesta.

## Lo que queda abierto

- Output sigue siendo el indicador peor leído (la mitad de los cambios). Es la siguiente palanca: +2 puntos si se leyera bien.
- La nota real de DeepSeek no es la del bot: el bot aplica la regla sin fallos. Falta medir si DeepSeek, con esta lectura y la regla en el manual, elige como el bot (ver la prueba masticada).
- Los títulos reservados confirman la mejora en percepción y en el simulador, pero no en la pérdida del banco.
