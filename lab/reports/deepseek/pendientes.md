# Pendientes de DeepSeek: candidatos y pruebas por confirmar

**En una frase (29 oct, noche):** la base es **`comprobante/cp-v12`**: las reglas de cp-v5a más el bucle de dos llamadas por respuesta, que los organizadores permiten (C49). Nota de fichas ~95–100 con cualquier proveedor. Sus dos partidas completaron: 56,80 y 62,83. Corte 1 oficial: 64,75, puesto 13 (C45).

Las reglas añadidas en cp-v8–cp-v11 quedan fuera mientras la réplica no esté calibrada. Lo que más puntos tiene es no hundirse (4 de 19 partidas largas) y llegar antes a L5 (C57, C58).

**Línea Mejora (cerrada el 30 oct; candidatos para entregar: `mejora/mv-5r` o `mejora/v4-loop`, filas de abajo; C68–C79. Resumen del 29 oct, 22:45 UTC; [informe](../mejora/README.md); HALLAZGOS C68–C72):** candidato **`mejora/mv-4`** = reglas de historias de v4 (vía ex-v1) + trimestre por tramos + freno de salud + **lectura de los costes ocultos en los meses de evaluación** + bucle de cp-v12 copiado byte a byte + «nunca termines una respuesta sólo con texto» en el manifest. Banco (159): pérdida en el mes previo de L1 **2,51** frente a 3,31–3,68 de v4; control de riesgo 0,84; control 0,34. 10 partidas reales esta noche (mv-3 y mv-4): completas 68,64 · 77,78 (L6) · 66,06 · 63,35 · 69,62 · 63,27, hundidas 3 (una por el defecto de mv-3, ya arreglado; una crisis; un despido en L1), fichas 95–100. Control cp-v12: 20,73. **En partidas no juega visiblemente mejor que v4; en nota de versión esperada, ~+3,5 por fichas y calidad.** **30 oct:** el sustituto es `mejora/mv-5r` (el mismo riesgo que v4 al preparar evaluaciones de L2–L4). La ventaja de lectura en L1 sobre v4 queda dentro del ruido (C68 rebajado; [mejora](../mejora/README.md) §9–§10). **Avisos:** (1) la redacción del bucle de `ex-v1`/`ex-v3` no empareja con DeepInfra (0 de 3): no entregarlos así; (2) con el texto de mv-3 una partida se quedó sin nota (`max_continuations`); mv-4 lo corrige. Gasto 3,23 USD.

**Línea Tramos (30 oct, 16:00 UTC; [informe](../tramos/README.md); HALLAZGOS tramos-1 a tramos-3):** antes de jugar partidas enteras, comparar candidatos en **tramos fieles** con `scripts/tramos/fiel.py`: el principio de la partida contra el motor oficial con la petición exacta de JiuwenSwarm, ~0,04 USD por tramo hasta el mes 6, en paralelo. El banco queda como filtro de regresiones. Piloto: el bucle de fichas no empeora el primer ascenso (v4-loop 3 de 4 y 11 de 14; v4 1 de 4 y 2 de 12). **Pendiente para el corte 2:** mv-5r frente a v4-loop, 15 por brazo, ~1,2 USD.

**Siguientes pasos, por orden (29 oct, noche, tras la línea Exploración):**
1. **Hecho: la réplica calibrada con las partidas reales** ([exploracion](../exploracion/README.md) §1). Un modelo de elección ajustado a las 2.743 decisiones reales predice el 87 % de las elecciones de DeepSeek y reproduce las partidas (completas 65,4 frente a 65,3). Dice que las reglas mueven la media ±1–2 y que el hueco hasta el planificador perfecto es percepción, sobre todo en el mes previo de L1.
2. **Probar `exploracion/ex-v1`** (cp-v12 + trimestre por tramos + freno de salud + texto para la rúbrica): sondas de la pareja y banco de L1, ~0,2 USD; si pasa, candidato al corte 2. Réplica +1,8 de partidas; juez de calidad +8. Plan: [plan-deepseek.md](../exploracion/plan-deepseek.md).
3. **Banco de L1 de `exploracion/ex-v3`** (~0,12 USD): lo discreto antes que plantarse en público en el mes previo de L1. Réplica +0,3; Sonnet cambia justo las decisiones previstas.
4. **«v4 frente a cp»** ya no hace falta jugarlo: en la réplica calibrada las reglas de historias de las dos familias valen lo mismo (+0,7 ± 0,4 para v4); los 5 puntos entre completas reales son azar (exploracion §1).
5. **Script en partida (C49, C60):** medido (exploracion §4). Detectar techos con el menú vale +0,0; decidir historias con un script, −3 a −4,5; el híbrido de Winfred, −0,7 a −3,0. `exploracion/ex-s1` queda como demostración, con sondas opcionales.
6. Reglas generales de BDCI: ya en la réplica calibrada (exploracion §5). Proyecto clave por defecto en L1–L3 y rotación desde L4; freno de salud +0,9.

Este es el sitio único de lo que falta probar con la clave. Quien gaste DeepSeek mantiene la lista: al terminar una prueba, actualiza la fila y pasa el resultado a [HALLAZGOS](../../../HALLAZGOS.md). Los comandos exactos están en el informe de cada línea, que es la fuente; aquí sólo se enlazan.

**Datos (29 oct).** Todo lo pagado de DeepSeek está en Git en [`lab/data/deepseek/`](../../data/deepseek/README.md):
- **Partidas oficiales:** las 21, en `partidas/`, con `partidas.csv` y `decisiones.csv.gz`.
- **Bancos:** `bancos/<brazo>/`.
- **Etiquetas de percepción:** `etiquetas/`.
- **Listas de situaciones:** `ids/`.

Los scripts leen `~/careerlab-data/deepseek` si existe y, si no (en la nube), la copia de Git, que `uv run python scripts/deepseek/datapaths.py materialize` deja con la estructura de siempre. Equivalencias:

| En el Mac | En Git |
|---|---|
| `~/careerlab-data/huawei-deepseek/runs/<run>/` | `lab/data/deepseek/partidas/<manual>__<id>/` |
| `~/careerlab-data/deepseek/runs/<brazo>/` | `lab/data/deepseek/bancos/<brazo>/` |
| `~/careerlab-data/deepseek/labels/` | `lab/data/deepseek/etiquetas/` |
| `~/careerlab-data/deepseek/ids-*.txt` | `lab/data/deepseek/ids/` |

Quien juegue o pase un banco nuevo vuelve a exportar con `uv run python scripts/deepseek/export_data.py`.

## 1. Árbol de manuales

| Manual | Padre | Qué cambia | Medido sin DeepSeek | Medido con DeepSeek | Qué falta y coste |
|---|---|---|---|---|---|
| `deepseek/t13-read-v4` | t13-read-v3 | — | Calidad de Claude 60–66 (C24); otro revisor 70–72 (C32) | **Partidas 71,67 y 70,22.** Una tercera murió en L1 por un choque de puertos. Fichas ~64 de 100 (C31) | Nada: es la referencia y lo **entregado en el corte 1** |
| `calidad/v4-c5` | v4 | Redacción para la rúbrica: un solo Skill, sin umbrales; arregla N = 1, Repair en la lista de energía y la energía del último trimestre | Calidad +4,2 (C24, C25); Haiku elige igual que con v4 (92–95 %) | Nada | Juez DeepSeek y banco de 320 historias, ≈ 1,3 USD. [calidad-skills §4](../calidad-skills/README.md) |
| `techo/v4-t0` | v4-c5 | Trimestre desde el nivel 4: Skill learning + Apply for rotation | Réplica +0,5; L6 del 16 % al 25 % con lectura exacta; el juez no baja | Nada. Con t13-final, DeepSeek pasó de 2 % a 65 % de «Skill en L4» (B20) | Banco «Skill en L4» (40 situaciones), ≈ 0,2 USD. [techo §7](../techo/README.md) |
| `techo/v4-t1` | v4-t0 | Además: Skill cuenta doble en las historias desde L4, Dignity protegida desde 7, Stalled anclado al valor (B38) | Réplica +1,1 exacta / +0,9 ruidosa; Haiku elige igual que con c5 en el 91 % | Nada | Historias de control, ≈ 0,5 USD. [techo §7](../techo/README.md) |
| `suelo/suelo-v1-min` | v4-c5 | Rescate de L1 tras dos evaluaciones sin ascenso (B30, B33); con todas las opciones arriesgadas, decide el tamaño del riesgo (B34); higiene de contexto (C43) | Réplica: menos hundimientos, pero buena parte de lo que gana `mag` ya está en v4; juez 62/66 frente a 61/63 de c5; Haiku no cambia de elección (C44) | Nada | Banco de trampas (176 situaciones), ≈ 0,3 USD por brazo. [suelo §6](../suelo/README.md) |
| `suelo/suelo-v1` | v4-c5 | min + prudencia tras una explosión (B35) + campo «Blow-ups» | Réplica: un tercio menos de crisis con lectura ruidosa; juez 54/62 (castiga la línea de estado de 7 campos) | Nada | El mismo banco, ≈ 0,3 USD más |
| `stat-perception/v4-lean` (rama `leah/workspace`) | v4 | Línea de estado corta, notas cortas, Skill desde L4, plan a 48 meses | Rúbrica 74,3 frente a 70,2; Haiku elige igual que con v4 (92–93 %); notas −25 % | Nada | Va con v4-lean-q |
| `stat-perception/v4-lean-q` (rama `leah/workspace`) | v4-lean | Trimestre planificado tras **un solo `observe`** | Modelo de fichas: −15 % (+0,7 de nota) | Nada | 1 partida para medir fichas por mes y que no haya acciones rechazadas, ≈ 0,8 USD. [09-v4-lean](https://github.com/aleetreny/huawei/blob/leah/workspace/lab/reports/stat-perception/09-v4-lean.md) |
| **`exploracion/ex-v1`** | cp-v12 | Trimestre: informes en el nivel inicial; Health recovery desde 5; L2–L3 informe, red, informe + proyecto clave; desde L4 Skill learning + informe + rotación. Historias: freno con Health ≤ 3. Texto para la rúbrica; la nota del ejemplo literal pierde «Reviews here» | Réplica calibrada +1,8 de partidas (muertes por salud 6,5 % → 1,1 %); juez Opus 84/83, Sonnet 72/71 (cp-v12 73/72, 66/66); lint y cumplimiento sin errores | **Sondas (línea Mejora, con el texto de mv-1, que lleva su bucle tal cual): DeepInfra 0 de 3, GMICloud 3 de 3** | **No entregar con esta redacción del bucle**: sustituida por la de cp-v12 en `mejora/mv-2`/`mv-3` (3 de 3 con DeepInfra). Banco de L1: no hace falta, sus reglas de historias son las de mv-1 sin el paso 4 nuevo |
| `mejora/mv-1` | ex-v1 + t13-read-v9 | Paso 4 de historias (Review in 1–2): «Read the hidden costs» (Network cae aunque sea con educación o justicia; Output cae cuando el tiempo o el mérito van a otro o a un proceso) y desempate «la que deja más cómodos a los implicados»; la lista de riesgo, sin tocar | Réplica: arreglar la lectura del mes previo de L1 vale +0,8 a +3,0 según cuánto se detecte | Banco (159): L1 2,58 / 15 que bajan N/O (v4 3,31–3,68 / 24–25); control de riesgo **2,23** (v4 0,93); sondas DeepInfra 0 de 3 | Sustituido por mv-3 |
| **`mejora/mv-3`** | mv-1 → mv-2 | mv-2 = mv-1 con «Turn loop» y «Status line» de cp-v12 byte a byte. mv-3 = mv-2 + paso 4: «Repair first» primero; Output = trabajo extra que no es tu entrega (un favor rápido y acotado no suele costar); el desempate sólo entre lo que pasa el paso 2 | Réplica (modelo de elección de v4): trimestre + freno de salud +2,3; juez de Claude Opus 82/79, Sonnet 66/66 (v4 71/74, 66/66) | **Banco (159): L1 2,51 · 64 % · 20 · 11; control de riesgo 0,84; control 0,34.** Sondas DeepInfra (mv-2, mismo bucle) 3 de 3. Partidas: 68,64 · 77,78 (L6) · 66,06 · **cortada por `max_continuations`** (respuestas sin llamada 9, 3, 7, 21) | Sustituido por mv-4 |
| **`mejora/mv-4`** | mv-3 | + en la instrucción del manifest: «Never end a reply with text only: until the run is over, every reply carries its tool calls, so put the decision in the take_action call, not in prose.» | — | Sondas DeepInfra 3 de 3. **Partidas: 63,35 · 69,62 · 37,06 (crisis) · 18,98 (L1) · 63,27**; respuestas sin llamada 2, 1, 1, 2, 2 (mv-3: 9, 3, 7, 21) | **Candidato a entregar** (fichas, calidad y lectura de L1). Para subir la media: los hundimientos ([mejora](../mejora/README.md) §8) |
| **`mejora/mv-5r`** | mv-4 | La viñeta «Read the hidden costs», su desempate y el paréntesis del manifest, sólo en el nivel inicial | — | Banco reservado de preparación L2–L4 (39): 0,59 / riesgo 4 (= v4; mv-4 0,96 / 6). L1 (90): 3,12 y 2,99 (mv 3,57 y 2,51; v4 3,31 y 3,68). Sondas DeepInfra 3 de 3 | **Candidato a entregar en lugar de mv-4.** Partidas: 22,65 (despido en L1), 69,00 (L5) y 24,51 (despido en L1); fichas 100, 0–1 paradas. La mecánica vale; en juego, sin prueba de mejora frente a v4 |
| `mejora/mv-4q` | mv-4 | Sólo calidad (calendario, plan de L4, mentoría, comprobación del menú, bonus); protocolo y manifest idénticos | Jueces de Claude 73,5 frente a 74,5 de mv-4 en la misma tanda | — | **Descartado** (criterio previo: +3 de calidad) |
| `mejora/mv-s` | mv-5r | Manual corto: protocolo idéntico y el resto en cinco reglas ordenadas (9.681 frente a 17.380 caracteres) | Jueces de Claude 71,3 frente a 71,8 | Banco: L1 3,20; preparación 0,72; control 0,47; control de riesgo 2,00 (una sola situación, la falsa alarma de «ayudar cuesta Output») | **Descartado** por el criterio fijado (control de riesgo ≤ 1,3); no mejora nada medido |
| **`mejora/v4-loop`** | t13-read-v4 (+ protocolo de cp-v12) | v4 byte a byte salvo «Turn loop» y «Status line» de cp-v12, las frases del bucle del manifest, «never end a reply with text only» y la traducción de Concerns/Stalled (campos que DeepSeek no usaba) | — | Sondas DeepInfra 3 de 3. Partidas: 23,23 (despido en L1) y 58,95 (L5); **302 y 432 mil fichas por mes** (nota 100), 1 parada cada una | **Candidato «v4 con menos fichas»: fichas confirmadas.** El juego es el de v4; dos partidas no dicen más ([mejora](../mejora/README.md) §12) |
| `exploracion/ex-v3` | ex-v1 | En el mes previo de L1, con RR. HH. amable o quiet y sin otro riesgo en el mes, lo discreto (en privado, por escrito después) antes que corregir, negarse o plantarse en público | Réplica +0,3 sobre ex-v1; Sonnet en el banco de L1: pérdida 4,71 → 3,90, cambia las decisiones previstas | Nada | Banco de L1 (~0,12 USD); entra si deja ≤ 18 elecciones que bajan N/O y ≤ 9 arriesgadas |
| `exploracion/ex-s1` | ex-v1 | Script con estado (C60) en una tercera llamada de cada respuesta | 1.470 marcas de «lleno» sin falsos en las partidas reales; réplica +0,0 | Nada | Opcional: sondas de tres llamadas (~0,06 USD). No entregar sin partidas |
| `exploracion/ex-v2` (descartado) | ex-v1 | Revisar la opción elegida en el mes previo de L1 | Sonnet: 24 frente a 24 elecciones que bajan N/O | — | No probar |
| `formato/script-v1`, `script-v3` (en pausa) | — | Un script decide con las etiquetas de DeepSeek | — | 76,87 y 13,23; 66,55, 60,45 y 32,59: más techo, menos suelo (C23, C35) | Sólo si una idea concreta gana en la réplica |

**Descartados con DeepSeek:**
- `t13-read-v5` (66,71) y `v7` (67,27);
- `v8`, `v9` y `perceive-v5`, en el banco ([hacia-80](https://github.com/aleetreny/huawei/blob/alejandro/deepseek/lab/reports/deepseek/hacia-80.md), rama `alejandro/deepseek`).

Ninguno mejora a v4.

**Los candidatos no son excluyentes.** c5, t0/t1, suelo-min y lean-q tocan partes distintas del manual: calidad del texto, trimestre de L4, historias en situaciones trampa, y fichas. Hay que juntarlos en un solo manual. Lo sensato es confirmar cada pieza en el banco y después jugar sólo el combinado.

## 2. Ideas que aún no están en ningún manual

| Idea | Por qué puede valer | Dónde |
|---|---|---|
| Citar el menú de `observe`: Defuse y Lay low dicen `HiddenRisk −1` | Es información publicada en la partida y ayuda a la percepción del riesgo, que es lo que DeepSeek lee mejor | C38 (suelo-v1 ya lo cita) |
| Texto de resultado «sigue ahí» o «se redujo pero no se quitó»: más prudencia el mes siguiente | El riesgo sube después el 43 % de las veces, frente al 18 % (otro equipo, sin verificar) | C39 |
| Un orden de prioridades sin cláusulas de escape («la primera gana») en la instrucción del manifest | Un «salvo que…» bastó para que DeepSeek se saltara la regla (otro equipo) | [fuentes-externas §5](../fuentes-externas/kingjinsight-v11.md) |
| Conocer los techos del nivel | +8,8 en la réplica (+4,9 con la detección de Haiku), pero DeepSeek no rellena «Stalled» (C18). Sólo un script podría llevarlo | B22, B38, `hacia-80` §3 |
| Menos fichas: llamadas, notas y `check_latest_logs` | La parte de fichas está en ~64 de 100 y crece con el cuadrado del número de llamadas | C31, C43; línea Fichas en la nube si se lanza |

## 3. Lo que no hay que pagar

Ya está descartado en la réplica o con DeepSeek (fila X de HALLAZGOS):
- tolerancia al riesgo escrita como regla;
- Network doble en L2–L3;
- Skill en el trimestre desde L3;
- estancamiento por «no ha subido en el trimestre»;
- aceptar riesgo para salvar el ascenso de L1;
- C40 (el trimestre del mes 3 a crecer);
- `t13-read-v8`, `v9` y `perceive-v5`.

## 4. Lo que cuesta cada prueba y lo que detecta

| Prueba | Coste | Qué detecta |
|---|---:|---|
| Juez de calidad con DeepSeek (`ds_judge.py`) | 0,1–0,2 USD por tanda | La nota de calidad que vería el modelo designado; el juez varía ±3–5 de una tanda a otra |
| Banco emparejado (`bench.py`) | ~0,0017 USD por situación: 320 historias ≈ 0,55 USD por brazo | Si cambian las elecciones. DeepSeek repite su propia elección el 91 % de las veces (B21), así que un cambio de pocos puntos se ve |
| Prefiltro gratis: banco con **Sonnet 5** | 0 USD (cuota de Claude) | Es el sustituto más parecido a DeepSeek (C28); Haiku no sirve para esto (C24, C44) |
| Partida oficial | 0,7–0,8 USD (hasta ~1,2) | Regresiones graves, fichas por mes y que no haya acciones rechazadas. Para ver 5 puntos de diferencia harían falta ~45 partidas por brazo |

## 5. Estrategia de cortes

Cuenta la mejor versión de todas las publicadas. El corte 1 (v4) ya está dentro, y su nota oficial aún no ha salido. Una versión nueva sólo suma si supera a la mejor que ya haya, así que en los cortes 2 y 3 tiene sentido entregar algo con más techo que v4, aunque sea algo menos seguro, siempre que no tenga una regresión clara.

## 6. Línea Comprobante (29 oct, rama `alejandro/comprobante`; al día 11:10 UTC)

Informe: [comprobante.md](comprobante.md). **Red de seguridad para el corte 2: `comprobante/cp-v5a`** (= v4-c5 + t0 + suelo-v1-min + bucle de una respuesta por decisión con `take_action` y `observe` juntos, sin texto, notas de una línea): 3 de 3 completas (66,27 · 65,10 · 68,13), 615–654 mil fichas por mes (nota de fichas 94–95). Sólo se sustituye por algo que la supere con pruebas (reglas de trabajo en comprobante.md §6.8).

Medido con DeepSeek:
- partidas de la familia (mismas reglas de historias): 13 largas, 10 completas de media 66,6, 2 hundidas (cp-v7 crisis mes 21; **cp-v8 atascada en L1, 28,28**), 1 explosión (cp-v8 68,20, mes 38, −5 de riesgo). `cp-v8` queda 68,20 · 28,28: su regla (Defuse antes de recuperar con RR. HH. inquieto) no intervino en ninguna de las dos;
- **el bucle de fichas depende del proveedor que OpenRouter elige para cada llamada (C56):** con Baidu, GMICloud, Parasail, Venice, SiliconFlow, Relace o Cloudflare el modelo razona en el canal oculto, calla y empareja casi siempre; con DeepInfra (y Crusoe, Wafer, DigitalOcean, Azure) no hay canal de razonamiento, piensa en voz alta y la pareja sale a cara o cruz en la primera respuesta (sondas ancladas: 1 de 3 en DeepInfra; GMICloud 1 de 2 hasta ahora). Las reglas prohíben confiar en un proveedor concreto en la evaluación. **Candidato `cp-v10`** (= cp-v9 + pareja sembrada en la pantalla Continue y desacoplada del silencio + menú principal aprendido en el primer trimestre): predicción cumplida, **8 de 8 sondas ancladas emparejan** (DeepInfra 5 de 5 narrando, GMICloud 3 de 3 en silencio; cp-v5a el mismo día 3 de 6). Partida de confirmación (29 oct, 13:05): pareja en el 100 % (91 de 91) sobre un proveedor sin razonamiento → **cp-v10 es el candidato del corte 2** (comprobante.md §6.10; guía para los documentos de `docs/entrega/cut2/` en §6.12). La partida se hundió en L1 (22,98), como la segunda de cp-v8 el mismo día: no cambia reglas (regla 1); el banco de L1 anclado (`ds-cp10-l1-GMICloud` 4,25 / `-DeepInfra` 3,63) dice que el proveedor no cambia las elecciones: los dos hundimientos son la tasa de la familia (3 de 15);
- **Candidato `cp-v11`** (= cp-v10 + trimestre de L1–L3 con la orden de v4: informes, red, informes, proyecto clave, sin Skill learning + tras una explosión sólo Defuse cada trimestre). Motivos: segunda partida de cp-v10 (61,24: Output 8–11 doce meses en L3 con Skill y Network en su tope; cierre completo = 24 meses de Defuse + Lay low); réplica: primer trimestre a Output +0,4 / +1,0, Defuse-sólo igual o mejor en las dos lecturas, cierre completo −4 de Skill y L6 25 → 21 % (comprobante.md §6.14–6.15). Lint limpio; juez igual que cp-v10. Primera partida: 25,75, muerte por Health en el mes 12 (los trimestres nuevos se cumplieron en 2 de 3; no hubo explosión). Ninguna regla pendiente de probar; más partidas sólo para media.
- **Hipótesis dudosa (Alejandro, 29 oct 16:30): la excepción de cp-v8 en la línea 2 del trimestre (Defuse antes que la recuperación con RR. HH. no tranquilo) puede hacer daño.** Números: la rama cp-v8 → cp-v10 → cp-v11 lleva 3 hundimientos en 5 partidas (28,28 y 22,98 en L1; 25,75 por salud) frente a 1 en 6 de cp-v5a/cp-v7, todas con salud 1–3 en los primeros meses. En las trazas, la excepción **sólo se disparó en cp-v10 n.º 1** (mes 6: Health 3, RR. HH. quiet → Defuse + 1 Health recovery + Lay low; mes 21: Health 4, uneasy); en cp-v8 n.º 2 y cp-v11 RR. HH. estaba sonriente con la salud baja y el trimestre fue a recuperación sin Defuse. Con una tasa base del 15–20 %, 3 de 5 sale por azar un ~20 % de las veces. No se descarta ni se confirma; **se deja de añadir reglas de trimestre o de historias por partidas sueltas, aunque la réplica las respalde, mientras la réplica no esté calibrada con las 33 partidas reales** (la ruidosa da ~42 frente a ~66 real).
- **Candidato `cp-v12`** (= reglas de cp-v5a sin tocar + sólo el bucle de cp-v10 y el menú del trimestre aprendido en la partida; lint limpio). Es el experimento limpio: separa el bucle (probado) de las reglas nuevas (no probadas). **Dos partidas completas, 56,80 y 62,83, pareja en el 100 % y fichas 100 con proveedores distintos: el bucle vale; cp-v12 es la base de cualquier entrega.** Lo que queda (comprobante.md §6.17 y Relevo 18:05): calibrar la réplica con las 35 partidas reales antes de volver a añadir reglas; probar «no se mueve» con una sonda con historial.
- lo que separa 66 de 72 en una partida completa es el mes en que llega L5 (Network tope 36 en L4 y 54 en L5; sueldo 0,7 → 1,0): 4–5 puntos. L4 se atasca en Skill (21 de 36 ascensos perdidos) y Output (12);
- la trampa de L1 es estructural: en el 24 % de las historias no hay opción sin riesgo que no cueste Network u Output; un lector estricto perfecto tiene una pérdida forzada en el 57 % de los meses previos (réplica: 73 % de ascensos en el mes 6, 9 % atascados; DeepSeek: 7 de 10 y 2 de 13).

**Candidato `cp-v9`** (texto final = cp-v8 + cierre tras explosión B35 + trimestre de L5 a Skill learning + informes + proyecto clave; réplica: neutro en nota, crisis −10 a −17 %, Output final +2,5; juez igual que cp-v8). Tres reglas de historias probadas el 29 oct se quitaron tras el banco de L1 (`ds-cp9-l1`: 28 elecciones que bajan Network u Output de 90 frente a 27 de cp-v5a y 24–25 de v4): la pista de lectura del catálogo, «no se mueve» sobre Best y el paso 4 antes que bienestar. **No se juega** (regla 4 de comprobante.md §6.8: tres partidas no pueden ver +0,3–0,5 de media); es la base de `cp-v10`.

Lo que no hay que pagar: redacciones en prosa para la pareja de llamadas (0 de 5 en sondas; sólo el bloque literal `tool_calls: [...]` funciona, y en el manifest, dentro de la instrucción, **rompe** el emparejamiento: 0 de 6); proteger S/N/O antes del riesgo también en N = 2 (réplica: −1,5, más despidos); contar las pérdidas de Health en Crecer (réplica: −0,7, más despidos en L1); trimestre al indicador «que menos ha crecido» sin conocer techos (réplica: 0).
