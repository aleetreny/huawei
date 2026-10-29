# Comprobante: el mejor manual para los cortes 2 y 3

**Conclusión provisional (29 oct, madrugada):** la palanca más barata y más grande que nadie había tocado es el **número de llamadas al modelo**, no lo que escribe. El total de fichas de una partida es cuadrático en las llamadas (cada una reenvía el historial entero, que JiuwenSwarm no comprime). `t13-read-v4` hace ~420 llamadas (un `observe` y un `take_action` por decisión, cada uno en su respuesta) y gasta 1,43 M por mes (nota de fichas 62). **JiuwenSwarm ejecuta en orden varias llamadas de una misma respuesta del modelo**, comprobado con un modelo falso en el runner oficial (0 USD): `take_action` seguido de `observe` en la misma respuesta funciona, y el `observe` ya enseña la situación siguiente. Con una respuesta por decisión y una por trimestre, el modelo haría ~170–210 llamadas y la partida bajaría a 0,4–0,6 M por mes: **nota de fichas 95–100, +3,5 puntos de versión** sin tocar ninguna decisión. Falta ver que DeepSeek obedezca (sonda en curso).

Línea `alejandro/comprobante` (worktree `~/huawei-comp`), 29 oct 2026. Encargo: una versión con nota automática ≥ 76; 10 USD de DeepSeek (hasta ~12 si algo prometedor está a punto de aclararse). Clave al empezar: 32,60 USD libres (17,40 usados).

## 1. De dónde sale la nota y cuánto cuesta cada punto

Nota de versión = 0,80 × media de 3 partidas + 0,10 × calidad + 0,10 × fichas. Fichas: 100 con ≤ 500 mil por mes, 0 con ≥ 3 M, lineal entre medias; una partida que no llega al mes 48 se queda en 50 como mucho.

| Parte | v4 hoy | Alcanzable | Puntos de versión |
|---|---:|---:|---:|
| Partidas (completas 70–72; 1 de cada ~9 se hunde) | ~64–66 de media esperada | ~70 sin hundirse; 73–74 exige L6 en alguna | 0,8 por punto de media |
| Calidad | 60–64 (Haiku, Sonnet) · 72 (Opus) | 66–70 (c5: +4,2) | +0,4 |
| Fichas | 62 (1,43 M por mes) | **95–100** | **+3,3 a +3,8** |

Para 76 hacen falta ≈ 73,5 de media de partidas con calidad 70 y fichas 100. Ninguna partida completa de nadie pasa de 73,1 salvo la de `script-v1` (76,87, L6). El objetivo exige una partida en L6 entre las tres, o tres partidas en L5 casi perfectas; lo que sí está al alcance con seguridad es llevar v4 de ~68–70 (sin hundirse) a ~72–73 de versión con fichas y calidad.

## 2. Anatomía de las fichas de una partida real de v4 (71,67)

Medido en `jiuwen.log` de `deepseek-pilo-f78c8b88-dff20f-00000-a1` (418 llamadas con `input_tokens`, `output_tokens`, `reasoning_tokens`).

- **Entrada por llamada:** 36.757 fichas en la primera, 278.920 en la 400.ª; crece en línea recta **608 fichas por llamada**. Suma 70,4 M.
- **Qué añade cada llamada al historial:** 176 fichas las escribe el modelo (texto visible y nota; el razonamiento oculto son sólo 84 mil fichas en toda la partida y no vuelve al historial) y **431 son resultados de herramientas y envoltorio** (`observe` ≈ 1.500 caracteres por historia, 3.000 en el trimestre; `{"success":true}`; nombres e identificadores).
- **Llamadas:** 207 `observe` + 207 `take_action` + 4 (handbook, skill, new_game, logs). Una respuesta del modelo por llamada.
- **Base fija por llamada:** ~36,7 mil fichas (mensaje de sistema de JiuwenSwarm en chino, 52 herramientas, manual, handbook). No depende del Skill salvo por el tamaño del SKILL.md y de la instrucción.

Modelo: `total ≈ N × 36,7k + g × N² / 2`, con N llamadas y g fichas añadidas por llamada. Reproduce los 68,7 M de la partida con N = 420 y g = 605.

| Bucle | N | g | Total | Por mes | Nota de fichas |
|---|---:|---:|---:|---:|---:|
| v4 real | 420 | 605 | 68,7 M | 1,43 M | 62,8 |
| v4 sin texto visible y notas cortas | 420 | 290 | 41,0 M | 0,85 M | 85,9 |
| … y trimestre con un solo `observe` | 372 | 290 | 33,7 M | 0,70 M | 91,9 |
| **`take_action` + `observe` en una respuesta, texto como v4** | 212 | 1.210 | 34,9 M | 0,73 M | 91,0 |
| **Una respuesta por decisión, sin texto** | 212 | 580 | 20,8 M | 0,43 M | 100 |
| Una respuesta por decisión y por trimestre, sin texto | 190 | 600 | 17,8 M | 0,37 M | 100 |

Las fichas de salida (158 mil en v4) no cambian nada. Kingjinsight (v3.1, 51 M) ya hacía 179 `observe` para 207 acciones y notas de 52 caracteres, con texto visible: eso explica sus 0,95 M por mes.

## 3. Lo que hace el runner oficial con varias llamadas en una respuesta (modelo falso, 0 USD)

`scripts/comprobante/fake_multi.py` responde al runner oficial (JiuwenSwarm 0.2.4b3, runner 00b084a8, en el hueco `slot-fake` de la línea Formato) con `[take_action, observe]` en cada respuesta, y una vez con `[take_action, take_action, observe]`. `scripts/comprobante/run_probe.sh multi2 50` (12 meses, 46 decisiones, 49 peticiones). Datos en `~/careerlab-data/comprobante/fake/multi2/` (texto del juego, fuera de Git).

- **Las llamadas se ejecutan en orden y todas vuelven antes de la siguiente llamada al modelo:** tras `[take_action, observe]` la petición siguiente trae los dos resultados y el `observe` muestra ya la historia siguiente (otro título, otro mes). 46 de 46 `take_action` con `success` true.
- **Tres llamadas también:** `[take_action(3), take_action(3), observe]` en el trimestre dejó la energía de 3 a 1 y el `observe` lo refleja.
- **JiuwenSwarm añade en cada petición un mensaje de usuario final** (`<system-reminder> … runtime`, 366 caracteres) que no se acumula en el historial.
- Lo que añade cada decisión al historial, en caracteres: 1.200–1.900 en una historia, ~3.000 en una pantalla trimestral.

Esto permite el bucle del manual `cp-v1`: una respuesta por decisión y una por trimestre.

## 4. El manual `cp-v1` (`lab/policies-src/comprobante/cp-v1`)

Padres: `calidad/v4-c5` (texto para la rúbrica, mismas decisiones que v4), `techo/v4-t0` (Skill en el trimestre desde el nivel 4), `suelo/suelo-v1-min` (arranque atascado y tamaño del riesgo), `stat-perception/v4-lean-q` (trimestre tras un solo `observe`). Nuevo:
- bucle de turno: tras un `observe`, decidir en silencio y responder sólo con las llamadas `take_action` y `observe`; en el trimestre, todas las acciones y el `observe` en una respuesta;
- línea de estado de cuatro campos: `Review in N | Now | Best | Reviews here` (fuera `Stalled`, que DeepSeek nunca rellenaba, y `Concerns`, sustituido por una frase);
- notas de una línea.

Lint: sólo avisos REVIEW, los mismos de c5, t0 y suelo (disparadores de calendario y el margen «4 o menos» declarado como nuestro).

## 5. Pruebas (se van añadiendo)

### 5.1 ¿Obedece DeepSeek el bucle? (`scripts/comprobante/turnprobe.py`, ~0,01 USD por sonda)
La sonda reconstruye la petición exacta del runner (mensaje de sistema de JiuwenSwarm con el IDENTITY del manual, las 52 herramientas, el primer mensaje del runner, el recordatorio por llamada) y deja a DeepSeek jugar 4–6 turnos sobre los `observe` grabados de la partida de v4.

| Manual | Texto visible por respuesta | Nota | Llamadas por respuesta |
|---|---:|---|---|
| `t13-read-v4` (control; reproduce la partida real) | 170–360 caracteres en chino | línea de estado + razón (235 caracteres en partida) | 1 |
| `cp-v1` («decide en silencio, sólo llamadas») | **0** | una línea (~75 caracteres) | 1 |
| `cp-v1b` (regla dura: dos llamadas por respuesta) | 0 | una línea | 1 |
| `cp-v1c` (en términos de API: «parallel tool calls») | 0–45 | una línea | 1 |
| `cp-v1b` en el trimestre (posición 9) | 0 | una línea | 1, pero **tres `take_action` seguidos sin `observe` entre medias** |

- **El silencio funciona:** DeepSeek deja de escribir y razona en el canal oculto (`reasoning_tokens` 200–1.000 por decisión frente a 20–340 con v4), que no vuelve al historial.
- **En la sonda no junta `take_action` y `observe` en una respuesta**, con ninguna redacción. Pero **en el banco sí** (§5.3): 97 respuestas con `take_action` + `observe` frente a 32 con `take_action` solo. La diferencia puede ser el mensaje de sistema o el patrón de la historia sintética (una llamada por mensaje). Lo decide la partida real (§5.4).
- El trimestre con un solo `observe` se obedece.
- **Lo que sí la hace emparejar (02:30 UTC):** el patrón del historial. Con tres respuestas emparejadas sembradas en la historia (`--paired`), sigue emparejando 4 de 4. Y desde el arranque en frío, **un ejemplo literal del formato de la respuesta** en el Skill y en la instrucción (`cp-v5a`: `tool_calls: [take_action(...), observe(...)]`) la hace emparejar **6 de 6** sin texto; pedir que empiece a emparejar desde la pantalla inicial (`cp-v5b`) no sirve (0 de 6). **Candidato: `cp-v5a`** = cp-v4 + ese ejemplo.

### 5.2 Juez de calidad (`scripts/calidad-skills/judge.py`, Haiku y Sonnet × 3, mismo lote que c5)

| Manual | Haiku | Sonnet |
|---|---:|---:|
| `calidad/v4-c5` | 64,0 · 65,3 | 68,7 · 69,7 |
| `cp-v1` | 64,7 | 62,3 |
| `cp-v2` | 63,3 | 61,0 |
| `calidad/v4-c5` (tercer lote) | 62,7 | 64,0 |
| **`cp-v4`** (mismas reglas, texto más corto) | **64,0** | **69,3** |
| `calidad/v4-c5` (cuarto lote) | 63,3 | 70,7 |
| `cp-v5a` (cp-v4 + ejemplo literal del formato de respuesta) | 62,7 | 65,0 |

Con cp-v1 y cp-v2 Sonnet bajaba 6–8 puntos y repetía tres quejas: la cascada de historias es densa, el arranque atascado y «Best» parecen mecánicas inventadas, la línea de L4 es rígida. `cp-v4` reescribe lo mismo más corto (2.421 palabras) y en su lote queda igual o por encima de c5 con los dos jueces. El juez se mueve ±5 entre lotes: léase «no baja». El ejemplo del formato de respuesta de `cp-v5a` le cuesta a Sonnet ~5 puntos (≈ −0,5 de versión) frente a cp-v4, mientras que las dos llamadas por respuesta que provoca valen ~+2 de versión en fichas: se queda. Dos redacciones más suaves del ejemplo (`cp-v6a`, una frase con el formato en línea; `cp-v6b`, el bloque sin la palabra `tool_calls`) **no emparejan** (0 de 5 cada una en la sonda): lo que dispara la pareja es el bloque literal con el array `tool_calls: [...]`. Se queda el de `cp-v5a` y se acepta el coste en el juez.

### 5.3 Banco de DeepSeek: ¿cambian las elecciones? (`scripts/deepseek/bench.py`, 69 situaciones de hacia-80: 40 de control y 29 de control de riesgo; ~0,13 USD por brazo)

| Brazo | Control (40): pérdida / mejor / arriesgadas | Control de riesgo (29): pérdida / mejor / arriesgadas | Misma elección que v4 (pasada 1) |
|---|---|---|---|
| `t13-read-v4`, pasada 1 (`ds-v4-full10`) | 0,38 / 88 % / 3 | 0,93 / 66 % / 1 | — |
| `t13-read-v4`, pasada 2 (`ds-v4-rep2`) | 0,23 / 92 % / 1 | 0,84 / 66 % / 1 | 64 de 68 |
| `cp-v1b` | 0,77 / 82 % / 2 | 1,04 / 59 % / 0 | 60 de 66 |
| **`cp-v4`** | **0,34 / 90 % / 2** | **0,79 / 66 % / 2** | 62 de 68 (66 de 68 con la pasada 2) |

- **`cp-v4` elige como v4 dentro del ruido de v4 consigo mismo** (62–66 de 68 frente a 64 de 68 entre dos pasadas de v4), con la misma pérdida por decisión. Las reglas nuevas (arranque atascado, tamaño del riesgo, Skill desde L4) no tocan estas situaciones, como se esperaba; lo que se comprueba es que el bucle de silencio y las notas cortas no cambian las elecciones.
- La pasada de `cp-v1b` salió peor (0,77) por dos errores de lectura y dos elecciones más prudentes en el mes previo; la de `cp-v4`, con las mismas reglas, sale igual que v4: era ruido de pasada (una pasada de v4 difiere de otra en 0,15 de pérdida y 4 elecciones).
- Texto visible en el banco: 184 caracteres por situación con cp-v4 (v4: varios cientos); notas 103 caracteres (v4: 258).
- **L1 con la evaluación cerca (90 situaciones, `ids-l1prep90`):** `cp-v5a` 4,42 de pérdida / 59 % mejor / 27 elecciones que bajan Network u Output / 8 arriesgadas; v4 pasada 1: 3,31 / 61 % / 24 / 7; v4 pasada 2: 3,68 / 60 % / 25 / 6. Coincide con v4 en 84 de 90 (v4 consigo mismo: 81 de 90). El exceso de pérdida (~1,0 por decisión) sale casi entero de dos copias de la misma historia (−45 cada una) en las que eligió «corregir en la sala» en vez de la aclaración por escrito; v4 toma esa misma opción 1 de cada 3 veces en el banco. No es una regresión de las reglas: es la moneda al aire de siempre en esa historia (B21).
- **En el banco DeepSeek sí junta `take_action` y `observe` en una respuesta:** 108 respuestas con las dos frente a 27 con `take_action` sola (cp-v4); 97 frente a 32 (cp-v1b). En el runner real no (§5.4).

### 5.4 Partidas oficiales

**`cp-v3` (una llamada por respuesta), hueco 1, 02:02–03:10 UTC: 56,92, 48 meses, 57,4 M de fichas (1,20 M por mes, nota de fichas 72,1), 1,73 USD.**
- Fichas: 390 llamadas (182 `observe`, 204 `take_action`); el historial crece 561 por llamada (423 de herramientas y envoltorio, 138 del modelo: `session_id`, `call_goal` en chino, nota de 89 caracteres y 66 caracteres de texto). Trimestres con un `observe`. Sólo la respuesta inicial lleva dos llamadas. La proyección de §2 para este bucle (~72) se cumple.
- Juego: L2 en el mes 12 (perdió el del 6 con Output 1), L3 en el 18, L4 en el 30, y ahí se queda (Skill 44 → 95, 2,8 al mes; L5 exige llegar a tiempo). Health baja toda la partida (4 en el mes 3, 5 al final), dinero 23,7, Network 36, riesgo final 1 (RR. HH. frowning en los meses 12 y 37–39, sin explosión). Las reglas nuevas se cumplen: Skill learning y Apply for rotation en todos los trimestres de L4 salvo cuando RR. HH. pedía Defuse y Lay low.
- Auditoría de decisiones contra el catálogo (`real_audit.py`): elige la mejor opción el 67 % en L1, 60 % en L2, 88 % en L3 y 64 % en L4 (las dos partidas completas de v4: 61 %, 90 %, 78 %, 83 %). El exceso de L4 viene de preferir Health, que estaba baja. No hay señal de que el silencio empeore las historias; es una partida de la cola baja de la familia (v5 y v7 sacaron 66,7 y 67,3; una de v4 se quedó en L1).
- **Coste:** 1,73 USD por 57 M de fichas, cuando v4 pagó 0,81 por 70 M: el proveedor que sirvió esta partida cobra más (la ruta la fija la organización). Cuenta para el presupuesto, no para la nota.

**`cp-v5a` (dos llamadas por respuesta), partida 1, hueco 2, 02:32–03:27 UTC: 66,27, 48 meses, 31,4 M de fichas (654 mil por mes, nota de fichas 93,8), 1,06 USD.**
- Fichas: 221 llamadas al modelo (178 `observe`, 201 `take_action`); **162 respuestas con dos llamadas**, 58 con una (trimestres y arranque). El historial crece 913 por llamada (dos llamadas) y la última petición lleva 238 mil fichas. **La proyección de §2 se cumple: la pareja de llamadas baja las fichas de 1,43 M a 0,65 M por mes.**
- Juego: L2 en el mes 12 (en el mes previo al 6 eligió una opción leída como segura que costó un punto de Output: la trampa de L1 de siempre), L3 en el 18, L4 en el 30 (una ventana perdida en L3 con RR. HH. frowning), L5 en el 48 (Skill 108 en el 42 con RR. HH. uneasy/frowning: ventana perdida; promoción en la última evaluación). Final: Skill 112, Network 36 (techo de L4), Output 28, dinero 24, Health y Dignity 10, riesgo 0. Desde L4, Skill learning y Apply for rotation en todos los trimestres sin RR. HH. inquieto (Skill 42 → 108 en 18 meses, 3,7 al mes; v4: 2,7).
- Auditoría: mejor opción el 62 % en L1, 100 % en L2, 64 % en L3, 82 % en L4 (v4: 61 / 90 / 78 / 83). Lo mismo que v4 dentro de lo que una partida permite ver.

**Lectura de las dos partidas nuevas (56,9 y 66,3) frente a las de v4 (71,7 y 70,2, y una atascada en L1):** las dos pierden el ascenso del mes 6 por un punto en el mes previo y llegan a cada nivel seis meses más tarde; Health anda baja en todas (también en las de v4) y come trimestres. Nada de eso lo causa el bucle de llamadas: el banco dice que elige igual que v4 (§5.3) y la auditoría también. Son dos partidas de la mitad baja de la familia t13 (v5 66,7; v7 67,3; v4 15 atascada), y con n = 2 no se puede separar más. **Partidas 2 y 3 de `cp-v5a` en juego** (huecos 1 y 2, desde las 03:15 y 03:30).

**Cuenta de la versión.** Nota de versión = 0,8 × partidas + 0,1 × calidad + 0,1 × fichas. Con calidad ~64 (juez de Claude) y fichas 94, `cp-v5a` saca **0,8 × P + 15,8**; v4, con calidad ~62 y fichas ~63, **0,8 × P + 12,5**. La pareja de llamadas vale **+3,3 de versión** a igualdad de partidas, así que cp-v5a sólo pierde frente a v4 si su media de partidas fuera más de 4 puntos peor, y no hay ninguna medida que lo diga.

## Gasto
- Clave al empezar (29 oct, 01:00 UTC): 32,60 USD libres (17,40 usados).
- Sondas `turnprobe` (13 tandas): ~0,30 USD. Bancos `ds-cp1b`, `ds-v4-rep2`, `ds-cp3`, `ds-cp4`: ~0,53. Partida `cp-v3`: 1,73. Partida `cp-v5a` 1: 1,06; partidas 2 y 3 en juego (~1 USD cada una). **Total hasta las 03:35: ~3,7 USD, con ~2 USD comprometidos.**

## Relevo (29 oct, 03:40 UTC)
1. **Hecho y por qué.** §2–§5. Lo nuevo desde las 02:10: `cp-v3` jugado (56,92; fichas 72 con una llamada por respuesta); descubierto que el patrón del historial decide si DeepSeek junta `take_action` y `observe`, y que un ejemplo literal del formato lo provoca desde frío (`cp-v5a`, 6 de 6 en la sonda; 162 de 221 respuestas en la partida real); `cp-v5a` jugado: 66,27 con 654 mil fichas por mes (nota de fichas 94). Juez: cp-v4 = c5; cp-v5a ~5 por debajo con Sonnet por el bloque del ejemplo. Banco: cp-v4 elige como v4 dentro del ruido de v4 consigo mismo.
2. **Resultados.** Tablas de §5. Partidas en `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-{b37dbff8,255b856f}-*`; registro en `~/careerlab-data/comprobante/games/`. Gasto ~3,7 USD más dos partidas en juego.
3. **A medias.** Partidas 2 y 3 de `cp-v5a`; sondas `cp-v6a`/`cp-v6b` (el ejemplo escrito de forma que el juez no castigue); la recomendación de cortes, que depende de las dos partidas.
4. **Siguiente paso.** Al terminar las partidas: `gametokens.py` sobre cada una, media de las tres, nota de versión estimada, y recomendación en la cabecera de este informe. Si `cp-v6a` o `cp-v6b` emparejan en la sonda, pasarlas por el juez y, si suben, entregar esa variante (mismas reglas). Comandos en el Relevo anterior; además:
   ```bash
   python3 scripts/comprobante/gametokens.py ~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-255b856f-*
   uv run python scripts/deepseek/real_audit.py ~/careerlab-data/huawei-deepseek/runs/<run>/events.jsonl
   ```
