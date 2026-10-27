# P1-base: línea base de la apertura (meses 1–5), cuatro manuales

**Pregunta.** ¿Qué manual asciende más en la primera evaluación (mes 6)?
**Diseño.** 30 partidas cortas de Haiku por brazo (actor `claude-cli:haiku^6`, CLI 2.1.303), cortadas al llegar al mes 6, intercaladas por rondas, 27 oct 00:35–01:08 UTC. Lote: [`batches/p1-base.json`](batches/p1-base.json).
**Medida.** Ascenso en la 1.ª evaluación, leído del primer estado del mes 6 (la evaluación se aplica al empezar ese mes). "En el umbral" = Skill, Network y Output en el mínimo que asciende en L1 según el estudio de caja negra (H6): material de laboratorio, nunca de un Skill.

## Resultado

| Manual | Partidas | Ascienden en la 1.ª (IC 95 %) | En el umbral (de ellos, ascienden) | Agotamiento antes del mes 6 |
|---|---:|---:|---:|---:|
| f3-lean-v1 (referencia) | 30 | 14 = 47 % (30–64) | 14 (14) | 0 |
| bb-mechanics-lean-v1 | 30 | 15 = 50 % (33–67) | 15 (15) | 2 |
| bb-mechanics-v1 | 30 | 11 = 37 % (22–54) | 11 (11) | 1 |
| observed-growth-v7 (Matteo) | 30 | 12 = 40 % (25–58) | 12 (12) | 0 |

- **Ningún manual se distingue de la referencia.** Las diferencias (13 puntos como mucho) están dentro del ruido de 30 partidas.
- **El ascenso es determinista:** 52 de 52 partidas en el umbral ascendieron, y ninguna por debajo.
- **Por qué no se asciende.** En casi todos los fallos el indicador que falta **se tenía y se perdió** (sólo 6 de 92 faltas son de un indicador que nunca llegó). Las pérdidas caen en los meses 4–5, sobre todo en el 5, el último antes de la evaluación (68 de 86 pérdidas, en el 5). Network falla tanto como Output.
- **Cómo se pierde (trazas).** Haiku elige respuestas de principios en público (pedir que se corrija un reconocimiento, poner una nota justa pero dura, plantarse) que suben la Dignidad (casi todas las partidas llegan al mes 6 con Dignidad 10) y cuestan Network. Con v7, Haiku escribe "Review: far" en el mes 5, justo antes de la evaluación, y cree que Network y Output están "por debajo de su máximo" cuando ya están en el techo: no sabe calcular cuándo llega la evaluación ni reconoce el techo.
- **Agotamiento.** Los dos bb-mechanics, que piden conservar Skill/Network/Output antes que la salud, tuvieron 3 agotamientos (salud 0) en los primeros 6 meses; f3-lean y v7, ninguno.

## Decisión

- Pasan a 15 partidas completas los dos mejores: **f3-lean-v1** y **bb-mechanics-lean-v1** (lote `full-base`).
- La palanca del P1 no es otro manual general, sino **no perder el punto en el último mes**: hipótesis H-P1a (reloj de evaluación), en un 2×2 con y sin el módulo sobre f3-lean y bb-mechanics.
- Lección para cualquier módulo: no anteponer los indicadores a la salud cuando la salud está baja.

Datos: registro del origen `secciones` (`lab/registry-origins/secciones/`) y `result.json` de cada partida en `~/careerlab-data/huawei-secciones/runs/` (fuera de Git). Tablas: `uv run python scripts/secciones/periods.py --batch p1-base` y `scripts/secciones/fail_r1.py --batch p1-base`.

## Diagnóstico de evitabilidad (01:40 UTC)

Con un catálogo de efectos anunciados construido con bots aleatorios (`scripts/secciones/avoidable.py`, lote b00 de ~700 partidas en `~/careerlab-data/secciones-bots/`, fuera de Git; material de laboratorio que nunca entra en un manual), se revisaron las decisiones de Haiku en los meses 4–5, en L1, en las que la respuesta elegida restó un punto de Network u Output que estaba en su techo:

| Manual | Decisiones de historia en los meses 4–5 | Restaron un punto en el techo | Había otra respuesta que conservaba ese indicador |
|---|---:|---:|---:|
| f3-lean-v1 | 180 | 32 | 32 |
| bb-mechanics-lean-v1 | 172 | 29 | 29 |
| bb-mechanics-v1 | 180 | 34 | 34 |
| observed-growth-v7 | 180 | 48 | 48 |

- **Siempre había alternativa**, aunque algunas son poco íntegras (los registros no muestran el riesgo oculto, así que no se puede separar "segura" de "arriesgada").
- **El patrón es general:** la respuesta que eligió Haiku es casi siempre la versión firme, formal o pública de una postura de principios (sube Dignidad y resta Network), y casi siempre existe una versión discreta y honesta del mismo fondo (en privado, por escrito después, abstenerse, ayudar esta vez y fijar un límite, preguntar en vez de señalar) que conserva la red. Como la Dignidad ya está en 10 en casi todas las partidas, esa subida se pierde.
- Consecuencia: la hipótesis `cap-trade` ("no compres lo que ya tienes": con la Dignidad alta, la versión discreta) ataca la causa exacta de los fallos.
