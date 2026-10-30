# Datos de DeepSeek en Git

**Qué es.** Todo lo de la línea DeepSeek que sólo estaba en el Mac de Alejandro (`~/careerlab-data`) y costó dinero de la clave o cuota de Claude, con el texto del juego incluido. Así lo pueden usar los chats de la nube (por ejemplo, para calibrar un jugador simulado contra decisiones reales) y no se pierde si falla el Mac. Decisión del equipo del 29 oct ([NORMAS](../../../NORMAS.md) §1.6). El repo es privado: **nada de esta carpeta puede ir a un Skill ni a un diseñador de manuales.**

Se rehace entera con `uv run python scripts/deepseek/export_data.py`, que copia desde `~/careerlab-data`, comprime y pasa un filtro que quita claves, cabeceras de autorización y rutas personales. Para usar los scripts de la línea sin el Mac, `uv run python scripts/deepseek/datapaths.py materialize` rehace en `~/.cache/careerlab/deepseek` la estructura original (`runs/`, `labels/`, `perceive/`, `ids-*.txt`, `calls.jsonl`, `gpt-*/`). Los scripts que leían rutas fijas lo hacen ya solos (`scripts/deepseek/datapaths.py`).

## Tablas resumen (empieza por aquí)

- **`partidas.csv`**: una fila por partida oficial (manual, línea, modelo, versión del programa, nota, meses, nivel, explosiones, indicadores finales, fichas, coste y de dónde sale, cómo acabó, número de decisiones, origen en el Mac).
- **`decisiones.csv.gz`**: una fila por decisión (2.831), con:
  - partida, manual, mes, tipo (`historia`, `energia`, `accion`), título de la situación, nodo del catálogo de la réplica si el título lo identifica sin duda (1.290);
  - número de opciones, opción elegida y su texto, último comentario de RR. HH. visto, nota del agente;
  - fichas y coste de la llamada que tomó la decisión (de `jiuwen.log`; vacío en las partidas del formato script, que no guardaron ese registro);
  - indicadores antes de decidir y su cambio hasta la siguiente observación (`d_*`; incluye el sueldo si cambia el mes).

## 1. `partidas/<manual>__<id>/`: las 21 partidas oficiales con DeepSeek

Programa oficial JiuwenSwarm 0.2.4b3, runner `00b084a8`, modelo `deepseek-v4-flash` por la clave de la competición (OpenRouter), juego de desarrollo. Cada carpeta tiene lo que guardó el programa: `score_report.json` (si lo hubo), `events.jsonl.gz` (todas las llamadas a herramientas y sus resultados: observaciones, elecciones y **notas** del agente), `transcript.log.gz` y, en las de la línea DeepSeek, `actor.json`, `result.json`, `dataset.log`, `play.log(.gz)` y `jiuwen.log.gz` (registro del programa con las fichas de cada llamada). Las del formato script traen `play.log`, `cost.txt` y `advisor-state/` (memoria del script).

| Partida | Manual | Nota | Meses | Nivel | Explosiones | Fichas de entrada | Coste (USD) | Fin |
|---|---|---:|---:|---|---:|---:|---:|---|
| `t13-read-v2__0b43b18e-00000` | t13-read-v2 | — | 26 | L3 | 0 | 22,2 M | 0,29 ¹ | cortada (sin informe) |
| `t13-read-v2__0b43b18e-00001` | t13-read-v2 | — | 33 | L2 | 0 | 36,6 M | 1,32 | max_continuations |
| `t13-read-v2__0b43b18e-00002` | t13-read-v2 | — | 40 | L4 | 1 | 45,4 M | 1,34 ¹ | cortada (sin informe) |
| `f1-steady-balance-v1__19618e77-00000` | f1-steady-balance-v1 | 18,76 | 24 | L1 | 1 | 16,0 M | 0,19 | eliminada |
| `t13-read-v7__31840d8e-00000` | t13-read-v7 | 67,27 | 49 | L5 | 0 | 60,3 M | 0,74 | completada |
| `t13-read-v3__4bdd76ad-00000` | t13-read-v3 | — | 48 | L5 | 0 | 62,7 M | 0,69 ¹ | cortada (sin informe) |
| `t13-read-v5__95ffe78b-00000` | t13-read-v5 | 66,71 | 49 | L5 | 0 | 66,6 M | 0,72 | completada |
| `t13-read-v1__f74ba2d9-00000` | t13-read-v1 | 14,98 | 24 | L1 | 2 | 18,2 M | 0,23 | eliminada |
| `t13-read-v1__f74ba2d9-00001` | t13-read-v1 | 42,51 | 30 | L4 | 1 | 27,0 M | 0,31 | eliminada |
| `t13-read-v4__f78c8b88-00000` | t13-read-v4 | 71,67 | 49 | L5 | 0 | 70,4 M | 0,81 | completada |
| `t13-read-v4__f78c8b88-00001` | t13-read-v4 | — | 22 | L1 | 0 | — | — | cortada (sin informe) |
| `t13-read-v4__f78c8b88-00002` | t13-read-v4 | 70,22 | 49 | L5 | 0 | 64,8 M | 0,72 | completada |
| `script-v1__sv1-g1` | script-v1 | 13,23 | 24 | L1 | 1 | 28,1 M | 0,83 | eliminada |
| `script-v1__sv1-g2` | script-v1 | 76,87 | 49 | L6 | 0 | 110,0 M | 1,24 | completada |
| `script-v2__sv2-g1` | script-v2 | 51,12 | 49 | L4 | 1 | 68,0 M | 0,74 | completada |
| `script-v2__sv2-g2` | script-v2 | 30,6 | 27 | L3 | 1 | 24,1 M | 0,31 | eliminada |
| `script-v3__sv3-g1` | script-v3 | 66,55 | 49 | L5 | 0 | 111,7 M | 1,22 | completada |
| `script-v3__sv3-g2` | script-v3 | 32,59 | 10 | L2 | 0 | 8,3 M | 0,12 | eliminada |
| `script-v3__sv3-g3` | script-v3 | 60,45 | 49 | L4 | 0 | 113,2 M | 1,21 | completada |
| `script-v4__sv4-g1` | script-v4 | — | 8 | L2 | 0 | — | — | cortada (sin informe) |
| `script-v4__sv4-g2` | script-v4 | — | 9 | L1 | 0 | — | — | cortada (sin informe) |

¹ Coste sumado de `jiuwen.log`: la partida se cortó sin informe. Seis partidas cortadas (`v2-00000`, `v2-00002`, `v3`, `v4-00001` y las dos de `script-v4`) se creían perdidas porque su carpeta no tenía `events.jsonl`; su registro en bruto seguía en el hueco del programa y está aquí. La de v3 llega al mes 48 en L5. `v4-00001` se cerró por un choque de puertos y no dejó registro de fichas; `v2-00001` acabó por el límite de 20 reanudaciones (C17) y su informe no tiene nota.

Informes: [deepseek/mejora-nota.md](../../reports/deepseek/mejora-nota.md), [deepseek/partidas-oficiales.md](../../reports/deepseek/partidas-oficiales.md), [formato/README.md](../../reports/formato/README.md). Scripts que las leen: `scripts/deepseek/real_audit.py` (acepta `.gz`), `scripts/formato/ingame.py`, `scripts/deepseek/export_data.py`.

## 2. `bancos/<brazo>/resultados.jsonl.gz`: bancos con DeepSeek (y Haiku)

Una línea por situación del banco, `{"file": …, "data": …}`, con la elección, la nota del agente, las lecturas del Skill y las fichas; `arm.json` (dentro) dice el manual. Las situaciones son las del banco de transmisión (`lab/data/transmision/bank-items.jsonl.gz`, con efecto exacto y `q` de cada opción).

| Brazo | Manual | Situaciones | Informe |
|---|---|---:|---|
| `ds-control`, `ds-control-b` | sin manual | 460, 140 | [obediencia](../../reports/deepseek/obediencia.md) |
| `ds-t13-final` | transmision/t13-final | 460 | [obediencia](../../reports/deepseek/obediencia.md) |
| `ds-t13-read` | deepseek/t13-read-v1 | 321 | [masticado](../../reports/deepseek/masticado.md) |
| `ds-v4-full10`, `ds-v4-rep` | deepseek/t13-read-v4 | 189, 91 | [hacia-80](../../reports/deepseek/hacia-80.md) |
| `ds-v8-full10` | deepseek/t13-read-v8 | 101 | [hacia-80](../../reports/deepseek/hacia-80.md) |
| `ds-v9` | deepseek/t13-read-v9 | 158 | [hacia-80](../../reports/deepseek/hacia-80.md) |
| `hk-control`, `hk-t10-countdown`, `hk-t13-final` | elecciones de Haiku grabadas en Transmisión, para comparar | 2.392, 2.215, 662 | [obediencia](../../reports/deepseek/obediencia.md) |

Scripts: `scripts/deepseek/bench.py` (corre, en el Mac), `scripts/deepseek/bench_sets.py`, `scripts/deepseek/paired.py`, `scripts/deepseek/obedience.py`, `scripts/transmision/score.py` (con `TRANSMISION_DATA=$(uv run python scripts/deepseek/datapaths.py where)`).

## 3. `etiquetas/`: lo que DeepSeek lee en cada opción

- `*.json`: etiquetas por opción del catálogo (`nodo:opción` → signos de los seis indicadores, riesgo y tipo). `ds-v*-r*-{dev,ho,full}`: lecturas de DeepSeek con los prompts `scripts/deepseek/prompts/perceive-v*.md` (dos repeticiones, títulos de diseño, reservados o todos); `truth-*`: la verdad del catálogo; `perfect-*`, `fix-*`, `fixrisk-*`: etiquetas sintéticas para medir en la réplica; `haiku*`: Haiku.
- `lecturas/<variante>-r<rep>.jsonl.gz`: las respuestas en bruto de DeepSeek a cada pregunta (`perceive.py score` las puntúa).

Informes: [percepcion](../../reports/deepseek/percepcion.md), [categorizacion](../../reports/deepseek/categorizacion.md). Scripts: `scripts/deepseek/perceive.py`, `scripts/deepseek/groupbot.py --labels`, `scripts/deepseek/signplanner.py`, `scripts/formato/simadv.py`, `scripts/deepseek/gpt_*.py`.

## 4. Lo demás

- **`ids/`**: listas de situaciones de cada banco (`ids-ds1.txt` y `ids-ds1-events.txt` de obediencia; `ids-full10*`, `ids-l1prep*`, `ids-riskcheck30.txt`, `ids-v9-*` de hacia-80) y `obedience-ds1.txt`.
- **`llamadas/calls.jsonl.gz`**: una línea por llamada directa a DeepSeek desde nuestros scripts (bancos y lecturas): hora, etiqueta, proveedor de OpenRouter, fichas, coste. `calls-nim.jsonl.gz`: la prueba por NVIDIA NIM ([nim](../../reports/deepseek/nim.md)).
- **`registros/`**: salidas de los bucles de partidas (`gameloop.sh`), de las partidas lanzadas a mano y de los bancos.
- **`gpt-principios/<carpeta>.tar.gz`**: datos de la auditoría desde principios básicos ([gpt-principios](../../reports/deepseek/gpt-principios/README.md)); casi todo son llamadas a Haiku y Sonnet (cuota de Claude). `datapaths.py materialize` los deja en su sitio.
- **`sustitutos/<modelo>.jsonl.gz`**: preguntas y respuestas de los sustitutos gratis (Haiku, Haiku 4.5, Sonnet 4.6, Sonnet 5, Qwen local, Luna) frente a DeepSeek ([sustitutos](../../reports/deepseek/sustitutos.md)); scripts `scripts/deepseek/proxies/`.
- **`programa/`**: lo que recibe el agente oficial, medido con un modelo falso a 0 USD (línea Formato, B27): `obs_seq.txt`, `tools.json` (las 52 herramientas), `fake.log`, `fake_llm.py`, `peek.py` y las tres partidas falsas (`modelo-falso/`).
- **`otros/`**: `answers.json.gz` (una fila por respuesta del catálogo con su texto; `scripts/question-bank/`), `items-g1.jsonl.gz` (bloque general del banco que usa `obedience.py`) y `public-v11/` (manual y partida públicos del equipo Kingjinsight, [fuentes-externas](../../reports/fuentes-externas/kingjinsight-v11.md)).

## 4b. `tramos/<tanda>/`: tramos fieles (línea Tramos, 30 oct)

Principio de partidas jugadas por DeepSeek contra el motor oficial con la petición exacta de JiuwenSwarm, hasta la primera observación del mes 6 ([tramos](../../reports/tramos/README.md)). Por tanda: `<brazo>-<n>.json.gz` (decisiones, notas, estado al parar, llamadas con fichas, coste y proveedor), `<brazo>-<n>.messages.json.gz` (todos los mensajes, con el texto del juego) y `calls.jsonl.gz`. Tandas: `smoke` (2 tramos hasta el mes 2), `r1-sin-razonamiento` (26 tramos, sin el razonamiento en el historial: ablación), `r2-fiel` (8 tramos, arnés fiel). Las crea `scripts/tramos/fiel.py run`, las copia aquí `fiel.py export` (rutas personales cambiadas por `~`) y las lee `scripts/tramos/analiza.py --data lab/data/deepseek/tramos/<tanda>`. Coste: 1,92 USD.

## 5. Lo que no se ha subido y por qué

| Qué | Dónde está | Por qué no |
|---|---|---|
| `nim.env`, `own-openrouter/.env` | `~/careerlab-data/` | Claves |
| Instalaciones del programa oficial (`*/target-slots`, `formato/slot-*`; 9–15 GB) | `~/careerlab-data/` | Software; se reinstala con `sh scripts/setup_official_runner.sh`. Sus salidas de partidas sí están aquí |
| `deepseek/items.jsonl` (81 MB) | `~/careerlab-data/deepseek/` | Se rehace del banco (`bench.py` lo crea si falta) |
| Vídeo y ZIP del corte 1 (1 GB) | `~/careerlab-data/entrega/cut1/` | Pesan demasiado para Git; hay copia fuera del Mac en iCloud Drive (`huawei-entrega-copia/cut1/`) |
| Partidas con Claude del laboratorio local (`~/careerlab-data/huawei/runs`, 200 MB, 26 oct) | `~/careerlab-data/huawei/` | No son de DeepSeek y quedan fuera de este encargo; se pueden subir igual si alguien las necesita |
| Bancos de calidad, techo y suelo | Nube | Esas líneas guardaron sus datos en la nube, no en este Mac |
