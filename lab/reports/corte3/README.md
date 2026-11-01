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
