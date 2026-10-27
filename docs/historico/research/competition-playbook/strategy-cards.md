# Fichas para experimentar cuando aparezca un atasco

**36 adaptaciones propuestas; ninguna ejecutada ni validada aquí.** La procedencia de cada mecanismo está en [los casos](cases.md). El [JSON](strategy-cards.json) incluye el protocolo común y etiquetas para consultar por síntoma. No cargar este catálogo completo como instrucciones del agente evaluado.

Antes de probar una ficha: fijar candidata, actor, periodo, comparador, mejora mínima útil y presupuesto; usar episodios terminales y confirmación nueva con incertidumbre compatible con comparaciones repetidas. Una regla de archivo no descarta descendientes. Véanse [protocolo previo](../hierarchical-lab/protocol.md) y [matemáticas](../hierarchical-lab/mathematics.md).

<a id="p01"></a>

## P01 — Memoria de obligaciones con evidencia

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** first_line_if_trigger_observed. Casos: [C01](cases.md#c01), [C07](cases.md#c07).

**Disparador:** olvida_compromisos, efectos_tardios.

**Hipótesis:** Un registro pequeño de compromisos vigentes evita decisiones incompatibles.

**Primera prueba:** Añadir al mismo actor una tabla breve: compromiso, evidencia del episodio, próxima oportunidad y estado; retirar entradas resueltas.

**Comparador:** La política anterior con memoria libre y presupuesto de contexto comparable.

**Medir:** Puntuación terminal; omisiones de compromisos y coste de contexto.

**Qué haría cambiar de decisión:** Si no disminuyen las omisiones o el mantenimiento desplaza el razonamiento útil, revisar o archivar.

<a id="p02"></a>

## P02 — Modos interrumpibles con vuelta al plan

**Ámbito:** policy. **Esfuerzo:** medium. **Prioridad:** first_line_if_trigger_observed. Casos: [C01](cases.md#c01), [C02](cases.md#c02).

**Disparador:** crisis_recurrentes, plan_rigido.

**Hipótesis:** Una emergencia puede interrumpir el crecimiento sin hacer permanente el modo defensivo.

**Primera prueba:** Especificar entrada, salida y objetivo al que volver para cada modo; usar sólo avisos y estado público.

**Comparador:** La misma política con una lista de prioridades sin estado de modo.

**Medir:** Puntuación; crisis evitables; tiempo defensivo tras resolverse el motivo.

**Qué haría cambiar de decisión:** Si aumentan las oscilaciones o se mantiene defensa innecesaria, probar reglas de salida más claras.

<a id="p03"></a>

## P03 — Acción como transacción verificable

**Ámbito:** engineering. **Esfuerzo:** small. **Prioridad:** first_line_if_trigger_observed. Casos: [C01](cases.md#c01), [C08](cases.md#c08).

**Disparador:** acciones_invalidas, errores_herramientas.

**Hipótesis:** Separar intención, elección válida y confirmación reduce fallos de ejecución.

**Primera prueba:** Envolver la llamada oficial con comprobación de identificador/fase/asequibilidad pública; ante ambigüedad observar antes de repetir.

**Comparador:** Cliente actual con la misma política y sin cambiar sus prioridades.

**Medir:** Acciones inválidas/duplicadas, episodios interrumpidos y latencia; score secundario.

**Qué haría cambiar de decisión:** Si sólo añade llamadas sin reducir errores, mantener únicamente las comprobaciones que aporten valor.

<a id="p04"></a>

## P04 — Objetivo persistente pero revocable

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** conditional. Casos: [C03](cases.md#c03), [C07](cases.md#c07).

**Disparador:** cambia_objetivo_sin_motivo, plan_rigido.

**Hipótesis:** Distinguir objetivo de carrera, trimestre y acción reduce el cambio caprichoso sin impedir corregir.

**Primera prueba:** Pedir objetivo actual, razón para mantenerlo y evidencia que lo invalidaría; revisar tras feedback relevante.

**Comparador:** Selección desde cero en cada decisión.

**Medir:** Puntuación; cambios sin evidencia; objetivos mantenidos pese a contradicción.

**Qué haría cambiar de decisión:** Si la persistencia genera coste hundido, modificar la condición de invalidez antes de ampliar la memoria.

<a id="p05"></a>

## P05 — Resolver conflictos de prioridades antes de gastar

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** first_line_if_trigger_observed. Casos: [C03](cases.md#c03), [C08](cases.md#c08).

**Disparador:** prioridades_contradictorias, recursos_mal_asignados.

**Hipótesis:** Un plan conjunto evita que una mejora marginal bloquee una necesidad crítica.

**Primera prueba:** Antes del trimestre, identificar usos que compiten por el mismo presupuesto y elegir un orden coherente; reobservar tras actuar.

**Comparador:** Greedy de una acción cada vez sin plan conjunto.

**Medir:** Puntuación; oportunidades necesarias que quedan sin presupuesto; acciones inválidas.

**Qué haría cambiar de decisión:** Si el plan inicial se vuelve rígido ante consecuencias nuevas, conservar planificación pero reabrir la decisión.

<a id="p06"></a>

## P06 — Enumeración de planes públicamente válidos

**Ámbito:** policy. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C13](cases.md#c13).

**Disparador:** acciones_invalidas, recursos_mal_asignados.

**Hipótesis:** Un filtro exacto de costes conocidos puede mejorar fiabilidad sin conocer efectos ocultos.

**Primera prueba:** Enumerar combinaciones pequeñas compatibles con el presupuesto público y comparar su utilidad cualitativa; ejecutar sólo la siguiente acción.

**Comparador:** El mismo razonador sin enumeración explícita.

**Medir:** Validez; puntuación terminal; tiempo y tokens adicionales.

**Qué haría cambiar de decisión:** Si filtra opciones válidas o trata beneficios supuestos como ciertos, corregir el filtro antes de evaluar utilidad.

<a id="p07"></a>

## P07 — Especialista en el subproblema que falla

**Ámbito:** policy. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C02](cases.md#c02).

**Disparador:** fallo_local_recurrente, modelo_no_sigue.

**Hipótesis:** Una revisión acotada puede resolver el cuello de botella sin complicar toda la política.

**Primera prueba:** Identificar por trazas la fase con errores y cambiar sólo su procedimiento; medir después toda la política.

**Comparador:** Política general y alternativa con instrucciones extra en todas las fases.

**Medir:** Puntuación; errores de esa fase; regresiones en fases restantes.

**Qué haría cambiar de decisión:** Si el fallo persiste en la fase o la coordinación empeora, estudiar capacidad del actor y no añadir más reglas.

<a id="p08"></a>

## P08 — Recuperación con condición explícita de salida

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** first_line_if_trigger_observed. **Prueba contraintuitiva.** Casos: [C01](cases.md#c01), [C09](cases.md#c09).

**Disparador:** sobrevive_sin_progresar, defensa_permanente.

**Hipótesis:** La prudencia puede dominar el comportamiento aun cuando ya se resolvió la necesidad.

**Primera prueba:** Añadir una reevaluación pública del motivo de recuperación y retorno a crecimiento cuando deje de justificarla.

**Comparador:** Política defensiva actual.

**Medir:** Puntuación; progreso; recaídas y duración defensiva.

**Qué haría cambiar de decisión:** Si las recaídas explican una pérdida de score, ensayar una transición más gradual; no imponer un calendario oculto.

<a id="p09"></a>

## P09 — Abandonar un objetivo que dejó de ser viable

**Ámbito:** policy. **Esfuerzo:** medium. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C07](cases.md#c07).

**Disparador:** coste_hundido, plan_rigido.

**Hipótesis:** Reformular un compromiso de crecimiento agotado puede liberar capacidad para terminar mejor.

**Primera prueba:** Permitir renunciar o renegociar cuando las opciones ofrecidas y el feedback lo justifican, registrando la alternativa concreta.

**Comparador:** Política que insiste en rescatar el objetivo previo.

**Medir:** Puntuación; coste de insistencia; consecuencias de compromisos abandonados.

**Qué haría cambiar de decisión:** Si abandona demasiado pronto o genera otras obligaciones peores, archivar esa variante sin descartar toda la familia.

<a id="p10"></a>

## P10 — Familia menos defensiva, con respuesta a avisos

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C09](cases.md#c09), [C10](cases.md#c10).

**Disparador:** sobrevive_sin_progresar, riesgo_no_calibrado.

**Hipótesis:** Puede haber oportunidades de progreso desaprovechadas por aversión genérica al riesgo.

**Primera prueba:** Comparar una política que prioriza oportunidades cuando no hay evidencia pública de urgencia, manteniendo respuesta a avisos reales.

**Comparador:** Política equilibrada/defensiva congelada.

**Medir:** Media terminal; duración y distribución de salidas tempranas; no sólo mejores partidas.

**Qué haría cambiar de decisión:** Si la ganancia aparente desaparece en media o depende de pocos éxitos extremos, hibernar la candidata.

<a id="p11"></a>

## P11 — Inversión que tarda en producir

**Ámbito:** policy. **Esfuerzo:** medium. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C05](cases.md#c05), [C15](cases.md#c15).

**Disparador:** proxy_temprano_enganoso, crecimiento_estancado.

**Hipótesis:** El valor de capacidad futura puede no aparecer en la mejora inmediata del panel.

**Primera prueba:** Crear una familia que considere aprendizaje, relaciones o capacidades como inversiones justificadas por horizonte y estado; usar episodios completos.

**Comparador:** Familia centrada en rendimiento inmediato.

**Medir:** Puntuación terminal; probabilidad de llegar a fases tardías; progreso acumulado.

**Qué haría cambiar de decisión:** Si no hay mejora terminal confirmada, no usar una narrativa de inversión para excusar resultados indefinidamente.

<a id="p12"></a>

## P12 — Concentración temporal en una dimensión

**Ámbito:** policy. **Esfuerzo:** medium. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C03](cases.md#c03), [C09](cases.md#c09), [C15](cases.md#c15).

**Disparador:** equilibrio_sin_avance, crecimiento_estancado.

**Hipótesis:** Mejorar un cuello de botella de forma concentrada puede superar pequeños avances en todo.

**Primera prueba:** Probar una prioridad dominante temporal apoyada en feedback, con excepciones por urgencia y condición de salida.

**Comparador:** Política que busca equilibrio en cada decisión.

**Medir:** Puntuación; resolución del cuello de botella; deterioro y salidas por otras dimensiones.

**Qué haría cambiar de decisión:** Si los daños colaterales superan el avance o el cuello de botella estaba mal identificado, cambiar la hipótesis.

<a id="p13"></a>

## P13 — Construir algo válido y reparar lo que falla

**Ámbito:** search. **Esfuerzo:** small. **Prioridad:** conditional. Casos: [C14](cases.md#c14), [C17](cases.md#c17).

**Disparador:** muchas_propuestas_invalidas, complejidad_sin_mejora.

**Hipótesis:** Un esqueleto sencillo puede dar una base mejor que una política ambiciosa incompleta.

**Primera prueba:** Generar una política completa breve; añadir una reparación general por fallo observado sin rehacer las partes que funcionan.

**Comparador:** Generación libre de una política compleja desde cero.

**Medir:** Mejor política confirmada por presupuesto; proporción de candidatas ejecutables.

**Qué haría cambiar de decisión:** Si la base restringe sistemáticamente ideas útiles, abrir otra familia en vez de acumular reparaciones sin límite.

<a id="p14"></a>

## P14 — Destruir y reconstruir módulos relacionados

**Ámbito:** search. **Esfuerzo:** medium. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C15](cases.md#c15), [C17](cases.md#c17).

**Disparador:** plateau_local, cambios_atomicos_no_ayudan.

**Hipótesis:** Algunas mejoras requieren cambiar juntas prioridades, memoria y condiciones de modo.

**Primera prueba:** Seleccionar un conjunto ligado a un fallo; retirar sus decisiones de diseño y regenerarlo como un bloque coherente.

**Comparador:** Mutaciones de un único módulo con igual presupuesto total.

**Medir:** Mejor score confirmado; tasa de mejora y coste de evaluación de bloques.

**Qué haría cambiar de decisión:** Si produce sobre todo regresiones, reducir el bloque o cambiar su selección; no confundir tamaño con innovación.

<a id="p15"></a>

## P15 — Vecindarios elegidos por el bloqueo observado

**Ámbito:** search. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C07](cases.md#c07), [C17](cases.md#c17).

**Disparador:** plateau_local, mutaciones_sin_diagnostico.

**Hipótesis:** Cambiar lo que causa la interacción puede rendir más que elegir al azar qué párrafo editar.

**Primera prueba:** Relacionar fallos con módulos causales plausibles y generar variantes específicas de esas interacciones; conservar hipótesis alternativas.

**Comparador:** Mutaciones aleatorias de módulos con las mismas oportunidades de prueba.

**Medir:** Ganancia confirmada por propuesta y por coste; diagnósticos refutados.

**Qué haría cambiar de decisión:** Si las atribuciones no predicen mejoras, ampliar el diagnóstico o volver a mutaciones diversas.

<a id="p16"></a>

## P16 — Aceptar retrocesos como escalones de investigación

**Ámbito:** search. **Esfuerzo:** medium. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C12](cases.md#c12), [C15](cases.md#c15).

**Disparador:** plateau_local, solo_refina_lider.

**Hipótesis:** Una candidata peor puede ser un punto de partida útil para descendientes.

**Primera prueba:** Mantener una población de desarrollo con cambios desfavorables y dar un presupuesto acotado a sus descendientes; el campeón se conserva aparte.

**Comparador:** Refinamiento exclusivamente del líder.

**Medir:** Mejor descendiente confirmado por presupuesto; origen de las mejoras.

**Qué haría cambiar de decisión:** Si consume presupuesto sin aportar descendientes distintos o útiles, dormir esa línea; un máximo ruidoso no basta para reactivarla.

<a id="p17"></a>

## P17 — Reinicios con familias realmente diferentes

**Ámbito:** search. **Esfuerzo:** small. **Prioridad:** conditional. Casos: [C05](cases.md#c05), [C15](cases.md#c15), [C17](cases.md#c17).

**Disparador:** poca_diversidad, plateau_local.

**Hipótesis:** El estancamiento puede deberse a empezar todas las variantes desde la misma representación.

**Primera prueba:** Abrir familias con prioridades, memoria o descomposición distintas y comprobar diferencias de comportamiento en episodios.

**Comparador:** Más revisiones del mismo líder con igual presupuesto.

**Medir:** Mejor política confirmada; cobertura conductual y coste de generación.

**Qué haría cambiar de decisión:** Si los textos distintos inducen el mismo comportamiento, reformular la diversidad antes de escalar agentes.

<a id="p18"></a>

## P18 — Aprender qué operador de mutación sirve ahora

**Ámbito:** search. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C15](cases.md#c15), [C17](cases.md#c17).

**Disparador:** operadores_desiguales, presupuesto_mal_asignado.

**Hipótesis:** Cambios pequeños, reconstrucciones y simplificaciones tienen productividad distinta según la fase.

**Primera prueba:** Registrar operador, coste y mejoras confirmadas; adaptar asignación conservando oportunidades exploratorias para operadores menos usados.

**Comparador:** Frecuencia uniforme de operadores.

**Medir:** Ganancia final por presupuesto; cambios en productividad y falsos éxitos.

**Qué haría cambiar de decisión:** Si la adaptación premia ruido o mata operadores de beneficio tardío, ampliar confirmación y mantener una cola justa.

<a id="p19"></a>

## P19 — Selector simple entre familias complementarias

**Ámbito:** search. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C11](cases.md#c11).

**Disparador:** ranking_cambiante, poca_diversidad.

**Hipótesis:** Una mezcla de asignación de experimentos puede explorar mejor que una cadena rígida de decisiones.

**Primera prueba:** Comparar un selector probabilístico sencillo de familias con el controlador actual; actualizar sólo con evaluaciones realmente observadas.

**Comparador:** Asignación uniforme y refinamiento del líder.

**Medir:** Mejor política objetivo confirmada bajo presupuesto equivalente.

**Qué haría cambiar de decisión:** Si no supera alternativas simples, conservar el controlador más legible; no imputar recompensas a políticas no jugadas.

<a id="p20"></a>

## P20 — Eliminar instrucciones para mejorar ejecución

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C11](cases.md#c11), [C14](cases.md#c14).

**Disparador:** modelo_no_sigue, complejidad_sin_mejora.

**Hipótesis:** Un selector o política más corta puede funcionar mejor por menor contradicción y carga de contexto.

**Primera prueba:** Retirar por grupos reglas redundantes o poco justificadas y congelar cada versión; conservar sólo procedimientos esenciales.

**Comparador:** Política larga y versión de igual longitud con mera reescritura.

**Medir:** Puntuación; seguimiento de instrucciones; tokens y errores.

**Qué haría cambiar de decisión:** Si la reducción elimina una capacidad útil, restaurarla con una formulación más clara y confirmar el conjunto.

<a id="p21"></a>

## P21 — Una prioridad principal y pocas excepciones

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C09](cases.md#c09), [C14](cases.md#c14).

**Disparador:** prioridades_contradictorias, complejidad_sin_mejora.

**Hipótesis:** Reducir grados de libertad puede hacer consistente al actor sin empobrecer la estrategia útil.

**Primera prueba:** Crear una familia con un objetivo dominante observable y excepciones de urgencia explícitas; compararla con variantes de distintos objetivos.

**Comparador:** Política con muchas prioridades simultáneas.

**Medir:** Puntuación; coherencia; fallos causados por prioridades ignoradas.

**Qué haría cambiar de decisión:** Si gana sólo en una región, tratarla como especialista y medir su integración; no declararla universal.

<a id="p22"></a>

## P22 — Necesidad → objetivo → opción

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C08](cases.md#c08), [C16](cases.md#c16).

**Disparador:** razonamiento_desordenado, modelo_no_sigue.

**Hipótesis:** Una representación intermedia puede facilitar decisiones de opciones sin convertirlas en una tabla.

**Primera prueba:** Pedir un registro conciso de necesidad con evidencia, objetivo elegido y comparación de opciones ofrecidas.

**Comparador:** Elección directa desde el texto y variante de longitud comparable.

**Medir:** Puntuación; coherencia entre necesidad y acción; coste de tokens.

**Qué haría cambiar de decisión:** Si añade prosa sin mejorar consistencia, simplificar la representación o retirarla.

<a id="p23"></a>

## P23 — Archivo de regresiones y campeón congelado

**Ámbito:** evaluation. **Esfuerzo:** small. **Prioridad:** first_line_if_trigger_observed. Casos: [C05](cases.md#c05), [C08](cases.md#c08).

**Disparador:** mejora_local_regresion_global, solo_mira_ultima_version.

**Hipótesis:** El progreso aparente puede esconder pérdida de capacidades ya conseguidas.

**Primera prueba:** Mantener referencias congeladas y diagnósticos de fallos conocidos; confirmar rendimiento de políticas completas en nuevos episodios.

**Comparador:** Promoción que compara sólo con la última versión en el lote de selección.

**Medir:** Score confirmado y regresiones por familia de fallo; coste total de comprobación.

**Qué haría cambiar de decisión:** Si el archivo guía sobreajuste a un conjunto pequeño, reservar una validación nueva y rotar la cobertura diagnóstica.

<a id="p24"></a>

## P24 — Diversidad de condiciones, no sólo del propio estilo

**Ámbito:** evaluation. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C05](cases.md#c05), [C10](cases.md#c10).

**Disparador:** fragilidad_escenarios, sobreajuste_dev.

**Hipótesis:** Los supuestos aprendidos de una colección estrecha pueden fallar en estados poco frecuentes.

**Primera prueba:** Registrar condiciones públicas de episodios completos y comprobar cobertura; añadir familias que produzcan recorridos distintos sin controlar semillas ocultas.

**Comparador:** Repeticiones sólo de la candidata que más se usa.

**Medir:** Media terminal y heterogeneidad; frecuencia de exposición a condiciones relevantes.

**Qué haría cambiar de decisión:** Si una aparente mejora depende de seleccionar escenarios tras ver resultados, repetir con diseño prefijado.

<a id="p25"></a>

## P25 — Diagnosticar capacidad con actores compartidos

**Ámbito:** evaluation. **Esfuerzo:** medium. **Prioridad:** first_line_if_trigger_observed. Casos: [C02](cases.md#c02), [C10](cases.md#c10).

**Disparador:** modelo_no_sigue, ranking_entre_modelos.

**Hipótesis:** El actor barato puede penalizar políticas complejas por ejecución, no por valor estratégico.

**Primera prueba:** Evaluar políticas congeladas de distintas familias con actores distintos y configuración fija; revisar también rechazos baratos sobre el objetivo.

**Comparador:** Elegir todas las candidatas exclusivamente con el actor barato.

**Medir:** Acuerdo de ranking con incertidumbre; falsos descartes; score objetivo por coste.

**Qué haría cambiar de decisión:** Si la fidelidad es baja, reducir su autoridad de selección o usar un actor más capaz; no arreglar sesgo sólo con más réplicas baratas.

<a id="p26"></a>

## P26 — Estructura adicional frente a contexto compacto

**Ámbito:** evaluation. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C02](cases.md#c02), [C16](cases.md#c16).

**Disparador:** modelo_no_sigue, latencia_alta.

**Hipótesis:** Un actor pequeño puede necesitar pasos claros; uno potente quizá rinda mejor con contexto mínimo.

**Primera prueba:** Cruzar política breve/estructurada con Haiku/Sonnet/Opus disponibles como diagnóstico de desarrollo, sin mezclar celdas.

**Comparador:** Una única configuración por modelo elegida intuitivamente.

**Medir:** Puntuación por actor/configuración; seguimiento; latencia y tokens.

**Qué haría cambiar de decisión:** Si una configuración mejora velocidad pero degrada score objetivo, no promoverla sólo por throughput.

<a id="p27"></a>

## P27 — Comprobar la intuición antes de actuar

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** conditional. Casos: [C10](cases.md#c10).

**Disparador:** decisiones_optimistas, trampas_tardias.

**Hipótesis:** Un segundo paso breve puede detectar compromisos y pérdidas irreversibles omitidos por la primera elección.

**Primera prueba:** Dentro del mismo agente, revisar la opción provisional contra evidencia contraria, horizonte y obligaciones, y decidir una vez.

**Comparador:** Elección directa; no cambiar modelo a mitad de la condición experimental.

**Medir:** Score terminal; acciones reconsideradas que evitan un fallo; coste de revisión.

**Qué haría cambiar de decisión:** Si siempre ratifica la intuición o sobrecorrige hacia defensa permanente, rediseñar la pregunta de comprobación.

<a id="p28"></a>

## P28 — Registro de hipótesis contradictorias

**Ámbito:** policy. **Esfuerzo:** small. **Prioridad:** conditional. Casos: [C01](cases.md#c01), [C07](cases.md#c07), [C10](cases.md#c10).

**Disparador:** decisiones_optimistas, repite_error_de_interpretacion.

**Hipótesis:** Separar lo observado de lo supuesto puede evitar repetir una interpretación errónea.

**Primera prueba:** Anotar sólo incertidumbres activas del episodio con evidencia a favor/en contra; actualizar tras feedback sin convertirlas en reglas ocultas.

**Comparador:** Memoria que sólo conserva conclusiones afirmativas.

**Medir:** Puntuación; errores repetidos de interpretación; tamaño de memoria.

**Qué haría cambiar de decisión:** Si el registro provoca indecisión o acumula hipótesis irrelevantes, podar por utilidad actual y comprobar una versión breve.

<a id="p29"></a>

## P29 — Auditoría de información disponible al decidir

**Ámbito:** evaluation. **Esfuerzo:** small. **Prioridad:** conditional. Casos: [C06](cases.md#c06).

**Disparador:** mejora_sospechosa, sesgo_de_supervivientes.

**Hipótesis:** Una explicación retrospectiva puede estar usando el final o una acción no observada.

**Primera prueba:** Revisar decisiones con el historial público hasta ese momento; marcar explícitamente el dato futuro y evitar usarlo como entrada del actor.

**Comparador:** Análisis retrospectivo sin separación temporal.

**Medir:** Fracción de diagnósticos que dependen de fuga; mejoras que sobreviven a nueva evaluación.

**Qué haría cambiar de decisión:** Si la ventaja desaparece al retirar información futura, retirar la afirmación y rehacer el experimento.

<a id="p30"></a>

## P30 — Revisión acotada de fallo con alternativas

**Ámbito:** search. **Esfuerzo:** small. **Prioridad:** conditional. Casos: [C07](cases.md#c07), [C12](cases.md#c12), [C16](cases.md#c16).

**Disparador:** muchas_revisiones_sin_mejora, mutaciones_sin_diagnostico.

**Hipótesis:** Un fallo bien descrito puede producir una intervención mejor que una recomendación general.

**Primera prueba:** Para cada revisión, conservar evidencia del fallo, dos explicaciones plausibles, cambio elegido y predicción comprobable.

**Comparador:** Prompt genérico de 'mejora la estrategia'.

**Medir:** Mejoras confirmadas por revisión; diagnósticos refutados; coste de generación.

**Qué haría cambiar de decisión:** Si las historias de fallo no predicen efectos, ajustar el análisis en vez de convertirlas en certezas.

<a id="p31"></a>

## P31 — Perfil de tiempo por componente del laboratorio

**Ámbito:** engineering. **Esfuerzo:** small. **Prioridad:** first_line_if_trigger_observed. Casos: [C04](cases.md#c04), [C09](cases.md#c09), [C12](cases.md#c12), [C14](cases.md#c14), [C16](cases.md#c16).

**Disparador:** latencia_alta, pocas_partidas_utiles.

**Hipótesis:** El cuello de botella puede ser orquestación, red, contexto o escritura y no el número de workers.

**Primera prueba:** Medir inicio, llamadas LLM, MCP, parseo, integrador y persistencia; optimizar componentes propios manteniendo el mismo trabajo.

**Comparador:** Ejecutor actual con mismo actor/política/protocolo.

**Medir:** Episodios terminales por hora; coste; tasa de errores y concordancia de resultados.

**Qué haría cambiar de decisión:** Si aumenta throughput a costa de truncar episodios o perder evidencia, revertir esa optimización.

<a id="p32"></a>

## P32 — Presupuesto de razonamiento según incertidumbre

**Ámbito:** policy. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C04](cases.md#c04), [C09](cases.md#c09).

**Disparador:** latencia_alta, errores_decisiones_dificiles.

**Hipótesis:** Un procedimiento breve para casos claros puede liberar recursos para los ambiguos.

**Primera prueba:** Probar dos niveles de análisis dentro de una política del mismo actor, activados por contradicción o impacto observado; registrar la activación.

**Comparador:** Presupuesto uniforme breve y uniforme largo.

**Medir:** Score terminal, coste y errores según nivel; política completa como unidad.

**Qué haría cambiar de decisión:** Si el selector se equivoca al decidir qué es fácil, simplificarlo o dejar el nivel uniforme que funcione mejor.

<a id="p33"></a>

## P33 — Reanudación y deduplicación de experimentos

**Ámbito:** engineering. **Esfuerzo:** medium. **Prioridad:** conditional. Casos: [C01](cases.md#c01), [C08](cases.md#c08).

**Disparador:** trabajo_perdido, resultados_duplicados.

**Hipótesis:** La productividad útil mejora si una interrupción no reinicia todo ni duplica muestras.

**Primera prueba:** Registrar tarea, política/hash, actor, proceso/sesión y aceptación; al reanudar comprobar estado real y usar sólo interfaces oficiales.

**Comparador:** Ejecución que sólo conserva resúmenes al final del lote.

**Medir:** Episodios recuperables; duplicados; pérdida de evidencia; coste repetido.

**Qué haría cambiar de decisión:** Si un proceso o sesión no puede verificarse, registrar incompleto antes que inventar continuidad o score.

<a id="p34"></a>

## P34 — Prueba de escalado antes de multiplicar workers

**Ámbito:** search. **Esfuerzo:** medium. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C14](cases.md#c14), [C15](cases.md#c15), [C16](cases.md#c16).

**Disparador:** plateau_local, pocas_partidas_utiles.

**Hipótesis:** Más presupuesto ayuda sólo si la curva de descubrimiento conserva margen.

**Primera prueba:** Comparar búsquedas completas con presupuestos crecientes, incluyendo coordinación y confirmación; medir mejora por coste y tiempo.

**Comparador:** Presupuesto base y cambio de representación con presupuesto comparable.

**Medir:** Mejor política confirmada al cerrar cada búsqueda; variación entre búsquedas.

**Qué haría cambiar de decisión:** Si el margen se agota, cambiar representación/operadores; no justificar escala con un único resultado máximo.

<a id="p35"></a>

## P35 — Especialista contextual con probabilidad de llegar

**Ámbito:** policy. **Esfuerzo:** medium. **Prioridad:** conditional. **Prueba contraintuitiva.** Casos: [C03](cases.md#c03), [C07](cases.md#c07), [C09](cases.md#c09).

**Disparador:** regla_mes8_sospechosa, beneficio_solo_supervivientes.

**Hipótesis:** Una candidata mala global puede aportar un modo útil, pero su contexto debe ser alcanzable.

**Primera prueba:** Integrar una continuación en una política completa con prefijo fijado; aleatorizar políticas desde el inicio y medir también frecuencia de llegada.

**Comparador:** Política general y regla temporal simple como hipótesis alternativa.

**Medir:** Puntuación terminal global; llegada al contexto; distribución de estado y resultados condicionales como diagnóstico.

**Qué haría cambiar de decisión:** Si sólo gana entre supervivientes seleccionados y pierde en media completa, no promover la integración.

<a id="p36"></a>

## P36 — Reserva de evidencia y tiempo para el jurado

**Ámbito:** presentation. **Esfuerzo:** small. **Prioridad:** conditional. Casos: [C12](cases.md#c12), [C16](cases.md#c16).

**Disparador:** deadline_cerca, mejora_no_explicable.

**Hipótesis:** La puntuación algorítmica puede no compensar una explicación débil o incoherente.

**Primera prueba:** Guardar decisiones, pruebas fallidas, cambios y evidencias durante el desarrollo; reservar una fase de síntesis y validación de entregables.

**Comparador:** Preparar la presentación sólo al acabar la búsqueda.

**Medir:** Cobertura de requisitos oficiales y trazabilidad; avance de score por tiempo restante.

**Qué haría cambiar de decisión:** Si una narrativa no puede apoyarse en una prueba real, recortarla o presentarla como hipótesis pendiente.
