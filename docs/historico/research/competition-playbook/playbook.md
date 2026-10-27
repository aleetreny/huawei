# Elegir un experimento según el atasco

Esta guía no modifica el controlador del laboratorio. Le ofrece un banco de hipótesis enlazado a [casos originales](cases.md) y [fichas completas](strategy-cards.md). La prioridad indicada depende de observar el disparador, no es una clasificación universal de estrategias.

## 1. Diagnosticar antes de generar otra variante

| Síntoma observado | Primeras fichas | Qué puede estar pasando | Qué comparar |
|---|---|---|---|
| Acciones inválidas, reintentos ambiguos o resultados duplicados | P03, P33 | Fallo operativo que se confunde con estrategia | Mismo actor/política y cliente corregido. |
| Olvida compromisos y repite malas interpretaciones | P01, P28 | Memoria sin evidencia o sin mantenimiento | Registro breve frente a memoria libre. |
| Sigue un objetivo pese a feedback contrario | P04, P09 | Coste hundido o plan que no se invalida | Objetivo persistente revocable frente a insistencia. |
| Sobrevive pero no progresa | P08, P10, P11 | Defensa permanente o falta de inversión | Cambio de salida del modo y familias de riesgo/inversión, separadamente. |
| Hay prioridades incompatibles o gasto trimestral torpe | P05, P06 | Cada acción parece buena por separado | Plan conjunto con restricciones públicas frente a greedy. |
| Muchas revisiones pequeñas no cambian el resultado | P14, P15, P17 | Valle entre planes o representación demasiado estrecha | Reconstrucción relacionada y reinicios frente a más ediciones atómicas. |
| Cada mejora local pierde otra capacidad | P23, P24 | Olvido o sobreajuste a una región | Nueva candidata frente a campeón y diagnósticos de regresión. |
| El actor barato ignora instrucciones o cambia el ranking | P07, P20, P25, P26 | Capacidad, complejidad o sesgo de modelo | Matriz de políticas y actores; auditoría de rechazos. |
| Aparece una regla aparente por mes o entre supervivientes | P29, P35 | Fuga de información, calendario espurio o selección | Políticas completas con prefijo fijado; llegada al contexto. |
| Hay muchas llamadas y pocas partidas útiles | P31, P32, P34 | Cuello de botella de coordinación o razonamiento mal asignado | Perfil por componente y pruebas de escalado. |
| La ventaja depende de una prosa enorme | P20, P21, P22 | Exceso de reglas o mala representación | Sustracción, una prioridad o representación intermedia. |
| Se acerca la entrega y el método no se puede explicar | P36 | Evidencia dispersa o retorno decreciente del algoritmo | Reservar síntesis y demostración del procedimiento real. |

Estas asociaciones son diagnósticos propuestos. Un síntoma puede tener varias causas. Antes de editar, formular al menos una explicación alternativa y una observación que permita distinguirlas.

## 2. Cómo utilizar una ficha

1. Identificar el fallo en trazas propias permitidas y delimitar si es del procedimiento, del actor, del cliente o del experimento.
2. Elegir una ficha pertinente y congelar el comparador. Conservar artefacto/hash, actor y periodo experimental.
3. Fijar mejora mínima relevante, precisión buscada, presupuesto y procedimiento de incertidumbre antes de mirar el lote de selección. El [apéndice matemático previo](../hierarchical-lab/mathematics.md) distingue media de una política y potencial de su familia.
4. Medir episodios hasta terminación real. Un final temprano legítimo es un dato; un fallo operativo no recibe una nota terminal inventada. Las tareas pendientes siguen pendientes.
5. Separar selección de confirmación. Una candidata prometedora se confirma con datos nuevos sobre el modelo objetivo. Las celdas Haiku/Sonnet/Opus/objetivo no se promedian como réplicas IID.
6. Registrar resultado: mejora confirmada, regresión, equivalencia práctica o evidencia insuficiente. La dormancia de una variante no elimina sus posibles descendientes.

No existe un número fijo de partidas que convierta cualquier media observada en su “puntuación real”. La varianza, el efecto que queremos distinguir, las comparaciones adaptativas y el coste determinan la asignación. Cuando el presupuesto no permite separar alternativas, la conclusión es incertidumbre, no una victoria estadística.

## 3. Combinaciones que merece la pena estudiar

### Memoria y modos: ¿ayuda guardar más o coordinar mejor?

Cruzar P01 (registro de obligaciones) y P02 (modos interrumpibles) produce cuatro políticas: base, memoria, modos, ambas. No son cuatro partidas: cada política necesita la evaluación que justifique el protocolo. Esto permite detectar si la combinación aporta algo que ninguna mejora logra sola. Mantener el mismo actor y revisar también el coste de contexto.

### Actor y complejidad: ¿estrategia mala o mala ejecución?

Cruzar una política breve y una estructurada con los actores disponibles, dejando cada configuración en su celda. P20/P26 ayudan a formular la revisión y P25 mide transferencia. Si un actor potente rescata la política larga, no queda demostrado que la larga sea mejor para el actor oficial; hace falta la celda objetivo. Revisar rechazos baratos para detectar candidatos perdidos.

### Vecindario y representación: ¿falta afinar o cambiar de enfoque?

Comparar tres procedimientos de búsqueda: mutación atómica, reconstrucción de un bloque relacionado (P14/P15) y nueva representación/familia (P17/P22). Igualar el presupuesto total, incluida generación, validación y coordinación. La unidad de réplica para afirmar que el buscador es mejor es una búsqueda completa, no las muchas partidas de una única búsqueda.

### Cosechar e invertir: ¿el proxy temprano está engañando?

Comparar una política equilibrada, una de inversión justificada por contexto (P11) y una de concentración temporal (P12). Medir terminales y probabilidad de alcanzar fases tardías. Si sólo observamos supervivientes, podemos invertir el orden global de políticas. No volver al mismo mes por clonación ni reclamar estados emparejados si la interfaz no lo proporciona.

### Regresión y novedad: ¿conservar el pasado bloquea descubrir?

P23 protege capacidades anteriores; P16/P17 permiten escalones peores y familias nuevas. Conservar un campeón de entrega aparte de la población de investigación. El criterio del archivo no obliga a cada descendiente a superar inmediatamente al campeón. Comparar cuota de exploración y reglas de reapertura mediante presupuesto fijado, sin anunciar una cuota universalmente óptima.

## 4. Propuestas contraintuitivas que sí tienen una pregunta concreta

| Idea | Fichas | Hipótesis que intenta refutar |
|---|---|---|
| Borrar una parte importante de las instrucciones | P20 | “Más reglas siempre producen mejores decisiones”. |
| Tener una sola prioridad principal temporal | P12, P21 | “Hay que equilibrar todas las dimensiones en cada acción”. |
| Invertir aunque el indicador inmediato progrese menos | P11 | “El mejor comienzo identifica al mejor final”. |
| Dejar de intentar rescatar un objetivo | P09 | “Persistir en un compromiso anterior siempre protege la carrera”. |
| Hacer la política menos defensiva cuando no hay avisos | P08, P10 | “Más prudencia siempre mejora la media final”. |
| Desarrollar descendientes de una candidata peor | P16 | “Un ancestro mediocre acota su subárbol”. |
| Cambiar juntos varios módulos | P14 | “Una mejora buena siempre se puede construir con pequeños pasos que ya mejoran”. |
| Añadir una abstracción intermedia a un modelo pequeño | P22, P26 | “Menos pasos de razonamiento siempre ejecutan mejor”. |
| Gastar más en medir si el presupuesto escala antes de lanzar más workers | P34 | “El cuello de botella es necesariamente falta de paralelismo”. |

Una idea extraña necesita comparador y criterio de refutación igual que una convencional. Conservar también los resultados negativos; evitar rescatar una hipótesis cambiando retrospectivamente la métrica o el subconjunto de episodios.

## 5. Qué se puede adaptar y qué depende de otra competición

| Mecanismo del precedente | Adaptación razonable para investigar | Dependencia que no se importa |
|---|---|---|
| Behaviour trees y roles de AutoAscend/Lux | Modos, condiciones de validez, memoria del episodio | Catálogo de objetos/eventos y números específicos del juego. |
| MCTS de Hungry Geese o simulación de Lux | Comprobación general; búsqueda externa entre políticas | Restaurar estados, undo o simulador generativo no documentado. |
| CP-SAT de Huawei | Validez con costes y presupuesto públicos | Beneficios, transiciones y probabilidades ocultas inventadas como datos. |
| LNS/SA de Flatland/AHC | Mutaciones pequeñas y reconstrucciones de políticas | Comparar como exactas evaluaciones de un solo episodio ruidoso. |
| RL/imitación de Lux | Diagnosticar capacidad y observabilidad; extraer procedimientos generales | Entrenamiento, replay de terceros o constantes ocultas sin aclaración. |
| Expertos de RPS | Selector de experimentos con observaciones reales | Recompensas contrafactuales para acciones o políticas no jugadas. |
| Evaluador rápido de Psyho/Unagi | Perfilar y optimizar nuestro cliente, integrador y contexto | Reescribir o inspeccionar el motor cerrado del CareerSim. |
| División de roles de un bot multijugador | Pasos de razonamiento de un único agente | Equipo de agentes cooperando en el runtime evaluado. |

La [regla vinculante](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html) exige aclarar métodos ambiguos antes de utilizarlos. Una ficha no establece permiso para flotas externas, grandes lotes, aprendizaje de modelos o nuevas interfaces. Se pueden preparar implementación y análisis independientes mientras se concreta ese alcance.

## 6. Las cifras de escala no son unidades intercambiables

- Una iteración de SA modifica un plan y llama a un evaluador barato.
- Un paso de RL es una transición del simulador.
- Un rollout puede ser parcial y usar un estado restaurable.
- Una partida completa tiene un comienzo y un final legítimos.
- Una decisión con LLM puede implicar varias llamadas, entrada acumulada, red y herramientas.

Los millones de evaluaciones internas de Psyho, los pasos de Lux y las partidas de Hungry Geese corresponden a infraestructuras distintas. Para este laboratorio medir por separado episodios terminales, decisiones, llamadas MCP, llamadas de modelo, tokens, segundos y coste. El dato que importa es cuánto mejora la selección de políticas por recursos disponibles, no que un contador alcance un millón.

## 7. Cómo convertir una prueba en evidencia para el jurado

Conservar el disparador, el caso que inspiró el cambio, la política anterior/nueva, los resultados de selección y confirmación, regresiones y coste. Un gráfico de linaje debe mostrar también ramas que fallaron. Una afirmación de mejora requiere sus datos; una afirmación de novedad requiere distinguir el mecanismo conocido de nuestra adaptación.

Una historia defendible puede ser: “Las ediciones pequeñas se habían estancado. Probamos reconstruir juntos los módulos que compartían este fallo. Esta comparación, con presupuesto comparable, mostró este resultado; al retirar la condición de salida reapareció esta regresión”. Sólo completar los valores cuando exista esa evidencia.
