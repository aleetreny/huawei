# Recrear Career Survival

**Conclusión:** con lo que hay en este repositorio se puede volver a jugar el juego entero sin la competición: `replica.py` reproduce el motor real en el 98,5 % de los pasos, el 99,8 % de los ascensos y con 0,35 puntos de error en la nota final, y el catálogo trae las 403 historias del juego de desarrollo con el efecto y el riesgo exactos de cada respuesta.

Todo salió de nuestras propias partidas por las 5 herramientas oficiales (`observe`, `take_action`, `check_latest_logs`…), sin leer el paquete del motor. El texto de las historias es del juego de desarrollo (dev 1.0.8).

## 1. Jugar en dos minutos

```bash
export BB_DATA=$PWD/lab/data/ingenieria-inversa
python3 scripts/ingenieria-inversa/replica.py play --catalog $BB_DATA/catalog_v2.json --games 200
```

Sólo usa la biblioteca estándar de Python. Salida de referencia (1 nov): media 67,8, máximo 79,5; 180 de 200 completas, 15 despidos, 5 crisis de confianza.

Para comprobar que la réplica sigue cuadrando con partidas reales:

```bash
python3 scripts/ingenieria-inversa/replica.py validate --catalog $BB_DATA/catalog_v2.json --batches v03-validation
```

## 2. Las piezas

| Pieza | Dónde | Qué es |
|---|---|---|
| Reglas del motor | [motor-exacto.md](../lab/reports/ingenieria-inversa/motor-exacto.md) | M1–M17: orden del mes, efecto de las respuestas, riesgo oculto y explosiones, avisos, evaluación (charla, nota, tono, bonus), trimestre, techos de Skill, regla de ascenso, dinero, derrotas, L7, estrategia óptima |
| Hallazgos de la ingeniería inversa | [hallazgos.md](../lab/reports/ingenieria-inversa/hallazgos.md) | Lo medido con bots, con números |
| Simulador | [`scripts/ingenieria-inversa/replica.py`](../scripts/ingenieria-inversa/replica.py) | `Replica` + `Catalog`: sorteo de historias, respuestas, trimestres, cambio de mes, evaluaciones, riesgo, explosiones, derrotas y nota final. Subcomandos `build`, `validate`, `play` |
| Catálogo | [`lab/data/ingenieria-inversa/catalog_v2.json`](../lab/data/ingenieria-inversa/) | 403 nodos (historias y continuaciones), riesgo de 521 respuestas, 7 bolsas de sorteo, nodo inicial, modelos de nota y tono. `catalog_v1.json` es la versión construida sólo con b00 + b01 |
| Valor de cada respuesta | [`answer_values.csv`](../lab/data/ingenieria-inversa/answer_values.csv) | Por mes, nivel y riesgo: efecto, cambio de riesgo, nota esperada y arrepentimiento |
| Catálogo legible por etapa | [`mac/catalogo-etapas.md`](../lab/data/ingenieria-inversa/mac/catalogo-etapas.md) | Las preguntas con sus respuestas, efecto, riesgo y paso siguiente (12.885 partidas) |
| Partidas de bots | [`lab/data/ingenieria-inversa/`](../lab/data/ingenieria-inversa/README.md) | ~13.000 partidas (al azar, oráculo, voraz, planificador, validación). Formato en su README |
| Evaluaciones | `mac/reviews-*.csv.gz` | 38.179 evaluaciones del juego real con el estado de cada una |
| Políticas | [`politica_optima.json`](../lab/data/ingenieria-inversa/politica_optima.json), `models/`, `search*_top.json` | Oráculos y planificadores ajustados en la réplica |
| Techo y suelo | [techo](../lab/reports/techo/), [suelo](../lab/reports/suelo/), B31 en [HALLAZGOS](../HALLAZGOS.md) | El jugador perfecto saca ~72,4 de media; dónde se hunden las partidas |
| Réplica calibrada con DeepSeek | [exploracion](../lab/reports/exploracion/), `lab/data/exploracion/calib.jsonl.gz` | Un jugador de la réplica que elige como DeepSeek (C61) |

## 3. El juego original

El motor oficial está en PyPI y lo instala `uv sync` (`career-emulator-engine` 1.0.6 con el conjunto de datos 1.0.8, ver [lab/README.md](../lab/README.md)). Se juega por MCP con las mismas 5 herramientas:

```bash
uv sync
uv run career-emulator-engine update --source distribution --split dev
```

El programa oficial de participación (JiuwenSwarm) se instala con `sh scripts/setup_official_runner.sh` en `local-runs/official-runner/`. Las reglas oficiales (`handbook.rst`, `competition-rules.rst`, `failure-and-ending.rst`, `mcp.rst`…) están en su `docs/`, [en línea](https://techarena-career-sim.readthedocs.io/en/latest/handbook.html) y copiadas en `~/careerlab-data/reglas-oficiales/` del Mac de Alejandro.

## 4. Lo que no cuadra todavía

1. El dinero ±1 al cambiar de mes (el juego lo enseña redondeado).
2. La nota A frente a B en L4 (87 % de acierto): depende también de la media del semestre.
3. Explosiones de respuestas poco observadas, cuyo riesgo está mal medido.

## 5. Para reconstruir el catálogo desde las partidas

```bash
export BB_DATA=$PWD/lab/data/ingenieria-inversa
python3 scripts/ingenieria-inversa/riskseq.py b00-random-safe,b01-oracle-eps
python3 scripts/ingenieria-inversa/replica.py build --batches b00-random-safe,b01-oracle-eps --risk riskd.json --out catalog.json
```

Las partidas brutas de los lotes jugados en el Mac (`b01-oracle-eps10`, `b02-stages`… `b09-oracle-v3`, ~230 MB) se quedaron fuera de Git porque se rehacen con bots; están en `~/careerlab-data/ingenieria-inversa/` del Mac de Alejandro.
