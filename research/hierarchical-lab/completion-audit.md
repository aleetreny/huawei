# Auditoría de cobertura de la investigación

26 de octubre de 2026. El objetivo auditado es **investigar y especificar** el laboratorio descrito por el usuario. No incluye ejecutar una flota, demostrar una política ganadora, gastar créditos externos, contactar organizadores ni preparar una entrega oficial. Las condiciones pendientes de ejecución se registran sin convertirlas en conclusiones de rendimiento.

## Cobertura de lo solicitado

| Requisito | Evidencia entregada | Conclusión |
|---|---|---|
| Identificar métodos matemáticos que encajan con el árbol propuesto | [Diseño, §§1–7](design.md); [matemáticas, §§1–5 y 13](mathematics.md); fuentes R01–R04, R19–R22, R36–R38 | MCTS-AHD y AB-MCTS son precedentes directos para búsqueda externa; teoría de optimización jerárquica exige hipótesis que no atribuimos al espacio de prompts. |
| Generalista a específico; presupuesto; beneficios tardíos; recuperación de ramas | [Diseño, §§5–11 y 16](design.md); [matemáticas, §§6, 8–12](mathematics.md); [contraejemplos](counterexamples.json) | Se distinguen réplica, mutación, reapertura y especialización. Dormancia reversible; episodios hasta terminación; comparación de políticas completas. |
| Opus coordinando Haiku y posible Sonnet | [Diseño, §§3, 12–13](design.md); [matemáticas, §7](mathematics.md); [protocolo, §§2–7](protocol.md) | Generación separada de medición, estadísticas por actor, piloto de transferencia y auditoría de descartes sobre el actor objetivo. No se asume fidelidad universal. |
| Reglas y condiciones reales | [Resumen de restricciones](README.md); [protocolo, §§1–4](protocol.md); R49–R54; [preguntas precisadas, no enviadas](../organiser-questions.md) | Runtime oficial de un agente y modelo designado. El laboratorio externo requiere aclaración específica antes de ejecutarse; no es una excepción ya aprobada. Nombres/precios verificados en páginas individuales, acceso por clave sin probar. |
| SOTA, referentes fuertes y muchas referencias | [Bibliografía anotada](bibliography.md), [55 registros con metadatos](references.json), [BibTeX](references.bib), [registro de descubrimiento](search-audit.json); [diseño, §§14–15](design.md) | Selección de fuentes primarias, con alcance de lectura por entrada. Incluye métodos recientes de 2026 y relatos de autores sobre competiciones; resultados ajenos no se atribuyen a CareerSim. |
| Guardar todo lo necesario para continuar desde el repositorio | [Protocolo, §§7–9](protocol.md), [contrato de cinco tipos de registro](records.schema.json), [especificación](lab-spec.json) | Artefactos inmutables, linaje con varios padres, resultados identificados, tareas con propietario, evidencia portable y verificación de procesos al reanudar. Es un contrato propuesto, sin lanzador implementado. |
| Ingeniosidad defendible y presentación | [Protocolo, §§10–13](protocol.md); [diseño, §§14–16](design.md) | Baselines de búsqueda, presupuestos comparables y ablaciones por componente; unidad de réplica externa definida. Aportación propia como adaptación y evidencia, sin atribuir novedad a mecanismos existentes ni inventar una subpuntuación de novedad. |
| Revisión final y entrega | Este documento; [notas](findings.md); comprobaciones abajo; navegación desde el README raíz | Paquete autocontenido de investigación. La propuesta retirada de dos Skills no se recrea. La publicación Git se verifica al finalizar. |

## Alcance verificable de las fuentes

- 23 búsquedas Exa en este objetivo: 185 posiciones de resultados solicitadas, 185 entradas exportadas, 184 URLs distintas de candidatos. No equivalen a 185 fuentes leídas o aceptadas.
- 55 fuentes primarias seleccionadas y deduplicadas, cada una con título, autores, URL, alcance, utilidad y límite. Documentación de competición y productos está incluida en ese total.
- Seis consultas de metadatos arXiv con sus parámetros exactos; 40 entradas recibidas, con repeticiones. Los originales quedan en `local-runs/literature/`, excluido de Git. El catálogo conserva la procedencia necesaria para consultar de nuevo.
- Los textos exactos de las consultas Exa no se conservaron en el export; sí temas, candidatos y URLs. Esto limita la reproducción exacta del descubrimiento, no se oculta como una búsqueda plenamente reproducible.
- Se corrigió una identificación errónea de FunSearch antes de incorporarla. Se siguió el título actualizado de Meta-TTL y se distinguieron publicaciones de conferencia, preprints y documentación. Ningún metadato arXiv seleccionado tiene fecha posterior al corte.
- R55 documenta el uso material de la herramienta **paper-lookup** y su artículo de procedencia. No se usa como prueba de que una estrategia sea eficaz.

## Comprobaciones realizadas

Se ejecutaron 24 comprobaciones del paquete: validez del esquema Draft 2020-12; aceptación de los cinco tipos de registro; estados incompletos sin nota terminal; rechazo de puntuación sin final real, notas fuera de rango, hashes mal formados, ausencia de evidencia terminal, campos inesperados y fecha inválida; lanzamiento deshabilitado; aritmética de contraejemplos y precios ilustrativos; pesos efectivos oficiales; presupuesto de error sumable; identidad, fechas y correspondencia entre catálogo, bibliografía y 55 entradas BibTeX; recuentos de búsqueda.

La comprobación de fechas usó un validador ISO explícito porque el entorno no incluye el comprobador opcional RFC 3339 de jsonschema. No es una prueba exhaustiva de conformidad RFC. El esquema valida formas, no integridad entre registros ni vida de procesos: esas obligaciones se especifican para la futura implementación.

También se revisan enlaces locales de Markdown y `git diff --check` antes de publicar. No son pruebas de rendimiento del juego. Los registros sintéticos utilizados para validar el contrato no se introducen en el registro de experimentos reales.

En la comprobación remota se detectó un nuevo commit del compañero, `27cd3c1`. Se revisaron sus ocho archivos de cambio y se añadió el resultado a [la auditoría de Matteo](../matteo-branch-review.md): candidato de tres Skills y plan de 100 partidas todavía sin ejecutar, sin nuevo benchmark. La rama del compañero se conserva y no se importa su solución como arquitectura elegida.

## Lo que queda para una futura ejecución

1. Aclaración escrita que cubra exactamente automatización, actores externos y concurrencia, además del límite de gasto autorizado por el equipo.
2. Acceso real a modelos, aislamiento por opciones oficiales y huella de la configuración objetivo.
3. Implementación del worker, planificador e integrador; medición de coste real por episodio.
4. Piloto de fidelidad y después búsqueda, confirmación y ablaciones.

Son prerrequisitos de implementación, **no trabajo de investigación omitido**. Este paquete no afirma haberlos resuelto ni que su combinación sea matemáticamente óptima. No se han hecho llamadas a los modelos externos ni nuevos lotes de juego para validar esta especificación.
