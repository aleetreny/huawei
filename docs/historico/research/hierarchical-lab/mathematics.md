# Apéndice matemático: qué puede optimizarse y qué no

Fecha de corte: 26 de octubre de 2026. Todas las reglas numéricas propuestas en este documento son **parámetros de un laboratorio**, no fórmulas ni umbrales internos del juego. No hemos ajustado estos modelos a un lote nuevo ni probado la superioridad del sistema.

## 1. El objeto que medimos

Sea `p_i` una política congelada, `m` un modelo actor y `e` una versión de entorno/protocolo. Un episodio produce:

`Y_i,m,e,r = quantitative_score / 100`, con `0 ≤ Y ≤ 1`.

El estimando es `μ_i,m,e = E[Y_i,m,e,r]`. Su distribución incluye las elecciones estocásticas del modelo y la aleatoriedad legítima del simulador. La historia observada dentro de un episodio se denota `h_t`; la política ejecutada por el modelo induce `π_i,m(a_t | h_t)`.

El objetivo de selección es encontrar una política con alto `μ_i,objetivo,e`, no sumar el máximo número de puntos mientras investigamos. Formalmente, para un conjunto de candidatas disponibles, el arrepentimiento simple de devolver `p_hat` es:

`r_simple = max_i μ_i,objetivo,e − μ_hat,objetivo,e`.

La identificación de la mejor alternativa se centra en este objetivo final. Maximizar recompensa acumulada durante el aprendizaje es otro problema y puede dedicar demasiado esfuerzo a explotar una política que ya conocemos. [Referencia de selección](https://proceedings.mlr.press/v49/russo16.html).

La clasificación oficial combina la media de tres partidas con calidad de Skills y eficiencia; sólo el top diez recibe revisión experta. Optimizar `μ` es un componente del trabajo, no una sustitución de toda la evaluación. No utilizamos `competition_partial_score` como si fuera el resultado bruto ni recuperamos una función oculta de dimensiones. [Reglas oficiales](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html).

## 2. Valor de una política frente a potencial de una familia

Para una familia `F`, el potencial ideal sería `M_F = sup_{p ∈ F} μ_p,objetivo,e`. Un ancestro `p ∈ F` sólo informa directamente sobre `μ_p`; puede tener descendientes muy distintos. No existe en general la implicación `μ_p bajo ⇒ M_F bajo`.

HOO/StoSOO usan particiones y regularidad del espacio para hacer eficiente una búsqueda jerárquica. BAST permite ciertos cortes con hipótesis de suavidad del árbol. No hemos demostrado una métrica que haga suaves las mutaciones de instrucciones: un cambio pequeño de texto puede cambiar completamente una decisión.

Por tanto, la **banda estadística de un candidato fijo** y el **índice heurístico de interés de una familia** deben tener nombres y campos diferentes. Una cota sobre la media del padre no certifica que un subárbol desconocido sea malo. [HOO](https://www.jmlr.org/papers/v12/bubeck11a.html), [StoSOO](https://proceedings.mlr.press/v28/valko13.html), [BAST](https://arxiv.org/abs/cs/0703062).

Un índice práctico de búsqueda puede combinar mejor descendiente confirmado, incertidumbre sobre nuevos cambios, diversidad y coste. Eso es una propuesta heurística que hay que comparar; no lo llamaremos límite superior válido del óptimo de la familia.

## 3. Por qué no copiar directamente el máximo observado

Un nodo probado una vez puede obtener una nota alta por azar. Buscar miles de nodos y conservar el mayor resultado selecciona tanto calidad como suerte. El máximo es especialmente engañoso si unas políticas tienen mayor varianza o más repeticiones que otras.

Separaremos:

- Resultado de cada episodio: dato original.
- Estimación de media de una política: todas sus muestras comparables.
- Mejor puntuación observada: diagnóstico, no estimador de rendimiento esperado.
- Mejor descendiente confirmado de una familia: guía de búsqueda, con su propia evidencia.

MCTS-AHD usa respaldo por máximo de hijos en su escenario de diseño de heurísticas. Nuestra adaptación debe tratar explícitamente el ruido por episodio en vez de interpretar ese respaldo como una garantía sobre políticas del juego. [Método original](https://proceedings.mlr.press/v267/zheng25o.html).

## 4. Réplicas y bandas que toleran mirar repetidamente

Para una política fija, supongamos episodios independientes, distribución estable y una media bien definida. Con puntuaciones normalizadas en `[0,1]`, una construcción conservadora por Hoeffding y unión sobre tamaños de muestra usa:

`b_i(n) = sqrt(log(π² n² / (3 δ_i)) / (2n))`, para `n ≥ 1`.

El intervalo es `[max(0, mean_i − b_i), min(1, mean_i + b_i)]`. Para cada `n`, la probabilidad de exceder esa anchura está acotada por `6 δ_i / (π² n²)`; al sumar sobre `n`, el error total no supera `δ_i`.

Si se incorporan candidatas sucesivamente, una posible asignación es `δ_i = 6 δ / (π² i²)`, por lo que la suma de presupuestos de error no supera `δ`. Las políticas adaptativamente propuestas pueden analizarse con datos futuros nuevos bajo las condiciones apropiadas; reciclar los datos que llevaron a proponerlas como si fueran confirmación independiente no sirve.

Es una derivación ilustrativa, no la implementación más eficiente. Las bandas pueden ser tan anchas con pocas muestras que no eliminen ninguna candidata. Las secuencias de confianza empíricas de Bernstein o basadas en mezclas pueden ser más útiles, pero sus supuestos y cómputo deben respetarse. [Howard y colaboradores](https://doi.org/10.1214/20-AOS1991).

Regla conservadora de dormancia de una política fija: su cota superior queda por debajo de la cota inferior de una contendiente, con una tolerancia de mejora práctica prefijada si procede. Eso no descarta sus descendientes ni resuelve incertidumbre sobre otro actor.

## 5. Decidir entre generar, repetir y validar

Una forma idealizada de valorar una consulta `q = (política, modelo, lote)` es su valor esperado de información para la selección:

`VOI(q) = E_Dnuevo[max_p E(μ_p,objetivo | D, Dnuevo)] − max_p E(μ_p,objetivo | D)`.

Dividir por el coste esperado permite comparar consultas caras y baratas. Esta expresión depende de un modelo probabilístico de la información y de las políticas consideradas; es una decisión de un paso, no la solución exacta del problema completo de investigación.

La generación de un descendiente requiere además modelar qué candidatos puede producir el operador de mutación. No es equivalente a repetir una media conocida. AB-MCTS explicita la opción de generar nuevos hijos; la selección bayesiana es una alternativa útil a imponer un número fijo de hermanos. [AB-MCTS](https://arxiv.org/abs/2503.04412), [múltiples fuentes de información](https://arxiv.org/abs/1603.00389).

Como versión inicial interpretable:

1. Si no está validada la fuente barata para esta familia, medir primero en el objetivo.
2. Si dos candidatas relevantes siguen ambiguas, darles réplicas comparables.
3. Si domina la incertidumbre sobre ideas nuevas y la familia tiene capacidad de expansión, generar un cambio.
4. Si vence el turno del archivo o aparece una hipótesis nueva, reabrir.
5. Si una candidata promete una mejora útil, reservar datos nuevos para confirmarla.

Es una política de laboratorio propuesta y auditable. Su evaluación debe competir contra alternativas más sencillas, no tomar “adaptativo” como sinónimo de mejor.

## 6. Reapertura y probabilidad de olvido

Podemos seleccionar trabajo con una mezcla:

`P_t(v) = (1 − ε_t) P_activo,t(v) + ε_t P_archivo,t(v)`.

El archivo puede priorizar antigüedad, incertidumbre y diversidad, además de incluir una componente aleatoria. Para que un nodo fijo no desaparezca para siempre, no basta con que su probabilidad sea positiva una vez: las oportunidades acumuladas deben ser suficientes.

Por ejemplo, si `ε_t = 1/t` y el archivo tiene aproximadamente `t` nodos, la probabilidad asignada a una rama concreta es del orden de `1/t²`; su suma es finita y no garantiza una revisión futura. Una cola justa o revisiones periódicas por antigüedad evita que “exploración decreciente” se convierta en olvido permanente. Un archivo que crece sin límite tampoco puede recibir revisión frecuente para todos sus elementos con presupuesto finito.

La cuota del archivo es un hiperparámetro a ensayar. MAP-Elites aporta una razón para conservar nichos distintos; no establece por sí mismo la frecuencia óptima de resurrección para este juego. [Archivo de élites](https://arxiv.org/abs/1504.04909).

## 7. Fidelidad entre actores: sesgo, no sólo ruido

La medida barata y la medida objetivo son funciones diferentes:

`μ_i,Haiku ≠ μ_i,objetivo` en general.

Un modelo provisional podría escribir `μ_objetivo(p) = a_m(x_p) + b_m(x_p) μ_m(p) + residual`, donde `x_p` describe la familia y complejidad. Es una hipótesis de calibración, no una relación conocida. Estimarla exige políticas compartidas entre actores, suficientes episodios y validación en familias nuevas.

No se debe promediar una partida Haiku de 80 y una del objetivo de 40 para concluir que la política vale 60. Tampoco confundir una mala ejecución por el trabajador con un mal procedimiento. La fidelidad puede variar precisamente en las candidatas más especializadas o largas.

La investigación sobre fuentes no fiables muestra que una fuente barata mal relacionada puede empeorar el coste de optimización; la de fidelidad dependiente de la entrada explica por qué un coeficiente global no basta. [rMFBO](https://arxiv.org/abs/2210.13937), [iMFBO](https://proceedings.mlr.press/v244/fan24a.html).

Diagnósticos de calibración:

- Acuerdo de ranking entre medias por política, con incertidumbre.
- Capacidad de recuperar las mejores candidatas del objetivo, no sólo correlación global.
- Tasa de falsos descartes detectada mediante auditoría aleatoria de rechazadas.
- Errores de seguimiento, acciones inválidas, omisión de avisos y sensibilidad a complejidad.
- Cambio de relación al pasar de familias generales a especialistas.

Si el acuerdo es insuficiente, usar el trabajador barato para tareas acotadas o exploración no concluyente, sin concederle poder de poda sobre el objetivo.

## 8. Poblaciones, productividad y ruido

Un planificador de islas puede usar la mejora reciente por coste para repartir esfuerzo. Sin embargo, `max(resultado_nuevo − mejor_anterior, 0)` es positivo por selección incluso sin una mejora real cuando hay ruido. Las mejoras de una isla inicialmente mala tampoco deben contar automáticamente más que avances valiosos cerca del líder.

La propuesta es calcular productividad sobre mejoras que superan un filtro de incertidumbre o confirmación y conservar un registro de éxitos aparentes que luego desaparecen. El tiempo desde el último avance puede activar nuevos operadores o familias, pero no prueba que la actual región esté agotada.

PBT/PB2 se refieren a poblaciones de procesos de entrenamiento con herencia de pesos y configuración; aquí podemos heredar **artefactos de política**, no copiar estados ocultos del juego. [PBT](https://arxiv.org/abs/1711.09846), [PB2](https://arxiv.org/abs/2002.02518).

## 9. Beneficios tardíos y recursos de evaluación

Hyperband, ASHA y BOHB son útiles para asignar recursos gradualmente, pero un recurso barato sólo ayuda si informa del objetivo. El número de episodios completos es una escala más defendible que truncar cada episodio antes de que aparezcan beneficios tardíos. [Hyperband](https://jmlr.org/papers/v18/16-558.html), [ASHA](https://arxiv.org/abs/1810.05934), [BOHB](https://proceedings.mlr.press/v80/falkner18a.html).

No afirmaríamos que un proxy de bienestar o progreso del mes 8 predice la puntuación de 48 meses sin medir ese vínculo. Una política que aprende primero y produce después puede perder en el proxy y ganar al final. Una que sobrevive con poco progreso puede hacer lo contrario.

Los episodios se ejecutan hasta final real o se registran como incompletos por una causa operativa. No se imputa una nota terminal a un episodio interrumpido ni se excluye silenciosamente una salida temprana legítima.

## 10. Asincronía y observaciones pendientes

Las partidas malas pueden acabar rápido y las exitosas tardar más. Si las decisiones del orquestador usan sólo las primeras respuestas recibidas, el tiempo de observación selecciona el tipo de resultado. La presencia de una tarea pendiente tampoco es evidencia de fracaso.

Mantendremos contadores distintos de lanzamientos, tareas pendientes, episodios terminales y fallos operativos. El número de pendientes puede reducir temporalmente la prioridad de asignar más trabajo idéntico; **no entra como una observación numérica** en el cálculo de media o incertidumbre.

PCTS estudia evaluaciones retrasadas y ruidosas en optimización jerárquica. Sus garantías no cubren sin más todos los retrasos dependientes del resultado, así que la versión inicial debería usar rondas comparables o decisiones que registren claramente qué resultados faltan. [Procrastinated Tree Search](https://doi.org/10.1609/aaai.v36i9.21280).

## 11. Modos de política y especialización por contexto

Una opción puede describirse como `o = (I_o, π_o, β_o)`: condición de inicio, procedimiento de acción y condición de finalización. Un selector elige un modo según el historial público; las acciones siguen siendo las alternativas realmente ofrecidas.

Esto permite probar una política con recuperación temporal, otra con énfasis en entrega y otra que cambia según evaluaciones o compromisos, sin identificar un mes como una ley del motor. También debemos evitar que el selector cambie de modo continuamente por señales mínimas; la estabilidad del cambio forma parte de la política que medimos. [Opciones](https://all.cs.umass.edu/pubs/1999/sutton_ps_AI99.pdf).

La complejidad tiene un coste: más reglas, más contradicciones y peor seguimiento por un actor pequeño. Podemos comparar una frontera entre puntuación, coste, complejidad y fiabilidad o usar una penalización de diseño previamente elegida. Esa penalización es nuestra preferencia de investigación, no la puntuación oficial.

## 12. Sesgo al condicionar en llegar al mes 8

Sea `T` la duración del episodio. El resultado completo puede descomponerse como:

`E[Q] = P(T ≥ 8) E[Q | T ≥ 8] + P(T < 8) E[Q | T < 8]`.

Si sólo comparamos `E[Q | T ≥ 8]`, ignoramos la probabilidad de llegar y los estados que cada política produce. No es una comparación del rendimiento global. Las diferentes causas terminales también compiten: morir pronto por salud impide observar riesgos tardíos.

Un estudio de continuaciones debe especificar un prefijo común y una asignación de alternativas que no altere lo anterior al punto de cambio; si no se puede asegurar eso, la comparación válida es la de políticas completas aleatorizadas desde el inicio. Sin clonación o semillas públicas no reclamaremos pares de estados idénticos.

## 13. Qué significaría converger

Para un conjunto finito y estable, réplicas suficientes y un muestreo adecuado pueden identificar diferencias de medias. Para un árbol infinito de políticas generadas, no conocemos toda la función ni una cobertura garantizada del espacio: la búsqueda depende de los operadores, la representación y el presupuesto.

La optimización bayesiana de parámetros pequeños puede ser útil cuando definimos un espacio numérico coherente. TuRBO no convierte un espacio arbitrario de prompts en uno suave. [TuRBO](https://arxiv.org/abs/1910.01739).

Las garantías de un componente no se suman para producir un teorema del sistema completo. Nuestra afirmación verificable será más modesta: bajo un presupuesto y protocolo fijados, esta combinación obtuvo o no una mejora frente a baselines concretos. Ninguna cantidad de muestras del dev elimina automáticamente el cambio de distribución del test.
