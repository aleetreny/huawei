# Dos lecturas, preguntas objetivas y formato

**Omitir la narración empeora; la revisión factual no añade mejoras, y el contexto fresco conserva los mismos errores reales.** Estas tres pruebas no admiten un candidato ni acreditan75consistente.

Alejandro propone dos turnos de pensamiento en decisiones críticas, preguntas objetivas simples para categorizar y variaciones de idioma/formato. Se revisa lo ya probado antes de decidir nuevas llamadas. No se ejecutan partidas nuevas niDeepSeek.

## Qué se había probado

- Autocomprobación en la misma respuesta:92contextos, formato obedecido pero peores elecciones (C21). No equivale a dos lecturas con contexto separado.
- `perceive-f1`:17códigos de indicios sí/no, incluidos ocultación, arreglos privados, trabajo desviado y relaciones. ConDeepSeek: riesgo90%frente88%de v3;Skilligual, otrosindicadorespeor. No volver a presentar esa lista como nueva.
- Runtime con `preferred_language:zh` y42negativas chinas en una traza: discrepancia verificada, causalidad no demostrada. Parcheinglés preparado, sin aplicar a slots activos ni llamar aDeepSeek. El idioma y formato no están descartados en general.

## Ablación de narración:64decisionesHaiku

Mismo v4 y estado/opciones/avisos públicos. Sólo se sustituyen título y descripción en un brazo. Datos congelados sin etiquetas verdaderas:32contextosL1,16antesdeevaluación, **31menús distintos**. Un menú reaparece en dos estados diferentes; no son32observaciones independientes de contenido. Orden de brazos alternado; narración retirada no reaparece en otro campo. No se dan registros previos a ninguno.

| Medida | Completo | Sólo opciones y estado |
|---|---:|---:|
| Riesgo positivo elegido |1|3|
| Pérdida de crecimiento |8|10|
| Pérdida evitable antes de evaluación |0|3|
| Riesgo positivo evitable |0|1|

26/32elecciones iguales.64/64lecturas válidas conSkill, cero errores/rechazos;Haiku5.5. Comprobaciones de salud/dignidad/dinero inmediato sin señales en ambosbrazos. La regla de admisión bloquea por mayor riesgo: **no llevar este cambio a carreras**. No demuestra que todo cambio de formato sea malo.

Se detectó un error de cache antes de interpretar resultados: la carpeta estaba identificada sólo por menú, aunque el estado también cambia.62lecturas realizadas; un segundo contexto se había omitido por colisión deID. Se conservan todas las respuestas, se verifica cada panel realmente servido y se hacen únicamente las2lecturas faltantes, manteniendo los32contextos y64lecturas máximas originales. La puntuación exige coincidencia exacta del panel. Planoriginal y corrección de identidad separados (`narrative-ablation-context-binding.json`), sin ocultar ni sustituir decisiones.

## Segunda lectura independiente con evidencia:16críticos

Se reutilizan las16primeras lecturas completas antes de evaluación, sin elegirlas por rendimiento. El crítico no ve la primera elección ni sus notas. Recibe el panel completo y v4enlínea, responde sobre desvío de trabajo, ruptura de relación, problema sin resolver y pago personal. Para `yes`, exige una cita literal de la acción; en otro caso permite `no/unclear`. La cita prueba presencia literal, no que la interpretación sea correcta ni que el juego cambie ese indicador.

Regla de combinación fijada: conservar la primera elección salvo coste explícito en ella y una recomendación alternativa sin ninguno de esos costes ni incertidumbre; el pago sólo limita si el dinero mostrado es no positivo. No se acepta un desacuerdo como mejora automática.

15/16respuestas con evidencia literal válida,41señales `yes` válidas. Una respuesta con cita no literal se conserva y no puede modificar la primera elección. Tras detenerse elrunner, se documentó antes de las13lecturas restantes una enmienda operativa: continuar sin reparar/repetir el caso y usar la primera elección como fallback. Misma selección/prompt,16lecturas totales; no describir esa enmienda como preregistrooriginal.

| Medida | Primera | Recomendación independiente | Regla de dos lecturas |
|---|---:|---:|---:|
| Riesgo positivo |0|1|0|
| Pérdida de crecimiento |2|3|2|
| Pérdida evitable antes de evaluación |0|1|0|

Sólo1/16desacuerdos, cero cambios por la regla. No hay mejora que justifique carreras. **La primera lectura ya tenía0pérdidas evitables:** este resultado tiene poco alcance para descartar rescate de errores reales. Seis comprobaciones sintéticas verifican que `unclear` no autoriza sustitución y que el guardia de pago depende del saldo mostrado.

## Pensamiento con contexto fresco:terminado

Todos los24turnos de historia inmediatamente anteriores a una evaluación en la carreraSonnet-v4ya completada. Mismo modeloSonnet5.5, Skill y systempromptoriginal exactos. Relectura con panel original y las3últimas notas de acciones previas aceptadas; no recibe la elección/notas del turno objetivo ni futuro. Control: elección real original en contexto completo. Se incluyen decisiones correctas e incorrectas, sin seleccionar porgold.

Es un diagnóstico histórico de contexto con n1carrera fuente, no un ensayo aleatorizado de carreras. No elimina toda variación entre muestras de un modelo. Se compararán riesgo, pérdidas evitables y recursos; no se convertirá una corrección local enQ.24relecturasMax máximo, sin partidas nuevas/DeepSeek, guardas0,65/0,45 y4procesos.

24/24lecturas válidas conSkill, modeloSonnet5.5y systempromptoriginal exactos. Coinciden22/24elecciones; las dos diferencias no alteran ninguna medida de perjuicio. Carrera original y relectura: riesgo3→3, pérdidas9→9, evitablesantesdeevaluación2→2. Persisten exactamente las dos pérdidas evitables del control. No hay señal de rescate que justifique carreras. Esto no demuestra que toda gestión de contexto sea inútil: controla un paquete específico de panel+3notas frente a la historia de una sola carrera, con muestras no aleatorizadas.

La constatación de errores compartidos orienta una prueba distinta: si se retoma la revisión factual, aplicarla a todos los turnos críticos de la carrera real, con la misma tarea y sin seleccionar únicamente errores. El primer banco factual tenía0errores evitables; no permite medir rescate de fallos presentes. No modificar preguntas por los relatos concretos ni introducir reglas privadas.

## Relevo

Completadas y no repetir:64lecturas de ablación,16críticas y24decontextofresco. Todos los procesos terminaron; no quedan actores que reanudar. Análisis sin llamadas: `uv run python scripts/deepseek/gpt_narrative_score.py`, `gpt_fact_second_score.py` y `gpt_fresh_context_score.py`.

Datos privados: `~/careerlab-data/deepseek/gpt-narrative-ablation/`, `gpt-fact-second-read/`, `gpt-fresh-context/`. Narrativas/citas no van aGit. Scripts compilados y controles de identidad/panel/evidencia pasan. Cuota compartida al cierre:5h4%, semana40%, redondeada; no atribuir consumo individual. Objetivo75repetible abierto. Evidencia actual no justifica nuevoSkill ni cambio de entrega.

## Contraste factual sobre la carrera real: cerrado

**La revision factual no rescata los errores y añade riesgo; no admitir a carreras.** Todos24turnoscriticos de la carreraSonnet, mismo lector factual/gate, modeloSonnet5.5.24/24respuestas con evidencia literal valida,38flagsyes,7desacuerdos. Gatecambia2elecciones: riesgo3→4, perdidas9→9, evitables2→2. Recomendacion sin gate: riesgo4, perdidas10, evitables3 yunaopcionagotaHealth. Cita literal no prueba efecto deljuego. Comparacionhistorica de n1carrera, sinQni transferenciaDS.

### Relevo
Proceso95901terminadoexit0; no reiniciar. Analisis sin llamadas: `uv run python scripts/deepseek/gpt_fact_career_score.py`. Datos privados gpt-fact-career-read/, resultados numericos fact-career-results.json. No hubo juegosnuevos/DeepSeek. No seguir afinando esta variante por historias concretas: el requisito de evidencia se cumple pero la inferencia de efectos siguefallando. Objetivo75abierto; esta prueba no lo resuelve.
