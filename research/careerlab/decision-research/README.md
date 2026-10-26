# Investigación de decisiones para mejorar estrategias

26 oct 2026 · propuesta y auditoría inicial · `alejandro/investigacion-decisiones`

La pregunta útil es: **¿qué cambio concreto de instrucciones mejora la carrera completa, con qué modelo y a qué coste de supervivencia?** Cada hallazgo debe terminar en una regla general que podamos probar y, si funciona, incorporar a un manual.

Esta línea complementa la carrera. No modifica `lab/protocol/prereg-v1.*`, sus criterios de selección, la cuota ni la cola de trabajos. No es un documento de entrega. No se han lanzado partidas, ajustado regresiones ni demostrado efectos causales en esta tarea.

## 1. Qué aporta sobre lo que ya existe

La carrera selecciona manuales; los digests permiten diagnosticar casos. Esta línea conecta ambos mediante un conjunto de decisiones con estado previo, hipótesis trazables y experimentos que cambian una regla. El protocolo §10 ya contempla cambios de modo, controles always/never y microaleatorización: se conserva y se concreta su uso, en lugar de crear un método de selección paralelo.

| Etapa | Pregunta | Evidencia que entrega |
|---|---|---|
| Auditoría | ¿Podemos reconstruir las decisiones sin perder partidas selectivamente? | Cobertura, hashes, faltantes y esquema |
| Descubrimiento | ¿Qué patrones sugieren una instrucción mejor? | Asociaciones y diagnóstico, nunca efectos causales |
| Experimento | ¿Cambiar esa instrucción mejora el resultado? | Comparación aleatoria de políticas completas |
| Confirmación | ¿Se repite en partidas frescas y en el modelo objetivo? | Evidencia para seleccionar y justificar la estrategia |

## 2. Auditoría inicial: límite real de los datos

Snapshot de exports de `main` en `3c1c993`; los hashes exactos están en [la auditoría](../../../lab/reports/decision-research/audit-canonical.json). Son datos retrospectivos en crecimiento, no el estado en vivo del servidor.

- Registro canónico: **322 evaluaciones**, de las cuales 316 son terminales válidas (80 completadas, 236 eliminadas) y 6 interrupciones excluidas. De las terminales, 150 son de bots y **166 de actores Claude**.
- En este Mac se localizan **99 de las 166 trazas Claude terminales**, con el hash primario correcto; **67 no están aquí**. Ausente en este Mac no significa perdida en la nube.
- El actor Haiku principal tiene 105 partidas terminales de 25 manuales, de las que 53 completan. Otras configuraciones tienen de 1 a 26 partidas: no hay tamaño para interacciones complejas por modelo y comportamiento.
- Hay **61 trabajos sin evaluación** en ese snapshot: 22 interrumpidos, 16 leased, 15 queued y 8 running. No son ceros ni fracasos observados. Estos 22 trabajos interrumpidos son distintos de las 6 interrupciones que sí tienen fila de evaluación.
- En los **383 trabajos** del export faltan campos explícitos `epoch`, `block_id`, `analysis_role` y `assignment_probability`. La documentación dice que se registran estas nociones, pero el export actual no permite verificarlas. Podrían recuperarse de decisiones u otros metadatos; no se inventan retrospectivamente.
- Export adicional `leah`: 7 evaluaciones (1 completada y 6 interrumpidas), inventariado por separado. Su única traza terminal no se ha comprobado en este Mac; no se mezcla con el registro canónico.

**Consecuencia:** antes de una regresión de comportamientos hay que recuperar/exportar las 67 trazas de nube, o ejecutar la extracción allí. Una regresión ajustada sólo a las 99 locales describiría esa muestra histórica; no representa automáticamente las 166 partidas. Los datos existentes siguen siendo útiles para descubrir hipótesis.

El script [decision_research_audit.py](../../../scripts/decision_research_audit.py) sólo lee exports del laboratorio y respuestas oficiales ya guardadas. Comprueba identidades y hashes, rechaza duplicados y dos intentos puntuados en una misma réplica, excluye interrupciones y separa actor/entorno. No lee el paquete ni las bases del simulador. No exporta razonamientos del modelo, títulos ni respuestas a eventos.

## 3. Construir el conjunto de decisiones

Se propone el siguiente esquema de extracción; **aún no está implementado**. La auditoría disponible no certifica el alineamiento temporal.

Una tabla por partida y otra por intento de acción, enlazadas mediante `origin`, `job_id`, `session_id` y un índice de decisión. Cada fila de decisión debe contener:

- Hashes del manual, actor completo, entorno y archivos fuente. Época y bloque, o `unknown` con la fuente del dato.
- Estado visible **anterior** a elegir: salud, dignidad, Output, Network, Skill, Wealth, nivel, tiempo en el nivel, fase y último feedback realmente observado.
- Conjunto de opciones disponibles, opción seleccionada e identificador del resultado oficial asociado. Rechazo/reintento y aplicación efectiva se conservan por separado.
- Categoría general de comportamiento: entrega/crecimiento, relación, recuperación o control de riesgo; permitir varias etiquetas y `unknown`. No asumir que una opción con nombre distinto es comparable.
- Estado posterior y horizonte transcurrido; evaluación, ascenso o eliminación, cuando se observan. Una acción que cambia de mes no se interpreta como un cambio instantáneo aislado.
- Para datos experimentales: brazo asignado, probabilidad conocida de asignación, semilla y momento de asignación, elegibilidad y versión de la regla.

Reglas de calidad:

1. Alinear por IDs de llamada/respuesta y sesión; una nueva acción invalida el estado anterior salvo que su respuesta proporcione explícitamente la siguiente observación. Nunca reutilizar silenciosamente una observación obsoleta.
2. Unir continuaciones en orden; registrar los hashes de **todos** los archivos. El hash que hoy registra CareerLab sólo cubre el archivo primario.
3. Comparar cobertura por actor, política, outcome, duración y origen. Faltante no equivale a cero; no imputar decisiones inexistentes tras una eliminación.
4. Codificar comportamientos sin ver la nota final. Revisar manualmente una muestra equilibrada de categorías, modelos y resultados; registrar desacuerdos y congelar el código de etiquetas antes de evaluar predicciones.
5. Calendario y nombres de eventos pueden usarse para auditar temporalidad, pero nunca se convierten en respuestas memorizadas o umbrales dentro de las Skills.

## 4. Regresión exploratoria: pequeña, predictiva y comprobable

El objetivo es producir como máximo dos hipótesis accionables por ciclo. El histórico conocido es descubrimiento, incluidos los resultados ya leídos en chats y digests. No se lo convierte retroactivamente en confirmación. Las partidas reservadas para confirmación quedan fuera de extracción exploratoria y ajuste.

Primer análisis propuesto, una vez superada la auditoría:

- Trabajar primero dentro del actor Haiku principal y un entorno/época verificables. Bots, modelos manuales y otras configuraciones quedan separados.
- Empezar con una regresión lineal regularizada para Q y una logística regularizada para completar. Usar pocas variables preespecificadas, unas 3–5 como punto de partida, según soporte real; no decenas de interacciones con unas cien partidas.
- Para predecir desde un punto intermedio, usar sólo decisiones y estados anteriores a ese punto. Reportar qué partidas seguían vivas y cuántas ya habían terminado. Una predicción entre supervivientes es condicional a estar vivo allí y no estima el efecto total de la estrategia.
- No usar nivel/riqueza finales para «descubrir» qué determina el score: son componentes del resultado. Una descomposición de puntos perdidos es descriptiva y se presenta como tal.
- Separar entrenamiento y evaluación por **partida**, y hacer una segunda comprobación dejando familias de manuales enteras fuera. Nunca repartir meses de la misma partida entre ambos conjuntos. Escalado, imputación, selección de variables y penalización se ajustan sólo en entrenamiento, con validación interna agrupada.
- Comparar contra predicciones simples: media de Q y frecuencia de completar del entrenamiento. Reportar error fuera de muestra para Q y calibración/Brier para completar. Si no mejora esos referentes o los coeficientes cambian mucho, no usarla para recomendar reglas.
- La incertidumbre de resúmenes y asociaciones se calcula remuestreando partidas enteras; si el número de partidas o familias no permite una partición útil, declarar datos insuficientes. No tratar miles de acciones como miles de carreras independientes.
- Incluir variación de contexto y opciones disponibles. Si una acción se elige siempre ante cierto estado, **no existe comparación observacional** allí: marcar falta de soporte, no extrapolar el efecto.

Ejemplo de resultado útil: «cuando no hay alerta de seguridad y no hubo ascenso, la prioridad de entrega merece un ensayo». Resultado inválido: «+1 acción de crecimiento causa +2 puntos». El estado previo afecta tanto la acción como la nota; además, decisiones anteriores modifican ese mismo estado. Una regresión ordinaria no resuelve por sí sola esa confusión temporal.

No se propone iniciar ahora modelos causales complejos, propensity scores estimados de texto ni evaluación fuera de política: el histórico no aporta probabilidades de asignación verificadas ni soporte suficiente. Una estimación sofisticada no recupera información ausente.

## 5. Primeras hipótesis para mejorar manuales

Son hipótesis basadas en diagnóstico existente, no hallazgos nuevos de una regresión.

| Hipótesis | Cambio que podemos hacer | Qué la debilitaría |
|---|---|---|
| H1. Concentrar crecimiento cuando la carrera es estable reduce el estancamiento | Añadir al mismo manual una prioridad explícita de entrega y apoyo al ascenso cuando no haya alerta de seguridad; mantener las reglas de protección | Se ejecuta la regla pero Y no mejora, o el beneficio en Q se acompaña de demasiadas eliminaciones |
| H2. Las elecciones de historia pueden deshacer el trabajo del trimestre | Reforzar la protección de Output/Network deteriorados al decidir entre opciones de historia, manteniendo integridad y salud | No cambia el comportamiento observado, o lo cambia sin mejorar Y en partidas completas |

Prioridad: **H1 primero**. El diagnóstico de bloque 3 relaciona promoción temprana con mejores carreras, pero la promoción también puede indicar una trayectoria favorable. No se afirma que forzar un ascenso produzca por sí mismo esa diferencia.

Ya existen candidatas cercanas (`f7-promotion-drive-v1`, `f7-delivery-stories-v1`, F8). Antes de escribir más manuales, auditar el diff contra el padre: si cambia varias reglas, sirve como candidata global pero no aísla H1/H2. Para el ensayo de mecanismo preparar una variante con una sola instrucción diferente y longitud semejante. No renombrar ni modificar políticas ya registradas.

## 6. Ensayo de políticas completas: el primer paso causal

La unidad de asignación es **una partida nueva**. Se congela una versión del manual base y se asigna aleatoriamente base/variante dentro del mismo actor, entorno y época; se intercalan en bloques equilibrados. La aleatoriedad se refiere al brazo del experimento: no se presupone que el simulador permita compartir semillas, clonar estados o repetir eventos.

Antes de lanzar, escribir un manifiesto inmutable con hashes de los dos manuales y su diff, actor/entorno/época, hipótesis, semilla del calendario de asignación, probabilidades conocidas, bloques, presupuesto, cortes de análisis, tratamiento de interrupciones y versión del script. Cada slot tiene un brazo preasignado; una reposición operativa conserva ese brazo y su identidad lógica.

**Estimando principal:** diferencia media de `Y = 0.8 Q + 0.1 E` entre instrucciones asignadas, usando todos los terminales válidos de los slots resueltos y el criterio prefix-complete del protocolo. Las eliminaciones cuentan con su puntuación terminal real. Las interrupciones operativas permanecen separadas y se recuperan/reponen según §3; se informan las alarmas de interrupciones, también por duración. No se puntúan trabajos pendientes ni se decide a partir de los que acabaron primero.

Para Claude, E es la sustitución `Ê` definida en v1, **no** una medida de eficiencia del modelo objetivo. La calidad documental se mantiene fuera de este estimando. Q, supervivencia, causas de eliminación y distribución de ascensos son diagnósticos secundarios. No ajustar el efecto total por ascensos, nivel final ni acciones realmente ejecutadas: son consecuencias de la asignación. El análisis principal es por la **instrucción asignada**, aunque el jugador la incumpla; la adherencia ayuda a entender por qué.

Presupuesto y decisiones:

- Una primera tanda equilibrada de **4 partidas por brazo** comprueba ejecución, instrumentación y variabilidad. No demuestra superioridad ni seguridad. Con cuota corta, incluso el experimento entero puede quedar como estimación.
- Usar Δ = **4 puntos Y**, la relevancia ya fijada en v1; planificar n con la cota de desviación del piloto y la fórmula de §5. Si la cuota no alcanza, no bajar Δ ni seguir mirando hasta obtener un resultado favorable.
- Antes de la confirmación fijar tamaño y un único análisis final, reservando datos frescos; aplicar §7 (Welch unilateral del 95 %, Bonferroni para como máximo dos afirmaciones). La confirmación no entra en generación ni selección. Cambiar el manual al verla consume esa reserva como desarrollo y exige nueva confirmación.
- Mostrar diferencia de probabilidad de completar e intervalo. No concluir «no perjudica supervivencia» por falta de significación: para afirmar no inferioridad habría que congelar un margen y dimensionar ese objetivo adicional antes de recoger datos.
- La comparativa de dos manuales sirve para H1. Si se quiere afirmar que **adaptar al estado** supera reglas fijas, añadir always/never y satisfacer §10; ganar sólo al padre no valida especialización.
- Resultados con Claude pueden orientar manuales y estimar qué investigar. La transferencia y selección de entrega requieren pruebas con DeepSeek por el runner oficial cuando exista clave. No combinar sus observaciones como réplicas de Claude.

## 7. Segunda etapa opcional: cuándo funciona una regla

Sólo si el ensayo anterior es prometedor y hay cuota, instrumentar la microaleatorización ya prevista en §10. En momentos elegibles declarados de antemano, registrar el estado **antes** del sorteo y activar/no activar la recomendación con p conocida (por ejemplo 0,5). Una recomendación que el actor puede ignorar identifica el efecto de recomendarla, no el efecto de obligar la acción.

Fijar el desenlace próximo y su horizonte antes del sorteo, conservar la eliminación como posible desenlace y no analizar sólo los que llegan a la próxima evaluación. Estimar efectos de la recomendación con probabilidades conocidas y errores agrupados por partida. La elegibilidad restringe la población a esos momentos; no extrapolar a estados peligrosos donde no hubo sorteo. Interacciones por estado son pocas y predeclaradas.

Esto estudia mecanismos locales; no basta para demostrar mejora de la carrera completa. La política resultante siempre vuelve a partidas frescas de 48 meses. Cualquier calendario/placebo es diagnóstico y nunca contenido del manual de entrega.

## 8. Entregables y siguiente paso

1. **Ahora, hecho:** protocolo de trabajo y auditoría reproducible, sin gasto de partidas/API.
2. **Siguiente implementación:** extracción temporal verificada y etiquetas generales; exportar las trazas faltantes o ejecutar en la nube; incorporar epoch/bloque/rol experimental con fuente verificable. Si no hay suficientes datos comparables, saltar la regresión y conservar sólo el diagnóstico.
3. **Primer ciclo experimental:** congelar un padre y una variante de H1, registrar el manifiesto antes de lanzar y reservar la tanda en la cuota existente. Sólo el organizador de la nube encola partidas.
4. **Producto de cada ciclo:** ficha de hipótesis, evidencia y límites, diff de una regla, adherencia, estimación de Y y supervivencia, decisión y siguiente prueba. Ninguna regla pasa a una Skill sólo por un coeficiente o una partida récord.

## Fuentes metodológicas

- [Gelman, Hill y Vehtari, capítulo 19 de *Regression and Other Stories*](https://www.cambridge.org/highereducation/books/regression-and-other-stories/DD20DD6C9057118581076E54E40C372C/causal-inference-using-regression-on-the-treatment-variable/5EC22DA4A13BFC9A5944C74D713D0408): distingue comparación predictiva y causal; la asignación experimental permite interpretar efectos de tratamientos y el ajuste debe respetar la temporalidad.
- [Hernán, Harvard](https://hsph.harvard.edu/profile/miguel-hernan/): la confusión que cambia con el tiempo y es afectada por tratamientos anteriores puede invalidar el ajuste mediante regresión convencional.
- [Equipo de MRTAnalysis, definición de efectos próximos](https://stat.ethz.ch/CRAN/web/packages/MRTAnalysis/vignettes/mrt-proximal-causal-effect.html): asignación con probabilidad conocida, disponibilidad anterior a la asignación y resultados próximos. La microaleatorización es una extensión futura, no una propiedad atribuida a nuestros datos históricos.

Estos fundamentos orientan el diseño. Los tamaños de tanda, hipótesis y orden de trabajo son decisiones prácticas del equipo; no resultados de las fuentes.
