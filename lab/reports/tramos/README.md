# Línea Tramos: evaluar un manual en la partida real, por tramos, antes de jugar partidas enteras

**Conclusión (30 oct, 16:00 UTC).** **El banco engañaba porque no preguntaba a DeepSeek en las condiciones de la partida, y ahora hay un arnés que sí lo hace:** `scripts/tramos/fiel.py` juega el principio de la partida contra el motor oficial con la misma petición que construye JiuwenSwarm, en paralelo, a ~0,04–0,07 USD por tramo hasta la primera evaluación. Reproduce las señales de las partidas reales que el banco no reproducía: tamaño de la primera llamada (±1 %), crecimiento del historial por llamada y cuenta atrás correcta.
- **Dos errores de método encontrados por el camino.** (1) JiuwenSwarm devuelve a DeepSeek su razonamiento en el historial (`reasoning_content`; C51 decía que no). (2) JiuwenSwarm manda `top_p` 0,1 y el banco no.
- **Piloto (1,92 USD, 34 tramos hasta el mes 6, todos servidos por GMICloud).**
  - Con el arnés fiel: **v4 asciende en el mes 6 en 1 de 4 y v4-loop en 3 de 4**.
  - Sin el razonamiento en el historial (ablación, que es lo que ve el modelo cuando el proveedor no lo devuelve): **v4 2 de 12, v4-loop 11 de 14** (Fisher p = 0,005).
  - Juntos: v4 3 de 16 frente a 14 de 18.
- **Lo que significa.**
  - **El bucle de fichas no es lo que hunde L1.** En igualdad de condiciones, las reglas de v4 con el bucle ascienden más que sin él, y aguantan sin el rastro de razonamiento; v4 sin bucle no.
  - **El 7 de 9 de v4 del 27 oct no se repite hoy:** 3 de 16, p = 0,009. Las condiciones del servicio cambian de un día a otro. Una partida suelta, o tres, no separan un manual de otro.
  - **v4 pierde en las historias de los meses 4–5** (2,1 decisiones por ventana que bajan Network u Output, frente a 1,0), no en el trimestre: los dos llegan al mes 4 con N3 O3.
- **Siguiente paso para el corte 2:** comparar mv-5r con v4-loop en tramos fieles, ~15 por brazo, ~1,2 USD y ~30 min. Hace falta el permiso de Alejandro: la clave queda en ~12,5 USD.

Pregunta: ¿podemos saber antes de gastar partidas enteras si un manual hace jugar mejor a DeepSeek? Rama `alejandro/tramos` (worktree `~/huawei-tramos`), subtrabajo de la línea DeepSeek. Scripts: `scripts/tramos/`. Datos: `~/careerlab-data/tramos/` (exportados a `lab/data/deepseek/tramos/`). Presupuesto aprobado en el chat: 2 USD de DeepSeek.

## 1. El problema, desde los datos

Cada candidato reciente ganó en el banco y no ganó en partidas (C68 → C76, C72, C78, C79). Lo más claro está en el **primer ascenso, en el mes 6**, que decide la trampa de L1 (la mitad de los hundimientos):

| Partidas reales que llegan al mes 6 | Ascenso en el mes 6 | Atascadas en L1 hasta el mes 22+ |
|---|---:|---:|
| Familia v4 sin bucle (`t13-read-v2`…`v7`, 27 oct) | **7 de 9 (78 %)** | 1 |
| Todas las del bucle de fichas (cp-v5a…cp-v12, mv-3/4/5r, v4-loop; 28–30 oct) | **10 de 28 (36 %)** | 7 |

Fisher bilateral p = 0,05. En el banco del mes previo de L1 el orden era el contrario (mv-3 2,51 < v4 3,31–3,68 < cp 3,6–4,4). `v4-loop` (las reglas de v4 tal cual con el bucle) ascendió en el 6 en 1 de 2 y mv-5r en 0 de 3. La diferencia está confundida con la fecha (proveedores de OpenRouter) y con las reglas, pero apunta a algo que el banco no puede ver.

## 2. Por qué el banco engaña: no pregunta en las condiciones de la partida

Comparación de lo que recibe DeepSeek en el banco (`scripts/deepseek/bench.py`) y en el programa oficial (peticiones grabadas con un modelo falso en el runner, `~/careerlab-data/comprobante/fake/multi2/requests.jsonl`, y eventos de las 36 partidas reales):

| | Banco | Partida real |
|---|---|---|
| Cuándo se lee el Skill | al empezar cada situación: 3–10 respuestas antes de decidir | **una sola vez, en el mes 0, en 36 de 36 partidas**; la decisión del mes 5 llega 40–60 respuestas después y la del mes 40, ~500 después |
| Prompt de sistema | `identity.md`, unas líneas en inglés | ~26.000 caracteres de JiuwenSwarm en chino («responde siempre en chino») con la instrucción del manifest dentro |
| Herramientas | 6 | 52 (~30.000 fichas) |
| Muestreo | temperatura 0,95, sin `top_p` (= 1) | temperatura 0,95 y **`top_p` 0,1**: casi determinista |
| Bucle | los pasos anteriores del mes son grabados de otra partida y no dependen de lo que elija | sus propias elecciones hacen el estado, el riesgo y el historial |
| Lo que se mide | pérdida media por decisión (q del planificador) | ascenso: todo o nada, por un punto |

Cada diferencia puede mover las elecciones. Juntas explican que un banco de una decisión con el Skill recién leído sea optimista con las reglas de historias: en la partida, la regla se leyó hace 50 respuestas y compite con el historial que el propio modelo ha escrito.

## 3. La propuesta del chat, vista con crítica

**Idea:** reproducir tramos concretos de la partida con DeepSeek en el motor, en vez de partidas enteras, para medir y mejorar cada tramo por separado.

- **Lo bueno.** Es el escalón que falta entre el banco (una decisión, contexto falso) y la partida (48 meses, n = 3). Un tramo corto en bucle cerrado mide lo que cuenta (¿asciende?) con n de decenas. DeepSeek es barato: con caché, ~0,001 USD por llamada.
- **La trampa.** Un tramo vale lo que valga su contexto. Un tramo del mes 27 que empieza con un contexto limpio **es otra vez el banco**: el Skill recién leído, sin historial. Lo que diferencia la partida del banco no es el tramo, es el contexto acumulado.
- **Qué se puede hacer con fidelidad total:**
  1. **Tramos desde el principio** (mes 0 → primera evaluación, o hasta salir de L1). El contexto es exactamente el de la partida porque *es* la partida, cortada. Cubre la trampa de L1, el primer problema.
  2. **Tramos posteriores, bifurcando partidas reales** (el prefijo grabado hasta el mes t y varias continuaciones). Exige poner el motor en ese estado: el motor oficial no tiene semillas ni carga de estado, así que haría falta la réplica (99,3 % de pasos) con un renderizador de observaciones idéntico al oficial. Sólo vale para cambios que no tocan lo que pasó antes del mes t.
- **Lo que no se puede hacer:** emparejar brazos con la misma semilla en el motor oficial (no la acepta). La varianza se paga con n.

Decisión: empezar por (1), con el motor oficial y el contexto exacto de JiuwenSwarm.

## 4. El arnés: `scripts/tramos/fiel.py`

DeepSeek juega contra el **motor oficial** (`career-emulator-engine-mcp`, modo competición, un proceso por tramo, en paralelo) con **la misma petición que construye JiuwenSwarm**:
- el prompt de sistema grabado del runner con el nombre, la descripción y la instrucción del manual donde JiuwenSwarm los pone; las 52 herramientas; el sobre del primer mensaje, el `<system-reminder>` de cada llamada y el mensaje de reanudación del runner;
- `temperature` 0,95, `top_p` 0,1, `tool_choice` auto, en streaming; sin devolver el razonamiento;
- los resultados como los devuelve JiuwenSwarm: `{'result': '<texto del motor>'}`, `success=True data={...}` para `skill_tool` y el error de JiuwenSwarm para nombres de herramienta rotos (C70).

Para en la primera observación del mes 6 (la evaluación ya aplicada: el nivel cambia entre el último paso del mes 5 y el primero del 6 en las partidas reales), con game over o tras 20 reanudaciones.

**Comprobaciones (0 USD, `fiel.py check`):** prompt de sistema idéntico byte a byte al grabado (con el manual de prueba), herramientas y `<system-reminder>` idénticos, primer mensaje igual salvo la hora, **primera observación del motor idéntica byte a byte a la grabada**, error de herramienta rota igual al de la partida real.

**Comprobación pagada (2 tramos cortos, 0,024 USD):** la primera llamada pesa 37.114 fichas con v4 y 37.325 con v4-loop, frente a 36.753 y 37.045 en sus partidas reales (`jiuwen.log`): +1 %, y la diferencia entre manuales se conserva. Queda una diferencia fija de ~300 fichas en el prompt de sistema (el runner real pudo tener memoria o rutas distintas); el manual, el Skill, las herramientas y las observaciones son los mismos.

**El razonamiento vuelve al historial (corrige C51).** La primera tanda tenía un defecto que sólo se vio comparando con las partidas reales:
- **Síntoma: el historial crecía menos.** En las partidas reales crece por llamada ~553–603 fichas con v4 y ~835–1.086 con v4-loop (`jiuwen.log`); en el arnés, 353 y 575. La diferencia es justo el razonamiento oculto de cada llamada.
- **Causa, en el código de JiuwenSwarm.** `openjiuwen/core/foundation/llm/model_clients/base_model_client.py`, `_convert_messages_to_dict`, añade `reasoning_content` a cada mensaje del asistente **que lleva llamadas a herramientas**, y `_extract_reasoning_content` lo saca de `reasoning_details` o de `reasoning`. Es el programa del agente, no el simulador (NORMAS §4).
- **Arreglo y comprobación.** Con el arreglo, el historial crece 450–813 fichas por llamada (v4) y 986–1.357 (v4-loop), como en las partidas reales.
- **Lo que cambia para Fichas.** C51 atribuía el crecimiento a resultados de herramientas y texto visible, y decía que el razonamiento no volvía. «Decidir en silencio» no saca el razonamiento del historial; lo que ahorra fichas es hacer menos llamadas. Los números medidos de fichas no cambian.
- **Prueba de que importa.** Sin el razonamiento, la cuenta atrás «Review in N» de las notas sale mal en ~40 % de los tramos (con los dos manuales; en las partidas reales de la familia v4, v4-loop, mv-4 y mv-5r, 0 de 114 notas de los meses 4–5). Con él, 23 de 24 bien.

## 5. Piloto

Motor oficial, juego de desarrollo, `deepseek-v4-flash` por la clave de la competición, sin elegir proveedor (OpenRouter mandó casi todo a GMICloud, que razona en oculto). Brazos intercalados a la misma hora; parada en la primera observación del mes 6. Datos: `lab/data/deepseek/tramos/`.

| Tanda | Brazo | Ascenso en el mes 6 | Fallos (Network/Output en el mes 6) | Llamadas por tramo | USD por tramo |
|---|---|---:|---|---:|---:|
| `r1-sin-razonamiento` (ablación) | v4 | **2 de 12** (IC 95 % 5–45 %) | 10: Output 0–2 en 7, Network 0–1 en 3 | 43 | 0,062 |
| | v4-loop | **11 de 14** (52–92 %) | 3: Network 2 en 2, Output 2 en 1 | 21 | 0,036 |
| `r2-fiel` | v4 | **1 de 4** | N1, N1, O2 | 42 | 0,074 |
| | v4-loop | **3 de 4** | N0 | 21 | 0,036 |
| Partidas reales | familia v4 (27 oct) | 7 de 9 | | | |
| | v4-loop (30 oct) | 1 de 2 | | | |

- **Las dos llegan igual al mes 4** (N3 O3 en 10 de 12 y 10 de 14): el trimestre del mes 3 no es lo que separa.
- **La diferencia está en las historias de los meses 4–5.** Decisiones por tramo que bajan Network u Output: v4 2,1, v4-loop 1,0 (ablación).
- **Por qué aguanta v4-loop sin el razonamiento:** sin contrastar. Lleva en la nota una línea de estado más rígida (`Review in N | Now | Best | Reviews here`) y empareja la observación con la acción. v4 apoya su protección del mes previo en el razonamiento anterior, que se pierde cuando el proveedor no lo devuelve.
- **Proveedores.** En la evaluación oficial no sabemos quién sirve. Un proveedor sin canal de razonamiento (DeepInfra, Azure…) deja al modelo en algo parecido a la ablación, aún peor: tampoco razona la decisión en curso. **Es un argumento de robustez a favor del bucle**, por encima de las fichas.
- **Lo que este piloto no dice.** Ni la nota final ni la tasa de despidos en L1 (para en el mes 6). Tampoco nada de mv-5r, ni de otros días u otros proveedores. Con n = 4, la tanda fiel sola no separa los brazos (p = 0,49); la señal fuerte es la ablación más la tanda fiel juntas.

## 6. El escenario completo: cómo usar los tramos para decidir

1. **Qué decide la nota.** Con calidad ~70 y fichas ~100, la nota de versión es 0,8 × media de partidas + 17. La media de una partida es ≈ P(completa) × 68 + P(hundida) × 25: cada 10 puntos de probabilidad de hundimiento valen ~4,3 de media de partidas, y la mitad de los hundimientos son la trampa de L1. Mejorar 2 puntos una partida completa vale menos que bajar 5 puntos la probabilidad de hundirse. Por eso la medida principal es el **primer ascenso** y, después, **salir de L1**, no la pérdida media por decisión.
2. **Puerta antes de cualquier partida entera.** Un manual nuevo se compara con un control (v4) en tramos fieles intercalados a la misma hora, hasta el mes 6. Coste ~0,04 USD por tramo con el bucle de fichas y ~0,08 sin él. Con 20 tramos por brazo se ve una diferencia de ~30 puntos en P(ascenso en el 6) (error típico de la diferencia ~0,15); para 15 puntos hacen falta ~80 por brazo. Regla escrita antes de mirar: el candidato pasa si no queda por debajo del control.
3. **Ampliar a L1 entera.** Los tramos guardan la base de datos del motor y los mensajes; los que no ascienden en el 6 se pueden continuar hasta el 12 y el 18 sin repetir los primeros meses. Así se mide P(despido en L1) directamente.
4. **El banco se queda como filtro de regresiones** (detectó la relajación de riesgo de v9 y la falsa alarma de mv-1), no como prueba de mejora.
5. **Tramos posteriores** (L3–L4, crisis de confianza): bifurcar partidas reales con la réplica y un renderizador de observaciones idéntico al oficial. Sólo si lo de L1 da fruto; cuesta construirlo y sólo vale para cambios que no tocan los meses anteriores.
6. **Partidas enteras** sólo para confirmar fichas, paradas (`max_continuations`) y que no hay regresiones tardías.

## Relevo

1. **Hecho y por qué.** El banco y las partidas se contradecían. En vez de otro manual:
   - comparé lo que recibe DeepSeek en el banco y en el programa oficial (§2);
   - construí un arnés que juega tramos con la petición exacta de JiuwenSwarm contra el motor oficial (§4);
   - lo validé contra las partidas reales: así salió que el razonamiento vuelve al historial;
   - jugué un piloto con v4 frente a v4-loop hasta la primera evaluación (§5).
2. **Resultados y datos.**
   - Conclusión arriba.
   - Tramos, mensajes y llamadas en `lab/data/deepseek/tramos/` (`r1-sin-razonamiento`, `r2-fiel`, `smoke`).
   - Las bases de datos del motor, para continuar los tramos, están en `~/careerlab-data/tramos/r2-fiel/engines/`.
   - Gasto: 1,92 USD (0,024 de humo, 1,453 de la ablación, 0,440 de la tanda fiel). La clave queda en ~12,5 USD.
3. **Qué falló o quedó a medias.**
   - La primera tanda salió sin el razonamiento en el historial; se conserva como ablación.
   - Dos tramos de v4 se cortaron por el tope de gasto, con unos 0,06 USD gastados.
   - Quedan ~300 fichas de diferencia fija en el prompt de sistema.
   - No hay comparación de mv-5r; la tanda fiel es pequeña.
   - Falta continuar los tramos hasta el mes 18 para medir despidos en L1 (el arnés guarda la base de datos, pero aún no tiene la orden `resume`).
4. **Siguiente paso.**
   - **Para el corte 2 (hoy):** mv-5r frente a v4-loop, 15 tramos fieles por brazo (~1,2 USD, ~30 min). Regla, escrita antes de mirar: se entrega el que más asciende en el mes 6. Si la diferencia es menor de 3 tramos, decide lo de siempre: fichas, calidad y riesgo en el banco reservado (C77).

   ```bash
   cd ~/huawei-tramos && CAREERLAB_MCP_EXE=$HOME/huawei/.venv/bin/career-emulator-engine-mcp TRAMOS_DATA=$HOME/careerlab-data/tramos/r3 uv run python -u scripts/tramos/fiel.py run --arm mv5r=lab/policies-src/mejora/mv-5r/bundle --arm v4loop=lab/policies-src/mejora/v4-loop/bundle --per-arm 15 --parallel 14 --budget 1.25
   ```

   ```bash
   cd ~/huawei-tramos && uv run python scripts/tramos/analiza.py --data ~/careerlab-data/tramos/r3
   ```

   - **Después:**
     - orden `resume` para seguir los tramos que no ascienden hasta el mes 12 y el 18 (P(despido en L1));
     - repetir fijando un proveedor sin razonamiento, para medir la robustez (sólo para investigar, como `DS_PROVIDER` en `scripts/deepseek/ds.py`; hay que añadirlo a `fiel.py`);
     - con el `top_p` 0,1 y el razonamiento en el historial, volver a pasar el banco para ver cuánto cambia su orden.
