# Comprobante: el mejor manual para los cortes 2 y 3

**Conclusión (29 oct, 04:50 UTC).** **Entregar en el corte 2 `comprobante/cp-v5a`.** Son las reglas de `t13-read-v4` tal como las reescribió Calidad (`v4-c5`), más el trimestre de Skill desde el nivel 4 (`techo/v4-t0`), el rescate del arranque atascado y el tamaño del riesgo (`suelo-v1-min`), y un **bucle de turno nuevo: una respuesta del modelo por decisión, con `take_action` y `observe` en la misma respuesta, sin texto y con notas de una línea**, que DeepSeek sigue porque el manual trae un ejemplo literal del formato.

- **Fichas: de 1,35–1,47 M por mes (nota 61–66) a 0,62–0,65 M (nota 94–95)** en las tres partidas completas de `cp-v5a`. Vale **+3,2 de nota de versión** a igualdad de partidas. Es la palanca más grande y más barata que quedaba, y nadie la había tocado: las fichas son cuadráticas en el número de llamadas al modelo (§2), el runner ejecuta en orden varias llamadas de una respuesta (§3) y DeepSeek las junta si el manual trae un ejemplo literal del formato (§5.1).
- **Partidas: `cp-v5a` 66,27 · 65,10 · 68,13 (media 66,5), las tres en L5 con riesgo 0.** La familia con las mismas reglas de historias suma seis partidas: cinco completas (media 66,3) y una crisis de confianza (`cp-v7` 3, mes 21). En el banco de DeepSeek elige como v4 dentro del ruido de v4 consigo mismo (§5.3) y la auditoría contra el catálogo da la misma tasa de mejores elecciones (§5.4). Pierde donde v4: el ascenso del mes 6 por un punto leído mal en el mes previo, ventanas en L3–L4 con RR. HH. inquieto y, una vez en seis, la crisis de confianza por opciones «pragmáticas» con RR. HH. frowning.
- **Calidad:** 61–69 con los jueces de Claude, lo mismo que `v4-c5` (v4: 60–64). El ejemplo literal del formato le cuesta ~5 a Sonnet y no se puede quitar sin perder la pareja de llamadas (§5.1, §5.2).
- **Nota de versión esperada: 0,8 × P + 16, con P la media de 3 partidas.** Con P = 66,5 (las tres partidas de cp-v5a), **69,2**; si una de las tres se hunde, ~60. v4 con las mismas partidas daría 0,8 × P + 12,5. **76 no está al alcance con pruebas**: exigiría P ≈ 75, tres partidas por encima de la mejor que ha sacado nadie salvo la de `script-v1` (76,87). Lo medido es un salto de ~3,5 sobre v4 a igualdad de juego.
- **Por qué cp-v5a y no cp-v7 (62,25 · 69,88 · 28,56):** son las mismas reglas salvo una frase; cp-v7 quitaba el «Lay low por Health» del trimestre y su hundimiento vino de un trimestre con Health baja y RR. HH. «quiet» en que no se limpió el riesgo. cp-v5a tiene las tres partidas completas y esa frase protege.
- **Corte 3:** candidato **`cp-v8`** = cp-v5a + «con RR. HH. no tranquilo, Defuse va primero aunque Health esté baja» (§5.4; juez igual que cp-v5a). Su partida de mecánica: 68,20 (L5, Skill 134, Network 54, pero riesgo final 5: la mejor trayectoria de la familia, con un riesgo sin limpiar al final que costó 5 puntos), 660 mil fichas por mes, 187 respuestas con dos llamadas. Entregarlo en el corte 3 sólo si la nota oficial del corte 2 confirma las fichas (~95) y hay 2–3 partidas suyas sin regresión; si no, no hace falta otra versión (cuenta la mejor). No cambiar reglas de historias: ninguna probada las mueve (C27).

**Actualización (29 oct, 13:50 UTC).** **Candidato del corte 2: `comprobante/cp-v10`** (§6.10): las reglas de historias de cp-v5a sin cambiar, el trimestre de L5 y el cierre tras explosión (réplica, §6.5–6.6), y un bucle de turno que empareja `take_action` + `observe` también cuando el proveedor no sirve el canal de razonamiento (8 de 8 sondas ancladas; partida de confirmación con la pareja en el 100 % sobre un proveedor sin razonamiento; cp-v5a el mismo día, 3 de 6 sondas). Juez igual que cp-v8. **cp-v5a sigue siendo aceptable** si quien empaqueta prefiere no cambiar: la diferencia sólo cuenta si el proveedor de la evaluación no sirve razonamiento (entonces cp-v5a cae a ~1,3 M fichas por mes y cp-v10 se queda en ~0,56 M). La partida de confirmación de cp-v10 se hundió en L1 (22,98), como la segunda de cp-v8: tercer hundimiento en 15 partidas largas de la familia, mismo mecanismo (un punto de Output o Network perdido en el mes previo); por la regla 1 de §6.8 no cambia ninguna regla. Pendiente: banco de L1 anclado por proveedor (§6.10).

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

- **La esperanza matemática de la familia v4 hoy** (15 partidas largas con las reglas de historias de v4, 29 oct 13:30): 10 completas de media 66,6, **3 hundidas** (dos en L1, una crisis), 1 con explosión. E[partida] ≈ 0,8 × 67 + 0,2 × 26 ≈ **59**; nota de versión esperada ≈ 0,8 × 59 + 6,5 + 9,5 ≈ **63**; si las tres partidas oficiales se completan, ≈ 69–70. **Cada hundimiento evitado en las tres partidas oficiales vale ~13 puntos de media y ~10 de versión**: es la variable que manda, por encima de cualquier regla de crecimiento (que vale 1–2).
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

**Partida de confirmación (hueco 1, 13:05–13:27 UTC, `deepseek-pilo-76e845c2-dff20f-00000-a1`, 0,28 USD): 22,98, eliminada en el mes 24 sin salir de L1; la pareja de llamadas en el 100 % de las respuestas (91 de 91 respuestas con dos llamadas; 79 `observe` para 91 `take_action`), con 3.600 fichas de razonamiento oculto en toda la partida (6 % de las llamadas): otra vez un proveedor sin canal de razonamiento, y esta vez el bucle aguantó.** Fichas 6,08 M en 24 meses (253 mil por mes; el historial crece 887 por llamada, de las que 417 las escribe el modelo: narra ~250 fichas por decisión); proyección a 48 meses con ese crecimiento, ~0,56 M por mes (nota de fichas ~98). Texto visible 86 mil caracteres en 24 meses (v4: 393 mil en 48). El trimestre en lote con los números del menú principal aprendidos en el primer trimestre funcionó en los seis trimestres (acción principal correcta en todos; `traj.py` corregido para traducir los lotes).

**Decisión preescrita, cumplida: cp-v10 sustituye a cp-v5a como candidato del corte 2.** Lo que la partida sí decide es el bucle (≥ 90 % pedido; salió 100 %, en el peor tipo de proveedor). Lo que no decide es la nota (regla 1): la partida se hundió en L1 como la segunda de cp-v8 esta mañana, por el mecanismo de siempre (Output 2 en el mes 5, Output 1 en el 11 por «dar las gracias / aclarar» con coste invisible, Network 2 en el 17; RR. HH. frowning en los meses 11–12 y 18–21, uneasy en el 21; Health 2 en el mes 6). Las reglas de historias de cp-v10 son las de cp-v5a, letra por letra.

**Pregunta abierta que la partida deja (no una conclusión):** las dos partidas de hoy servidas sin canal de razonamiento (cp-v8 n.º 2, 24 mil fichas de razonamiento; cp-v10, 3,6 mil) se hundieron en L1; las ocho de la familia servidas con razonamiento (72–132 mil) salieron de L1 (una acabó en crisis en el mes 21). Dos de dos frente a cero de ocho es sugerente, pero los hundimientos antiguos de `t13-read-v1` y `f1` tenían razonamiento al 100 %, y el banco de L1 de esta mañana, servido por DeepInfra, dio la misma pérdida por decisión que con GMICloud (4,20 frente a 4,42). Medido (14:10 UTC) con el mismo banco de 90 situaciones de L1 con cp-v10 anclado a cada proveedor (0,22 USD; `ds-cp10-l1-GMICloud`, 296 llamadas, razonamiento 100 %; `ds-cp10-l1-DeepInfra`, 378 llamadas, razonamiento 0 %):

| Brazo | Pérdida por decisión | Elige la mejor | Baja Network u Output | Arriesgadas |
|---|---:|---:|---:|---:|
| v4, dos pasadas (Baidu/GMICloud) | 3,31 · 3,68 | 61 % · 60 % | 24 · 25 | 7 · 6 |
| cp-v5a (GMICloud) | 4,42 | 59 % | 27 | 8 |
| cp-v10 anclado a GMICloud | 4,25 | 61 % | 26 | 6 |
| **cp-v10 anclado a DeepInfra** | **3,63** | **67 %** | **22** | 7 |

**Sin canal de razonamiento DeepSeek no elige peor** (si acaso algo mejor, dentro del ruido entre pasadas de v4, 0,37). El proveedor cambia la forma de la respuesta (narración, razonamiento oculto, pareja de llamadas), no las elecciones de historias. Los dos hundimientos de hoy son la tasa de siempre de la familia: **3 de 15 partidas largas (20 %)**, todas por la trampa estructural de L1 o por una crisis.

**Resultado (12:20 UTC):** ancladas a DeepInfra, **cp-v10 empareja 5 de 5** (texto visible 160–1.000 caracteres por respuesta, razonamiento oculto 0 en todas); cp-v5a en el mismo proveedor y las mismas horas, 1 de 3 (control), y en GMICloud 2 de 3 (en silencio, con razonamiento). `scripts/comprobante/probeprov.py` junta cada sonda con el proveedor y el razonamiento de `calls.jsonl`. Comprobación en GMICloud (cp-v10 × 3): **3 de 3 emparejan y callan** (0 caracteres salvo 43 en una respuesta; razonamiento oculto 180–1.600): el cambio no rompe el modo silencioso donde existe. En total **8 de 8** sondas ancladas frente a 3 de 6 de cp-v5a el mismo día. Texto final de cp-v10 (tras §6.11): 2.873 palabras, lint 15 avisos REVIEW, 0 errores; juez (`j-cp10.jsonl`, misma tanda que cp-v8): **cp-v10 66,7 / 65,0 frente a cp-v8 62,0 / 65,0** (Haiku / Sonnet), sin ceros.

**Partida de confirmación de cp-v10, lanzada a las 12:50 UTC en el hueco 1 (`~/careerlab-data/comprobante/games/cp-v10-game1.log`); predicción escrita antes de lanzarla (regla 4):** proveedor el que toque. Se espera: pareja `take_action` + `observe` en ≥ 90 % de las respuestas de historia desde la segunda respuesta de la carrera (la pantalla Continue); fichas por mes < 800 mil si se completa (< 700 mil si el proveedor sirve razonamiento y calla); elecciones de historias y trimestres como la familia (auditoría contra el catálogo con `riskaudit.py`; trimestre de L5 con informes y proyecto clave si llega). Lo que decide: **si la pareja sale, cp-v10 sustituye a cp-v5a como candidato del corte 2** (misma red de reglas de historias; dos reglas de trimestre y cierre con respaldo de réplica; bucle robusto al proveedor); la nota de esa partida no decide nada por sí sola (regla 1). Si la pareja no sale (< 60 % de las respuestas de historia), cp-v10 no mejora el bucle en partidas y se queda cp-v5a.

**Decisión según salga:** si se cumple, cp-v10 pasa a candidato del corte 2 en lugar de cp-v5a, con una partida de confirmación (~0,9 USD; lo que la confirmaría: pareja desde la segunda respuesta, fichas < 800 mil por mes, elecciones de historias como siempre; una partida no juzga la nota) y, si Alejandro lo aprueba, dos más antes del corte 3. Si no se cumple (≤ 2 de 5), la pareja no se puede asegurar en proveedores sin razonamiento, se queda cp-v5a y el riesgo queda documentado en CP6 para la entrega.

### 6.11 Lo que dice la auditoría de GPT del corte 2 (`alejandro/gpt-principios`, `auditoria-cut2.md`) y qué se toma

Leída con ojo crítico (29 oct, 12:40 UTC):
- **Se toma.** (1) El trimestre en lote se apoya en «los números del menú no cambian», una afirmación sobre el entorno de desarrollo; el menú de Energy se ve en el `observe` del trimestre (las acciones van en el orden de la tabla del handbook), pero el de la acción principal se elige sin verlo. cp-v10 lo cambia: **en el primer trimestre de la partida, Energy → `observe` → acción principal → `observe`, y los números de ese menú se reutilizan después**; cuesta una llamada por partida y deja de depender de nada aprendido fuera de la partida. (2) El calendario («la charla llega al empezar el mes 6, 12 …; el mes previo es el último que cuenta») y la escala del tamaño del riesgo se escriben como observaciones de nuestras partidas («in our runs»), no como hechos del juego. (3) Si cp-v10 sustituye a cp-v5a, los documentos de `docs/entrega/cut2/` (que GPT ya reescribió para cp-v5a) tienen que describir el bucle nuevo; aviso en pendientes.
- **No se comparte.** (1) Su hipótesis del PR #23 §1 (riesgo 5 por «cierre con señal atrasada»): la fórmula resta 5 por explosión y cp-v8 explotó en el mes 38 con RR. HH. sonriente al final (§6.7). (2) Tratar la pareja de llamadas y el silencio como algo a defender: el propio documento concluye que no hay prohibición y que las llamadas pasan por la interfaz oficial con su validación y su contabilidad; la eficiencia de fichas es un término explícito de la nota. (3) Su estimación de 2,7–6 puntos de fichas por desarmar el lote trimestral entero: no hace falta desarmarlo (ver arriba). (4) «No es una regresión, es la moneda al aire» del banco de L1 lo presenta como conclusión indebida: tiene razón en que 90 situaciones con dos copias no son independientes; se deja como «dentro del ruido medido entre dos pasadas de v4», que es lo que se midió.
- **Pendiente de otros.** Sus P1 sobre los documentos de entrega y las frases «never / exactly two / no text» del manifest: cp-v10 ya pide silencio «si puedes» y la pareja «desde Continue hasta el último mes»; lo demás es del chat que empaqueta.

### 6.12 Para quien empaquete el corte 2, si cp-v10 pasa la partida

Lo que cambia respecto a cp-v5a y debe decir `skills_design.md` (en inglés), sin presentar nada como norma del juego:
1. **Bucle de turno:** cada decisión de historia es una respuesta con dos llamadas, `take_action` y `observe`, desde la pantalla «Continue» hasta el último mes; el runner las ejecuta en orden por la interfaz oficial, con su validación y su contabilidad. El silencio es una preferencia («write no analysis if you can»), no una condición: con proveedores que no devuelven razonamiento el modelo piensa en el contenido y la pareja se mantiene igual (§6.9–6.10). El ahorro viene de la mitad de llamadas al modelo y menos texto repetido, no de alterar nada del juego.
2. **Trimestre:** en el primer trimestre de la partida, Energy → `observe` → acción principal → `observe`, y se apuntan los números de los dos menús en la nota; desde el segundo, el trimestre entero en una respuesta. Así los números salen de la propia partida.
3. **Dos reglas nuevas con respaldo de réplica:** tras una explosión, el resto de la partida se lee el comentario de RR. HH. un paso peor (Defuse cada trimestre; Lay low si no es sonriente); desde el nivel 5 el trimestre compra Skill y Output (Skill learning, Prepare report materials, Apply for a key project), porque en nuestras partidas Output es lo que las historias apenas mueven a ese nivel.
4. **Evidencia que se puede citar:** cp-v5a 66,27 · 65,10 · 68,13 con 615–654 mil fichas por mes (sus tres partidas son del padre, no de cp-v10); cp-v10: 8 de 8 sondas ancladas emparejan (5 en un proveedor sin razonamiento, 3 en uno con razonamiento) frente a 3 de 6 de cp-v5a el mismo día, y la partida de confirmación de §6.10. Las reglas de historias son las de v4-c5 + t0 + suelo-v1-min, sin cambios desde cp-v5a.
5. **Lo que no se dice:** nada de proveedores concretos ni de contar con uno; nada de umbrales; el calendario de evaluaciones y el tamaño del riesgo van como observaciones de nuestras partidas.

### 6.13 Segunda partida de cp-v10 (pedida por Alejandro, 29 oct 14:30 UTC: «olvídate del corte, quiero ver cómo actúa en partidas completas»)

Predicción antes de lanzarla: la pareja de llamadas en ≥ 90 % de las respuestas de historia sea cual sea el proveedor; si el proveedor no sirve razonamiento, narración de ~250 fichas por decisión y 0,5–0,7 M de fichas por mes; si sirve, silencio y ~0,6 M. Juego: la misma familia (ascenso en el mes 6 con ~70 % de probabilidad; L4 en el 24–30; trimestres de L4 con Skill learning y rotación; **si llega a L5, trimestres con Skill learning + Prepare report materials + Apply for a key project**, que es la regla nueva que sólo una partida completa puede enseñar; si hay una explosión, Defuse y Lay low cada trimestre después). Lo que no decide: ninguna regla cambia por su nota (regla 1); lo que sí enseña: si las dos reglas de trimestre y cierre se ejecutan cuando toca, y el coste real de fichas de una partida completa narradora.

**Resultado (hueco 1, 14:33–15:20 UTC, `deepseek-pilo-76e845c2-dff20f-00001-a1`, 0,65 USD): 61,24, completa, L5 en el mes 48; 21,9 M de fichas, 455 mil por mes, nota de fichas 100** con 1.186 fichas de razonamiento en toda la partida (proveedor sin razonamiento, narrando: 364 fichas escritas por llamada) y la pareja en 162 respuestas (163 `observe` para 195 `take_action`). Dimensiones: Skill 96 (12 de 15), Network 34 (5,7), dinero 34 (8,6), riesgo 5 (una explosión en el mes 23).

Lo que enseña, como mecanismo (no como nota):
- **El cierre tras explosión tal como estaba escrito es demasiado caro.** Explosión en el mes 23 (L3); desde el mes 24 hasta el 48, los nueve trimestres fueron Defuse legacy risk + Network maintenance + Lay low and reduce risk, con RR. HH. sonriente en 19 de esos 25 meses: 24 meses sin Skill learning, rotación ni proyecto clave. L4 llegó en el 30 y L5 en el 48; Skill final 96. La réplica (§6.15) confirma que el cierre completo cuesta L6 y Skill, y que basta con Defuse cada trimestre. cp-v11 lo cambia.
- **Output se queda atrás en L3 cuando Skill y Network ya están en su tope.** Meses 17–29: Skill 40–42 y Network 19–21 (sus topes de L3), Output 8–15 cuando el umbral de L4 pedía 14; los trimestres de los meses 12–21 gastaron Skill learning (inútil con Skill en el tope) y un informe. La línea 7 de la familia cp permite Skill learning en L1–L3; la de v4 no (informes, red, informes + proyecto clave), y las dos partidas de v4 llegaron al tope de Output en todos los niveles. cp-v11 vuelve a la orden de v4 en L1–L3 (sin Skill learning).
- **Fichas:** una partida completa narradora con la pareja cuesta 455 mil por mes (100), menos que cp-v5a en silencio (615–654 mil): sin razonamiento oculto las respuestas son más cortas en total aunque narren. El bucle de cp-v10 vale en los dos tipos de proveedor.
- Mes 6: ascendió con Output 3 desde el mes 3 (el trimestre del mes 3 incluyó un informe) pese a Health 3–4 y Network 1 en el mes 5 (recuperado a 3 por la historia siguiente).

### 6.14 Los primeros seis meses de las 14 partidas con registro, y una regla de trimestre que sale de ahí

| Partida | Mes 6 | Health m1–m6 | Output m1–m6 | Trimestre del mes 3 |
|---|---|---|---|---|
| v4 71,67 | sube | 5 4 5 4 2 7 | 0 1 1 3 3 5 | Health, Network, Network + proyecto |
| v4 70,22 | sube | 4 6 8 7 7 7 | 0 −1 1 3 3 5 | Network, informe, Health + proyecto |
| v7 67,27 | sube | 6 5 6 6 5 7 | 1 3 3 3 3 6 | Health, Network, informe + proyecto |
| v5 66,71 | sube | 6 7 5 6 3 4 | 0 1 1 3 3 5 | Skill learning, Network + proyecto |
| cp-v5a 66,27 | **no** | 4 3 6 6 5 6 | 0 3 3 3 3 3 | Health, Network, informe + proyecto |
| cp-v5a 65,10 | **no** | 5 6 5 5 3 8 | 2 3 3 3 3 3 | Network, Skill learning + proyecto |
| cp-v5a 68,13 | sube | 5 4 6 6 3 5 | 0 −1 0 3 3 4 | Health, Network, Network + proyecto |
| cp-v7 62,25 | **no** | 5 4 6 6 6 5 | 1 1 2 3 3 3 | Health, Network, Network + proyecto |
| cp-v7 69,88 | sube | 4 4 6 6 6 5 | 0 0 3 3 3 3 | Health, Network, informe + proyecto |
| cp-v7 28,56 | sube | 5 5 5 5 5 5 | 2 3 3 3 2 3 | Health, Network, informe + proyecto |
| cp-v8 68,20 | sube | 5 4 5 5 6 8 | 0 0 0 3 3 2 | Network, informe, Network + proyecto |
| cp-v8 28,28 | **no** | 4 1 7 7 7 7 | 0 −1 −1 2 2 3 | Health, Health, Network + proyecto |
| cp-v10 22,98 | **no** | 4 4 5 4 4 2 | 0 0 2 2 2 3 | Skill learning, Network + proyecto |
| cp-v3 56,92 | **no** | 4 4 5 4 4 8 | 1 3 3 3 3 1 | Health, Network, informe + Lay low |

- **Network llega a su tope del nivel inicial en el mes 1–2 y Skill en el 3–4; Output es el rezagado:** llega al umbral en el mes 4 en seis partidas y en el mes 6 en las tres atascadas (en dos de ellas bajó a −1 en el mes 2). El trimestre del mes 3 gasta casi siempre en Network maintenance con Network ya en el tope (inútil) y Health recovery; sólo seis de catorce incluyen un informe.
- **De los seis ascensos perdidos en el mes 6:** cuatro tienen una pérdida de Network u Output en una historia del mes 5 (la trampa estructural, §6.3), y dos (cp-v8 n.º 2 y cp-v10) llegaron al mes 5 con Output en 2 porque nunca lo compraron.
- **Réplica (`cpbot.py`, flag `q1out`): en el nivel inicial, Energy a Prepare report materials hasta que Output deje de subir (después Network maintenance), proyecto clave de acción principal:** 60,27 frente a 59,83 con lectura exacta (+0,4) y 41,91 frente a 40,86 con la ruidosa (+1,0; error típico 0,4), con el mismo paso de L1 (91 % / 74 %) y sin más crisis. Es una regla de trimestre, así que la réplica es la prueba que pide la regla 3 de §6.8; se escribe en **`cp-v11`** (= cp-v10 + una frase en la línea 7 y en el manifest: «at your starting level, Prepare report materials comes first with every Energy point that lines 2 and 3 leave»). Lint sin errores; juez en `j-cp11.jsonl`. Health sigue teniendo prioridad (línea 2) y el riesgo también (línea 3).

### 6.15 Réplica: cómo cerrar tras una explosión sin congelar la partida (2.000 partidas por brazo, sobre `qskill=4+q1out`)

| Variante | Exacta: nota / L6 / crisis / Skill final | Ruidosa: nota / crisis |
|---|---|---|
| sin regla tras explosión | 60,27 / 25 % / 175 / 127 | 41,91 / 645 |
| cierre completo (cp-v10: comentario un paso peor en historias y trimestres) | 60,01 / 21 % / 148 / 123 | 41,97 / 574 |
| sólo trimestres (Defuse + Lay low cada trimestre) | 60,08 / 21 % / 160 / 123 | 41,87 / 600 |
| sólo historias (comentario un paso peor en historias) | 60,28 / 25 % / 188 / 128 | 41,17 / 710 |
| **sólo Defuse cada trimestre, acción principal normal** (cp-v11) | **60,33 / 24 % / 173 / 127** | **42,08 / 620** |
| Defuse cada trimestre + historias un paso peor | 60,41 / 24 % / 171 / 127 | 41,84 / 652 |

El cierre completo compra crisis a cambio de L6 y Skill; en la partida real costó 24 meses de crecimiento. Defuse cada trimestre y nada más es la única variante igual o mejor en las dos lecturas. Con la lectura ruidosa, endurecer las historias tras la explosión **empeora** (más crisis: el bot descarta tanto que acaba en opciones peores).

**cp-v11, texto final** (`lab/policies-src/comprobante/cp-v11`; lint sin errores): cp-v10 + (1) línea 7 de L1–L3 con la orden de v4 (informes, red, informes; proyecto clave; sin Skill learning), (2) tras una explosión sólo Defuse cada trimestre. Juez en `j-cp11b.jsonl` (la primera redacción, sólo con el primer trimestre a Output, dio 64,0 / 66,0 frente a 60,7 / 60,3 de cp-v10).

### 6.16 Primera partida de cp-v11 (aprobada por Alejandro; hueco 1, 15:52–16:00 UTC, `deepseek-pilo-0ec37fa7-dff20f-00000-a1`, 0,09 USD)

**25,75: muerte por Health 0 en el mes 12, un mes después de ascender a L2 en la segunda evaluación.** Proveedor con razonamiento (27,6 mil fichas en 42 llamadas); pareja en todas las respuestas (47 de 46 `take_action`); 231 mil fichas por mes.

- **Qué pasó.** Mes 5: «fin de semana en familia para recuperar Health» (Dignity +1, Health +2, **Network −1, Output −1, Skill −1**) con Health 5 → S8 N2 O2 y ascenso del mes 6 perdido. Meses 10–11 (mes previo a la segunda evaluación): cuatro opciones seguidas con coste de Health leídas como ayuda o profesionalidad («hacer turnos para ayudar al equipo, Network antes de la evaluación» Health −2; «aclarar la métrica con el VP» −1; «llevar al compañero borracho a casa» −1; «pair una hora, mantener el arreglo, *protect health*» −1, con Health 1, cuando la alternativa sin coste de Health perdía Network −1 y el paso 4 la descartó). Ascendió a L2 en el mes 12 y murió en el mismo mes.
- **Qué dice de cp-v11.** Las dos reglas nuevas hicieron lo previsto donde tocaba: trimestres de los meses 6 y 9 con informe, red, informe + proyecto clave (Output llegó a 3 en el mes 4); en el mes 3, con Health 4, la línea 2 puso Health recovery primero y el resto fue Network maintenance ×2 en vez de informes (desviación menor: tras la recuperación el texto pide informes). No hubo explosión, así que el Defuse-sólo no se vio.
- **Qué dice del juego.** Es el **cuarto tipo de hundimiento** de la familia y el primero por salud (réplica: 2 % con lectura exacta, 7 % con la ruidosa). Las tres pérdidas del mes previo por una opción de descanso (gimnasio en cp-v3, karaoke en cp-v8 n.º 2, fin de semana aquí) y esta muerte por cuatro opciones de «ayudar» con coste de Health son las dos caras de la misma moneda: DeepSeek no ve los costes de Health ni de Output/Network en el texto de la opción (B17), y una regla que ordene bienestar antes que evaluación salva unas partidas y hunde otras. **No se propone ninguna regla nueva** (reglas 1 y 5 de §6.8).
- **Hoy, 3 hundimientos en 4 partidas** (L1, L1, salud) frente a 2 en las 13 anteriores de la familia. Con una tasa base del 15 % la probabilidad de 3 de 4 es ~2–4 %: puede ser azar, y no hay un factor común claro (dos sin razonamiento, esta con razonamiento; tres manuales distintos con las mismas reglas de historias). Queda apuntado para vigilar en las próximas partidas, no como conclusión.

**Familia completa a las 16:10 UTC: 17 partidas largas, 11 completas (media 66,1; 61,2–71,7), 4 hundidas (24 %: dos en L1, una crisis, una por salud), 2 con una explosión.** E[partida] ≈ 0,76 × 66 + 0,24 × 25 ≈ 56; E[versión] ≈ 61 (0,8 × 56 + 6,3 + 9,8), 69 si las tres partidas oficiales se completan.

### 6.17 `cp-v12`: las reglas de cp-v5a con el bucle de cp-v10, y nada más (Alejandro, 29 oct, 16:30 UTC)

Alejandro separa lo probado (el bucle) de lo no probado (las reglas de trimestre y cierre de cp-v8 → cp-v11): la rama cp-v8/v10/v11 lleva 3 hundimientos en 5 partidas frente a 1 en 6 de cp-v5a/cp-v7, y la réplica ruidosa que respaldaba las reglas nuevas no está calibrada (~42 frente a ~66 real). La excepción de cp-v8 (Defuse antes que la salud con RR. HH. no tranquilo) sólo se disparó en una de las tres hundidas (cp-v10 n.º 1, meses 6 y 21); queda apuntada como dudosa en pendientes.md. **Decisión: no añadir más reglas por partidas sueltas mientras la réplica no esté calibrada con las partidas reales.**

`lab/policies-src/comprobante/cp-v12` = `cp-v5a` con sólo la sección Turn loop del Skill y las frases del bucle del manifest sustituidas por las de cp-v10 (primeras tres respuestas con la pantalla Continue como primera pareja; silencio «si puedes» y pareja independiente del texto; primer trimestre Energy → `observe` → acción principal → `observe`, después un trimestre por respuesta). Diff con cp-v5a: 5 líneas del Skill y una frase del manifest. Lint sin errores (14 avisos REVIEW, los de cp-v5a). Juez (`j-cp12.jsonl`, misma tanda que cp-v5a): **cp-v12 61,7 / 66,7 frente a cp-v5a 68,0 / 67,7** (Haiku / Sonnet). La única diferencia de texto es la sección del bucle, más larga y mecánica; en otra tanda el mismo bucle (cp-v10) salió por encima de cp-v8 con Haiku (66,7 frente a 62,0), así que la lectura honesta es «ruido del juez, con la sección del bucle como lo que más critica»; si se entrega cp-v12, vale la pena acortar esa sección sin tocar su contenido.

**Predicción antes de las partidas (3 si el presupuesto llega, ~0,7 USD cada una completa):** pareja ≥ 90 % de las respuestas de historia con cualquier proveedor; fichas < 0,7 M por mes en las completas; primer trimestre en dos respuestas y el resto en una, sin errores de menú; elecciones de historias y trimestres como cp-v5a (mismo texto). Notas: la distribución de la familia (completas ~62–72, un hundimiento cada 5–7). **Qué se hará según salga:** si la pareja sale y no hay error de menú, cp-v12 pasa a ser la base de cualquier entrega (cp-v5a con el bucle robusto); su media de 3 se compara con la de cp-v5a (66,5) sólo como dato, no como decisión. Si la pareja falla en una partida completa, el bucle de cp-v10 no es tan robusto como dicen las sondas y se vuelve a cp-v5a. Ninguna regla de historias o trimestre cambia por lo que salga.

## Gasto
- Clave al empezar (29 oct, 01:00 UTC): 32,60 USD libres (17,40 usados).
- Sondas `turnprobe` (13 tandas): ~0,30 USD. Bancos `ds-cp1b`, `ds-v4-rep2`, `ds-cp3`, `ds-cp4`: ~0,53. Partida `cp-v3`: 1,73. Partidas `cp-v5a`: 1,06 + 0,84 + 0,91. Banco L1 `ds-cp5a-l1`: 0,12. Partidas `cp-v7`: 0,65 + 1,09 + ~0,3 (eliminada). Partida `cp-v8`: 0,86. Segunda partida `cp-v8` (29 oct, 09:08): 0,42. Banco `ds-cp9-l1`, sonda `turnprobe-cp-v9` y juez: se anotan en el Relevo. Sondas del 29 oct (cp-v9 ×3, cp-v5a control y 6 ancladas, cp-v10 8 ancladas): ~0,24. Bancos `ds-cp9-l1` 0,19, `ds-cp10-l1-GMICloud` 0,10, `ds-cp10-l1-DeepInfra` 0,12. Partidas `cp-v8` n.º 2 0,42 y `cp-v10` 0,28. **Total de la línea: 10,09 USD** (con la segunda partida de cp-v10, 0,65, y la de cp-v11, 0,09) (partidas 8.09 + llamadas sueltas 1.26; techo de Alejandro ~15).

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

## Relevo (29 oct, 12:55 UTC)
1. **Hecho y por qué.** Reglas de trabajo de Alejandro (§6.8). Banco de L1 de cp-v9: las reglas de historias no mueven a DeepSeek → quitadas; cp-v9 queda con dos reglas de trimestre y cierre con respaldo de réplica (§6.6) y no se juega (regla 4). **El proveedor que sirve la llamada decide el bucle de fichas** (§6.9, CP6): sin canal de razonamiento (DeepInfra) DeepSeek narra y la pareja es una moneda. `cp-v10` (§6.10) siembra la pareja en la pantalla Continue y la desacopla del silencio: 8 de 8 en sondas ancladas (DeepInfra 5, GMICloud 3) frente a 3 de 6 de cp-v5a. Auditoría de GPT leída y respondida (§6.11); dos retoques tomados. `main` juntado; datos pagados exportados a `lab/data/deepseek` (NORMAS §1.6 nueva).
2. **Resultados.** Tablas de §6.5–§6.10. Sondas: `~/careerlab-data/comprobante/turnprobe-cp-v10-pin-*.json`, `turnprobe-cp-v5a-pin-*.json`; léelas con `uv run python scripts/comprobante/probeprov.py '<glob>'`. Banco `ds-cp9-l1` en `lab/data/deepseek/bancos/`. Gasto de la línea ~9,3 USD antes de la partida de cp-v10 (techo 15).
3. **En marcha.** Partida de confirmación de cp-v10 (hueco 1, ~45 min, ~0,9 USD) y juez `j-cp10.jsonl`. Lo que decide la partida está escrito en §6.10: pareja ≥ 90 % de las respuestas de historia → cp-v10 sustituye a cp-v5a como candidato del corte 2 (los documentos de `docs/entrega/cut2/` tendrían que describir el bucle nuevo y el primer trimestre en dos respuestas); si no, cp-v5a.
4. **Siguiente paso.** Al acabar la partida: `python3 scripts/comprobante/gametokens.py ~/careerlab-data/huawei-deepseek/runs/<run>` (pareja, fichas por mes, texto visible), `uv run python scripts/comprobante/riskaudit.py detail <run>/events.jsonl` (elecciones contra el catálogo) y `scripts/comprobante/traj.py <run>` (trimestres: primer trimestre en dos respuestas, L5 con informes y proyecto clave si llega). Después, `uv run python scripts/deepseek/export_data.py` y commit. Si cp-v10 pasa, proponer a Alejandro dos partidas más antes del corte 3 (~1,8 USD) sólo para la media; no cambiar ninguna regla por su nota.

## Relevo (29 oct, 13:50 UTC)
1. **Hecho.** Partida de confirmación de `cp-v10` (§6.10): bucle confirmado (100 % de parejas sobre un proveedor sin razonamiento), partida hundida en L1 (22,98). `traj.py` corregido para los trimestres en lote. Datos exportados a `lab/data/deepseek` (31 partidas). Decisión preescrita aplicada: **cp-v10 candidato del corte 2**; guía para quien empaqueta en §6.12.
2. **Resultados.** §6.10; `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-76e845c2-dff20f-00000-a1` y `lab/data/deepseek/partidas/cp-v10__76e845c2-00000/`. Gasto de la línea ~9,6 USD + 0,24 del banco anclado en marcha (techo 15).
3. **En marcha.** Banco `ds-cp10-l1-GMICloud` y `ds-cp10-l1-DeepInfra` (90 situaciones cada uno): `uv run python scripts/deepseek/bench_sets.py ~/careerlab-data/deepseek/ids-l1prep-set.json ds-v4-full10 ds-v4-rep ds-cp5a-l1 ds-cp9-l1 ds-cp10-l1-GMICloud ds-cp10-l1-DeepInfra`. Pregunta: ¿el proveedor cambia también las elecciones? Si la pérdida de DeepInfra ≤ GMICloud + 0,4 (ruido entre pasadas de v4), no.
4. **Siguiente paso.** Avisar al chat que empaqueta: cp-v10 en lugar de cp-v5a, con §6.12. Para el corte 3, Alejandro decide si gasta en 2 partidas más de cp-v10 (~1,8 USD) sólo para tener media de la familia bajo este bucle; ninguna regla cambia por una partida. Sin tocar: reglas de historias (dos direcciones cerradas hoy: pista del mes previo y «no se mueve»; ampliar la excepción de L1 vale +0,2 en la réplica).

## Relevo (29 oct, 14:15 UTC; cierre de la jornada)
1. **Hecho.** Banco de L1 anclado por proveedor (§6.10): el proveedor no cambia las elecciones; pregunta cerrada. Gasto exacto de la línea recalculado: 9.35 USD.
2. **Recomendación en vigor.** Corte 2: `comprobante/cp-v10` (cp-v5a de reserva). Guía para los documentos: §6.12. Corte 3: nada que probar en partidas cambia la elección entre cp-v10 y cp-v5a (mismas reglas de historias); dos partidas más de cp-v10 sólo darían media de la familia, no una decisión. Las direcciones cerradas hoy están en §6.6–6.8 (reglas de historias en el mes previo, «no se mueve», Health en Crecer, proteger N = 2, ampliar la excepción de L1).
3. **Lo que queda abierto, para quien siga.** (a) El hundimiento de L1 es estructural (§6.3, §6.7): la única palanca real es aceptar riesgo pequeño en el mes previo cuando toda opción segura pierde, que vale +0,2 en la réplica; no hay nada más que probar con texto. (b) L6 sólo llega con L5 en el mes 36 y Output comprado en L5 (cp-v10 lo lleva); se verá en partidas que lleguen. (c) Si el proveedor de la evaluación oficial no sirve razonamiento, cp-v10 mantiene la nota de fichas (~95–98) y cp-v5a la perdería (~65).
4. **Comandos.** Sondas por proveedor: `DS_PROVIDER=<Proveedor> uv run python scripts/comprobante/turnprobe.py --bundle <bundle> --turns 6 --start 0 --stop-usd 14 --out <json>` y `uv run python scripts/comprobante/probeprov.py '<glob>'` (sólo investigación; nunca en el runner). Banco: `DS_PROVIDER=<Proveedor> uv run python scripts/deepseek/bench.py run --variant <bundle> --name <arm> --ids ~/careerlab-data/deepseek/ids-l1prep90.txt`, después `bench_sets.py`. Partidas: como en el Relevo de las 05:25 con `--policy cp-v10` (registrado, id `76e845c2d60600d9`). Tras gastar: `uv run python scripts/deepseek/export_data.py` y commit.

## Relevo (29 oct, 15:45 UTC)
1. **Hecho.** Segunda partida de cp-v10 (§6.13): completa, 61,24, fichas 100 narrando sin razonamiento; dos mecanismos vistos (cierre tras explosión demasiado caro; Output rezagado en L3 con Skill learning inútil). Análisis de los primeros seis meses de las 14 partidas (§6.14). Réplica: primer trimestre a Output (+0,4 / +1,0) y variantes del cierre (§6.15). **`cp-v11`** escrito con las dos correcciones; datos exportados.
2. **Resultados.** §6.13–6.15; `lab/data/deepseek/partidas/cp-v10__76e845c2-00001/`. Gasto de la línea 10,0 USD (techo 15).
3. **A medias.** Juez de cp-v11 (`j-cp11b.jsonl`). Nada más en marcha.
4. **Siguiente paso.** Una partida completa de cp-v11 (~0,7 USD) con predicción: informes en todos los trimestres de L1–L3 (Output en su tope de L1 en el mes 3, de L2 por el 9–11, de L3 por el 15–17), pareja ≥ 90 %, y si hay explosión, Defuse cada trimestre con acción principal normal. Lo que no decide: la nota. Comandos como en el Relevo de las 05:25 con `--policy cp-v11` (registrar antes: `uv run python -m careerlab.target register lab/policies-src/comprobante/cp-v11 --by "Alejandro Treny Ortega"`).

## Relevo (29 oct, 16:15 UTC)
1. **Hecho.** Partida de cp-v11 (§6.16): muerte por salud en el mes 12; las reglas nuevas se ejecutaron donde tocaba; ninguna regla cambia. Datos exportados (33 partidas en `lab/data/deepseek`).
2. **Dónde queda el «mejor modelo».** `cp-v11` es el mejor diseño con pruebas: reglas de historias de v4-c5 + t0 + suelo-min (idénticas a cp-v5a), trimestre de L1–L3 en la orden de v4 (réplica +0,4 / +1,0; partidas reales de v4 llegan al tope de Output), Skill desde L4 y Output desde L5, Defuse cada trimestre tras una explosión (réplica igual o mejor), y un bucle de fichas que empareja con cualquier proveedor (10 de 10 sondas y partidas). Lo que ningún texto ha movido: la lectura de los costes de Health, Network y Output en las opciones (cinco intentos en tres días: v8, v9, perceive-v5, cp-v9, y los avisos de lectura de la familia), que es de donde salen los hundimientos (24 % de las partidas largas).
3. **Lo que no hay que repetir.** §6.6–6.8 y §6.16: pistas de lectura, «no se mueve», Health en Crecer, proteger N = 2, ampliar la excepción de L1, cierre completo tras explosión, bloque literal en el manifest, bienestar antes o después de evaluación en el mes previo.
4. **Siguiente paso, si se sigue gastando.** Sólo partidas de `cp-v11` para tener media (no deciden reglas); cada una ~0,7 USD si completa. Comandos como en el Relevo de las 05:25 con `--policy cp-v11` (ya registrado, id `0ec37fa7905b8836`). Gasto de la línea 10,09 USD.
