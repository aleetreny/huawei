# Progreso (hora UTC)

## 26 oct 2026

- 22:20 Encargo de Alejandro: ingeniería inversa del juego con bots, por etapas, partiendo del trabajo de Matteo. Rama `alejandro/ingenieria-inversa`, en el worktree `.claude/worktrees/ingenieria-inversa`, creada desde `origin/main` (3b729ef).
- 22:25 Leídos ESTADO.md (21:38), findings.md, el informe de Matteo (`first-review-search`), el estudio de ascensos, los bots de energía (T10), el análisis de primeros principios (`alejandro/carrera-rapida`, 22:21), el manual del juego y las normas oficiales (`competition-rules.rst`, `rules.rst`, `failure-and-ending.rst`, `mcp.rst`).
- 22:30 Prueba de una partida: unos 7 ms por paso. `check_latest_logs` devuelve la partida entera. Disco: 18 GB libres, así que los datos se guardan comprimidos y sin duplicar textos, fuera de iCloud.
- 22:34 Arnés `scripts/ingenieria-inversa/` (`harness.py`, `policies.py`, `run.py`, `bbdata.py`, `model.py`). Lote de prueba de 40 partidas correcto. Lote **b00**: 20.000 partidas aleatorias con energía segura (4 procesos × 3 servidores, nice 10), a unas 15–22 partidas por segundo.
- 22:50 Hallazgos H1–H4 (techos por nivel, ascenso de L1 casi determinista, señales de riesgo y efectos fijos de las acciones trimestrales) en [hallazgos.md](hallazgos.md).
- 22:55 Oráculo v1 (modelo m01, sólo L1–L2): termina 42 %, nota 48,5; muere sobre todo por crisis de confianza. Lote **b01** lanzado: 6.000 partidas del oráculo v1 con un 10 % de decisiones al azar, para tener datos de L3–L6 con contrafactuales.
- 23:05 Con b00 y el b01 parcial: techos y umbrales de L1 a L5 (H6), notas (H7) y despido (H8). Medida del riesgo a 3 meses por respuesta (H9).
- 23:15 Oráculo v2 (modelo m03, pesos por umbral y castigo de explosiones): 84 % terminadas, nota media 62,7 (H10).
- 23:00 Parado b01 en 2.400 partidas. Lanzado **b02-stages**: 17 brazos × 300 partidas (oráculo v2; al azar sólo los eventos o sólo el reparto trimestral de un semestre).
- 23:05 Etiquetado de las 954 respuestas por rasgos generales (4 agentes Sonnet, en el scratchpad, sin pasar texto al repo) para probar si los rasgos predicen los efectos con títulos reservados (`semantics.py`).
- 23:10 Hallazgos H11–H15: fórmula de la nota final exacta; efectos deterministas; eventos exclusivos de niveles altos; los eventos deciden la partida; umbrales de L4 y L5 (la Skill es el cuello de botella); la 1.ª evaluación se pierde en el último mes. Lanzado **b03-review-boost** (protección del mes previo a cada evaluación ×1, ×5, ×20).
- 23:12 b02 parado con ~112 partidas por brazo; tabla final en H13. b03: proteger el mes previo a la evaluación sube la nota de 61,4 a 66,5 (H17).
- 23:13 Generalización con las 954 respuestas etiquetadas (H16): el carácter de la respuesta predice riesgo, dignidad, salud, Network y Skill con títulos reservados (R² 0,40–0,58), pero no el Output. Lanzado el etiquetado extra de "entrega propia".
- 23:14 b05: dar más peso a la Skill desde L3 no cambia la nota del oráculo (65,3–65,8). Lanzado b06 con el "bot de principios", que usa sólo las predicciones por rasgos, con y sin conocer techos y umbrales.
- 23:15 Borrador de manual `lab/policies-src/bb-mechanics/bb-mechanics-v1` (una Skill, `career-mechanics`): lint sin avisos, sin jugar aún con IA.
- 23:16 Historias de varios pasos: en 94 de 110 preguntas con continuación, la mejor respuesta inmediata es también la mejor contando la historia entera; en las 16 restantes se pierde poco. El Output explica la mayoría de los fallos en la 1.ª evaluación, también en el bot de principios.
