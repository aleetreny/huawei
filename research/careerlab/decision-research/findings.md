# Hallazgos

- ESTADO remoto (16:55 UTC) ya tiene 150 partidas de IA; líder provisional F7, posterior 55,2. Los números de la respuesta anterior describían un snapshot anterior.
- El protocolo v1 exige células por política, actor, entorno y época; incluye Y, datos completos, exclusión de interrupciones y confirmación fresca.
- §10 ya contempla ensayos de cambio de modo, controles always/never y microaleatorización. Esta línea debe aportar extracción, hipótesis y ensayos ejecutables, evitando duplicarlo o sustituirlo.
- Los exports guardan resultados terminales y rutas/hashes de trayectorias. Hay que comprobar cobertura antes de ajustar regresiones de decisiones.

## Auditoría ejecutada

- 322 evaluaciones canónicas: 316 terminales, 6 interrumpidas. Terminales: 150 bots, 166 Claude (80 completadas y 86 eliminadas entre Claude).
- En el Mac: 99 trazas Claude con hash primario verificado (48 completadas, 51 eliminadas), 67 ausentes (32 completadas, 35 eliminadas). Todas las 99 verificadas contienen observaciones oficiales; ninguna requiere continuación en este snapshot.
- Export sin `epoch`, `block_id`, `analysis_role`, `assignment_probability` explícitos en 383 jobs; no se infieren. Hay 61 jobs sin evaluación (22 interrumpidos, 16 leased, 15 queued, 8 running).
- La auditoría separada de Leah contiene una partida terminal y seis interrupciones. No se mezclan con la muestra canónica ni se comprueba su traza sin un mapeo de rutas explícito.
- Documentado un protocolo complementario con extracción temporal pendiente, regresión predictiva agrupada y ensayo aleatorio de reglas, más confirmación según v1.

## Fuentes consultadas

- Capítulo 19 de *Regression and Other Stories* (página de Cambridge): diferencias entre comparación predictiva y causal, ensayos aleatorios y ajuste previo al tratamiento.
- Página de Miguel Hernán en Harvard: confusión temporal afectada por tratamientos previos y límites de regresión convencional.
- Vignette oficial de MRTAnalysis en CRAN: probabilidades conocidas y disponibilidad anterior a la asignación en microaleatorización.
