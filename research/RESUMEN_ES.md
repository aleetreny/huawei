# Cómo competir con opciones reales de ganar

**Actualización:** el usuario ha retirado la propuesta anterior. El plan vigente empieza sin Skills seleccionadas y está en [from-zero-lab.md](from-zero-lab.md); la [revisión de Matteo](matteo-branch-review.md) recoge sus simulaciones y mi exploración manual posterior. El texto siguiente conserva la investigación general inicial, no una arquitectura aprobada.

**Investigación: 26 de octubre de 2026.** Carpeta vinculada al repositorio privado `aleetreny/huawei`. Propuesta para Gradient Depression; no hay todavía resultados experimentales propios ni una estrategia ganadora demostrada.

## Mi apuesta

Construiría un agente pequeño y consistente que complete los 48 meses, aproveche bien los trimestres y corrija sus errores a partir del feedback de la partida. Usaría los créditos para comparar unas pocas estrategias realmente distintas y mejorar las Skills con pruebas. No gastaría el presupuesto intentando reconstruir todo el motor.

La ventaja buscada es una cadena completa: interpretar bien el estado → identificar el cuello de botella → comparar acciones disponibles → proteger la continuidad → actuar → comprobar qué ocurrió → ajustar. Un prompt brillante sin esta disciplina puede perder frente a un agente sencillo que nunca olvida un problema acumulado.

## Lo que cambia tu idea de la fuerza bruta

Podemos investigar y ensayar estrategias por las interfaces oficiales. Pero **no está acreditado que se permitan millones de llamadas**. Las reglas dicen que hay que consultar a los organizadores cuando un método no está resuelto en la documentación; no publicar un límite no equivale a dar permiso.

Además, prohíben incluir respuestas fijas por evento y fórmulas o umbrales no publicados presentados como reglas conocidas, **con independencia de cómo se hayan obtenido**. Deducirlos con llamadas legales no autoriza automáticamente incorporarlos a la entrega. Una hipótesis empírica tampoco debe disfrazarse de ley del juego. La inferencia numérica de dinámicas ocultas y cualquier política entrenada con ella necesitan aclaración antes de utilizarlas. Fuente vinculante: [reglas oficiales](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html).

La alternativa con mejor relación esfuerzo/resultado es buscar buenas **políticas generales**: cuándo recuperar, qué carencia profesional priorizar, cuándo corregir riesgos observados y cómo repartir los tres puntos de Energy. No hay todavía una propuesta de Skills seleccionada: primero vamos a observar y comparar comportamientos.

## Qué se puntúa realmente

| Componente | Primera fase | Peso final si entramos en el top 10 |
|---|---:|---:|
| Resultado del juego: media de tres partidas | 80% | 56% |
| Calidad de las Skills | 10% | 7% |
| Eficiencia de tokens | 10% | 7% |
| Revisión experta de vídeo, diseño y Skills | — | 30% |

No hay revisión experta para quienes queden fuera del top 10. Por eso primero necesitamos competitividad en las partidas, sin descuidar documentación y vídeo. La cifra local correcta es `quantitative_score`; no hay que aplicar de nuevo el factor de `competition_partial_score`. [Evaluación oficial](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#official-evaluation-score-releases-and-final-score).

Un detalle muy aprovechable: la eficiencia da la máxima nota hasta **500.000 tokens por mes sobrevivido**. Para 48 meses son 24 millones de tokens. Ahorrar por debajo de esa cifra no mejora ese componente, aunque sí permite hacer más pruebas con los **50 USD máximos** de la clave. No asumiría que el límite alto de puntuación hace asequible consumirlo. [Clave y restricciones](https://techarena-career-sim.readthedocs.io/en/latest/api-key.html).

## Precedentes que sí nos sirven

| Caso | Qué aprender | Qué no trasladar automáticamente |
|---|---|---|
| Huawei Irlanda 2024, equipo de Linan | Búsqueda local y evaluación rápida. Según sus autores, primero en algoritmo y tercero global por una presentación insuficiente. | Allí se conocía el evaluador; aquí no podemos inspeccionar el motor. |
| Huawei Irlanda 2024, segundo puesto declarado | Combinar restricciones con búsqueda: CP-SAT y pattern search. | Necesitan un modelo explícito que este reto no publica. |
| Huawei Irlanda 2025, ganador de eficiencia LLM | Medir calidad y coste juntos. | Era respuesta a preguntas, no una carrera de 48 meses. |
| AHC058, ALE-Agent de Sakana | Proponer alternativas diversas y usar resultados verificables para seleccionar. | Su presupuesto y su evaluador no son los nuestros; no justifica usar varios agentes en el juego. |
| Lux AI y Selenia City | Buenas heurísticas, acciones válidas y pruebas repetidas pueden ser muy competitivas. | Otros concursos permiten inspeccionar simuladores o reconocer mapas; aquí esas prácticas pueden estar prohibidas. |
| GEPA, Vending-Bench y Project Vend | Revisar trazas, mantener memoria útil y comprobar efectos reales. | No basta con reflexionar: las mejoras deben sobrevivir a nuevas partidas. |

En [la guía de precedentes](precedents-and-reading.md) están los enlaces y las limitaciones de cada comparación. UK 2023/2024/2025 no eran anteriores ediciones idénticas de este juego. CareerSim-BDCI26 es un reto de la misma familia y de 2026; no he verificado una solución campeona aplicable al UK actual.

## Plan que ejecutaría esta semana

1. **26 de octubre:** preparar el runner oficial sin cambiar JiuwenSwarm `0.2.4b3`; comprobar clave y modelo recibidos; hacer una partida de referencia y leer sus salidas. Medir coste completo, fallos de herramientas y causas de deterioro.
2. **27 de octubre:** comparar la base con dos variantes: recuperación preventiva frente a desarrollo profesional equilibrado. Conservar la que funcione mejor en varias partidas completas. Grabar ya un vídeo válido y dejar preparado el primer paquete.
3. **28–29 de octubre:** concentrar pruebas en los dos mejores candidatos; añadir memoria breve de tendencias y avisos; corregir un fallo cada vez. Probar si la planificación conjunta de Energy y acción principal aporta mejora.
4. **30 de octubre:** segunda versión con una mejora sustantiva documentada. Mantener un candidato estable y reservar créditos para validar el final.
5. **31 de octubre–1 de noviembre:** nuevas partidas de validación, revisión de Skills, vídeo y ZIP. Evitar cambios grandes sin tiempo para medirlos.

Los cortes son a las **24:00 GMT del 27 y 30 de octubre y del 1 de noviembre**: equivalen a las 00:00 del 28, 31 y 2, respectivamente. El vídeo en inglés, de hasta diez minutos, se exige ya en cualquier ZIP final evaluable. Las versiones ya puntuadas conservan su nota; la mejor válida determina la primera fase. Esto hace valioso llegar a los tres cortes con mejoras reales, aunque no hay garantía de que cada nueva versión mejore. [Envíos y evaluación](https://techarena-career-sim.readthedocs.io/en/latest/submission.html).

## Dónde pondría los créditos

Presupuesto inicial propuesto: 5 USD para comprobar el sistema, 15 para explorar, 15 para confirmar finalistas, 10 para validación final y 5 de reserva. Son límites de trabajo, no tarifas del proveedor. Después de la primera partida hay que recalcular cuántas partidas caben realmente.

La fuerza bruta útil está en generar candidatos de Skills, eliminar variantes malas y explorar combinaciones pequeñas descritas públicamente. Un millón de llamadas repetidas a `observe` no aporta un millón de experimentos. Tampoco existe un `clone_state`, un `undo` ni un parámetro de semilla documentados: no podemos asumir que podemos probar todas las ramas desde el mismo punto.

## Primera decisión estratégica

La propuesta anterior se ha retirado y borrado por petición del usuario. El punto de partida es ahora una fase de exploración y experimentos, sin decidir aún cuántas Skills habrá ni sus responsabilidades. El plan vigente está en [from-zero-lab.md](from-zero-lab.md), junto con la revisión de la rama de Matteo.

La investigación extensa está en [strategy-dossier.md](strategy-dossier.md); las pruebas concretas en [experiment-plan.md](experiment-plan.md); los cálculos de fuerza bruta y créditos en [budget-and-search.md](budget-and-search.md). Las [preguntas para los organizadores](organiser-questions.md) están redactadas en inglés y no se han enviado.
