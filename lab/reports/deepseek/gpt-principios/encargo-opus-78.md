# Encargo vigente para Opus — 30 octubre

> **Para el Opus que ya está trabajando:** esta es una revisión externa para contrastar con tu investigación actual. Valora qué ideas aportan algo, cuáles ya has probado y cuáles descartas. No reinicies ni sustituyas tu plan por este documento. La sustitución de encargos mencionada abajo se refiere sólo a las propuestas anteriores de esta auditoría.


**Investiga una mejora verificable de mv-4 hacia carreras de 72+ frecuentes y nota automática 78; no prometas una solución ni escribas otra versión sin justificar su ganancia. Este encargo sustituye los anteriores de L6 y de 76.**

Lee ESTADO.md, NORMAS.md y HALLAZGOS.md; después `lab/reports/deepseek/gpt-principios/revision-opus-78.md`, que corrige las propuestas anteriores y contiene la evidencia. No uses DeepSeek, APIs de pago ni partidas oficiales. Usa archivos guardados y cálculo local. Conserva el protocolo operativo de mv-4. No pases texto ni respuestas de eventos al diseñador: entrega mecanismos agregados.

**Objetivo.** A = 0,8·juego + 0,1·calidad + 0,1·eficiencia. Con eficiencia 100, calidad 80 exige juego medio 75; calidad 90 exige 73,75. El 72 frecuente es un hito intermedio. Mide todas las carreras, completas bajas, derrotas e interrupciones; además de la media, informa P(Q≥72). L6 es diagnóstico, no objetivo único. No atribuyas calidad oficial a los jueces sustitutos.

**Primero entrega un mapa de pérdidas por evaluación.** Reconstruye desde trazas crudas cuándo faltó Skill/Network/Output y qué decisiones crearon el déficit; el CSV es preacción y no contiene todo el trimestre. Separa lectura errónea, prioridad, intercambio forzoso y crecimiento insuficiente. Los 16 casos dominados son controles auxiliares: siete repiten el mismo nodo y ya reducen riesgo. No trates sus ventajas locales como puntos finales.

**Investiga en este orden:**
1. Costes de tiempo, crédito y relaciones mal interpretados cerca de evaluación, y falsas alarmas de riesgo que descartan alternativas válidas. Empieza en L1 y comprueba también L2/L3. La protección ya está escrita: repetirla no es una hipótesis nueva.
2. Riesgo añadido sin beneficio suficiente antes de HR adverso, más comparación de gravedad cuando todas las opciones son malas. Valora crecimiento, recuperación y ventanas conjuntamente. No endurezcas ni relajes globalmente el riesgo. La denuncia anónima del mes 26 eligió +1 frente a +2: no es el fallo demostrado.
3. En variante separada, claridad y calidad del Skill manteniendo el protocolo. Eficiencia 100 se satura a 500.000 tokens/mes: busca margen y ausencia de reanudaciones, sin añadir otra llamada de reflexión.

Antes de redactar, estima el potencial de cada mecanismo con continuaciones coherentes. Distingue referencia con información perfecta de una corrección que el agente pueda ejecutar con información permitida. Los modelos antiguos aciertan ~87 % en mv, menos en grupos críticos; eso no valida causalmente una nueva frase. No sumes ganancias de intervenciones solapadas.

Una modificación por candidato, máximo dos candidatos estratégicos activos. Prueba reservada por historias completas, control repetido, controles de riesgo/salud/crecimiento y coste de las discrepancias ponderado por frecuencia natural. No reutilices como reservado el banco que eligió al ganador. Una mejora aislada debe sobrevivir al contexto de partida y al historial largo. Define criterio de abandono antes de comparar.

No reabras trimestre por déficit, salud genérica, revisor, memoria o cierre como gran apuesta sin explicar qué mecanismo nuevo cambia la evidencia negativa previa. Si no aparece una mejora transferible suficiente, cuantifica la brecha y detente; no maquilles el resultado.

Entrega una tabla **pérdida / mecanismo / potencial y límites / cambio mínimo / prueba / abandono**, un candidato sólo si se justifica y un plan de confirmación pendiente. Tres carreras buenas no prueban consistencia. Documenta Relevo, ESTADO, commit/push y solicita integración según NORMAS.
