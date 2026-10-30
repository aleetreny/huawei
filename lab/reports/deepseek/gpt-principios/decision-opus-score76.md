# Decisión revisada: qué merece investigar para una media general de 76+

> **Revisión posterior, 30 oct:** [revision-opus-78.md](revision-opus-78.md) y [encargo vigente](encargo-opus-78.md). Se conserva este informe como evidencia histórica; sus prioridades han sido revisadas.

**Conclusión: mantener mv-4 y concentrar el siguiente trabajo en errores de interpretación y de aplicación de prioridades identificables en las trazas; no abrir otro planificador ni una batería de reglas trimestrales. La evidencia actual no demuestra un camino hasta 76 de media sostenida.**

Esta revisión **sustituye las prioridades** de hoja-ruta-opus-l6.md. Ese documento es demasiado amplio y propone como apuestas principales ideas cercanas a pruebas ya hechas. No enviarlo a Opus sin esta corrección. Entrega breve: encargo-opus-score76.md.

## 1. Objetivo corregido con la regla oficial

Fuente: local-runs/official-runner/docs/competition-rules.rst:145–198. Stage 1 = 0,8 × media de tres quantitative_score + 0,1 × calidad del Skill + 0,1 × media de eficiencia. competition_partial_score ya lleva 0,7 y NO entra como quantitative_score. El 70/30 con jurado es Stage 2 y no se mezcla aquí.

Para 76 general y eficiencia 100:

| Calidad oficial supuesta | Juego medio necesario |
|---|---:|
| 70 | 73,75 |
| 73 | 73,375 |
| 80 | 72,50 |
| 90 | 71,25 |
| 100 | 70,00 |

La calidad 73 es aproximación de jueces sustitutos de mv-3, no dato oficial. No suponer que los rivales tienen 73 ni que su 76 exige tres L6. La clasificación consultada por web no fue accesible en esta sesión; el registro local C45 contiene 75,99 y el usuario señala 76+. No se ha verificado una clasificación nueva. Un score de tres carreras y mejor versión no identifica esperanza poblacional ni constancia. El 76+ prueba éxito en una evaluación, no la técnica utilizada.

## 2. La distancia real: dos problemas, no uno

Recálculo de ocho informes mv puntuados (una novena intentada quedó sin nota): juego 58,095; eficiencia media 85,737; general hipotético con calidad 73 = **62,350**. No es una nota oficial ni una estimación precisa de una sola política: mezcla mv-3/mv-4 con muestras pequeñas. Seis completas: 68,12. Dos derrotas puntuadas: media 28,02.

Aunque se sustituyeran mágicamente todas las derrotas por una carrera media de 68,12, con calidad 73 y fichas 100 el resultado sería **71,796**, no 76. Hay que mejorar las completas y reducir fallos. Tampoco basta con producir L6 ocasionales.

Sensibilidad, no pronóstico: sea C la media completa y p la probabilidad de derrota; supónganse derrotas de 28,02, calidad 73, eficiencia completa 100 y derrotas 50. Entonces E[general] = 0,8[(1−p)C+p·28,02]+7,3+10−5p. Para llegar a 76:
- C=75 requiere p≤3,05 %;
- C=77,78 permite p≤7,86 %;
- C=74 requiere p≤1,20 %.

Esto explica por qué no elegimos entre techo y suelo: necesitamos ambos. La tasa actual de dos derrotas de ocho no es una estimación precisa de p.

Las completas pierden en promedio 1,50 puntos de bienestar frente al máximo, 0,897 de Skill directo, 0,167 de riesgo y 2,75 de red. Son déficits contables, no ganancias recuperables garantizadas ni independientes. El cierre puede aportar, pero no sustituye adelantar ascensos y generar riqueza.

## 3. Corrección importante: la denuncia anónima NO era el error demostrado

En mv-4__0f4bf379-00002, mes 26, el catálogo empírico propio para el menú observado (nodo 7f4fb6deb62e) da riesgo +1 a la opción elegida y +2 a la otra. El Skill contiene un fallback para todas las opciones arriesgadas: elegir la menor. Por tanto mi diagnóstico anterior de incumplimiento inequívoco del veto era incorrecto. No redactar una regla que prohíba la mejor opción disponible en ese menú.

La carrera tiene decisiones anteriores con alternativa de menor riesgo, y una elección de +2 frente a +1 en el mes 18 cuando todas eran arriesgadas. La opción anónima no es el sitio donde demostrar la reparación. Hace falta valorar los intercambios anteriores y las continuaciones; cambiar una elección no conserva necesariamente el resto de la historia.

También debemos evitar tratar el comentario mensual de HR como contador vivo o conocimiento del futuro.

## 4. Auditoría nueva de registros de decisiones

Reproducible: `python3 scripts/deepseek/gpt_mv_evidence.py`; salida guardada en mv-evidence.json. Sólo datos pagados y catálogo de la réplica; ninguna API ni simulación. De 1.056 registros de historia con varias opciones, se identificaron 1.050 mediante título, número de opciones y texto elegido; cuatro no tienen elección/texto válido y dos son ambiguos/no emparejados. El formato del catálogo guarda sólo riesgos no nulos (replica.build): ausencia implica cero según ese modelo.

Resultados descriptivos de los nueve intentos mv, incluida la parte observada del interrumpido:

| Señal | Recuento | Interpretación correcta |
|---|---:|---|
| Elección con riesgo positivo | 114/1.050 | Riesgo según catálogo, no percepción disponible al agente |
| Riesgo positivo con alternativa no positiva y no letal por Health inmediatamente | 62 | Puede haber costes de crecimiento, dignidad u otras consecuencias; no son 62 errores probados |
| Lo anterior fuera de los dos meses previos a evaluación | 31 | Investigar acumulación temprana y riesgos no necesarios; no vetarlos todos a ciegas |
| Lo anterior con HR frowning/uneasy/angry | 6 de 106 decisiones con ese HR | Sólo endurecer modo estricto actúa sobre un subconjunto pequeño |
| Todas las opciones con riesgo positivo | 51 | Son menús sin opción de riesgo cero |
| En esos menús elige más riesgo que el mínimo | 7 | Fallos locales de magnitud potencialmente corregibles; no demuestra mejora de carrera |
| Pérdida N/O cerca de evaluación con alternativa de riesgo no positivo y N/O no decreciente | 14 de 346 decisiones cercanas | Cuatro L1, cuatro L2, tres L3, tres L4; puede costar Skill u otro indicador |
| Opción dominada en los seis efectos inmediatos y riesgo | 16 | Alternativa al menos igual en todos y mejor en alguno; no prueba dominancia de continuación futura |

Los subconjuntos se solapan. Son registros exportados, no una prueba independiente por elección; se agrupan por carrera/título para inferencia. No son cuotas de mejora causal. La auditoría no infiere cada contador de riesgo ni reconstruye la carrera alternativa.

Los menús con todas las opciones arriesgadas aparecen 13 veces en 470 registros mv-3 y 38 en 580 mv-4. No atribuir sin más la diferencia de notas al manifest: las exposiciones difieren, por azar y/o por continuaciones inducidas por decisiones. Tampoco atribuirlas todas a suerte.

## 5. Qué retiro de la hoja de ruta anterior

Fuente directa: comprobante.md §6.5, techo/README.md §§3–6, exploracion/README.md §3.

| Idea | Evidencia existente | Decisión |
|---|---|---|
| Trimestre al indicador más lejos de su umbral verdadero | 59,8→60,2; L6 25→26 % (réplica antigua, lectura exacta) | No apuesta principal. Incluso ese control privilegiado ofrece poco en esa prueba |
| Trimestre al indicador que menos ha crecido | 59,8→59,8; L6 25→21 % | No repetir con otro nombre |
| Más Output desde L5 | ~0 en media en la batería de Comprobante; combinaciones ya buscadas en Exploración | No justificarlo por la única carrera que quedó corta de Output |
| Penalizar pérdida de Health en crecimiento | 59,8→59,1, más despidos | No proponer salud preventiva como solución demostrada; falta mecanismo nuevo medido |
| Endurecer todo después de explosión | Menos crisis, pero −0,2 y L6 25→20 % con lectura exacta | No trasladar automáticamente al candidato |
| Scripts que deciden historias / híbrido de confianza | −3 a −4,5 / hasta −0,7 en réplica calibrada | Fuera del siguiente encargo |
| Relectura, revisor genérico, memoria de resultados, checklist amplio | Pruebas sin mejora o regresiones | No reabrir sin nueva evidencia específica |
| Seguir bajando tokens cuando ya puntúan 100 | Ganancia marginal de nota cero | Congelar bucle y su anclaje |

Las réplicas antiguas tienen problemas de calibración; estos negativos no son teoremas universales. Sí son razón suficiente para no destinar el siguiente esfuerzo a repetirlos de forma especulativa.

## 6. Mi apuesta real: dos hipótesis y una puerta de entrada

### Puerta: localizar errores recuperables antes de escribir

Construir una tabla sin texto de eventos para el diseñador, agrupada por mecanismo. Priorizar los 16 casos localmente dominados, los 14 de protección de N/O y los 31 de riesgo fuera de ventana. Confirmar en trazas crudas los casos que vayan a sostener una conclusión. Valorar las mejores alternativas con continuaciones coherentes y controles de información; no sumar diferencias locales como si fueran nota final.

Seleccionar como máximo dos mecanismos que se repitan en varias carreras/títulos y tengan impacto. No forzar el mismo mecanismo a explicar toda derrota. Si un caso se debe a menú sin alternativa, no generar un veto nuevo.

### Hipótesis 1: corregir una confusión semántica estrecha, con prueba reservada

La evidencia más fuerte de transferencia textual es mv-1→mv-3: nombrar costes específicos y arreglar la prioridad del desempate cambió elecciones reales en banco sin romper controles. Es más prometedor que diseñar otra política de trimestre.

Aplicar ese método a UNA confusión repetida encontrada por la puerta anterior: p. ej. que la intención constructiva haga invisible un coste, que se confunda trabajo propio con trabajo adicional, o que se trate toda reparación como reducción de riesgo. Son posibles categorías, no conclusiones ya demostradas. No escribir una nueva lista general de palabras peligrosas.

Desarrollo en un conjunto, evaluación por títulos reservados, control mv-4 repetido. Evaluar coste y riesgo de las discrepancias, no sólo coincidencia de elección. Mantener prueba de L1, salud y riesgo para detectar contaminación. Si no cambia la lectura/elección relevante más que el ruido del control, abandonar.

### Hipótesis 2: corregir una ambigüedad de ejecución de la política, sólo si explica casos

Candidatos a auditar: «Skip a step if it would remove every option» frente al fallback de menor riesgo; tabla «Review month: step 4 first» frente a sus condiciones HR/atasco; primera línea trimestral aplicable de salud frente a limpieza de riesgo y gasto del resto de energía. Son tensiones del texto, no bugs probados en cada carrera.

Aislar UNA precedencia para comparar, conservando definiciones y bucle. No reordenar globalmente salud/riesgo/ascenso ni eliminar excepciones por comodidad del redactor. Un agente que leyó mal el efecto no se arregla cambiando la precedencia.

### Calidad y cierre: secundarios y medidos

Una mejora real de calidad de 73 a 83 aporta 1 punto general; valiosa, insuficiente para la brecha actual. No seguir ciegamente las recomendaciones de los jueces: j02 propone recortar el bucle y eliminar memoria, justo lo que puede romper la pareja, y cambiar prioridades ya medidas. Aceptar sólo ajustes documentales/claridad con controles de comportamiento y protocolo. No dar por oficial el juez sustituto.

Cierre: reutilizar la línea existente de Mecánicas emergentes. Abrir una prueba pequeña sólo si las trazas muestran puntos finales que el manual deja escapar pudiendo recuperarlos sin comprometer el último ascenso. No abrir otra arquitectura de cierre.

## 7. Criterio honesto de avance

Objetivo principal: media general esperada de 76+, y probabilidad de superar 76 con tres carreras como indicador secundario; L6 y caída extrema son diagnósticos. No maximizar P(Q≥77,78) como objetivo único: no coincide con la petición actual ni con la fórmula de la competición.

No hay evidencia suficiente de que dos frases nos lleven de 62 a 76. Si las intervenciones con información ideal ya dan poco, detener esa vía. Si dan mucho y la lectura real no permite ejecutarlas, el cuello es percepción: no disfrazarlo de falta de un planificador. Si el banco sólo gana en los títulos usados para diseñar, no hay mejora confirmada.

Orden: diagnóstico acotado → dos hipótesis como máximo → comparación aislada → reservado y controles → sólo entonces candidato y propuesta de confirmación. DeepSeek sigue prohibido en este encargo; no lanzar bancos ni carreras con él, ni gastar APIs. La fase actual puede preparar pruebas y medir en réplica con datos ya guardados, pero no certificar transferencia al modelo real.

## Relevo

Hecho: fórmula oficial revisada; cotejadas pruebas negativas de trimestre/salud/riesgo; auditados 1.050 registros contra catálogo; corregida la lectura del menú anónimo; calculadas medias y sensibilidades de score. Script sólo estándar Python, sin red, API ni ejecución del simulador; salida agregada reproducible.

Verificación: ejecución del script, cobertura explícita, riesgos cero según serialización de replica.build, contraste de dimensiones con score_report y comprobación de sumas. No se modifican políticas, scripts ajenos ni datos primarios. La clasificación web no estuvo accesible.

Pendiente: atribución causal con continuaciones y definición de los dos mecanismos; ningún candidato nuevo. Encargo listo en encargo-opus-score76.md. Commit/push en alejandro/gpt-principios y solicitud de integración en main. No se envió a otro chat.
