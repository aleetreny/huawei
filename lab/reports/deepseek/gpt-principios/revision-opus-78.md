# Revisión para 72+ frecuente y 78 automático

**Conclusión: la mejor apuesta sigue siendo corregir decisiones de historias que cuestan evaluaciones o acumulan riesgo innecesario; pero mi propuesta anterior sobrevaloraba un pequeño conjunto de errores locales y no exigía demostrar que las mejoras alcanzaran la distancia hasta 78. La calidad del Skill debe entrar en el objetivo desde el principio. No existe todavía una receta validada que garantice ese resultado.**

30 octubre 2026. Encargo vigente: [encargo-opus-78.md](encargo-opus-78.md). Sustituye los encargos de L6 y de 76. Sólo análisis de archivos existentes: ninguna API, llamada a DeepSeek, partida oficial, simulación de carreras ni cambio de manual. Rama `alejandro/gpt-principios`, main sincronizada en `b294ef6`. También revisado el commit posterior de Mejora `a340059` (29 oct, 23:14 UTC).

## 1. Definir bien lo que se quiere conseguir

Reglamento público local, `local-runs/official-runner/docs/competition-rules.rst`, sección Automated score: **A = 0,8 × juego medio + 0,1 × calidad + 0,1 × eficiencia media**. La evaluación de una versión usa tres carreras, incluidas las que terminan antes de tiempo. La calidad oficial de mv-4 no está disponible; los jueces sustitutos no la certifican.

Con eficiencia 100:

| Calidad supuesta | Juego medio necesario para A = 78 |
|---|---:|
| 73 | 75,875 |
| 80 | 75,000 |
| 90 | 73,750 |
| 100 | 72,500 |

**72 exactos de juego no bastan: incluso con los otros dos componentes perfectos dan 77,6.** Conseguir 72+ frecuentemente es un hito intermedio, no el criterio de éxito de 78. Ejemplo de objetivo con margen: media de juego 76, calidad 80 y eficiencia media 98 darían 78,6. Es una combinación objetivo, no una predicción ni tres resultados ya obtenidos.

Separar dos métricas: media incluyendo derrotas y frecuencia de Q≥72. Para interpretar «consistente», propongo como hito de investigación Q≥72 en al menos el 90 % de intentos; las interrupciones cuentan como incumplimientos, aunque su Q oficial quede desconocida. No borrar intentos sin nota ni inventarles una nota oficial. Un 90 % por carrera sólo da 72,9 % de tres éxitos seguidos bajo independencia. La pretensión de que casi todas las tandas sean buenas exige mayor fiabilidad.

Aquí interpreto «78 final» como nota automática. Si se refiere a la clasificación tras jurado, la regla es 0,7 × automático + 0,3 × jurado: por ejemplo, 76 automático y 82,67 de jurado dan aproximadamente 78. No mezclar esa ruta con subir Q a 78.

## 2. Qué dicen realmente los resultados actuales

Nueve intentos mv: ocho con nota, seis completos, dos derrotas y una interrupción técnica. Sólo uno de los ocho puntuados supera 72. Media de los puntuados 58,095; de los completos 68,12. Estas cifras mezclan mv-3 y mv-4 y no estiman con precisión el rendimiento de mv-4 por sí solo.

**Incluso escogiendo retrospectivamente las tres mejores carreras puntuadas para A, darían sólo 77,338 con calidad 100; con calidad 80, 75,338.** Es un cálculo descriptivo favorable, no un método válido de evaluación. Confirma que faltan más carreras altas, además de eliminar las malas.

Sensibilidad con derrotas de Q=28,02 y eficiencia 50, completas con eficiencia 100:

| Q media de completas | Calidad | A sin derrotas | Máxima tasa de derrota compatible con media A=78 |
|---|---:|---:|---:|
| 75 | 80 | 78,000 | 0 % |
| 75 | 90 | 79,000 | 2,35 % |
| 77,78 | 73 | 79,524 | 3,40 % |
| 77,78 | 80 | 80,224 | 4,96 % |
| 77,78 | 90 | 81,224 | 7,20 % |

Modelo ilustrativo: A = 0,8[(1−p)C+p·28,02]+0,1D+10−5p. No incorpora interrupciones técnicas ni describe toda la distribución. Una carrera de 63 completa también queda por debajo de 72: «no derrotas» y «72+ consistente» son objetivos distintos.

L6 importa, pero no resume el problema. Frente al 69,62 de mv-4, el 77,78 gana 3 puntos por nivel y 4,57 por riqueza. Sueldo, bonos y gasto contribuyen a riqueza. No atribuir todo el dinero al ascenso. Adelantar ventanas aumenta el horizonte de crecimiento; llegar a L6 al final no reconstruye automáticamente lo perdido antes. Tampoco se ha demostrado que L6 sea condición necesaria para Q≥72.

## 3. Auditoría nueva: qué fallaba en mi propuesta

Reproducible con `uv run --offline python scripts/deepseek/gpt_score78_audit.py`; salida [score78-audit.json](score78-audit.json). Usa catálogo empírico propio y trazas pagadas, no el interior del motor oficial.

### A. Los 16 casos dominados no justifican una estrategia de investigación entera

Confirmé en los resultados crudos que las 16 acciones fueron aceptadas. Abarcan ocho títulos y ocho intentos, pero **siete repiten un mismo nodo y ya eligen una acción que reduce riesgo**: la alternativa lo reduce más, y a veces ofrece Skill adicional. Una reducción nominal puede no valer nada si el riesgo ya era cero; la observación mensual no establece el contador dentro del mes. Sólo seis de las 16 elecciones añaden riesgo y sólo cuatro están en los dos meses previos a evaluación.

Doce admiten alternativa con la misma continuación catalogada y alguna ventaja visible tras recortar al techo, o reducción nominal adicional de riesgo. Cuatro cambian de continuación. Esto mejora el diagnóstico local, pero **no cuantifica puntos de carrera recuperables**. Las cifras se solapan; no sumarlas.

Retiro la prioridad automática «primero los 16». Son comprobaciones útiles para detectar confusiones, no el mapa principal de pérdida de puntuación. El mapa debe agruparse por tramo entre evaluaciones y explicar el coste futuro de la decisión.

### B. La réplica predice bastante bien mv, pero no convierte una hipótesis textual en efecto causal

Evalué los dos modelos de elección guardados, sin reajustarlos: el de la familia completa y el de v4. Su conjunto de ajuste excluye mv-3/mv-4. La evaluación comparte títulos y etiquetas históricas con la investigación anterior; no es una prueba de generalización a relatos nuevos.

| Subconjunto | Registros | Acierto modelo de familia | Acierto modelo v4 |
|---|---:|---:|---:|
| Todos los emparejados | 1.050 | 86,9 % | 86,5 % |
| Último mes de L1 antes de evaluación | 47 | 76,6 % | 78,7 % |
| Todas las opciones con riesgo positivo | 51 | 76,5 % | 74,5 % |
| HR adverso | 106 | 83,0 % | 81,1 % |

Se emparejaron 1.050 de 1.056 registros. En 1.045 emparejados también se identificó un único resultado crudo con `success=true`; cinco no se reconciliaron mediante esa clave y no se clasifican como rechazos. Restringiendo a los 1.045, v4 conserva 86,5 % de acierto. Las 16 dominadas están verificadas individualmente. Los registros de una historia/carrera no son ensayos independientes.

El modelo v4 asigna una suma de probabilidades de 107,8 elecciones con riesgo positivo frente a 114 observadas: no hay evidencia aquí de un desajuste global enorme. Sin embargo, acertar elecciones frecuentes no valida las probabilidades de colas ni el efecto de introducir otra frase. Además, utiliza efectos verdaderos del catálogo como predictores: es una herramienta de investigación con información privilegiada, no un lector entregable. Simular que detecta más pérdidas no demuestra cómo conseguirlo con texto.

### C. Evitar dos nuevos callejones

- El commit de Mejora `a340059` añade `EndBot/endhd`; su mensaje declara +0,1 al priorizar salud/dignidad al final. El commit no incorpora una tabla nueva de resultados, por lo que no lo trato como estimación verificada de precisión conocida. Junto al beneficio previo de cierre de Mecánicas emergentes (+0,55 en su propio contexto), desaconseja vender el último trimestre como salto principal. Los dos experimentos no son la misma intervención ni tienen la misma base.
- El 74,4 del planificador de Exploración es una referencia con información perfecta, **no un máximo demostrado**. Ni autoriza a declarar imposible 78 ni a esperar que un manual corto replique sus decisiones. Con Q=74,4 y eficiencia 100 haría falta calidad 84,8 para A=78.

### D. Calidad no puede quedar como un retoque para el final

Con eficiencia saturada, cada +10 de calidad vale +1 de A. La referencia anterior de «calidad secundaria» era insuficiente para este objetivo. Debe medirse desde el comienzo, en una variante separada, sin sacrificar juego. A la vez, apuntar a calidad 90 no hace que sea alcanzable: los jueces actuales no son el juez oficial y discrepan entre sí. Un aumento aparente de 10 en un juez que reduce Q en 2 pierde 0,6 de A.

## 4. Qué seguiría probando, en orden

### 1. Recuperar ventanas perdidas por lectura, no rehacer el trimestre

La primera apuesta es la **interpretación de costes de tiempo, crédito y relaciones en las historias cercanas a evaluación**, junto a falsas alarmas de riesgo que expulsan alternativas válidas. Es la vía con señal textual directa en el banco mv, aunque éste se reutilizó para elegir entre nueve variantes y su mejora puede estar sobreestimada.

El siguiente trabajo debe reconstruir por cada evaluación fallida: estado antes de la última decisión, estado que llega al examen, indicador que faltó, cuándo se perdió y alternativas disponibles. El CSV guarda estado preacción y omite acciones posteriores de trimestres agrupados; hay que usar las trazas crudas. No hace falta otra exploración global de miles de variantes.

Empezar por L1, pero **no encerrar la investigación allí**. La referencia calibrada anterior sitúa +4,8 al sustituir historias de las dos ventanas previas de L1 por decisiones privilegiadas y +8,2 al hacerlo en todos los niveles. Esas cifras no se suman ni se transfieren a mv-4. Muestran por qué interesa extender el diagnóstico a L2/L3 antes de volver a apostar sólo por acelerar Skill en L4. La regla actual de protección ya existe; la novedad tendría que ser leer correctamente una clase de costes, no repetir la orden.

### 2. Riesgo antes de que impida crecer, con sus intercambios explícitos

La segunda apuesta es encontrar elecciones que **añaden riesgo sin comprar una ventaja suficiente**, antes del comentario adverso y antes de una explosión. Comparar el crecimiento ganado con los turnos de recuperación, la ventana sacrificada y el daño posterior. Medir también elegir más riesgo del mínimo en menús malos. No considerar error cualquier riesgo positivo: en algunos menús no hay alternativa limpia, y en otros protege una evaluación.

Dos controles imprescindibles: falsas alarmas que expulsan una solución válida; pérdidas forzosas de N/O cuyo único reemplazo es riesgo alto. El caso anónimo del mes 26 ya está corregido: +1 frente a +2, no ejemplo probado de incumplimiento. Tampoco añadir otra regla de rescate L1 o de prudencia tras explosión si repite lo que el manual ya contiene o lo que Suelo/Comprobante ya probaron.

### 3. Calidad y economía de instrucciones, como variante separada

Conservar byte a byte el protocolo de llamadas, la línea de estado y la instrucción operativa del manifest. Probar quitar ambigüedades y duplicados estratégicos, haciendo que una excepción tenga el mismo alcance en el texto principal y en la tabla. No borrar salvaguardas para satisfacer a un juez ni convertir una aclaración documental en un cambio silencioso de estrategia.

Para puntuación, eficiencia 100 exige ≤500.000 tokens por mes sobrevivido; por debajo no hay bonus adicional. Para robustez puede fijarse un margen interno, por ejemplo ≤450.000 como objetivo de ingeniería, **sin afirmar que ya se cumple**. Medir tokens contabilizados por el runner, reanudaciones, llamadas por decisión y errores. No sustituir esas medidas por palabras del Skill o tokens de una única respuesta. Ninguna relectura/revisor adicional por defecto.

Estas tres prioridades no prometen sumar los puntos que faltan. Primero hay que medir cuánto recuperan conjuntamente y cuánto sobrevive cuando el lector sólo dispone de información permitida. Si la suma conjunta no alcanza el objetivo, se reconoce la brecha; no se sigue retocando sin una hipótesis nueva.

## 5. Un procedimiento que impida a Opus perderse

1. **Una tabla de pérdidas por ventanas**, no sólo ranking de decisiones. Separar lectura, prioridad, costes forzosos, crecimiento insuficiente y fallo técnico. Mantener también las completas bajas, no investigar únicamente las dos derrotas.
2. **Una estimación de potencial por mecanismo.** Usar continuaciones coherentes y condiciones de recuperación del estado. Cambiar de rama implica simular su propia continuación. Reutilizar el resto de una traza fija tras una elección distinta no es un contrafactual válido. Separar referencia privilegiada y variante que sólo ve lo observable. Una referencia heurística que no mejora no demuestra imposibilidad, pero sí puede quitar prioridad al mecanismo.
3. **Una corrección por candidato; como máximo dos candidatos estratégicos activos.** El límite controla la búsqueda, no es la tesis de que bastan dos frases. La calidad se compara por separado. Si no hay mecanismo repetido con coste relevante, no producir otro manual por obligación.
4. **Reserva por títulos e historias completas, control repetido y frecuencia natural.** Los ejemplos ya inspeccionados son desarrollo; no llamarlos reservado. Un banco enriquecido en errores sirve para detectar cambios, no para estimar mejora media. Para hacerlo, ponderar su frecuencia natural y medir también daños fuera del grupo tratado. No permitir que una nueva versión gane sólo por sobreajustar el banco de L1 reutilizado.
5. **Prueba final independiente de lo usado para seleccionar.** Fijar antes tamaño, métrica, criterio de abandono y margen tolerable de deterioro. Comparar coste de las equivocaciones, incertidumbre agrupada por historia/carrera, tasa Q≥72, derrotas, llamadas y tokens. Cuando proceda, evaluar también comportamiento en contexto e historial largo: ganar una decisión aislada no verifica obediencia durante 48 meses. No combinar dos correcciones antes de probar por separado y revisar su interacción.
6. **Declarar qué falta para hablar de consistencia.** Tres éxitos no certifican una tasa alta. Bajo ensayos independientes y política/proveedor estables, 29 intentos sin incumplimiento sitúan el límite superior unilateral del 95 % para su tasa por debajo del 10 %; 59, por debajo del 5 %. Sirve tanto para definir incumplimiento Q<72 como para fallos, si se fija de antemano. No es una orden para lanzar esas partidas ahora, ni sustituye estimar la media necesaria para 78. La selección repetida y los cambios de proveedor invalidan una lectura ingenua de esos límites.

La restricción actual impide demostrar transferencia con el modelo de competición: **sin DeepSeek**. Con archivos guardados y cálculo local sí se puede entregar un diagnóstico contrastable, un candidato mínimo si se justifica y un plan de confirmación. Las pruebas posteriores quedan pendientes; no se ejecutan ni se promete su resultado.

## Relevo

- **Hecho:** auditoría adversarial de las propuestas de L6/76; revisión del commit nuevo de Mejora; cuentas de objetivo 78; unión de decisiones con resultados aceptados; evaluación sin reajuste de los modelos guardados sobre mv; revisión de continuaciones de elecciones dominadas. No se ha enviado nada a otro chat.
- **Evidencia:** `score78-audit.json`, `mv-evidence.json`, informes Mejora/Exploración/Suelo/Techo/Mecánicas emergentes y reglamento público. Los nuevos archivos de salida sólo contienen agregados, sin narrativas ni respuestas del juego para el diseñador.
- **Límites:** cinco registros emparejados sin aceptación cruda reconciliada; alternativas valoradas sólo localmente; no se ha estimado ganancia causal nueva de carrera ni calidad oficial ni fiabilidad futura. El +0,1 de `endhd` sólo consta en el mensaje de commit revisado.
- **Reproducción:** `uv run --offline python scripts/deepseek/gpt_score78_audit.py > /tmp/score78-audit.json` y comparar con la salida guardada. Siguiente trabajo: seguir exclusivamente `encargo-opus-78.md`; los encargos anteriores son historia.
- **Cierre:** actualizar README y ESTADO, verificar salida y diff, commit/push en la rama propia y solicitar integración en main. No cambiar ni incluir los archivos ajenos modificados en el workspace.
- **Verificación realizada:** segunda ejecución con salida idéntica byte a byte, compilación del script, comprobaciones de cobertura/aceptación, cuentas de objetivo y `git diff --check`. No se requiere ejecutar partidas ni la batería de tests del motor para este análisis documental; no se modificó su código.
