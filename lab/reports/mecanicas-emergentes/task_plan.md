# Mecánicas emergentes — 27 octubre 2026

Objetivo solicitado: descubrir y comprobar al menos un patrón útil nuevo, partiendo de los últimos experimentos.
Rama propia `alejandro/mecanicas-emergentes`. Base inicial de exploración `4cec65d`; base final de publicación `main-1nddsg@da81e4a` (M1–M23), excluyendo la integración ajena de T20. No editar el plan global.

## Fases
1. [x] Leer ESTADO, H1–H25, M1–M17, T18/T20 y código de la réplica.
2. [x] Formular y probar intervenciones aisladas en la réplica.
3. [x] Confirmar la mejor hipótesis en semillas nuevas y, si procede, bots por las cinco herramientas oficiales.
4. [x] Informe con incertidumbre, artefactos reproducibles y principios generales; tests; commit, push y PR.

## Hipótesis escritas antes de simular
- E1: el planificador premia reducir riesgo incluso cuando ya está en cero. Corregir esa valoración podría liberar decisiones para crecer sin más explosiones (no cambia el motor).
- E2: el cierre desde el mes 46 abandona una evaluación que aún puede dar un ascenso en el mes 48. Mantener la preparación de esa evaluación y cerrar después podría mejorar nivel y nota.
- E3: planificar conjuntamente energía y acción principal evita gastos redundantes y puede usar recuperación/aprendizaje como combinación, en vez de comparar cada acción por separado.
- E4: valorar la habilidad por encima del mínimo antes del ascenso podría acelerar el ascenso siguiente; probar sólo tras evaluar E1–E3.

Exploración: brazos base y cambios aislados; 400 semillas por brazo. Selección por nota media incluyendo derrotas. Confirmación: semillas nuevas, diferencia y IC 95%, sin seleccionar de nuevo. Réplica no equivale a motor oficial: confirmar por MCP la intervención ganadora si muestra valor. No IA ni API de pago. No leer internos del motor.

## Errores y límites
- `/goal` ya había creado el objetivo; no se creó un duplicado.
- Fetch completo devuelve colisión macOS `Matteo`/`matteo/*`. Las ramas de interés sí se actualizaron; no se modifica ninguna referencia ajena.
- El primer estado local estaba >100 commits atrasado; se tomó la rama más reciente que incorpora la réplica, no main antiguo.

## E5, formulada después de screen-03 y antes de screen-04
El recurso escaso puede ser cada plaza de evento. Una continuación consume una plaza que podría producir otro evento: valorar sólo su beneficio bruto puede elegir historias largas con bajo rendimiento por decisión. Prueba: horizonte de cadena 6 con coste de oportunidad por continuación 0/3/6/10 (unidades de la función de valor, NO parámetros del motor). Se compara con base para separar profundidad y coste. No se copiarán respuestas ni catálogo a Skills.

## E6, antes de screen-05
El último trimestre permite recuperar salud/dignidad y reducir riesgo después de los últimos eventos. Ese recurso futuro cambia el coste real de aceptar un coste de salud en el último evento. Comparar base, optimizar sólo trimestre final, optimizar Q inmediata en eventos finales, anticipar trimestre final en eventos finales. Todas las decisiones anteriores al mes 48 permanecen iguales. No cambiar el motor.

## E7, antes de screen-06
`w_skill_hi` sólo multiplica habilidad por ENCIMA del umbral; las búsquedas previas ligaban todos los crecimientos bajo umbral al mismo peso. Probar multiplicadores de valor real de habilidad 2/3/5 desde L4, también bajo umbral, con cierre después de la última evaluación. Comparación con base y late_close. Predicción: mayor frecuencia L7 y ascensos adelantados, aunque podría costar salud/riesgo/dinero. No afirmar que mejora Q si sólo mejora nivel.

## Confirmación oficial fijada antes de lanzar
E6/terminal_q es el candidato: se limita a la última fase trimestral y enumera combinaciones completas. 300 partidas por brazo, asignación aleatoria, 2 procesos × 3 servidores aislados, sin semillas/clones del juego. Primaria: ganancia Q desde la entrada al último trimestre (control variate pretratamiento), entre quienes llegan a ese punto; secundaria Q final sin ajustar de todas las partidas. Todas las decisiones antes de ese punto son idénticas entre brazos; por tanto llegar al último trimestre es selección pretratamiento. Auditar además estados finales predichos frente a los oficiales y contrafactual de cada estado inicial (etiquetado como cálculo de réplica). No ampliar N según significación.
