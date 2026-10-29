# Plan de pruebas con DeepSeek para los candidatos de Exploración

**En una frase:** probar primero, con unos 0,5 USD, que el candidato `ex-v1` empareja las llamadas igual que cp-v12 y elige como él en las situaciones de L1, y sólo después gastar en partidas; `ex-v3` (preferir lo discreto a la confrontación en el mes previo de L1) se juega sólo si gana en el banco.

Escrito para el chat local con la clave de DeepSeek; no hace falta haber leído el chat de Exploración. Contexto: [README de la línea](README.md) (réplica calibrada, qué vale cada idea) y [pendientes.md](../deepseek/pendientes.md).

## Qué se prueba y por qué

| Candidato | Qué cambia sobre `comprobante/cp-v12` | Respaldo sin DeepSeek | Riesgo |
|---|---|---|---|
| `exploracion/ex-v1` | **Trimestre:** en el nivel inicial, toda la energía libre a Prepare report materials; recuperar Health desde Health 5 (antes 4); en L2–L3, el orden de v4 (informe, red, informe; proyecto clave), sin Skill learning; desde L4, Skill learning + Prepare report materials (antes, + Network maintenance) y rotación. **Historias:** con Health 3 o menos, fuera toda opción que la baje. **Texto:** reescrito para la rúbrica (plan por fases, tabla de límites, observaciones marcadas como nuestras); la línea de estado pierde «Reviews here» (el arranque atascado se lee de «Months at current level»). El bucle de turno es el de cp-v12 salvo el campo quitado de la nota del ejemplo literal | Réplica calibrada: **+1,3** de media de partidas sólo por el trimestre, **+1,8** con el freno de salud (muertes por salud 6,5 % → 1,1 %); juez de calidad Opus 83–84 (cp-v12: 72–73), Sonnet 71–72 (66) | El ejemplo literal del bucle cambia en un campo: hay que comprobar la pareja con sondas |
| `exploracion/ex-v3` | ex-v1 + en el mes previo de L1, con RR. HH. amable o quiet y sin otra elección arriesgada en el mes, tratar el problema de forma discreta (en privado con la persona, por escrito después de la reunión) en vez de corregir, negarse o plantarse en público | Réplica +0,3 (sólo ahí; en todos los meses resta). Sonnet en el banco de L1: pérdida por decisión 4,71 → 3,90 y cambia justo las decisiones previstas | Puede subir el riesgo en ese mes |
| `exploracion/ex-s1` | ex-v1 + script con estado (C60) en una tercera llamada de cada respuesta | 1.470 marcas de «lleno» sin una falsa en las partidas reales; réplica +0,0 | La tercera llamada puede romper la pareja; **opcional** (paso 7) |
| `exploracion/ex-v2` | ex-v1 + revisar la opción elegida en el mes previo de L1 | Sonnet: sin efecto (24 frente a 24) | **No probar** |

Control: `comprobante/cp-v12` (bancos y partidas ya pagados; no hay que repetirlos).

## Presupuesto

| Paso | Coste | Acumulado |
|---|---:|---:|
| 1. Sondas del bucle de ex-v1 (6) | ~0,06 USD | 0,06 |
| 2. Banco de L1 de ex-v1 | ~0,12 | 0,18 |
| 3. Banco de L1 de ex-v3 | ~0,12 | 0,30 |
| 4. Juez DeepSeek de ex-v1 y cp-v12 | ~0,15 | 0,45 |
| 5. Partidas: 2–3 del ganador | 0,5–0,7 cada una | 1,5–2,5 |
| 7. (Opcional) sondas de ex-s1 | ~0,06 | 2,0–2,6 |

Total: **~2–3 USD**. No pasar de 3,5 USD sin permiso de Alejandro; la reserva de 15 USD para el último corte no se toca.

## Paso 0. Preparación (0 USD)

```bash
cd ~/huawei && git fetch origin && git checkout main && git pull
```

```bash
uv run careerlab lint lab/policies-src/exploracion/ex-v1
```

```bash
uv run python -m careerlab.target register lab/policies-src/exploracion/ex-v1 --by "<tu nombre>"
```

Lo mismo con `ex-v3` si va a jugar (registra también a su padre ex-v1).

Si se quiere repetir algo de la réplica calibrada (gratis): `uv run python scripts/exploracion/calib_data.py` y después `uv run python scripts/exploracion/final_eval.py --games 4000` (README §1).

## Paso 1. ¿Empareja ex-v1 como cp-v12? (sondas, ~0,06 USD)

El ejemplo literal del bucle es el de cp-v12 con un campo menos en la nota (`Reviews here`). C53 y C59 dicen que lo que dispara la pareja es el bloque `tool_calls: [...]`, no su contenido, pero hay que comprobarlo.

```bash
DS_PROVIDER=DeepInfra uv run python scripts/comprobante/turnprobe.py --bundle lab/policies-src/exploracion/ex-v1/bundle --turns 6 --start 0 --stop-usd 14 --out ~/careerlab-data/exploracion/turnprobe-ex1-deepinfra-1.json
```

Tres veces con `DeepInfra` y tres con `GMICloud` (cambiar el sufijo de `--out`). Después:

```bash
uv run python scripts/comprobante/probeprov.py '~/careerlab-data/exploracion/turnprobe-ex1-*.json'
```

**Decisión.** 5 o más de 6 sondas emparejan → seguir. 4 o menos → volver a poner `| Reviews here: 0` en la nota del ejemplo literal de ex-v1 (como cp-v12) y repetir 3 sondas en DeepInfra.

## Paso 2. ¿Elige ex-v1 como cp-v12 en L1? (banco, ~0,12 USD)

```bash
uv run python scripts/deepseek/bench.py run --variant lab/policies-src/exploracion/ex-v1/bundle --name ds-ex1-l1 --ids lab/data/deepseek/ids/ids-l1prep90.txt
```

```bash
uv run python scripts/deepseek/bench_sets.py lab/data/deepseek/ids/ids-l1prep-set.json ds-ex1-l1 ds-cp10-l1-DeepInfra ds-cp10-l1-GMICloud ds-cp5a-l1
```

Referencias ya pagadas (las reglas de historias de cp-v10 son las de cp-v12): pérdida 3,63–4,42 por decisión, 22–27 elecciones que bajan Network u Output, 6–8 arriesgadas. Sonnet con ex-v1: 4,46 / 24 / 8.

**Decisión.** ex-v1 sirve si queda en ≤ 28 que bajan Network u Output y ≤ 9 arriesgadas (el ruido entre dos pasadas de v4 es ~4 elecciones). Si no, mirar las notas de las elecciones nuevas (`~/careerlab-data/deepseek/runs/ds-ex1-l1/*.json`) y avisar: no jugar.

## Paso 3. ex-v3 en el banco de L1 (~0,12 USD)

Igual que el paso 2 con `--variant lab/policies-src/exploracion/ex-v3/bundle --name ds-ex3-l1`, y comparar con `ds-ex1-l1`. Las notas de las elecciones que cambian dicen si aplica la regla (Sonnet escribió «clarify in writing after the meeting» donde antes «correct openly»).

**Decisión.** ex-v3 sustituye a ex-v1 sólo si baja las elecciones que bajan Network u Output a **18 o menos** sin pasar de **9 arriesgadas** y sin subir la pérdida por decisión. Entre 19 y 21: una segunda pasada (otros 0,12 USD) y decidir con la suma. Más de 21: se descarta y se apunta en HALLAZGOS (fila X).

## Paso 4. Juez de calidad con DeepSeek (~0,15 USD; informativo)

```bash
uv run python scripts/calidad-skills/ds_judge.py --out lab/reports/exploracion/data/j-ds.jsonl --reps 3 --budget 0.30 lab/policies-src/exploracion/ex-v1 lab/policies-src/comprobante/cp-v12
```

No decide nada: si DeepSeek puntúa ex-v1 por debajo de cp-v12 en más de 5, avisar en el README (los jueces de Claude dicen lo contrario).

## Paso 5. Partidas (0,5–0,7 USD cada una)

Del candidato que haya pasado los pasos 1–3 (ex-v3 si ganó; si no, ex-v1). Una partida cada vez, sin cortar ninguna (ESTADO §3: `CAREERLAB_TARGET_NEVER_STOP=1`, `lsof` antes de arrancar).

```bash
export CAREERLAB_ORIGIN=deepseek CAREERLAB_RUNNER_DIR=~/huawei/local-runs/official-runner CAREERLAB_TARGET_ENV=~/huawei/local-runs/official-runner/.env CAREERLAB_TARGET_PARALLEL=1 CAREERLAB_TARGET_NEVER_STOP=1
```

```bash
uv run python -m careerlab.target play --policy ex-v1 --spend --games 1 --slot 1 --max-usd-per-game 3 --reserve-usd 15 --purpose pilot --why "Exploración: ex-v1, partida de mecánica"
```

```bash
python3 scripts/comprobante/gametokens.py ~/careerlab-data/huawei-deepseek/runs/<run>
```

```bash
python3 scripts/comprobante/traj.py ~/careerlab-data/huawei-deepseek/runs/<run>
```

**Predicción escrita antes de jugar** (lo que las partidas sí pueden comprobar):
- pareja en ≥ 90 % de las respuestas de historia, con cualquier proveedor; < 0,55 M fichas por mes si completa;
- trimestres del nivel inicial con Prepare report materials en toda la energía libre (salvo Health ≤ 5 o RR. HH. no amable);
- Health recovery en cuanto Health ≤ 5; ninguna muerte por salud;
- en L2–L3, informe, red, informe y proyecto clave; desde L4, Skill learning y rotación.

**Lo que no pueden decidir:** la media. Con la dispersión de la familia (completas 56–72, un hundimiento cada 4–5 partidas), 3 partidas no distinguen +1 punto. No se cambia ninguna regla por una partida (regla 1 de comprobante §6.8). Una partida sí puede tumbar el candidato si la pareja cae por debajo del 80 %, si hay un error de menú en el trimestre o si muere por salud con la regla nueva ignorada.

## Paso 6. Entrega

- **Corte 2 (30 oct, 24:00):** ex-v1 si pasa los pasos 1 y 2 (no hace falta ninguna partida: sus cambios de juego son de trimestre, que DeepSeek obedece, B20). Si falla el paso 1 o 2, cp-v12. Los documentos de `docs/entrega/cut2/` deben describir el bucle y los cambios de trimestre (sin umbrales como reglas del juego; las observaciones como «in our runs»).
- **Corte 3 (1 nov):** ex-v3 si ganó el banco y tiene 2 partidas sin regresión de mecánica; si no, otra tirada del mejor (C47: cada versión distinta es una tirada nueva, pero tiene que llevar una mejora de verdad).

## Paso 7 (opcional). ¿Mantiene ex-s1 la pareja con una tercera llamada? (~0,06 USD)

Sólo si sobra presupuesto: ex-s1 no sube la nota en la réplica (+0,0); sirve para saber si el bucle aguanta un script con estado (C60) por si una idea futura lo necesita, y para el vídeo. `turnprobe_bash.py` es `turnprobe.py` con la llamada `bash` al script ejecutada de verdad en una carpeta temporal.

```bash
DS_PROVIDER=DeepInfra uv run python scripts/exploracion/turnprobe_bash.py --bundle lab/policies-src/exploracion/ex-s1/bundle --turns 6 --start 0 --stop-usd 14 --out ~/careerlab-data/exploracion/turnprobe-s1-deepinfra-1.json
```

Tres con DeepInfra y tres con GMICloud. **Decisión:** la pareja `take_action` + `observe` en ≥ 5 de 6 y el script respondiendo sin error en ≥ 90 % de las llamadas → apuntarlo en HALLAZGOS como «bucle de tres llamadas posible»; si no, apuntar que la tercera llamada rompe el patrón. No se entrega ex-s1 en ningún caso sin partidas.

Después de gastar: `uv run python scripts/deepseek/export_data.py` y commit (NORMAS §1.6); resultados a la tabla de [pendientes.md](../deepseek/pendientes.md).
