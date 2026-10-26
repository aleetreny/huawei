# Casos estudiados: qué utilizaron y qué merece probarse

Corte: 26 de octubre de 2026. **17 casos de 14 competiciones/ediciones**. Incluye ganadores por categoría y dos contrastes de podio; no son 17 campeones generales independientes. El puesto y su verificación se indican por separado. Resultados ajenos atribuidos a sus autores; ningún método de esta colección se ha probado aún en nuestro juego.

Las adaptaciones son propuestas propias. Véanse [fuentes y alcance](sources.md), [fichas de experimentos](strategy-cards.md) y [guía de uso](playbook.md).

<a id="c01"></a>

## C01 — AutoAscend: memoria y estrategias interrumpibles

**Competición:** NetHack Challenge, 2021. **Resultado:** Ganador general, simbólico y no industrial. **Verificación:** `organiser_confirmed`. Fuentes: [S01](https://nethackchallenge.com/report.html), [S02](https://proceedings.mlr.press/v176/hambro22a/hambro22a.pdf), [S03](https://github.com/maciej-sypetkowski/autoascend), [S04](https://github.com/maciej-sypetkowski/autoascend/blob/master/autoascend/strategy.py).

**Por qué compararlo:** Alta: un agente, observación parcial, recursos, compromisos largos y muerte irreversible.

**Mecanismo documentado:**

- Mantiene una representación explícita de objetos, inventario y niveles visitados; la decisión no depende sólo de la pantalla actual.
- Compone estrategias con condición de entrada, ejecución y finalización. Una estrategia puede interrumpir a otra: exploración, combate, emergencia.
- Abstrae operaciones de teclado de varios pasos para reducir errores operativos. El código publica condition, until, preempt y repeat.

**Lo que falló o limita la conclusión:** Los organizadores señalan que ningún agente ascendió en más de medio millón de juegos de evaluación. Ganar por puntuación mediana no significó resolver el juego; el camping temprano podía aumentar score sin avanzar.

**Adaptación para probar:**

- Probar una memoria breve de compromisos y evidencia del episodio, con condiciones de validez y actualización.
- Definir modos que puedan interrumpirse y retomarse, con condiciones de salida para evitar recuperación permanente.

**Límite de transferencia:** No importar su catálogo de objetos, conocimiento externo detallado, seeding ni modificaciones de NLE. La jerarquía es una secuencia de razonamiento de un agente, no un equipo dentro de la partida.

**Pregunta experimental:** ¿Disminuyen los errores de compromiso y las salidas evitables sin sacrificar el progreso terminal?

<a id="c02"></a>

## C02 — RAPH: aprender sólo el subproblema difícil

**Competición:** NetHack Challenge, 2021. **Resultado:** Ganador de la categoría neural; no ganador general. **Verificación:** `organiser_category_confirmed`. Fuentes: [S01](https://nethackchallenge.com/report.html), [S02](https://proceedings.mlr.press/v176/hambro22a/hambro22a.pdf).

**Por qué compararlo:** Alta para modularidad; el mecanismo de entrenamiento requiere condiciones distintas.

**Mecanismo documentado:**

- Un selector de alto nivel activa habilidades de alimentación, combate, exploración e inventario.
- El combate lo decide una política neural entrenada; otros comportamientos usan procedimientos algorítmicos.
- La política entrenada recibe características y acciones simplificadas, y concentra experiencia en segmentos relevantes.

**Lo que falló o limita la conclusión:** El mejor híbrido de su categoría quedó por debajo de los mejores simbólicos en la clasificación general. El caso no demuestra que añadir RL a cualquier módulo mejore el conjunto.

**Adaptación para probar:**

- Aislar qué fase o tipo de decisión concentra los errores de un actor barato antes de cambiar todo el modelo.
- Comparar un procedimiento general breve con una revisión específica del subproblema; medir la política integrada.

**Límite de transferencia:** Entrenamiento, segmentos pegados, selección dinámica de varios modelos y cambios de herramientas no se presumen permitidos. En el runtime oficial se conserva el único modelo designado.

**Pregunta experimental:** ¿El cuello de botella está en una habilidad acotada o en la coordinación global?

<a id="c03"></a>

## C03 — Lux S2: roles persistentes y explotación de un cuello de botella

**Competición:** Lux AI Season 2, edición original, 2023. **Resultado:** Primer puesto, ry_andy_. **Verificación:** `platform_and_host_confirmed`. Fuentes: [S05](https://www.kaggle.com/competitions/lux-ai-season-2/writeups/ry-andy-1st-place-solution).

**Por qué compararlo:** Media-alta: recursos con retorno tardío, memoria de objetivos y múltiples demandas.

**Mecanismo documentado:**

- Cada unidad conserva un rol no permanente y un objetivo de varios pasos; se comprueba su validez antes de reasignarla.
- Selecciona acciones por prioridades y evita que tareas menores consuman recursos o posiciones que necesita una tarea crítica.
- La estrategia ice conflicts acepta posiciones económicas aparentemente peores para restringir el recurso clave del rival. El autor también utilizó simulación futura aproximada.

**Lo que falló o limita la conclusión:** El autor reconoce que las cadenas logísticas de otros equipos eran económicamente superiores y que su bloqueo fallaba ante un rival con transporte flexible. Una idea contraintuitiva puede ser un especialista explotable.

**Adaptación para probar:**

- Separar objetivo de carrera, objetivo del trimestre y próxima acción; invalidar planes por feedback nuevo.
- Probar una familia que priorice el recurso limitante del estado actual y otra que preserve flexibilidad ante explicaciones alternativas.

**Límite de transferencia:** No trasladar bloqueos contra rivales a narrativas concretas ni reproducir el simulador. Las cifras y reglas de Lux no dicen nada de los umbrales del CareerSim.

**Pregunta experimental:** ¿Una prioridad dinámica evita conflictos entre crecimiento, recuperación y compromisos mejor que una lista fija?

<a id="c04"></a>

## C04 — Lux S2 NeurIPS: un pipeline explícito y presupuesto de cálculo

**Competición:** Lux AI Season 2, NeurIPS Edition, 2023. **Resultado:** Primero de 64 equipos según el autor. **Verificación:** `author_reported`. Fuentes: [S06](https://github.com/ryandy/Lux-S2-neurips-public), [S07](https://github.com/ryandy/Lux-S2-neurips-public/blob/main/src/agent_act.cpp).

**Por qué compararlo:** Media: ingeniería de ejecución y coordinación; distinto juego y edición.

**Mecanismo documentado:**

- El README identifica un agente C++ y un runner concreto; es una implementación distinta de la Python de la edición original.
- El código act ordena fases de acciones, reserva decisiones urgentes y recorre un horizonte futuro sujeto a configuración y tiempo.
- Los roles de recursos, transporte, defensa y final de episodio tienen pasos explícitos, haciendo visibles las interacciones.

**Lo que falló o limita la conclusión:** Leer el pipeline no demuestra qué componente causó la victoria. No se ejecutó el agente ni se recuperó una tabla oficial independiente de ese primer puesto.

**Adaptación para probar:**

- Convertir decisiones operativas repetitivas del laboratorio en código verificable y medir su coste por fase.
- Dar más presupuesto a decisiones o candidatas inciertas sin perder una acción válida ni inventar resultados pendientes.

**Límite de transferencia:** El horizonte futuro usa un simulador que nuestro MCP no expone. La lección de ingeniería se aplica a orquestación y comprobaciones públicas, no a reconstruir el motor.

**Pregunta experimental:** ¿El tiempo se consume en decidir mejor o en repetir trabajo mecánico?

<a id="c05"></a>

## C05 — Flat Neurons: profesor congelado y diversidad de experiencia

**Competición:** Lux AI Season 3, NeurIPS 2024, Finalizado en 2025. **Resultado:** Primer puesto. **Verificación:** `platform_labelled`. Fuentes: [S08](https://www.kaggle.com/competitions/lux-ai-season-3/writeups/flat-neurons-1st-place-approach-by-flat-neurons).

**Por qué compararlo:** Media-alta para memoria, cambio de entorno y robustez; baja para entrenamiento directo.

**Mecanismo documentado:**

- Combina IMPALA/V-trace con arquitectura que conserva información temporal y separa la elección de acción del objetivo de ataque.
- Para evitar olvido, conserva un profesor congelado y mezcla oponentes antiguos con el agente actual.
- Adapta exploración y escala de recompensas. El relato describe más de 20.000 millones de pasos durante sus experimentos.

**Lo que falló o limita la conclusión:** El campeón consideró mezclar imitación de replays externos, pero declara que finalmente no la incorporó. Sus tácticas para ocultar fuerza en el leaderboard y su gran entrenamiento no son condiciones de nuestro juego.

**Adaptación para probar:**

- Mantener un conjunto de regresión con políticas o situaciones ya dominadas; una mejora nueva debe mostrar qué pierde y qué conserva.
- Conservar familias distintas y pruebas sobre escenarios encontrados por varias políticas, con evaluación real sobre episodios completos.

**Límite de transferencia:** No importar reconstrucción de constantes ocultas, políticas entrenadas o un conjunto cerrado de respuestas por evento. Los pasos RL no son partidas completas con LLM.

**Pregunta experimental:** ¿El nuevo especialista mejora una región mientras olvida capacidades previas?

<a id="c06"></a>

## C06 — Lux S3: cambiar de enfoque cuando las reglas dejan de escalar

**Competición:** Lux AI Season 3, NeurIPS 2024, Finalizado en 2025. **Resultado:** Tercer puesto; contraste entre métodos. **Verificación:** `platform_labelled`. Fuentes: [S09](https://www.kaggle.com/competitions/lux-ai-season-3/writeups/adg4b-imitation-learning-3rd-place-solution).

**Por qué compararlo:** Media: representación de la información disponible y diagnóstico del estancamiento.

**Mecanismo documentado:**

- Tras semanas sin mejorar su bot de reglas, el autor cambió a imitación y obtuvo un agente superior a su propia base.
- Separó la predicción de tipo de acción y objetivo en dos redes.
- Reconstruyó las características desde lo observable para el agente de replay, no directamente desde toda la información del replay.

**Lo que falló o limita la conclusión:** La selección de datos privilegia resultados ganadores y omite segmentos sin interés; eso introduce selección y no demuestra que cada decisión del ganador sea buena. El autor describe limitaciones de unidades superpuestas.

**Adaptación para probar:**

- Cambiar representación o procedimiento cuando persiste un cuello de botella, en lugar de seguir añadiendo excepciones.
- Usar sólo información que el actor tenía al decidir en cualquier análisis de trayectorias; distinguir resultado bueno de decisión causalmente buena.

**Límite de transferencia:** Imitación/entrenamiento y extracción de constantes del juego requerirían aclaración; no se proponen como implementación autorizada. La adaptación inmediata es auditoría de observabilidad y revisión general de procedimientos.

**Pregunta experimental:** ¿La supuesta mejora depende de información futura o de seleccionar sólo supervivientes?

<a id="c07"></a>

## C07 — Kore: un registro temporal y permiso para abandonar

**Competición:** Kore 2022, 2022. **Resultado:** Primer puesto, Harm Buisman. **Verificación:** `platform_labelled`. Fuentes: [S10](https://www.kaggle.com/competitions/kore-2022/writeups/harm-buisman-1st-place-solution).

**Por qué compararlo:** Alta para efectos diferidos, recursos comprometidos y planes que pueden dejar de ser viables.

**Mecanismo documentado:**

- Mantiene un ledger por posición y tiempo de daño real/potencial, además de fases de defensa, ataque, expansión, minería y producción.
- Busca rutas condicionadas por objetivos y actualiza sus evaluaciones con las acciones ya comprometidas.
- Si una base no se puede defender, activa alternativas de abandono/rescate/recolocación en lugar de consumir todos los recursos en su defensa.

**Lo que falló o limita la conclusión:** El campeón necesitó dos semanas y 26 revisiones para superar consistentemente una versión propia. Un rival explotó una condición de su expansión; ajustes intuitivos y muchas versiones no garantizaron mejorar.

**Adaptación para probar:**

- Registrar obligaciones, oportunidades de recuperación y revisiones pendientes en el episodio, con fuente y fecha.
- Probar una política que pueda abandonar un objetivo de crecimiento agotado y reformularlo, sin abandonar automáticamente la partida.

**Límite de transferencia:** El ledger exacto de daño y las rutas dependen de reglas conocidas. Aquí se conservan compromisos observados y planes cualitativos, no contadores secretos ni predicciones exactas.

**Pregunta experimental:** ¿La política mantiene un objetivo por coste hundido cuando el feedback ya justifica cambiarlo?

<a id="c08"></a>

## C08 — Halite 2020: tareas, coordinación y evaluación de regresiones

**Competición:** Halite by Two Sigma en Kaggle, 2020. **Resultado:** Primer puesto declarado por ttvand. **Verificación:** `author_reported`. Fuentes: [S11](https://github.com/ttvand/Halite), [S12](https://github.com/ttvand/Halite/blob/master/Logic/rule_actions_v3.py), [S13](https://github.com/ttvand/Halite/blob/master/Logic/main_rule_based.py).

**Por qué compararlo:** Media-alta: economía de recursos, fin de horizonte y mezcla de prioridades.

**Mecanismo documentado:**

- Las secciones revisadas separan actualizar historial, puntuar tareas de alto nivel, construir un plan coordinado y traducirlo a acciones.
- El código incluye retorno al final, rescate y adaptación al comportamiento observado de rivales.
- El harness evalúa configuraciones frente a versiones y un pool fijo; conserva y evoluciona configuraciones a partir de resultados.

**Lo que falló o limita la conclusión:** El hilo original no fue recuperable. Se inspeccionaron secciones concretas del repositorio, sin ejecutar código ni probar que el archivo v3 sea exactamente el envío ganador. Sus umbrales de promoción no son una garantía estadística transferible.

**Adaptación para probar:**

- Separar razonamiento de prioridades, comprobación de recursos y ejecución exacta de una opción ofrecida.
- Comparar regresiones y resultados terminales antes de promover una variante, manteniendo actor y protocolo.

**Límite de transferencia:** No copiar números, simulación, semillas ni cierres tempranos del harness. El CareerSim se evalúa con episodios terminales y estadísticas propias.

**Pregunta experimental:** ¿Una estrategia promete una mejora que se pierde al ejecutar, coordinar o cerrar la carrera?

<a id="c09"></a>

## C09 — Halite II: fases distintas y concentración deliberada

**Competición:** Halite II, 2017–2018. **Resultado:** Primer puesto, reCurs3. **Verificación:** `organiser_confirmed`. Fuentes: [S14](https://recursive.cc/blog/halite-ii-post-mortem.html), [S15](https://www.twosigma.com/articles/halite-ii-concludes-winners-announced/).

**Por qué compararlo:** Media-alta para modos, prioridades y control de complejidad.

**Mecanismo documentado:**

- Distingue fase inicial, planificación estratégica, ajuste táctico y un modo de supervivencia para partidas prácticamente perdidas.
- Una máscara estratégica concentra esfuerzos sobre un rival, con excepciones locales para amenazas cercanas.
- Primero genera acciones razonables y después mejora bajo presupuesto; perfila la detección de interacciones para evitar trabajo irrelevante.

**Lo que falló o limita la conclusión:** El autor reconoce cegueras de la máscara y que su modo de supervivencia no intenta volver al crecimiento. Sobrevivir era una condición de clasificación en Halite; en CareerSim no sustituye la media de puntuación.

**Adaptación para probar:**

- Probar foco temporal con condiciones de excepción, y una variante que salga del modo defensivo al resolverse su causa.
- Usar un procedimiento breve por defecto y dedicar análisis adicional a decisiones inciertas o irreversibles.

**Límite de transferencia:** No ocultar avisos del juego para forzar el foco, ni importar su retirada terminal como estrategia permanente. La máscara se adapta a prioridades, no a borrar evidencia.

**Pregunta experimental:** ¿Intentar optimizar todo simultáneamente causa indecisión o derroche de recursos?

<a id="c10"></a>

## C10 — HandyRL: intuición rápida más comprobación de trampas

**Competición:** Hungry Geese, 2021. **Resultado:** Primer puesto, equipo HandyRL. **Verificación:** `author_and_participant_institution_reported`. Fuentes: [S16](https://engineering.dena.com/blog/2021/12/distributed-reinforcement-learning-with-handyrl/), [S17](https://dena.ai/news/kaggle-hungry-geese/).

**Por qué compararlo:** Alta para supervivencia frente a objetivo final y modelos con supuestos frágiles.

**Mecanismo documentado:**

- Los autores combinan una política de RL con un agente de MCTS para compensar errores de táctica y final de partida.
- Amplían experiencia desde self-play a oponentes antiguos y agresivos; detectan cooperación implícita que otros rivales no respetan.
- Adaptan representación a la geometría del juego y hacen explícito el horizonte restante.

**Lo que falló o limita la conclusión:** El relato describe 16 millones de partidas de entrenamiento inicial y 3 millones adicionales, con simulador rápido. También reconoce que el orden final dependió de emparejamientos y resultados de otros rivales.

**Adaptación para probar:**

- Añadir una comprobación general de consecuencias y compromisos a la intuición inicial, y medir su beneficio neto.
- Diseñar contrastes que cuestionen los supuestos optimistas del agente y revisar decisiones de final de horizonte.

**Límite de transferencia:** No hay restauración de estados o simulador de rollouts documentado en nuestro MCP. Se transfiere la comprobación cualitativa y la diversidad de pruebas, no su MCTS interno.

**Pregunta experimental:** ¿La política actúa como si los acontecimientos futuros fueran más cooperativos o benignos de lo que muestra el feedback?

<a id="c11"></a>

## C11 — RPS: expertos complementarios y simplificación del selector

**Competición:** Rock, Paper, Scissors en Kaggle, 2020–2021. **Resultado:** Primero según el repositorio de thisisbowen; contraste con el segundo puesto. **Verificación:** `author_reported`. Fuentes: [S18](https://github.com/thisisbowen/RPS-Kaggle-1st-Place-Solution), [S19](https://www.kaggle.com/competitions/rock-paper-scissors/writeups/georg-streich-2nd-place-solution).

**Por qué compararlo:** Media para selección adaptativa; baja para feedback y horizonte.

**Mecanismo documentado:**

- El ganador combina expertos y transformaciones de uno/dos pasos con selección probabilística y una distribución Dirichlet.
- Relata una mejora al eliminar muchos if-elses del selector; corregir la alimentación de cada experto fue decisivo.
- El segundo puesto combina buen rendimiento en un horizonte más largo con selección reciente, conservando aleatoriedad.

**Lo que falló o limita la conclusión:** El ganador declara no haber logrado una evaluación local consistentemente alineada con un leaderboard ruidoso. El método de actualización dispone de la jugada rival, que permite valorar expertos no elegidos.

**Adaptación para probar:**

- Probar un selector de familias de investigación con diversidad y estadísticas separadas, y compararlo con una regla simple.
- Ensayar la eliminación de reglas redundantes y comprobar si el actor sigue mejor una política corta.

**Límite de transferencia:** En CareerSim no conocemos los resultados de las acciones no tomadas. No actualizar todas las políticas con el resultado de una sola ni dar por evaluada una mezcla de expertos sin jugarla.

**Pregunta experimental:** ¿El selector añade complejidad sin superar a una candidata simple bien medida?

<a id="c12"></a>

## C12 — Huawei Ireland: búsqueda local con operaciones sustantivas

**Competición:** Huawei Ireland Tech Arena, Server Fleet Management, 2024. **Resultado:** Primero algorítmico y tercero general según el equipo. **Verificación:** `author_reported`. Fuentes: [S20](https://github.com/linanwx/huawei2024), [S21](https://nansenli.com/post/2024/10/huawei2024/), [S22](https://github.com/linanwx/huawei2024/blob/main/tech_arena_24_phase_2/real_diff_SA_basic.py), [S35](https://huawei.agorize.com/en/challenges/ireland-tech-arena-ai-for-cloud-x/pages/final-results?lang=en).

**Por qué compararlo:** Media en recursos y efectos tardíos; alta en formato de hackathon y presentación.

**Mecanismo documentado:**

- Usa simulated annealing con operaciones distintas de compra, movimiento, cantidad, tiempo, retirada, fusión y precio.
- Conserva estado de capacidad y operaciones pendientes para evaluar cambios coherentes.
- El autor atribuye una mejora de 1000x a acelerar el evaluador y reconoce esfuerzo perdido en PPO y en pulir el algoritmo al final.

**Lo que falló o limita la conclusión:** El mismo equipo dice superar 4–5% a los siguientes en algoritmo y quedar tercero global por la presentación. La página oficial accesible no permite corroborar ese desglose; los dos relatos del equipo no son dos verificaciones independientes.

**Adaptación para probar:**

- Definir mutaciones estructurales de política: cambiar una prioridad, un modo, una condición o varios componentes relacionados.
- Reservar tiempo y evidencias para la presentación mientras se desarrolla; no consumir el calendario sólo en subir score.

**Límite de transferencia:** Acelerar un evaluador abierto no autoriza leer o reescribir nuestro motor. Las operaciones y SA sobre políticas son propuestas externas con ruido, no optimización exacta de planes del CareerSim.

**Pregunta experimental:** ¿El atasco viene de mutaciones superficiales o de invertir en el componente equivocado?

<a id="c13"></a>

## C13 — Huawei Ireland: separar restricciones de la búsqueda

**Competición:** Huawei Ireland Tech Arena, Server Fleet Management, 2024. **Resultado:** Segundo puesto según autores. **Verificación:** `author_reported`. Fuentes: [S23](https://github.com/acheong08/hwta-ireland-2024), [S24](https://github.com/acheong08/hwta-ireland-2024/blob/phase2/solver/sat.py), [S25](https://github.com/acheong08/hwta-ireland-2024/blob/phase2/heuristics.py).

**Por qué compararlo:** Media para presupuestos explícitos; baja para predecir el futuro del juego.

**Mecanismo documentado:**

- El repositorio declara CP-SAT y Pattern Search; el código construye variables enteras para acciones de compra/retirada/capacidad.
- Modela restricciones y costes, y maximiza un beneficio definido en ese problema.
- Un módulo heurístico ordena decisiones de capacidad por rentabilidad y disponibilidad.

**Lo que falló o limita la conclusión:** No se reprodujo el modelo ni se aisló la contribución de cada módulo al resultado. La mera presencia de CP-SAT no demuestra que su modelo sea una descripción exacta del problema real.

**Adaptación para probar:**

- Enumerar o filtrar planes trimestrales mediante costes y límites públicos antes de que el agente los compare.
- Separar validez de una acción de su utilidad estratégica desconocida; garantizar lo primero sin fingir lo segundo.

**Límite de transferencia:** No atribuir probabilidades o beneficios inventados a opciones narrativas para alimentar un solver. Cualquier puntuación subjetiva debe declararse como hipótesis, no regla interna.

**Pregunta experimental:** ¿Perdemos por acciones inválidas o por elegir mal entre opciones válidas?

<a id="c14"></a>

## C14 — Psyho: reducir la representación antes de escalar

**Competición:** AtCoder World Tour Finals Heuristic, 16 de julio de 2025. **Resultado:** Primer puesto. **Verificación:** `organiser_confirmed`. Fuentes: [S26](https://github.com/FakePsyho/cpcontests/blob/master/atcoder/awtf2025/approach.md), [S27](https://atcoder.jp/contests/awtf2025heuristic/tasks/awtf2025heuristic_a/editorial).

**Por qué compararlo:** Alta para investigación bajo tiempo; baja para simulación exacta.

**Mecanismo documentado:**

- Reduce un problema de muchos grupos a un grupo y trayectoria común; busca paredes y repara destinos con BFS.
- Pasa de hill climbing a SA y mejora también el orden de reparación.
- Prueba 10x tiempo para diagnosticar potencial de escala. Al observar margen, acelera el verdadero cuello de botella en vez de añadir otra arquitectura.

**Lo que falló o limita la conclusión:** Algunas ideas intuitivamente prometedoras no ayudaron; el autor distingue mejoras futuras no implementadas y reconoce que el resultado dependió del problema. Sus millones de simulaciones son iteraciones de evaluación barata dentro de su solver.

**Adaptación para probar:**

- Probar una política con una prioridad principal y pocas excepciones, frente a un diseño con muchas reglas.
- Hacer un experimento de escalado del presupuesto para separar falta de exploración de una representación pobre; contar episodios, tokens y tiempo.

**Límite de transferencia:** No convertir 10x iteraciones de un solver determinista en una promesa de 10x partidas MCP o de rendimiento. La simplificación debe conservar decisiones válidas y evaluarse de nuevo.

**Pregunta experimental:** ¿Estamos optimizando demasiado un espacio de políticas innecesariamente complicado?

<a id="c15"></a>

## C15 — ALE-Agent: reconstrucciones grandes y valor de inversión futura

**Competición:** AtCoder Heuristic Contest 058, 14 de diciembre de 2025. **Resultado:** Primer puesto según el informe del equipo y comentarios citados de organizadores. **Verificación:** `author_reported_with_organiser_comments`. Fuentes: [S28](https://sakana.ai/ahc058/).

**Por qué compararlo:** Alta para estancamiento y diseño de candidatos; baja para evaluador.

**Mecanismo documentado:**

- Construye planes diversos con un greedy parametrizado y los refina con simulated annealing.
- Además de pequeños cambios, incorpora vecindarios que reconstruyen grandes partes del plan.
- La heurística virtual power da valor a inversiones que todavía no producen; los resultados de pruebas se resumen para orientar nuevas generaciones.

**Lo que falló o limita la conclusión:** Autores reportan 4773 llamadas de dos modelos y ~USD1300 con infraestructura. El propio informe dice que aislar qué componentes causaron el resultado sigue siendo investigación; no prueba que gastar más gane siempre.

**Adaptación para probar:**

- Mutar conjuntamente prioridad, condición de entrada y salida cuando los cambios atómicos no pueden cruzar un valle.
- Probar una familia de inversión con retorno tardío y evaluarla hasta terminación, sin descartarla por un proxy temprano.

**Límite de transferencia:** No importar el valor numérico de virtual power, tablas precomputadas de un motor cerrado ni el simulador rápido. El laboratorio propone y evalúa políticas por la interfaz legítima.

**Pregunta experimental:** ¿Necesitamos cambiar de plan global para que una inversión que hoy parece mala tenga sentido?

<a id="c16"></a>

## C16 — Unagi: cambiar la representación de un subproblema medible

**Competición:** ICFP Programming Contest, 2025. **Resultado:** Primer premio: MOYOU y Unagi en la página oficial. **Verificación:** `organiser_joint_first_prize`. Fuentes: [S29](https://sakana.ai/icfp-2025/), [S30](https://icfpcontest2025.github.io/prizes.html).

**Por qué compararlo:** Alta para ciclo humano/LLM/evaluador y abstracciones; baja para el problema SAT.

**Mecanismo documentado:**

- Unagi parte de un solver humano y encarga a ShinkaEvolve optimizar su codificación SAT con un objetivo de tiempo concreto.
- En 320 pruebas/~USD60, el autor reporta pasar 2,86→0,44 s y 127→13 s en dos tamaños.
- Una representación intermedia separa qué vértices se conectan de qué puertas concretas; la idea se reutiliza después por humanos.

**Lo que falló o limita la conclusión:** Es un experimento focal dentro de una solución y equipo mayores, no una victoria autónoma por USD60. La página oficial también incluye MOYOU en el primer premio.

**Adaptación para probar:**

- Buscar una abstracción intermedia que el trabajador pueda seguir: necesidad observada → objetivo → comparación de opciones.
- Optimizar un cuello de botella comprobable y trasladar una idea sólo después de validarla en otras familias de política.

**Límite de transferencia:** No copiar codificaciones SAT para fórmulas desconocidas del juego. Más estructura textual puede ayudar o perjudicar a un actor pequeño; debe medirse.

**Pregunta experimental:** ¿Un cambio de representación vale más que muchas revisiones de redacción?

<a id="c17"></a>

## C17 — Flatland: greedy válido, reparación local y vecindarios adaptativos

**Competición:** Flatland Challenge, 2020. **Resultado:** Primer puesto OR, An_Old_Driver. **Verificación:** `competition_report_confirmed_category`. Fuentes: [S31](https://jiaoyangli.me/files/2021-ICAPS.pdf), [S32](https://proceedings.mlr.press/v133/laurent21a/laurent21a.pdf).

**Por qué compararlo:** Alta para interdependencias, cambios inesperados y presupuesto de búsqueda.

**Mecanismo documentado:**

- Tras comprobar que CBS exacto no escalaba, usan planificación priorizada para obtener una solución válida.
- Large Neighborhood Search retira y replanifica subconjuntos relacionados por demoras, cruces o salida común; adapta la frecuencia de operadores a su mejora.
- Conserva varias prioridades iniciales y repara parcialmente tras averías, manteniendo partes no afectadas.

**Lo que falló o limita la conclusión:** Los autores encuentran que aumentar el tamaño del grupo en el solver exacto no ayuda y sí encarece. Su mejora de flujo se mide sobre sus instancias; no establece un tamaño óptimo universal de vecindario.

**Adaptación para probar:**

- Crear una política sencilla válida y reconstruir sólo los módulos vinculados a un fallo, con regresiones del resto.
- Elegir mutaciones por dependencia del fallo: obligaciones, prioridades, memoria y salida del modo pueden necesitar cambiar juntas.

**Límite de transferencia:** Su sigla MCP significa Minimum Communication Policies, no Model Context Protocol. Sus garantías de rutas y presupuesto exacto requieren un grafo conocido; no se trasladan al juego.

**Pregunta experimental:** ¿Los módulos que interactúan bloquean las mejoras cuando sólo cambiamos uno cada vez?
