# Comprobante: el mejor manual para los cortes 2 y 3

**Conclusión (29 oct, 04:50 UTC).** **Entregar en el corte 2 `comprobante/cp-v5a`.** Son las reglas de `t13-read-v4` tal como las reescribió Calidad (`v4-c5`), más el trimestre de Skill desde el nivel 4 (`techo/v4-t0`), el rescate del arranque atascado y el tamaño del riesgo (`suelo-v1-min`), y un **bucle de turno nuevo: una respuesta del modelo por decisión, con `take_action` y `observe` en la misma respuesta, sin texto y con notas de una línea**, que DeepSeek sigue porque el manual trae un ejemplo literal del formato.

- **Fichas: de 1,35–1,47 M por mes (nota 61–66) a 0,62–0,65 M (nota 94–95)** en las tres partidas completas de `cp-v5a`. Vale **+3,2 de nota de versión** a igualdad de partidas. Es la palanca más grande y más barata que quedaba, y nadie la había tocado: las fichas son cuadráticas en el número de llamadas al modelo (§2), el runner ejecuta en orden varias llamadas de una respuesta (§3) y DeepSeek las junta si el manual trae un ejemplo literal del formato (§5.1).
- **Partidas: `cp-v5a` 66,27 · 65,10 · 68,13 (media 66,5), las tres en L5 con riesgo 0.** La familia con las mismas reglas de historias suma seis partidas: cinco completas (media 66,3) y una crisis de confianza (`cp-v7` 3, mes 21). En el banco de DeepSeek elige como v4 dentro del ruido de v4 consigo mismo (§5.3) y la auditoría contra el catálogo da la misma tasa de mejores elecciones (§5.4). Pierde donde v4: el ascenso del mes 6 por un punto leído mal en el mes previo, ventanas en L3–L4 con RR. HH. inquieto y, una vez en seis, la crisis de confianza por opciones «pragmáticas» con RR. HH. frowning.
- **Calidad:** 61–69 con los jueces de Claude, lo mismo que `v4-c5` (v4: 60–64). El ejemplo literal del formato le cuesta ~5 a Sonnet y no se puede quitar sin perder la pareja de llamadas (§5.1, §5.2).
- **Nota de versión esperada: 0,8 × P + 16, con P la media de 3 partidas.** Con P = 66,5 (las tres partidas de cp-v5a), **69,2**; si una de las tres se hunde, ~60. v4 con las mismas partidas daría 0,8 × P + 12,5. **76 no está al alcance con pruebas**: exigiría P ≈ 75, tres partidas por encima de la mejor que ha sacado nadie salvo la de `script-v1` (76,87). Lo medido es un salto de ~3,5 sobre v4 a igualdad de juego.
- **Por qué cp-v5a y no cp-v7 (62,25 · 69,88 · 28,56):** son las mismas reglas salvo una frase; cp-v7 quitaba el «Lay low por Health» del trimestre y su hundimiento vino de un trimestre con Health baja y RR. HH. «quiet» en que no se limpió el riesgo. cp-v5a tiene las tres partidas completas y esa frase protege.
- **Corte 3:** candidato **`cp-v8`** = cp-v5a + «con RR. HH. no tranquilo, Defuse va primero aunque Health esté baja» (§5.4; juez igual que cp-v5a). Tiene una partida de mecánica (abajo). Entregarlo en el corte 3 sólo si la nota oficial del corte 2 confirma las fichas (~95) y hay 2–3 partidas suyas sin regresión; si no, no hace falta otra versión (cuenta la mejor). No cambiar reglas de historias: ninguna probada las mueve (C27).

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
| `cp-v5a` (cp-v4 + ejemplo literal del formato de respuesta) | 62,7 · 64,7 | 65,0 · 60,7 |
| **`cp-v7`** (cp-v5a sin «Lay low por Health» en el trimestre) | **69,3** | **66,7** (mismo lote que el 64,7 / 60,7 de cp-v5a) |
| `cp-v8` (cp-v5a + Defuse primero con RR. HH. no tranquilo aunque Health esté baja) | 64,7 (cp-v5a en el mismo lote: 68,7) | 63,3 (65,0) |

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

**`cp-v5a`, partida 2, hueco 1, 03:15–03:50 UTC: 65,10, 48 meses, 29,5 M de fichas (615 mil por mes, nota de fichas 95,4).** 197 llamadas, 183 respuestas con dos o más llamadas (el patrón se mantiene toda la partida). L2 en el 12, L3 en el 18, L4 en el ~30, L5 antes del 48; Skill 104, Network 36, dinero 24,4, Health y Dignity 20, riesgo 0. Auditoría: mejor opción 72 % en L1, 88 % en L2, 68 % en L3, 73 % en L4.

**`cp-v5a`, partida 3, hueco 2, 03:30–03:58 UTC: 68,13, 48 meses, 30,6 M de fichas (638 mil por mes, nota de fichas 94,5), 0,91 USD.** Ascensos en los meses 6, 12, 18 y 42 (L5); Skill 112, Network 41, dinero 29,2, Health y Dignity 20, riesgo 0. 184 de 197 respuestas con dos o más llamadas.

| Partida | Nota | Fichas por mes | Nota de fichas | Ascensos | Coste |
|---|---:|---:|---:|---|---:|
| `cp-v5a` 1 | 66,27 | 654k | 93,8 | 12, 18, 30, 48 | 1,06 |
| `cp-v5a` 2 | 65,10 | 615k | 95,4 | 12, 18, ~30, <48 | 0,84 |
| `cp-v5a` 3 | 68,13 | 638k | 94,5 | 6, 12, 18, 42 | 0,91 |
| **media `cp-v5a`** | **66,5** | **636k** | **94,6** | | |
| `cp-v7` 1 (cp-v5a sin «Lay low por Health») | 62,25 | 450k | **100** | 6, 12, 18, 30 (L5; Skill 92, dinero 19) | 0,65 |
| `cp-v7` 2 | 69,88 | 769k | 89,3 | 4 ascensos (L5; Skill 122, Network 42, dinero 31,5) | 1,09 |
| `cp-v7` 3 | **28,56** (eliminada, mes 21) | 383k | 50 (tope por no terminar) | 6, 12 (L3); crisis de confianza | ~0,3 |
| `cp-v3` (una llamada por respuesta) | 56,92 | 1.196k | 72,1 | 12, 18, 30 | 1,73 |
| `t13-read-v4` (referencia) | 71,67 · 70,22 · (atascada en L1) | 1.470k · 1.354k | 61,2 · 65,8 | 6, 12, 24, 42 | 0,81 · 0,72 |

**Nota de versión estimada de `cp-v5a`: 0,8 × 66,5 + 0,1 × 65 + 0,1 × 94,6 ≈ 69,2.** Las mismas tres partidas con las fichas y la calidad de v4 darían ~65,8. Con la partida de `cp-v7` la familia nueva suma cuatro partidas completas (media 65,4; v4: dos completas de 71 y una atascada), ninguna hundida.

**El hundimiento de `cp-v7` 3 (crisis de confianza en el mes 21).** Primera explosión en el mes 12: en el trimestre del mes 9, con Health 2 y RR. HH. «quiet», la línea 2 («cerca de un límite») se llevó las 3 de energía a Health recovery y Network, y no hubo Defuse (la línea 3 va después); RR. HH. pasó a frowning (10), uneasy (11) y angry (12). Segunda, en el 21: con RR. HH. frowning en los meses 19–20 eligió «ayudar en silencio a los que se van», «dejarlo ahí para no dejar mal al jefe» y, en el 21, «negarse al traslado». Es la ruta de derrota conocida (C6: opciones «pragmáticas» con RR. HH. inquieto) y el mismo tipo de hundimiento que la familia v4 tuvo con `t13-read-v1`. En la familia nueva: 1 hundimiento en 6 partidas (v4: 1 atascada en 3).

De ahí **`cp-v8`** = cp-v5a + una excepción en la línea 2: si RR. HH. no está tranquilo, Defuse se lleva las dos primeras de energía y la recuperación la tercera. Una partida de mecánica en juego; es el candidato para el corte 3, no para el 2 (sin partidas).

`cp-v7` 1 gastó aún menos (167 llamadas: los 16 trimestres enteros en una respuesta cada uno, 163 `observe` para 204 acciones) y sacó la nota de fichas máxima, 100. Su juego fue el más flojo de los cuatro (Skill 92, dinero 19): la auditoría da 75 % / 70 % / 79 % / 80 % de mejores elecciones en L1–L4, como las demás; la diferencia está en la suerte de las historias, no en una regla distinta (sólo cambia la frase del trimestre con Health baja, que esta partida no usó en el mes 3).

**Lectura de las dos partidas nuevas (56,9 y 66,3) frente a las de v4 (71,7 y 70,2, y una atascada en L1):** las dos pierden el ascenso del mes 6 por un punto en el mes previo y llegan a cada nivel seis meses más tarde; Health anda baja en todas (también en las de v4) y come trimestres. Nada de eso lo causa el bucle de llamadas: el banco dice que elige igual que v4 (§5.3) y la auditoría también. Son dos partidas de la mitad baja de la familia t13 (v5 66,7; v7 67,3; v4 15 atascada), y con n = 2 no se puede separar más. La tercera partida (68,13) ascendió en el mes 6 y en el 18, como la mejor partida que tenemos hasta el 24.

**Cuenta de la versión.** Nota de versión = 0,8 × partidas + 0,1 × calidad + 0,1 × fichas. Con calidad ~64 (juez de Claude) y fichas 94, `cp-v5a` saca **0,8 × P + 15,8**; v4, con calidad ~62 y fichas ~63, **0,8 × P + 12,5**. La pareja de llamadas vale **+3,3 de versión** a igualdad de partidas, así que cp-v5a sólo pierde frente a v4 si su media de partidas fuera más de 4 puntos peor, y no hay ninguna medida que lo diga.

## Gasto
- Clave al empezar (29 oct, 01:00 UTC): 32,60 USD libres (17,40 usados).
- Sondas `turnprobe` (13 tandas): ~0,30 USD. Bancos `ds-cp1b`, `ds-v4-rep2`, `ds-cp3`, `ds-cp4`: ~0,53. Partida `cp-v3`: 1,73. Partidas `cp-v5a`: 1,06 + 0,84 + 0,91. Banco L1 `ds-cp5a-l1`: 0,12. Partidas `cp-v7`: 0,65 + 1,09 + ~0,3 (eliminada). Partida `cp-v8`: en juego (~0,9). **Total: ~8,6 USD de los 10.**

## Relevo (29 oct, 04:50 UTC)
1. **Hecho y por qué.** Anatomía de fichas de las partidas reales (§2); prueba del runner con un modelo falso (§3); manuales `cp-v1`→`cp-v8` (§4); sondas con DeepSeek del bucle (§5.1); juez (§5.2); bancos de control, riesgo y L1 (§5.3); **8 partidas oficiales** (§5.4): cp-v3 56,92; cp-v5a 66,27 · 65,10 · 68,13; cp-v7 62,25 · 69,88 · 28,56; cp-v8 en juego. La conclusión y la recomendación de cortes están en la cabecera.
2. **Resultados.** Tablas de §2–§5. Partidas en `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-{b37dbff8,255b856f,d650b363,64fa828b}-*`; registro de lanzamientos en `~/careerlab-data/comprobante/games/`; sondas y modelo falso en `~/careerlab-data/comprobante/`; bancos en `~/careerlab-data/deepseek/runs/ds-cp*`; juez en `lab/reports/deepseek/comprobante-data/`. Gasto ~8,6 USD (medido con `total_cost` y `cost`).
3. **A medias.** La partida de mecánica de `cp-v8`; el juego de DeepSeek en las partidas tiene la varianza de siempre (62–70 cuando termina, 1 de 6 se hunde) y 8 partidas no la reducen.
4. **Siguiente paso.** Para el otro chat: empaquetar `lab/policies-src/comprobante/cp-v5a/bundle` para el corte 2 (lint limpio; documentos de diseño: el bucle de una respuesta por decisión hay que explicarlo en `skills_design.md`). Para esta línea: leer la partida de `cp-v8` con `gametokens.py`; si queda presupuesto y Alejandro lo aprueba, 2 partidas más de `cp-v8` antes del corte 3. Comandos:
   ```bash
   cd ~/huawei-comp && export CAREERLAB_ORIGIN=deepseek CAREERLAB_RUNNER_DIR=~/huawei/local-runs/official-runner CAREERLAB_TARGET_ENV=~/huawei/local-runs/official-runner/.env CAREERLAB_TARGET_PARALLEL=1 CAREERLAB_TARGET_NEVER_STOP=1
   uv run python -m careerlab.target play --policy cp-v8 --spend --games 1 --slot 1 --max-usd-per-game 3 --reserve-usd 15 --purpose pilot --why "..."
   python3 scripts/comprobante/gametokens.py ~/careerlab-data/huawei-deepseek/runs/<run>
   uv run python scripts/deepseek/real_audit.py ~/careerlab-data/huawei-deepseek/runs/<run>/events.jsonl
   ```
