# Encargo para Opus: L6 repetible y carreras de 77–78

> **Histórica, sustituida:** leer [revisión para 78](revision-opus-78.md) y [único encargo vigente](encargo-opus-78.md). Las revisiones encontraron experimentos negativos que despriorizan varias ideas de esta hoja y corrigieron el diagnóstico de la denuncia anónima.

**Conclusión: el objetivo central es completar L6 conservando riqueza, bienestar y control de riesgo; optimizar sólo supervivencia o ganancia inmediata de indicadores no basta. Esta hoja de ruta propone experimentos, no resultados ya obtenidos.**

## Encargo y límites

Investiga cómo aumentar P(nota de juego ≥77,78) y P(completar en L6 o superior), preservando la media y evitando nuevas derrotas. Usa mv-4 como control estable. No prometas todas las carreras a 77,78 ni declaremos un techo imposible sin demostrarlo. NO uses DeepSeek, no gastes APIs ni lances partidas oficiales. Primero datos guardados y réplica local; una confirmación futura con el modelo real necesita autorización del usuario. No modifiques el protocolo de llamadas de mv-4 durante la investigación estratégica.

Lee ESTADO, NORMAS, HALLAZGOS y lab/reports/mejora/README.md, además de mv-3-mv-4-consistencia.md en esta carpeta. Mejora ya está integrada en origin/main (b294ef6, incorporado a esta rama). El diagnóstico anterior documenta el estado previo a esa integración. Mantén el trabajo como apoyo a la línea actual, sin crear otra línea activa. No pasar texto de eventos al diseñador del manual: el análisis de datos produce conclusiones agregadas; la redacción usa esas conclusiones, no respuestas ni títulos de eventos.

## El objetivo exacto

El 77,78 de mv-3/2 combina L6, riqueza 43,8, Skill 134, Network 53, Health+Dignity 20, riesgo final 0 y componente de riesgo 10. L6 aporta 18 puntos de los 77,78. Con esos demás componentes y L5 se obtendrían 74,78: es el hito principal de la ruta observada, no condición matemática demostrada para toda posible carrera de 77,78.

Con L6 y todos los demás componentes no monetarios al máximo, la suma es 68 y hacen falta 9,78 puntos de riqueza (~39,12). Con Network 53 como en la ganadora se necesita aproximadamente su riqueza de 43,8. Son cuentas de investigación a partir de la réplica/score reports, NO umbrales para copiar al Skill. Llegar tarde a L6 con poco dinero, mala salud o una explosión puede quedar muy lejos de 77,78.

La réplica sitúa la saturación del componente directo de Skill en 120, pero el ascenso de L5 pide Skill 130, Network 45 y Output 32. Output no tiene componente propio de nota. Esto revela una discrepancia entre puntuar ahora y preparar el ascenso: no confundirla con permiso para entregar umbrales internos. Usar números exactos sólo para diagnóstico y controles con información privilegiada.

Métricas primarias: P(Q≥77,78), P(completar L6+). Secundarias: mes de entrada a cada nivel, P(crisis/despido/interrupción), percentil 10 y media, riqueza y bienestar finales; eficiencia como restricción. Separar todas las intentadas, todas las puntuadas y completas. No presentar 68,12 de las completas como media de la familia (58,095 en las ocho puntuadas, más una interrupción).

## Fase 1 — ¿Dónde se pierde la posibilidad de L6?

**Producto:** una tabla por carrera y ventana de evaluación, no otra lista de notas finales.

Reconstruir estado después de la última acción antes de evaluación (el CSV muestra estado preacción), déficit de cada requisito en la réplica, nivel, salud, HR y acciones trimestrales. Identificar la primera ventana evitable perdida y qué decisiones anteriores crearon el déficit. Separar errores de percepción, prioridades mal aplicadas, crecimiento insuficiente, costes forzosos y fallos técnicos.

Desde estados registrados, simular continuaciones alternativas en la réplica: mv-4 aproximado, un planificador con efectos exactos y uno con sólo información permitida/lecturas disponibles. Medir frecuencia de L6 y Q≥77,78, no sólo Q media. Un planificador heurístico que falla NO prueba imposibilidad. Si se usa un oráculo que ve futuros, etiquetarlo como privilegiado y no desplegable. Verificar fidelidad de transiciones donde cambia el diagnóstico.

Conservar azar emparejado sólo donde la réplica permita acoplarlo correctamente: cambiar una acción puede cambiar la continuación. No pegar efectos alternativos a una traza futura fija como si fuese una carrera válida.

Pregunta clave: ¿en qué estados aún se salva L6 con mejores decisiones y en cuáles sólo lo salva información que el agente no tiene? Priorizar los primeros.

## Fase 2 — Calendario hacia atrás, con rutas de recuperación

La ruta observada 6→12→18→36→48 deja dos evaluaciones sin ascenso en L4 y una en L5. No demuestra que L4 en 18 sea obligatorio: probar L4 en 24 con L5 en 36, y L5 en 42 con L6 en 48. Eliminar calendarios imposibles sólo con evidencia adecuada.

**Hipótesis A:** la política fija por nivel pierde oportunidades porque no estima qué indicador limita la siguiente evaluación. Investigar una política de déficit previsto: qué falta y qué crecimiento seguro cabe conseguir con el tiempo y las acciones restantes. Empezar con déficit exacto como referencia de investigación; después degradarlo a estado observado, resultados propios y tendencias sin umbrales ocultos. Si sólo gana el control privilegiado, no hay candidato desplegable.

Contrastar con mv-4 y con las reglas ya descartadas de «Skill doble»/«todo a Skill». La novedad es reasignación dependiente del cuello de botella y horizonte, no un nuevo peso fijo.

**Producto:** rutas frecuentes a L6, estados donde recuperarlas y magnitud de mejora que sobrevive a información incompleta.

## Fase 3 — Tres candidatos de mecanismo, por separado

### A. Evitar el déficit de Output en L5 sin frenar Skill en L4

Probar cambios condicionales en energía/acción principal y decisiones cercanas a evaluación: crecimiento de Skill cuando sigue siendo el límite, producción cuando ésta amenaza el ascenso, no priorizar Network sólo porque está por debajo de su máximo histórico. «Debajo de Best» no significa necesariamente «limita el ascenso».

Auditar primero si el brazo vigente desperdicia acciones por esa confusión y si el cambio recupera ventanas. No elegir una receta fija de trimestre sólo por ajustar la ganadora. Comparar con el trimestre ya buscado en Exploración y comprobar que la señal existe fuera de las semillas de búsqueda.

### B. Salud preventiva como inversión en crecimiento

mv-4 omite Skill learning cuando Health no permite hacerlo. Una opción temprana de historia que cuesta salud puede consumir luego energía de recuperación y retrasar el ascenso. Medir cuántos trimestres de crecimiento se pierden así y si evitar ese coste antes del trimestre compra más progreso neto que «recuperar al llegar al margen».

El candidato debe ser selectivo: no bajar globalmente ambición ni repetir un mero cambio del umbral de salud. Medir recuperación, Skill acumulada, ventanas ganadas, N/O cedidos y crisis. Descartar si la supervivencia mejora pero L6 se vuelve menos frecuente sin compensación suficiente en Q.

### C. Modo estricto que evalúe el mecanismo, no la buena intención

Hipótesis histórica: separar intención constructiva del mecanismo de la acción. **Corrección:** la denuncia anónima de mv-4/3 ofrecía +1 frente a +2 de riesgo; no prueba contradicción con el filtro/fallback. No usar ese caso para justificar una regla nueva. Las prioridades vigentes están en la revisión para 78.

Banco con HR adverso y después de explosión, más controles de reparación segura y de todas-las-opciones-malas. Analizar también el riesgo temprano que obliga luego a gastar trimestres limpiando y pierde crecimiento. No esperar a la primera explosión para medir daño: aunque sobreviva, la penalización y los recursos de recuperación perjudican 77,78.

No reabrir tolerancia global al riesgo: ya produjo crisis. Una excepción nueva sólo se estudia donde recupera una ventana y existe una recuperación posterior plausible con información disponible; el contador real oculto sólo sirve de control de investigación.

## Fase 4 — Lectura enfocada en la decisión que cambia el ascenso

El objetivo no es reconocer todos los signos con igual precisión. Identificar las opciones para las que confundir una pérdida de Output/Network cambia la posibilidad de ascender, y las falsas alarmas que bloquean una alternativa válida. Medir coste por error, no sólo acierto global.

Probar una representación breve y concreta: entrega propia, carga adicional, crédito, efecto interpersonal, mecanismo de reparación y dudas. Es hipótesis; no generar checklist largo por defecto (ya falló). Separar interpretación de elección para diagnosticar si el problema es leer o aplicar prioridades.

Reservar títulos completos fuera del desarrollo. Probar errores en L2/L3/L4, no sólo L1: la mejora existente está concentrada allí, mientras que seis meses perdidos más tarde también pueden eliminar L6. No trasladar automáticamente las señales sociales de L1 a todos los meses; ya sabemos que extenderlas puede empeorar crisis.

Con la restricción actual se construye y analiza el banco usando material ya pagado. No confundir una simulación de «detectar el 80 % de los errores» con un método que realmente lo consigue.

## Fase 5 — Convertir L6 en nota alta

Una vez suba L6, separar ascenso de liquidación final. Si la última promoción ya ocurrió, dejar de gastar en crecimiento sin valor y comparar recuperación de bienestar, reducción de riesgo y riqueza/red. Antes de la última evaluación, no abandonar Skill/Output necesarios por perseguir puntos directos.

Los márgenes dependen del estado: no copiar una regla universal de bienestar antes que riesgo cuando podría ocurrir una crisis. Hay trabajo previo de cierre (Mecánicas emergentes, B15): usarlo como control, no anunciarlo como descubrimiento nuevo. Medir Q condicionado a completar L6 y gasto monetario evitable. No atribuir toda diferencia de riqueza al sueldo.

## Fase 6 — Selección, integración y prueba de repetibilidad

- Congelar mv-4 y los conjuntos de evaluación antes de seleccionar.
- Primero una modificación por brazo; después sólo combinar las que ganen y estudiar su interacción. El control conserva exactamente el protocolo de llamadas.
- Evaluación emparejada en réplica con semillas nuevas, varias lecturas/modelos de elección y análisis por familias; reportar incertidumbre del modelo además del error Monte Carlo. Unas miles de semillas no crean miles de carreras reales de evidencia.
- Un candidato avanza si sube P(L6 completo) y P(Q≥77,78), sin empeoramiento material de crisis/cola baja; fijar el margen de no inferioridad antes de ver resultados. Ganancia sólo con efectos exactos: pista de investigación, no manual aprobado.
- Las futuras pruebas reales sólo tras autorización y con tamaño definido por la precisión necesaria. Una tanda de tres es una comprobación operativa, no evidencia de constancia. Registrar interrupciones, proveedor cuando esté disponible y todas las partidas, no sólo récords.

Incluso P(Q≥77,78)=80 % por carrera dejaría P(tres de tres)=51,2 %, suponiendo independencia y estabilidad. Con 95 % sería 85,7 %. El objetivo «continuamente» exige reducir colas, no sólo elevar la media; dependencia entre proveedores o tandas puede alterar esa cuenta.

## Orden de trabajo y entrega esperada

1. Tabla de ventanas y continuaciones: localizar dónde se pierde L6.
2. Medir por separado A (Skill/Output), B (salud que habilita crecimiento), C (riesgo que destruye crecimiento). Elegir orden de implementación por pérdida recuperable observada, no por preferencia estética.
3. Banco crítico de lectura si el cuello sigue siendo semántico.
4. Cierre económico y bienestar sólo cuando haya más carreras L6.
5. Integrar como máximo las mejoras con evidencia y proponer una validación futura, sin ejecutarla con DeepSeek.

Entregar: diagnóstico con datos, tabla de resultados positivos/negativos, un candidato mínimo si existe evidencia transferible, límites, validación pendiente y Relevo. Si no emerge mejora, decir qué mecanismo no se pudo trasladar y qué observación lo cambiaría. No concluir «no hay margen» a partir del fracaso de un solo controlador.

## Relevo

Esta sesión sólo preparó el encargo. Comprobados fórmula de puntuación de la réplica y actualización main con Mejora; ninguna simulación, API, modelo externo ni partida nueva. Documento en la línea de apoyo alejandro/gpt-principios, con README y ESTADO actualizados. Solicitar integración documental en main; no se ha enviado a otro chat ni cambiado el manual.
