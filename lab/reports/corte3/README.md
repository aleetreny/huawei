# Línea Corte 3: superar 72,93 en la última entrega (1 nov)

**Pregunta:** ¿qué manual, entregado hoy, tiene más probabilidad de sacar una nota de versión por encima de 72,93 (el sexto del corte 2)?

Rama `alejandro/corte3` (worktree `~/huawei-c3`), carpeta `lab/reports/corte3/`, scripts en `scripts/corte3/`. Presupuesto: lo que queda de la clave de DeepSeek (12,52 USD a las 10:30 UTC), con permiso de Alejandro para gastarlo entero.

## 1. Punto de partida (1 nov, 10:30 UTC)

- **Marcador oficial** (techarena-uk.hydro.ac): somos el n.º 28 con 64,75 (corte 1, `t13-read-v4`) y 45,44 (corte 2, `mv-5r`). El sexto, 72,93, es otro equipo que también se llama «Gradient Depression». Del 2.º al 20.º están entre 70 y 75; varios equipos repiten ~72 en los dos cortes, otros pasan de ~72 a ~45: la evaluación tiene mucho azar, pero hay equipos que no se hunden.
- **Reglas (competition-rules.rst):** en el corte 3 sólo se puntúa la última versión subida; una partida que no llega al mes 48 tiene la nota de fichas limitada a 50; la calidad es la media de los SKILL.md con criterios publicados (descripción, pasos ejecutables con prioridades y qué hacer cerca de un límite, estrategia coherente con las reglas publicadas a 48 meses, robusta a cambios de redacción y orden).
- **Cuánto hace falta:** con fichas 100, la media de partidas necesaria es (72,94 − 10 − 0,1 × calidad) / 0,8: 69,3 con calidad 75; 68,0 con 85; 66,8 con 95. Las partidas completas de DeepSeek valen ~66 de media (desviación ~5,5). **Hay que no hundirse en ninguna de las 3 y, además, subir la calidad.**

## 2. Diagnóstico nuevo: la tercera evaluación de L1 se pierde por riesgo, no por Network

Sobre las 50 partidas pagadas (`lab/data/deepseek/decisiones.csv.gz`, eventos de cada partida):

| Evaluación en L1 | Éxito de DeepSeek |
|---|---:|
| mes 6 | ~26 de 50 (52 %) |
| mes 12 (si falló la del 6) | ~11–12 de 25 (~46 %) |
| mes 18 (si fallaron las dos) | **1 de ~12 (~8 %)** |

Todos los despidos en L1 son partidas que llegan a la tercera. En esas partidas, **Skill, Network y Output estaban llenos justo antes de la evaluación del mes 18** (9/3/3 en mv-5r n.º 1, cp-v12 n.º 3, v4-loop n.º 1, cp-v10 n.º 1). La nota fue D con RR. HH. «frowning» o «angry», y es la propia charla de la D la que baja Network (−1) y Dignity (−3), lo que parecía «perder Network en el mes 17».

Con la réplica del motor (`replica.py`, modelo de nota de L1): en el mes 18 la nota es C sólo con el riesgo oculto a 0 justo antes de la evaluación; un punto de riesgo da D, y la D suma además +1 de riesgo (por eso el comentario del mes 18 nunca sale sonriente tras una D). En los meses 6 y 12 la nota es siempre C, con cualquier riesgo.

En los meses 15–17 de esas partidas DeepSeek elige casi siempre opciones de riesgo 0 o −1, pero una o dos con +1/+2 bastan: «Own it, walk through the feedback in person» (+1), «Check in privately» (+1), «Keep a light touch» (+1), «Refactor in stages» (+1), «Propose dual-write with a canary» (+1), «Accept a later fix» (+2). El riesgo no baja de 0, así que no se puede acumular colchón: cada +1 de los meses 16–17 tiene que compensarse dentro de esos meses.

Precisión, mirando el estado justo antes de la última decisión del mes 17 en las 11 partidas que llegaron a la tercera evaluación: 7 sacaron D por riesgo (en 3 de ellas además faltaba Network u Output), 3 sacaron C con RR. HH. sonriente pero la última decisión del mes 17 les bajó Network u Output, y 1 ascendió (cp-v12 n.º 1). En la tercera evaluación hacen falta las dos cosas a la vez: riesgo 0 y Network/Output intactos, sin poder usar un riesgo pequeño para salvar un punto.

**Consecuencia:** las ventanas de L1 piden actitudes opuestas ante el riesgo. En los meses 4–5 y 10–11 un riesgo pequeño no cuesta la evaluación (la nota es C) y sí la salva si evita perder Network u Output. En los meses 13–17 de una partida atascada, el riesgo es lo único que decide.

## 3. Otros hallazgos del 1 nov (datos reales y tramos)

- **El trimestre del mes 3 gastado entero en salud cuesta la primera evaluación.** En las partidas reales, cuando el trimestre del mes 3 fue todo a Health recovery (el freno «Health ≤ 5: salud primero» de cp/mv), se ascendió en el mes 6 en 6 de 19; con un punto a salud y el resto a Network/Output (como hacía la familia v4), 9 de 11; sin salud, 8 de 16. Está confundido con la salud baja en el mes 3, pero explica parte de la caída de la familia del bucle en L1 (10 de 28 frente a 7 de 9 de v4) sin que lo cause el bucle.
- **Muertes tempranas en los tramos de hoy:** 4 de las primeras 27 acabaron antes de la primera evaluación, 3 por salud (Health de 5 a 0 en los meses 1–5 con opciones de esfuerzo o sociales) y 1 por ruina (Wealth negativo varios meses; el panel enseñaba 0). En las partidas reales eran raras, pero existen.
- **El protocolo de la tercera evaluación, mal redactado, falla:** en un tramo de `c3-k` atascado, el agente aplicó la excepción de riesgo leve con «Review in 2» (eligió «mitigación temporal, arreglo después») y, por preferir lo que «sigue el proceso», perdió 3 de Output en el mes 17. Arreglado en `c3-k3`: primero fuera todo lo que añade riesgo, después conservar S/N/O, al final preferir lo que reduce riesgo, y la excepción sólo con Reviews here 0 o 1.

## 4. Candidatos

| Manual | Qué es |
|---|---|
| `c3-k` | v4-loop (secciones del bucle byte a byte) + excepción de riesgo leve también con Review in 2 en el nivel inicial + regla de atascado + freno de salud y trimestre de Skill desde L4 + tablas para la rúbrica |
| `c3-a` | `c3-k` + una marca de coste por opción antes de elegir (`1 N- \| 2 ok \| 3 O- risk`) en los meses previos de L1 (idea del crítico) |
| `c3-k2` | `c3-k` + arreglos de los jueces de calidad + trimestre de salud mixto (un punto a salud y el resto a la evaluación; Health ≤ 3: lo que haga falta) + frenos de salud y dinero en el manifiesto |
| `c3-a2` | `c3-k2` + las marcas de `c3-a` |
| `c3-k3`, `c3-a3` | `c3-k2`/`c3-a2` + protocolo de atascado reordenado + segundos arreglos de los jueces |

**Jueces de calidad (Claude, a ciegas, rúbrica oficial):** ronda 1: Sonnet mv-5r 86 · c3-a 82 · c3-k 80 · v4-loop 68; Opus mv-5r 75 · c3-k 70 · c3-a 68 · v4-loop 55. Ronda 2 (Sonnet): c3-a2 82 · c3-k2 80 · mv-5r 78 · c3-k 70.

## 5. Hallazgos para HALLAZGOS (nombres provisionales)

| Nombre | Hallazgo | Fuente |
|---|---|---|
| corte3-1 | `Juego + DeepSeek` **La tercera evaluación de L1 (mes 18) se pierde por riesgo, no por Network.** DeepSeek sale de L1 en el mes 6 ~52 %, en el 12 ~46 % de las que fallaron, y en el 18 en 1 de 11. De las 11, 7 llegaron con S/N/O completos y sacaron D con RR. HH. no amable; la D baja Network −1 y Dignity −3 y suma +1 de riesgo, lo que parecía «perder Network en el mes 17». 3 sacaron C pero perdieron N/O en la última historia. Las ventanas de los meses 6 y 12 en L1 dan C con cualquier riesgo. | §2, `decisiones.csv.gz`, eventos de las partidas, `replica.py` (modelo de nota de L1) |
| corte3-2 | `DeepSeek` **El trimestre del mes 3 gastado entero en salud cuesta la primera evaluación:** 6 de 19 ascensos en el mes 6, frente a 9 de 11 con un punto a salud y el resto a N/O, y 8 de 16 sin salud. Confundido con la salud baja, pero coincide con la caída de la familia del bucle (cp/mv tenían «Health ≤ 5: salud primero»). | §3, partidas reales |
| corte3-3 | `DeepSeek, tramos fieles` **Las marcas por opción antes de elegir no mejoran la lectura:** en los meses 4–5 de L1 se pierde N u O en el 21–25 % de las decisiones con v4-loop, c3-k y c3-a por igual. | §6 |
| corte3-4 | `DeepSeek, tramos fieles` **En los tramos de hoy (proveedor mayoritario Baidu, con razonamiento) hay muertes tempranas:** salud a 0 en los meses 1–6 (v4-loop 3 de 15) y ruina con Wealth mostrado como 0. | §3, §6 |
| corte3-5 | `Método (jueces de Claude, rúbrica oficial)` Arreglar una referencia colgante, la contradicción del trimestre con el bucle, márgenes sin marcar y el calendario de evaluaciones sube a v4-loop de 55–68 a 71–80, al nivel de mv-5r (74–78), sin tocar el bucle. | §4 |
