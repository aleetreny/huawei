# Investigación del laboratorio jerárquico de estrategias

Fecha de corte: **26 de octubre de 2026**. Este paquete desarrolla el enfoque solicitado: Claude Opus 5.5 como orquestador de investigación, trabajadores Haiku 5.5 o Sonnet 5.5 que prueban políticas, exploración generalista que se especializa, archivo de ramas y reapertura. **Es una especificación basada en investigación, no un sistema ejecutado ni una estrategia ganadora demostrada.** No recrea la propuesta retirada de dos Skills.

## Recomendación

Construiría un árbol de **versiones de políticas**, acompañado de un archivo de comportamientos diversos y una matriz de resultados por modelo. Usaría un enfoque inspirado en MCTS-AHD/AB-MCTS para decidir dónde generar variantes, comparaciones secuenciales para decidir qué política necesita más partidas y validación en el modelo oficial para aceptar mejoras. El orquestador debe poder elegir entre generar, refinar, repetir, especializar, reabrir y validar; no limitarse a lanzar otro trabajador.

El árbol representa decisiones de investigación. No representa copias del estado del juego. Cada evaluación ordinaria empieza una partida nueva y avanza por la interfaz oficial; volver a una política guardada no devuelve el simulador al mes 8 de una partida anterior.

Documentos del paquete:

- [Informe y diseño del procedimiento](design.md): por qué esta combinación encaja con la propuesta y qué decisiones toma el orquestador.
- [Apéndice matemático](mathematics.md): objetivos, incertidumbre, potencial de descendientes, fidelidad por modelo y políticas de cambio de contexto.
- [Protocolo, persistencia y presentación](protocol.md): cómo medir, guardar, reanudar y explicar sin confundir investigación con evidencia.
- [Bibliografía anotada](bibliography.md) y [catálogo estructurado](references.json): 55 fuentes seleccionadas, con límites y alcance de lectura.
- [Contrato propuesto de registros](records.schema.json) y [configuración de investigación](lab-spec.json): especificación, sin claves ni lanzador de modelos.
- [Contraejemplos numéricos](counterexamples.json): ejemplos diseñados para mostrar errores de selección; no son resultados del juego.
- [Registro de búsqueda](search-audit.json) y [notas de verificación](findings.md).
- [Auditoría de cobertura y comprobaciones](completion-audit.md).

## La correspondencia más cercana con tu idea

| Lo que quieres | Método especialmente relacionado | Qué tomaría |
|---|---|---|
| Abrir muchas actitudes generales y luego afinarlas | MCTS-AHD; AB-MCTS | Árbol de candidatos y elección explícita entre mayor anchura y mayor profundidad. |
| Reutilizar información de los mejores sin perder variedad | ShinkaEvolve; MAP-Elites | Archivo, familias distintas e inspiración entre ramas. |
| Repartir trabajadores según progreso | AdaEvolve; identificación de la mejor alternativa | Separar generación de candidatos de medición repetida. |
| Recuperar ramas descartadas | Archivos evolutivos; Go-Explore como inspiración parcial | Dormancia reversible, causa registrada y pruebas de reapertura. |
| Cambiar de actitud cuando la carrera lo requiere | Opciones; políticas interpretables por contexto | Reglas generales de entrada/salida de un modo, evaluadas dentro de la política completa. |
| Opus supervisando a Haiku/Sonnet | Orquestación documentada por Anthropic; optimización con múltiples fuentes | Contextos independientes y calibración del sesgo de cada actor. |
| Que sea defendible ante el jurado | Ablaciones y trazabilidad | Mostrar qué componente ayudó, qué falló y qué no podemos afirmar. |

Los mecanismos anteriores tienen antecedentes claros. La contribución propia defendible sería **cómo los adaptamos a este problema, qué errores evitamos y qué mejora medimos**, no afirmar que inventamos el árbol evolutivo o una nueva variante óptima de MCTS.

## Cinco conclusiones que cambian la ejecución

1. **Una mala política no prueba que todos sus descendientes sean malos.** La puntuación del padre no es una cota superior de su familia.
2. **Un buen comienzo no garantiza un buen final.** El recurso escalable debe ser el número de episodios terminales; no asumir que puntuar sólo ocho meses preserva el orden de estrategias.
3. **Haiku y Sonnet no son réplicas intercambiables.** Una misma instrucción puede inducir conductas distintas. Hay que conservar estadísticas separadas y comprobar transferencia al modelo objetivo.
4. **Una rama no se vuelve buena sólo por reabrirla.** Puede haber ruido, un descendiente mejor, un especialista contextual o un cambio de modelo/entorno. Cada explicación requiere una prueba distinta.
5. **Miles de trabajadores no compran independencia ni generalización automáticamente.** La unidad estadística sigue siendo el episodio y un millón de partidas del dev no revela el test oculto.

## Restricción decisiva de la competición

El runtime evaluado requiere JiuwenSwarm `0.2.4b3`, modo `agent`, y el modelo designado por los organizadores. Las reglas prohíben `team` y procedimientos de entrega que dependan de un líder con compañeros. Este laboratorio externo de episodios independientes se analiza como diseño de investigación **condicionado a aclaración escrita sobre modelos externos, automatización y concurrencia**. No se presenta como una excepción ya autorizada. Los mecanismos de memoria de otros papers tampoco autorizan tablas de respuestas por evento ni fórmulas ocultas en la entrega. [Reglas vinculantes](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html).

Las páginas oficiales de Anthropic confirman los tres modelos 5.5 propuestos; no se ha comprobado su disponibilidad en una clave concreta ni se ha hecho ninguna llamada a ellos. Los IDs, precios y supuestos de coste comprobados están en [el protocolo](protocol.md). La investigación no ha consumido la clave de competición ni ha arrancado otra tanda de simulaciones.

## Qué haría primero

Antes de la gran búsqueda: comprobar autorización y aislamiento, medir el coste real de un episodio y hacer un piloto de **transferencia entre actores** con políticas de familias distintas. Después ejecutaría una versión sencilla del árbol con archivo y episodios completos. Añadiría selección bayesiana, especialización y reapertura adaptativa sólo cuando podamos medir su utilidad frente a esa base.

La primera demostración convincente no sería una imagen de un árbol enorme: sería una comparación con igual presupuesto donde el método encuentra una política mejor, una rama reabierta aporta una mejora replicada o detectamos que Haiku iba a descartar una candidata buena para el modelo oficial.
