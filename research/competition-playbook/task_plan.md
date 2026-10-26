# Plan — biblioteca de enfoques de competiciones

Objetivo: profundizar en soluciones ganadoras de competiciones comparables y convertir sus mecanismos en una base utilizable de experimentos para cuando el laboratorio de Career Survival se estanque. Investigación separada de la implementación concurrente de Claude.

## Requisitos y evidencia de cierre
1. [complete] Buscar y verificar casos: distinguir resultado oficial, puesto declarado por autores y mera referencia exploratoria.
2. [complete] Leer en detalle métodos y código público pertinente; documentar por qué funcionaron y sus límites.
3. [complete] Cubrir decisiones a largo plazo, recursos/riesgo, exploración/búsqueda, híbridos, adaptación y validación; buscar contradicciones y casos negativos.
4. [complete] Crear fichas accionables con disparador de atasco, hipótesis, intervención, comparador, medición y decisión posterior.
5. [complete] Mapear cada ficha a fuentes verificadas, separar adaptación propia de resultado publicado y definir combinaciones útiles.
6. [complete] Revisar reglas vigentes y compatibilidad; evitar importar acceso al motor, respuestas memorizadas o capacidades ausentes del MCP.
7. [complete] Entregar catálogo legible y estructurado, navegación para Claude, auditoría de cobertura y publicación sin interferir con su trabajo. Verificados 25 controles y 105 enlaces; el commit y la referencia remota se inspeccionan antes de la respuesta final.

## Alcance
- Fecha de corte: 26 de octubre de 2026; sólo competiciones ya celebradas antes del corte.
- Fuentes primarias: autores, repositorios de sus soluciones y organizadores. Los puestos sin corroboración oficial se etiquetan.
- Priorizar analogías sustantivas sobre coincidencia de marca Huawei. No afirmar una genealogía de campeones del CareerSim actual sin evidencia.
- No ejecutar partidas, gastar créditos de modelos ni enviar mensajes a Claude/organizadores durante esta investigación.
- Mantener archivos nuevos en esta carpeta y comprobar el estado compartido antes de modificar navegación o hacer commits.

## Errores y correcciones
- Un nombre supuesto de referencia de la skill Exa no existía. Se consultó el índice real de referencias y se continuó con searching/source-quality/synthesis.
- Exa agrupaba varios resultados en un bloque: corregido el parser y conservados los 90 candidatos de 13 consultas.
- Hilo Kaggle Halite con error de carga y URL supuesta inexistente: se recurrió al repositorio original y código seleccionado, sin fingir lectura del writeup.
- Listado recursivo de GitHub demasiado extenso en la salida: se filtraron rutas y metadatos antes de imprimir en las consultas siguientes; no se descargaron los datos enumerados.
- Git diff --check detectó una línea vacía extra al final de tres Markdown generados. Se normalizó el final de archivo antes del commit; no se ejecutó ningún commit fallido.
