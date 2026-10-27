# Auditoría de cobertura y entrega

26 de octubre de 2026. Objetivo: profundizar en competiciones pasadas comparables y crear una base de enfoques concretos para probar cuando el laboratorio se estanque. Esta investigación no ejecuta el laboratorio que Claude desarrolla en paralelo.

## Evidencia por requisito

| Requisito | Evidencia inspeccionable | Resultado |
|---|---|---|
| Identificar estrategias ganadoras y distinguir su procedencia | [17 casos](cases.json), campos placing/placing_evidence/source_ids; [35 fuentes](sources.json) | Puestos generales, de categoría, de plataforma y declarados separados. ICFP enumera MOYOU y Unagi; los dos contrastes de podio no se llaman campeones generales. |
| Entrar en detalles de los procedimientos | [Casos desarrollados](cases.md), mecanismo/tradeoff/transfer/boundary; alcance de lectura por fuente | Memoria y preempción; roles persistentes; RL+heurísticas; expertos; CP-SAT; SA/LNS; representación y reparación; validación y rendimiento. Código público seleccionado revisado sin ejecutarlo. |
| Crear una base utilizable cuando haya atasco | [36 fichas JSON](strategy-cards.json) y [legibles](strategy-cards.md) | Cada ficha tiene disparadores, hipótesis, intervención, control, métricas, criterio de revisión, esfuerzo y procedencia. Todas están sin ejecutar. |
| Incluir diversidad y enfoques contraintuitivos | [Guía](playbook.md), tabla de propuestas y combinaciones | 12 fichas contraintuitivas. Incluye restar reglas, concentrar, abandonar objetivos, desarrollar descendientes peores y reconstruir módulos. Ninguna se presenta como ganadora validada del CareerSim. |
| Cubrir comparabilidad, límites y resultados negativos | Cada caso y §§3–6 de la guía | Se separan juegos de acción secuencial y optimización abierta, categorías, objetivos, unidades de simulación y fallos. Un resultado publicado no demuestra causalidad de cada componente. |
| Respetar el juego actual | S33 reconsultada; límites por caso; protocolo común de fichas | Sin motor interno, base de datos, tablas por evento, umbrales ocultos, semillas o clonación asumidos. Revisión de alcance antes de técnicas ambiguas. |
| Permitir consulta por Claude sin interferir | [README](README.md), [handoff](handoff-for-claude.md), registros propios | Nuevos materiales en esta carpeta. No se cambian los archivos del laboratorio ni sus planes, no se le envían mensajes y no se lanzan experimentos. |

## Alcance de la búsqueda

Se conservaron 13 consultas Exa exactas, con 90 posiciones de resultados solicitadas. Esos resultados son descubrimiento, no 90 lecturas completas. El catálogo seleccionado tiene 35 fuentes primarias, algunas ya presentes en la investigación anterior y aquí leídas en mayor detalle. Varias fuentes del mismo equipo no cuentan como corroboraciones independientes.

Las competiciones/ediciones cubiertas son NetHack 2021; Lux S2 original y NeurIPS; Lux S3; Kore 2022; Halite 2020; Halite II; Hungry Geese; RPS; Huawei Ireland 2024; AWTF 2025; AHC058; ICFP 2025 y Flatland 2020. Son 14 grupos de concurso/edición. Es una biblioteca amplia y ampliable, no un censo de todos los concursos históricos.

La página accesible de Huawei Ireland 2025 publica una victoria pero no detalle técnico suficiente: se conserva como contexto sin inventar su pipeline. Las páginas inaccesibles y el origen alternativo usado en Halite están anotados. No se emplean fuentes sobre internos del CareerSim actual.

## Verificación

Pasaron **25 comprobaciones**: JSON parseable; unicidad de IDs/URLs; referencias ficha→caso→fuente; campos obligatorios no vacíos; recuentos; cobertura de los casos; estado no ejecutado; lanzamiento deshabilitado; coherencia entre JSON y Markdown; y espacios finales. Se resolvieron **105 enlaces locales**, incluidos **75 enlaces a anclas explícitas**. El resultado se guarda en [verification.json](verification.json). El diff de publicación se revisa además con Git.

Estas comprobaciones acreditan integridad de la biblioteca, no rendimiento de políticas ni reproducción de los resultados históricos. No se ha realizado una nueva partida, llamada a un modelo actor del laboratorio, envío a organizadores o entrega de competición para este objetivo.

## Publicación y trabajo concurrente

Los cambios propios se limitan a esta carpeta y su commit se inspecciona por rutas. Los archivos y el plan global que Claude edita permanecen fuera del alcance del commit de investigación. La referencia publicada y la rama remota se verifican al terminar; no se usa force push ni se altera Matteo.
