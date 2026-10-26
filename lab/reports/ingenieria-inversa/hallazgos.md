# Hallazgos (caja negra, dev 1.0.8)

Material de investigación del repo privado. **Nada de esto se copia a una Skill tal cual:** los números son del dataset de desarrollo y la norma prohíbe presentarlos como reglas. Cada hallazgo lleva su traducción permitida en la sección final.

Cada hallazgo indica el lote del que sale, cuántas partidas lo respaldan y cómo se midió.

## H1. Techos por nivel: se aplican al instante y lo que sobra se pierde (lote b00, 26 oct 22:50 UTC)

Se compararon, en 8.000 partidas, el efecto anunciado de cada opción (línea del registro oficial) y el cambio real del estado en el mismo mes:

| Nivel | Skill | Network | Output | Health | Dignity |
|---|---:|---:|---:|---:|---:|
| L1 | 9 | 3 | 3 | 10 | 10 |
| L2 | 21 | 7 | 6 | 10 | 10 |

- Con Skill 9 en L1, cualquier subida de Skill se pierde entera; con 8, sólo entra 1 punto. Igual en Network y Output con su techo.
- Los mínimos son Skill 1, Network 0, Dignity 0 y Output −1.
- A veces se ven valores por encima del techo en el cambio de mes, por efectos de fin de historia. La siguiente acción los recorta.

## H2. El ascenso de L1 a L2 es casi determinista (b00, 2.043 partidas que llegaron al mes 6)

**El dato que cuenta es el estado justo antes de la evaluación:** el estado antes de la última decisión del mes 5, más el efecto de esa decisión con los techos aplicados.

| Estado justo antes de la 1.ª evaluación | Ascienden |
|---|---:|
| Skill ≥ 8, Network ≥ 3 y Output ≥ 3 | **113 de 119 (95 %)** |
| …de ellos, en el techo exacto (9/3/3) | 80 de 84 |
| Skill 7, con Network y Output en el techo | 0 de 24 |
| Network 2 | 0 de 38 |
| Output 2 | 0 de 51 |
| Output ≤ 1 | 0 de 130 |

**Los 113 ascensos cumplen la condición.** El "55 % en el techo" del estudio de ascensos salía de medir el estado antes de la última decisión del mes 5, sin su efecto. Por eso la parte "aleatoria" era casi toda un error de medida. Quedan 6 casos que cumplen y no ascienden: hay que mirarlos (dignidad, explosión de riesgo en la transición).

**Consecuencia:** en L1 basta con llegar a la evaluación en el techo de Network y Output y a un punto del de Skill, y no perderlo en el último mes. Lo difícil es que las opciones de los eventos del último mes no tiren abajo un punto de Network u Output.

## H3. Señales de la partida que delatan el estado oculto (b00)

Son textos de los registros oficiales (desarrollo). Sirven para interpretar la partida, no para copiarlos.

- **Riesgo oculto: el comentario mensual de RR. HH.** tiene 5 grados, del más tranquilo al más grave: sonriente ("doing all right") → en voz baja ("some risk, isn't serious yet") → con el ceño fruncido ("risks have piled up") → inquieto ("you're on your own now") → enfadado ("everything you buried is about to go off").
- **Avisos:**
  - explosión de riesgo ("Old landmines all go off at once…");
  - deudas ("Payday just means paying off debts…");
  - habilidad por detrás de lo esperado ("jargon you cannot keep up with…");
  - aislamiento ("nobody asks you to lunch…");
  - dignidad agotada ("do I really need this job?");
  - evaluación floja ("the next one has to be better").
- **Charla semestral:** 6 tonos, de "Acceptable overall" a "This is your last chance". Su relación con la nota está por medir.
- **Ascenso rápido:** "You climbed too fast…" anuncia más fricción con los contactos. Su efecto está por medir.

## H4. Acciones trimestrales: efectos fijos (b00)

Las acciones principales tienen efectos fijos en todas las partidas:

| Acción principal | Efecto |
|---|---|
| Proyecto clave | Output +2, Skill +1, Network +1 |
| Rotación | Skill +2, Network +1 |
| Mentoría | Skill +1, Network +2 |
| Pedir recursos | Output +1, Network +1 |
| Informar al jefe | Output +1, Network +1, Dignity +1 |
| Mostrar resultados | Output +1, Dignity +1 |
| Reparar relación | Network +1, Dignity +1 |
| Pasar desapercibido | Health +1 (¿y menos riesgo? por medir) |

Las acciones de energía siguen los `status_updates` que muestra el propio juego.

## H5. Qué respuestas acumulan riesgo oculto (b00, 500 respuestas con 40 casos o más)

**Método.** En b00 las respuestas se eligen al azar. Para cada respuesta se mide cuánto cambia el comentario de RR. HH. del mes siguiente frente a las demás respuestas de la misma pregunta. Es una medida ruidosa, en grados del comentario.

| Más riesgo | Menos riesgo |
|---|---|
| Unirse a las quejas o al cotilleo | Atacar la causa raíz ("revertir, fijar la versión y buscar la causa") |
| Aceptar un enlace sin abrirlo y "borrarlo después" | Mantener los controles de calidad aunque cueste |
| Quedarse callado en una revisión | Seguir el proceso completo, con un plan para limitar el daño |
| Relajar umbrales o controles para ir más rápido | Negarse a filtrar información confidencial |
| Saltarse pasos para entregar antes | Bloquear un cambio inseguro hasta que se arregle |
| Pasar gastos dudosos "porque todos lo hacen" | Pasar sólo los gastos claramente permitidos |
| Negar o inventar excusas ("me hackearon la cuenta") | Ser transparente sobre lo que se sabe |
| Aguantar a base de cafeína o sin descansar | |
| Contar planes internos | |

- Muchas respuestas seguras **cuestan algo de Network u Output** en el momento. Es el dilema del juego: el atajo da puntos ahora y crea riesgo oculto que explota después.
- Las acciones principales también cuentan. "Pasar desapercibido" baja el comentario de RR. HH. unos 0,55 grados más que las demás, así que reduce el riesgo aunque no lo anuncie. "Pedir recursos" y "rotación" se asocian a algo más de explosiones en los 3 meses siguientes (30–31 % frente a 25–28 %).
- Una explosión de riesgo cuesta en el acto Dignity −3/−4, Wealth −2 y a veces Output. La segunda termina la partida (crisis de confianza).

## H6. Techos y umbrales de ascenso de L1 a L6 (b00 + b01 parcial, 9.315 evaluaciones; 26 oct 23:05 UTC)

Los techos se miden con los recortes. Los umbrales son el mínimo de cada indicador entre los ascendidos, comprobado como condición suficiente: entre las evaluaciones que cumplen los tres mínimos, qué parte asciende.

| Nivel | Techo S / N / O | Umbral de ascenso S / N / O | Cumplen y ascienden |
|---|---|---|---|
| L1 | 9 / 3 / 3 | 8 / 3 / 3 | 96 % en la 1.ª evaluación y 99 % en la 2.ª |
| L2 | 21 / 7 / 6 | 18 / 6 / 5 | 482 de 486 (99 %) |
| L3 | 42 / 21 / 16 | 35 / 18 / 14 | 358 de 373 (96 %) |
| L4 | 108 / 36 / 26 | **90** / 33 / 22 | 106 de 106 (100 %) |
| L5 | ≥142 / 54 / 38 | ~130 / ~45 / ~33 | sólo 6 casos (provisional) |

- **El salto de Skill en L4 (de 35 a 90) es el cuello de botella.** El oráculo asciende hasta L4 casi en cada evaluación (meses 6, 12 y 18). De L4 a L5 nadie asciende antes del mes 36 (18 meses en L4) porque hace falta acumular Skill.
- En la mayoría de los fallos que cumplían los mínimos, la nota era D o coincidían con una explosión de riesgo, o la dignidad estaba agotada (casi todos en L1).
- No hace falta un tiempo mínimo en el nivel: en L2 y L3 se asciende a los 6 meses en cuanto se cumplen los mínimos.

## H7. La nota de la evaluación sigue al nivel y al ascenso (mismas evaluaciones, sin contar la 1.ª)

| Situación | Nota más frecuente |
|---|---|
| L1, 1.ª y 2.ª evaluación | C (siempre) |
| L1 con 17 meses o más en el nivel (3.ª y 4.ª) | **D (88 %)** |
| L2 cumpliendo los mínimos para L3 | B (96 %); si no, C (87 %) |
| L3 | B (97 %), cumpla o no |
| L4 cumpliendo los mínimos para L5 | A (96 %); si no, B (79 %) |
| L5 | B (95 %) |

La nota casi no depende de nada más: subir de nivel arrastra la nota, y la D llega por quedarse en L1.

## H8. El despido llega en el mes 24 a quien sigue en L1 (todos los despidos de b00+b01)

- Los 76 despidos ocurrieron en la 4.ª evaluación (mes 24), con secuencias C C D D (55), C C C D (10), C C D C (9) y C C C C (1). Todas con L1 al llegar a la 3.ª y 4.ª evaluación, salvo 6 que ascendieron en la 4.ª y aun así fueron despedidas.
- Con notas flojas en la 3.ª y la 4.ª pero ya en L2, ninguna partida fue despedida (8 de 8 siguieron).
- En la 3.ª evaluación (mes 18) no se despide a nadie.
- **Lectura práctica:** el primer año es una ventana de gracia. Hay que salir de L1 como muy tarde en la 3.ª evaluación (mes 18); si se llega al mes 24 en L1 con notas flojas, el despido es casi seguro. La regla exacta está por precisar (¿cuenta el aviso "the next one has to be better"?).

## H9. Riesgo: el comentario de RR. HH. es un buen termómetro, y ciertas respuestas lo disparan (b00 + b01)

- **La medida basada en RR. HH. es fiable.** Para 486 respuestas, el exceso de explosiones en los 3 meses siguientes frente a las demás respuestas de la misma pregunta se correlaciona en **0,82** con la medida basada en el comentario de RR. HH. (H5).
- **El efecto es grande.** Las peores respuestas suben **entre 25 y 36 puntos** la probabilidad de explosión en 3 meses: apostar a que un fallo no salte, ocultar un informe, quedarse callado en una revisión, negar, inventarse una contribución, cotillear, insinuar fallos de un compañero o contar a alguien que está en una lista confidencial. Las mejores la bajan entre 25 y 34 puntos: parar el despliegue y revertir, admitir, avisar a seguridad, negarse a filtrar y seguir el proceso con un plan de contención.
- **Dónde estallan.** Las explosiones salen al empezar el mes (con el comentario "enfadado", el 24 % de esos meses) o justo después de una decisión de evento. Pueden llegar con cualquier comentario: 93 de 965 llegaron con el comentario "sonriente".

## H10. Un bot que juega bien llega a una nota media de 63 (oráculo v2, 150 partidas; 26 oct 23:15 UTC)

El oráculo v2 tiene tres ingredientes:
- efectos de cada respuesta aprendidos en dev;
- pesos que priorizan los indicadores por debajo del umbral de ascenso de su nivel;
- un castigo fuerte para las respuestas que disparan explosiones.

| | Oráculo v1 (sin riesgo a 3 meses) | **Oráculo v2** |
|---|---:|---:|
| Terminan los 48 meses | 42 % | **84 %** |
| Nota media / mediana | 48,5 / — | **62,7 / 67,5** (máx. 78,4) |
| Crisis de confianza | 60 de 120 | 7 de 150 |
| Nivel final | sobre todo L4–L5 | **L6: 65, L5: 62** |

- Calendario típico del v2: L2 en el mes 6, L3 en el 12, L4 en el 18 (73 de 131), L5 en el 36 y L6 en el 48.
- **El tramo lento es L4, por el umbral de Skill.**
- Fallos que quedan: despido por quedarse en L1 (14) y crisis de confianza (7).
- **Partidas terminadas:** nivel 55, dinero 41, salud+dignidad 92, habilidad 97, riesgo 72 y red 85 (puntuaciones normalizadas). **Lo que más falta es dinero y nivel.**
- **No es una Skill:** usa conocimiento del dataset. Pero marca una referencia: jugando bien los eventos se pasa de ~55 a ~63–68.

## H11. Fórmula de la nota final, comprobada al céntimo (2.639 partidas de b01 y del oráculo v2)

**Q = 0,3·(10·nivel) + 0,2·mín(100, máx(0, dinero)/80·100) + 0,15·mín(100, (salud+dignidad)/20·100) + 0,15·mín(100, habilidad/120·100) + 0,1·máx(0, (10 − riesgo oculto final)·10) + 0,1·mín(100, red/60·100)**

Las 2.639 partidas cuadran sin ninguna discrepancia.

- **Dinero de las partidas terminadas del oráculo:** sueldo 29,1 + bonus 5,6 + eventos 0,4 + 1 inicial − 6,8 de otras pérdidas (explosiones de riesgo de −2 cada una, desenlaces de historias). El sueldo depende sólo del nivel y del tiempo en él, así que **el dinero también se gana ascendiendo antes**.
- Habilidad (tope en 120) y red (tope en 60) se llenan pronto en una buena partida. Lo que queda abierto es el nivel (cada nivel vale 3 puntos) y el dinero (cada 10 de dinero vale 2,5 puntos).

## H12. El juego es determinista salvo el sorteo de eventos y las explosiones (b00+b01+b02)

- **Cada respuesta tiene un efecto fijo:** el mismo cambio anunciado siempre, en cualquier nivel y partida. Se comprobó en 3.359 combinaciones de respuesta y nivel con 5 casos o más, sin una sola excepción, y en 800 respuestas vistas en varios niveles.
- **Las historias siguen siempre el mismo camino:** la misma respuesta lleva al mismo paso siguiente (164 de 164 respuestas con continuación; las 58 "ramificadas" son el mismo evento que vuelve a salir más tarde).
- **El azar está en qué eventos salen y en qué orden, y en cuándo explota el riesgo.** Hay 168 títulos y 403 preguntas. Cerca de 29 títulos sólo aparecen desde L2 o L3: dilemas de carrera como elegir entre gestión o especialización, ascensos que exigen dirigir personas, denunciar cifras falsas o cláusulas de no competencia. En esos dilemas, la respuesta reflexiva y comprometida da Skill, Network y Dignity; perseguir sueldo o cargo sin pensarlo, o no decidir, resta.

## H13. Lo que decide la partida son las respuestas a los eventos, en todas las etapas (b02, provisional con 40 partidas por brazo)

El oráculo v2 juega bien toda la partida salvo un semestre, en el que decide al azar sólo los eventos o sólo el reparto trimestral.

| Semestre al azar | Eventos | Reparto trimestral |
|---|---:|---:|
| S1 (meses 1–6) | −41 | 0 |
| S2 (7–12) | −37 | −4,5 |
| S3 | −24 | −2 |
| S4 | −30 | −2 |
| S5 | −25 | −3 |
| S6 | −18 | −1 |
| S7 | −15 | −1,5 |
| S8 (43–48) | −9 | −3 |

- La pérdida llega sobre todo por crisis de confianza: seis meses de respuestas descuidadas bastan para que explote el riesgo dos veces.
- **El reparto trimestral apenas importa cuando los eventos se juegan bien.**
- El crecimiento sale de los eventos: Skill ~2,8 de 3,3 al mes, Network ~2,0 de 2,5 y Output ~0,9 de 1,5.

## H14. En los niveles altos el ascenso depende sólo de la Skill (b02, 9.081 evaluaciones; 26 oct 23:25 UTC)

| De → a | Techo S / N / O | Umbral S / N / O | Cumplen y ascienden | Fallos con sólo la Skill por debajo |
|---|---|---|---|---:|
| L4 → L5 | 108 / 36 / 26 | **90** / 30 / 22 | 886 de 886 | 1.759 |
| L5 → L6 | ≥154 / 54 / 38 | **130** / 45 / 32 | 377 de 378 | 618 |
| L6 → L7 | ? / 72 / 54 | ? | 0 de 19 (Skill máx. 154) | — |

- **Progresión de umbrales:**

  | Indicador | L1 | L2 | L3 | L4 | L5 |
  |---|---:|---:|---:|---:|---:|
  | Skill | 8 | 18 | 35 | 90 | 130 |
  | Network | 3 | 6 | 18 | 30 | 45 |
  | Output | 3 | 5 | 14 | 22 | 32 |

  El gran salto es la Skill de L4: casi el triple que en L3.
- **Ritmo de crecimiento** con buenas respuestas: Skill ~3,3 al mes; Network y Output, de sobra para sus umbrales. Para pasar de L4 a L5 hay que juntar ~50–55 puntos de Skill, unos 15 meses. Por eso el oráculo llega a L5 hacia el mes 36 y a L6 en el 48.
- **La palanca de la segunda mitad:** cada punto de Skill que se adelanta acerca el siguiente ascenso. Hay que priorizar Skill en los eventos, la rotación o la mentoría como acción principal y el aprendizaje en la energía cuando la salud lo permita, siempre que Network y Output sigan por encima de su umbral.

## H15. La primera evaluación se pierde en el último mes (b02, oráculo v2: 745 de 1.067 ascienden en la 1.ª)

- **En los 343 fallos, Network u Output ya estaban en el umbral y se perdieron después.** 288 de esas pérdidas llegan por una respuesta del **último mes antes de la evaluación**. En L1 el techo de Network y Output coincide con el umbral, así que no hay margen: un −1 en ese mes cuesta el ascenso.
- **Al perder el punto en ese mes:**

  | Situación | Casos |
  |---|---:|
  | Existía una respuesta segura que lo conservaba (el bot eligió mal) | 101 |
  | Las respuestas que lo conservaban eran arriesgadas (dilema real del juego) | 149 |
  | Todas las respuestas restaban (mala suerte con el evento) | 113 |
- La primera evaluación tiene una parte de lotería por los eventos del último mes. Proteger ese mes con cuidado (no ceder Network u Output si hay alternativa segura) debería subir el ascenso del 70 % a ~80 %. Se está midiendo en el lote b03.

## H16. El carácter de una respuesta predice sus efectos en historias que no se han visto (26 oct 23:30 UTC)

**Método.**
- Cuatro agentes (Sonnet) etiquetaron las 954 respuestas de dev con rasgos generales: asumir, transparencia, proceso, calidad, confidencialidad, ayudar, colaborar, escalar, poner límites, visibilidad, atajo, ocultar, engañar, cotillear, enfrentarse, pasividad, sobreesfuerzo, complacer, aprender y autocuidado. Además, una nota de integridad de −2 a +2.
- Se ajusta una regresión de rasgos a efectos con **validación por títulos reservados**: cada predicción sale de un modelo que no vio esa historia, como pasará con los eventos cerrados de la evaluación.

| Efecto | R² con títulos reservados | Correlación |
|---|---:|---:|
| Dignidad | 0,58 | 0,76 |
| Explosión de riesgo a 3 meses | 0,50 | 0,71 |
| Salud | 0,49 | 0,71 |
| Network | 0,42 | 0,65 |
| Skill | 0,40 | 0,63 |
| Riesgo según RR. HH. | 0,40 | 0,62 |
| **Output** | **0,02** | 0,20 |
| Dinero | 0,00 | 0,13 |

**Medias por integridad** (exceso de explosión a 3 meses frente a las demás respuestas de la misma pregunta):

| Integridad | Respuestas | Explosión | Skill | Network | Output | Dignidad |
|---:|---:|---:|---:|---:|---:|---:|
| −2 | 91 | **+19 puntos** | 0,0 | −0,45 | +0,1 | **−1,4** |
| −1 | 286 | +11 | −0,1 | −0,4 | −0,1 | −0,5 |
| 0 | 101 | +3 | +0,1 | −0,2 | **+0,5** | +0,2 |
| +1 | 125 | −5 | +0,6 | +0,5 | +0,1 | +0,7 |
| +2 | 350 | **−13** | **+0,8** | +0,5 | +0,2 | **+1,1** |

**Rasgos más claros:**

| Rasgo | Explosión a 3 meses | Otros efectos medios |
|---|---:|---|
| Ocultar | +17 puntos | |
| Engañar | +16 | Dignidad −1,6 |
| Cotillear | +15 | |
| Atajo | +12 | |
| Enfrentarse o culpar | +12 | **Network −1,6** |
| Complacer sin criterio | +10 | Dignidad −0,8, Salud −0,6 |
| Sobreesfuerzo | +8 | **Salud −1,9** |
| Pasividad | +8 | Network −0,4, Dignidad −0,4 |
| Aprender | | Skill +1,3 |
| Calidad | | Skill +1,2 |
| Asumir el problema | | Skill +0,9, Network +0,4, Output +0,3 |
| Ayudar | | **Network +1,4** |
| Colaborar | | **Network +1,3**, Skill +0,8 |
| Transparencia, proceso, confidencialidad, escalar bien, límites | | Dignidad +1,0 a +1,3; algo de riesgo menos |
| Autocuidado | | Salud +1,1 |

- **Lectura.** La integridad casi no tiene coste: las respuestas íntegras dan más Skill, Network y Dignidad, y bastante menos riesgo.
- **La excepción es el Output.** Lo dan las respuestas que se centran en entregar el propio trabajo (no ofrecerse para extras, seguir con el proyecto previsto). Lo quitan las que desvían tiempo: voluntariados, mentoría intensiva, rehacer a demanda, investigaciones, parar un despliegue. Una pasada extra de etiquetado mide ese eje.
- **Consecuencia para la Skill.** Una regla general sobre el carácter de la respuesta, del tipo "descarta lo que oculta, engaña, cotillea, toma atajos o culpa; entre lo demás, elige lo que alimenta el indicador que te falta", se apoya en efectos que generalizan a historias nuevas.

## H17. Proteger el mes previo a cada evaluación sube la nota unos 5 puntos (b03, 64 partidas por brazo)

| Oráculo v2 | Nota media | Terminan | Ascenso en la 1.ª evaluación | Llegan a L5 |
|---|---:|---:|---:|---:|
| Sin protección | 61,4 ± 4,3 | 80 % | 70 % | 75 % |
| Protección ×5 en el mes previo | 66,5 ± 2,7 | 86 % | 84 % | 91 % |
| Protección ×20 | 66,4 ± 3,0 | 86 % | 88 % | 91 % |

"Protección" quiere decir que, en el mes anterior a cada evaluación, perder un punto de un indicador por debajo de su umbral pesa mucho más. Basta con no regalar esos puntos cuando hay alternativa. La ganancia viene de ascender a tiempo, y ascender a tiempo arrastra todo lo demás.

## H18. La Dignidad también decide el ascenso, y el riesgo oculto resta un poco (37.282 evaluaciones de b00–b05; 26 oct 23:18 UTC)

Entre las evaluaciones que cumplen los tres umbrales de Skill, Network y Output de su nivel:

| Dignidad justo antes de la evaluación | Ascienden |
|---|---:|
| 0–3 | **0 de 40** |
| 4 | 31 de 38 |
| 5 | 37 de 39 |
| 6 o más | 17.044 de 17.470 (97,6 %) |

| Comentario de RR. HH. en el mes de la evaluación | Ascienden |
|---|---:|
| Tranquilo | 9.975 de 9.976 |
| En voz baja | 98,3 % |
| Ceño fruncido | 95,5 % |
| Inquieto | 93,9 % |
| Enfadado | 89,9 % (89 % si además explota) |

- La salud no cuenta: con salud 0–1 ascienden 50 de 51.
- **El ascenso es casi determinista:** cumplir los tres umbrales, tener la Dignidad sana y el riesgo bajo asciende prácticamente siempre. Lo que parecía azar es sobre todo riesgo oculto.
- **No se ha visto ninguna nota S** en 37.282 evaluaciones (B 16.390, C 14.448, A 5.663, D 781).
- **La charla semestral tiene tres tonos,** con tres variantes de texto cada uno:

  | Tono | Nota que lo acompaña |
  |---|---|
  | Elogio ("keep this pace", "colleagues sizing you up") | siempre A |
  | Neutro ("flag blockers early", "same bar in six months") | B o C |
  | Aviso ("show real change or I can't protect you") | C o D |

  Comenta la nota recién puesta; no la anticipa.

## H19. Cuánto se consigue sólo con reglas generales (b06, 200 partidas por brazo; b05 como referencia)

El "bot de principios" decide las respuestas con lo que predicen los rasgos de cada respuesta. Usa predicciones fuera de muestra: el modelo nunca vio esa historia. El resto lo juega igual que el oráculo.

| Bot | Nota | Terminan | Asciende en la 1.ª evaluación | Fallos principales |
|---|---:|---:|---:|---|
| Principios, sin conocer techos ni umbrales (los detecta en la partida) | 41,9 ± 2,8 | 41 % | 38 % | despido 53, crisis de confianza 39, agotamiento 21 |
| Principios, conociendo techos y umbrales | 48,4 ± 2,9 | 56 % | 44 % | despido 45, crisis 21, agotamiento 17 |
| Oráculo con efectos reales (1.003 partidas) | 64,1 ± 0,9 | 80 % | 86 % | crisis 158, ruina 27, despido 13 |

- **Saber cómo funciona el ascenso vale unos 6,5 puntos** a igualdad de todo lo demás.
- **El bot pierde sobre todo en la primera evaluación,** porque el modelo de rasgos no prevé el Output (R² 0,02). Acaba despedido en L1 en una de cada cuatro partidas.
- Un modelo de lenguaje lee las respuestas mejor que una regresión lineal de 21 rasgos, así que esto es un suelo, no un techo. Pero indica dónde debe insistir la Skill: **el Output en la entrada** y **no ceder puntos antes de la evaluación**.
- **Otros detalles medidos:**

  | Detalle | Efecto |
  |---|---|
  | Defuse (frente a la media de las acciones trimestrales) | −0,44 grados en el comentario de RR. HH. del mes siguiente |
  | Pasar desapercibido | −0,32 grados |
  | Sobreesfuerzo (High-intensity work) | **+0,67 grados** |
  | Aviso de "subiste demasiado rápido" | Network −2,7 y Dignidad −0,9 más que un ascenso normal; no compensa frenar |

- **El modelo numérico exacto del riesgo oculto sigue abierto.** Una regresión aditiva sobre el riesgo final no generaliza (R² −0,1 con partidas reservadas), porque casi siempre termina en 0 y se recorta.

## H20. Las explosiones tienen detonantes: respuestas que destapan lo acumulado (b00–b06; 26 oct 23:25 UTC)

**Método.** Para cada respuesta con 15 casos o más en cada situación (743 respuestas), se mide la probabilidad de que la explosión llegue **justo después** de elegirla. Se compara el riesgo alto (comentario de RR. HH. con el ceño fruncido o peor) con el bajo (tranquilo o en voz baja).

- **Mediana de todas las respuestas con riesgo alto: 0 %.** Casi ninguna respuesta provoca explosiones por sí misma.
- **59 respuestas detonan con riesgo alto en el 30 % de los casos o más,** y con riesgo bajo casi nunca:

  | Respuesta (resumida) | Riesgo alto | Riesgo bajo |
  |---|---:|---:|
  | Guardar un informe y apostar a que no salte | 91 % | 1 % |
  | Firmar con otros una carta a RR. HH. y al CEO sobre la cultura del equipo | 90 % | 1 % |
  | Seguir con el lanzamiento y apostar a que el fallo no salte | 89 % | 1 % |
  | Pedir a RR. HH. una investigación formal | 89 % | 14 % |
  | Unirse a las risas para no romper el ambiente | 87 % | 1 % |
  | Restar importancia a un riesgo en la comunicación oficial | 85 % | 0 % |
  | Negarse a un traslado alegando el deber | 85 % | 2 % |
  | Negar saber nada | 89 % | 15 % |
  | Inventarse una contribución | 57 % | 14 % |
  | Seguir encadenando excusas | 42 % | 0 % |
  | Decir "a tiempo" y recuperar en secreto trabajando de más | 43 % | 0 % |

- **Rasgos de los 59 detonantes:** ocultar 22, engañar 19, complacer 18, atajo 9, pasividad 9, cotilleo 7, enfrentarse 5. Además hay 4–5 respuestas **íntegras que atraen escrutinio formal**: quejas firmadas, investigaciones, plantarse ante la dirección.
- **El mecanismo, completo:**
  1. Las respuestas poco íntegras acumulan riesgo oculto, que el comentario de RR. HH. mide.
  2. Con riesgo acumulado, lo que puede salir a la luz (una mentira, una ocultación) o lo que pone a uno bajo escrutinio formal lo hace estallar en el acto.
  3. Además, con el comentario "enfadado", estalla al empezar el mes en una de cada cuatro ocasiones.
- **Consecuencia práctica.** Con el riesgo bajo, defender los principios es seguro (incluso pedir una investigación). Con riesgo acumulado, primero hay que desactivarlo (Defuse, pasar desapercibido) y evitar tanto las mentiras como exponerse a una revisión formal.

## H21. Evitar los detonantes vale 4,6 puntos (b07, ~130 partidas por brazo)

El oráculo v2 tiene protección del mes previo a la evaluación, Skill priorizada desde L3 y modelo m06. Se compara con y sin penalizar los detonantes según el riesgo del momento (H20):

| Oráculo | Nota | Termina | Asciende en la 1.ª evaluación | Crisis de confianza | Nivel final |
|---|---:|---:|---:|---:|---:|
| Sin detonantes | 64,5 ± 2,5 | 85 % | 78 % | 7 % | 5,29 |
| **Con detonantes** | **69,1 ± 1,9** | **94 %** | 88 % | **2 %** | 5,61 |

La regla "con riesgo acumulado, ni excusas ni exponerse a una revisión formal" se confirma en partidas completas.

## H22. En un contexto neutro, Haiku elige bien con o sin manual (banco de decisiones, 150 preguntas)

Se dieron a Haiku 150 preguntas reales de dev, con el contexto "mitad de carrera, todo por debajo de lo necesario, salud y dignidad bien, RR. HH. tranquilo". Las elecciones se puntúan con los efectos medidos.

| Elección | Elige la mejor | Elige una arriesgada (explosión +10 puntos o más) | Valor |
|---|---:|---:|---:|
| Al azar | 44 % | 31 % | 0,59 |
| Haiku sin instrucciones | 83 % | 6 % | 4,89 |
| Haiku con el manual campeón (targeted-1026-201334) | 83 % | 5 % | 4,89 |
| Haiku con el borrador `bb-mechanics-v1` | 81 % | 5 % | 4,90 |
| La mejor posible | 100 % | 0 % | 5,84 |

- **En lo básico, el juicio de Haiku ya es bueno, y ningún manual lo cambia.** Coincide con la observación de la nube de que Haiku elige lo mismo con cualquier manual.
- **Sus fallos tienen un patrón:** prefiere plantarse en público por principios (corregir al cliente en plena reunión, decir con firmeza que un comentario no es aceptable, impugnar una cláusula). El juego premia la forma discreta: reconducir sin montar una escena, aclarar por escrito después, compartir el razonamiento con el equipo.
- **Consecuencia:** el margen de un manual no está en el juicio ético de cada respuesta, sino en **el contexto**: el mes previo a la evaluación, el riesgo acumulado, cuándo un indicador ya está en su techo, y la mecánica que el modelo no puede adivinar. Se mide en un segundo banco con contexto.

## Traducción permitida a principios de Skill (borrador)

| Hallazgo | Principio general, sin números | Cómo lo comprueba el agente en la partida |
|---|---|---|
| H1 | Cada indicador de crecimiento tiene un techo que depende del nivel; lo que te ofrece una opción por encima del techo se pierde | Si una opción anunciaba +X y el indicador no subió, ya estás en el techo: usa ese esfuerzo en otro indicador |
| H2 | El ascenso premia llegar a la evaluación con Skill, Network y Output en su techo. Cuenta el estado del momento de la evaluación, y la evaluación llega antes de los eventos de su mes | En el mes previo a la evaluación, no elijas opciones que bajen Skill, Network u Output, y completa el que esté por debajo de su máximo reciente |
| H3 | El tono del comentario mensual de RR. HH. mide el riesgo acumulado; actúa en cuanto deja de ser tranquilo | Lee el comentario cada mes y usa Defuse cuando sube de grado |
