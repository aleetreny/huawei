# Diario de la revisión

- Inicio: leídos ESTADO.md y las skills planning-with-files y Exa Search. Memoria consultada sin coincidencias de Huawei/CareerLab.
- Consultado el registro de worktrees y conservada la revisión anterior con su PR; creada copia aislada para este diagnóstico.
- Base actualizada a `917565c`, rama propia `alejandro/diagnostico-estrategias`. Sin partidas ni mutaciones del laboratorio.
- Verificados reglamento, reglas públicas, handbook y MCP mediante fuentes oficiales. Exa: cuatro búsquedas de cinco resultados (20 posiciones, no 20 artículos revisados); se excluyen resultados de otros eventos y se consultan tres artículos primarios.
- Análisis offline reproducible: recuentos por origen/actor, supervivencia, notas, consumo, interrupciones e incertidumbre. Las interrupciones con nota nula se conservan fuera del cálculo.
- Reproducido exactamente el ranking #114; probado el cambio de familias manteniendo partidas fijas y el caso robust=false con DORMANT que no bloquea el camino real de decisión.
- Ruta de una Skill F3 inicialmente supuesta incorrecta; localizada con `rg --files` antes de continuar. No se modifican las Skills.
- Cerrado el informe desde primeros principios: objetivo real, supervivencia/crecimiento, transferencia, inferencia incorrecta de techo, causalidad, sensibilidad de familias, protecciones y costes; experimentos priorizados y límites explícitos.
- Main avanzó a 3c1c993 durante el análisis: leído el diagnóstico del bloque 3 y sus tres nuevas hijas F7. Se reconoce el progreso y se priorizan sus contrastes para no duplicar trabajo.
- Verificación: scripts offline ejecutados, recuentos y hashes comprobados, enlaces locales correctos. `uv run pytest -q`: 230 passed, 1 warning (Authlib) in 32.69s. Línea informativa propia finalizada; no se cambian las del equipo ni el plan global.
