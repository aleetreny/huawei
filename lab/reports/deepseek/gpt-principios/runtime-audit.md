# Auditoría del runtime

**Hay diferencias de ejecución verificadas, pero ninguna explica todavía el 75 consistente.**

Una traza de DeepSeek terminó viva en el mes 33, en L2, por el límite de continuaciones. Se contaron 42 negativas genéricas en chino. La preferencia de idioma actual no prueba la configuración histórica ni la causa de las negativas. El parche inglés se preparó y probó offline, sin aplicarlo a instancias activas.

El historial crece durante la partida. La ausencia de razonamiento en el transcript no demuestra que esté desactivado: el runner omite esos fragmentos. Los datos de uso disponibles tampoco resuelven el modo efectivo del proveedor.

El inyector público de reasoning_level de Jiuwen no reconoce OpenRouter. Las pruebas sin red lo confirman, pero no determinan todos los parámetros de las solicitudes reales. No se ha verificado una vía entregable para cambiar esfuerzo desde el Skill; no se han modificado paquetes, credenciales ni slots.

La siguiente pregunta prioritaria es descomponer las fichas que deja cada decisión en el historial: observaciones, mensajes del modelo, notas, relecturas y consultas al registro.

## Evidencia y relevo

Los detalles numéricos y criterios se conservan en [reasoning-adapter.json](reasoning-adapter.json) y en los archivos relacionados de esta carpeta. Los originales con narrativas permanecen fuera de Git. El historial de commits conserva las versiones extensas anteriores de este informe.

No repetir las colecciones terminadas ni presentar estos resultados como una solución para 75 consistente. Consultar el [Relevo principal](README.md#relevo) antes de continuar.

## Conteo de herramientas en v4 (29 oct)

Las dos partidas completas de v4 leen `skill_tool` una sola vez y llaman `check_latest_logs` una sola vez cada una. La de 71,67 registra 207 `observe` y 207 `take_action`; la de 70,22, 190 y 204 respectivamente. Se contaron sólo eventos completos, omitiendo las copias `delta` y deduplicando identificadores de llamada. Fuentes: `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-f78c8b88-dff20f-00000-a1/events.jsonl` y la terminada en `00002-a1`.

El contenido de los resultados de `observe` suma 315.191 y 269.248 caracteres; los argumentos de `take_action`, 64.416 y 51.217. Son caracteres de las representaciones registradas, no fichas facturadas ni todo el historial: faltan mensajes visibles del modelo y envoltorios. No convertir estas proporciones en un ahorro de nota. El conteo sí descarta las relecturas de Skill y consultas repetidas al registro como fuente principal del crecimiento en estas dos carreras.
