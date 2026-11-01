# Vídeo del corte 3 (`mv-3`)

**Conclusión:** guion de ~8:45 en inglés, presentación animada (artifact y PDF) y hoja de comprobación listos para grabar; todo coincide con el `SKILL.md`, el manifiesto y `docs/entrega/cut3-mv3/`, cuyos documentos se corrigieron en cuatro cifras para que digan lo mismo que el vídeo ([comprobación §4](comprobacion.md)).

Interno, en español. El vídeo y las diapositivas van en inglés. Nada de esta carpeta va en el ZIP salvo el `presentation.mp4` que se grabe.

| Fichero | Qué es |
|---|---|
| [ENCARGO.md](ENCARGO.md) | El encargo: reglas del vídeo, historia, números verificados |
| [guion.md](guion.md) | Guion hablado completo, en inglés, con tiempos por bloque y la diapositiva de cada párrafo (`[Sn]`); notas de grabación al final |
| [presentacion.html](presentacion.html) | **La presentación para grabar** (artifact: https://claude.ai/artifact/8GaV8coHbdR1EeKANBtX4T). 14 diapositivas animadas: cada una se abre como una llamada del agente en la línea de registro y la barra de abajo es la carrera de 48 meses. Flechas o espacio para avanzar, N para las notas del orador (el guion), `#s5` en el enlace abre la diapositiva 5 |
| [presentacion.pdf](presentacion.pdf) | La misma presentación en PDF, una página por diapositiva y sin animaciones |
| [presentacion-b.html](presentacion-b.html) | **Segunda opción** (artifact: https://claude.ai/artifact/YSBvZYSEpuV8zmvXxNPAcJ). Cuaderno de laboratorio: papel cuadriculado, tinta negra y un solo color (subrayador), una frase clave por diapositiva y menos texto, con tono de equipo universitario. Mismas 14 diapositivas en el mismo orden, así que el guion y las notas sirven igual; `#p5` abre la página 5 |
| [presentacion-b.pdf](presentacion-b.pdf) | La segunda opción en PDF |
| [slides.pptx](slides.pptx) | Versión anterior en PowerPoint, con el guion en las notas del orador |
| [comprobacion.md](comprobacion.md) | Cada afirmación con su fuente y su comprobación contra el Skill y los documentos entregados; las diferencias encontradas |
| `scripts/entrega/cut3_video_slides.py` | Genera `slides.pptx`; toma las notas del orador de `guion.md` |
| `scripts/entrega/cut3_video_notes.py` | Copia las notas del orador de `guion.md` a las dos presentaciones |

## Resumen de lo hecho (1 nov)

1. **Lectura.** El encargo entero; el Skill entregado (`lab/policies-src/mejora/mv-3/bundle/`: `SKILL.md` y `manifest.json`, y `diff` con mv-4); los tres documentos de `docs/entrega/cut3-mv3/`; `lab/reports/corte3/README.md`; §2 de `lab/reports/mejora/README.md`; las filas de HALLAZGOS que cita el encargo; las reglas del vídeo en `competition-rules.rst`; y las filas de mv-3, mv-4 y mv-5r de `lab/data/deepseek/partidas.csv`, de donde recalculé notas medias y fichas por mes.
2. **Guion** ([guion.md](guion.md)). Responde a las cinco preguntas en orden, con 40 s de presentación antes y 20 s de cierre después. El hilo: tres preguntas en cada decisión → lo que enseñaron los registros (un punto perdido antes de la evaluación, riesgo «responsable», costes mal leídos, fichas cuadráticas) → la frase de mv-4 que arreglaba el síntoma y empeoró el juego → las pruebas baratas nos engañaron y las carreras completas no → por eso mv-3. Pocas cifras: 83 % frente a ~45–49 %, 64,75 y 45,44 oficiales, 1,4 M → 0,5–0,8 M fichas por mes, 7 de 9 completas con media 70,1 frente a 5 de 11 terminadas antes, 1 de 11 en la tercera evaluación del nivel inicial. 1.266 palabras: ~8:45 a 145 palabras por minuto, 9:05 a 140.
3. **Diapositivas** ([slides.pptx](slides.pptx)). Una idea por diapositiva: el juego, las tres preguntas, el diagrama del bucle de decisión con la línea de estado literal, Skill frente a manifiesto, la línea de tiempo de los tres cortes, registros → reglas, fichas, la tabla mv-3 frente a mv-4, pruebas baratas frente a carreras, scripts, robustez y límites, agentes y Skills, y el cierre. Fuentes Cambria y Calibri. Pasa el validador de la skill de pptx; la revisión visual se hizo con un visor en el navegador (sin LibreOffice en el Mac), así que la tipografía real puede variar un poco en PowerPoint o Keynote.
4. **Hoja de comprobación** ([comprobacion.md](comprobacion.md)). 22 afirmaciones sobre el Skill y 31 de cifras y hechos, cada una con su fuente. Lo del Skill coincide en todo.

## Diferencias con los documentos entregados: corregidas

La hoja de comprobación encontró cuatro diferencias de cifras con `decision_report.md` (mv-4 tenía 11 partidas, no 10; fichas de mv-3 frente a las de «la familia»; la «mejor partida» del advisor; el nivel de la partida 31,01). Alejandro eligió corregir los documentos: cambios en `docs/entrega/cut3-mv3/decision_report.md` (§5c, §6, §8), `skills_design.md` (§7) y `lab/reports/corte3/README.md` (§7), detallados en [comprobacion.md](comprobacion.md) §4. El Skill no cambia, y el vídeo y los documentos dicen ahora lo mismo.

## Relevo

1. **Qué he hecho y por qué.** Las tres piezas del encargo §6 (diapositivas, guion y hoja de comprobación), más este resumen. Rama `alejandro/video-cut3` (worktree `~/huawei-video`), salida de `alejandro/corte3`. Sin DeepSeek, sin API y sin tocar el Skill. En `docs/entrega/cut3-mv3/` sólo se corrigieron cuatro cifras, a petición de Alejandro.
2. **Resultados.** Los ficheros de la tabla de arriba.
3. **Qué queda a medias.** No se ha grabado el vídeo, y el ZIP hay que reconstruirlo desde esta rama (worktree `~/huawei-video`) para que lleve los documentos corregidos. No he podido ver las diapositivas en PowerPoint o Keynote: Keynote pidió una pantalla de alta («Usage Status») y no hay LibreOffice.
4. **Siguiente paso.**
   - Si cambia el guion, copiar las notas a la presentación y volver a publicarla en el mismo artifact; el PDF se rehace con Chrome sin cabecera (servir la carpeta con `python3 -m http.server` y abrirla con `--headless=new --print-to-pdf`):

     ```bash
     python3 scripts/entrega/cut3_video_notes.py
     ```

   - La versión .pptx se regenera así:

     ```bash
     uv run --with python-pptx python scripts/entrega/cut3_video_slides.py
     ```

   - Grabar `presentation.mp4` (≤ 10 min, velocidad normal) y reconstruir el ZIP con `build_cut.py`, como dice [ENCARGO.md](ENCARGO.md) §8. Subirlo antes de las 24:00 UK.
