# Suelo: que ninguna de las 3 partidas oficiales se hunda

**Conclusión en una frase (28 oct, en curso):** en la réplica, con un jugador que imita a `t13-read-v4`, las partidas hundidas salen de dos sitios, quedarse en L1 (despido) y la segunda explosión (crisis de confianza), y cuatro reglas generales las recortan a menos de la mitad sin bajar la media: el rescate de la tercera evaluación en L1 con el riesgo a cero (B30), «si todas las opciones son arriesgadas decide el tamaño del riesgo, no el crecimiento», más prudencia tras una explosión y menos texto en el contexto. Están en el candidato `lab/policies-src/suelo/suelo-v1`; falta confirmarlas con DeepSeek (chat local).

Subtrabajo de la línea DeepSeek. Rama `claude/linea-suelo-hundimientos-5xjrnm`, carpeta `lab/reports/suelo/`, código en `scripts/suelo/`. Sin clave de DeepSeek: todo lo de aquí sale de la réplica, de los lotes de bots, del juez de calidad y del banco con Haiku.

**Pregunta.** Con v4, las partidas que salen bien sacan ~70, pero ~1 de cada 9 se hunde (~17), y la media esperada de una versión (3 partidas) se queda en 63–65. ¿Qué reglas generales, que DeepSeek pueda seguir, eliminan los hundimientos?

## 1. De dónde salen los hundimientos (réplica)

Jugador: el bot de regla escrita de la línea DeepSeek (`scripts/deepseek/groupbot.py`, `LexBot`), configurado como v4 (riesgo primero, ascenso antes que riesgo leve en el mes previo con RR. HH. tranquilo, protección de Network y Output dos meses antes en L1, reparación, trimestre «como DeepSeek», sin conocer los techos), con dos lectores:
- **exacta:** ve el signo real de cada efecto y del riesgo;
- **ruidosa:** un lector con las tasas medidas de DeepSeek (percepción v3: ve el 78 % de las subidas de Skill, el 47 % de las de Output, el 86 % de los riesgos, con sus falsas alarmas), que vuelve a leer cada vez. A escala completa es demasiado pesimista (muere por salud y explota mucho más que DeepSeek en partidas reales); la escala 0,5 se usa como banda inferior.

La réplica lleva un parche con B30: en la tercera evaluación de L1 la nota es C, y se asciende, sólo con el riesgo oculto a 0 (`scripts/suelo/floor.py`, clase `B30Grade`; la réplica de `main` da D siempre).

Resultados con 3.000 partidas por brazo, mismas semillas en todos (`python3 scripts/suelo/floor.py --games 3000 --arms ...`):

| Jugador (lector exacto) | Nota | Partidas < 40 | Alguna < 40 en 3 | En L1 en el mes 13 | Rescatadas en el 18 | Explosiones por partida | Despidos | Crisis |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| v4 sin B30 en la réplica (lo que medía la línea DeepSeek) | 63,3 | 11,4 % | 30 % | 10,4 % | 0 | 0,31 | 306 | 45 |
| v4 con B30 (el juego real) | 66,0 | 4,0 % | 11,6 % | 10,4 % | 151 de 313 | 0,33 | 85 | 49 |

Lectura: **la mitad de las partidas atascadas en L1 ya se salva en el mes 18 con las reglas trimestrales de v4** (Defuse con RR. HH. «quiet»), porque el juego real asciende en la tercera evaluación si el riesgo está a cero (B30). La réplica de `main` no lo modelaba y por eso la línea DeepSeek estimaba un suelo peor del que hay.

Por qué se pierden las evaluaciones de L1 (lector exacto, 3.000 partidas): en el mes 6, 2.073 ascienden, 475 llegan al mes 5 ya cortas (casi siempre Network u Output) y 452 pierden el punto durante el mes 5; en el mes 12, 612 / 153 / 160. En L1 el techo de Network y Output es su mínimo de ascenso, así que no hay colchón: la mitad de los fallos son pérdidas forzosas del mes previo.

## 2. Qué vale cada regla (réplica, 3.000 partidas emparejadas)

Sobre la base «v4 + B30 + margen de salud»:

| Regla añadida | Lector exacto: nota / <40 / despidos / crisis | Lector ruidoso 0,5: nota / <40 / despidos / crisis | Veredicto |
|---|---|---|---|
| Base (v4 con B30) | 62,5 / 7,8 % / 61 / 185 | 58,7 / 13,1 % / 116 / 237 | — |
| **`mag`: si todas las opciones son arriesgadas, la de menor tamaño** (v4 lo dice en una frase; el bot base no lo hacía) | **65,9 / 4,1 % / 62 / 26** | **62,1 / 8,2 % / 94 / 92** | **Entra.** La mayor palanca del suelo: las crisis bajan a una séptima parte |
| + `rescue`: en L1 tras dos evaluaciones sin ascenso, riesgo primero (sólo opciones que lo bajan, Defuse y Lay low cada trimestre, no ceder Network ni Output) | con `mag`: 66,0 / 4,0 % / 85 / 49 (3.000) frente a 98 → 107 rescates de 224 sin regla (2.000) | 61,9 / 8,6 % / 146 / 144 | Entra: lleva el riesgo a 0 en casi todas las atascadas (con riesgo > 0 en el mes 18: de 50 a 16 de 224). Lo que queda son partidas cortas de Output o Network en el mes 18 |
| + `blow`: tras una explosión, leer el comentario de RR. HH. un paso peor (Defuse con el tranquilo, sólo opciones que bajan el riesgo) | 66,0 / 4,1 % / 87 / 44 | **62,5 / 7,6 % / 142 / 97** | Entra: con lectura imperfecta baja las crisis un tercio |
| `sloss`: si la pérdida es forzosa, que caiga en Skill | 66,1 / 3,9 % / 75 / 60 | 62,1 / 8,4 % / 139 / 141 | +0,1; se apoya en un margen no publicado (Skill tiene uno en L1): no se escribe |
| `q3l1` (C40): en L1 con RR. HH. «quiet», el trimestre del mes 3 a Output y Network antes que Defuse | 66,0 / 4,1 % / 87 / 50 | 61,7 / 9,2 % / 156 / 146 | 0 con lector exacto, −0,2 con ruido: no entra |
| `ll1`: Lay low ya con «quiet» | 66,1 / 3,8 % / 84 / 38 | 62,0 / 8,0 % / 153 / 107 | +0,1, menos crisis, más despidos: no compensa el texto |
| `lastl1`: en L1, la tercera historia del mes previo acepta cualquier riesgo | 65,8 / 4,7 % / 77 / 85 | 61,6 / 9,2 % / 143 / 165 | Peor: lo que gana en ascensos lo pierde en crisis |
| `rvl1`: en L1 el ascenso antes que el riesgo con cualquier comentario | 65,4 / 5,4 % / 83 / 103 | — | Peor |
| `norvc`: quitar la excepción del mes previo de v3/v4 | 65,0 / 5,2 % / 132 / 18 | 61,1 / 10,1 % / 230 / 69 | Confirma la excepción: sin ella se atasca el 17 % en vez del 10 % |
| `dq2`: Defuse sólo desde «frowning» | 65,7 / 4,2 % / 88 / 59 | — | Peor que Defuse desde «quiet» (v4) |

Con el lector ruidoso a escala completa (1,0), `mag` + `rescue` + `blow` dan 55,6 frente a 50,9 de la base sin B30: las mismas reglas, con más efecto cuanto peor se lee.

**Lo que queda después:** con lector exacto, 2,8 % de despidos (atascadas en L1 que llegan al mes 18 cortas de Output o Network: pérdidas forzosas sin opción de reparar) y 1,6 % de crisis. En L1 los techos son los umbrales y no hay colchón posible; ninguna regla probada baja más los despidos sin subir las crisis.

**El tamaño del riesgo se puede leer sin eventos.** Con las etiquetas de Haiku de los 10 tipos (`lab/reports/question-bank/labels.json`) frente al riesgo del catálogo v2: ocultar (HIDE) es arriesgado el 88 % de las veces y de +2 o más el 64 %; atacar, empecinarse y ceder (ATTACK, PERSIST, YIELD), arriesgados el 65–85 % y de +2 o más el 25–35 %; evitar y venderse (AVOID, SELL), arriesgados el 46–54 % y de +2 o más el 9–14 %; arreglar, asumir y protegerse, 11–14 %. De ahí la escala del manual: aplazar o rodear < forzar, confrontar o ceder < ocultar, negar o apostar.

## 3. Los cortes del programa (contexto)

Lo medido con las situaciones grabadas del banco (`lab/data/transmision/bank-items.jsonl.gz`, 800 situaciones): la respuesta de `observe` ocupa unos 1.200 caracteres en una historia y unos 2.400 en una fase trimestral; cada entrada del registro, unos 320. Una llamada a `check_latest_logs` con 30 entradas mete unos 10.000 caracteres (≈ 2.500 fichas) en un historial que no se comprime (C17): tres llamadas así valen lo que diez decisiones. Desde el Skill sólo se puede pedir: un `observe` por decisión, `check_latest_logs` sólo cuando la nota no está a la vista y con pocas entradas, notas cortas en inglés sin repetir la opción ni las reglas. `suelo-v1` lo dice así en el bucle de turno y en la instrucción del manifest. No se puede medir aquí si DeepSeek lo obedece.

## 4. El candidato `suelo-v1`

`lab/policies-src/suelo/suelo-v1`, a partir de `calidad/v4-c5`. Cambios:
1. **Arranque atascado** («Reviews here» en la línea de estado): tras dos evaluaciones en el nivel inicial sin ascenso, el riesgo va primero en historias (opciones que lo bajan) y trimestres (Defuse y Lay low salvo con el comentario tranquilo; la energía que sobra, a lo que esté por debajo de su Best), hasta ascender. Se apoya en lo publicado («two weak half-year reviews and you hand the badge in») y en lo observado («en nuestras partidas sólo salió bien con el comentario tranquilo»).
2. **Si todas las opciones son arriesgadas, decide el tamaño del riesgo**, con la escala del §2, y no el crecimiento.
3. **Tras una explosión** («Blow-ups» en la línea de estado), el comentario de RR. HH. se lee un paso peor, en historias y trimestres, y la excepción del mes previo deja de aplicarse.
4. **Higiene de contexto:** un `observe` por decisión, `check_latest_logs` sólo sin nota a la vista y con pocas entradas, notas cortas.
5. El menú trimestral publica el efecto sobre el riesgo oculto de Defuse, Lay low y High-intensity (C38): se cita como información del juego.

Pasa `uv run careerlab lint` (sólo avisos REVIEW, los mismos que v4-c5). Juez de calidad y banco: §5 (en curso).

## 5. Comprobaciones aquí (sin DeepSeek)

**Lint.** `suelo-v1` y `suelo-v1-min` pasan `uv run careerlab lint` sin errores (sólo avisos REVIEW, los mismos de v4-c5: disparadores de calendario y el margen «4 o menos» declarado como nuestro).

**Juez de calidad** (`scripts/calidad-skills/judge.py`, rúbrica oficial, mismo lote, 4 lecturas por modelo; datos en `data-j-pair.jsonl`, `data-j-min.jsonl`):

| Manual | palabras | Haiku | Sonnet |
|---|---:|---:|---:|
| `calidad/v4-c5` (base) | 2.099 | 61,5 ± 4,1 | 62,5 ± 5,7 |
| `suelo/suelo-v1` | 2.634 | 61,5 ± 5,0 | 61,0 ± 1,7 |
| `suelo/suelo-v1-min` | 2.415 | (en curso) | (en curso) |

Igual que la base dentro del ruido del juez (±5). Lo que los jueces señalan de nuevo en `suelo-v1`: la línea de estado es más larga (siete campos) y la frase del rescate parecía una mecánica sin fuente; la segunda se reescribió como supuesto de trabajo. En una tanda anterior con el texto antiguo, Haiku 62,7 / Sonnet 62,3 (`data-j-suelo-v1.jsonl`); la base en esa tanda, 45,7 / 63,3 con una lectura a 0 de Haiku por «contradice el juego» en la frase del mes previo que v4-c5 ya llevaba: el juez tiene ese ruido.

**Banco de trampas con Haiku** (`scripts/suelo/trapbank.py` + `scripts/transmision/runbench.py`, entrega oficial del Skill, Haiku por la CLI 2.1.312; 176 situaciones de los lotes de bots `v03`, `v02`, `b01`, `d01`, `c01`, `h01`, 45 por tipo: L1 tras dos evaluaciones sin ascenso (28 historias, 17 trimestres), L1 en el mes previo, todas las opciones arriesgadas con tamaños distintos, tras una explosión con RR. HH. inquieto). Se puntúa lo que pide la regla, no el valor de la réplica (`scripts/suelo/trapscore.py`), porque la réplica sin B30 no puede valorar el rescate. Resultados: (en curso; se añaden abajo al terminar).

## 6. Qué debe correr el chat local con DeepSeek

Todo desde la carpeta del repo en el Mac, con la rama de esta línea juntada (o `main` cuando se junte). Orden por coste y por lo que enseña; parar en cuanto algo refute.

**1. Juez con DeepSeek (≈ 0,2 USD).** ¿Ve el modelo designado la misma calidad?

```bash
uv run python scripts/calidad-skills/ds_judge.py --out lab/reports/suelo/data-j-deepseek.jsonl --reps 5 --budget 0.30 lab/policies-src/calidad/v4-c5 lab/policies-src/suelo/suelo-v1 lab/policies-src/suelo/suelo-v1-min
```

Confirma: `suelo-v1` no baja más de 5 puntos frente a `v4-c5` (el ruido del juez). Si baja más, usar `suelo-v1-min`.

**2. Banco de trampas con DeepSeek (≈ 0,3 USD por brazo; tres brazos ≈ 0,9 USD).** ¿Hace DeepSeek lo que piden las reglas? Es la prueba que de verdad confirma: en 3 partidas la trampa de L1 casi nunca aparece.

Regenerar el banco (determinista a partir de `lab/data/ingenieria-inversa`, ~5 min, 2,7 GB en `~/careerlab-data/suelo/`):

```bash
python3 scripts/suelo/trapbank.py extract
```

```bash
python3 scripts/suelo/trapbank.py truth --per-tag 45 --rollouts 48
```

```bash
python3 scripts/suelo/trapbank.py ids --out ~/careerlab-data/suelo/ids-suelo.txt
```

```bash
TRANSMISION_DATA=~/careerlab-data/suelo uv run python scripts/transmision/runbench.py assemble --bank ~/careerlab-data/suelo/bank.jsonl --sit ~/careerlab-data/suelo/sit.jsonl --out ~/careerlab-data/suelo/items.jsonl --k-long 18
```

Jugarlo con DeepSeek (el arnés de la línea DeepSeek, `bench.py`, lee `items.jsonl` de la carpeta que diga `DEEPSEEK_DATA` y escribe en `runs/<brazo>/`; lleva su tope de gasto):

```bash
DEEPSEEK_DATA=~/careerlab-data/suelo uv run python scripts/deepseek/bench.py run --variant lab/policies-src/calidad/v4-c5/bundle --name ds-c5 --ids ~/careerlab-data/suelo/ids-suelo.txt
```

```bash
DEEPSEEK_DATA=~/careerlab-data/suelo uv run python scripts/deepseek/bench.py run --variant lab/policies-src/suelo/suelo-v1/bundle --name ds-suelo-v1 --ids ~/careerlab-data/suelo/ids-suelo.txt
```

```bash
SUELO_DATA=~/careerlab-data/suelo python3 scripts/suelo/trapscore.py --arms ds-c5,ds-suelo-v1
```

Confirma `suelo-v1` (frente a `ds-c5` en las mismas situaciones):
- **L1 tras dos evaluaciones, historias:** «adds risk» a la mitad o menos que c5 y «lowest risk» ≥ 85 %; «loses N/O avoidably» no sube.
- **L1 tras dos evaluaciones, trimestres con RR. HH. no tranquilo:** Defuse ≥ 80 % de las fases de energía y Lay low ≥ 80 % de las acciones principales (c5 no lo hace con «quiet» en la principal).
- **Todas arriesgadas:** «lowest risk» ≥ 85 % (Haiku con c5: 81 %).
- **Tras una explosión:** «adds risk» ≤ 10 %.
- **Mes previo en L1:** «loses N/O avoidably» igual o menor que c5 (sin regresión).
Si falla sólo lo de después de la explosión, vale `suelo-v1-min` (brazo `ds-suelo-v1-min`, otros 0,3 USD). Si DeepSeek no aplica el rescate (añade riesgo igual que c5 en L1 tras dos evaluaciones), la regla hay que llevarla a la instrucción del manifest con más peso o descartarla: no gastar en partidas.

**3. Partidas oficiales (0,7–0,8 USD cada una; 3 ≈ 2,4 USD).** Sólo si 1 y 2 confirman. Comprueban que no hay regresión en una partida normal; no pueden medir el suelo (la trampa sale 1 de cada 9 veces).

```bash
scripts/deepseek/start-loops.sh <tope de saldo> lab/policies-src/suelo/suelo-v1 lab/policies-src/suelo/suelo-v1 lab/policies-src/suelo/suelo-v1 1
```

Confirma: las 3 completas, media de las completas ≥ 68 (v4: 70–72), ninguna explosión en una partida con RR. HH. tranquilo la mayor parte del tiempo, y en las notas aparecen `Reviews here` y `Blow-ups` rellenos (DeepSeek no rellenaba «Stalled», C18: si tampoco rellena estos, el rescate depende de que lea el nivel y cuente las evaluaciones por su cuenta). Refuta: una eliminación, o media de completas < 66.

**Coste total del plan: ≈ 3,5 USD** (de los ~35 que quedan, 15 de reserva).

## Relevo

(Se completa al final.)
