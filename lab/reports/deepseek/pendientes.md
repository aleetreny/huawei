# Pendientes de DeepSeek: candidatos y pruebas por confirmar

**En una frase (29 oct):** hay seis manuales candidatos derivados de `t13-read-v4`, todos probados sólo con la réplica, jueces de Claude o Haiku. Ninguno se ha confirmado con DeepSeek. La apuesta con más probabilidad de pasar a DeepSeek es el trimestre de L4 (`techo/v4-t0`), porque DeepSeek obedece las reglas del trimestre (B20). Las reglas de historias (`suelo`) son las más dudosas, porque las elecciones de DeepSeek en historias dependen de cómo lee las opciones y casi no cambian con la redacción (C27, `hacia-80.md`).

Este es el sitio único de lo que falta probar con la clave. Quien gaste DeepSeek mantiene la lista: al terminar una prueba, actualiza la fila y pasa el resultado a [HALLAZGOS](../../../HALLAZGOS.md). Los comandos exactos están en el informe de cada línea, que es la fuente; aquí sólo se enlazan.

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

## 6. Línea Comprobante (29 oct, rama `alejandro/comprobante`)

Informe: [comprobante.md](comprobante.md). **Candidato para el corte 2: `comprobante/cp-v7`** (= v4-c5 + t0 + suelo-v1-min + bucle de una respuesta por decisión con `take_action` y `observe` juntos, sin texto, notas de una línea). Medido con DeepSeek:
- fichas: 615–654 mil por mes en dos partidas completas de `cp-v5a` (nota de fichas 94–95; v4: 61–66), +3,2 de versión;
- partidas: 66,27 y 65,10 (L5, riesgo 0), tercera en juego; `cp-v3` (una llamada por respuesta) 56,92;
- banco: elige como v4 dentro del ruido (control, riesgo y L1);
- juez: 63–69, como c5.

Lo que queda por confirmar con la clave: la partida de `cp-v7` (en juego; sólo difiere de cp-v5a en que con Health baja el trimestre mantiene el proyecto clave en vez de Lay low). Lo que no hay que pagar: redacciones en prosa para la pareja de llamadas (0 de 5 en sondas; sólo el bloque literal `tool_calls: [...]` funciona).
