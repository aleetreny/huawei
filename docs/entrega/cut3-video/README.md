# Vídeo del corte 3 (`mv-3`)

**Conclusión:** guion de ~8:45 en inglés, 14 diapositivas y hoja de comprobación listos para grabar; todo lo que dicen del Skill coincide con el `SKILL.md`, el manifiesto y `docs/entrega/cut3-mv3/`, pero antes de grabar hay que decidir cuatro diferencias de cifras con `decision_report.md` ([comprobación §4](comprobacion.md#4-diferencias-con-decision_reportmd-avisar-a-alejandro)).

Interno, en español. El vídeo y las diapositivas van en inglés. Nada de esta carpeta va en el ZIP salvo el `presentation.mp4` que se grabe.

| Fichero | Qué es |
|---|---|
| [ENCARGO.md](ENCARGO.md) | El encargo: reglas del vídeo, historia, números verificados |
| [guion.md](guion.md) | Guion hablado completo, en inglés, con tiempos por bloque y la diapositiva de cada párrafo (`[Sn]`); notas de grabación al final |
| [slides.pptx](slides.pptx) | 14 diapositivas (16:9), con el guion de cada una en las notas del orador |
| [comprobacion.md](comprobacion.md) | Cada afirmación con su fuente y su comprobación contra el Skill y los documentos entregados; las diferencias encontradas |
| `scripts/entrega/cut3_video_slides.py` | Genera `slides.pptx`; toma las notas del orador de `guion.md` |

## Resumen de lo hecho (1 nov)

1. **Lectura.** El encargo entero; el Skill entregado (`lab/policies-src/mejora/mv-3/bundle/`: `SKILL.md` y `manifest.json`, y `diff` con mv-4); los tres documentos de `docs/entrega/cut3-mv3/`; `lab/reports/corte3/README.md`; §2 de `lab/reports/mejora/README.md`; las filas de HALLAZGOS que cita el encargo; las reglas del vídeo en `competition-rules.rst`; y las filas de mv-3, mv-4 y mv-5r de `lab/data/deepseek/partidas.csv`, de donde recalculé notas medias y fichas por mes.
2. **Guion** ([guion.md](guion.md)). Responde a las cinco preguntas en orden, con 40 s de presentación antes y 20 s de cierre después. El hilo: tres preguntas en cada decisión → lo que enseñaron los registros (un punto perdido antes de la evaluación, riesgo «responsable», costes mal leídos, fichas cuadráticas) → la frase de mv-4 que arreglaba el síntoma y empeoró el juego → las pruebas baratas nos engañaron y las carreras completas no → por eso mv-3. Pocas cifras: 83 % frente a ~45–49 %, 64,75 y 45,44 oficiales, 1,4 M → 0,5–0,8 M fichas por mes, 7 de 9 completas con media 70,1 frente a 5 de 11 terminadas antes, 1 de 11 en la tercera evaluación del nivel inicial. 1.266 palabras: ~8:45 a 145 palabras por minuto, 9:05 a 140.
3. **Diapositivas** ([slides.pptx](slides.pptx)). Una idea por diapositiva: el juego, las tres preguntas, el diagrama del bucle de decisión con la línea de estado literal, Skill frente a manifiesto, la línea de tiempo de los tres cortes, registros → reglas, fichas, la tabla mv-3 frente a mv-4, pruebas baratas frente a carreras, scripts, robustez y límites, agentes y Skills, y el cierre. Fuentes Cambria y Calibri. Pasa el validador de la skill de pptx; la revisión visual se hizo con un visor en el navegador (sin LibreOffice en el Mac), así que la tipografía real puede variar un poco en PowerPoint o Keynote.
4. **Hoja de comprobación** ([comprobacion.md](comprobacion.md)). 22 afirmaciones sobre el Skill y 31 de cifras y hechos, cada una con su fuente. Lo del Skill coincide en todo.

## Diferencias encontradas (no he tocado los documentos entregados)

- **D1 (la importante):** `decision_report.md` §5c dice que mv-4 terminó antes en «five of ten» y no lista la partida 59,47; en `partidas.csv` hay 11 partidas de mv-4 (6 completas, media 64,2), como dice el encargo. El vídeo dice 5 de 11. Arreglar el informe antes de reconstruir el ZIP o, si no, cambiar el vídeo a «about half».
- **D2:** el informe da 0,46–0,70 M fichas por mes para «la familia»; mv-3 solo gasta 0,49–0,78 M. Los documentos dicen «a third» y «two thirds» del corte 1; para mv-3 es ~43 %. El vídeo dice «on average, less than half».
- **D3:** `decision_report.md` §6 llama a la mejor partida del advisor «our best single career», pero mv-3 tiene una mejor (77,78 frente a 76,87).
- **D4:** la partida 31,01 de mv-3 figura «at the starting level at month 24» en el informe, pero `partidas.csv` dice L2. El vídeo no entra en el detalle.

## Relevo

1. **Qué he hecho y por qué.** Las tres piezas del encargo §6 (diapositivas, guion y hoja de comprobación), más este resumen. Rama `alejandro/video-cut3` (worktree `~/huawei-video`), salida de `alejandro/corte3`. Sin DeepSeek, sin API y sin tocar el Skill ni `docs/entrega/cut3-mv3/`.
2. **Resultados.** Los ficheros de la tabla de arriba.
3. **Qué queda a medias.** Las diferencias D1–D4 las tiene que decidir Alejandro. No se ha grabado el vídeo. No he podido ver las diapositivas en PowerPoint o Keynote: Keynote pidió una pantalla de alta («Usage Status») y no hay LibreOffice.
4. **Siguiente paso.**
   - Decidir D1 (y, si se quiere, D2–D4) en `docs/entrega/cut3-mv3/decision_report.md`.
   - Si cambia el guion, regenerar las diapositivas para que las notas sigan el texto:

     ```bash
     uv run --with python-pptx python scripts/entrega/cut3_video_slides.py
     ```

   - Grabar `presentation.mp4` (≤ 10 min, velocidad normal) y reconstruir el ZIP con `build_cut.py`, como dice [ENCARGO.md](ENCARGO.md) §8. Subirlo antes de las 24:00 UK.
