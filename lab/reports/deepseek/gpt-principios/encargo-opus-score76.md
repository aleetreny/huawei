# Encargo acotado para Opus

> **Histórico, sustituido el 30 oct:** usar exclusivamente [encargo-opus-78.md](encargo-opus-78.md). La nueva revisión corrige el objetivo, la prioridad de los casos dominados y el papel de la calidad.

**Objetivo: aumentar la media general hacia 76+, no repetir exactamente 77,78 ni maximizar L6 a costa de derrotas.** Lee ESTADO.md, NORMAS.md, HALLAZGOS.md y lab/reports/deepseek/gpt-principios/decision-opus-score76.md. Ese informe sustituye las prioridades de la hoja de ruta anterior.

Mantén mv-4 como control y congela su bucle de herramientas. No uses DeepSeek, no gastes APIs ni lances partidas oficiales. Trabaja primero con trazas pagadas y réplica. No cambies el manual antes de identificar un mecanismo recuperable.

1. Audita los casos señalados en mv-evidence.json mediante scripts/deepseek/gpt_mv_evidence.py. Prioriza elecciones localmente dominadas, pérdidas N/O cerca de evaluación con alternativa segura y riesgo asumido fuera de esa ventana. Los conjuntos se solapan y sus alternativas pueden tener otros costes. Confirma los casos relevantes en trazas crudas y separa lectura errónea, prioridad mal aplicada, intercambio deliberado y menú sin salida segura. La denuncia anónima del mes 26 de mv-4/3 tenía riesgos +1/+2 y eligió el menor: NO la uses como ejemplo de incumplimiento corregible.
2. Selecciona como máximo DOS mecanismos repetidos en varias carreras/títulos, con mejora potencial en continuaciones coherentes. No sumes efectos locales como puntos de carrera. Una réplica con información privilegiada sólo identifica potencial, no una solución entregable. Produce para el diseñador conclusiones agregadas sin texto ni respuestas de eventos.
3. Propón una corrección mínima por mecanismo. Primera preferencia: una confusión semántica concreta, siguiendo la evidencia positiva de mv-3. Segunda: una ambigüedad de prioridad que las trazas demuestren. No añadir un revisor genérico ni una lista amplia de señales de riesgo.
4. Define pruebas separadas con control repetido, títulos reservados y controles de L1, salud y riesgo. Mide coste de las discrepancias, no sólo acierto o coincidencia. Sin nueva autorización no ejecutes pruebas con DeepSeek; deja explícita la transferencia pendiente.

No reabras planificación trimestral por déficit, penalización general de Health, tolerancia global al riesgo, scripts decisores ni relectura genérica: ya tienen pruebas débiles o negativas. Sólo reconsiderarlos con un mecanismo nuevo identificado y evidencia que explique por qué cambiaría el resultado. No sigas recomendaciones de jueces que alteren el bucle validado.

Entrega una tabla «mecanismo / evidencia / alternativa / ganancia potencial y límites / cambio mínimo / prueba / criterio de abandono». Si no hay dos mecanismos sólidos, entrega uno o ninguno. No fabriques una promesa de 76: con calidad 73 y eficiencia 100 hacen falta 73,375 de media de juego incluyendo derrotas; las seis completas actuales promedian 68,12. Hay que mejorar completas y fallos. Documenta Relevo, actualiza la línea, commit/push y solicita integración según NORMAS.
