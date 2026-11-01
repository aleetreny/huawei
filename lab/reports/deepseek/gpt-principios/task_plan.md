# Plan de trabajo

**Primero se limpia la PR #23; el objetivo de 75 consistente continúa abierto.**

1. Integrar main y conservar su versión de HALLAZGOS si hay conflicto. No duplicar las filas ya renumeradas.
2. Revisar la redacción de los informes y dejar una sola línea de apoyo a DeepSeek en ESTADO.
3. Comprobar que los cambios no incluyen narrativas del juego, secretos ni trabajo ajeno.
4. Revisar el diff, pasar los tests, actualizar la descripción en español y sacar la PR de borrador.
5. Comparación de Sonnet terminada, sin repetir ni reemplazar respuestas; no se promueve el paquete.
6. Investigar la composición del crecimiento del historial en las trazas reales de DeepSeek; considerar después las comprobaciones C39 y C40.

## Restricciones

No realizar nuevas llamadas a DeepSeek. Priorizar Sonnet como modelo de aproximación, sin dar por probada su equivalencia. No leer archivos internos del motor ni trasladar fórmulas, umbrales o respuestas concretas a los Skills. Las narrativas se conservan fuera de Git.

## Relevo

La comparación de memoria terminó y no justifica promover el paquete. Consultar el resultado y el Relevo principal antes de nuevas pruebas. Los planes y datos numéricos de los experimentos anteriores permanecen disponibles para reproducir el análisis; no se modifican para cambiar retrospectivamente sus criterios.
