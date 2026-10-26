# Diagnóstico de CareerLab desde primeros principios

26 de octubre de 2026. Revisión solicitada por Alejandro. Rama `alejandro/diagnostico-estrategias`; base `917565c`, ESTADO.md de las 16:55 UTC e informe cloud de las 16:57 UTC. Es una fotografía reproducible de los archivos guardados, no una inspección del contenedor en directo. No se lanzan partidas ni se cambia la carrera.

**Actualización contrastada antes de cerrar:** `main` avanzó a `3c1c993` (17:19 UTC) mientras se hacía esta revisión. La nube ya analizó 38 digests de Haiku y creó tres hijas F7 sobre tendencias, decisiones de historia y ascensos. Se incorpora ese avance en §8F y en el orden de experimentos, sin volver a mezclar sus resultados posteriores con la fotografía numérica congelada. Los módulos del fallo de robustez, ejecución y registro no cambiaron entre ambas bases.

**Conclusión:** el laboratorio ya puede producir partidas. Lo que más limita el avance es trasladar lo aprendido al agente oficial, convertir resultados en explicaciones comprobables y concentrar evidencia suficiente en unas pocas hipótesis. Más ejecuciones del mismo proceso pueden reforzar un ranking dependiente del modelo y de sus supuestos sin descubrir una estrategia mejor.

## 1. Qué estamos optimizando realmente

La unidad de competición es un manual que ejecuta un único agente DeepSeek en JiuwenSwarm. Las [reglas oficiales](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html#official-evaluation-score-releases-and-final-score) puntúan cada versión con:

`S = 0,80 × media(Q de tres partidas) + 0,10 × calidad de los SKILL.md + 0,10 × eficiencia de tokens`.

La calidad automática es el promedio de los **SKILL.md**, incluidos descubrimiento y pasos ejecutables. Los documentos `design/` sirven al jurado, junto con el vídeo, si llegamos al top 10. ESTADO.md abrevia ese 10% como calidad de los documentos de diseño: conviene que la organizadora precise la distinción. Se mantiene la decisión de empezar la documentación de entrega el 27 de octubre.

Buscar un buen resultado con Claude es un medio. Nuestro objetivo es la distribución de resultados de DeepSeek con el paquete final, su capacidad de ejecutarlo y la validez de la entrega. El máximo de hasta tres versiones puntuadas da valor a conservar una versión estable y probar mejoras distintas; no autoriza a confundir variabilidad con superioridad.

### Supervivencia y crecimiento son dos palancas diferentes

Por identidad matemática, `E[Q] = p × E[Q | completa] + (1−p) × E[Q | eliminada]`.

El Haiku principal, entre distintas políticas y excluyendo el smoke de infraestructura, tiene:

| Medida | Resultado |
|---|---:|
| Partidas | 91 |
| Completadas | 45: 49,5% |
| Q media de todas | 43,93 |
| Q media de completadas | 59,81 |
| Q media de eliminadas | 28,40 |
| Eliminaciones con supervivencia declarada de 24 meses | 25 de 46 |
| Acciones rechazadas | 1 de 13.821 acciones |

Como **escenario algebraico**, manteniendo las medias condicionales, subir la probabilidad de completar diez puntos porcentuales añadiría 3,14 Q. Mejorar cinco Q sólo en las carreras completadas añadiría 2,47 Q con la tasa actual. Son escenarios para comparar palancas, no efectos estimados de una intervención: una carrera rescatada no tiene por qué parecerse a los supervivientes observados.

El diagnóstico «faltan puntos en nivel y dinero entre quienes terminan» identifica una oportunidad, pero no su rentabilidad marginal. Un indicador alejado de 100 puede ser caro o inalcanzable de mejorar en 48 meses. Hay que medir cuánto cambia al intervenir, qué cuesta y si la intervención altera la supervivencia.

## 2. Prioridades por impacto

P0 significa que puede desviar la decisión principal; P1, que limita seriamente el aprendizaje; P2, que merece optimización después de lo anterior.

| Prioridad | Cuello de botella | Evidencia o límite | Cambio propuesto |
|---|---|---|---|
| P0 | Transferencia al objetivo sin medir | No hay resultados de DeepSeek; Haiku y Opus ordenan de forma distinta las seis políticas compartidas | Resolver T5/T6 y validar candidatos diversos con el programa oficial antes de fiarse del ranking proxy |
| P0 | T13 interpretada como techo | Prueba una combinación nueva de manual, esfuerzo y contexto; ninguna garantiza dominar a otras políticas o modelos | Usarla como diagnóstico de esa combinación y para estudiar fallos; eliminar la inferencia de que una nota baja demuestra poco margen |
| P1 | Pocas muestras frente a mucha variación | 4–5 repeticiones por muchos candidatos; el líder cayó de 61,3 Y a 55,2 | Separar exploración, comparación concentrada y confirmación nueva; informar incertidumbre |
| P1 | Ranking sensible al modelo estadístico | Con partidas fijas, cambiar familias cambia el líder y de 0 a 8 políticas dormidas | Añadir sensibilidad de agrupación y un resumen de supervivencia/notas; confirmar por resultados nuevos |
| P1 | Faltan datos portables para explicar fallos | Las rutas de trazas exportadas no existen aquí; el registro no guarda la causa terminal completa | Exportar un resumen estructurado por episodio que incluya decisiones, feedback y causa de salida |
| P1 | Protecciones que no bloquean el camino real | Reproducción offline: `robust=false` y acción `DORMANT` simultáneas | Hacer cumplir robustez, alarmas y ámbito de selección antes de emitir acciones operativas |
| P1 | Cambios difíciles de atribuir | La destilación completa añade varias reglas y modifica la recuperación; comparaciones de actores también cambian contexto | Un cambio de mecanismo por contraste, y comprobar que el jugador lo ejecutó |
| P1 | Detector defensivo demasiado amplio, como hipótesis | F3 incluye cualquier mención a HR, compliance, complaint o audit entre señales de riesgo | Auditar falsos positivos y medir defensa necesaria frente a defensa que desplaza crecimiento |
| P1 | Perder rendimiento en decisiones de historia | El diagnóstico nuevo de 38 digests relaciona caídas tras la última fase trimestral con peores revisiones; la nube ya prueba hijas F7 | Priorizar esas pruebas existentes, verificar la ejecución y evitar atribuir causalidad a asociaciones entre revisiones |
| P2 | Contexto y llamadas al LLM | Mediana Haiku completo: 12,1 min y 32,32 M tokens, casi todos lecturas de caché | Contexto compacto y menos llamadas redundantes, manteniendo fidelidad y capacidad de recuperar estado |
| P2 | Novedad medida por texto | Más manuales no garantizan comportamientos distintos | Comparar huellas de acciones y mecanismos; aparcar duplicados de comportamiento |
| P2 | Restricciones finales y fechas | Hay componentes distintos de puntuación, vídeo obligatorio y corte cercano | Mantener la ruta de entrega; mejorar claridad de las Skills también puede mejorar ejecución |

## 3. Transferencia: política, jugador y programa están entrelazados

El [informe cloud](../../../lab/reports/cloud-run-status.md#problem-a-check-haiku-vs-opus100k-on-shared-policies) ya compara seis políticas: Spearman descriptivo −0,26 entre medias posteriores de Haiku y Opus~100k. Opus favorece F1/P0; Haiku, variantes de F3. Las celdas tienen pocas repeticiones: esto no prueba una correlación poblacional negativa, pero sí invalida asumir un orden universal.

Además, los actores registrados usan `skills_mode=inline`: [render_system_prompt](../../../careerlab/actors/claude_cli.py#L62) añade el texto de todas las Skills al mensaje de sistema. Eso no mide fielmente descubrimiento, selección de Skills ni conservación tras compresión en el programa objetivo. El modo `plugin` de Claude puede servir para una prueba intermedia, pero tampoco sustituye JiuwenSwarm.

Hay al menos tres preguntas distintas:

1. ¿La idea de la estrategia es buena para el juego?
2. ¿Este modelo entiende las condiciones y ejecuta sus acciones?
3. ¿El programa le carga las instrucciones y conserva el estado que necesitan?

Un resultado bajo no distingue esas causas. Propongo pruebas de decisiones sobre observaciones ya guardadas: exigir una acción, la señal pública que la justifica y el modo activo; comparar actores y formatos sobre las mismas entradas. Es una prueba barata de ejecución, no un sustituto del resultado de una partida completa. Las respuestas se contrastan con la intención del manual y la observación, no con supuestas respuestas óptimas de eventos.

Dos partidas piloto del modelo final miden coste y detectan fallos evidentes. No certifican transferencia. La comprobación posterior debería incluir diseños de mecanismos diferentes y algún candidato que Claude penalizó, además de sus líderes. Sólo comprobar líderes impide detectar buenos manuales rechazados por el sustituto. El presupuesto de [target-budget.md](../target-budget.md) ya reconoce esta necesidad: hay que ejecutarlo y recalcularlo con coste medido, no crear otro presupuesto ficticio.

## 4. T13 no proporciona una cota superior

El [informe de T13](../../../lab/reports/opus-ceiling/README.md) clasifica una media baja como «cerca del techo» y propone mover esfuerzo de búsqueda a fiabilidad y tokens. También afirma que Opus acota desde arriba lo que alcanzaría un modelo más débil con ese texto. **Esa inferencia no está justificada.**

- La capacidad general de un modelo no implica dominancia de rendimiento para cada manual. Las comparaciones compartidas ya muestran órdenes distintos.
- T13 cambia a la vez el manual, esfuerzo y configuración de contexto. Un fallo puede proceder de cualquiera de ellos.
- Las cuatro o seis partidas miden la variación de esa combinación; no exploran el espacio de estrategias.
- Su propio documento estima errores estándar de 6–8 Y, más anchos que sus bandas de cinco puntos.
- La referencia congelada Y=60,21 era un líder elegido entre muchos con poca muestra; ahora el líder está en 55,21. La incertidumbre de esa referencia también importa.

La lectura útil es: qué hace una síntesis extensa con un razonador potente, qué instrucciones respeta y por qué falla. Un resultado bajo pide localizar y contrastar el fallo; no demuestra que no exista una política mejor. Un resultado alto mostraría un rendimiento observado prometedor de esa combinación, sin garantizar su traslado a DeepSeek.

Tampoco hay una probabilidad fundada de «ganar a todos los equipos»: desconocemos su distribución de resultados. Podemos mejorar nuestra puntuación esperada, fiabilidad, evidencia y entrega.

## 5. Ruido, agrupaciones y falsa precisión

La [reproducción offline](model-sensitivity.json) mantiene exactamente las partidas del prefijo de Haiku y sólo cambia su agrupación para el modelo jerárquico:

| Agrupación | Primer candidato | Y estimada de F7 / F3 recombinada | Dormidos |
|---|---|---|---:|
| Familias registradas | F7 tres skills | 55,21 / 50,90 | 2 |
| Una familia común | F7 tres skills | 47,41 / 46,93 | 0 |
| Una familia por política | F3 recombinada | 57,77 / 58,49 | 8 |

Esto no demuestra que deba eliminarse el agrupamiento. Sin él, cuatro victorias pueden producir una confianza excesiva en una política que aún no ha mostrado su cola de derrotas. Demuestra que la genealogía asignada condiciona bastante la decisión. La robustez entre distribuciones de ruido no cubre esta sensibilidad de familias.

F7 completa 5/5; su intervalo descriptivo de Wilson al 95% para completar es aproximadamente 56,6–100%. F3 recombinada completa 4/4: 51,0–100%. No son intervalos válidos para todos los momentos de una búsqueda adaptativa, ni garantías de fiabilidad. Ayudan a visualizar lo poco que dicen muestras tan pequeñas.

Con SD de Y dentro de las políticas de Haiku ≈16,14, la fórmula aproximada de planificación del protocolo —alfa unilateral 10%, potencia 80%, diferencia relevante 4 Y— da **unas 147 partidas por brazo**. No significa que debamos gastar eso en todos los manuales. Significa que afirmar pequeñas mejoras con cuatro partidas sería injustificado y que conviene buscar mecanismos con efectos grandes, reducir ruido evitable y concentrar pruebas en pocos finalistas.

Una política tiene dos riesgos distintos: variación entre carreras y desconocimiento de su media. Como la evaluación oficial promedia tres carreras, una muestra local de victorias no garantiza estabilidad oficial. Conviene mirar la distribución predictiva de esa media, además de la posterior de la media verdadera.

Un modelo de dos partes puede servir como sensibilidad: probabilidad de completar y distribución de Q condicionada a completar o eliminarse. Facilita entender qué cambia. Con pocos datos necesita priors prudentes y sensibilidad; no es una mejora demostrada sobre el método vigente. El resultado principal sigue siendo Y y la validación final son partidas nuevas del objetivo. Un cambio de protocolo requiere una nueva versión, sin reescribir v1.

## 6. Qué información estamos dejando sin aprovechar

Los agregados dicen cuánto, pero no explican qué corregir. [Registry.ingest](../../../careerlab/store.py#L201) conserva Q, meses, dimensiones normalizadas y uso, pero no exporta como campos propios la causa completa de fallo, cronología de ascensos, evaluaciones ni acciones por fase. Cuando la traza queda en otra máquina, [analysis.load_cells](../../../careerlab/analysis.py#L44) reconstruye el resultado sin `failure_reason`; algunas causas quedan vacías en los informes importados.

En esta revisión ninguna de las 151 rutas de traza de IA puntuadas es accesible localmente. Eso no demuestra que se hayan perdido: limita lo que una nueva sesión puede estudiar. Los 14 digests de Opus ayudan, pero no cubren todos los Haiku ni las nuevas hipótesis.

El siguiente artefacto de mayor utilidad sería un **resumen portable por episodio**, generado por quien tiene la traza, con:

- Versión/hash, actor, entorno, origen, estado terminal y motivo de salida.
- Por decisión: fase, señales públicas relevantes, acción elegida y efecto observado; distinguir la fase y evolución del estado.
- Notas breves del agente, modo previsto, modo que parece ejecutar y posibles contradicciones.
- Evaluaciones y feedback, ascensos, consumo de energía por acción, tendencias de salud/dignidad y dinero.
- Interrupciones y continuaciones; métricas que incluyan todos los segmentos de traza.
- Texto original consultable de los casos dudosos, conservado como artefacto privado del desarrollo y sin copiar respuestas de eventos al paquete final.

Así se puede distinguir un manual que no se entiende de uno bien ejecutado pero malo. Las partidas con incumplimientos siguen contando en su resultado: el diagnóstico de ejecución no debe servir para eliminar resultados incómodos.

## 7. Protecciones del método y camino real de decisión

### Hallazgo reproducido: robustez informativa pero no bloqueante

[block_decision](../../../careerlab/decisions.py#L49) calcula la robustez y las acciones por separado. Devuelve las acciones de `stats.decide` incluso cuando la robustez es `inconclusive`. El [driver cloud](../../../scripts/cloud-run/driver.py#L97) registra esa salida. En cambio, la búsqueda del juguete incluye su propio tratamiento de inconclusión.

El [script de sensibilidad](model_sensitivity.py) reutiliza el ejemplo de colapsos de `tests/test_stats.py`. Sustituye sólo la lectura del registro por datos en memoria; el cálculo de robustez es real y se fija su semilla para reproducibilidad. Obtiene:

```text
robust = false
acciones: L=STOP, M=STOP, N=REPEAT, X=DORMANT
nota: la dormancia de X cambia entre normal, Student-t y bootstrap
```

La función permite emitir una acción que el protocolo dice que debería esperar. **No demuestra que la decisión #114 sea errónea: esa decisión reporta robustez positiva.** La organizadora puede detectar casos manualmente, pero la protección no está impuesta en ese camino del programa.

### Ámbito de selección y alarmas

El mismo camino no impone la autoridad del actor objetivo antes de rotular PROMOTE/DORMANT ni integra las alarmas de interrupción del §3. Algunas celdas de Haiku tienen 1 intento interrumpido entre 5 o 6 resueltos; no se deduce que sigan averiadas, porque pudo arreglarse la infraestructura después. Hace falta una comprobación y una resolución registradas, no asumirla a partir del rótulo.

`collect` permite filtrar entorno, pero es opcional y el driver no lo especifica. Hoy sólo hay un entorno exportado: no hay evidencia de mezcla de versiones en estas cifras. También recoge todos los propósitos y reconstruye el orden por propósito y repetición; sería prudente definir el conjunto de datos y la frontera de bloque explícitamente antes de ampliar el sistema.

Recomendación: las decisiones operativas deben incluir `exploratory` frente a `target`, autoridad, alarmas, ámbito de datos y si son ejecutables. Una comprobación fallida debe impedir aparcar o promocionar automáticamente. Probar ese contrato en el camino completo del driver aporta más que añadir otra prueba aislada de una fórmula estadística. No se ha implementado ningún cambio en esta revisión.

## 8. Mecanismos del juego que merecen experimentos

Son hipótesis, no fórmulas descubiertas ni reglas garantizadas.

### A. La defensa puede consumir el presupuesto de crecimiento

F3 lean considera señal de riesgo cualquier referencia a HR, compliance, complaint o audit, entre otras. Palabras institucionales pueden acompañar una advertencia real o una situación normal. Si se sobreactiva el modo defensivo, `Defuse legacy risk` consume dos de los tres puntos de energía; queda poco margen para otras inversiones. La [regla pública](https://techarena-career-sim.readthedocs.io/en/latest/rules.html#quarterly-energy-actions) permite calcular ese coste sin adivinar un efecto oculto.

Contraste: advertencia semántica de exposición acumulada o problema pendiente frente a detección por vocabulario amplio, manteniendo iguales las respuestas a señales inequívocas. Medir falsos positivos, frecuencia de defensa, resultados de evaluaciones y crisis. Menos defensa sólo es una mejora si su riesgo adicional no anula el crecimiento.

### B. Una evaluación débil necesita una corrección ejecutable

El estado describe despidos tras rachas de evaluaciones débiles. Interrumpirlas es un objetivo auxiliar razonable, pero una asociación observada no demuestra un contador universal ni una condición suficiente de despido. La nota no debe convertirse en «haz X en el mes 24».

Hay que comprobar si el jugador combina una corrección de resultados con gestión del riesgo, o si una prioridad anula a la otra. Una acción principal puede buscar rendimiento mientras la energía contiene riesgo y recuperación. El [análisis de destilación](../../../lab/reports/teacher-digests/distilled-rules.md) propone mecanismos útiles, pero contiene confusión entre actor, política y comportamientos elegidos. Muchas evaluaciones de una misma partida no son muestras independientes.

### C. Los indicadores deben interpretarse por significado y tendencia

«Mejorar el indicador menor» puede comparar magnitudes en escalas diferentes. Network pequeño no prueba que sea el cuello de botella respecto a Skill u Output. Contraste: elegir por feedback explícito y tendencias observadas frente a tamaño numérico. Verificar también que una subida nominal se refleja en el estado o en resultados posteriores: una respuesta sin cambio no demuestra por sí sola un tope oculto.

### D. Crecer requiere convertir trabajo en reconocimiento y dinero

Las [reglas públicas](https://techarena-career-sim.readthedocs.io/en/latest/rules.html) dicen que el salario mensual aumenta con el nivel: 0,3 en L1, 1,0 en L5 y 9,1 en L10. Una promoción temprana puede influir en varios meses de ingresos. También suben las exigencias de promoción y desempeño. Forzar una promoción sin capacidades sostenibles puede empeorar la trayectoria.

Contrastes útiles: crecimiento eficiente con acciones de evidencia/visibilidad frente a esfuerzo intensivo; y consolidar capacidades tras un ascenso frente a seguir acelerando. Las opciones de historia que convierten resultados en responsabilidad reconocida o remuneración son una hipótesis a leer en contexto, no un catálogo de respuestas fijas.

### E. Complejidad de instrucciones y memoria

Una síntesis extensa puede sumar reglas que compiten por los mismos recursos. La hija destilada completa mezcla varias modificaciones; su mal resultado no refuta cada regla. Propongo contrastar una única modificación sobre un padre congelado y registrar precedencia y condición de salida del modo.

El manual candidato debería poder expresarse con pocas prioridades: proteger lo que amenaza la continuidad, corregir el feedback vigente, aprovechar oportunidades de crecimiento y revisar el efecto. La energía y la acción principal necesitan una coordinación explícita. Una memoria breve puede retener compromisos, último feedback, tendencias y problemas pendientes sin repetir la historia; debe probarse que el programa oficial la conserva.

### F. Lo que añade el diagnóstico nuevo de la nube

El [diagnóstico del bloque 3 en `3c1c993`](https://github.com/aleetreny/huawei/blob/3c1c993/lab/reports/cloud-run-diagnostics/block3-generation.md) es un avance en la dirección correcta: estudia 38 digests de Haiku y propone tres hijas del líder, `f7-trend-marking`, `f7-delivery-stories` y `f7-promotion-drive`. Es preferible evaluar esas hipótesis ya escritas a volver a producir variantes equivalentes.

Encuentra que 12/14 carreras con primer ascenso en la primera revisión completan, frente a 0/13 sin ascenso en las dos primeras. También describe 14/60 revisiones «buenas» tras una caída de Output/Network por historias después de la última fase trimestral, frente a 34/66 sin esa caída. Las mezclas de energía y acción principal son parecidas en los grupos. Esto eleva la prioridad de comprobar decisiones de historia y conversión a ascensos, frente a otro barrido general de energía.

Hay cuatro precauciones de identificación:

- **Ascender pronto es un resultado intermedio, no una asignación al azar.** La diferencia de 57 frente a 22 Q entre esos grupos no mide lo que ganaría una misma política por forzar un ascenso. Las carreras pueden diferir antes en riesgo, decisiones o eventos.
- **La unidad sigue siendo la partida.** Las 126 revisiones de ese contraste pertenecen a 38 carreras; no son 126 observaciones independientes. Además, el diagnóstico define revisión «buena» como B o mejor **o ascenso**, que no equivale a contar sólo notas B.
- **La variable operativa cambia.** «En su máximo» se define en el diagnóstico usando el máximo visto en todo el conjunto para ese nivel. Un manual sólo puede usar la información de su partida y su pasado. La hija de tendencias utiliza un máximo reciente propio; hay que verificar si ese sustituto recoge el mismo fenómeno.
- **Causas y cohortes deben quedar claras.** El diagnóstico cuenta 11 despidos al mes 24 entre sus digests, frente a los 14 del estado, y encuentra una carrera con B que sale en el mes 24 por crisis de confianza. Una B puede relacionarse con evitar el despido por rendimiento sin evitar otras causas de salida. Conviene corregir la afirmación más general del estado al integrar, conservando su responsable.

La acción más útil es seguir esas hijas con resúmenes de cumplimiento y resultados de carrera completa. La hipótesis de que el cuello está en conservar resultados entre la última inversión trimestral y la revisión es concreta y falsable; aún no es una ley del juego.

## 9. Secuencia de experimentos propuesta

Estas propuestas no crean nuevas tareas del tablero ni autorizan ejecuciones aquí. La organizadora decide cuáles caben en T1–T4/T6, el presupuesto y el ensanchamiento de familias. No hay que ejecutar toda la lista a la vez.

| Orden | Pregunta | Contraste y datos | Decisión que cambia |
|---|---|---|---|
| E0 | ¿Funciona el paquete en el objetivo y cuánto cuesta? | T5/T6 existentes: dos partidas del programa oficial; registrar carga de Skills, uso, coste y estado final | Fijar presupuesto real y detectar fallos de traslado antes de gastar el resto |
| E1 | ¿Por qué fallan los manuales actuales? | Autopsia de 8–12 trazas existentes: varios fallos y victorias del mismo actor y manuales relevantes; resumen portable | Elegir un mecanismo concreto que corregir; separar obediencia y estrategia |
| E2 | ¿El modelo interpreta la misma instrucción igual? | 30–50 observaciones guardadas, equilibradas por fases y señales; comparar manual compacto/modular y actores con respuestas estructuradas | Descartar una redacción ambigua y detectar diferencias de interpretación; no seleccionar por Q ficticia |
| E3 | ¿Las decisiones de historia y el marcado de riesgo cambian la trayectoria? | Aprovechar las tres hijas F7 del bloque 3; comparar cada cambio con su padre y registrar tendencias, acciones y ascensos, manteniendo el resto constante si se quiere atribución | Contrastar la hipótesis nueva ya respaldada por trazas, sin duplicar candidatos |
| E3b | ¿Riesgo y visibilidad se complementan, si sigue sin resolverse? | Diseño 2×2 en episodios nuevos: bloque de dos puntos Defuse frente a recuperación, y último punto Prepare report frente a Network; acción principal y reglas de seguridad comunes | Distinguir defensa, evidencia e interacción; secundario frente a E3 con la evidencia nueva |
| E4 | ¿La defensa se activa demasiado? | Padre congelado frente a una única hija con detector contextual; mismas respuestas a señales inequívocas | Mantener o reducir defensa según Q, crisis y cumplimiento real |
| E5 | ¿Qué crecimiento compensa sin más eliminaciones? | Sobre una base estable, una hija de crecimiento eficiente y, si hay evidencia, otra de consolidación tras ascenso | Comprobar rentabilidad neta y posible trampa de crecer antes de estar preparado |
| E6 | ¿Cuál resiste el cambio de actor/programa? | Contrastar finalistas diversos y un candidato penalizado por Claude con DeepSeek; congelar y confirmar los elegidos en partidas nuevas | Elegir la entrega por evidencia del objetivo, con incertidumbre explícita |
| E7 | ¿Podemos reducir uso sin perder decisiones? | Contexto compacto frente al vigente, instrucciones iguales y configuración nueva identificada; registrar recuperación de estado | Ganar capacidad de investigación y presupuesto sin ocultar una regresión |

E3b es una propuesta de contraste experimental, no una recomendación de energía universal. El diseño completo debe escribirse antes de usar sus datos: alternativas de igual coste, momentos elegibles y protección de estado crítico comunes, y comprobar cuántas veces se ejecuta la intervención. Se evalúa el efecto del manual asignado desde una partida nueva. Si las reglas de seguridad anulan todas las diferencias, el experimento no informa sobre el mecanismo. Cualquier restricción metodológica nueva se versiona; no se reescribe el protocolo congelado.

### Cuántas pruebas y cuándo parar

- **Exploración:** el mínimo actual de cuatro episodios sirve para detectar errores grandes y verificar la ejecución. Si 3/4 repiten el mismo fallo de ejecución, aplicar la regla ya existente y corregir; una nota baja no equivale a fallo de ejecución.
- **Comparación:** ampliar un pequeño conjunto, por ejemplo hasta 12–20 repeticiones cuando el presupuesto y el asignador lo permitan. Eso mejora la estimación, pero no asegura distinguir cuatro Y con la dispersión actual. Elegir por utilidad esperada y coste de equivocarse cuando no alcanza la precisión.
- **Aparcar:** seguir el protocolo, su robustez y sus reaperturas; mantener las conclusiones proxy como exploratorias. Una señal de ejecución ausente exige revisar la manipulación, no inventar un mecanismo causal.
- **Confirmación:** nuevas partidas del objetivo después de congelar finalistas, sin usarlas para seguir editando. Si no alcanzan la diferencia relevante, llamarlo estimación. El tiempo de corte limita cuánto se puede aprender; se elige el mejor candidato respaldado, sin prometer certeza imposible.
- **Estancamiento:** una hipótesis que contradiga el diagnóstico dominante, con un cambio interpretable, vale más que diez reescrituras parecidas. Ejemplos: menos defensa contextual, visibilidad barata en vez de esfuerzo intensivo, o consolidar después de ascender.

No hay semillas controladas ni clonación en el MCP documentado. Intercalar lanzamientos equilibra condiciones de ejecución, pero no crea partidas pareadas con los mismos eventos. Las muchas decisiones de una carrera tampoco son episodios independientes. Si se usan intervenciones dentro de una carrera, deben registrarse probabilidades, elegibilidad y efectos acumulados; no confundir ese diagnóstico con la evaluación de una política completa.

## 10. Cómo usar millones de simulaciones con sentido

Con el contrato actual, las simulaciones posibles son distintas:

| Recurso | Preguntas que sí puede contestar | Lo que no establece |
|---|---|---|
| Juego sintético propio | Si el asignador se equivoca con beneficios tardíos, cambios de ranking, colas de pérdidas o deriva | Una estrategia ganadora o la fórmula del juego real |
| Bots rápidos sobre el MCP real | Efectos de contrastes acotados de acciones bajo sus reglas fijas; estabilidad del programa | Que la conclusión se mantenga con decisiones de historia distintas o con DeepSeek |
| Partidas completas con LLM | Rendimiento de ese manual/modelo/programa y trazas de sus decisiones | Por sí solas, causalidad de cada regla ni transferencia a otro actor |
| Pruebas de decisiones guardadas | Comprensión, precedencia, carga y consistencia del manual | Consecuencias contrafactuales a 48 meses |

El principal límite de bots aleatorios es alcanzar los estados importantes: casi todos mueren antes de poder informar sobre ascensos y dinero. Un millón de repeticiones concentradas ahí reduce incertidumbre sobre ese fracaso, pero no sobre una buena carrera. Para estudiar crecimiento hace falta una política base que llegue a esas situaciones y contrastes que cambien una cosa manteniendo la interpretación de las historias comparable.

A 726,56 segundos por carrera completa de Haiku, seis jugadores simultáneos producirían alrededor de 714 carreras completas/día si ese rendimiento fuera constante y no hubiese límites. Un millón exigiría unos 1.400 días, antes de cuota o fallos. Es una extrapolación de ritmo, no un pronóstico. La velocidad de los bots y del MCP no elimina el coste de razonar cada turno.

En Haiku completado, el tiempo de API reportado representa 98,6% de la duración y las lecturas de caché 99,2% de los tokens contados. Los 32,32 M tokens no son todos tokens nuevos ni equivalen a cuota facturada. Aun así, conservar un historial largo implica procesamiento repetido. El rendimiento debería medirse como incertidumbre útil reducida por unidad de cuota, tiempo y gasto del objetivo; los dólares a precio de lista de Claude no miden su cuota de suscripción.

La mediana proxy de 673.305 tokens/mes correspondería aritméticamente a E≈93,1 si esos conteos se interpretasen como los oficiales: bajar a la meseta de 500.000 aportaría unos 0,69 puntos automáticos. No es una predicción de E para DeepSeek. Sí ilustra por qué los tokens importan para el presupuesto, pero reducirlos no debe sacrificar varios puntos de Q.

### Métodos que sí encajan, y sus condiciones

- **Reflexión sobre trazas al estilo [GEPA](https://arxiv.org/abs/2507.19457):** generar cambios por fallos observados y conservar soluciones complementarias. Adaptarlo a este juego exige evaluación estocástica y confirmación; su éxito publicado no certifica este caso.
- **Diseño experimental dirigido a decisiones:** elegir el siguiente contraste por cuánto puede cambiar la elección del manual y por su coste. La [investigación de active learning orientado a decisiones](https://arxiv.org/abs/2106.04193) justifica ese objetivo; implementarlo aquí exige supuestos calibrados y no calcular una ganancia de información ficticiamente exacta.
- **Carreras adaptativas y modelos de respuesta pequeños:** después de fijar unos pocos factores de estrategia, asignar más repeticiones donde una comparación importa. Un sustituto estadístico ayuda a proponer experimentos; la comparación final vuelve al juego real.
- **Incertidumbre y confirmación:** la [literatura de evaluación con pocas ejecuciones](https://arxiv.org/abs/2108.13264) respalda tratar rankings e intervalos con cautela. Aquí el promedio oficial sigue siendo el objetivo; no sustituirlo por otra métrica porque se vea más estable.
- **Modelo aprendido del juego:** puede ordenar hipótesis con incertidumbre, pero las observaciones son parciales y las acciones de las trazas no se eligieron al azar. Ajustar millones de transiciones no identifica automáticamente efectos causales. Un planificador puede explotar errores del modelo; el rendimiento predicho necesita pruebas reales nuevas.

Un MCTS exacto necesitaría ramificar desde el mismo estado o un simulador generativo fiel. El [MCP documentado](https://techarena-career-sim.readthedocs.io/en/latest/mcp.html#available-mcp-tools) no ofrece esas operaciones. Tampoco es válido estimar el resultado de una política nueva simplemente contando coincidencias con acciones de una traza: faltan acciones no elegidas y probabilidades conocidas de selección.

## 11. Qué haría primero

1. Desatascar la clave y el piloto objetivo por T5/T6. Mantener mientras tanto la carrera exploratoria con sus límites existentes.
2. Pedir a quien tiene las trazas los resúmenes portables y autopsias de fallos concretos. Utilizar los Opus de T13 como casos de diagnóstico, sin tratar su nota baja como techo.
3. Hacer efectivas las protecciones del camino real de decisión. Documentar y resolver alarmas; distinguir rótulos exploratorios y decisiones para entrega.
4. Concentrar el siguiente aprendizaje en **una pregunta causal**: primero aprovechar las hijas F7 ya creadas sobre conservación de resultados, tendencias y ascensos. Después, si sigue abierto, comprobar si el detector de riesgo consume demasiadas oportunidades de rendimiento. No lanzar todas las hipótesis propuestas a la vez.
5. Mantener finalistas de mecanismos distintos, comprobar el traslado y congelar para confirmación. Reservar la entrega y el vídeo; la experimentación adicional tiene valor sólo si puede cambiar una decisión a tiempo.

La capacidad del laboratorio ya es suficiente para esta fase. El siguiente salto probable viene de mejorar qué aprendemos de cada partida y de ejecutar un manual claro en el sistema que realmente puntuará.

## 12. Reproducibilidad y límites

- [summary.json](summary.json): descriptivos de 308 filas exportadas, de las cuales seis son interrupciones sin puntuación. 302 terminales: 150 bots y 152 IA incluyendo un smoke; quitándolo, 150 de la carrera central y una de Leah. Los 400 bots T10 tienen registro separado.
- [analyse_exports.py](analyse_exports.py): cálculo offline con biblioteca estándar, incluyendo hashes de los archivos de entrada, verificaciones de unicidad y exclusión explícita de interrupciones. La descripción por actor/política/origen/entorno evita mezclar celdas para tomar decisiones.
- [model-sensitivity.json](model-sensitivity.json) y [model_sensitivity.py](model_sensitivity.py): reproducción del ranking, sensibilidad de familias y fallo de robustez con datos de prueba, sin crear ni consultar un registro SQLite.
- [findings.md](findings.md), [progress.md](progress.md) y [task_plan.md](task_plan.md): evidencia y seguimiento de esta revisión. [sources.md](sources.md): fuentes externas y alcance de las búsquedas.
- Suite de la base revisada: `uv run pytest -q` → **230 passed, 1 warning in 32.69s**. Aviso de deprecación de Authlib en una dependencia. Estos tests no prueban la validez causal ni el éxito de los manuales.
- Todas las inferencias son de desarrollo. No se han examinado paquetes ni bases internas del simulador, no se han enviado mensajes ni ejecutado partidas y no se han gastado créditos de la clave. No se ha alterado ningún manual ni el protocolo.

## Relevo

1. **Hecho y motivo.** Diagnóstico solicitado de proceso y estrategias. Se distinguen objetivo oficial, transferencia, causalidad, incertidumbre, implementación y coste. Se aportan hipótesis y una secuencia de experimentos para que la organizadora elija.
2. **Resultados.** Base `917565c`; datos y hashes en summary.json. Haiku 45/91 completadas y 25/46 eliminaciones al mes 24; ranking sensible a familias; reproducción `robust=false` con `DORMANT`. Suite: 230 tests correctos. Evidencia y limitaciones arriba.
3. **Pendiente o límites.** Faltan acceso al actor objetivo y trazas completas portables; no se han estimado efectos causales de los cambios propuestos. El fallo de integración queda diagnosticado, sin corregir porque la tarea pedía diagnóstico. La organizadora mantiene la carrera; los resultados posteriores pueden cambiar el ranking.
4. **Retomar.** Revisar/integrar la PR de `alejandro/diagnostico-estrategias`. Desde la raíz del repo: `python3 research/careerlab/diagnostico-2026-10-26/analyse_exports.py` y `uv run python research/careerlab/diagnostico-2026-10-26/model_sensitivity.py`. Los scripts vuelven a calcular sobre la exportación presente: conservar sus hashes para comparar con esta fotografía. Después priorizar T5/T6, resúmenes de trazas y protección del camino de decisión; cualquier ejecución queda a cargo de la organizadora según ESTADO.md.
5. **Estado propio.** Línea informativa de este diagnóstico en ESTADO.md, rama propia, commit/push y solicitud de integración mediante PR. Se conservan las filas de tareas del equipo y el plan global.
