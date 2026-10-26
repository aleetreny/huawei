# Relevo: checkpoint solicitado por Alejandro por límite de cuota

**Estado: implementación parcial, no lista para integrar ni desplegar.** Base `b288805`, rama `alejandro/laboratorio-adaptativo`. Alejandro pidió guardar inmediatamente el trabajo. Esta nota permite continuar sin depender del chat.

## Implementado en este checkpoint

- `careerlab/decision_guard.py` y cambios en `decisions.py`: separación exploratoria/objetivo, exclusión de confirmación e infraestructura del ranking de desarrollo, validación de entorno y bloque, alarmas de interrupción, sensibilidad de familias y acciones no ejecutables cuando hay bloqueadores. El objetivo usa tokens observados, sin imputar eficiencia si faltan.
- `careerlab/budget.py`: libro de admisión por eventos persistentes, límites de USD 50 y fases, reserva protegida, una partida facturable simultánea, conciliación explícita y bloqueo ante costes desconocidos o superiores a la reserva estimada. **Es admisión por estimación, no un límite duro de facturación por petición.**
- `careerlab/evidence.py`: evidencia portable de salidas, decisiones, evaluaciones, ascensos y observaciones para pruebas de comprensión. Adaptadores para trazas Claude, ejecutor programático y formato del runner oficial leído de su repositorio público. Falta completar su batería de pruebas.
- `store.py`: migración aditiva de evidencia, exportación/importación del registro financiero, evidencia al ingerir y corrección de un fallo previo: los nuevos IDs de trabajos incluyen entorno para evitar colisiones entre celdas. No se reescribe el historial.
- `official_runner.py` y `scheduler.py`: preflight de credenciales sin mostrar valores, partida objetivo secuencial con reserva, no reutilizar un score report anterior, timeout de play, copia de trazas públicas y envoltorio temporal de evaluación. El envoltorio no constituye los documentos finales de entrega.
- `adaptive_cli.py`, `cli.py` y `research.py`: comandos de configuración privada, presupuesto, decisión, evidencia, propuestas, planificación acotada, congelación y confirmación separada. Son piezas iniciales que necesitan revisión y pruebas de integración; no se da por completado el ciclo.
- Nuevas pruebas de guardas y presupuesto, incluidas concurrencia, costes inciertos e importación.

## Validación realizada

- 22 pruebas existentes de core y orígenes pasaron tras los primeros cambios de esquema.
- Primera tanda de pruebas nuevas: 14 pasaron y una descubrió la colisión previa de IDs entre entornos. El ID nuevo se corrigió. Se volvió a lanzar esa tanda antes del checkpoint; consultar el resultado final del proceso o repetir el comando de abajo.
- No se ha pasado aún la suite completa sobre el conjunto final de cambios. No afirmar que esta rama está validada para producción.
- No se han ejecutado partidas ni llamadas de pago. La clave no se ha leído, recibido ni configurado: Alejandro confirmó que todavía no está configurada.

## Karpathy: conclusión crítica y fuentes

Leídos [README](https://github.com/karpathy/autoresearch) y [program.md](https://github.com/karpathy/autoresearch/blob/master/program.md), este último con blob `dea9bcc0174f1502d0ba64000b94b81ba605855b`.

Transferible: evaluador fijo, superficie de cambio pequeña, hipótesis concreta, registro persistente y un programa de investigación legible. Inadecuado para copiar literalmente: conservar una variante por una sola mejora observada, descartar por una ejecución, cortar carreras a un tiempo fijo, resetear Git perdiendo experimentos o mantener un bucle facturable sin presupuesto. El juego es estocástico, de horizonte largo, y cambia de jugador/programa entre proxy y objetivo. No existe una garantía de hallar una estrategia perfecta.

Ambos posts X enlazados devolvieron SOURCE_NOT_AVAILABLE/403. Las cifras atribuidas a esos posts por terceros no se verificaron ni deben presentarse como evidencia primaria. El enlace repetido corresponde al mismo post.

## Relevo

1. **Qué se hizo y por qué.** Se inició la implementación de todas las mejoras del diagnóstico, priorizando guardas, evidencia y crédito finito sobre la estructura existente. Se conserva el plan global y no se modifican las filas del equipo.
2. **Resultados y datos.** Implementación y pruebas en esta rama; 22 pruebas existentes verificadas y primera tanda nueva 14/15 antes del arreglo de entorno. Se guarda el resultado posterior en progress.md cuando termine. No hay resultados de juego ni gasto de DeepSeek.
3. **Trabajo pendiente y riesgos concretos.** Conectar el `--batch-out` al driver cloud y filtrar sus jobs por actor/entorno; añadir pruebas end-to-end de objetivo con actor falso, evidencia portable y planificación. Revisar `research.py`: firmas de helpers estadísticos, idempotencia, fronteras de bloques, congelación y confirmación. Revisar recuperación de cargos empezados y conflictos de importación del ledger. Completar limpieza de procesos/archivos y validación del runner; falta probar credenciales y reportes antiguos. Añadir protocolo operativo versionado y programa de investigación, sin editar v1. Corregir mediante una nota posterior la interpretación de T13, sin reescribir lo predeclarado. No desplegar esta rama parcial.
4. **Siguiente paso concreto.** Continuar en `alejandro/laboratorio-adaptativo`. Leer este informe y `task_plan.md`; ejecutar `uv run pytest tests/test_adaptive_guards.py tests/test_target_budget.py -q`, completar la integración y ejecutar `uv run pytest -q`. Para pruebas usar sólo actores falsos y directorios temporales. La configuración de la clave queda para el runner cloud mediante entrada oculta, nunca pegada en el chat ni guardada en Git. Mantener los límites y conciliación antes de cualquier piloto.
5. **Publicación.** Checkpoint a petición expresa de Alejandro por cuota: commit y push en rama propia, PR en borrador y línea propia actualizada en ESTADO.md. Pedir integración sólo cuando el trabajo pendiente y sus pruebas estén completos.
