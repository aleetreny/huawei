# Encargo: la presentación definitiva de mv-3 (vídeo del corte 3)

Interno, en español. **La presentación se hace en inglés** (lo exige el reglamento). No va en el ZIP.

## Prompt para pegar en el chat nuevo

> Eres responsable de la presentación final del equipo Gradient Depression para Huawei TechArena UK 2026 (*Career Survival*). Clona `https://github.com/aleetreny/huawei`, cambia a la rama `alejandro/corte3` y lee entero `docs/entrega/cut3-video/ENCARGO.md`: ahí están las reglas del vídeo, la historia del proyecto, los números verificados con su fuente y lo que tienes que entregar. Prepara (1) las diapositivas, (2) el guion hablado completo en inglés con tiempos, para un vídeo de 8–9 minutos que responda en orden a las cinco preguntas oficiales, y (3) una hoja de comprobación. Tiene que entenderlo un jurado técnico que no conoce nuestro trabajo: cuenta la trayectoria (qué probamos, qué falló, qué aprendimos y por qué entregamos mv-3) con frases claras y pocos números bien elegidos. Usa sólo cifras de este documento o de los ficheros que cita. Todo lo que digas del Skill tiene que coincidir con `lab/policies-src/mejora/mv-3/bundle/` y con `docs/entrega/cut3-mv3/`. Sube tu trabajo a `docs/entrega/cut3-video/` en una rama tuya (`<persona>/video-cut3`), con commit y push, y resume en español qué has hecho.

## 1. Qué se entrega y quién lo ve

- **Entrega del corte 3 (1 nov):** el manual `mv-3`, ZIP en `~/careerlab-data/entrega/cut3/gradient-depression-mv-3-cut3.zip` (Mac de Alejandro). Lleva `presentation.mp4`, que por ahora es el vídeo del corte 2 (habla de `mv-5r`, hermano de mv-3). **El vídeo nuevo sustituye a ese.**
- **Quién lo ve:** sólo si quedamos entre los 10 primeros de la fase automática. Entonces un jurado experto puntúa el vídeo, `design/skills_design.md`, `design/decision_report.md` y los propios Skills, y esa nota vale el **30 % de la nota final**. Leen el vídeo junto con lo que el Skill dice y hace: **cualquier contradicción resta**.
- **Reglas del vídeo** (`~/huawei/local-runs/official-runner/docs/competition-rules.rst`, apartado *Video presentation*):
  - en inglés;
  - responde a las cinco preguntas **en este orden**:
    1. *How did you think while designing the Skills? Describe the reasoning, not only the finished structure.*
    2. *While debugging your submission, what did you find in the logs of an earlier version that was worth improving, and how did you change it in a later version?*
    3. *Why did you use scripts or reference files in the Skills, or why did you not use them?*
    4. *How general and robust are your Skills? If the environment settings change, how well can the agent adapt?*
    5. *What did this competition lead you to think about the relationship between an agent and agent Skills? What do Skills add for an agent, and where do they fall short?*
  - como mucho 10 minutos, a velocidad normal;
  - basta una persona a cámara; las diapositivas son opcionales;
  - después de las cinco preguntas se puede añadir lo que se quiera.
- **Lo que busca el jurado** (mismo fichero, *Stage 2*): el enfoque de decisión, cómo se reparten las responsabilidades los Skills, qué información pública y qué señales de la partida usa, los riesgos principales que vimos y cómo generaliza más allá del juego de desarrollo.

## 2. Qué leer (rama `alejandro/corte3`)

| Para | Fichero |
|---|---|
| **El Skill entregado** (la fuente de verdad) | `lab/policies-src/mejora/mv-3/bundle/skills/career-rules/SKILL.md` y `bundle/manifest.json` |
| **Documentos entregados** (el vídeo debe decir lo mismo) | `docs/entrega/cut3-mv3/README.md`, `skills_design.md`, `decision_report.md` |
| El día del corte 3, con las partidas | `lab/reports/corte3/README.md` (§2, §6, §7 y Relevo) |
| De dónde sale mv-3 | `lab/reports/mejora/README.md` (§2, §4–§7) |
| Fichas y bucle de dos llamadas | `lab/reports/deepseek/comprobante.md`; HALLAZGOS C51–C59 |
| Todo lo aprendido, por importancia | `HALLAZGOS.md` (sección «Lo esencial»; filas A1–A7, B1, B17, B30, B31, C45, C51, C53, C57, C58, C62, C72) |
| Estado del proyecto | `ESTADO.md` |
| Réplica del juego (método) | `lab/reports/ingenieria-inversa/` (README) |
| Obediencia y «contaminación» de reglas | `lab/reports/transmision/resumen.md` |
| Percepción de DeepSeek | `lab/reports/deepseek/percepcion.md` |
| Tramos fieles (por qué el banco engañaba) | rama `alejandro/tramos`, `lab/reports/tramos/README.md` (resumen en `lab/reports/corte3/README.md`) |
| Todas las partidas pagadas | `lab/data/deepseek/partidas.csv` (78 partidas) y su README |
| Borradores antiguos (cifras viejas: no copiar números) | `docs/entrega/jury-story.md`, `docs/entrega/cut1-t13-read-v4/` |

**No leer** el paquete del motor ni sus datos (NORMAS §4), y no citar en el vídeo títulos de eventos ni texto del juego.

## 3. La historia, en orden

1. **Entender el juego sin mirar dentro.** Una IA vive 48 meses de carrera: 3 historias al mes con efectos ocultos, un reparto de energía cada trimestre y una evaluación cada seis meses. Con nuestras propias partidas construimos una réplica que reproduce el 99,3 % de los pasos y el 99,5 % de los ascensos (B1). La usamos sólo para investigar: nada de ella va al Skill.
2. **Lo que decide la nota** (A1–A3): el nivel y el dinero (que sale del sueldo, es decir, del nivel), ascender en cada ventana y no acumular riesgo oculto. El riesgo sólo se ve por el tono del comentario mensual de RR. HH.: dos explosiones son el despido. Además, un despido seguro si sigues en el primer nivel en el mes 24.
3. **El cuello de botella es la percepción** (A6, B17): DeepSeek reconoce el 83 % de las opciones arriesgadas, pero sólo ~45–49 % de las que suben Skill u Output. Las reglas que mejor se obedecen son las del trimestre; las de historias se obedecen a medias y se cuelan en otras decisiones (A7).
4. **Corte 1 (`t13-read-v4`, 64,75, puesto 13 de 34).** Una guía de lectura de consecuencias, cinco pasos ordenados para cada historia, protección de Skill, Network y Output en los dos meses previos a cada evaluación y una línea de estado como memoria. Gastaba 1,35–1,47 M fichas por mes de juego (nota de fichas ~64).
5. **Las fichas son cuadráticas** (C51–C53). Cada llamada reenvía todo el historial, así que lo que importa es el número de respuestas. Con una respuesta de dos llamadas por decisión (`take_action` + `observe`), el gasto bajó a 0,3–0,7 M por mes (nota de fichas ~89–100). Una redacción del bucle fallaba con un proveedor que no razona en privado; la elegida aguanta con varios.
6. **Corte 2 (`mv-5r`, 45,44).** Nombraba los costes ocultos de las opciones «educadas» sólo en el primer nivel, porque un banco de situaciones grabadas decía que en los demás añadía riesgo. Dos de tres partidas se hundieron en el primer nivel. **Lección:** el banco no reproduce la partida (Skill recién leído, otro prompt, otro muestreo). Construimos los «tramos fieles», que juegan el principio de una partida con la petición exacta del programa.
7. **Corte 3, el último día.** Con lo que quedaba de la clave probamos en partidas reales:
   - una reconstrucción de las reglas del corte 1: mejor en los tramos y con los jueces de calidad, peor en partidas;
   - variantes «valientes» que aceptaban riesgo para subir antes: subían, pero explotaban;
   - **mv-4 frente a mv-3**: el mismo Skill, y mv-4 añade al manifiesto «never end a reply with text only… put the decision in the take_action call, not in prose».

   **Ganó mv-3**, el Skill de nuestras mejores carreras.
8. **Por qué mv-3 (la tesis del vídeo).** Las pruebas baratas (banco, tramos, jueces) nos engañaron varias veces; las carreras completas no. Y una sola frase del manifiesto parece cambiar cómo juega el modelo. Es una hipótesis, sin probar: le quita el razonamiento escrito cuando el proveedor no razona en privado.

## 4. Números verificados (usa sólo estos)

| Qué | Cifra | Fuente |
|---|---|---|
| Notas oficiales | corte 1: 64,75 (`t13-read-v4`); corte 2: 45,44 (`mv-5r`) | marcador oficial; ESTADO |
| Réplica | 99,3 % de pasos, 99,5 % de ascensos, ~0,3 puntos de error en la nota | HALLAZGOS B1 |
| Percepción de DeepSeek | riesgo 83 %; subidas de Skill 45 %, de Output 49 % | B17 |
| Fichas por mes | v4: 1,35–1,47 M (nota ~64); mv-3: 0,49–0,78 M (nota 89–100, media ~96 en completas) | C51, C53; `lab/data/deepseek/partidas.csv` |
| Fórmula de fichas | ≤ 500 mil/mes = 100; ≥ 3 M = 0; lineal entre medias; una partida que no llega al mes 48 tiene 50 como máximo | competition-rules.rst |
| **mv-3 en partidas** | completas 68,64 · **77,78 (L6)** · 66,06 · **74,12 (L6)** · 70,38 · 63,31 · 70,12 (media 70,1); no completas: 1 cortada por el programa (21 respuestas sin llamada), 31,01 (primer nivel hasta el mes 24) | `lab/reports/corte3/README.md` §7; `partidas.csv` |
| mv-4 en partidas | completas 63,35 · 69,62 · 63,27 · 59,99 · 69,70 · 59,47 (media 64,2); no completas: 37,06, 37,39 y 32,73 (crisis de confianza), 18,98 (despido en el primer nivel), 31,34 (ruina) | ídem |
| La trampa del primer nivel | 1.ª evaluación ganada ~52 %; la 2.ª ~46 % de las que fallan la 1.ª; la 3.ª, 1 de 11 (se pierde por el riesgo oculto) | `lab/reports/corte3/README.md` §2 |
| Alternativa «reglas del corte 1 + bucle» | tramos: sale del primer nivel el 79 % (frente al 73 %); partidas: 58,06 · 52,32 · 28,76 · 24,90 · 28,34 | §6 |
| Alternativa «valiente» | 60,62 · 63,02 · 61,53 · 63,62 · 62,73 · 59,89, con explosiones; 19,62 y 41,32 | §7 |
| Advisor con script (otra línea) | mejor partida 76,87 (L6), pero 3 de 7 terminaron antes y gastaba ~1,6 veces más fichas | `docs/entrega/cut3-mv3/decision_report.md` §6 |
| Techo teórico | un planificador con información perfecta saca ~72 de media; L6 vale hasta ~79,6 | B31 |

Todas son partidas de desarrollo con el programa oficial y DeepSeek, **no notas oficiales**. Dilo así en el vídeo.

## 5. Qué debe decir cada respuesta (guía, no texto final)

1. **Diseño.**
   - Tres preguntas en cada decisión: qué cambia probablemente esta opción, qué necesita ahora la carrera y qué regla toca en esta fase.
   - Un solo Skill, porque con varios el agente abría uno y perdía reglas, y el manifiesto repite lo esencial porque el Skill se lee una vez al principio.
   - Una línea de estado como memoria (`Review in N | Now | Best | Reviews here`), pasos ordenados para las historias, el trimestre como «primera línea que aplica» y un plan por nivel.
   - Cada cambio fue una hipótesis con su criterio de descarte.
2. **De los registros a los cambios.** Elige 3 o 4 ejemplos claros:
   - ascensos perdidos por un punto en la última historia, que llevaron a proteger S/N/O antes de la evaluación y al valor Best;
   - arreglos «constructivos» en privado que sumaban riesgo, de donde salió la lista de redacciones arriesgadas;
   - 1,4 M fichas por mes, que se resolvieron con una respuesta de dos llamadas;
   - una carrera cortada por respuestas sin llamada. Probamos una frase en el manifiesto y la quitamos: en carreras reales coincidió con más finales prematuros. Es el ejemplo más honesto de «lo que parecía arreglo empeoró».
3. **Sin scripts ni ficheros de referencia, y por qué.** Los organizadores los permitían si usan sólo datos de la partida.
   - El advisor con script de otra línea tuvo la mejor partida, pero también más finales prematuros y más fichas.
   - Un script con estado no mejoró nada en la réplica (C63).
   - Lo que falla es leer las opciones, y un script no lo resuelve.
   - Menos superficie de revisión.
4. **Generalidad y robustez.**
   - Ningún título de evento ni umbral oculto: todo se apoya en lo que el agente ve (tono de RR. HH., charlas de evaluación, efectos del menú trimestral, sus propias notas) y en el calendario publicado, con una salvaguarda si la charla llega tarde.
   - Probado con varios proveedores del modelo.
   - Límites honestos: la percepción, el calendario de evaluaciones y los proveedores que escriben la llamada como texto.
5. **Agente y Skills.**
   - Los Skills cambian muy bien *cómo* trabaja el agente (el formato redujo las fichas a un tercio) y mal *qué percibe*.
   - Las reglas de historias se cuelan en otras decisiones.
   - Una frase puede cambiar el juego.
   - Hay que medir en condiciones reales: las pruebas baratas engañan.
   - Cierre: los Skills son prioridades y disciplina, no comprensión.

## 6. Qué entregar (en `docs/entrega/cut3-video/`)

1. **Diapositivas** (10–14), en inglés:
   - una idea por diapositiva;
   - pocos números y grandes;
   - un diagrama del bucle de decisión;
   - una línea de tiempo corte 1 → 2 → 3;
   - la tabla mv-3 frente a mv-4.

   En `.pptx`, o en Markdown/HTML si no se puede, con notas del orador.
2. **Guion completo** en inglés con tiempos por bloque: unos 8,5 minutos, sin pasar de 9:30. Frases cortas que se puedan leer en voz alta.
3. **Hoja de comprobación** (en español): cada afirmación del guion con su fuente en este repo, y la confirmación de que coincide con el SKILL.md y los documentos entregados (`docs/entrega/cut3-mv3/`).
4. **Resumen** en español de lo hecho, al final del README de esa carpeta.

## 7. Cosas que no se pueden hacer

- Citar títulos de eventos o texto del juego, o presentar umbrales del motor como reglas («the bar is Skill 8»). Usa «in our runs…».
- Decir que conocemos la nota oficial del corte 3, o presentar notas de desarrollo como oficiales.
- Mencionar el paquete del motor, la réplica como fuente de reglas, ni nada que suene a leer estado oculto.
- Cambiar el Skill o los documentos entregados. Si encuentras una contradicción entre el vídeo y los documentos, **apúntala** en la hoja de comprobación y avisa.
- Mencionar a Claude como contribuidor: el vídeo es del equipo.

## 8. Después: cómo se mete el vídeo en la entrega

Cuando Alejandro grabe el vídeo (`presentation.mp4`, en inglés, ≤ 10 min), se reconstruye el ZIP con el mismo Skill y los mismos documentos:

```bash
uv run python scripts/entrega/build_cut.py --policy lab/policies-src/mejora/mv-3 --cut cut3 --design docs/entrega/cut3-mv3 --video <ruta/al/presentation.mp4>
```

El script comprueba la validación oficial, el inglés, los `TODO`, la duración del vídeo y que el contenido no sea idéntico a un corte ya puntuado. Deja el ZIP en `~/careerlab-data/entrega/cut3/`, que hay que subir antes de las 24:00 UK del 1 nov.
