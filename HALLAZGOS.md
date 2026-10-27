# Hallazgos, por importancia

Todo lo que sabemos del juego y de cómo hacer que la IA lo juegue bien, en un solo sitio. Actualizado el 27 oct 2026 a las 16:00 UTC con las tres líneas activas: **motor** (rama `main-1nddsg`), **categorías** (rama `alejandro/optimistic-gauss-edyw1j`) y **transmisión** (rama `alejandro/transmision`); a las 18:00 UTC, con la línea **palancas** (rama `alejandro/palancas`: B22, B23, C9, C10 y tres filas de X).

**Niveles**
- **A:** decide la nota y está confirmado con muchos datos.
- **B:** útil y confirmado.
- **C:** pista, sin confirmar.
- **X:** descartado con datos; no volver a probarlo sin una razón nueva.

**De qué sale cada fila** (etiqueta al principio):
- `Juego`: cómo funciona el juego. Vale para cualquier modelo.
- `Bot`: medido en el simulador con un bot. No dice si una IA lo hará.
- `Haiku`: medido con Haiku, nuestro sustituto. **No vale para DeepSeek hasta comprobarlo con él**; ya hay casos en que se porta distinto (C7, C3).
- `DeepSeek`: medido con DeepSeek, el modelo de la evaluación. Es lo que más cuenta para la entrega.
- `Programa`: cómo carga y guarda las cosas el programa oficial.
- `Método`: cómo medimos.

Cada hallazgo lleva su fuente. Nada de esta página entra en una Skill como número, umbral, título de evento ni respuesta fija: las normas lo prohíben aunque sea cierto ([NORMAS.md](NORMAS.md)).

## A. Deciden la nota

| # | Hallazgo | Fuente |
|---|---|---|
| A1 | `Juego` **La nota final es una fórmula fija:** nivel 30 %, dinero 20 %, salud + dignidad 15 %, habilidad 15 %, control de riesgo 10 %, red 10 %. El nivel y el dinero (que sale del sueldo, es decir, del nivel) separan una partida buena de una excelente. | motor, H11 |
| A2 | `Juego` **Ascender es casi automático.** Se asciende en la evaluación semestral si, justo antes, Skill, Network y Output están en el umbral del nivel, Dignity es 4 o más y la nota no es D (acierta el 99,5 %). En L1, Network y Output no tienen margen entre el umbral y el techo; Skill sí tiene un pequeño margen. Perder un punto del indicador que está justo en su mínimo puede costar el ascenso. | motor, M12, H2 |
| A3 | `Juego` **El riesgo oculto manda en las derrotas.** Cada respuesta suma o resta un número entero de riesgo que no se ve. El comentario mensual de RR. HH. lo muestra en 5 tonos (sonriente → enfadado). Al llegar a 5 explota (se pierde medio año de resultados, dinero y dignidad); la segunda explosión es el despido por crisis de confianza. En el simulador, la regla de riesgo vale 40–54 puntos. | motor, M10, M23 |
| A4 | `Juego` **Dos rutas frecuentes de derrota en nuestros bots:** no ascender nunca en L1 (despido en el mes 24) y la crisis de confianza. No son las únicas: también hay derrotas por salud y ruina. | motor H8; nube |
| A5 | `Juego + Haiku` **El margen está en las historias.** El mejor planificador medido saca 72,4 en el juego real (máximos observados ~80; no es una prueba de optimalidad); los manuales con IA sacan ~50. Casi todo lo que falta se decide en las respuestas a las historias, no en el reparto trimestral. | motor M17, M21; transmisión |
| A6 | `Haiku + DeepSeek` **Un cuello de botella demostrado de la IA es la percepción:** no sabe qué indicador sube o baja cada respuesta antes de elegir. Un bot que sólo ve el tipo de respuesta pierde 21 puntos frente al que ve los efectos; 14 de ellos por no saber qué indicador mueve. Haiku obedece la regla “no bajes Output antes de la evaluación”, pero no reconoce qué opción cuesta Output. | categorías §2; transmisión |
| A7 | `Haiku (DeepSeek parecido: B20, C3, C6)` **Dónde manda un manual y dónde está la nota no coinciden.** Las reglas del reparto trimestral se obedecen (60–93 % frente a 14–70 % sin manual) pero valen poco (menos de 1,5 puntos). Las reglas de historias valen mucho, se obedecen a medias y **contaminan las demás historias**: cambian 1 de cada 5 decisiones aunque no apliquen, y un manual así perdió 12–21 puntos en partidas. | transmisión ([resumen](lab/reports/transmision/resumen.md)) |

## B. Útiles y confirmados

**Sobre el juego**

| # | Hallazgo | Fuente |
|---|---|---|
| B1 | `Juego` El simulador `scripts/ingenieria-inversa/replica.py` reproduce el 99,3 % de los pasos, el 99,5 % de los ascensos y la nota con 0,3 puntos de error en partidas nuevas. Permite probar estrategias sin cuota. | motor M14, Fase 3 |
| B2 | `Juego` Cada respuesta tiene **siempre el mismo efecto**; las historias siguen siempre el mismo camino; no hay riesgo retardado; no hay eventos por nivel ni por estado. Los eventos se desbloquean por semestre. | motor M18, M27 |
| B3 | `Bot` **7 reglas generales** (sin números) sacan 68,1 en el simulador. Aguantan si cambian los parámetros: riesgo (R1), salud (R7), techo del nivel (R3) y limpieza final (R5). “Todo a Skill desde L4” no aporta. | motor M22, M23 |
| B4 | `Juego` **Charla de aviso en la evaluación:** depende de Dignity y Health frente al riesgo (regla exacta en M24). Llegar a la evaluación con Dignity alta y riesgo bajo la evita. | motor M24 |
| B5 | `Juego` Techos por nivel: lo que pasa del techo se pierde. Skill es el freno de los niveles altos. L7 es alcanzable por muy poco; L8+ no; la nota S no existe. | motor H1, H14, M16, Fase 3 |
| B6 | `Juego` Las pérdidas de dinero se multiplican con el nivel (×2 en L3–L4, ×3 en L5–L6); las ganancias no. | motor M13 |

**Sobre las respuestas a las historias**

| # | Hallazgo | Fuente |
|---|---|---|
| B7 | `Haiku` **10 tipos de respuesta** (arreglar, asumir, protegerse, escalar, venderse, evitar, ceder, empecinarse, atacar, ocultar), etiquetados a ciegas por Haiku, separan el riesgo: 78 % de acierto y el 92 % de las respuestas peligrosas detectadas. | categorías §2 |
| B8 | `Juego` **Señales de lenguaje.** Suben el riesgo aunque suenen bien: resolverlo en privado, arreglarlo a medias o más tarde. Lo bajan: dejarlo por escrito, arreglarlo entero, asumirlo en el momento. | categorías §2; motor M28 |
| B9 | `Haiku` Haiku ya elige casi siempre respuestas seguras (detonantes: 91 % bien sin manual; casi nunca gasta dinero con poco dinero). | transmisión; categorías |

**Sobre cómo escribir el manual (transmisión)**

| # | Hallazgo | Fuente |
|---|---|---|
| B10 | `Programa + Haiku (DeepSeek: B20)` En el programa oficial sólo el nombre y la descripción del Skill (y la instrucción del manifest) están siempre a la vista; el cuerpo se lee bajo demanda. Haiku lo lee siempre. El sitio de la regla no cambia la obediencia. | transmisión, [fase 0](lab/reports/transmision/fase0-carga-skills.md) |
| B11 | `Haiku` Se obedece lo imperativo, en orden de prioridad (“la primera línea que aplica gana”) y con condiciones **definidas por exclusión** (“todo comentario que no sea uno de estos dos suaves”). | transmisión, rondas |
| B12 | `Haiku (DeepSeek peor: C7)` **Un interruptor que la IA calcula y escribe** (“Review in N” en cada nota) aísla una regla de historias: la aplica sólo en su mes y el resto juega como sin manual. | transmisión, [rondas 8–10](lab/reports/transmision/ronda-8-10.md) |
| B13 | `Haiku` Un solo Skill: con varios, la IA abre sólo el que cree relevante y se pierden reglas. | transmisión, ronda A |
| B14 | `Método` Medir siempre los efectos secundarios: un bloque de historias al azar y la “huella” de las elecciones frente a un control repetido (que coincide consigo mismo un 96 %). | transmisión, [bloque general](lab/reports/transmision/bloque-general.md) |

**Cierre y fidelidad de la réplica (motor, investigación terminada).**

| # | Hallazgo | Fuente |
|---|---|---|
| B15 | `Bot` Planificar conjuntamente energía y acción principal tras la última evaluación mejora la ganancia de cierre en +0,552 Q (IC 95% [0,298; 0,805], 600 partidas oficiales aleatorizadas). El planificador dejaba energía útil sin usar y descartaba red que aún puntúa. La nota global sin ajustar no prueba un nuevo campeón; transferencia a Skill pendiente. | [Mecánicas emergentes §1](lab/reports/mecanicas-emergentes/README.md) |
| B16 | `Juego` La terminación liquida el mes 48 y deja estado en mes 49, con 48 nóminas. Ambos generadores de la réplica omitían esa transición. Confirmado en 1.156 completadas históricas y 568 nuevas; corrección con modo histórico explícito para reproducir experimentos. | [Mecánicas emergentes §2](lab/reports/mecanicas-emergentes/README.md) |

**Sobre DeepSeek (`deepseek-v4-flash`, con la clave de la competición)**

| # | Hallazgo | Fuente |
|---|---|---|
| B17 | `DeepSeek` **DeepSeek ve bien el riesgo y mal Skill y Output.** Leyendo sólo el texto de la opción, sin ayuda, detecta el 83 % de las respuestas que suben el riesgo oculto (90 % de las de +2 o más), pero sólo el 45 % de las que suben Skill y el 49 % de las que suben Output. Lee los 10 tipos mejor que Haiku. | deepseek, [percepción](lab/reports/deepseek/percepcion.md) |
| B18 | `DeepSeek` **Pistas de lectura generales mejoran su percepción y lo confirman los títulos reservados.** “Skill sube siempre que usas tu propio juicio (analizar, aportar datos, preparar, aprender, negociar con argumentos), también en temas de personas o dinero”, “Output baja cuando tu tiempo o tu mérito se van a otros” y las señales de riesgo de B8 más “quejarse de la empresa, su cultura o sus reglas, aunque sea por el canal formal”. Con ellas ve el 78 % de las subidas de Skill (antes 45 %) y el 86 % de los riesgos. | deepseek, [categorización](lab/reports/deepseek/categorizacion.md) |
| B19 | `DeepSeek + bot` **La mejor categorización para DeepSeek es leer cada opción como seis signos más el riesgo**, no los 10 tipos. Un bot que elige sólo con esa lectura de DeepSeek saca 56,0 en el simulador, frente a 46,7 con los tipos de Haiku y 67,7 el oráculo. Con etiquetas perfectas, esa lectura casi iguala al oráculo (67); las agrupaciones gruesas no pasan de 53–63. Una regla escrita por orden (descarta lo arriesgado, lo que baja Health o Dignity si están bajas y, antes de la evaluación, lo que baja Skill, Network u Output; después, lo que más sube los indicadores de crecimiento) saca 53,7. | deepseek, [categorización](lab/reports/deepseek/categorizacion.md) |
| B20 | `DeepSeek` **DeepSeek lee el Skill en el 100 % de las situaciones y obedece el reparto trimestral como Haiku** (con t13-final: Skill en L4 del 2 % al 65 %; comentario de RR. HH. del 15 % al 65 %). | deepseek, [obediencia](lab/reports/deepseek/obediencia.md) |
| B21 | `Haiku + DeepSeek` **DeepSeek es menos constante que Haiku**: sin manual repite la elección en el 91 % de las historias (Haiku, 96 %), y entre dos lecturas cambia el 12–18 % de las etiquetas. Una sola pasada de etiquetas hace variar 5–7 puntos la nota de un bot en el simulador: hay que medir con varias pasadas. | deepseek, [obediencia](lab/reports/deepseek/obediencia.md), [categorización](lab/reports/deepseek/categorizacion.md) |

**Palancas del juego (nota como memoria, techos)**

| # | Hallazgo | Fuente |
|---|---|---|
| B22 | `Bot + Haiku` **Detectar el techo del nivel durante la partida vale +8,8 puntos en el simulador** (+4,9 con la detección que consigue Haiku). La pista es una subida anunciada que no se mueve. Después hay que dejar de gastar en ese indicador y no arriesgarse por él. Aguanta si cambian techos o umbrales (+5 a +10). Darlo como números sería peor (con techos −10 %, 56,7 frente a 59,6) y está prohibido. Olvidarlo al mes siguiente cuesta ~3 puntos. | palancas, [techos](lab/reports/palancas/techos.md) |
| B23 | `Haiku` **La nota sirve de memoria.** Una línea de estado fija en cada nota (`Review in N \| Now S N O \| Stalled \| Risky this month`):<br>• Haiku la rellena bien el 100 % de las veces;<br>• vuelve entera tras un resumen por `check_latest_logs` (97–100 %);<br>• se obedece: el gasto en un techo apuntado baja del 27 % al 3–9 %;<br>• no tiñe las historias (86–89 % de elecciones iguales al control, frente al 81–85 % de `t13-final`).<br>Para que la IA *descubra* el techo hay que apuntar lo que se espera (`Expect`) y comparar un número: así pasa del 16 % al 49–63 %. | palancas, [nota-memoria](lab/reports/palancas/nota-memoria.md) |

**De las ramas de Leah y Matteo (revisado el 27 oct, 18:30 UTC)**

| # | Hallazgo | Fuente |
|---|---|---|
| B24 | `Bot + Haiku` **Nunca presentes una conducta arriesgada como forma de ganar un indicador.** Decirle a la IA que “venderte sube Output” dobla las crisis de confianza (73 → 174 por 1.000 partidas en la réplica, emparejadas) y baja la nota 5 puntos (53,2 → 48,1). Encaja con B7–B8. | Leah, `lab/reports/stat-perception/03-errores-output.md` (rama `leah/workspace`) |
| B25 | `Programa` **Mecánica de la nota.**<br>• Guarda hasta 1.000 caracteres: lo que pasa se corta a 997 + “...”.<br>• En *Continue* no se guarda.<br>• Persiste tras reconectar y reiniciar el servidor.<br>• En `check_latest_logs`, `count=N` cuenta entradas del registro, no decisiones.<br>Hay que mantener la línea de estado de B23 corta y al principio. | Matteo, `lab/reports/action-notes-study/README.md` (rama `matteo-t4-growth`; 256 notas) |

**Auditoría de representación y control (27 oct, apoyo a DeepSeek).**

| # | Hallazgo | Fuente |
|---|---|---|
| B26 | `Bot, contexto privilegiado` **La suficiencia de los signos depende del controlador.** Con el mismo Planner y estado ideal, efectos visibles exactos + riesgo exacto dan71,10; signos visibles perfectos + riesgo exacto70,69; signos visibles perfectos + sólo signo de riesgo58,11 (800 semillas por brazo). Perder magnitud de riesgo puede hacer que admita intercambios peligrosos. Un precio prudente recupera parte sin leer magnitudes reales; **no demuestra que haga falta otra taxonomía ni que DeepSeek alcance esa nota**. | [principios §5](lab/reports/deepseek/gpt-principios/README.md), factorial corregido y pantalla de márgenes |

## C. Pistas sin confirmar

| # | Pista | Fuente |
|---|---|---|
| C1 | `Haiku` El manual `t13-final` (reparto con prioridad + interruptor de evaluación) saca 57,2 ± 5,1 frente a 50,5 ± 2,5 de f3-lean en partidas de Haiku (12 frente a 43): +6,7 ± 5,7, prometedor pero no seguro; t10, con las mismas reglas y otra redacción, saca 47,6. | transmisión, lotes g1–g6 |
| C2 | `Haiku` La instrucción del manifest no añade nada con Haiku; quizá sí con DeepSeek, que podría olvidar antes. | transmisión, [contexto largo](lab/reports/transmision/contexto-largo.md) |
| C3 | `DeepSeek` DeepSeek en partidas oficiales: f1 despedido en el mes 24 (18,8; 0,19 USD); `t13-read-v1` despedido en el mes 24 (14,98; 0,23 USD), porque la regla trimestral “céntrate en lo que falta” se coló en las historias y el riesgo explotó antes de la evaluación del mes 12 ([partidas oficiales](lab/reports/deepseek/partidas-oficiales.md)). Son anécdotas. Cómo percibe y etiqueta DeepSeek ya está medido (B17–B21). | carrera (histórico) |
| C4 | `Bot + Haiku` Una política por tipo de respuesta recupera dos tercios de la distancia entre el azar y la óptima (47 de 68 en el simulador). Falta saber cuánto saca DeepSeek razonando con esos tipos. | categorías §2 |
| C5 | `DeepSeek` Con DeepSeek, t13-final probablemente **mejora** las historias del bloque general (pérdida −0,40 a −0,79 puntos por decisión según el control de referencia; con Haiku no era seguro), aunque las aparta un poco de Skill (cambia 3–4 historias de cada 100 más que el ruido). | deepseek, [obediencia](lab/reports/deepseek/obediencia.md) |
| C6 | `DeepSeek` Con DeepSeek, t13-final empeora los detonantes (pérdida +0,95, al límite): ante un comentario de RR. HH. inquieto, la regla trimestral “protégete” se cuela en las historias y elige arreglos en privado, que suman riesgo. | deepseek, [obediencia](lab/reports/deepseek/obediencia.md) |
| C7 | `DeepSeek` La cuenta atrás “Review in N” aísla peor con DeepSeek: abre la referencia del mes de evaluación en todos los meses previos a una evaluación, pero también en un 9–26 % de los demás. | deepseek, [obediencia](lab/reports/deepseek/obediencia.md) |
| C8 | `DeepSeek` Con DeepSeek, añadir a t13-final la ficha de lectura y la regla de historias por orden (`t13-read-v1`) arregla los detonantes (−0,97) y la deriva lejos de Skill, pero empata con t13-final en la pérdida media de las historias (−0,02 ± 0,30). Falta confirmarlo en partidas. | deepseek, [masticado](lab/reports/deepseek/masticado.md) |
| C9 | `Bot + Haiku` Contar las respuestas arriesgadas elegidas desde el último comentario de RR. HH. vale +4,3 en el simulador para un jugador que se arriesga; las cifras de riesgo del reparto, solas, +0,4. Con Haiku el contador está siempre en la nota, pero sólo marca el 19 % de las respuestas arriesgadas que eligió (4 de 21; falsas alarmas, 1 %): no las reconoce (A6) y no cambia nada medible. DeepSeek ve mejor el riesgo (B17): con él, por medir. | palancas, [riesgo](lab/reports/palancas/riesgo.md) |
| C10 | `Programa + DeepSeek` Los tokens valen como mucho +0,7 de nota final. Las partidas oficiales con DeepSeek gastaron ~667.000 y ~756.000 por mes (f1, t13-read-v1), y el máximo se da con 500.000. La línea de estado no añade tokens medibles. Terminar la partida pesa mucho más: sin terminar, ese término se queda en 50. | palancas, [tokens](lab/reports/palancas/tokens.md) |
| C11 | `Bot + Haiku` Con Haiku, pedir el signo de los 5 indicadores en cada opción sube un bot de réplica de 49 a 53, y votar 5 lecturas lo lleva a 55. Repetir el etiquetado mueve ±1,2. Ese bot juzga el riesgo por la categoría y los significados se escribieron con la mitad de la réplica, así que no es comparable con B19. | Leah, `stat-perception/01-siete-formas.md`, `04-defs3-y-ruido.md` |
| C12 | `Bot` En un bot de réplica, percibir bien Output vale más que percibir bien Skill (+2,5 frente a −2,1). Puede depender de que ese bot persigue Skill sin mirar los techos: hay que repetirlo con el bot de B19 antes de reorientar nada. | Leah, `stat-perception/02` |
| C13 | `Haiku` Añadir la lectura de los 5 indicadores a la referencia del mes previo de t13-final no mejora a Haiku (n = 60, una pasada; 30 % frente a 18 % de puntos perdidos, ≈1,5 errores típicos, con otro CLI). | Leah, `stat-perception/05` |
| C14 | `Bot` Más prudencia tras una explosión de riesgo (un comentario de RR. HH. tranquilo no basta) baja las crisis de 20 a 4 por 256 partidas en un bot. Sólo vale la idea general: el bot usa respuestas concretas, que no pueden ir a un Skill. | Matteo, trust-risk-study |
| C15 | `Haiku` Los manuales de Matteo `observed-growth-v10` (59,6 ± 6,0; 8 partidas) y `v7` (57,6 ± 4,5; 9) igualan a t13-final (57,2 ± 5,1; 12), con otro actor, otro CLI y sin control común. v10 es la mejor de ~12 versiones (v3 bajó de 71 a 51 al repetirla). Llevan reglas de historias siempre visibles y no muestran la pérdida que describe la sección X. Hace falta un cara a cara alternado de ≥30 partidas por brazo. | Matteo, `research/matteo/INDICE.md`, `lab/registry-origins/matteo/` |
| C16 | `Método` **El banco de transmisión no es verdad exacta.**<br>• Pierde las continuaciones de historias pendientes de respuestas anteriores.<br>• No liquida el último mes.<br>• Usa el catálogo v1 (19 diferencias de riesgo con v2).<br>• “Acierto” mezcla obedecer una regla con elegir lo mejor.<br>El 56,0 de B19 lo saca un bot que ve techos y riesgo exactos: es un techo, no una previsión. No cambia las conclusiones generales; hay que arreglarlo antes de afinar más con el banco. | ChatGPT, [review-2](lab/reports/deepseek/independent-designs/review-2.md) §2; comprobado en `bank.py` |
| C17 | `Bot + Método` El efecto del precio prudente del riesgo cae al quitar privilegios: con caps aprendidos y HR retrasado48,83→51,37 (2.000 semillas), mientras el veto conocido da52,99. No es un nuevo candidato superior. La auditoría no ha reproducido75 estable ni encontrado un repo público atribuible a los equipos que lo logran. | [principios](lab/reports/deepseek/gpt-principios/README.md) |
| C18 | `Haiku, banco` **Obedecer la nota no implica elegir mejor.** En92 contextos de48 títulos, añadir propuesta/coste/alternativa/comprobación a un mismo Skill obtiene el formato92/92, pero riesgo positivo4→5/92 y dominancia inmediata3→6/92. Control repetido24/24 coincide; no certifica estabilidad poblacional. No hay motivo para pasar esta variante a partidas. | [prueba decisional](lab/reports/deepseek/gpt-principios/decision-audit.md),208 llamadasMax, modeloHaiku5.5/CLI2.1.303 |
| C19 | `Programa + DeepSeek, una traza` Un ensayo t13-read-v2 termina por max_continuations, vivo enmes33/L2,137 acciones correctas y42 negativas genéricas en chino. Los tres slots actuales tienen preferred_language:zh; no son fingerprints históricos. Parche inglés listo y33 tests offline pasan. **No se ha probado que el idioma cause las negativas ni que arreglarlo mejore Q.** | [runtime](lab/reports/deepseek/gpt-principios/runtime-audit.md) |

## X. Descartado (no repetir sin una razón nueva)

| Idea | Por qué no | Fuente |
|---|---|---|
| `Bot` Función de valor aprendida, mejora por simulación | no superan al planificador | motor M21, M29 |
| `Bot` “Todo a Skill desde L4” como regla sin umbrales | +0,6, nada | motor M23 |
| `Haiku` Reglas sobre historias visibles todo el tiempo (también “sólo en tal mes” o en `reference/` sin interruptor) | en los manuales de transmisión contaminaron 1 de cada 5 historias y perdieron 12–21 puntos en partidas (dato final de t3-instr en el mismo lote: −13,7). No es una ley general: v7 y v10 de Matteo las llevan y no muestran esa pérdida (C15) | transmisión; ChatGPT review-2 |
| `Haiku` “Evita confrontar / exponerte” | la IA cede para agradar, que también es arriesgado | transmisión, ronda A |
| `Haiku` Varios Skills, uno por regla | la IA lee sólo uno | transmisión, ronda A |
| `Haiku` Pedir que mire el registro para calibrar | lo mira (96 %), pero no elige mejor | transmisión, [fase 3](lab/reports/transmision/fase3-rubrica.md) |
| `Haiku` Reloj de evaluación, “no cambiar Dignity por Network”, leer el registro, limpieza preventiva del último año (noche del 26) | no mejoran | [histórico T18](lab/reports/historico/secciones/resumen-noche.md) |
| `Haiku` Carrera de manuales por estilo (prereg-v1, fastloop) | mucha cuota para diferencias dentro del ruido | [ESTADO antiguo](docs/historico/ESTADO-2026-10-26-carrera.md) |
| `Juego` Nota S, niveles L8–L10, variantes de historias, efectos según el estado, efecto del campo `notes` | no existen | motor M19, M26, M27 |
| `DeepSeek` Agrupaciones gruesas de respuestas para DeepSeek (sólo el riesgo; el indicador que más sube; tipo + riesgo) | aun con etiquetas perfectas se quedan en 47–63, frente a 67 con los seis signos | deepseek, [categorización](lab/reports/deepseek/categorizacion.md) |
| `DeepSeek` Mejorar los 10 tipos con pistas de lectura | con DeepSeek, las pistas mejoran los signos (+5,5) pero no los tipos (49,4 → 48,5) | deepseek, [categorización](lab/reports/deepseek/categorizacion.md) |
| `Bot` Reaccionar a los avisos con 3 meses de margen (dinero, aislamiento, dignidad) o al de la tercera evaluación en L1 | 0 puntos en el simulador; las derrotas por condición casi no ocurren y la tercera evaluación en L1 ya no tiene arreglo | palancas, [avisos](lab/reports/palancas/avisos.md) |
| `Bot` Preparar la reputación antes de la evaluación para evitar la charla de aviso (M24) | +0,1 con la regla exacta, −0,5 con la general | palancas, [reputación](lab/reports/palancas/reputacion.md) |
| `Revisor de rúbrica` Llamar “Caps” o “techo del nivel” a lo que no sube | el revisor de la rúbrica lo lee como una mecánica sin publicar (el manual dice “0–unbounded”); hay que describir lo que se ve (“Stalled”) | palancas, [nota-memoria](lab/reports/palancas/nota-memoria.md) |
