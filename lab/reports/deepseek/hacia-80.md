# Hacia 80: dónde están los puntos y qué se puede mover con DeepSeek

**Conclusión (28 oct).** **Una media de 80 no se puede alcanzar.**
- Es más de lo que saca un jugador con información perfecta: 72,4 de media en 360 partidas reales.
- La nota máxima es 79,6 acabando en L6 y 82,6 en L7.

**Lo que sí se puede mover, medido hoy por 1,6 USD y sin ninguna partida:**
- **Dónde se pierde.** Las elecciones caras de DeepSeek se concentran en L1–L3, y en las situaciones de L1 con la evaluación cerca pierde ~3–4 puntos por decisión, diez veces más que en una historia normal.
- **La causa.** La mitad de esas elecciones descartan la mejor opción como "riesgo oculto" (en privado, después). Pero relajar esa lista (`t13-read-v9`) hace que DeepSeek coja opciones privadas que sí son arriesgadas, y empeora el control de riesgo.
- **Lo que no funciona.** Decirle que Health y Dignity se quedan en 10 (`t13-read-v8`) y reescribir la pista de riesgo de la lectura (`perceive-v5`) no cambian nada.
- **Lo que queda.** La lectura de DeepSeek manda (~11 puntos en la réplica) y no responde a la redacción. Lo único medido que queda por probar es el trimestre de L4 (Skill cuando Network y Output ya no suben), unos +1,5 en la réplica. Con DeepSeek decidiendo no se activa nunca, así que tendría que llevarlo un script.

**`t13-read-v4` sigue siendo el mejor manual.** No se ha jugado ninguna partida porque nada ha pasado el filtro de "de verdad prometedor".

28 oct 2026, rama `alejandro/deepseek` (worktree `~/huawei-ds`). Encargo de Alejandro: objetivo 80, razonando mucho antes de cada llamada a DeepSeek y jugando una partida sólo cuando sea de verdad prometedora.

## 1. Lo que significa 80

- **Nota máxima por nivel final** (todo lo demás al máximo, motor M16): L5 75,8 · L6 79,6 · L7 82,6. Una partida de 80 tiene que acabar en L7, o en L6 sin un solo fallo.
- **Política óptima con información perfecta** (planificador ajustado, efectos y riesgo exactos, umbrales conocidos): **72,4 de media** en 360 partidas reales (mediana 74,9, máximo 80,8; L6 en el 72 %).
- Por tanto, **una media de 80 está por encima de lo que saca un jugador perfecto**. Lo alcanzable con DeepSeek es acercar la media a ~70 y que algunas partidas lleguen a L6 (~76–79).

**Dónde pierde una partida completa de `t13-read-v4` (71,67) frente a una L6 perfecta (79,6):** L5 en vez de L6 (−3), Skill 105 en vez de 120 (−1,9), dinero 38 en vez de ~48 (−2,4), Network 54 en vez de 60 (−1).

## 2. El freno de L6 en las partidas reales

| Partida | Ascensos | Skill al mes en L4 | Final |
|---|---|---:|---|
| `t13-read-v4` 71,67 | 6, 12, **24**, 42 | ~2,7 | L5 |
| `script-v1` 76,87 (línea Formato) | 6, 12, **18**, 36, 48 | ~3,8 | L6 |

- v4 perdió el ascenso del mes 18 por 3 puntos de Skill y 3 de Output, y pasó 18 meses en L4.
- **En L4, Network y Output estuvieron 12 meses parados en su máximo** (36 y 26, meses 29–41) y DeepSeek siguió gastando cada trimestre en informes, red y proyecto clave: ni una vez Skill learning ni rotación.
- Las charlas de evaluación de los meses 30 y 36 alaban la entrega y la colaboración, ponen una A y no ascienden: dicen por exclusión que falta Skill. v4 no tiene ninguna regla que lea eso.

## 3. Qué parte es regla y qué parte es lectura (réplica, gratis)

Réplica `scripts/ingenieria-inversa/replica.py`; lecturas de DeepSeek = dos pasadas v3 del catálogo (una al azar por encuentro). 1.500–3.000 partidas por brazo, mismas semillas.

| Política | Lectura perfecta | Lectura de DeepSeek |
|---|---:|---:|
| Regla escrita tipo v4 (`LexBot`, `strict+rvc+blind+qb+lonetwo+rep+nofar`) | 58,9 | 52,0 |
| Planificador óptimo que sólo ve signos ±1 y la marca de riesgo (×2) | **68,4** (L6 62 %) | **57,0** (L6 23 %) |
| Planificador con efectos exactos | 73,4 | — |

Ablación del planificador de signos con la lectura de DeepSeek (57,0):

| Sin… | Nota | Cambio |
|---|---:|---:|
| conocer los umbrales (usa el techo) | 55,1 | −1,9 |
| su trimestre (usa el de v4) | 55,3 | −1,7 (L6 del 23 % al 9 %) |
| las dos cosas | 53,8 | −3,2 |
| el peso extra de Skill en historias | 57,0 | 0 |
| el peso del dinero | 56,9 | 0 |

**Lectura.** Sin umbrales, lo que se gana cambiando la regla son ~2–3 puntos; la lectura vale ~11 (68,4 frente a 57,0). Ninguna regla de peso en L1 (Network y Output dobles, no ceder nunca en L1) cambia los despidos. Dar más peso a Skill en las historias desde L3 tampoco (Skill 109 → 111).

**Calibración.** La réplica cuadra con las partidas reales en la media: v4 real (71,67 · 70,22 · ~15) ≈ 52 frente a 52–53; la familia script real 49,9 frente a 51,5. Sirve para ordenar ideas, no para afinar décimas.

## 4. Auditoría de las decisiones reales de DeepSeek (gratis)

419 historias de 5 partidas oficiales de `t13-read-v2` a `v7` enlazadas con el catálogo exacto (el resto no se pudo enlazar por título). Cada elección se compara con la mejor según la función de valor del planificador óptimo (efectos y riesgo exactos).

| Nivel | Decisiones | Elige la mejor | Elige más riesgo del mínimo | Deja pasar crecimiento |
|---|---:|---:|---:|---:|
| L1 | 56 | 66 % | 7 % | 20 % |
| L2 | 110 | 75 % | 7 % | 15 % |
| L3 | 94 | 74 % | 7 % | 19 % |
| L4 | 134 | 86 % | 2 % | 7 % |
| L5 | 25 | 76 % | 8 % | 12 % |

**Causa de las 76 decisiones caras** (pérdida > 1 en unidades del planificador):

| Causa | Casos | Pérdida |
|---|---:|---:|
| **Elige una subida de Health o Dignity que ya están en 10**, con el mismo riesgo o menos | **37** | **205** |
| La mejor era más arriesgada (v4 la descarta a propósito) | 15 | 157 |
| Otras lecturas erróneas | 16 | 136 |
| Más Health o Dignity (sin estar llenas) en vez de crecer | 8 | 85 |

En esas 37 decisiones DeepSeek dejó pasar 10 de Skill, 7 de Network y 10 de Output (22 de ellas en L2–L3). Dignity está en 10 casi toda la partida, así que cada opción de "actuar con integridad" que la sube no vale nada. Ejemplo en la partida de v4 atascada en L1: en el mes 10 (Review in 2), con Dignity 10, eligió fijar su horario (Dignity +2, Health +1, Network −1) y llegó a la evaluación del mes 12 con Network un punto por debajo.

El rango 0–10 de Health y Dignity está publicado en el manual oficial: decir que una subida a partir de 10 se pierde no usa nada oculto.

## 5. `t13-read-v8`: v4 + "Health y Dignity se quedan en 10"

Un solo cambio sobre v4 (commit de v4 `09d5735`):
- en la lectura: *"Health and Dignity stop at 10. A rise in one that is already at 10 is lost, so read it as no change. It never makes up for a lower Skill, Network or Output, or for added risk."*;
- en el desempate de Grow: "more Health and Dignity that are under 10";
- en la instrucción del manifest (siempre a la vista): *"Health and Dignity stop at 10: a rise in one already at 10 is worth nothing, so never prefer an option for it."*

`careerlab lint`: 0 errores.

### Banco (DeepSeek, forma oficial de entrega): resultado nulo

`scripts/deepseek/bench.py` con los objetos del banco de transmisión, que traen el efecto exacto de cada opción y su `q` (nota final esperada tras elegirla, por continuaciones de la política óptima). Pérdida = mejor `q` − `q` elegido, en puntos de nota final. 60 objetos con la trampa (Health o Dignity en 10 y una opción que la sube frente a otra, igual de arriesgada o menos, que crece más; 30 de L1 y 30 de L2+) y 40 historias al azar de control. Una pasada por brazo, ~0,46 USD.

| Serie | `t13-read-v4` pérdida / cae en la trampa | `t13-read-v8` pérdida / cae en la trampa |
|---|---|---|
| Trampa en L1 (30) | 4,38 / 8 | 6,12 / 7 |
| Trampa desde L2 (30) | 3,53 / 7 | 3,71 / 8 |
| Control (40) | 0,38 / — (3 con riesgo) | 0,44 / — (3 con riesgo) |

**v8 no cambia nada** fuera del ruido. Las notas de DeepSeek lo explican: nunca eligen por Dignity. Eligen "corregirlo en la sala" porque lo leen como lo honesto y lo que arregla el problema del todo, y descartan "aclararlo por escrito después" como un arreglo aplazado, aunque en el catálogo esa opción baja el riesgo y la otra cuesta Network y Output. La correlación con Dignity era un efecto del diseño del juego (las opciones honestas suben Dignity), no la causa. **Descartado.**

Lo que sí deja el banco: **en las situaciones de L1 con la evaluación cerca, v4 pierde ~4,4 puntos por decisión, diez veces más que en una historia cualquiera (0,4).** Es la trampa del primer ascenso vista decisión a decisión.

### Por qué descarta la opción buena: la lista de riesgo

- **Notas reales:** en 30 de las 61 elecciones caras de las partidas reales en que la mejor opción no era más arriesgada, la nota de DeepSeek la descarta citando riesgo oculto: "en privado", "después", "aplazado", "enterrar el problema". En la partida de v4 de 70,22 son 9 de 11.
- **Catálogo:** la lista de palabras de riesgo de v4 sólo acierta en un ~55–60 % de los casos:

  | Palabras en la opción | Opciones | Con riesgo | Sin riesgo (0 o −1) | Network + Output medio |
  |---|---:|---:|---:|---:|
  | en privado | 24 | 54 % | 46 % | +0,96 |
  | después, más tarde | 20 | 60 % | 40 % | +0,75 |
  | en silencio, discretamente | 21 | 62 % | 38 % | +0,19 |
  | a medias, por fases, de momento | 9 | 56 % | 44 % | +1,44 |
  | por escrito, documentar | 15 | 27 % | 73 % | +0,20 |
  | abiertamente, en la sala, en público | 16 | 56 % | 44 % | −0,25 |

- **Lectura aislada del catálogo** (v3, dos pasadas): DeepSeek detecta el 88 % de las opciones con riesgo, pero marca el 24 % de las seguras (precisión 71 %).
- **Réplica** (2.000 partidas, lectura de DeepSeek r1):

  | Lectura | Nota | Despidos | Crisis |
  |---|---:|---:|---:|
  | Tal cual | 52,6 | 403 | 198 |
  | Sin falsas alarmas | 54,4 | 281 | 316 |
  | Sin riesgos no vistos | 56,2 | 303 | 80 |

**Pista de riesgo reescrita en la lectura (prompt `perceive-v5`, títulos de diseño, ~0,04 USD).** El cambio: lo que cuenta es si el problema llega a quien le toca y queda constancia, no si se dice en público. No mueve la lectura aislada: detección 86 % (igual), falsas alarmas 23 % (antes 22 %), precisión 72 % (74 %). Como con las pistas de Network y Output, la lectura de DeepSeek no responde a la redacción.

## 6. `t13-read-v9`: el camino discreto antes de la evaluación

Una idea sobre v4, en dos sitios:
- **Paso 4 (evaluación cerca) y manifest:** costes sociales escondidos en opciones educadas (decir que no a un compañero, corregir en público, destacar lo propio junto a un compañero, salirse de algo de grupo). Si ninguna opción está libre de ellos, elegir la que no incomoda a nadie y aun así hace lo correcto: una palabra en privado, un seguimiento por escrito, una cortesía breve antes de volver a lo propio, dejar que decida quién encaja mejor.
- **Lista de riesgo:** sube cuando el problema se oculta, se niega, se deja sin resolver o se parchea. Baja cuando llega a quien le toca y queda constancia. "Una palabra en privado o una nota escrita poco después a los afectados no es enterrar el problema"; guardar información confidencial de otro no es ocultar.

Banco: 90 situaciones de L1 con la evaluación cerca (70 historias distintas, alguna opción baja Network u Output y la mejor no), 29 de control de riesgo (con una opción privada o aplazada que sí es arriesgada y otra que no) y las 40 de control general.

| Serie | Manual | Pérdida por decisión | Elige la mejor | Elecciones que bajan Network u Output (y la mejor no) | Con riesgo |
|---|---|---:|---:|---:|---:|
| L1, evaluación cerca (90) | v4 | 3,31 | 61 % | 24 | 7 |
| | **v9** | 3,04 | 69 % | 19 | 7 |
| Control de riesgo (29) | v4 | 0,93 | 66 % | 4 | 1 |
| | **v9** | **2,15** | 62 % | 7 | **3** |
| Control general (40) | v4 | 0,38 | 88 % | 2 | 3 |
| | v9 | 0,38 | 85 % | 2 | 3 |

**Ruido del banco** (v4 repetido en las 90 de L1, `ds-v4-rep`): pérdida 3,68 frente a 3,31; la misma elección en 81 de 90 (90 %). v9 coincide con v4 en 74 de 90 y su ventaja en L1 es ~−0,46 sobre la media de las dos pasadas de v4, apenas por encima del ruido.

**v9 queda descartado.** En L1 mejora poco: ~−0,46 por decisión, casi dentro del ruido; a mitad de pasada parecía −1,1. En el control de riesgo empeora, justo como se temía: con "en privado no es enterrar el problema", DeepSeek elige opciones privadas que sí son arriesgadas. Dos ejemplos:
- **Objeción al diseño de otro equipo:** con el comentario de RR. HH. ya serio (riesgo 4), lo habla 1:1 con su responsable (+1, explosión; q 61 → 30) en vez de comentar en público con los datos (−1).
- **Equipo que va con retraso:** coordina en privado y le da una semana más (+2) en vez de escalarlo (−1).

En el catálogo, el 54 % de las opciones "en privado" son arriesgadas, y DeepSeek no distingue cuáles. **La lista prudente de v4 es el equilibrio correcto para su lectura:** las falsas alarmas cuestan crecimiento en L1, pero evitan explosiones.

## 7. Siguiente paso con más valor esperado: el trimestre por script

- **Réplica.** Con la lectura de DeepSeek, el trimestre de la política óptima frente al de v4 vale +1,3 a +1,7 de media, y L6 pasa del 9 % al 23 %.
- **Partidas reales.** En la partida de v4 de 71,67, Network y Output estuvieron 12 meses llenos en L4 y DeepSeek no invirtió nunca en Skill. DeepSeek no rellena "Stalled" (0 de 160 notas), así que no lo detecta.
- **Propuesta.** Un script del Skill (`bash`, B27) que sólo lleve el trimestre. Detectaría en la propia partida qué indicador ya no sube con una acción que debería subirlo y propondría la energía y la acción principal. Las historias seguirían con el texto de v4, sin tocar.
- **Por qué no se ha probado ya.** El híbrido `script-v2` de la línea Formato (script en estado y trimestre) sacó 51,12 y 30,6, pero sus fallos vinieron de las historias. Hay que probarlo primero en la réplica con el script real y medir en el banco que las historias no cambian (las 40 de control y las 28 de riesgo) antes de jugar.

## Relevo (28 oct)

1. **Qué se ha hecho y por qué.**
   - Análisis de lo que significa 80 desde los fundamentos (§1).
   - Diagnóstico mes a mes de las partidas de v4 frente a la de 76,87 (§2).
   - Separación de regla y lectura en la réplica (§3).
   - Auditoría de 419 decisiones reales contra el catálogo exacto (§4).
   - Tres hipótesis probadas con DeepSeek en el banco o en la lectura del catálogo, todas baratas: v8 (§5), `perceive-v5` (§5) y v9 (§6).
   - Ninguna partida oficial: nada pasó el filtro.
2. **Resultados.** En las tablas de §3–§6. Gasto de DeepSeek hoy: 1,56 USD; la clave tiene 32,6 USD libres a las 11:50 UTC y la reserva de 15 sigue intacta. Entre las 23:30 de ayer y esta mañana alguien más gastó ~1,6 USD de la clave.
   - **Datos:** `~/careerlab-data/deepseek/runs/{ds-v4-full10,ds-v8-full10,ds-v9,ds-v4-rep}/`, las listas `ids-full10*.txt`, `ids-l1prep90.txt`, `ids-riskcheck30.txt` y `ids-v9-sets.json`, y la lectura `perceive/v5-r1`.
3. **Qué falló.** Las tres hipótesis fallaron. El banco es ruidoso: dos pasadas de v4 difieren en 0,37 puntos por decisión en las 90 de L1. Hay que comparar con `ds-v4-rep` antes de creer una diferencia de menos de ~0,5.
4. **Siguiente paso** (§7). Mañana, el trimestre por script, probado primero en la réplica (gratis) y después en el banco. Comandos:

   ```bash
   # réplica: planificador de signos y ablaciones
   uv run python scripts/deepseek/signplanner.py 1500 2:1:,2:1:lexq,2:1:capthr+lexq ds-v3-r1-full.json+ds-v3-r2-full.json
   # auditoría de decisiones reales
   uv run python scripts/deepseek/real_audit.py ~/careerlab-data/huawei-deepseek/runs/<run>/events.jsonl
   # banco: un manual frente a v4 en las mismas situaciones
   CAREERLAB_TARGET_ENV=~/huawei/local-runs/official-runner/.env DS_STOP_USD=<tope> uv run python scripts/deepseek/bench.py run --variant <bundle> --name <arm> --ids ~/careerlab-data/deepseek/ids-v9-all.txt
   uv run python scripts/deepseek/bench_sets.py ~/careerlab-data/deepseek/ids-v9-sets.json ds-v4-full10 ds-v4-rep <arm>
   ```
