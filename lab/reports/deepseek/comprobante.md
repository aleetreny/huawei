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

### 5.1 ¿Obedece DeepSeek el bucle? (`scripts/comprobante/turnprobe.py`)
Pendiente.

### 5.2 Juez de calidad
Pendiente.

### 5.3 Banco de DeepSeek: ¿cambian las elecciones?
Pendiente.

### 5.4 Partida oficial: fichas por mes
Pendiente.

## Gasto
- Clave al empezar (29 oct, 01:00 UTC): 32,60 USD libres. Gasto de esta línea: se anota aquí por prueba con `total_cost`/`cost`.
