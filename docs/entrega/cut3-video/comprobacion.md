# Hoja de comprobación del vídeo del corte 3

Cada afirmación del [guion](guion.md) y de las [diapositivas](slides.pptx), con su fuente en este repo (rama `alejandro/corte3`) y la comprobación contra lo entregado: el Skill `lab/policies-src/mejora/mv-3/bundle/` (SKILL.md y manifest.json) y los documentos `docs/entrega/cut3-mv3/` (README, `skills_design.md`, `decision_report.md`).

**Resultado:** todo lo que el vídeo dice del Skill coincide con el SKILL.md, el manifiesto y los documentos. Hay **cuatro diferencias de cifras** entre los datos más recientes y `decision_report.md`; ninguna es sobre el Skill, pero el jurado lee las dos cosas. Están en §4 con la propuesta de arreglo; **no he tocado los documentos entregados**.

Abreviaturas: **S** = `SKILL.md`, **M** = `manifest.json`, **SD** = `skills_design.md`, **DR** = `decision_report.md`, **C3** = `lab/reports/corte3/README.md`, **CSV** = `lab/data/deepseek/partidas.csv`, **E** = `docs/entrega/cut3-video/ENCARGO.md`.

## 1. Lo que el vídeo dice del Skill

| # | Afirmación (diapositiva) | Fuente | ¿Coincide con lo entregado? |
|---|---|---|---|
| K1 | Un solo Skill, `career-rules`, usado en cada turno (S1, S5) | SD §2; README entregado | Sí: el bundle sólo tiene `skills/career-rules/SKILL.md` y `manifest.json` (comprobado con `find`) |
| K2 | Sin scripts ni ficheros de referencia (S5, S11) | SD (cabecera); README entregado | Sí, mismo `find` |
| K3 | Con varios Skills el agente abría uno y perdía reglas de otro (S5) | SD §2 «Why one Skill»; DR §6 | Sí |
| K4 | El agente lee el Skill al principio y luego trabaja con el contexto; no reabría ficheros de apoyo; por eso el manifiesto repite lo esencial (S5, S11) | SD §2 «Why the manifest repeats the scope» | Sí. M empieza por «reread it whenever its rules are not in view» |
| K5 | Lo que repite el manifiesto: bucle de dos llamadas, historias y trimestres por separado, descartar opciones que pueden enterrar un problema, proteger S/N/O antes de la evaluación, plan trimestral desde el nivel 4, nota de una línea (S5) | M; SD §2 | Sí, las seis cosas están en M, en ese orden |
| K6 | Tres preguntas: qué cambia la opción, qué necesita la carrera, qué regla toca en esta fase (S3) | SD §1; E §5.1 | Sí (SD §1 lo dice con esas palabras; S está ordenado así: guía de lectura, prioridades, `Review in N`) |
| K7 | La sección de historias empieza con una guía de lectura en palabras generales, sin nombres de eventos ni respuestas (S3) | S «Story decisions» (primer párrafo y viñetas); SD §4 | Sí |
| K8 | Prioridades fijas: seguir en la partida, ganar la siguiente evaluación, crecer (S3) | S «What this Skill is for», «Priorities, in order» | Sí |
| K9 | Cinco pasos ordenados: sobrevivir, riesgo, bienestar, cierre de evaluación, crecer (S4) | S pasos 1–5; SD §4 | Sí (nombres: Survive, Risk, Wellbeing, Review close, Grow) |
| K10 | Trimestre: «la primera línea que aplica gana», plan por nivel y freno de salud (S4) | S «Quarterly phases: first matching line wins», líneas 2 y 4–6; SD §5 | Sí |
| K11 | La línea de estado: meses hasta la evaluación, S/N/O ahora, mejores valores del nivel, evaluaciones recibidas aquí (S4) | S «Status line» (formato literal `Review in N \| Now … \| Best … \| Reviews here: 0`) | Sí, la diapositiva copia el formato literal |
| K12 | «Review in N» es un interruptor: las reglas de evaluación sólo se aplican con N = 1 o 2 (S4) | S paso 4 «Review close (Review in 1 or 2)»; SD §3 | Sí |
| K13 | La línea es la memoria del agente; las notas sobreviven a los resúmenes (S4) | S «Status line» primer párrafo | Sí |
| K14 | `Best` y la regla de proteger Network y Output dos meses antes de la evaluación y reparar enseguida (S7) | M («In the two months before a review…repair any loss at once»); S paso 4 «Repair first»; SD §6 fila v4 | Sí |
| K15 | Lista de redacciones arriesgadas y modo estricto cuando el comentario de RR. HH. no es amable (S7) | S viñeta «Hidden risk» y paso 2 «Strict mode»; SD §6 fila v2 | Sí |
| K16 | El Skill nombra los costes: Network cae cuando alguien queda decepcionado, aunque sea con educación; Output cae cuando tu tiempo va al trabajo de otro (S7) | S paso 4 «Read the hidden costs»; M («costs Network even when polite»); SD §4 | Sí. El guion dice «someone else's work»; S dice «extra work that is not your own deliverable». Mismo sentido |
| K17 | Una respuesta por decisión con dos llamadas, `take_action` y `observe`, con la forma literal en el Skill (S8) | S «Turn loop» paso 3 y bloque `tool_calls: [...]`; M; HALLAZGOS C53 | Sí |
| K18 | mv-4 = mv-3 + una frase del manifiesto, «Never end a reply with text only … not in prose»; es la única diferencia (S9) | `diff -r` de `mejora/mv-3/bundle` y `mejora/mv-4/bundle`: sólo cambian `name` y esa frase de M | Sí. SD §6 la cuenta como añadida en mv-5r y «Removed again in mv-3»; DR §5c igual |
| K19 | El Skill no tiene títulos de eventos, respuestas fijas ni umbrales ocultos; todo se apoya en el comentario de RR. HH., las charlas de evaluación, los efectos del menú trimestral y las notas propias (S12) | S (lectura completa); SD §7 | Sí |
| K20 | Único calendario: el publicado (evaluación cada seis meses); si la charla llega tarde, sigue protegiendo hasta que aparece (S12) | S «Review calendar» | Sí |
| K21 | Lo aprendido en nuestras partidas está marcado como observación nuestra y manda lo que muestra el juego (S12) | S «Published and ours» | Sí |
| K22 | Bucle comprobado con dos proveedores, uno que razona en privado y otro que no (S12) | SD §7 «Reply format»; DR §5c | Sí. E §5.4 dice «varios proveedores»; uso «two», como los documentos |

## 2. Cifras y hechos de la trayectoria

| # | Afirmación (diapositiva) | Cifra | Fuente | ¿Coincide con DR/SD? |
|---|---|---|---|---|
| T1 | El juego: 48 meses, 3 historias al mes con efectos ocultos, trimestres con Energía, evaluación cada 6 meses; 16 trimestres (S2) | — | E §3.1; handbook publicado (16 = 48 / 3) | Sí (SD §1) |
| T2 | Se pierde por no ascender, por el riesgo oculto (dos explosiones) o por agotamiento/ruina; el riesgo sólo se ve por el tono del comentario de RR. HH. (S2) | — | HALLAZGOS A3, A4; S «Throughout» | Sí |
| T3 | DeepSeek detecta el 83 % de las opciones arriesgadas y sólo ~45–49 % de las que suben Skill u Output (S3) | 83 %; 45 %; 49 % | HALLAZGOS B17; `lab/reports/deepseek/percepcion.md` | Sí (DR §4) |
| T4 | Corte 1: `t13-read-v4`, 64,75 oficial, puesto 13 de 34 (S6) | 64,75; 13/34 | ESTADO §2; HALLAZGOS C45 | Sí. Es el puesto del corte 1, no el actual |
| T5 | Corte 2: `mv-5r`, 45,44 oficial (S6) | 45,44 | C3 §1; DR §5c | Sí |
| T6 | Corte 3: nota oficial desconocida (S6) | — | E §7 | Sí |
| T7 | Ascensos perdidos por un punto de Network u Output en la última historia antes de la evaluación (S7) | — | DR §5 punto 1; SD §6 fila v3 | Sí |
| T8 | Opciones «responsables» (charla en privado, arreglo por fases) con riesgo oculto (S7) | — | DR §5 punto 2; SD §6 fila v2 | Sí |
| T9 | Las notas del agente mostraban que aplicaba la regla pero creía que una negativa educada conservaba Network (S7) | — | `lab/reports/mejora/README.md` §2; SD §6 fila mv-5r («for example, that a polite refusal keeps Network») | Sí |
| T10 | Corte 1: ~1,4 M fichas por mes de juego (S8) | 1,35–1,47 M | HALLAZGOS C51, C53; DR §5 y §5c | Sí |
| T11 | Cada llamada reenvía todo el historial; el coste crece más deprisa que el número de respuestas (S8) | — | HALLAZGOS C51 (cuadrático); SD §3 | Sí |
| T12 | DeepSeek sólo emparejaba las llamadas con la forma literal de la respuesta en el Skill (S8) | 0/5–0/6 sin ejemplo, 6/6 con él | HALLAZGOS C53 | No está en DR/SD, pero no lo contradice (S lleva ese bloque) |
| T13 | mv-3: 0,5–0,8 M fichas por mes; de media, menos de la mitad que el corte 1 (S8, S13, S14) | 0,49–0,78 M; media 0,60 M (43 % de ~1,4 M) | CSV, filas `mv-3` completas, (entrada + salida) / 48; E §4 | **Diferencia ⚠ D2** |
| T14 | Eficiencia de fichas completa con ≤ 0,5 M por mes (S8) | 0,5 M | `competition-rules.rst` (Token efficiency); E §4 | Sí (DR §5c) |
| T15 | Una carrera de mv-3 cortada por el programa tras 21 respuestas sin llamada (S9) | 21 | DR §5c; C3 §7; CSV `mv-3__e8cdf663-00003` (`max_continuations`, mes 15) | Sí |
| T16 | mv-4 terminó antes 5 veces de 11 (S9) | 5 de 11 | CSV (11 filas `mv-4`, 6 completas); E §4 | **Diferencia ⚠ D1** |
| T17 | mv-3: 7 completas de 9, media 70,1, dos en el sexto nivel (S9, S14) | 70,06 → 70,1; L6: 77,78 y 74,12 | CSV; C3 §7; E §4 | Sí (DR §5c) |
| T18 | mv-4: media de las completas 64,2; ninguna en el sexto nivel (S9) | 64,23 | CSV (63,35 · 69,62 · 63,27 · 59,99 · 69,70 · 59,47); E §4 | DR no da la media; ver **D1** |
| T19 | No completas: mv-3, 1 cortada por el programa y 1 acabada en el mes 24; mv-4, 3 crisis de confianza, 1 despido, 1 ruina (S9) | 31,01; 37,06 · 37,39 · 32,73 · 18,98 · 31,34 | CSV; DR §5c | Sí; ver **D4** sobre el 31,01 |
| T20 | Hipótesis sin probar: la frase quita el razonamiento escrito cuando el proveedor no razona en privado (S9) | — | C3 §7; DR §5c («plausibly») | Sí, dicho como hipótesis |
| T21 | Corte 2: el banco decía que el texto de costes añadía riesgo en niveles altos; se restringió al nivel inicial; 2 de 3 partidas se hundieron en ese nivel (S10) | 69,00 · 22,65 · 24,51 | DR §5c y §6; CSV `mv-5r` (dos eliminadas en L1 en el mes 24) | Sí |
| T22 | Reconstrucción de las reglas del corte 1: mejor en los tramos (79 % frente a 73 %) y con dos revisores; en 5 partidas, 3 despidos en el nivel inicial (S10) | 79 %/73 %; 58,06 · 52,32 · 28,76 · 24,90 · 28,34 | DR §5d; C3 §6; E §4 | Sí |
| T23 | Variante «valiente»: no llegó más alto que mv-3 y hubo explosiones (S10) | 60,62 · 63,02 · 61,53 · 63,62 · 62,73 | DR §5d; C3 §6–§7 | Sí. No digo «subían antes», porque DR §5d dice que se atascaron en L4 |
| T24 | Advisor con script (otra línea): su mejor partida llegó al sexto nivel; 3 de 7 terminaron antes; las completas gastaban ~1,6 veces más fichas (S11) | 76,87; 3/7; 1,6× | DR §6; CSV filas `script-v*` | Sí; ver **D3** |
| T25 | Los scripts que usan sólo datos de la partida estaban permitidos (S11) | — | HALLAZGOS C49; ESTADO §5 | Sí |
| T26 | En la réplica, un script con estado no añadió nada (S11) | +0,0 | HALLAZGOS C63 | No está en DR/SD; no los contradice. La réplica se menciona sólo como herramienta de investigación (E §7) |
| T27 | Cerca de una partida de cada cuatro se hunde, sobre todo en el nivel inicial (S12) | ~1/4 | SD §7 «Perception» | Sí |
| T28 | La tercera evaluación del nivel inicial la ganó 1 de las 11 partidas que llegaron; el motivo fue el riesgo oculto, no los indicadores (S12) | 1 de 11 | DR §5d; C3 §2 | Sí. C3 §2 dice «~12» en una tabla y «11» en el texto; uso 11 como DR |
| T29 | Las directrices trimestrales concretas se siguen mucho más que los objetivos generales (S13) | (2 % y 15 % → 65 %) | SD §5 (última frase); DR §3; HALLAZGOS A7 | Sí. El vídeo no da la cifra |
| T30 | Un manual anterior cambió 1 de cada 5 historias que no le tocaban (S13) | ~1/5 | DR §3; HALLAZGOS A7 | Sí |
| T31 | Todas las notas son de partidas de desarrollo, salvo las dos notas oficiales de los cortes (S9, S14) | — | E §4 (última línea); DR (cabecera) | Sí |

## 3. Lo que el vídeo evita (E §7, NORMAS §4)

- Ningún título de evento ni texto del juego. Los ejemplos de S7 («a private talk», «a phased fix», «a polite refusal») son las palabras de DR §5 y SD §6, no títulos.
- Ningún umbral del motor como regla (nada de «the bar is…», ni los máximos por nivel de B31, ni la regla de nota C/D de B30). La tercera evaluación se cuenta como lo visto en nuestras partidas.
- No se menciona el paquete del motor. La réplica sale una vez (S11) como herramienta de investigación, igual que en DR §2.
- No se presenta ninguna nota de desarrollo como oficial; el corte 3 se da como desconocido.
- No se menciona a Claude: los «quality reviewers» de S10 son los «two independent reviewers» de DR §5d.

## 4. Diferencias con `decision_report.md` (avisar a Alejandro)

| | Qué dice el vídeo | Qué dicen los documentos entregados | Qué es lo correcto | Propuesta |
|---|---|---|---|---|
| **D1** | mv-4 terminó antes 5 de 11; 6 completas, media 64,2 | DR §5c: «five of ten careers ended early» y lista 5 completas (falta 59,47). C3 §7 igual (5 completas, 65,2) | CSV: 11 partidas de mv-4, 6 completas (`mv-4__0f4bf379-conf00005`, 59,47, L5, mes 49). E §4 ya lo recoge | Antes de reconstruir el ZIP, en DR §5c cambiar «five of ten» por «five of eleven» y añadir 59.47 a la lista de completas. Si no se toca DR, decir en el vídeo «about half» y quitar el «6 of 11» de S9 |
| **D2** | mv-3 gasta 0,5–0,8 M por mes; de media menos de la mitad que el corte 1 | DR §5c: «careers of this family used 0.46–0.70 million (efficiency 92–100)»; SD §7: «about a third of our Cut 1 version»; DR §8: «cut … by two thirds» | CSV, completas de mv-3: 0,49–0,78 M (eficiencia 89–100, media ~96); media 0,60 M. Lo de DR es «la familia», no mv-3 sola | No es contradicción estricta, pero «a third» y «two thirds» exageran para mv-3 (43 %). El vídeo no los repite. Si se toca DR, «0.49–0.78 million for `mv-3` (efficiency 89–100)» |
| **D3** | El advisor con script: «its best career reached the sixth level» | DR §6: «reached our best single career (sixth level)» | 76,87 (advisor) < 77,78 (mv-3, 29 oct). DR §5c dice que mv-3 es «the Skill behind our best development careers» | Contradicción interna de DR. Arreglo: «reached the sixth level (76.87)». El vídeo ya usa la redacción correcta |
| **D4** | La partida 31,01 de mv-3 «ended at month 24» | DR §5c: «still at the starting level at month 24»; E §4 igual | CSV: `mv-3__e8cdf663-conf00001`, `eliminada`, 24 meses, **nivel L2** | Comprobar en la partida (`python3 scripts/corte3/partida.py <run_dir>`) si ascendió en el mes 24 y aun así fue despedida, o si el CSV registra mal el nivel. El vídeo no entra en el detalle |

## 5. Cómo se comprobó

- Skill: lectura completa de `SKILL.md` y `manifest.json`; `find lab/policies-src/mejora/mv-3/bundle -type f` (dos ficheros); `diff -r` contra `mejora/mv-4/bundle`.
- Cifras de partidas, recalculadas desde `partidas.csv` (fichas = entrada + salida, entre 48 meses; eficiencia = (3 − M) / 2,5 × 100, con tope en 100):

```bash
python3 -c "
import csv
for m in ['mv-3','mv-4']:
  r=[x for x in csv.DictReader(open('lab/data/deepseek/partidas.csv')) if x['manual']==m]
  c=[x for x in r if x['completada']=='True']
  t=[(int(x['fichas_entrada'])+int(x['fichas_salida']))/48e6 for x in c]
  print(m, len(c), 'de', len(r), round(sum(float(x['nota']) for x in c)/len(c),2), [round(v,2) for v in t])
"
```

- Duración: 1.266 palabras habladas; ~8:45 a 145 palabras por minuto (contado por bloque en el script de [guion.md](guion.md)).
