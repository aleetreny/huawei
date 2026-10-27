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

## Ciclo 001: extracción temporal

- Snapshot nuevo integrado: main `9b8fbe9`, 360 evaluaciones. Se ha congelado `exploration-v1.json` antes de ajustar modelos.
- Comprobación técnica en la partida de humo: 197 acciones pero sólo 178 observaciones; 20 acciones no tienen una observación nueva anterior. La respuesta de take_action sólo devuelve success/error. Reutilizar el estado de la acción anterior daría un estado obsoleto.
- Adaptación antes de mirar asociaciones: evaluar estados frescos en cada landmark; modelar comportamientos sólo si todo el prefijo anterior está alineado. No descartar una observación temprana porque falten estados más tarde. Reportar tamaños por modelo y no comparar errores obtenidos sobre cohortes diferentes como si fueran una mejora incremental.
- Los scripts de digests anteriores conservan la última observación tras take_action. Sus resúmenes siguen siendo diagnósticos útiles, pero no se usarán como tabla temporal verificada para regresión de decisiones.
- Consultada documentación oficial de scikit-learn sobre separación de grupos, validación anidada y preprocessing dentro del entrenamiento; la implementación usa álgebra de ridge con NumPy ya presente, sin nuevas dependencias.

## Primera ejecución exploratoria (001)

- 204 terminales Claude elegibles del snapshot actual; 99 trazas locales extraídas, 105 no localizadas aquí. Actor primario: 53 trazas de 129 partidas terminales. Son una muestra histórica local, no todas las partidas de ese actor.
- En el mes 6: promovidos 26 (Q media 55,41; 18 completan) frente a 27 aún L1 (Q 35,90; 10 completan). En el mes 12: promovidos 38 (Q 53,07; 26 completan) frente a 14 aún L1 (Q 26,24; 2 completan). Asociación condicional, no efecto de promover.
- Ridge de cinco estados tempranos, validación anidada por familias: RMSE 16,04 frente a 18,46 de la media al mes 6; 14,94 frente a 18,37 al mes 12. Error residual importante; no es un selector validado ni una política.
- Sólo 20 prefijos de comportamiento completos al mes 6 y 17 al mes 12. La regla de mínimo 30 impide ajustar esos modelos; no se bajó el mínimo tras ver el resultado.
- Entre 28 carreras completadas del actor primario, nivel pierde 16,18 puntos Q y riqueza 13,28. La salud/dignidad pierde 0,21, pero esto es una contabilidad entre supervivientes y no implica que podamos dejar de protegerlas.
- 1177 de 4701 transiciones de historia alineadas dentro del mismo mes pierden Output o Network. Son cambios hasta la próxima observación, no efectos aislados ni 4701 réplicas independientes.
- Revisión de la salida 001: el inventario de soporte de variables de comportamiento contaba también valores parciales, aunque los modelos sí excluían correctamente esos prefijos. Se conserva 001 y se corrige el inventario en una segunda ejecución 002, con linaje que declara cero partidas nuevas. Las predicciones y conclusiones no cambian.
