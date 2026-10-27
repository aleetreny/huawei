# Datos de la ingeniería inversa (bots, dev 1.0.8)

Son partidas de bots jugadas por las 5 herramientas oficiales, el 27 oct de 2026, en la nube. Llevan texto del juego de desarrollo, así que **sólo sirven para estudiar en este repo privado y nunca se copian a un manual**.

| Carpeta o archivo | Qué es |
|---|---|
| `b00-random-safe/` | ~9.700 partidas al azar con energía segura. Lote de descubrimiento. Algunos miembros gzip quedaron cortados al parar el lote; los lee `gzrobust.py` |
| `b01-oracle-eps/` | 571 partidas del oráculo m01 con un 15 % de decisiones al azar. Lote de descubrimiento |
| `c01-greedy-real/` | 300 partidas de la política voraz del simulador, en el juego real |
| `c02-planner-real/` | 162 partidas del planificador ajustado, en el juego real (2 brazos; las cortó el reinicio del contenedor) |
| `v02-validation/` | 600 partidas del oráculo m02r con un 5 % al azar. **Lote de validación**, que no se usó para descubrir reglas |
| `catalog_v1.json` | Catálogo del simulador construido sólo con b00 + b01: efectos, continuaciones, riesgo, modelos de nota y tono |
| `riskd.json` | Riesgo oculto entero de cada respuesta (`riskseq.py`) |
| `models/` | Modelos del oráculo; m02r lleva el riesgo exacto |
| `search_top.json` | Las mejores configuraciones del planificador encontradas en el simulador |
| `validation_v02.txt` | Salida de la validación final |
| `analisis/` | Scripts de análisis exploratorio que llevaron a cada regla |
| `*.log` | Registros de cada lote |

El lote `v01-validation` se corrompió porque se lanzó dos veces sobre los mismos archivos, y no se incluye.

Formato de cada partida (una línea JSON por partida en `games-*.jsonl.gz`):
- `steps`: lista de `[mes, fase, nodo, elección, estado, texto_eventos, etiqueta]`;
- `final` y `end`: estado y nota final;
- `logs`: registro oficial;
- los textos y las preguntas, deduplicados, están en `texts-*.jsonl` y `nodes-*.jsonl`.

Para usar estos datos con los scripts:

```bash
export BB_DATA=$PWD/lab/data/ingenieria-inversa
python3 scripts/ingenieria-inversa/replica.py validate --catalog $BB_DATA/catalog_v1.json --batches v02-validation
python3 scripts/ingenieria-inversa/replica.py play --catalog $BB_DATA/catalog_v1.json --games 500
```
