# Repartos contrafactuales en caminos observados

**Cambiar sólo el reparto lleva un camino de réplica de63,83–64,05 a70,47–70,70/L6, pero no resuelve otro que muere enL1 ni demuestra75.** No convertir estos replays en una nota del modelo.

Se conservan historias y respuestas observadas en cada carrera; los nuevos repartos no ven las historias futuras. Ancla al inicio del mes3 para evitar la excepción de capsstartup, usando sólo el estado público y el historial deOutput de los meses anteriores. El dinero visible define intervalo inicial+0..0,9. Reproducción de las acciones originales antes de interpretar intervenciones: mismo desenlace yQreal dentro de0,5 del intervalo.

- Carrera1: control65,71–65,93 frente a66,86 real: **no pasa fidelidad**; no interpretar sus diferencias como efecto confirmado.
- Carrera2:18,08–18,31 frente a18,23; reproduce el despido. Reparto observado, aprendizaje de main y limpieza conHRalgo preocupado no la rescatan.
- Carrera3:63,83–64,05 frente a64,15; mismo desenlace. El controlador observado existente llega aL6 y70,47–70,70, pero conserva una explosión. Añadir aprendizaje de main no cambia esa nota; actuar conHRmenos preocupado da70,30–70,53 y tampoco evita la explosión.

Ampliaciones explícitamente exploratorias, registradas después del primer replay: usar signosDeepSeek ya guardados para vigilar la propuesta nativa (riesgo conHR>=2), más dominancia estimada descontando ganancias aprendidas como bloqueadas. Sin lecturas nuevas, sin efectos verdaderos para elegir. Se restringe a nodos sin continuaciones en ninguna opción para no invalidar el camino futuro guardado: **esa restricción usa el catálogo y no es entregable**. En el tercer camino cambian1o3elecciones, sin mejora sobre70,47–70,70. No rescatan el segundo. En el primero, que no pasó fidelidad, no atribuir mejoras.

No son muestras independientes, agentes completos ni estimaciones de media. Congelar respuestas futuras del nativo es una intervención artificial; un modelo real cambiaría sus decisiones al cambiar el estado. No confundir alcance de esta prueba con la líneaFormato, que ya probó scripts reales conDeepSeek y plantea un veto híbrido.

## Relevo

Código `scripts/deepseek/gpt_native_replay.py`, resultados y hashes en `native-quarter-replay.json`. No procesos pendientes ni llamadas. Un camino original censurado que se rescate queda sinQsi faltan eventos futuros; no se inventa una carrera completa. Corregida la etiqueta de censura cuando ya había muerte al cambio de mes. Próximo paso: auditar el77real deFormato y los70reales deDeepSeek, incluyendo su formato y fallos. No promover `observable-allocation-v1` por esta pantalla.

## Comprobacion con registros oficiales,28oct
El problema de menus encadenados detectado posteriormente enSonnet motivó reemparejar todas las acciones con los registros publicos propios: `gpt_native_replay_aligned.py`, archivo separado `native-quarter-replay-aligned.json`. Las tres carrerasHaiku requieren cero correcciones; se mantienen los resultados originales y la exclusion de la primera por falta de fidelidad. No se atribuye su desviacion a este parser. No hubo partidas ni llamadas de modelo adicionales.
