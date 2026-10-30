# Línea Mejora: un manual mejor que `t13-read-v4`

**Actualización (30 oct).** El candidato es **`mejora/mv-5r`**. En lo medible, juega las historias como v4 (la ventaja de lectura en L1 quedó dentro del ruido al repetir el banco). Lo que aporta es fichas 95–100 y no cortarse por respuestas sin llamada. Una versión corta y otra sólo de calidad no mejoraron nada (§9–§11 y Relevo).

**Conclusión anterior (29 oct, 22:45 UTC).** **`mejora/mv-4` es mejor manual que v4 en todo lo que se puede medir con precisión, pero en 9 partidas reales no juega visiblemente mejor:**
- **Fichas:** 95–100 en sus partidas completas frente a ~64 de v4. A igualdad de partidas son **+3,3 de nota de versión**.
- **Decisiones del mes previo de L1** (banco de DeepSeek, 90 situaciones): pérdida **2,51** por decisión frente a 3,31–3,68 de v4 y 3,6–4,4 de la familia cp. Es la mejor de 9 variantes, sin empeorar el control de riesgo (0,84 frente a 0,93) ni el general (0,34 frente a 0,38).
- **Calidad** (jueces de Claude): 73 frente a 69.
- **Partidas** (mv-3 y mv-4, mismas reglas de juego): 68,64 · **77,78 (L6, la mejor partida de DeepSeek del proyecto)** · 66,06 · cortada · 63,35 · 69,62 · 37,06 · 18,98 · 63,27.
  - Las 6 completas promedian 68,1, como v4 y su familia.
  - Hubo 3 hundidas: un defecto de mv-3, ya arreglado; una crisis de confianza; un despido en L1. Es la tasa de siempre (~25 %), y con 9 partidas no se distinguen ±5 puntos de media.
- **Dos defectos encontrados y arreglados por el camino:**
  - la redacción del bucle de `ex-v1` no empareja con DeepInfra (0 de 3 sondas);
  - con el texto de mv-3 el agente acaba respuestas sin llamada y una partida se quedó sin nota (`max_continuations`). mv-4 lo corrige: 1–2 por partida, como cp-v12.

En nota de versión esperada, mv-4 ≈ v4 + 3,5 (fichas y calidad) + lo que valgan sus mejores decisiones en L1 (réplica +1 a +2, sin confirmar en partidas). Lo que sigue decidiendo la nota son los hundimientos, y sus causas son variadas (§8). Hallazgos: C68–C72.

Pregunta: ¿qué manual saca más nota de versión que `t13-read-v4` (corte 1: 64,75), partiendo de sus reglas? Rama `alejandro/mejora-v4` (worktree `~/huawei-mejora`), subtrabajo de la línea DeepSeek. Candidato: [`lab/policies-src/mejora/mv-4`](../../policies-src/mejora/mv-4). Scripts: `scripts/mejora/`. Presupuesto aprobado por Alejandro: 5 USD de DeepSeek; **gastados 3,23** (clave de 28,63 a 31,86 USD usados, 18:10–22:40 UTC; quedan 18,14).

## 1. Dónde está la nota, desde los datos reales

La nota de versión es 0,8 × media de 3 partidas + 0,1 × calidad + 0,1 × fichas. v4 sacó 64,75 con partidas de ~65, calidad ~65 y fichas ~64 (C45).

- **Fichas (+3,5 casi seguro).** ≤ 500 mil por mes da 100 (`competition-rules.rst`); v4 gastaba 1,35–1,47 M (~64). El bucle de dos llamadas de cp-v12 dio 370 y 492 mil en sus dos partidas (C59).
- **Partidas completas.** Las diferencias entre partidas completas son el ritmo de ascensos (`decisiones.csv.gz`): v4 hizo L2/L3/L4/L5 en los meses 6/12/24/42 sus dos veces (71,67 y 70,22); las de 62–68 llegan a L5 en el 48. L4 se atasca en Skill 12–30 meses; la primera evaluación de L3 falla por 1–5 puntos de Output o Network. La nota de una completa en L5 es 65 + 0,2 × dinero como mucho, y el dinero sale casi todo del sueldo (del ritmo).
- **Hundimientos.** Con una tasa del 15–20 %, P(las 3 completas) ≈ 0,5–0,6. El primero de la tabla (75,99) se explica con partidas como las dos completas de v4 + fichas y calidad altas y ninguna hundida: no hace falta un juego distinto, hace falta no hundirse.
- **La trampa de L1, partida a partida.** En las 11 partidas reales que no ascendieron en el mes 6, el fallo fue casi siempre **una sola decisión** de los meses 4–5 que bajó Network u Output (5 veces la última historia del mes 5), y 2 veces un trimestre del mes 3 que gastó la energía en salud o en Lay low con Output a medias.

## 2. Por qué DeepSeek pierde en el mes previo de L1

Banco de L1 ya pagado (90 situaciones × 6 brazos, `bench_sets.py`): v4 pierde 3,3–3,7 por decisión y elige una opción que baja N/O en 24–25 de 90. **Las notas de DeepSeek muestran que aplica la regla («protege S/N/O antes de la evaluación») pero lee mal los costes:**
- «poner una B justa», «un límite educado», «elogiar a la compañera y añadir lo tuyo», «negarse a hacer campaña» → cree que conservan Network; en el juego la bajan (−1/−2): **la red cae cuando alguien queda decepcionado, aunque sea con educación o con justicia**;
- «escribir una nota formal de reconocimiento», «guiarla con preguntas» → lee Network +; en el juego Output −1: **Output cae cuando tu tiempo va a otro o a un proceso**.
- La mejor opción suele ser la que deja cómodo al otro y te devuelve a tu trabajo, a veces con un riesgo pequeño.

**Lo que se había enterrado:** `t13-read-v9` sí mejoró ese banco (elecciones que bajan N/O 24 → 19, mejor opción 61 % → 69 %, pérdida 3,31 → 3,04). Se descartó porque además relajó la definición global de riesgo («una palabra en privado es segura») y en el control de riesgo eligió «hablarlo en privado» con el riesgo ya en 4 (pérdida 0,93 → 2,15). El daño venía de esa relajación, no de nombrar los costes sociales.

## 3. Réplica calibrada con el modelo de elección de v4 (`beta=v4fam`, 3.000 partidas por brazo)

`scripts/mejora/l1arms.py`, `scripts/mejora/mbot.py`. Error típico ~0,27.

| Brazo | Media | Despidos | Salud | Crisis | 1.er ascenso en el 6 |
|---|---:|---:|---:|---:|---:|
| Trimestre tipo v4 (RNR, SLN; Health desde 4) | 58,31 | 286 | 169 | 112 | 54 % |
| + trimestre de ex-v1 (L1 informes; L2–3 RNR + proyecto clave; L4+ SL + informe + rotación; Health desde 5) | 59,91 | 294 | 87 | 119 | 54 % |
| + freno de salud en historias (ex-v1) | **60,63** | 292 | 36 | 118 | 55 % |
| + veto perfecto a perder N/O en el mes previo de L1 (riesgo ≤ 1) | 63,59 | 118 | 50 | 130 | 69 % |
| … el mismo veto viendo el 50 % / 30 % de las pérdidas | 61,89 / 61,46 | 229 / 250 | | | 60 % / 57 % |
| … viendo el 50 % con un 15 % de falsas alarmas | 59,95 | 342 | | | 54 % |

- Lo que DeepSeek obedece (trimestre y freno de salud) vale **+2,3** sobre el comportamiento de v4.
- Arreglar la lectura del mes previo de L1 vale hasta +3,0 con lectura perfecta; **+0,8 a +1,3 si se ve un 30–50 % más de las pérdidas, y resta si marca opciones buenas como malas**. Por eso la regla nueva tiene que señalar costes concretos, no vetar a ciegas.
- Descartado en la réplica: trimestre de L5 a Network y mentoría (±0,05) y bajar el umbral de Health recovery en el nivel inicial (−0,2 a −0,7).

## 4. El candidato `mejora/mv-1`

ex-v1 (las reglas de historias de v4 a través de cp, el trimestre por tramos, el freno de salud, el bucle de dos llamadas y el texto para la rúbrica) **+ lo que funcionó de v9, sin lo que lo rompió**:
- paso 4 de las historias (sólo con Review in 1–2) con una viñeta «Read the hidden costs»: Network cae cuando alguien queda decepcionado aunque sea con educación o con justicia; Output cae cuando tu tiempo o tu mérito van a otro o a un proceso; si ninguna opción está libre de esos costes, la que deja más cómodos a los implicados y te devuelve a tu trabajo;
- la misma pista en un paréntesis de la instrucción del manifest;
- la lista de riesgo de v4 sin tocar.

Lint sin errores (los mismos 20 avisos REVIEW que ex-v1). Juez de calidad (`data/j01.jsonl`, Opus y Sonnet × 2): v4 71/74 · 66/66; ex-v1 80/83 · 66/62; **mv-1 81/82 · 63/62**.

## 5. Banco con DeepSeek

Las mismas 159 situaciones que v9 (`ids-v9-all.txt`: 90 del mes previo de L1, 29 de control de riesgo, 40 de control general), `bench.py` + `bench_sets.py`. Las referencias ya estaban pagadas.

| Brazo | L1: pérdida · mejor · bajan N/O · arriesgadas | Control de riesgo | Control general |
|---|---|---:|---:|
| v4 (`ds-v4-full10` / `ds-v4-rep`) | 3,31 / 3,68 · 61 / 60 % · 24 / 25 · 7 / 6 | 0,93 | 0,38 |
| cp-v5a, cp-v9, cp-v10 ×2 (familia de ex-v1) | 3,63–4,42 · 59–67 % · 22–28 · 5–8 | — | — |
| v9 | 3,04 · 69 % · 19 · 7 | 2,15 | 0,38 |
| **mv-1** | **2,58 · 69 % · 15 · 8** | 2,23 | 0,34 |
| **mv-3** | **2,51 · 64 % · 20 · 11** | **0,84** | **0,34** |

**mv-3 es el candidato:** la menor pérdida por decisión en L1 de las 9 variantes medidas (−0,8 a −1,2 frente a v4) sin empeorar el control de riesgo ni el general. Cambia el reparto: en vez de evitar tantas pérdidas de N/O como mv-1, acepta más riesgos pequeños (suma de riesgo de sus 90 elecciones −5, frente a −13 y −16 de v4: unas +0,1 por decisión, +0,6 a +1 por partida, que el trimestre desactiva). Es lo que hace el planificador: en el mes previo de L1 un riesgo pequeño cuesta menos que el ascenso.

- **mv-1 frente a v4 en L1:** mejora 13 situaciones (+104 puntos q) y empeora 3 (−22). Sus notas citan las pistas nuevas («charla unos minutos y vuelve al plazo: conserva Network y Output», «aclarar por escrito conserva Network», «no ir a esa reunión protege Output»).
- **El control de riesgo empeora por dos fallos de redacción, no por relajar el riesgo** (la lista de v4 está intacta): −32 de los −38 son una sola situación (L1, mes previo, Network ya bajo su Best: «declinar con educación» en vez de «ayudar esta vez», leyendo la ayuda como coste de Output: una falsa alarma) y −5 el desempate «la más cómoda» aplicado antes que el filtro de riesgo (en L3 eligió coordinar en privado, riesgo +2).
- **mv-3** arregla esas dos cosas y nada más: «Repair first» va primero en el paso 4; la pista de Output se ciñe a «trabajo extra que no es tu entrega» y añade que un favor rápido y acotado no suele costar; el desempate sólo entre las opciones que pasan el paso 2.
- **Traducido a la réplica** (`mbot.py`, `CountBot`): la tasa base de elecciones que bajan N/O en el mes previo de L1 es 21,8 % (real 22 %). Bajarla un 39 % (lo que hizo mv-1 en el banco) equivale a detectar ~0,8–0,9 de las pérdidas: +2 a +2,5 de media de partidas sin falsas alarmas. Con una sola pasada del banco y alguna falsa alarma, lo prudente es contar +1 a +2.

## 6. Sondas de la pareja de llamadas

`turnprobe.py`, 6 turnos desde la pantalla Continue, proveedor fijado (`DS_PROVIDER`). Datos en `~/careerlab-data/mejora/turnprobe-*.json`.

| Manual | DeepInfra (sin canal de razonamiento) | GMICloud (razona en oculto) |
|---|---|---|
| cp-v10 (comprobante, ya pagado) | 5 de 5 | 3 de 3 |
| **mv-1 (bucle con la redacción de ex-v1)** | **0 de 3** (narra y manda `take_action` sola) | 3 de 3 |
| mv-2 (secciones «Turn loop» y «Status line» de cp-v12 copiadas tal cual) | **3 de 3** (18 de 18 respuestas) | — |

**La redacción del bucle de ex-v1 rompe la pareja con los proveedores sin razonamiento.** Cambia tres frases del paso 3 del bucle y quita `Reviews here: 0` de la nota del bloque literal; con DeepInfra la nota de fichas volvería a ~65 (C56). Copiar byte a byte las dos secciones de cp-v12 lo arregla. Esto afecta también a `exploracion/ex-v1` y `ex-v3`, que llevan la misma redacción: **no entregarlos sin restaurar las secciones de cp-v12**.

## 7. Partidas

Programa oficial (slot 1, juego de desarrollo, runner `00b084a8`), `careerlab.target play`, una cada vez, ninguna cortada. Datos en `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-e8cdf663-*`; análisis con `scripts/comprobante/gametokens.py` y `traj.py`.

| Partida | Nota | Fin | Ascensos (mes) | Final S / N / dinero / H+D / riesgo | Fichas por mes (nota) | Paradas | Coste |
|---|---:|---|---|---|---|---:|---:|
| mv-3 n.º 1 | **68,64** | completa, L5 | 12, 18, 24, 42 | 123 / 46 / 29 / 18 / 0 | 704 mil (91,8) | 8 | 0,45 |
| mv-3 n.º 2 | **77,78** | completa, **L6** | 6, 12, 18, 36, 48 | 134 / 53 / 43 / 20 / 0 | 486 mil (100) | 0 | 0,29 |
| mv-3 n.º 3 | **66,06** | completa, L5 | 12, 18, 30, 48 | 109 / 32 / 34 / 18 / 0 | 533 mil (98,7) | 7 | 0,30 |
| mv-3 n.º 4 | — | **cortada por el programa** (`max_continuations`), mes ~14, L1 | — | — | — | 21 | 0,13 |
| mv-4 n.º 1 | **63,35** | completa, L5 | 12, 24, 30, 48 | 98 / 36 / 26 / 18 / 0 | 615 mil (95,4) | 2 | 0,35 |
| cp-v12 (control, misma noche) | 20,73 | **despedida en L1** (mes 24) | — | — | 282 mil (50) | 1 | 0,18 |
| mv-4 n.º 2 | **69,62** | completa, L5 | 6, 12, 24, 42 | 129 / 54 / 25 / 19 / 0 | 461 mil (100) | 1 | 0,45 |
| mv-4 n.º 3 | 37,06 | **crisis de confianza** (mes 27, L4) | 6, 12, 18 | 66 / 32 / 10 / — / — | (50) | 1 | 0,12 |
| mv-4 n.º 4 | 18,98 | **despedida en L1** (mes 24) | — | 9 / 2 / 7 / — / — | (50) | 2 | ~0,2 |
| mv-4 n.º 5 | **63,27** | completa, L5 | 6, 18, 24, 48 | 110 / 40 / 30 / 15 / 0 | 499 mil (100) | 2 | 0,30 |

- **N.º 1.** Perdió el ascenso del mes 6 (RR. HH. ya «frowning» en el mes 5: el modo estricto anuló la excepción y Output quedó en 2), pero encadenó 12, 18 y 24 y llegó a L5 en el 42 con Skill 123. El trimestre se cumplió como estaba escrito (mes 3: toda la energía a informes).
- **N.º 2: la mejor partida de DeepSeek del proyecto** (antes, 76,87 de `script-v1`). Ascendió en cada evaluación hasta L4 en el mes 18 (el ritmo del planificador perfecto), L5 en el 36 y L6 en el 48. En los meses de evaluación de L1 eligió lo que el planificador elige en el banco («bromear con lo de los snacks», «charlar unos minutos y volver al plazo», «prometer una evaluación de impacto», «un no firme a la merienda y comer otro día»): la lectura nueva actúa en partida real.
- **N.º 3.** Tampoco ascendió en el mes 6, pero no por N/O: llegó al mes 5 con Skill en 1–3 (hacen falta ~8), así que ese ascenso era imposible. Después, L4 lenta (L4 en el 30, L5 en el 48).
- **Los dos ascensos del mes 6 perdidos no son la trampa de antes.** En la n.º 1 el riesgo acumulado en los meses 1–4 activó el modo estricto, que anula la excepción del mes previo; en la n.º 3 faltaba Skill. En la n.º 2 los meses previos de L1 salieron como en el planificador; en la n.º 1, en el mes 11, repitió una vez el «declinar con educación» que cuesta Network (la falsa alarma de mv-1), y aun así ascendió en el 12.
- **N.º 4: la partida se quedó sin nota.** El agente terminó 21 respuestas sin ninguna llamada y el programa la cerró al llegar a 20 reanudaciones, hacia el mes 14 y todavía en L1. El vigilante no lanzó la 5 ni la 6. En esas respuestas el modelo escribe la llamada como XML dentro del texto y **la salida llega corrompida carácter a carácter** («mcp_career-ulator-engine_take_ation», «aprameter», «tring="tue"»); una vez en el historial, el patrón se repite. El registro de JiuwenSwarm no guarda qué proveedor de OpenRouter sirvió cada llamada.
- **Respuestas sin llamada por partida** (`jiuwen.log`, `tool_call_count=0`): cp-v12 1 y 2, cp-v10 1; mv-3 9, 3, 7 y 21. No es que narre más: la media de texto visible por llamada es parecida (cp-v12 53–194 caracteres, mv-3 167–189; cp-v10 narró 708 y sólo paró una vez). Las de cp se jugaron hacia mediodía UTC y las de mv-3 de 18:25 a 21:30: puede ser el proveedor de esa franja o el texto. Prueba en curso, a la misma hora: `mv-4` (mv-3 + «nunca termines una respuesta sólo con texto» en la instrucción del manifest; 3 de 3 sondas emparejadas con DeepInfra), una partida de control de cp-v12 y otra de mv-4.
- **Resultado de la prueba de las paradas (misma franja, 20:17–21:47 UTC):** mv-4 1 y 1; el control cp-v12 1. La frase de mv-4 en el manifest («never end a reply with text only…») las corta, y el proveedor de esa noche no rompía todas las partidas: el exceso era propio del texto de mv-3. Con n = 2 es una señal, no una prueba; partidas 3–5 de mv-4 en curso.
- **mv-4 n.º 1 (63,35), por qué fue lenta.** Mes 6: la última historia del mes 5 sólo ofrecía negarse (Network −1) o dos opciones con riesgo +2/+3; eligió bien y perdió el punto (la pérdida forzosa de C58). En L2, con RR. HH. «frowning», el modo estricto forzó fuera de la ventana de evaluación opciones de «arreglo completo» que bajaron Output de 5 a −1, y perdió el ascenso del 18. Llegó a Health 1 en el mes 37 pese al freno.
- **mv-4 n.º 3 (37,06).** Ascendió en 6, 12 y 18 (L4 en el 18, el ritmo del planificador), pero en L4 el riesgo subió de «quiet» a «frowning» en los meses 22–25 y explotó; con RR. HH. ya «angry» eligió «denunciarlo de forma anónima a RR. HH.» (lo anónimo está en la lista de riesgo y el modo estricto debía descartarlo) y llegó la segunda explosión. No era un mes de evaluación (la regla nueva no actuaba): es el fallo de C55, opciones «correctas» que DeepSeek no lee como arriesgadas.
- **Control cp-v12 (20,73).** Se quedó en L1 hasta el despido del mes 24: la trampa que ataca la lectura nueva.
- **Paradas del agente.** En 9 respuestas el proveedor escribió las llamadas como texto (XML roto y con erratas: `mcp_career-emulaor-engne_tak_ction`), el runner no vio ninguna llamada y tuvo que reanudar la partida (8 reanudaciones; el programa corta en 20 y la partida quedaría a medias). cp-v12 tuvo 1–2 por partida. Cada reanudación trae un `check_latest_logs` y un `observe` de más: 224 llamadas al modelo frente a ~170, y 704 mil fichas por mes. Es la degradación de algunos proveedores cuando el modelo narra mucho (C56), no las reglas.

## 8. Qué decide ahora la nota: los hundimientos

En las 10 partidas de esta noche (9 de mv, 1 de control) hubo 4 hundidas, y cada una por una causa distinta:

| Partida | Causa | ¿Qué la habría evitado? |
|---|---|---|
| mv-3 n.º 4 | respuestas sin llamada con salida corrompida → `max_continuations` | arreglado en mv-4 (frase del manifest) |
| mv-4 n.º 3 | riesgo acumulado en L4 en los meses 22–25, varias historias con todas las opciones a +1; en el mes 26 eligió la denuncia anónima (+1) frente a «no decir nada» (+2), la menor (corregido el 30 oct, §9) → segunda explosión | riesgo sin beneficio antes de RR. HH. adverso (§9) |
| mv-4 n.º 4 | L1: una nota de reconocimiento en el mes 5 (Output −1, la pista nueva no bastó), una pérdida forzosa en el 11 (todas las alternativas con riesgo +2/+3) y RR. HH. no sonriente en el 18 | aceptar el riesgo pequeño del mes previo de L1 con más decisión; rescate del mes 18 (B30) |
| cp-v12 (control) | L1, tres evaluaciones perdidas | lo mismo |

En partidas, el primer ascenso en el mes 6 salió **4 de 8 puntuadas** en mv (corregido el 30 oct: antes ponía 3; v4: 5 de 6; cp: 5 de 14). **No todas llegan preparadas al mes 5:** mv-3 n.º 3 con Skill 1 y Output 1, y otras tres con Output 1–2. Con estas muestras, la diferencia entre familias en partidas no se separa del azar.

## 9. Revisión del 30 oct: mapa de pérdidas, contraste con la auditoría de Codex y riesgo

Contrasta [revision-opus-78.md](../deepseek/gpt-principios/revision-opus-78.md) y [encargo-opus-78.md](../deepseek/gpt-principios/encargo-opus-78.md) (commit `95f3159`) con las partidas reales. Scripts: `scripts/mejora/lossmap.py`, `p72.py`; tabla de calibración regenerada con las partidas mv (`calib_data.py`, 4.893 historias).

**Correcciones aceptadas.**
- Los 72,4 (juego real) y 74,4 (réplica) del planificador son resultados medidos con información perfecta, **no un techo demostrado** (A5 ya lo decía). Retiro «77,78 de media no es realista» como afirmación; lo que sí dicen los datos es que ningún mecanismo medido lo acerca.
- Primer ascenso en el mes 6: 4 de 8 puntuadas, no 3. No todas llegan llenas al mes 5.
- La denuncia anónima del mes 26 (mv-4 n.º 3) era +1 frente a +2: eligió el riesgo menor; no fue un incumplimiento.

**Mapa de pérdidas por evaluación** (`lossmap.py`; evaluaciones sin ascenso de las partidas reales, indicador que faltó y causa en los dos meses previos):

| Tramo | Familia | Lectura errónea | Excepción +1 no usada | Forzosa | Crecimiento insuficiente |
|---|---|---:|---:|---:|---:|
| L1 | v4 (6 partidas) | 0 | 1 | 2 | — |
| L1 | cp (15) | 8 | 3 | 10 | — |
| L1 | mv (9) | 1 | 2 | 7 | — |
| L2–L3 | v4 / cp / mv | 2 / 4 / 1 | 2 / 3 / 1 | 4 / 8 / 3 | 3 / 3 / 2 |
| L4+ | v4 / cp / mv | 0 / 7 / 2 | 1 / 5 / 4 | 5 / 5 / 7 | **11 / 27 / 16** |

**Las 11 decisiones de mv que perdieron N/O/S en el mes previo de L1:**

| Alternativa limpia disponible | Casos |
|---|---:|
| sin riesgo (lectura errónea) | 3 |
| con riesgo +1 (la excepción ya escrita) | 2 |
| con riesgo +2 | 3 |
| ninguna | 3 |

**Errores de lectura en partidas reales**, en las ventanas de evaluación de L1. Es la prueba en contexto y con historial largo, y separa los títulos que se usaron para elegir variantes:

| Familia | Títulos vistos en el banco | Títulos nuevos |
|---|---:|---:|
| v4 | 5,0 % | 0 % |
| cp | 8,6 % | 12,2 % |
| mv | 4,1 % | 4,8 % |

En L2–L3 las tres familias están en 1,5–4 %. **La lectura nueva de mv devuelve a v4 lo que la familia cp había perdido, pero no mejora a v4.** La ventaja de 2,51 frente a 3,3–3,7 en el banco de L1 está probablemente inflada por haber elegido sobre ese banco (C68 queda matizado).

**Skill en L4.** DeepSeek ya elige casi todo el Skill seguro disponible: 0,86–0,93 por decisión frente a 0,93–0,94 de la mejor alternativa segura, es decir, deja 0,2–0,3 al mes. El ritmo de L4 (18 meses en todas las familias) no se arregla con lectura de historias.

**Riesgo elegido por decisión** (positivo; L2+):

| Familia | Review in 1 | Review in 2 | Resto | RR. HH. adverso |
|---|---:|---:|---:|---:|
| v4 | 0,210 | **0,029** | 0,111 | 0,136 |
| cp | 0,172 | 0,113 | 0,120 | 0,175 |
| mv | 0,190 | **0,143** | 0,109 | 0,158 |

En L4+, mv suma 0,161 por decisión (v4 0,110), y el riesgo sin beneficio (había una opción sin riesgo con igual o más crecimiento útil) es 0,030 frente a 0,009. Las elecciones arriesgadas de mv en el mes de preparación son casi todas «+1/+2 para no perder Output o Network» en L2–L4, donde sí hay margen entre umbral y techo.

**Réplica con la métrica del objetivo** (`p72.py`, 3.000 partidas, calidad supuesta 75):

| Brazo | Media | P(Q ≥ 72) | L6 | Despidos | Crisis | P(A ≥ 78) por tanda |
|---|---:|---:|---:|---:|---:|---:|
| Base tipo mv-4 | 60,6 | 17,7 % | 12,9 % | 9,7 % | 3,9 % | 0,12 % |
| + veto L1, detección 50 %, riesgo ≤ 1 | 61,9 | 20,4 % | 14,6 % | 7,6 % | 4,0 % | 0,15 % |
| + veto L1, detección 50 %, riesgo ≤ 2 | 62,0 | 20,6 % | 15,2 % | 6,5 % | 4,9 % | 0,17 % |
| + veto L1 perfecto, riesgo ≤ 2 | 63,7 | 24,0 % | 18,0 % | 2,5 % | 6,7 % | 0,25 % |
| Percepción perfecta de todas las opciones (preferencias actuales) | 61,9 | 19,3 % | 21,5 % | 7,1 % | 5,4 % | 0,17 % |

**Decisión sobre la regla de riesgo pequeño en L1: descartada.**
- mv-4 ya permite riesgo +1 en el mes previo con RR. HH. amable o quiet.
- Sólo 2 de las 11 pérdidas reales están en ese terreno, así que la interpretación de la regla no es el problema principal.
- Ampliarla a +2 cambia despidos por crisis (réplica: 6,5 % frente a 7,6 % de despidos y 4,9 % frente a 4,0 % de crisis), con +0,1 de media.
- Si algún día se reabre, estos son los controles que haría falta:
  - sólo el nivel inicial y sólo Review in 1;
  - sólo con RR. HH. amable, no quiet;
  - sólo la primera elección arriesgada del mes;
  - nunca en el arranque atascado;
  - Defuse y Lay low obligatorios en el trimestre siguiente;
  - como criterio de abandono, que las crisis no suban en la réplica ni en el control de riesgo del banco.

**Banco reservado de riesgo (DeepSeek, 0,55 USD).** 140 situaciones nunca usadas para elegir variantes (`lab/data/mejora/ids-riesgo-sets.json`):
- 39 de preparación de evaluación (Review in 2) en L2–L4;
- 101 de «tentación», donde una opción arriesgada da tanto crecimiento útil como la mejor segura.

Criterio fijado antes de mirar: hay candidato si mv-4 suma ≥ 30 % más riesgo que v4 y pierde ≥ 0,3 más por decisión.

| Conjunto | Brazo | Pérdida por decisión | Mejor opción | Riesgo sumado |
|---|---|---:|---:|---:|
| Preparación L2–L4 (39) | mv-4 | 0,96 | 72 % | 6 |
| Preparación L2–L4 (39) | v4 | 0,59 | 77 % | 4 |
| Tentación (101) | mv-4 | 0,37 | 75 % | 12 |
| Tentación (101) | v4 | 0,46 | 74 % | 13 |

El criterio se cumple sólo en el subconjunto de preparación, y con cifras muy pequeñas (2 puntos de riesgo); en el total no hay diferencia (0,54 frente a 0,50). La dirección coincide con las partidas reales (0,143 frente a 0,029 por decisión en Review in 2), pero es una señal débil. Además, la mayor parte de la diferencia con v4 viene de la base de cp, no de la lectura nueva: cp ya tenía 0,113.

**Qué adopto de la auditoría:**
- el objetivo como nota automática con calidad y eficiencia, informando P(Q ≥ 72) y contando las interrupciones;
- el mapa de pérdidas por ventana;
- probar sobre títulos y decisiones no usados para elegir;
- una modificación por candidato y la calidad en una variante separada;
- el protocolo de mv-4 byte a byte.

**Qué descarto, con los datos de arriba:**
- la regla de riesgo pequeño en L1;
- empujar Skill en las historias de L4 (no hay margen);
- el último trimestre como apuesta grande (+0,1);
- la afirmación de que C68 mejora a v4 (en partidas, igual que v4).

**Siguiente prueba con más valor por dólar.** Dos candidatos separados, como máximo:
- **mv-5r:** la viñeta «Read the hidden costs» y su desempate sólo en el nivel inicial, para que en L2+ el paso 4 vuelva a ser el de v4. Prueba: banco de preparación (39) + L1 (90), ~0,25 USD. Se abandona si la pérdida en L1 sube más de 0,3 sobre 2,51 o si el riesgo en preparación no baja al nivel de v4.
- **mv-4q:** sólo calidad (quitar duplicados y ambigüedades, protocolo idéntico). Se mide primero gratis con los jueces de Claude y después se comprueba en el banco que elige igual que mv-4 (~0,3 USD).

Ninguna de las dos acerca el 78. En la réplica, todos los mecanismos medidos dejan P(A ≥ 78) por debajo del 0,3 % por tanda y P(Q ≥ 72) por debajo del 25 %. La brecha con el objetivo está cuantificada y no hay hoy un mecanismo que la cierre.

## 10. Las dos variantes (30 oct): mv-5r se queda, mv-4q se descarta, y C68 se rebaja

**mv-4q (sólo calidad): descartada.** Cambios:
- el calendario de evaluación sin contradecir el orden del handbook;
- el plan de L4 coherente con su acción principal;
- el intercambio Skill/Output de guiar con preguntas, dicho explícitamente;
- una comprobación del menú antes del trimestre en bloque;
- el bonus del handbook;
- la fila de evaluación de la tabla rápida.

Protocolo y manifest idénticos. Jueces en la misma tanda (`data/j03.jsonl`, Opus y Sonnet × 3):

| Manual | Opus | Sonnet | Media |
|---|---|---|---:|
| mv-4q | 84 · 79 · 84 | 66 · 62 · 66 | 73,5 |
| mv-4 | 79 · 84 · 84 | 58 · 71 · 71 | 74,5 |

El criterio previo era +3 o más: no se cumple, y no se gastó su banco. Lo que los jueces critican de verdad es la longitud del protocolo y la contabilidad de la nota. No se puede tocar sin arriesgar la pareja de llamadas (C69).

**mv-5r (la lectura de costes ocultos sólo en el nivel inicial): se queda.**

| Conjunto | mv-5r | mv-4 | v4 |
|---|---|---|---|
| Preparación L2–L4 (39): pérdida · riesgo sumado | **0,59 · 4** | 0,96 · 6 | 0,59 · 4 |
| L1 (90), pérdida por decisión | 3,12 · 2,99 | 3,57 (mv-4) · 2,51 (mv-3) | 3,31 · 3,68 |
| L1, elecciones que bajan N/O | 22 · 23 | 24 · 20 | 24 · 25 |

- En la preparación de L2–L4 vuelve exactamente a v4.
- El criterio previo para L1 (≤ 2,81, es decir, 2,51 + 0,3) no se cumplió en la primera pasada (3,12). Pero ese margen era más estrecho que el ruido entre pasadas: v4 varió 0,37 consigo mismo y mv-4 sacó 3,57 donde mv-3 sacó 2,51.
- Regla fijada antes de repetir: abandonar si la media de dos pasadas de mv-5r supera en más de 0,3 la media de mv. Resultado: mv-5r 3,06 frente a 3,04. **Se queda.**
- Sondas de la pareja con DeepInfra: 3 de 3 (18 de 18 respuestas).

**C68 se rebaja.** Con dos pasadas por familia, la pérdida en el mes previo de L1 es mv 3,04 frente a v4 3,50 (diferencia 0,46, con un ruido de ~0,4 entre pasadas); en partidas reales, los errores de lectura son 4–5 % en mv frente a 0–5 % en v4. La lectura de costes ocultos corrige la regresión de la familia cp (8,6–12,2 %), pero **no hay prueba de que mejore a v4**. La lección de método: una sola pasada del banco de L1 no basta para decidir entre variantes, porque unas pocas situaciones con valores q muy grandes dominan la media.

**Qué queda frente a v4, con pruebas:**
- fichas 95–100 frente a ~64 (+3,3 de nota de versión a igualdad de partidas);
- los dos arreglos de formato (C69, C70);
- y, con mv-5r, el mismo riesgo que v4 al preparar las evaluaciones.

El juego de historias es, en lo medible, el de v4.

## 11. Partidas de mv-5r y la vía «manual simple» (30 oct)

**Dos partidas de mv-5r** (0,89 USD):

| Partida | Nota | Fin | Ascensos (mes) | Fichas por mes (nota) | Paradas | Coste |
|---|---:|---|---|---|---:|---:|
| mv-5r n.º 1 | 22,65 | **despedida en L1** (mes 24) | — | (50) | 0 | 0,23 |
| mv-5r n.º 2 | **69,00** | completa, L5 | 12, 18, 30, 42 | 461 mil (100) | 1 | 0,66 |
| mv-5r n.º 3 | 24,51 | **despedida en L1** (mes 24) | — | (50) | 0 | 0,23 |

La mecánica funciona: pareja de llamadas, fichas 100 y 0–1 paradas. La n.º 1 cayó en la trampa de L1 de siempre:
- RR. HH. ya estaba «frowning» en el mes 3, así que el modo estricto anuló la excepción.
- En el mes 5, «negarse y ceñirse a los hechos» costó Network.
- En el mes 11, una comida para dar las gracias costó Output.
- En el mes 17, «nombrar sólo a quienes hicieron el trabajo» (uno de los costes que la viñeta nombra) costó Network, con el riesgo por encima de 0.

**¿Le damos demasiadas indicaciones?** (propuesta de Alejandro). Lo que ya decían los bancos pagados, comparando DeepSeek **sin manual** con manuales en las mismas situaciones:

| Conjunto | Sin manual | t13-final | t13-read-v1 |
|---|---|---|---|
| General (320): pérdida · riesgo | 1,37 · 46 | 0,92 · 45 | 0,91 · 33 |
| Antes de evaluación (51): pérdida | **0,89** | 1,03 | 1,08 |

El manual sirve sobre todo para no coger riesgo. Las reglas de los meses de evaluación no ganan a DeepSeek sin manual.

**`mejora/mv-s`:**
- protocolo de llamadas y línea de estado byte a byte, y el mismo manifest que mv-5r;
- el resto en cinco reglas ordenadas («la primera que aplica»), un trimestre en tres líneas y una tabla por nivel;
- 9.681 caracteres, frente a 17.380 de mv-5r y 9.377 de v4.

Jueces de Claude: 71,3 tras añadir el plan por fases, los tonos de RR. HH. y «gasta los 3 puntos» (70,2 sin ellos), frente a 71,8 de mv-5r.

| Conjunto | mv-s | Límite fijado antes | Referencias |
|---|---:|---:|---|
| L1 (90) | 3,20 | ≤ 3,5 ✓ | mv-5r 3,12 · 2,99; v4 3,31 · 3,68 |
| Preparación L2–L4 (39) | 0,72 | ≤ 0,89 ✓ | mv-5r y v4 0,59; mv-4 0,96 |
| Control de riesgo (29) | **2,00** | ≤ 1,3 ✗ | v4 0,93; mv-3 0,84; mv-1 2,23 |
| Control general (40) | 0,47 | ≤ 0,6 ✓ | v4 0,38; mv-3 0,34 |

- El control de riesgo falla por **una sola situación**: L1, mes 11, Network bajo su Best. Eligió «declinar con educación» (−32) en vez de «ayudar esta vez», la falsa alarma que ya tuvo mv-1. Sin ella sacaría 0,93.
- **Por el criterio fijado, mv-s queda descartada.** Tampoco mejora nada medido: juega como mv-5r con la mitad de texto, y el ahorro de fichas es de ~7 mil por mes, despreciable.

**Conclusión sobre la hipótesis.** DeepSeek no se «pierde» con el manual largo:
- sus notas citan el paso correcto;
- obedece el trimestre;
- un manual de la mitad de largo elige igual.

Lo que falla es la percepción de los costes y los intercambios forzosos, y eso no cambia con la longitud. Lo que sí trajo el texto añadido fueron efectos secundarios: más paradas con mv-3 (C70) y más riesgo al preparar evaluaciones en L2–L4 (mejora-7). Un manual simple no los tiene, pero tampoco sube el techo. La falsa alarma «ayudar cuesta Output» aparece en 2 de 4 pasadas del texto de L1. Es el punto débil de esa viñeta y merece un control en cualquier versión futura.

## Relevo (30 oct, para seguir en un chat nuevo)

1. **Estado.**
   - El candidato es **`mejora/mv-5r`**:
     - las reglas de historias de v4 (vía ex-v1), con la lectura de costes ocultos sólo en el nivel inicial;
     - el trimestre por tramos y el freno de salud de ex-v1;
     - el bucle de dos llamadas de cp-v12 byte a byte;
     - «never end a reply with text only» en el manifest.
   - Frente a v4, lo probado es:
     - fichas 95–100 (≈ +3,3 de nota de versión a igualdad de partidas);
     - sin respuestas sin llamada que corten la partida (C70);
     - el mismo riesgo que v4 al preparar evaluaciones (mejora-9).
   - En el juego de historias es, en lo medible, v4: la ventaja de lectura en L1 quedó dentro del ruido al repetir el banco (mejora-8).
   - Partidas de mv-5r: 22,65 (despido en L1) · 69,00 · 24,51 (despido en L1). En las dos despedidas, las tres evaluaciones de L1 cayeron por Network: pérdidas forzosas (la historia del antiguo compañero que pesca información, negarse = Network −1 frente a alternativas +2/+3), proteger Output a costa de Network y un desplome de Network en los meses 15–16. **mv-5r no ascendió en el mes 6 en ninguna de las tres.** En partidas reales no hay prueba de que mv-5r supere a v4, y la trampa de L1 sigue siendo el problema número uno.
2. **Lo que se ha descartado con datos** (no repetir sin una razón nueva):
   - aceptar más riesgo en el mes previo de L1: cambia despidos por crisis (§9);
   - empujar Skill en las historias de L4: DeepSeek ya toma el 93 % del Skill seguro (§9);
   - el último trimestre como apuesta grande: +0,1 (§9);
   - una versión sólo de calidad (`mv-4q`, §10) y una versión corta (`mv-s`, §11): ninguna mejora lo medido;
   - creer que DeepSeek se pierde con el manual largo: con la mitad de texto elige igual (§11).
3. **Lo que decide la nota y sigue abierto.**
   - Los hundimientos (~25 %), sobre todo la trampa de L1. Las pérdidas del mes previo son en su mayoría forzosas (sin alternativa limpia con riesgo ≤ 1), y el riesgo acumulado pronto activa el modo estricto y anula la excepción (§9, §11).
   - El ritmo de L4: 18 meses en todas las familias.
   - En la réplica, todos los mecanismos medidos dejan P(Q ≥ 72) por debajo del 25 % y P(A ≥ 78) por debajo del 0,3 % por tanda. Hace falta una idea nueva, no otra regla del mismo tipo.
4. **Método aprendido.**
   - Repetir siempre el banco: una pasada de L1 varía ~0,4.
   - Fijar el criterio de abandono antes de mirar.
   - Comprobar en las decisiones reales de las partidas (`calib_data.py` y `lossmap.py`) y en situaciones no usadas para elegir.
   - Cualquier cambio en «Turn loop» o «Status line» necesita sondas con DeepInfra (C69).
   - La falsa alarma «ayudar cuesta Output» del texto de L1 sale en 2 de 4 pasadas: vigilarla.
5. **Datos y órdenes.**
   - Bancos en `lab/data/deepseek/bancos/ds-mv*` y `ds-v4-riesgo`; conjuntos en `lab/data/mejora/`.
   - Partidas en `lab/data/deepseek/partidas/mv-*` (tabla en `partidas.csv`).
   - Jueces en `data/j0*.jsonl`.
   - Gasto de la línea: 5,96 USD (3,23 el 29 oct y 2,74 el 30 oct); la clave queda en ~15,40 USD.
   - Para empezar en un chat nuevo:

   ```bash
   cd ~/huawei-mejora && git pull && uv run python scripts/exploracion/calib_data.py && uv run python scripts/mejora/lossmap.py
   ```

   ```bash
   CAREERLAB_TARGET_ENV=~/huawei/local-runs/official-runner/.env uv run python scripts/deepseek/bench.py run --variant lab/policies-src/mejora/<candidato>/bundle --name ds-<candidato> --ids lab/data/mejora/ids-mvs.txt --slots 14
   ```

   ```bash
   uv run python scripts/deepseek/bench_sets.py lab/data/mejora/ids-mvs-sets.json ds-<candidato> ds-mvs
   ```

### Relevo anterior (29 oct, noche)


1. **Hecho y por qué.**
   - Diagnóstico desde los datos reales: las completas se separan por el ritmo de ascensos y las notas de DeepSeek muestran que pierde el mes previo de L1 por leer mal costes sociales y de tiempo (§1–§2).
   - Réplica calibrada con el modelo de elección de v4 (§3).
   - Candidatos mv-1 → mv-4 (§4), banco de DeepSeek (§5), sondas (§6), 10 partidas reales (§7), análisis de hundimientos (§8).
   - Juez de calidad.
   - Exportación de todo lo pagado a `lab/data/deepseek/` (NORMAS §1.6), con `export_data.py` arreglado para llamadas con argumentos corrompidos.
2. **Resultados y datos.**
   - Bancos: `lab/data/deepseek/bancos/ds-mv1`, `ds-mv3`.
   - Partidas: `lab/data/deepseek/partidas/mv-3__*`, `mv-4__*` y `cp-v12__5be05936-00002`; tabla en `partidas.csv`.
   - Sondas: `~/careerlab-data/mejora/turnprobe-*.json`.
   - Jueces: `data/j01.jsonl`, `j02.jsonl`.
   - Réplica: `scripts/mejora/l1arms.py` y `mbot.py`, con las órdenes del §3.
   - Gasto: 3,23 USD.
3. **Qué falló o quedó a medias.**
   - mv-3 tenía un defecto (paradas) que sólo se vio en partidas.
   - La lectura nueva mejora el banco, pero no se ha podido ver en los ascensos reales de L1 (3 de 8).
   - No hay pasada de banco de mv-4 (sus reglas de historias son las de mv-3; sólo cambia una frase del manifest sobre el formato de respuesta).
4. **Siguiente paso.**
   - **Para entregar:** mv-4 es el mejor candidato para la nota de versión. Fichas y calidad suman ~+3,5 sobre v4 a igualdad de partidas. Frente a cp-v12 o ex-v1 tiene la lectura de L1 y los dos arreglos (bucle, paradas). Hay que adaptar los documentos de `docs/entrega/cut2/` a mv-4 y empaquetar con `scripts/entrega/build_cut.py`.
   - **Para subir la media de partidas:** atacar los hundimientos (§8).
     - En L1: que DeepSeek acepte con más decisión el riesgo pequeño del mes previo cuando toda opción segura pierde (réplica: veto con riesgo ≤ 1 = +2,5) y el rescate del mes 18.
     - En L4: prudencia tras la primera explosión.
     - Cada idea se prueba primero en el banco (~0,2 USD), no en partidas.
   - Órdenes para repetir el banco de un candidato nuevo, del mismo modo que §5:

   ```bash
   CAREERLAB_TARGET_ENV=~/huawei/local-runs/official-runner/.env uv run python scripts/deepseek/bench.py run --variant lab/policies-src/mejora/<candidato>/bundle --name ds-<candidato> --ids lab/data/deepseek/ids/ids-v9-all.txt --slots 16
   ```

   ```bash
   uv run python scripts/deepseek/bench_sets.py lab/data/deepseek/ids/ids-v9-sets.json ds-<candidato> ds-mv3 ds-v4-full10
   ```
