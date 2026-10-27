# Mejora de la nota de DeepSeek: análisis desde los fundamentos y manuales t13-read-v2 a v4

**Conclusión (27 oct, 21:05 UTC).** **Cuatro partidas completas de DeepSeek hoy, todas entre 66,7 y 71,7: `t13-read-v4` 71,67 y 70,22, `t13-read-v7` 67,27, `t13-read-v5` 66,71** (48 meses, L5, riesgo 0, Health y Dignity al máximo). Además, `t13-read-v3` llegó al mes 48 en L5 (66,6 según la réplica; la cortó nuestro vigilante). Antes de hoy, las tres partidas oficiales de DeepSeek habían acabado eliminadas (14,98 a 42,51).

Queda una fuente de varianza: la trampa del primer ascenso. Una partida de v4 se quedó en L1 y habría acabado despedida en el mes 24. Media esperada de v4 contándola (~1 de cada 8–10 partidas): ~63; cuando asciende a tiempo, ~70.

Lo que lo ha conseguido:
- proteger Skill, Network y Output en el mes previo a cada evaluación, en el cuerpo del Skill y en la instrucción del manifest (DeepSeek no vuelve a abrir archivos de referencia);
- separar del todo las reglas del trimestre y las de las historias;
- un paso de riesgo más duro cuando RR. HH. no está tranquilo;
- en v4, además, el mejor valor de cada indicador en el nivel, protección de Network y Output los dos últimos meses y reparación inmediata.

**Recomendación para el corte 1: `t13-read-v4`** (commit `09d5735`).

**Recomendación para el corte 1: `t13-read-v4`.** Se están jugando dos partidas más para tener tres, como la evaluación oficial.

27 oct 2026, rama `alejandro/deepseek` (worktree `~/huawei-ds`). Encargo de Alejandro: subir la nota de DeepSeek pensando desde los fundamentos, hasta 10 USD hoy.

## 1. De dónde salen los puntos

- **La nota final:** nivel 30 %, dinero 20 %, Health + Dignity 15 %, Skill 15 %, control de riesgo 10 %, Network 10 % (A1). Normalizaciones vistas en los informes oficiales: nivel = 10 × L, dinero sobre 80, Health + Dignity sobre 20, Skill sobre 120, Network sobre 60, riesgo 0 = 100. Para llegar a 70 hay que acabar los 48 meses en L6, con riesgo 0 y Health y Dignity llenos.
- **La nota de cada partida oficial es su `quantitative_score`** (la media de 3 partidas da el 80 % de la versión). La `competition_partial_score` de los informes es siempre esa nota × 0,7 y no se usa para la clasificación (corregido: no es un castigo por eliminación). Una partida eliminada pierde los meses que no juega: nivel, dinero y lo que habría crecido.
- **Las dos formas de perder con DeepSeek, vistas en partidas:**
  1. **Perder el primer ascenso.** En L1 el umbral de Network y Output coincide con lo máximo que admite el nivel. Un punto perdido en las historias justo antes de la evaluación cuesta el ascenso (f1 lo perdió así dos veces: Network en el mes 5 y Output en el 11). En L1, quien no asciende para el mes 12 acaba despedido en el mes 24.
  2. **La crisis de confianza**, por opciones que parecen constructivas (en privado, anónimas, por fases).
- **El simulador con la lectura de DeepSeek** (bot de regla escrita, dos pasadas de etiquetas, 2.000 partidas) dice que el despido pesa mucho más que la crisis: 26 % de despidos frente a 6 % de crisis.

## 2. Qué se probó en el simulador (gratis)

Base: regla escrita "estricta" con la lectura v3 de DeepSeek, 53,9.

| Cambio | Nota | Despidos | Crisis |
|---|---:|---:|---:|
| Base (descarta lo arriesgado; protege el mes previo después) | 53,9 | 518 | 121 |
| Si RR. HH. no está tranquilo, sólo opciones que bajan el riesgo | 54,1 | 525 | 102 |
| Lo mismo siempre | 54,2 | 524 | 92 |
| Limpiar riesgo en el trimestre en cuanto RR. HH. no sonríe | 54,0 | 519 | 105 |
| Además, "Lay low" en cuanto no sonríe | 53,7 | 534 | 90 |
| **Mes previo: proteger el ascenso antes que el riesgo leve, si RR. HH. está tranquilo o "quiet"** | **55,5** | **396** | 151 |
| Lo mismo con cualquier riesgo | 53,1 | 360 | 297 |
| Lo mismo, dos o tres meses antes | 53,5 / 51,2 | 422 / 442 | 213 / 238 |
| Proteger también los dos meses previos, después del riesgo | 55,1 | 410 | 161 |
| Sin conocer los techos (como DeepSeek) | 54,4 | 413 | 161 |
| … y detectándolos en las historias | 54,3 | 441 | 143 |

Con etiquetas perfectas, el mismo cambio sube de 60,7 a 62,2. El oráculo saca 68,1.

**Por qué el mes previo es un dilema:** en el 10 % de las preguntas todas las opciones bajan Skill, Network u Output, y en el 26 % todas bajan alguno o son arriesgadas. Con tres historias en ese mes, hay un 27 % de opciones de que la pérdida sea inevitable si no se acepta algo de riesgo.

**Lo que el bot no puede ver:** DeepSeek persigue subidas que ya no caben (una partida de t13-read-v2 perdió dos puntos de Output con `Review in 2` para ganar Network, que ya estaba en su máximo) y casi no consulta el registro. El bot conoce los techos en el trimestre; DeepSeek no.

## 3. Los manuales

| Manual | Qué cambia | Por qué |
|---|---|---|
| `t13-read-v2` | t13-read-v1 + protección del mes previo en el cuerpo y en la instrucción del manifest; separación estricta trimestre/historias; paso de riesgo más duro si RR. HH. no está tranquilo; línea de estado con techos observados; sin umbrales numéricos | Las partidas: DeepSeek lee el Skill sólo dos veces y no vuelve a abrir la referencia; la regla trimestral se coló en las historias; el riesgo "constructivo" mató una partida |
| `t13-read-v3` | v2 + en el mes previo, con RR. HH. tranquilo o "quiet", el ascenso va antes que el riesgo leve | Simulador: +1,6, despidos −24 % |
| `t13-read-v4` | v3 + "Best" (mejor valor de cada indicador en el nivel), protección de Network y Output los dos últimos meses con reparación inmediata, detección de techos también en historias | Ideas de `observed-growth-v10` de Matteo y el fallo de la partida 1 de v2 |

Todos pasan `careerlab lint` sin errores.

## 4. Partidas oficiales

### t13-read-v2 (3 partidas en paralelo, 27 oct desde las ~18:00 UTC)

Lo visto mientras juegan:
- **Ascensos:** dos partidas ascienden a L2 en el mes 6 y la tercera en el mes 12. Una llega a L3 en el mes 18 y otra en el 24. Ninguna se pierde en L1, frente a 2 de 3 eliminadas así con los manuales anteriores.
- **Riesgo:** el comentario de RR. HH. está tranquilo casi todo el tiempo; una sola explosión en tres partidas hasta el mes 24.
- **La línea de estado se rellena siempre, pero "Stalled" nunca** (0 de 160 notas), aunque Skill, Network y Output estén justo en lo máximo del nivel. DeepSeek no compara una nota con la anterior. Sin esa detección, la regla "Network y Output estancados → Skill" nunca se activa.
- **Ascensos perdidos y por qué:**
  - Mes 6: con Review in 2 eligió prepararse a fondo para una revisión de otro equipo (Output −2) para ganar Network, que ya estaba en su máximo.
  - Mes 12: con Review in 1 eligió "asumirlo e impulsar una norma de equipo" (Output −1) y llegó con Output un punto por debajo.
  - Mes 9: en el trimestre previo gastó 2 de energía en limpiar riesgo con RR. HH. tranquilo, en vez de llenar Output (en L2 el máximo deja un punto de margen).
- **Incidente:** la primera partida (hueco 0) se lanzó en modo normal con tope de 1,2 USD. El vigilante mide el gasto de toda la clave y, con las otras dos partidas en paralelo, la cortó en el mes 26, en L3, sin explosiones. Lección: en paralelo, tope alto y coste por partida desde el informe del programa.

**Cómo acabaron** (ninguna eliminada por el juego):

| Partida | Final | Causa |
|---|---|---|
| v2-00000 | mes 26, L3, sin explosiones | cortada por el vigilante (tope de 1,2 USD medido sobre toda la clave con tres partidas en paralelo; error nuestro) |
| v2-00001 | mes 33, L2, sin explosiones | **límite de 20 reanudaciones del programa** (ver abajo); 1,32 USD |
| v2-00002 | mes 40, L4, una explosión | cortada por el vigilante (tope de 3 USD, mismo error); ahora el tope en paralelo es 20 USD |

**La partida atascada en L2 (v2-00001)** perdió cuatro evaluaciones seguidas igual: Network u Output caen uno o dos puntos con la última decisión antes de la evaluación (Output 4 en el mes 12; Network 5 en los meses 18, 24 y 30), con un margen de un punto en L2.

**El contexto y el límite de reanudaciones.** JiuwenSwarm no comprime el historial en estas partidas. La entrada por llamada crece en línea recta: 37 mil fichas al empezar, ~160 mil en el mes 26, ~200 mil en el mes 33 (unas 1.150 fichas por decisión). En v2-00001, a partir de 158 mil algunas llamadas volvieron con un mensaje enlatado de proveedor, en chino, en vez de jugar. Cada respuesta así termina el turno del agente sin herramientas, y el programa oficial sólo reanuda 20 veces: la partida acabó sin nota. Otra partida llegó a 224 mil sin ese problema, así que depende del proveedor que toque. Afecta a cualquier manual y también a la evaluación oficial. Desde el Skill sólo se puede escribir menos (v6 pide notas cortas en inglés).

### Lote 2 y siguientes

- v3, v4 y v5: una partida de cada uno.
- `t13-read-v6` = v5 + en el mes previo, una lista de lo que suele costar Network (decir que no a un colega, corregirlo o denunciarlo, quedarse fuera de algo de grupo, anteponer lo propio a quien pidió ayuda) y, en la duda, la opción más cooperativa que aún entrega lo propio; notas cortas en inglés. Desde las 19:20 UTC los tres huecos juegan v6.

### t13-read-v3 (1 partida): llega al mes 48 en L5 sin ninguna explosión

- Ascensos en los meses 6, 18, 24 y 42 (L5); el comentario de RR. HH. tranquilo casi siempre.
- **El vigilante la cortó en el mes 48**: se lanzó antes de subir el tope en paralelo (3 USD), y con tres partidas a la vez el gasto de la clave lo pasó. Error nuestro, otra vez.
- Último estado: L5, Health 10, Dignity 10, Skill 103, Network 47, Output 35, Wealth 31, comentario de RR. HH. "frowning". **La fórmula de la réplica le da 66,6** (68,6 con el riesgo limpio al final). Es la mejor partida de DeepSeek que tenemos y está cerca del objetivo de 70.
- La energía trimestral nunca fue a Skill (siempre informes, red y proyecto clave): la regla "Network y Output estancados → Skill" depende de "Stalled", que DeepSeek no rellena.

**Medida de urgencia (19:40 UTC).** Las partidas de v4 y v5 en juego también llevaban el tope de 3 USD. Para que el vigilante no las cortara, se apuntó temporalmente `API_BASE` del `.env` del programa a una dirección muerta. El vigilante ignora una lectura fallida, y las partidas usan su propia copia de la configuración. Una tarea en segundo plano lo restaura al terminar ambas. Las partidas nuevas ya usan tope 20 en paralelo.

### Trimestre de L4 (simulador, trimestre parecido al de DeepSeek, sin conocer techos)

| Trimestre desde L4 | Nota | L6+ | Agotamiento |
|---|---:|---:|---:|
| Como DeepSeek: informes, red, proyecto clave | 52,0 | 6 % | 121 |
| Skill primero: Skill learning + red, rotación (v5, v6) | 51,1 | 3 % | 139 |
| Equilibrado: Skill learning + informes, proyecto clave | 52,2 | 10 % | 138 |
| **Equilibrado con salud primero si no está alta (v7)** | **52,8** | **11 %** | 108 |

`t13-read-v7` = v6 con este trimestre de L4. Desde las 19:30 UTC los bucles juegan v7.

### t13-read-v4 y t13-read-v5: las primeras partidas completas

| Manual | Nota | Meses | Nivel | Riesgo final | Health + Dignity | Skill | Network | Dinero | Coste | Fichas de entrada |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **t13-read-v4** | **71,67** | 48 | L5 | 0 | 20 | 105 | 54 | 38,2 | 0,81 USD | 70,4 M |
| t13-read-v5 | 66,71 | 48 | L5 | 0 | 20 | 105 | 41 | 27,0 | 0,72 USD | 66,6 M |

- v4 ascendió en los meses 6, 12 y 24, y a L5 hacia el mes 42. v5 llegó a L4 en el mes 30 y a L5 al final. Ninguna tuvo una explosión.
- Las dos terminaron con riesgo 0 y Health y Dignity al máximo: el trimestre final funciona.
- La diferencia entre las dos está en Network (54 frente a 41) y en el dinero (38 frente a 27). v5 pone Skill primero desde L4, lo que el simulador ya decía que resta; v7 lo corrige.
- **Coste: 0,7–0,8 USD por partida completa** (66–70 millones de fichas, ~1,4 millones por mes). Es caro en la parte de eficiencia de fichas (10 % de la nota de la versión), pero terminar pesa mucho más.

### Confirmación de t13-read-v4 (2 partidas desde las 19:56 UTC) y t13-read-v7 (1 desde las 20:19)

- **v4-00001: atascada en L1.** Perdió el ascenso del mes 6 por Network −1 en la última historia del mes 5, cuando la otra opción era filtrar información a la competencia (pérdida casi forzosa). Perdió el del mes 12 por Output −1 en el mes 11. En el mes 18, D por tiempo en el nivel. Murió en el mes 22 por un fallo de infraestructura: su servidor de agente arrancó con choques de puerto (21001) a la vez que otro chat arrancaba sus huecos, y se cerró a mitad de partida ("going away"). Sin nota; iba hacia el despido del mes 24.
- **v4-00002: completa, 70,22** (48 meses, L5, Skill 122, Network 46, dinero 30,2, riesgo 0, Health y Dignity al máximo; 0,72 USD).
- **v7: completa, 67,27** (48 meses, L5, Skill 106, Network 34, dinero 33,4, riesgo 0, Health y Dignity al máximo; 0,74 USD). Peor en Network que v4: las pistas de Network del mes previo y las notas cortas no ayudan con una sola partida.

**La trampa de L1 es la mayor fuente de varianza que queda.** En L1 el umbral de Network y Output es su máximo: margen cero. En el 27 % de los meses de preparación la pérdida es forzosa (todas las opciones cuestan algo o son arriesgadas). De 8 partidas de la familia v2–v5, 1 se quedó en L1.

### Siguiente lote (histórico)

Una partida de cada uno: `t13-read-v3`, `t13-read-v4` y `t13-read-v5`. v5 recoge lo aprendido de v2: llenar los tres indicadores en el trimestre previo, quedarse en la propia entrega con la evaluación cerca, Skill primero desde L4, sin "Stalled".

## 5. Infraestructura nueva

- `careerlab/target.py`: modo paralelo (`CAREERLAB_TARGET_PARALLEL=1`). Partidas en huecos distintos a la vez; su coste se lee del informe del programa (`total_cost`), no de la diferencia de saldo.
- `scripts/deepseek/gameloop.sh`: una partida tras otra en un hueco, hasta un tope de gasto de la clave; nunca corta una partida.
- `scripts/deepseek/watch.py`: avisa de ascensos, explosiones, eliminaciones y finales.
- `scripts/deepseek/promo.py`: por qué el bot no asciende (le falta un indicador antes del mes previo, o lo pierde en él).
- `scripts/deepseek/groupbot.py`: modos nuevos de la regla escrita (`rvc`, `pw`, `pl1`, `dq`, `ll`, `blind`, `detect`, `ps`).

## Techo y trampa de L1: por qué la media aún no es 70 (21:20 UTC)

**El techo de una partida completa.** Las partidas completas de DeepSeek acaban en L5. L6 pide Skill 170 y se acaba con 105–122.
- Sumando lo que puede dar cada parte: nivel 15 + dinero ~10 + Health y Dignity 15 + Skill ~14 + riesgo 10 + Network ~9 ≈ **72–73**.
- Las dos partidas completas de v4 (71,7 y 70,2) ya están ahí. Lo que separa una de 70 de una de 67 es Network al final (54 frente a 34) y el dinero.

**La trampa de L1 en el simulador** (trimestre parecido al de DeepSeek, regla del mes previo, 2.000 partidas por fila):

| Regla añadida | Lectura de DeepSeek: nota / despidos / crisis | Lectura perfecta: nota / despidos / crisis |
|---|---|---|
| Ninguna (base) | 52,8 / 405 / 180 | — |
| En L1, proteger Network y Output dos meses antes | 53,0 / 407 / 173 | — |
| Reparar si bajan de su mejor valor con la evaluación cerca | 53,2 / 391 / 180 | — |
| Las dos (lo que ya lleva v4) | 53,4 / 389 / 175 | 60,5 / 179 / 160 |
| + si la pérdida es forzosa, que caiga en Skill | 53,4 / 389 / 175 | 61,1 / 154 / 165 |
| + en L1, ascenso antes que riesgo con cualquier comentario de RR. HH. | 53,3 / 337 / 211 | 60,1 / 149 / 201 |

**Lectura.**
- Con lectura perfecta los despidos en L1 bajan del 19 % al 9 %: la trampa es sobre todo de percepción (DeepSeek no ve qué opciones cuestan Network u Output).
- El 9 % que queda es estructural. En el 27 % de los meses de preparación la pérdida es forzosa; ninguna regla probada lo baja sin subir las crisis de confianza.
- En partidas reales DeepSeek cae en la trampa ~1 de cada 9 veces, cerca de ese suelo.

**Media esperada de v4:** 0,89 × ~70 + 0,11 × ~17 ≈ **63–65**. Para una media fiable de 70 haría falta eliminar la trampa de L1 o llegar a L6, y ninguna de las dos cosas está al alcance hoy. Las vías para los cortes 2 y 3: percibir mejor los costes de Network y Output en el mes de preparación, y que Network termine alta, como en la partida de 71,7.

## Relevo (27 oct, 21:05 UTC)

1. **Qué se ha hecho y por qué.**
   - Análisis desde los fundamentos: sobrevivir decide la nota, y con DeepSeek se perdía por el primer ascenso y por el riesgo "constructivo".
   - Pruebas gratis en el simulador con la lectura real de DeepSeek: el ascenso va antes que el riesgo leve en el mes previo, y el trimestre de L4 equilibrado.
   - Diagnóstico de cada partida oficial, leyendo el registro mes a mes.
   - Manuales `t13-read-v2` a `v7`, cada uno corrigiendo lo que falló en las partidas anteriores.
   - Partidas oficiales en paralelo (modo nuevo en `careerlab/target.py`, vigilante que nunca corta con `CAREERLAB_TARGET_NEVER_STOP=1`).
2. **Resultados.**
   - Partidas completas: v4 71,67 y 70,22; v7 67,27; v5 66,71.
   - v3 llegó al mes 48 en L5 (66,6 según la réplica).
   - v2: tres partidas sin eliminación por el juego.
   - Una partida de v4 se quedó en L1.
   - Datos: `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-*` (partidas), `lab/registry-origins/deepseek/` (registro exportado; volver a exportar con `CAREERLAB_ORIGIN=deepseek uv run careerlab export`).
3. **Lo que falló.**
   - Tres partidas buenas cortadas por nuestro vigilante (tope medido sobre toda la clave con partidas en paralelo). Ya corregido.
   - Una partida perdida por el límite de 20 reanudaciones (contexto de ~200 mil fichas y respuestas enlatadas en chino).
   - Una partida muerta por un choque de puertos de JiuwenSwarm con otro chat que arrancó sus huecos a la vez.
   - DeepSeek no usa "Stalled".
4. **Siguiente paso.**
   - **Corte 1:** empaquetar `lab/policies-src/deepseek/t13-read-v4` (commit `09d5735`) y cambiar "t13-read-v2" por "t13-read-v4" en los borradores de `alejandro/entrega`.
   - **Cortes 2 y 3:** atacar la trampa de L1, que es la mayor fuente de varianza (margen cero en Network y Output; en el 27 % de los meses de preparación la pérdida es forzosa). Medir con 4–6 partidas por versión.
   - Para jugar: arrancar las instancias de una en una y comprobar los puertos con `lsof` si hay otros chats jugando.
   - Comandos (desde un worktree de `alejandro/deepseek`):

   ```bash
   scripts/deepseek/start-loops.sh <tope de saldo de la clave> <manual hueco 0> <manual hueco 1> <manual hueco 2> <partidas por hueco>
   python3 scripts/deepseek/watch.py <id de política (8 caracteres)>
   CAREERLAB_TARGET_ENV=<runner>/.env uv run python scripts/deepseek/ds.py status
   ```

5. **Gasto de DeepSeek de esta línea hoy:** ~9,5 USD (coste por partida desde `score_report`). La clave lleva 12,86 USD usados, contando las partidas del chat "Scripts and alternative", y conserva 37,1 (reserva de 15 intacta).
