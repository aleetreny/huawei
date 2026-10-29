# Auditoría desde principios básicos

**Todavía no se ha demostrado una puntuación de partida de 75 de forma consistente.** Esta investigación apoya la línea DeepSeek y distingue resultados reales, pruebas con otros modelos y simulaciones. No se han realizado nuevas llamadas a la API de DeepSeek.

## Qué se ha aprendido

La partida de 76,87 del equipo es real. La auditoría reprodujo las 750 salidas del asesor, las 747 acciones aceptadas y las cinco memorias finales de sus trazas. La ejecución del programa fue fiel; su familia de estrategias no mantiene esa nota de forma consistente. Estos resultados ya están recogidos en C35 de HALLAZGOS.

Un modelo más capaz tampoco basta por sí solo. La referencia completa con Sonnet y v4 terminó en 49,95, mientras que las tres carreras anteriores con Haiku obtuvieron 66,86, 18,23 y 64,15. No son comparaciones aleatorizadas ni resultados transferibles automáticamente a DeepSeek. HALLAZGOS recoge esta limitación en C36.

Las pruebas de autocomprobación, revisión factual, contexto fresco y predicción numérica no justificaron nuevos candidatos. Sus resultados y limitaciones se describen en [ideas del usuario](user-ideas.md) y en los archivos numéricos correspondientes. Las variantes descartadas no deben volver a presentarse como nuevas.

La memoria de retornos ofrece una señal favorable en la réplica: aprender de consecuencias registradas, después de elegir, mejoró la media en 5,39 puntos en una primera tanda y en 4,30 en otras 600 semillas. Ambas comparaciones mantuvieron el mismo lector y controlador. No se pueden sumar esas diferencias a las notas reales de v4: falta demostrar el transporte y su eficacia con un modelo.

Se encontró también una versión pública de otro participante con una partida de 73,1. Su traza reporta DeepSeek, pero una sola partida no demuestra repetibilidad ni identifica el método privado de los equipos mencionados por Alejandro. Su arquitectura combina memoria desde el registro, control trimestral por código y elección de historias por el modelo. No se han copiado sus reglas numéricas.

## Informes

- [Auditoría de las trazas de DeepSeek](format-trace-audit.md).
- [Capacidad y feedback](capacity-and-learning.md).
- [Ideas del usuario y pruebas de lectura](user-ideas.md).
- [Piloto de carreras con Haiku](native-pilot.md).
- [Reconstrucción de trimestres](native-quarter-replay.md).
- [Auditoría del runtime](runtime-audit.md).
- [Conclusiones y límites metodológicos](findings.md).

Los planes detallados, resultados y comprobaciones de integridad están en los archivos JSON de esta carpeta. Los registros con narrativas y las respuestas originales permanecen en `~/careerlab-data/deepseek/`. Los archivos comprimidos contienen datos numéricos o copias de código, según su tipo; no se incluyen relatos de partidas.

## Relevo

Encargo actualizado: sólo proponer líneas; otro modelo las comprobará. Prioridad: [líneas para el salto](lineas-salto.md). No lanzar más experimentos desde este chat.

29 oct, prueba de representación terminada: 48 lecturas válidas de Sonnet. Comparar alternativas mantiene las pérdidas evitables en 3 de 24, reduce el riesgo positivo de 4 a 2 y las elecciones que agotarían la salud de 1 a 0. No mejora el resultado principal y no se promueve a partidas. El tratamiento mezcla comparación y advertencia contra pistas léxicas; no identifica cuál produjo la diferencia. Resultados en `pairwise-probe-results.json`; análisis reproducible con `uv run python scripts/deepseek/gpt_pairwise_score.py`. Los 313 tests pasaron antes del cierre; desde entonces sólo se añadieron resultados y documentación. La sesión 99501 terminó con código 0. Se solicita integrar este checkpoint. Siguiente paso: completar la descomposición de historial de DeepSeek y buscar intervenciones que aporten información distinta a sus errores compartidos, sin repetir este banco.

29 oct: [diagnóstico de errores compartidos](shared-reading-errors.md). Dos lecturas repiten 192 de los 285 errores iniciales de Output y 151 de los 185 de riesgo positivo. La siguiente prueba debe cambiar la representación de las alternativas y medir valor de carrera. C40 ya está descartado en main. Se solicita integrar este diagnóstico; no hay un candidato nuevo validado.


Se ha integrado main y reescrito la documentación de la PR #23. HALLAZGOS conserva la versión de main, sin duplicar las antiguas filas C24–C31; ESTADO contiene una sola línea de apoyo. La validación completa pasa con 313 tests y un aviso preexistente de Authlib. La revisión de los archivos JSON y comprimidos no encontró narrativas del juego. Se solicita integrar esta PR en main tras su revisión.

La comparación de 48 lecturas de Sonnet ya terminó. Con memoria de retornos, las pérdidas evitables pasaron de 2 a 3 y el riesgo se mantuvo en 2; una señal de agotamiento de salud presente en el control desapareció. Es una comparación de decisiones aisladas, no una mejora de carrera, y no justifica promover el paquete. El resultado está en `return-packet-probe-results.json`. No quedan actores de esta tanda que reanudar.

Tras la limpieza, la siguiente investigación prioritaria es descomponer el crecimiento del historial en las trazas reales de DeepSeek: observaciones, texto del modelo, notas, lecturas del Skill y consultas al registro. Las comprobaciones C39 y C40 son alternativas baratas. Antes de nuevas llamadas, comprobar la cuota y registrar el tamaño de la prueba en ESTADO.

El objetivo de 75 consistente sigue abierto. Esta PR aporta evidencia y herramientas; no entrega todavía una estrategia que lo consiga.
