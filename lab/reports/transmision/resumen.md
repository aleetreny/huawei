# T20 Transmisión: resumen vivo

Rama `alejandro/transmision` (desde `origin/main`, con `main-1nddsg` y `alejandro/lab-secciones` juntadas), origen de registro `transmision`. Actor: Haiku (`claude-haiku-5-5`) por el CLI 2.1.303.

**El problema.** Ya sabemos qué hay que hacer (el simulador `replica.py` y el planificador, que saca 70,5 en el juego real). No sabemos cómo escribirlo para que un modelo pequeño lo obedezca. Este trabajo mide la obediencia en un banco de situaciones reales y busca la forma de escribir cada regla que más la sube.

## Tabla principal: regla → formulación ganadora → obediencia frente al control

Validación final (27 oct, 13:50–14:45 UTC): conjunto `ids-V2`, situaciones que **no** se usaron para elegir formulaciones, ≥ 200 por regla, con **todos** los títulos reservados (30 % de los títulos, nunca vistos al diseñar). Haiku, entrega oficial, contexto corto. Manual ganador: **`t10-countdown`** (lista trimestral con prioridad + cuenta atrás de la evaluación; [carpeta](../../policies-src/transmision/t10-countdown/)). Acierto = elige una opción a 0,5 puntos o menos de la mejor según el simulador (o la acción de la regla en el reparto); entre paréntesis, intervalo al 95 %. Pérdida = nota final media perdida frente a la mejor opción (simulador).

| Regla | Formulación ganadora | Situaciones | Acierto control | Acierto ganadora | Pérdida de nota (control → ganadora) | Sólo títulos reservados (n: control → ganadora) |
|---|---|---:|---|---|---|---|
| No ceder puntos antes de la evaluación | Cuenta atrás `Review in N` escrita en cada nota de historia; con N = 1, abrir `reference/review-month.md` (marcar qué opción va contra una persona o quita tiempo de la entrega propia; nunca salvar un punto escondiendo o apostando) | 230 | 73 % (67–78) | 76 % (70–81) | 2,05 → 1,56 | 150: 71 % → 77 % |
| Skill en L4 | Línea imperativa del reparto: “L4 or above: Energy on Skill learning (2)…; main action Apply for rotation” | 230 | 14 % (10–19) | **77 % (71–82)** | 0,23 → 0,21 | 150: 11 % → 73 % |
| Comentario de RR. HH. | Línea del reparto definida por exclusión: cualquier comentario que no sea uno de los dos suaves → Defuse legacy risk y Lay low and reduce risk | 230 | 18 % (14–24) | **60 % (53–66)** | 0,43 → 0,30 | 150: 19 % → 58 % |
| Detonantes | **Sin regla** (Haiku ya los evita; toda regla probada empeoró: “evita exponerte” lleva a ceder, que también es riesgo) | 230 | 91 % (87–94) | 88 % (83–92) | 0,51 → 0,70 | 150: 93 % → 92 % |
| Ruina temprana | **Sin regla** (Haiku casi nunca gasta con poco dinero: 2–3 % sin Skill) | 210 | 54 % (48–61) | 54 % (48–61) | 1,57 → 1,40 | 109: 44 % → 45 % |
| Cierre | Primera línea del reparto: “Final month of the career (month 48): main action Lay low…; Energy Defuse, Health, Dignity, then Network; never Skill learning” | 210 | 70 % (63–76) | **83 % (78–88)** | 0,33 → 0,20 | 72: 71 % → 81 % |
| Salud baja (añadida tras las partidas) | Línea del reparto: Health recovery primero con Health baja | 230 | 89 % (84–92) | 91 % (87–94) | 1,05 → 0,94 | 101: 86 % → 92 % |
| Efectos secundarios (historias fuera de las reglas) | — | 223 | 72 % (66–77) | 73 % (66–78) | 1,15 → 1,11 | 68: 72 % → 75 % |

Alternativa para “antes de la evaluación”: las seis reglas en el cuerpo con filtro (`t2-veto`) da el mismo acierto (76 %; pérdida 1,60), pero cambia 1 de cada 5 historias de otros meses y empeora los detonantes (pérdida 0,96).

**Resultado en partidas de Haiku** (completas, entrega oficial, intercaladas con f3-lean-v1 en los mismos lotes g1–g6; las de f3-lean se suman de todos los lotes; paradas a las 15:57 UTC del 27 oct a petición de Alejandro):

| Manual | Partidas | Terminadas | Nota media ± error | Diferencia con f3-lean | Derrotas |
|---|---:|---:|---:|---:|---|
| f3-lean-v1 (referencia) | 43 | 30 | 50,5 ± 2,5 | — | despido 6, crisis de confianza 5, ruina 2 |
| **t13-final** (manual que junta las reglas: reparto con prioridad + cuenta atrás de la evaluación, redactado para la rúbrica) | 12 | 10 | **57,2 ± 5,1** | **+6,7 ± 5,7** | agotamiento 1, despido 1 |
| t10-countdown (mismas reglas, redacción anterior) | 13 | 7 | 47,6 ± 5,5 | −2,9 ± 6,0 | despido 3, ruina 2, crisis 1 |
| t9-quarter (sólo reparto) | 15 | 7 | 44,0 ± 5,5 | −6,5 ± 6,0 | crisis 4, despido 4 |
| t3-instr (todas las reglas en el cuerpo, también de historias) | 9 | 3 | 38,4 ± 5,5 | **−12,1 ± 6,0** | despido 3, crisis 2, agotamiento 1 |

Sólo en el lote g6 (mismo tiempo y orden): t13-final 57,2 ± 5,1 (12) frente a f3-lean 48,4 ± 6,0 (11), +8,9 ± 7,9. **Lectura:** t13-final es el mejor manual de esta línea y va por delante de f3-lean, pero con 12 partidas la ventaja no es segura (aproximadamente 1,2 errores típicos). t10 tiene las mismas reglas y sale peor, así que una parte de la diferencia es azar. Lo que sí está claro es que poner reglas de historias a la vista (t3-instr) hunde la nota.

## Cómo escribir para que Haiku obedezca: lo aprendido

1. **Haiku lee el Skill.** En la forma oficial (sólo nombre y descripción en el mensaje de sistema, cuerpo con `skill_tool`) lo lee en el 100 % de las situaciones, también tras el mensaje oficial de continuación. Poner la regla en la descripción o en la instrucción del manifest no cambia la obediencia, ni con 18 decisiones de historial ([contexto-largo.md](contexto-largo.md)).
2. **Se obedece lo imperativo y concreto:** una condición visible y el nombre exacto de la acción del juego (“Energy: Skill learning; main action Apply for rotation”). Así el reparto trimestral pasa del 17–62 % al 73–93 %.
3. **El orden es la prioridad.** Decir “first matching line wins” y ordenar: con la regla de cierre detrás de la de Skill, Haiku eligió Skill learning en el mes 48.
4. **Una condición que el modelo debe reconocer se define por exclusión**, no con adjetivos: “cualquier comentario que no sea uno de estos dos suaves” (73 %) frente a “riesgo acumulado, serio o peor” (36 %).
5. **Las reglas sobre historias tiñen todas las historias.** Cualquier texto sobre costes de las opciones cambia 1 de cada 5 historias aunque no aplique (más Output y riesgo, menos Skill) y eso hundió un manual en partidas (−21 puntos). Avisar “sólo en tal mes” no lo evita, ni esconderlo en `reference/` ([bloque-general.md](bloque-general.md)).
6. **Un interruptor que el modelo calcula y escribe sí aísla la regla.** Con `Review in N` al principio de cada nota, Haiku acierta el número siempre, abre la referencia sólo cuando N = 1 y fuera de ese mes elige como sin manual ([ronda-8-10.md](ronda-8-10.md)).
7. **Prohibir un efecto oculto exige percibirlo.** “No bajes Output” se obedece, pero Haiku no sabe qué opción cuesta Output; la ganancia en el mes previo a la evaluación es real pero parcial.
8. **“Evita confrontar” se lee como “cede”,** y ceder para agradar también acumula riesgo. Hay que separar “mantener tu opinión con calma” de “ceder”.
9. **Un solo Skill.** Con un Skill por regla, Haiku abre sólo el que cree relevante y la regla de RR. HH. cae al 36 %.
10. **Medir efectos secundarios**, no sólo la regla: bloque de historias al azar, huella de las elecciones y un control repetido (96 % de coincidencia consigo mismo).

## Experimentos

| # | Informe | Qué mide | Estado |
|---|---|---|---|
| 0 | [fase0-carga-skills.md](fase0-carga-skills.md) | Cómo llega el Skill al modelo en el programa oficial | hecho |
| 1 | [banco.md](banco.md) | Construcción del banco y verdad del simulador | hecho (1.869 situaciones decisivas) |
| 2 | [ronda-a.md](ronda-a.md) | Rondas A y 2: dónde y cómo escribir cada regla (contexto corto) | hecho |
| 3 | ronda 3 | Prioridad explícita, ejemplos de cómo leer el coste de una opción, instrucción del manifest | en marcha |
| 4 | [contexto-largo.md](contexto-largo.md) | Las mismas reglas con 18 decisiones de historial antes | hecho: la obediencia no cae; la instrucción del manifest no añade nada |
| 5 | [partidas-g1.md](partidas-g1.md) | `t3-instr` frente a f3-lean-v1, partidas completas, entrega oficial | parado: −21 ± 8 puntos (7 + 7); la regla se salía de su contexto |
| 7 | [bloque-general.md](bloque-general.md) | Huella de las elecciones en historias fuera de las reglas | hecho: toda regla de historias cambia 1 de cada 5 historias |
| 8 | [ronda-8-10.md](ronda-8-10.md) | Sólo reparto trimestral (t8, t9) y una regla de historias tras una cuenta atrás (t10) | hecho |
| 9 | [fase3-rubrica.md](fase3-rubrica.md) | Reescritura para la rúbrica (58 → 73) sin cambiar el comportamiento; calibrar con el registro (t14) no mejora la percepción | hecho |
| 10 | [valor-obediencia.md](valor-obediencia.md) | Cuánta nota vale cada punto de obediencia (simulador y partidas) | hecho |
| 6 | partidas `g2-full` | `t6-scoped-instr` (reglas acotadas) frente a f3-lean-v1, 30 + 30 | en marcha desde las 12:30 UTC |

## Relevo

**27 oct, 16:00 UTC: cierre de la línea en la nube.**
1. **Hecho.**
   - Fase 0: cómo carga Skills el programa oficial ([fase0-carga-skills.md](fase0-carga-skills.md)).
   - Banco de obediencia con verdad del simulador ([banco.md](banco.md)); los datos, en `lab/data/transmision/`.
   - Rondas de formulaciones ([ronda-a.md](ronda-a.md), [ronda-8-10.md](ronda-8-10.md)), contexto largo, bloque general y huella.
   - Validación final en ≥ 200 situaciones por regla con títulos reservados ([validacion-final.md](validacion-final.md)).
   - Valor de la obediencia ([valor-obediencia.md](valor-obediencia.md)) y rúbrica ([fase3-rubrica.md](fase3-rubrica.md)).
   - Partidas g1–g6 (tabla de arriba).
   - Modo `#official` en `careerlab/actors/claude_cli.py`.
2. **Resultados.** Tabla principal y tabla de partidas de arriba. Manual recomendado: [t13-final](../../policies-src/transmision/t13-final/), 73 en la rúbrica y 57,2 frente a 50,5 de f3-lean en partidas.
3. **Parado o a medias.**
   - Lote g6 parado a petición de Alejandro: 13 partidas canceladas y las 4 en juego cortadas (quedan como interrumpidas).
   - Bancos parados a medias, sin conclusión: t15 (ganancias perdidas por estar al máximo) y t9 sobre la validación.
   - El runner está parado: existe `~/careerlab-data/huawei-transmision/STOP` en el contenedor de la nube.
4. **Siguiente.**
   - La línea sigue en local con DeepSeek: el prompt está en [prompt-deepseek.md](prompt-deepseek.md). Primero, qué percibe DeepSeek de cada opción (indicador que mueve y riesgo); después, el banco con DeepSeek frente al control y t13-final; por último, la forma masticada de darle las reglas.
   - Comandos: `uv run python scripts/transmision/score.py --items <items> --arms control,<brazo> --common`; `uv run python scripts/transmision/fingerprint.py --items <items> --arms control,<brazo>`; `uv run python scripts/transmision/games.py --batch g6-full` (necesita el registro del contenedor; el exporte está en `lab/registry-origins/transmision/`).
5. **ESTADO.md:** la fila de Transmisión pasa a “en pausa, sigue en la línea DeepSeek (local)”.
