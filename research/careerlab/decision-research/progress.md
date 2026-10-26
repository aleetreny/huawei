# Progreso

26 oct 2026: leído ESTADO primero, inspeccionados protocolo y método, worktree separado sobre main actualizado. Preparación de auditoría de registros y trazas, sin nuevas partidas ni gasto de API.

Auditoría terminada: 166 terminales Claude canónicas, 99 trazas verificadas, 67 no localizadas en el Mac. Informes JSON con hashes generados; protocolo complementario escrito y Relevo completo. Suite inicial completa: 241 passed en 34,97 s (una advertencia previa de Authlib); dos tests adicionales y validación de identidades/outcome incorporados para la comprobación final.

El plan global y el protocolo congelado no se editaron. La implementación se limita a inventario reproducible y sus salvaguardas: la extracción y los experimentos están definidos como fases pendientes.

Validación final: 243 passed en 31,22 s, una advertencia previa de Authlib; enlaces locales, `py_compile` y `git diff --check` OK. Exports auditados de nuevo con todas las salvaguardas finales, sin cambios en sus conteos ni hashes. Relevo y línea propia de ESTADO terminados. Publicación en la rama y solicitud de integración por PR como cierre de esta fase de diseño/auditoría.

Publicado el commit `5d3cb1d` y abierta [PR #3](https://github.com/aleetreny/huawei/pull/3) a main. Integración pendiente del organizador; fase local de diseño/auditoría terminada. No se ha enviado un mensaje a otro chat ni iniciado la fase experimental.

Inicio ciclo 001: Alejandro pide una primera exploración e infraestructura para continuar en este chat, subiendo conclusiones. Leído ESTADO primero; integrada `origin/main` (`9b8fbe9`) en la rama propia. Se conserva `.serena/` ajena sin incluirla. Los registros nuevos y los digests de Opus se auditarán con procedencia explícita; no se lanzan partidas.

Implementados extractor temporal, ridge con validación anidada por políticas/familias, pipeline de ciclos inmutables y tests de fuga temporal/reserva de confirmación. 23 tests dirigidos pasan. Primera ejecución 001 terminada: 99 trazas, 53 del actor primario; predicción de estados posible, regresión de comportamiento detenida por sólo 20/17 prefijos completos. Corregido después el inventario descriptivo de soporte parcial (sin cambiar modelos), para una ejecución 002 ligada a 001 y sin datos nuevos.

Ciclo 002 revisado: 99 partidas reutilizadas y 0 nuevas; predicciones y episodios idénticos a 001. Añadidos cinco insights con límites y siguientes pruebas, cola MEASURE-01/H-DR-01/H-DR-02 e instrucciones de continuidad por ciclos en este chat. Ambas ejecuciones conservan copias exactas del código verificadas contra sus hashes; los ciclos futuros guardan código/runtime automáticamente y prohíben incluir propósitos reservados aunque se modifique la especificación.

Validación final de esta fase: **255 passed**, 34,03 s, una advertencia previa de Authlib. Verificados hashes de todos los artefactos originales y fuentes archivadas de 001/002, datos numéricos sin notas/razonamientos ni textos de historias, enlaces locales y `git diff --check`. No se han lanzado partidas ni usado APIs de juego. Resultados exploratorios, sin pretensiones de causalidad ni de validación con DeepSeek.
