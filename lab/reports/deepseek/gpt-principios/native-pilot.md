# Criterio profesional en carreras completas

**El control native-craft-v1 no alcanza75: tres carreras Haiku dan66,86 ·18,23 ·64,15, media49,75; completar dos carreras tampoco basta (media65,51 entre completadas).** No promover este control ni repetirlo sin una intervención concreta.

Plan original:4 carreras independientes, secuenciales, actor congelado Haiku/CLI2.1.303/entrega `official` emulada, con las cinco herramientas oficiales del juego y `skill_tool`. Se anunció antes enESTADO. Se escogió como caracterización end-to-end después de92 decisiones válidas del banco, no como mejora demostrada contra un control contemporáneo. Sin nuevas llamadas DeepSeek. Entorno: engine1.0.6, dataset1.0.8, competición, env oficial. Cada partida tiene servidor y datos propios; no toca la cola/registro compartidos ni un slotDeepSeek.

| Carrera | Q real | Meses | Final | Acciones / rechazadas | Explosiones observadas |
|---|---:|---:|---|---:|---|
|1|66,86|48|L5, completa|198/0|ninguna|
|2|18,23|24|L1, despido|97/0|mes17|
|3|64,15|48|L5, completa|197/0|mes36|

**Cambio posterior del plan:** tras las primeras dos notas se canceló la cuarta antes de toda llamada, dejando acabar la tercera ya iniciada. Incluso100/100 en las dos restantes habrían dejado la media realizada de4 en71,27. Es una decisión operativa posthoc, no una regla preregistrada ni un límite de la media poblacional. Se conservan el plan original y `native-pilot-futility.json`; ninguna derrota se sustituye ni se corta para subir la media. El padre terminó con exit1 al encontrar el directorio de cancelación: esa guardia impidió arrancar la cuarta. Las tres carreras ejecutadas tienen resultados terminales válidos; no hay una cuarta interrumpida que deba puntuarse cero.

## Qué cambió nuestra interpretación

- La primera mantiene salud y dignidad máximas al terminar, pero llega aL5 sólo en la última evaluación. No basta con ser prudente y profesional.
- La segunda teníaNetwork3 en el panel anterior a la última elección del mes5; esa elección lo deja en2. Reconstruir el estado después de la respuesta, antes de evaluar, evita atribuir preparación al panel equivocado. Las siguientes evaluaciones también mezclan pérdidas deOutput y deterioro por riesgo: no todo se explica por una sola variable.
- En la tercera el control mejora las primeras promociones pero pierde Skill para la evaluación intermedia y luego una explosión cuesta calidad final. Termina conSkill127, Network48 y una penalización de riesgo acumulada; el bucle necesita progreso y fiabilidad.
- Hay inversiones con coste y sin mejora visible. La auditoría sólo las cuenta cuando una acción queda aislada entre paneles del mismo mes/nivel; excluye limpieza de riesgo y reserva, cuyos retornos no son puramente visibles. En la tercera se agrupan varias acciones de energía sin observar entre ellas, por lo que esas transiciones no se pueden atribuir individualmente; ausencia de conteo no significa ausencia de pérdidas.
- El banco sólo incluía48 títulos. En la primera,30/144 respuestas reconocidas coinciden con sus nodos y26/30 eligen una opción ya elegida en algún contexto del banco. Catorce de sus16 riesgos positivos están fuera de ese solapamiento. La diferencia de tasa bruta no prueba deterioro por contexto largo.

El diagnóstico de contexto separado (`context-audit.json`) usa un heurístico privilegiado, sin continuación y con riesgo actual fijado0. En34pares del mismo nodo, el nativo cambia2 veces; en6pares los óptimos heurísticos son disjuntos y no cambia. No es regret deQ ni prueba de que el heurístico sea correcto.

## Límite de la emulación, actualizado28oct

La línea Formato verificó después que JiuwenSwarm oficial expone52herramientas, incluidas `bash` y `code`, y puede ejecutar scripts entregados con el Skill. Este actorHaiku restringido no reproduce esa capacidad ni el mensaje de sistema completo deJiuwenSwarm. Sus resultados caracterizan la decisión con este manual y actor; no son una cota de DeepSeek ni del formato oficial. Consultar el informe actualizado deFormato antes de diseñar otra prueba. No repetir el veto híbrido como si fuera una idea inédita: esa línea ya lo propone.

## Datos, verificación y Relevo

Datos narrativos sólo en `~/careerlab-data/deepseek/gpt-native-pilot/game-{1,2,3}/`: streams, resultado, logs del jugador obtenidos mediante la herramienta oficial. Metadatos, hashes, plan, cancelación y filas numéricas comprimidas en esta carpeta. Cuota compartida observada5h11→14%, semana38→38%; no atribuir exactamente el consumo redondeado a esta línea. Guardas0,65/0,45; secuencial, máximo4procesos compartidos; no se activaron sobrecostes ni APIdeDeepSeek.

Para analizar sin modelos: `uv run python scripts/deepseek/gpt_native_trace.py` y `uv run python scripts/deepseek/gpt_native_replay.py`. `gpt_native_logs.py` sólo consulta logs de nuestras partidas terminadas. **No ejecutar `gpt_native_pilot.py --run` para retomar:** las tres terminaron y la cuarta está cancelada. El modo sin `--run` sólo inspecciona. El prototipo `observable-allocation-v1` pasa lint pero no está validado ni admitido a carreras; no sustituye la entrega.

Siguiente: partir de las trazasDeepSeek nuevas70–77 y del conocimiento real delruntime, no seguir variando este control que ya falló. Objetivo75estable sigue abierto.
