# Auditoría del runtime

**Hay diferencias de ejecución verificadas, pero ninguna explica todavía el 75 consistente.**

Una traza de DeepSeek terminó viva en el mes 33, en L2, por el límite de continuaciones. Se contaron 42 negativas genéricas en chino. La preferencia de idioma actual no prueba la configuración histórica ni la causa de las negativas. El parche inglés se preparó y probó offline, sin aplicarlo a instancias activas.

El historial crece durante la partida. La ausencia de razonamiento en el transcript no demuestra que esté desactivado: el runner omite esos fragmentos. Los datos de uso disponibles tampoco resuelven el modo efectivo del proveedor.

El inyector público de reasoning_level de Jiuwen no reconoce OpenRouter. Las pruebas sin red lo confirman, pero no determinan todos los parámetros de las solicitudes reales. No se ha verificado una vía entregable para cambiar esfuerzo desde el Skill; no se han modificado paquetes, credenciales ni slots.

La siguiente pregunta prioritaria es descomponer las fichas que deja cada decisión en el historial: observaciones, mensajes del modelo, notas, relecturas y consultas al registro.

## Evidencia y relevo

Los detalles numéricos y criterios se conservan en [reasoning-adapter.json](reasoning-adapter.json) y en los archivos relacionados de esta carpeta. Los originales con narrativas permanecen fuera de Git. El historial de commits conserva las versiones extensas anteriores de este informe.

No repetir las colecciones terminadas ni presentar estos resultados como una solución para 75 consistente. Consultar el [Relevo principal](README.md#relevo) antes de continuar.
