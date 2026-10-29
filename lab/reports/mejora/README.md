# Línea Mejora: un manual mejor que `t13-read-v4`

**Conclusión (29 oct, noche; provisional).** PENDIENTE (banco, sondas y partidas).

Pregunta: ¿qué manual saca más nota de versión que `t13-read-v4` (corte 1: 64,75), partiendo de sus reglas? Rama `alejandro/mejora-v4` (worktree `~/huawei-mejora`), subtrabajo de la línea DeepSeek. Candidato: [`lab/policies-src/mejora/mv-1`](../../policies-src/mejora/mv-1). Scripts: `scripts/mejora/`. Presupuesto aprobado por Alejandro: 5 USD de DeepSeek (clave en 28,63 USD usados al empezar, 29 oct 18:10 UTC).

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

- **N.º 1.** Perdió el ascenso del mes 6 (RR. HH. ya «frowning» en el mes 5: el modo estricto anuló la excepción y Output quedó en 2), pero encadenó 12, 18 y 24 y llegó a L5 en el 42 con Skill 123. El trimestre se cumplió como estaba escrito (mes 3: toda la energía a informes).
- **N.º 2: la mejor partida de DeepSeek del proyecto** (antes, 76,87 de `script-v1`). Ascendió en cada evaluación hasta L4 en el mes 18 (el ritmo del planificador perfecto), L5 en el 36 y L6 en el 48. En los meses de evaluación de L1 eligió lo que el planificador elige en el banco («bromear con lo de los snacks», «charlar unos minutos y volver al plazo», «prometer una evaluación de impacto», «un no firme a la merienda y comer otro día»): la lectura nueva actúa en partida real.
- **Paradas del agente.** En 9 respuestas el proveedor escribió las llamadas como texto (XML roto y con erratas: `mcp_career-emulaor-engne_tak_ction`), el runner no vio ninguna llamada y tuvo que reanudar la partida (8 reanudaciones; el programa corta en 20 y la partida quedaría a medias). cp-v12 tuvo 1–2 por partida. Cada reanudación trae un `check_latest_logs` y un `observe` de más: 224 llamadas al modelo frente a ~170, y 704 mil fichas por mes. Es la degradación de algunos proveedores cuando el modelo narra mucho (C56), no las reglas.

## Relevo

PENDIENTE.
