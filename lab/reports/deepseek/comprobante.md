# Comprobante: el mejor manual para los cortes 2 y 3

**Conclusión (29 oct, 04:50 UTC).** **Entregar en el corte 2 `comprobante/cp-v5a`.** Son las reglas de `t13-read-v4` tal como las reescribió Calidad (`v4-c5`), más el trimestre de Skill desde el nivel 4 (`techo/v4-t0`), el rescate del arranque atascado y el tamaño del riesgo (`suelo-v1-min`), y un **bucle de turno nuevo: una respuesta del modelo por decisión, con `take_action` y `observe` en la misma respuesta, sin texto y con notas de una línea**, que DeepSeek sigue porque el manual trae un ejemplo literal del formato.

- **Fichas: de 1,35–1,47 M por mes (nota 61–66) a 0,62–0,65 M (nota 94–95)** en las tres partidas completas de `cp-v5a`. Vale **+3,2 de nota de versión** a igualdad de partidas. Es la palanca más grande y más barata que quedaba, y nadie la había tocado: las fichas son cuadráticas en el número de llamadas al modelo (§2), el runner ejecuta en orden varias llamadas de una respuesta (§3) y DeepSeek las junta si el manual trae un ejemplo literal del formato (§5.1).
- **Partidas: `cp-v5a` 66,27 · 65,10 · 68,13 (media 66,5), las tres en L5 con riesgo 0.** La familia con las mismas reglas de historias suma seis partidas: cinco completas (media 66,3) y una crisis de confianza (`cp-v7` 3, mes 21). En el banco de DeepSeek elige como v4 dentro del ruido de v4 consigo mismo (§5.3) y la auditoría contra el catálogo da la misma tasa de mejores elecciones (§5.4). Pierde donde v4: el ascenso del mes 6 por un punto leído mal en el mes previo, ventanas en L3–L4 con RR. HH. inquieto y, una vez en seis, la crisis de confianza por opciones «pragmáticas» con RR. HH. frowning.
- **Calidad:** 61–69 con los jueces de Claude, lo mismo que `v4-c5` (v4: 60–64). El ejemplo literal del formato le cuesta ~5 a Sonnet y no se puede quitar sin perder la pareja de llamadas (§5.1, §5.2).
- **Nota de versión esperada: 0,8 × P + 16, con P la media de 3 partidas.** Con P = 66,5 (las tres partidas de cp-v5a), **69,2**; si una de las tres se hunde, ~60. v4 con las mismas partidas daría 0,8 × P + 12,5. **76 no está al alcance con pruebas**: exigiría P ≈ 75, tres partidas por encima de la mejor que ha sacado nadie salvo la de `script-v1` (76,87). Lo medido es un salto de ~3,5 sobre v4 a igualdad de juego.
- **Por qué cp-v5a y no cp-v7 (62,25 · 69,88 · 28,56):** son las mismas reglas salvo una frase; cp-v7 quitaba el «Lay low por Health» del trimestre y su hundimiento vino de un trimestre con Health baja y RR. HH. «quiet» en que no se limpió el riesgo. cp-v5a tiene las tres partidas completas y esa frase protege.
- **Corte 3:** candidato **`cp-v8`** = cp-v5a + «con RR. HH. no tranquilo, Defuse va primero aunque Health esté baja» (§5.4; juez igual que cp-v5a). Su partida de mecánica: 68,20 (L5, Skill 134, Network 54, pero riesgo final 5: la mejor trayectoria de la familia, con un riesgo sin limpiar al final que costó 5 puntos), 660 mil fichas por mes, 187 respuestas con dos llamadas. Entregarlo en el corte 3 sólo si la nota oficial del corte 2 confirma las fichas (~95) y hay 2–3 partidas suyas sin regresión; si no, no hace falta otra versión (cuenta la mejor). No cambiar reglas de historias: ninguna probada las mueve (C27).

**Actualización (29 oct, 11:05 UTC).** Segunda partida de `cp-v8`: **28,28, atascada en L1 y despedida en el mes 24, y sin el bucle de fichas** (DeepSeek narró desde la primera respuesta y no emparejó las llamadas; §5.4). `cp-v8` queda 68,20 · 28,28 y **`cp-v5a` sigue siendo la red de seguridad del corte 2**. Dos correcciones a la lectura anterior: (1) **los 5 puntos de control de riesgo de la primera partida de cp-v8 fueron una explosión en el mes 38**, no riesgo sin limpiar al final: la nota de riesgo resta 5 por explosión (fórmula del motor en la réplica, `score()`), el comentario de RR. HH. era sonriente en los meses 47–49 y el riesgo final 0; ninguna regla de cierre los recupera (responde a la hipótesis §1 de `revision-comprobante.md`, PR #23). (2) **El bucle de una respuesta por decisión es bimodal por partida** (7 de 8 partidas, 1 de 4 sondas hoy frente a 13 de 13 ayer): cuando el modelo arranca narrando no se corrige. La auditoría de las 13 partidas (§6) dice dónde están los puntos: el mes en que se llega a L5 (4–5 puntos: Network y dinero), la trampa estructural de L1 (una pérdida forzada de Network u Output en el 57 % de los meses previos para un lector estricto) y las explosiones. Candidato `cp-v9` (§6.6), sólo si gana en banco, réplica y juez; reglas de trabajo de Alejandro en §6.8.

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
| `cp-v8` 1 (cp-v5a + Defuse primero con RR. HH. no tranquilo) | 68,20 | 660k | 93,6 | 4 ascensos (L5 pronto; Skill 134, Network 54, dinero 36,8, **riesgo final 5**) | 0,86 |
| `cp-v3` (una llamada por respuesta) | 56,92 | 1.196k | 72,1 | 12, 18, 30 | 1,73 |
| `t13-read-v4` (referencia) | 71,67 · 70,22 · (atascada en L1) | 1.470k · 1.354k | 61,2 · 65,8 | 6, 12, 24, 42 | 0,81 · 0,72 |

**Nota de versión estimada de `cp-v5a`: 0,8 × 66,5 + 0,1 × 65 + 0,1 × 94,6 ≈ 69,2.** Las mismas tres partidas con las fichas y la calidad de v4 darían ~65,8. Con la partida de `cp-v7` la familia nueva suma cuatro partidas completas (media 65,4; v4: dos completas de 71 y una atascada), ninguna hundida.

**El hundimiento de `cp-v7` 3 (crisis de confianza en el mes 21).** Primera explosión en el mes 12: en el trimestre del mes 9, con Health 2 y RR. HH. «quiet», la línea 2 («cerca de un límite») se llevó las 3 de energía a Health recovery y Network, y no hubo Defuse (la línea 3 va después); RR. HH. pasó a frowning (10), uneasy (11) y angry (12). Segunda, en el 21: con RR. HH. frowning en los meses 19–20 eligió «ayudar en silencio a los que se van», «dejarlo ahí para no dejar mal al jefe» y, en el 21, «negarse al traslado». Es la ruta de derrota conocida (C6: opciones «pragmáticas» con RR. HH. inquieto) y el mismo tipo de hundimiento que la familia v4 tuvo con `t13-read-v1`. En la familia nueva: 1 hundimiento en 6 partidas (v4: 1 atascada en 3).

De ahí **`cp-v8`** = cp-v5a + una excepción en la línea 2: si RR. HH. no está tranquilo, Defuse se lleva las dos primeras de energía y la recuperación la tercera. Una partida de mecánica en juego; es el candidato para el corte 3, no para el 2 (sin partidas).

`cp-v7` 1 gastó aún menos (167 llamadas: los 16 trimestres enteros en una respuesta cada uno, 163 `observe` para 204 acciones) y sacó la nota de fichas máxima, 100. Su juego fue el más flojo de los cuatro (Skill 92, dinero 19): la auditoría da 75 % / 70 % / 79 % / 80 % de mejores elecciones en L1–L4, como las demás; la diferencia está en la suerte de las historias, no en una regla distinta (sólo cambia la frase del trimestre con Health baja, que esta partida no usó en el mes 3).

**Lectura de las dos partidas nuevas (56,9 y 66,3) frente a las de v4 (71,7 y 70,2, y una atascada en L1):** las dos pierden el ascenso del mes 6 por un punto en el mes previo y llegan a cada nivel seis meses más tarde; Health anda baja en todas (también en las de v4) y come trimestres. Nada de eso lo causa el bucle de llamadas: el banco dice que elige igual que v4 (§5.3) y la auditoría también. Son dos partidas de la mitad baja de la familia t13 (v5 66,7; v7 67,3; v4 15 atascada), y con n = 2 no se puede separar más. La tercera partida (68,13) ascendió en el mes 6 y en el 18, como la mejor partida que tenemos hasta el 24.

**Cuenta de la versión.** Nota de versión = 0,8 × partidas + 0,1 × calidad + 0,1 × fichas. Con calidad ~64 (juez de Claude) y fichas 94, `cp-v5a` saca **0,8 × P + 15,8**; v4, con calidad ~62 y fichas ~63, **0,8 × P + 12,5**. La pareja de llamadas vale **+3,3 de versión** a igualdad de partidas, así que cp-v5a sólo pierde frente a v4 si su media de partidas fuera más de 4 puntos peor, y no hay ninguna medida que lo diga.

**`cp-v8`, segunda partida (hueco 1, 09:08–09:31 UTC, pedida por Alejandro): 28,28, eliminada en el mes 24 sin salir de L1; 15,7 M de fichas en 24 meses (655 mil por mes, nota de fichas 50 por no llegar al mes 48), 0,42 USD.**
- **La trampa de L1 entera:** Health 4 → 1 en los meses 1–2 por tres opciones seguidas que lo bajaban (comer con el equipo a diario con Network ya en su techo, aceptar una revisión de arquitectura y escribir el informe completo); Output −1 en el mes 2. Los tres indicadores estaban en el umbral (S9 N3 O3) desde el mes 3 hasta el 23, y las tres evaluaciones se perdieron por un punto perdido en la última historia del mes previo: mes 5, karaoke con el comité (Network +3 inútil, Health −2) en vez de la opción que subía Output; mes 11, «dejar constancia por correo, factual y profesional» ante un compañero que echa la culpa (Dignity +2, **Network −1**; la única opción sin pérdida tenía riesgo +2); mes 17, pedir carga ligera por un problema de salud (**Output −1**) y la historia del compañero charlatán (Network −1). RR. HH. sonriente hasta el mes 18: el rescate del arranque atascado (B30) no pudo actuar porque lo que faltaba no era riesgo sino los puntos.
- **El bucle de fichas no se disparó:** 1 respuesta con dos llamadas de 184; texto visible en cada respuesta («Story analysis … Applying steps …», 138 mil caracteres en 24 meses), desde la primera respuesta («I'll start by reading the career-rules skill»), antes de leer el Skill. El mismo manual emparejó 187 veces en la partida anterior y las seis de cp-v5a y cp-v7 también: **el bucle es bimodal por partida (7 de 8 bien)**, y cuando el modelo arranca narrando, el ejemplo literal del Skill no lo corrige. cp-v9 lleva el bloque literal también en la instrucción del manifest, que está en el mensaje de sistema de cada llamada.
- Con las dos partidas, cp-v8 queda en 68,20 y 28,28: la regla que lo distingue de cp-v5a (Defuse antes que la recuperación con RR. HH. inquieto) no intervino en ninguna de las dos (riesgo a cero todo el tiempo en la segunda hasta el mes 18).

## 6. Auditoría de las 10 partidas completas de DeepSeek: dónde se pierden los puntos (29 oct, 0 USD)

Datos: `events.jsonl` de las 10 partidas completas de la familia v4 (v4 ×2, v5, v7, cp-v5a ×3, cp-v7 ×2, cp-v8) más las 3 hundidas, leídos con `scripts/comprobante/traj.py` (trayectoria mes a mes) y `riskaudit.py` (decisiones contra el catálogo exacto; sólo investigación). Umbrales y techos salen de la réplica (`replica.py`), nunca van al Skill.

### 6.1 Qué separa una partida de 66 de una de 72 (y del techo de 75,8 en L5)

| Partida | Nota | Nivel | Dinero (de 20) | Skill (de 15) | Riesgo (de 10) | Network (de 10) | Ascensos |
|---|---:|---|---:|---:|---:|---:|---|
| v4 | 71,67 | L5 | 9,6 | 13,1 | 10 | 9,0 | 6 · 12 · 24 · 42 |
| v4 | 70,22 | L5 | 7,6 | 15 | 10 | 7,7 | 6 · 12 · 24 · 42 |
| cp-v7 | 69,88 | L5 | 7,9 | 15 | 10 | 7,0 | 6 · 12 · 24 · 42 |
| **cp-v8** | 68,20 | L5 | 9,2 | 15 | **5** | 9,0 | 6 · 12 · 24 · **36** |
| cp-v5a | 68,13 | L5 | 7,3 | 14 | 10 | 6,8 | 6 · 12 · 18 · 48 |
| v7 | 67,27 | L5 | 8,4 | 13,3 | 10 | 5,7 | 6 · 18 · 30 · 48 |
| v5 | 66,71 | L5 | 6,8 | 13,1 | 10 | 6,8 | 6 · 18 · 30 · 48 |
| cp-v5a | 66,27 | L5 | 6,1 | 14 | 10 | 6,2 | 12 · 18 · 30 · 48 |
| cp-v5a | 65,10 | L5 | 6,1 | 13 | 10 | 6,0 | 12 · 18 · 30 · 48 |
| cp-v7 | 62,25 | L5 | 4,8 | 11,5 | 10 | 6,0 | 12 · 24 · 36 · 48 |

Salud y dignidad valen 15 de 15 en las diez. **Lo que separa las partidas es cuándo llegan a L5**: el sueldo pasa de 0,7 a 1,0 al mes (dinero) y, sobre todo, en L4 Network no puede pasar de 36 y en L5 sí (hasta 54; la nota de Network da 100 con 60). Una partida que entra en L5 en el mes 36 acaba con Network ~54 (9 de 10) y dinero ~37; una que entra en el 48 acaba con Network 36–41 (6–7) y dinero 24–29. La diferencia son **4–5 puntos de nota de partida**. La familia cp-v5a no juega peor las historias (§5.3): sus tres partidas perdieron el ascenso del 18 o del 6 y llegaron a L5 en el 48.

**cp-v8 (68,20) es la mejor trayectoria de las diez** (L5 en el 36, Skill 134, Network 54, dinero 37) y perdió 5 puntos de control de riesgo por una explosión en el mes 38 (§6.5), más el dinero y el Output que se lleva la explosión: sin ella habría sido una partida de ~73–74.

### 6.2 Qué indicador bloquea cada ascenso perdido

Comparando el estado del mes previo con el umbral de la réplica, en las 10 partidas completas y la de cp-v3 (48 meses en L4):

| Nivel | Ascensos perdidos | Faltaba Skill | Faltaba Network | Faltaba Output |
|---|---:|---:|---:|---:|
| L1 (mes 6) | 4 (+3 en la partida hundida de cp-v8) | 0 | 1 | las otras por un punto perdido en la última historia del mes previo (§6.3) |
| L2 | 1 | 0 | 1 | 0 |
| L3 | 8 | 4 | 3 | 5 |
| **L4** | **17** | **21** | 1 | **12** |
| L5 | 3 | 4 | 1 | 3 |

- **L4 es el cuello de botella de todas las partidas:** entre el techo de L3 y el umbral de L4 hay casi 50 puntos de Skill, y las historias dan ~3,1 al mes en L4. El trimestre de `v4-t0` (Skill learning + rotación) añade ~1 al mes: es lo que llevó a cp-v8 a L5 en el 36 (Skill 46 en el mes 24, 90 en el 35, justo). Output también falta en L4 en 12 ocasiones: crece 0,4 al mes en las historias y DeepSeek casi nunca elige la opción que lo sube.
- **El mes 18 se pierde en L3 por un punto:** cp-v8 llegó con Network 17 (hacía falta 18) tras elegir en el mes 17 «declinar un premio que no era suyo» (Network −2 en el catálogo); el trimestre del mes 12 había gastado 2 Energy en Health recovery (Health 3) en vez de Network. cp-v5a 66,27: Network 16 en el mes 23.
- **L6 en el mes 48 estuvo al alcance de cp-v8 y lo perdió sólo Output:** Skill 131 y Network 54 en el mes 47, Output 24 (hacía falta 32). En L5 Output creció 3 puntos en 12 meses: las historias dan 0,3–0,8 al mes y el trimestre de t0 lo deja fuera (Skill learning + Network maintenance + rotación). En las otras tres partidas que pasaron por L5, Output acabó en 24, 37 y 38 y lo que faltó fue Skill (L5 en el 42: sin tiempo).
- Lo que **no** sirve: las charlas semestrales codifican la nota (A/B/C) con seis plantillas, no el indicador que falta (cp-v5a 68,13, mes 36: «Delivery stayed steady» con Output 19 cuando faltaban 3 de Output). La línea 4 del trimestre («una charla nombró un indicador») no se dispara nunca.

### 6.3 El punto perdido en la última historia antes de la evaluación

Las tres primeras promociones perdidas con la familia v4 (3 de 10 partidas; cada una cuesta ~2–3 puntos de nota al retrasar todo seis meses) vienen de una opción honesta con un coste invisible en el mes 5:
- «Thanking a colleague from the next team»: Dignity +2, Health +1, Network +3, **Output −1** (Output 3 → 2; la única opción sin ese coste tenía riesgo +2);
- «Named on a department award you did not work on»: Dignity +2, **Network −2** (Network 3 → 1; la única opción que lo conservaba tenía riesgo +2);
- «The gym after work, or staying late»: Dignity +1, Health +2, **Output −1**, con Health baja (el paso 3, bienestar, ganó al paso 4); la opción «quedarse» era segura y subía Output.

En el catálogo (936 opciones), **las opciones que suben Dignity 2 o más cuestan Network el 42 % de las veces y Network u Output el 54 %**; las que suben Health 2 cuestan Output el 52 %. Las que suben Dignity 1 son las más seguras (23 %). Es la regularidad que DeepSeek no ve (B17): el gesto de integridad fuerte cuesta Network; el descanso cuesta Output. cp-v9 lo dice en el paso 4 y hace que, en el mes previo, el paso 4 vaya antes que el de bienestar.

### 6.4 Riesgo: dónde sale mal con el manual actual

- **Elecciones arriesgadas con alternativa segura: sólo 19 en 9 partidas (~2 por partida)**, siempre de +1 y casi siempre las mismas tres historias («dual-write canary», «challenge the framing with data», «light-touch mentoring»). El filtro de riesgo del manual funciona.
- **La explosión de cp-v8 (mes 38)** vino de dos historias seguidas del mes 37 en que las dos opciones eran arriesgadas (cultura tóxica: carta firmada a RR. HH. y al CEO frente a «ayudar en silencio a los afectados»; relación no declarada de un jefe: denuncia anónima frente a «no decir nada, es su vida privada»). Eligió «en silencio» y «anónimo» siguiendo la regla del tamaño del riesgo, y el comentario de RR. HH. pasó de sonriente a explosión en un mes: **el comentario mensual no puede frenar una racha dentro del mes**. Las dos historias no están en el catálogo, así que no sabemos qué opción era la buena.
- **Cuántas explosiones:** 1 en las 10 partidas completas; 2 crisis de confianza en 13 partidas largas (cp-v7, t13-read-v1). Tras la primera explosión, la segunda llegó en 9 y 22 meses con el manual siguiendo las reglas normales. El cierre tras explosión (B35: leer el comentario un paso peor el resto de la partida) está en cp-v9.

### 6.5 Réplica (lectura exacta, 2.000 partidas, `scripts/comprobante/cpbot.py` sobre `techobot`)

| Variante sobre `qskill=4` (t0) | Nota | L6 | Crisis | Output final |
|---|---:|---:|---:|---:|
| t0 (base) | 59,8 | 25 % | 179 | 31,9 |
| L5: Energy a informes, proyecto clave | 59,9 | 24 % | 176 | 34,7 |
| **L5: Skill learning + informe, proyecto clave** (cp-v9) | 59,8 | 26 % | 178 | 34,3 |
| Trimestre al indicador que menos ha crecido desde el ascenso | 59,8 | 21 % | 179 | 33,3 |
| … sabiendo los techos | 60,8 | 28 % | 182 | 34,0 |
| Trimestre al indicador más lejos del umbral real (cota) | 60,2 | 26 % | 179 | 33,5 |
| **Cierre tras explosión** (cp-v9) | 59,6 | 20 % | **148** | 31,0 |
| Contar las pérdidas de Health en Crecer | 59,1 (más despidos en L1) | 22 % | 160 | 30,9 |

Con lectura ruidosa (misma batería): cierre tras explosión 41,0 frente a 40,9, crisis 576 frente a 639. Lectura: **el trimestre de L5 no mueve la media en la réplica** (el planificador óptimo gana por las historias, no por el trimestre, como ya dijo Techo), pero sí sube Output ~2,5 sin bajar Skill, que es justo lo que le faltó a cp-v8 para L6. El cierre tras explosión cuesta 0,2 en lectura exacta y recorta las crisis un 10–17 %.

### 6.6 Candidato `cp-v9` (`lab/policies-src/comprobante/cp-v9`): lo que pasó las pruebas y lo que no

**Texto final: cp-v8 más dos reglas de trimestre y cierre, ninguna de historias** (lint: 13 avisos REVIEW, los de cp-v8 más uno por «Health above 4»; 2.707 palabras frente a 2.507):
1. **Tras una explosión**, el resto de la partida se lee el comentario de RR. HH. un paso peor (sonriente = quiet → Defuse cada trimestre; quiet = frowning → también Lay low), y la excepción del mes previo deja de aplicarse (B35; réplica §6.5: crisis −10 a −17 %, −0,2 de nota con lectura exacta).
2. **Trimestre desde L5 (línea 6 nueva):** Skill learning + Prepare report materials y Apply for a key project; L4 sigue como t0. Neutro en la réplica, +2,5 de Output final; es lo que le faltó a cp-v8 para L6 en el mes 48.
3. El manifest se queda **en prosa**: el bloque literal `tool_calls: [...]` dentro de la instrucción rompió el emparejamiento en una sonda en frío (0 de 6, en la que con el manifest en prosa salió 6 de 6 con el mismo Skill; las dos servidas por DeepInfra, §6.9).

**Tres reglas de historias probadas y quitadas el mismo día** (regla 3 de §6.8: una regla de historias pasa primero por el banco):
- pista de lectura del catálogo en el paso 4 (implicar a otros casi nunca cuesta Output; el gesto de integridad fuerte cuesta Network la mitad de las veces);
- «no se mueve»: un indicador igual a su Best en las tres últimas notas no cuenta como subida;
- el paso 4 antes que el de bienestar en N = 1.

Banco `ds-cp9-l1` (90 situaciones de L1 con la evaluación cerca, 0,12 USD, servido por DeepInfra): **pérdida 4,20 por decisión, 61 % mejor, 28 elecciones que bajan Network u Output, 5 arriesgadas**, frente a v4 3,31 / 3,68 (24–25; 6–7) y cp-v5a 4,42 (27; 8). Las tres reglas juntas no mueven las elecciones de DeepSeek en el mes previo (28 frente a 27), como ya pasó con `t13-read-v9` (hacia-80 §6): **segunda vez en la misma dirección sin resultado → se cierra la dirección** (regla 5). La primera versión de «no se mueve» hablaba de «techo por nivel» y le valió un 0 del juez Haiku por contradecir el rango publicado (0–sin tope) de los tres indicadores; reescrita como «no se mueve», el juez volvía a cp-v8 (`j-cp9c`: Haiku 63 / Sonnet 65 frente a 64 / 63), pero tampoco pasó el banco.

**Réplica, excepción del mes previo estrecha frente a ancha** (`rfnarrow`): si en N = 1 sólo se protegen las opciones sin pérdida cuyo riesgo real es 1 como mucho (lo que DeepSeek hace de hecho), frente a protegerlas todas (lo que dice el texto y hace el bot): 59,65 frente a 59,83; despidos 218 frente a 175, crisis 149 frente a 179. **Ampliar la excepción en el texto vale +0,2 en la réplica**: no merece banco ni partida.

Juez del texto final (`j-cp9d.jsonl`, Haiku y Sonnet × 3, misma tanda que cp-v8): **cp-v9 64,3 / 62,0 frente a cp-v8 59,7 / 63,3**, sin ceros: empate dentro del ruido (±5).

Qué cambiaría una decisión de entrega: nada de cp-v9 toca las historias ni el bucle; sus dos reglas sólo actúan tras una explosión o desde L5. Con 3 partidas (~2,7 USD) no se puede ver una diferencia de +0,3–0,5 de media: **cp-v9 no se juega** (regla 4). Es la base para el corte 3 sólo si Alejandro prefiere llevar las dos reglas de la réplica sin partidas; con pruebas, cp-v5a.

### 6.7 Lo que falta, en números, y qué manual es el ganador

- **La esperanza matemática de la familia v4 hoy** (13 partidas largas con las reglas de historias de v4): 10 completas de media 66,6, 2 hundidas (L1 y crisis), 1 con explosión. E[partida] ≈ 0,85 × 67 + 0,15 × 28 ≈ **61**; nota de versión esperada ≈ 0,8 × 61 + 6,5 + 9,5 ≈ **65**; si las tres partidas oficiales se completan, ≈ 69–70. **Cada hundimiento evitado en las tres partidas oficiales vale ~13 puntos de media y ~10 de versión**: es la variable que manda, por encima de cualquier regla de crecimiento (que vale 1–2).
- **El hundimiento de L1 es estructural, no sólo de lectura:** en el catálogo, en el 24 % de las historias no hay ninguna opción sin riesgo que no cueste Network u Output; en un mes previo de tres historias, un lector perfecto y estricto con el riesgo tiene una pérdida forzada el 57 % de las veces. Por eso el bot de la réplica con lectura exacta asciende en el mes 6 sólo el 73 % y se queda atascado el 9 %, igual que DeepSeek (7 de 10 completas en el mes 6; 2 atascadas de 13). La única salida es aceptar un riesgo pequeño en ese mes cuando toda opción segura pierde un punto (el planificador óptimo pasa del 61 % al 78 % con eso, B36); la regla ya está en v4 desde v3 pero DeepSeek la aplica estrecha («riesgo leve: en privado, parcial, después»), y en el mes 11 de la segunda partida eligió Network −1 antes que la opción con riesgo +2 que salvaba el ascenso. Ampliar esa excepción sólo en el nivel inicial («antes que cualquier riesgo salvo ocultar o negar») es lo siguiente a probar en el banco de L1; en la réplica no se distingue, porque el bot ya la aplica entera.
- **El bucle de fichas es bimodal** (7 de 8 partidas): cuando falla, la partida cuesta el doble de fichas y la nota de fichas de la versión baja de ~95 a ~85. cp-v9 pone el ejemplo literal también en el manifest; medirlo exige partidas, no sondas (las 13 sondas y 7 partidas emparejaron).
- **Qué separa 66 de 72 dentro de una partida completa:** el mes en que llega L5 (§6.1): Network y dinero valen 4–5 puntos. Lo decide Skill en L4 (t0, en cp-v5a/v8/v9) y no perder el mes 18 en L3 por un punto de Network.
- **Los 5 puntos de riesgo de cp-v8 (68,20) no eran riesgo sin limpiar:** la nota de control de riesgo es 10 − (riesgo final + 5 × explosiones), en décimas (réplica `score()`, validada con 0,3 de error); cp-v8 acabó con RR. HH. sonriente (riesgo 0) y una explosión (mes 38). La hipótesis del PR #23 (§1 de `revision-comprobante.md`: cierre con señal atrasada) no se sostiene en esa traza; lo que evita esos 5 puntos es no explotar en L5, es decir, el riesgo en las historias (§6.4) y el cierre tras explosión no aplica (fue la primera).
- **L6 (+4) es posible pero no controlable:** la trayectoria de cp-v8 lo tuvo a 8 puntos de Output en el mes 47; cp-v9 compra Output desde L5. Con la lectura de DeepSeek la réplica da 2–3 % de L6; una partida real en L6 sería la mejor de las tres y subiría la versión ~3.

**El manual ganador, con la evidencia de hoy:** `cp-v9` es el mejor diseño (todo lo aprendido de las 13 partidas, sin números nuevos), pero **no tiene partidas**. Para el corte 2 se entrega `cp-v5a` (3 de 3 completas, 66,5, fichas 94–95). Para el corte 3, la decisión es de presupuesto: cp-v9 sólo se entrega si consigue 2–3 partidas completas sin regresión (≈ 0,9 USD cada una; la línea va en 8,7 USD de los 10, hasta ~12 si algo promete); si no hay partidas, se queda cp-v5a, que ya cuenta como mejor versión.

### 6.8 Reglas de trabajo para lo que queda (Alejandro, 29 oct, 10:50 UTC)

Presupuesto de la línea hasta ~15 USD en total si cada gasto lo merece. El corte 2 no está cerrado: `cp-v5a` es la red de seguridad y sólo se sustituye por algo que la supere **con pruebas**. Para no caer en «una partida, una regla nueva, otra partida»:
1. Una partida suelta no decide nada: quedarse en L1 pasa 1 de cada 7–9 veces con cualquier manual de la familia. No se cambia una regla por una partida mala ni se da por buena por una buena.
2. Antes de cada idea, mirar la fila X de HALLAZGOS (proteger S/N/O todos los meses de L1 antes del riesgo ya está descartado en la réplica: sube los despidos).
3. Una regla de historias pasa primero por el banco (~0,12 USD por 90 situaciones, `ids-l1prep90` frente a cp-v5a); una de trimestre o de cierre, por la réplica o por las partidas que ya tenemos. Sólo lo que gane ahí merece una partida.
4. Una partida sólo vale si puede cambiar una decisión de entrega; antes de lanzarla se escribe qué se espera ver y qué se hará según salga.
5. Dos intentos seguidos en la misma dirección sin resultado: cambiar de dirección o parar y explicar lo aprendido.

Avisos suyos sobre cp-v9: el uso de «Best» para detectar techos choca con B38 (la marca sólo funciona anclada a un valor) y C18 (DeepSeek no rellena campos que tiene que llevar él); la regla «no se mueve» de cp-v9 usa sólo el campo Best, que sí rellena, y compara con las últimas tres notas, pero **hay que medir en el banco si la aplica** antes de creerla.

### 6.9 El proveedor que sirve la llamada decide el bucle de fichas (29 oct, 11:40 UTC)

`~/careerlab-data/deepseek/calls.jsonl` guarda el proveedor que OpenRouter eligió para cada llamada de las sondas y los bancos (no las partidas: JiuwenSwarm no lo registra). `deepseek-v4-flash` se reparte entre doce proveedores (Baidu 10.736 llamadas, GMICloud 2.531, DeepInfra 674, Parasail 671, Venice 632, SiliconFlow 356, Relace 300, Cloudflare 61 …).

| Sondas en frío (`turnprobe`) | Proveedor | Empareja | Texto visible | Razonamiento oculto |
|---|---|---|---|---|
| cp-v5a, 28–29 oct madrugada | GMICloud, SiliconFlow | 6 de 6 | 0 | sí (200–1.000 por decisión) |
| cp-v5a, 29 oct 10:45 (control) | DeepInfra | 0 de 6 | 387–1.050 caracteres en inglés | **0** |
| cp-v9 (manifest con bloque) | DeepInfra | 0 de 6 | 113–246, chino | 0 |
| cp-v9 (manifest en prosa), sonda 1 | DeepInfra | **6 de 6** | 102–402, chino | 0 |
| cp-v9 (manifest en prosa), sonda 2 | DeepInfra | 0 de 6 | 189–550, chino | 0 |

**Qué proveedores sirven el canal de razonamiento** (las 16.072 llamadas registradas de la línea DeepSeek, bancos y sondas):

| Proveedor | Llamadas | Con razonamiento oculto | Fichas de salida por llamada |
|---|---:|---:|---:|
| Baidu | 10.736 | 100 % | 592 |
| GMICloud | 2.538 | 95 % | 906 |
| **DeepInfra** | 694 | **0 %** | 375 |
| Parasail | 671 | 100 % | 818 |
| Venice | 632 | 100 % | 777 |
| SiliconFlow | 356 | 92 % | 803 |
| Relace | 300 | 100 % | 1.365 |
| Cloudflare | 61 | 98 % | 618 |
| Crusoe, Wafer, DigitalOcean, Azure | 85 | 0 % | 150–510 |

DeepInfra y los cuatro pequeños sirven el modelo sin canal de razonamiento (o sin devolverlo); los demás, con él. En nuestro histórico son el 5 % de las llamadas, pero el 100 % de las de esta mañana: el reparto cambia por horas.

Partidas (sin proveedor registrado, pero con el razonamiento oculto total de `gametokens`): las siete que emparejaron tienen 72–132 mil fichas de razonamiento oculto; la segunda de cp-v8, que narró y no emparejó, **24 mil**. Lectura: **cuando el proveedor no sirve el canal de razonamiento, DeepSeek piensa en voz alta en el contenido, y el texto antes de la llamada rompe el patrón de dos llamadas** (CP3: lo que mantiene la pareja es el historial). Con DeepInfra la pareja sale a cara o cruz en la primera respuesta y luego se mantiene (6 de 6 o 0 de 6). La nota oficial usa «organiser-controlled upstream routing» (`docs/mcp.rst`): si ese proveedor no sirve razonamiento, las fichas de cualquier manual vuelven a ~1,3 M por mes (nota ~65) y lo que queda de cp-v5a es su juego (igual que v4). No podemos elegir el proveedor en la entrega («Do not add OpenRouter provider routing settings»); sí anclarlo en nuestras sondas para medir (`DS_PROVIDER`, sólo en `ds.py`, nunca en el runner). Sondas ancladas de cp-v5a (3 en DeepInfra, 3 en GMICloud, ~0,07 USD): se anotan abajo. Lo que vale medir después, si DeepInfra narra siempre: qué texto consigue la pareja también sin canal de razonamiento (por ejemplo, exigir que la primera respuesta de la carrera, el «Continue», lleve ya las dos llamadas, para sembrar el patrón).

### 6.10 `cp-v10`: la pareja de llamadas sin depender del proveedor (predicción escrita antes de medir)

`lab/policies-src/comprobante/cp-v10` = cp-v9 + un bucle de turno que no depende del silencio: el Turn loop abre con las tres primeras respuestas escritas (`new_game`; `observe`; la pantalla «Continue» ya como pareja `take_action` + `observe`), el paso 2 pide silencio «si puedes» y dice que la pareja no depende del texto («si escribes, una línea corta, y las dos llamadas en la misma respuesta»), y el paso 3 añade «desde la pantalla Continue hasta el último mes»; lo mismo en la instrucción del manifest, en prosa. Lint: 15 avisos REVIEW, sin errores.

**Por qué:** §6.9. Con un proveedor sin canal de razonamiento DeepSeek narra, y la pareja sale a cara o cruz en la primera respuesta de historia; una vez salida, se mantiene (CP3). Si la pareja se siembra en la pantalla Continue y se desacopla del silencio, debería salir aunque narre. Una partida emparejada que narra cuesta ~0,73 M de fichas por mes (nota ~91, tabla de §2) frente a ~1,3 M sin pareja (~65).

**Predicción (antes de las sondas):** ancladas a DeepInfra, cp-v10 empareja en 4 de 5 arranques en frío o más (cp-v5a allí: ~la mitad; control en marcha, 3 sondas); ancladas a GMICloud, sigue en silencio y emparejando. Coste: ~0,06 USD por brazo.

**Decisión según salga:** si se cumple, cp-v10 pasa a candidato del corte 2 en lugar de cp-v5a, con una partida de confirmación (~0,9 USD; lo que la confirmaría: pareja desde la segunda respuesta, fichas < 800 mil por mes, elecciones de historias como siempre; una partida no juzga la nota) y, si Alejandro lo aprueba, dos más antes del corte 3. Si no se cumple (≤ 2 de 5), la pareja no se puede asegurar en proveedores sin razonamiento, se queda cp-v5a y el riesgo queda documentado en CP6 para la entrega.

## Gasto
- Clave al empezar (29 oct, 01:00 UTC): 32,60 USD libres (17,40 usados).
- Sondas `turnprobe` (13 tandas): ~0,30 USD. Bancos `ds-cp1b`, `ds-v4-rep2`, `ds-cp3`, `ds-cp4`: ~0,53. Partida `cp-v3`: 1,73. Partidas `cp-v5a`: 1,06 + 0,84 + 0,91. Banco L1 `ds-cp5a-l1`: 0,12. Partidas `cp-v7`: 0,65 + 1,09 + ~0,3 (eliminada). Partida `cp-v8`: 0,86. Segunda partida `cp-v8` (29 oct, 09:08): 0,42. Banco `ds-cp9-l1`, sonda `turnprobe-cp-v9` y juez: se anotan en el Relevo. Sondas de hoy (cp-v9 ×3, cp-v5a control, 6 ancladas): ~0,13. Banco `ds-cp9-l1`: 0,12. **Total de la línea: ~8,95 USD** (techo nuevo ~15; uso de la clave 17,40 → ~26,4).

## Relevo (29 oct, 05:25 UTC; cierre de la línea)
1. **Hecho y por qué.** Anatomía de fichas de las partidas reales (§2); prueba del runner con un modelo falso (§3); manuales `cp-v1`→`cp-v8` (§4); sondas con DeepSeek del bucle (§5.1); juez (§5.2); bancos de control, riesgo y L1 (§5.3); **9 partidas oficiales** (§5.4): cp-v3 56,92; cp-v5a 66,27 · 65,10 · 68,13; cp-v7 62,25 · 69,88 · 28,56; cp-v8 68,20. La conclusión y la recomendación de cortes están en la cabecera: **cp-v5a al corte 2; cp-v8 candidato al corte 3 si consigue 2–3 partidas sin regresión.**
2. **Resultados.** Tablas de §2–§5. Partidas en `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-{b37dbff8,255b856f,d650b363,64fa828b}-*`; registro de lanzamientos en `~/careerlab-data/comprobante/games/`; sondas y modelo falso en `~/careerlab-data/comprobante/`; bancos en `~/careerlab-data/deepseek/runs/ds-cp*`; juez en `lab/reports/deepseek/comprobante-data/`. Gasto de la línea: 8,26 USD (`total_cost` de las partidas + `cost` de las llamadas).
3. **A medias.** `cp-v8` tiene una sola partida. El juego de DeepSeek conserva la varianza de siempre (62–70 cuando termina, 1 de 7 se hunde); 9 partidas no la reducen y ninguna regla probada mueve las historias.
4. **Siguiente paso.** Para el otro chat: empaquetar `lab/policies-src/comprobante/cp-v5a/bundle` para el corte 2 (lint limpio; en `skills_design.md` explicar el bucle de una respuesta por decisión y por qué ahorra fichas). Para esta línea, con permiso de Alejandro: 2 partidas más de `cp-v8` (~1,8 USD) antes del corte 3 y decidir con las tres. Comandos:
   ```bash
   cd ~/huawei-comp && export CAREERLAB_ORIGIN=deepseek CAREERLAB_RUNNER_DIR=~/huawei/local-runs/official-runner CAREERLAB_TARGET_ENV=~/huawei/local-runs/official-runner/.env CAREERLAB_TARGET_PARALLEL=1 CAREERLAB_TARGET_NEVER_STOP=1
   uv run python -m careerlab.target play --policy cp-v8 --spend --games 1 --slot 1 --max-usd-per-game 3 --reserve-usd 15 --purpose pilot --why "..."
   python3 scripts/comprobante/gametokens.py ~/careerlab-data/huawei-deepseek/runs/<run>
   uv run python scripts/deepseek/real_audit.py ~/careerlab-data/huawei-deepseek/runs/<run>/events.jsonl
   ```

## Relevo (29 oct, 11:10 UTC)
1. **Hecho y por qué.** Segunda partida de `cp-v8` (pedida por Alejandro): 28,28, atascada en L1, sin bucle de fichas (§5.4). Auditoría de las 13 partidas largas con `scripts/comprobante/traj.py` y `riskaudit.py` (§6.1–6.4): descomposición de la nota por dimensión, indicador que bloquea cada ascenso, el punto perdido del mes previo, dónde falla el riesgo. Réplica con `scripts/comprobante/cpbot.py` (§6.5): trimestre de L5, objetivo por indicador, cierre tras explosión, Health en Crecer, proteger S/N/O en N = 2. Candidato `cp-v9` (§6.6). Juez: tres tandas (`comprobante-data/j-cp9*.jsonl`); la frase de «techo por nivel» le valió un 0 de Haiku por contradecir el rango publicado y se reescribió como «no se mueve».
2. **Resultados.** Tablas de §6. Partida 2 de cp-v8 en `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-64fa828b-dff20f-00001-a1`. Sondas en `~/careerlab-data/comprobante/turnprobe-cp-v9*.json` y `turnprobe-cp-v5a-ctrl2.json`: hoy 1 de 4 empareja y las 4 narran (ayer 13 de 13 emparejaban en silencio). Banco `ds-cp9-l1` (90 situaciones de L1, `~/careerlab-data/deepseek/runs/ds-cp9-l1`) lanzado a las 10:40 UTC: comparar con `uv run python scripts/deepseek/bench_sets.py ~/careerlab-data/deepseek/ids-l1prep-set.json ds-v4-full10 ds-v4-rep ds-cp5a-l1 ds-cp9-l1`. Gasto de la línea ~8,9 USD.
3. **A medias.** El banco de cp-v9 y la tercera tanda del juez (`j-cp9c.jsonl`) estaban corriendo al escribir esto. La bimodalidad del bucle no tiene causa conocida (¿proveedor detrás de OpenRouter? el registro de JiuwenSwarm no guarda el `provider`); sin ella medida, la nota de fichas de la versión puede ser ~85 en vez de ~95 si una de las tres partidas oficiales sale narradora.
4. **Siguiente paso.** (a) Leer el banco de cp-v9: si no baja Network u Output menos veces que v4 (24–25 de 90) ni reduce la pérdida, la pista del paso 4 y la regla «no se mueve» no valen y se quitan. (b) Comparar juez `j-cp9c` con cp-v8 en la misma tanda. (c) Sólo si (a) y (b) salen bien: 3 partidas de cp-v9 (~2,7 USD) con la predicción escrita antes (Output comprado desde L5; sin regresión en L1; fichas < 800 mil por mes) y la decisión: entregar cp-v9 en el corte 2 o 3 sólo si las 3 completan con media ≥ 66 y fichas como cp-v5a; si no, cp-v5a. (d) Sobre la bimodalidad: una sonda de 10 arranques en frío de cp-v5a (~0,1 USD) para saber si es del día o del manual.
