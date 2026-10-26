# Plan maestro: estrategias muy distintas, sección a sección

Escrito el 26 oct 2026, hacia las 23:45 UTC, a petición de Alejandro. Quiere dejar de probar planes generales, que acaban todos en la misma nota, y probar caminos muy distintos, a mano y de uno en uno, dividiendo el juego en partes. Este documento es el mapa; el chat "laboratorio por secciones" lo ejecuta y lo va corrigiendo con lo que aprenda.

## 0. ¿Dividir el juego en secciones? Sí, y por qué

**Por qué los planes generales no avanzan.** La nota de una partida es la suma de varios problemas distintos: sobrevivir al primer año, subir de nivel, ganar dinero y llegar bien al final. Un plan general es un término medio entre todos ellos, y además lo medimos con la partida entera, donde el azar mueve unos 19 puntos. Por eso todos acaban entre 53 y 56.

**Lo que gana una sección:**
- **Un objetivo claro.** Por ejemplo, "llegar a la primera evaluación con habilidad, red y resultados en su máximo".
- **Una medida rápida y con menos azar.** "¿Ascendió en la primera evaluación?" se sabe en el mes 6, no en el 48. Además, la partida corta cuesta unas 8 veces menos.
- **Efectos grandes.** En el estudio de Matteo, ascienden el 55–69 % de quienes llegan a la evaluación con todo en su máximo, frente al 0–3,5 % del resto. Una diferencia así se ve con 20–30 partidas; una de 3 puntos en la nota final necesitaría cientos.

**La división que propongo.**
- **Eje principal: el tiempo.** El juego tiene un ritmo de 6 meses (evaluación y ventana de ascenso) y una evaluación final aparte.
- **Dentro de cada sección, tres canales de decisión:** los eventos (de donde sale la mayor parte del crecimiento), el reparto de energía al final de cada trimestre y la acción principal del trimestre.
- **Reglas fijas que valen para todas las secciones:** salud, dignidad, riesgo oculto, y red y dinero por encima de cero.

**Límites, y cómo cubrirlos.**
- Las secciones se tocan: apretar al principio puede dejar riesgo para después.
- No se puede empezar una partida a mitad. Para probar la sección 2 hay que jugar antes la 1 con su mejor plan.
- Por eso, al final, los ganadores de cada sección se juntan en un manual y se comprueba con partidas completas.

**¿Esperamos a las simulaciones brutas?** Sólo en parte. La sección del cierre (S5) se apoya en algo que ya sabemos con exactitud, cómo se calcula la nota final, así que puede empezar ya. Las secciones del principio y del medio (S1–S4) dependen de la mecánica que está estudiando ese chat; se afinan cuando llegue su informe (preguntas en la sección 6).

## 1. Lo que sabemos de la mecánica

| Hecho | Evidencia | Qué implica |
|---|---|---|
| **Nota final = 30 % nivel + 20 % riqueza + 15 % salud y dignidad + 15 % habilidad + 10 % control de riesgo + 10 % red**, cada dimensión de 0 a 100 | Ajuste exacto sobre 556 partidas (error máximo 0,01) | Cada nivel vale 3 puntos (L5 = 50 en la dimensión de nivel). **No se puede escribir en un Skill** porque es una fórmula no publicada; sirve para decidir qué investigar |
| En las partidas terminadas, la mediana es: control de riesgo 80 (una de cada cuatro, 50 o menos), red 60, habilidad 81. El 36 % acaba en L4 | 211 partidas terminadas | Subir riesgo, red y habilidad hasta el nivel de las mejores partidas daría **+7,8 puntos por partida terminada**, y llevar a L5 las que acaban en L4, +1 de media. Es la palanca más clara del juego en partidas que ya terminan |
| Se asciende si habilidad, red y resultados están en el máximo del nivel **en el momento** de la evaluación | Bots de Matteo: 55 % frente a 3,5 %; Haiku: 9 de 13 frente a 0 de 11 | Hay que mantener las tres en su máximo antes de cada evaluación, no sólo alcanzarlas una vez |
| La evaluación se aplica **al principio** de su mes, antes de los eventos y del reparto de ese mes | 2.511 de 2.511 primeras evaluaciones | Antes de la primera evaluación sólo hay un reparto trimestral. El resto lo deciden los eventos |
| La primera evaluación es siempre C | 1.940 de 1.940 | El primer ascenso no depende de la nota, sino de estar en el máximo |
| Quien no asciende en el primer año no termina | 0 de 13 que no habían ascendido en la segunda evaluación terminaron | El primer año decide unos dos tercios de lo que varía la nota |
| Unas 9 de cada 10 subidas salen de los eventos, y Haiku elige igual en cada evento sea cual sea el manual | v1 de Matteo; diagnósticos de la nube | Un plan que no cambie las elecciones en los eventos apenas cambia el juego |
| Los bots que llegaron al nivel 6 ascendieron en las tres primeras evaluaciones | 4 de 400 bots | Encadenar ascensos al principio es lo que lleva más alto |
| La riqueza sube con el nivel (L4: 31; L5: 40) y con las notas de evaluación (bonus de 0,25 a 3 veces el salario) | Registro y reglas publicadas | La riqueza depende sobre todo de subir de nivel |
| 132 eventos distintos, en orden aleatorio, el 44 % encadenados. La evaluación oficial usa otros eventos | Estudio de Matteo y reglas oficiales | Nada de respuestas por evento: hay que guiarse por señales que se ven en la partida |

## 2. Qué premian y qué castigan los organizadores

Leyendo sus reglas, su rúbrica y su forma de puntuar:

- **Premian:**
  - decidir con el estado y la información de la partida;
  - responder a los avisos;
  - el equilibrio a largo plazo;
  - preparar las ventanas de ascenso y mirar los 48 meses;
  - elegir opciones éticas (los atajos alimentan el riesgo oculto);
  - que el manual siga sirviendo si cambian los eventos o los parámetros.
- **Castigan:** maximizar una sola cosa, ignorar avisos, reglas rígidas o respuestas fijas a eventos, números no publicados y Skills vagos.
- **Pistas de diseño:**
  - Dicen que el ascenso premia "resultados sostenidos" y no un pico.
  - La salud y la dignidad pesan un 15 % en la nota final, y el control de riesgo un 10 %.
  - Hay una herramienta de registros (`check_latest_logs`) que casi no usamos.
  - El manual del juego se puede leer durante la partida.
- **Consecuencia para los planes:** apoyarse en señales que el jugador ve, como un valor que ha dejado de subir (señal de que está en su máximo), los avisos de RR. HH., del jefe o del médico, o las notas de evaluación. Nunca en los números de los eventos de desarrollo.

## 3. Secciones y planes

Cada sección tiene planes muy distintos entre sí. **A**, **B**, **C** y **D** no son variantes de lo mismo: atacan la sección por caminos diferentes.

### S5. Cierre: el último año y la evaluación final (se empieza por aquí)

- **Objetivo:** llegar al final con el máximo en las dimensiones de la nota.
- **Medida:** las dimensiones finales y la nota de las partidas terminadas.
- **Por qué primero:** se apoya en algo que conocemos exactamente, se puede probar gratis con bots, se suma a cualquier manual y su efecto esperado es de **+4 a +8 puntos** por partida terminada.

| Plan | Idea | Hipótesis |
|---|---|---|
| **S5-A Limpieza final** | En los últimos trimestres: limpiar el riesgo (Defuse) y cuidar la red con la energía; como acción principal, rotación o mentoría (habilidad y red); ninguna opción de evento que añada riesgo; salud y dignidad en la mitad alta | El control de riesgo, la red y la habilidad se quedan cortos porque nadie prepara el final |
| **S5-B Último ascenso** | Mantener habilidad, red y resultados en su máximo para la última ventana de ascenso; la limpieza, sólo en el último trimestre | Un nivel más vale 3 puntos, más que casi cualquier limpieza |
| **S5-C Equilibrio final** | En cada reparto del último año, la energía va a la dimensión más lejos de su mejor valor visto: riesgo si hubo avisos, red si ha bajado, habilidad si aún sube | Repartir según la carencia de cada partida rinde más que una receta fija |

### S1. Apertura: hasta la primera evaluación (los 5 primeros meses)

- **Objetivo:** llegar a la primera evaluación con habilidad, red y resultados en su máximo, sin dañar la salud ni acumular riesgo.
- **Medida:** porcentaje que está en el máximo y porcentaje que asciende en la primera evaluación (hoy, alrededor del 37 %). Se mide con partidas cortas de 6 meses.

| Plan | Idea | Hipótesis |
|---|---|---|
| **S1-A Guardián de eventos** | Procedimiento explícito para cada evento: ver qué entrada no está en su máximo y elegir la opción que más la sube; en los meses antes de una evaluación, rechazar cualquier opción que pueda bajar la red o los resultados, aunque cueste algo de salud, dignidad o dinero | La mayoría no asciende porque pierde un punto de red o resultados justo antes de la evaluación (11 de 15 casos en Haiku) |
| **S1-B Rutina de los bots de nivel 6** | Cada trimestre, un punto de salud, preparar informes y cuidar la red; acción principal siempre "proyecto clave"; en los eventos, quedarse con lo que suponga hacerse cargo del trabajo | Una rutina simple y constante, que nunca pierde salud, llega igual de lejos que una lista de reglas |
| **S1-C Contabilidad con registros** | Tras cada evento, leer `check_latest_logs` y anotar en las notas el mejor valor de cada entrada en este nivel; si una baja, recuperarla enseguida | El jugador no se da cuenta de que ha perdido un punto; los registros y las notas se lo muestran |
| **S1-D Apertura agresiva** | Gastar salud en crecer al principio (aprender, trabajo intenso) y recuperarla justo después de la evaluación | Llegar al máximo pronto deja margen para mantenerlo; hay que ver si la salud aguanta |

### S2. Escalada temprana: segunda y tercera evaluación

- **Objetivo:** ascender en cada evaluación, como los bots que llegaron al nivel 6.
- **Medida:** nivel en el mes 18 (partidas cortas de 18 meses).

| Plan | Idea | Hipótesis |
|---|---|---|
| **S2-A Ciclo repetido** | Cada semestre es una apertura nueva con el máximo del nivel nuevo, que se reconoce porque los valores dejan de subir | El mismo mecanismo vale en cada nivel |
| **S2-B Acelerador** | Crecer con trabajo intenso y aprendizaje cuando la salud está en la mitad alta; usar cada evaluación para recuperar | En niveles altos los eventos no bastan para llegar al máximo a tiempo |
| **S2-C Nota alta** | Buscar notas A o S con resultados visibles (informes, mostrar resultados) | La nota y el ascenso comparten entradas, y una nota alta además da dinero |

### S3. Salvavidas: si no se asciende en la primera evaluación

- **Objetivo:** que no te despidan al final del segundo año.
- **Medida:** sobrevivir más allá del mes 24 cuando no se ascendió en la primera evaluación.

| Plan | Idea | Hipótesis |
|---|---|---|
| **S3-A Todo a lo que falta** | Tras no ascender, poner todos los canales en la entrada que no estaba en su máximo hasta conseguir el ascenso | El fallo es concreto y se puede corregir |
| **S3-B Rendimiento y riesgo** | Tras una nota C o D, resultados visibles primero y limpiar el riesgo (las D vienen con avisos de riesgo: 37 de 37) | Las notas muy bajas que llevan al despido nacen del riesgo acumulado |

### S4. Crecimiento medio: del mes 18 al 41

- **Objetivo:** pasar del nivel 5 y sumar riqueza.
- **Medida:** nivel en el mes 42 y dimensión de riqueza.

| Plan | Idea | Hipótesis |
|---|---|---|
| **S4-A Máximo por ciclo** | Seguir con el ciclo de S2-A | Igual que S2-A |
| **S4-B Riqueza** | Pedir condiciones concretas cuando haya ofertas de sueldo o de puesto, evitar opciones que cuesten dinero y buscar notas altas | La riqueza se queda corta también por las elecciones en los eventos |
| **S4-C Cuello de botella en niveles altos** | Concentrar la energía en la entrada más lejos de su máximo | En v4 falló en el nivel 1, pero puede funcionar más arriba, donde los máximos crecen |

### Planes globales muy distintos (comodines, en paralelo si hay cuota)

| Plan | Idea | Para qué sirve |
|---|---|---|
| **G1 Minimalista** | Un manual de 150 palabras como mucho: sólo las reglas fijas y "todo en su máximo antes de cada evaluación" | Ver si sobran instrucciones. Gasta pocos tokens y quizá le va mejor a DeepSeek |
| **G2 Fortaleza** | Terminar las 48 partidas es lo único que importa: nada de riesgo, salud y dignidad altas, limpiar el riesgo con cada aviso | Marca el techo de la fiabilidad |
| **G3 Lector de señales** | Leer el manual del juego al empezar, los registros tras cada evaluación y los avisos, y usar las notas como memoria | Es lo que parecen querer los organizadores, y DeepSeek juega con contextos muy largos |
| **G4 Procedimiento único** | Un mismo procedimiento sin números para todas las decisiones, con prioridades que cambian según la fase | Un manual fácil de seguir que además puntúa bien en la rúbrica |

## 4. Cómo probar cada plan

1. **Primero lo gratis.** Si el plan es sobre todo de repartos trimestrales (S5, parte de S1), se prueba antes con bots sin IA. Ya existe la base de los bots de energía en `scripts/energy-bots/run.py`.
2. **Después, Haiku contra una referencia**, en el mismo chat y en las mismas condiciones:
   - para S1 y S2, partidas cortas (hay que construir la herramienta para cortarlas, primer trabajo del laboratorio);
   - para S5, partidas completas, mirando sólo las terminadas.
3. **Decidir con números:**
   - **Prometedor** si, con al menos 20–30 partidas por plan, la medida de su sección mejora de forma clara: por ejemplo, 15 puntos más de ascensos en la primera evaluación, o 3 puntos más de nota en las partidas terminadas para S5.
   - Si es prometedor, **a por él**: 2 o 3 mejoras seguidas sobre ese mismo plan.
   - Si no, se descarta, se apunta por qué y se pasa al siguiente.
   - Con 4 partidas no se decide nada.
4. **Juntar:** cuando haya ganadores de S5 y S1, se juntan en un manual con un Skill por sección. Eso también lo valora el jurado ("cómo se reparten las responsabilidades los Skills"). Se comprueba con 20–30 partidas completas y es candidato a las versiones 2 y 3.
5. **Todo se apunta:**
   - un informe por plan en `lab/reports/secciones/`;
   - lo aprendido, a `lab/fastloop/lessons.md`;
   - este plan maestro se actualiza con cada decisión.

**Orden propuesto:** S5 → S1 (cuando llegue el informe de las simulaciones brutas) → S3 → S2 → S4 → juntar. Los comodines van en paralelo si hay cuota.

## 5. Chats en paralelo (como mucho 3 jugando partidas de Claude a la vez)

| Chat | Qué hace |
|---|---|
| **Laboratorio por secciones** (nuevo, T18) | Ejecuta este plan, de uno en uno |
| **Comodines** (opcional, T19) | Prueba G1–G4 contra la misma referencia |
| **Entregas** (T15) | La versión 1 de mañana. Si S5 sale bien a tiempo (antes de las 16:00 UK), puede añadirla |
| **Simulaciones brutas** (T17, en marcha) | Mecánica con bots, sin cuota |
| **Matteo** | Su línea de v7 (mecanismo del ascenso), que encaja con S1 y S2 |

## 6. Qué necesitamos de las simulaciones brutas

1. Confirmar cuándo se aplican las evaluaciones, los ascensos y los repartos en cada ciclo.
2. Los máximos de cada nivel, y cómo los reconoce un jugador durante la partida (qué señal ve).
3. Qué devuelve `check_latest_logs`: ¿los cambios de cada valor? ¿explica las evaluaciones?
4. Qué decide las notas B, A y S en niveles altos, y qué papel tiene la dignidad.
5. Cuántas evaluaciones malas llevan al despido y qué reinicia la cuenta.
6. Cómo se calculan al final el control de riesgo, la red y la habilidad: ¿estado final o historial? Prueba con bots: el mismo bot con y sin limpieza en el último año.
7. Qué mueve la dimensión de riqueza: sueldo, bonus, eventos.
8. Qué hace falta para pasar del nivel 5 y qué hicieron los bots que llegaron al 6.

## 7. Prompts para pegar

**Laboratorio por secciones (T18)**

```text
Lee ESTADO.md, research/careerlab/plan-maestro-secciones-2026-10-26.md (tu plan), research/careerlab/estrategia-primeros-principios-2026-10-26.md, research/careerlab/chats-independientes-2026-10-26.md, lab/fastloop/lessons.md y lab/reports/matteo-promotion-study.md.
Eres el laboratorio por secciones (T18). Trabajas a mano y de uno en uno con los planes del plan maestro. Rama alejandro/lab-secciones; origen de registro "secciones" (uv run careerlab origin set secciones). Como mucho 4 partidas a la vez (--slots 4) y --max-five-hour 0.65. Puedes usar subagentes para tareas acotadas, pero no diseñadores automáticos.
Paso 0, herramienta: añade a careerlab una forma de cortar una partida de Claude en un mes dado (por ejemplo, vigilando el stream del jugador y parándolo al pasar del mes N). Guarda el estado en ese momento: nivel, habilidad, red, resultados, salud, dignidad, si ascendió y la nota de cada evaluación. Que una partida cortada nunca cuente como terminada ni como eliminada. Con pruebas.
Paso 1, S5 (cierre):
- primero gratis, con bots (base: scripts/energy-bots/run.py): el mismo bot con y sin limpieza en el último año, y comparar riesgo, red y habilidad finales;
- si mueve las dimensiones, escribe S5-A, S5-B y S5-C como Skills que se añaden a un manual de referencia (f3-lean-v1 u observed-growth-v3) y juega partidas completas de Haiku hasta tener unas 15 terminadas por plan;
- compara la nota de las terminadas.
Paso 2, S1 (apertura), cuando el chat de simulaciones brutas haya publicado su informe (léelo y ajusta el plan con él): S1-A a S1-D, con partidas cortas de 6 meses, unas 30 por plan; la medida es el porcentaje en el máximo y ascendidos en la primera evaluación.
Después: S3, S2 y S4 en ese orden, y al final junta los ganadores en un manual con un Skill por sección.
Reglas para decidir: con 4 partidas no se decide nada. Si un plan mejora claramente la medida de su sección, profundiza en él con 2 o 3 mejoras seguidas. Si no, descártalo y apunta por qué.
Cumplimiento: en los Skills nada de eventos con nombre, meses concretos, umbrales ni fórmulas no publicadas. Apóyate en señales que se ven en la partida, como un valor que ha dejado de subir o los avisos. Pasa uv run careerlab lint.
Documenta: un informe por plan en lab/reports/secciones/<plan>.md con números y decisión; lo aprendido, en lab/fastloop/lessons.md; tu línea T18 de ESTADO.md; commit, push y PR cada vez que cierres una sección. Si algo de S5 sale bien antes de las 16:00 UK del 27 oct, avisa en tu línea de ESTADO.md para que el chat de entregas lo pueda usar.
```

**Comodines (T19, opcional, en paralelo)**

```text
Lee ESTADO.md, research/careerlab/plan-maestro-secciones-2026-10-26.md (sección "Planes globales muy distintos"), research/careerlab/chats-independientes-2026-10-26.md y lab/fastloop/lessons.md. Eres el chat de comodines (T19). Prueba de uno en uno G1 (minimalista), G2 (fortaleza), G3 (lector de señales) y G4 (procedimiento único), cada uno contra f3-lean-v1, en las mismas condiciones. Rama alejandro/comodines; origen de registro "comodines"; --slots 4; --max-five-hour 0.65.
Para cada plan: escríbelo (pasa uv run careerlab lint) y juega 12 partidas de Haiku del plan y 12 de la referencia. Si destaca en partidas terminadas, ascensos en el primer año o nota media con su error estándar, súbelo a 25 por lado; si no, descártalo. Nunca concluyas con 4 partidas.
Documenta cada plan en lab/reports/comodines/<plan>.md, actualiza tu línea T19 de ESTADO.md y abre una PR al cerrar cada plan.
```
