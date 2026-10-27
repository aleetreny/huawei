# Fuentes y alcance

Consultadas el 26 de octubre de 2026. Búsqueda con Exa: cuatro consultas de cinco posiciones, 20 resultados solicitados antes de deduplicar. No equivale a 20 fuentes íntegramente verificadas. Una búsqueda de documentación devolvió eventos TechArena ajenos al juego y otros sitios; se excluyeron. Se validan los hechos del juego en el dominio oficial y los métodos en artículos originales.

## Documentación oficial leída

- [Inicio](https://techarena-career-sim.readthedocs.io/en/latest/): plataforma, modelo, proceso y objetivo.
- [Reglas y fair play](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html): puntuación, ejecución de un agente, conocimiento y conductas permitidos. El diagnóstico conserva las decisiones de autorización ya registradas por el equipo y no inicia nuevos métodos de acceso.
- [Reglas públicas](https://techarena-career-sim.readthedocs.io/en/latest/rules.html): costes de energía, efectos direccionales, salarios, desempeño y ascensos.
- [Handbook](https://techarena-career-sim.readthedocs.io/en/latest/handbook.html): estado visible y límites de información pública.
- [MCP](https://techarena-career-sim.readthedocs.io/en/latest/mcp.html): cinco herramientas y argumentos; sin semilla ni clonación documentadas.

## Investigación primaria

- [Agrawal et al., GEPA, arXiv:2507.19457, versión 2](https://arxiv.org/abs/2507.19457), y [repositorio de autores](https://github.com/gepa-ai/gepa): reflexión sobre trazas, cambios de instrucciones y conservación de soluciones complementarias. No demuestra rendimiento en Career Survival.
- [Agarwal et al., Deep Reinforcement Learning at the Edge of the Statistical Precipice, arXiv:2108.13264](https://arxiv.org/abs/2108.13264): problemas de evaluación con pocas ejecuciones e incertidumbre. Sus agregados multijuego no sustituyen la media oficial de tres carreras.
- [Filstroff et al., Targeted Active Learning for Bayesian Decision-Making, arXiv:2106.04193](https://arxiv.org/abs/2106.04193): orientar adquisición de información a decisiones. Transferimos el principio, sin afirmar optimalidad de una implementación aún no medida en este juego.

## Evidencia interna principal

ESTADO.md; findings.md; protocolo v1; method-decision.md; target-budget.md; informes cloud, T10, T13 y destilación; exportaciones JSONL del laboratorio; módulos de ejecución, registro, análisis, decisión y búsqueda; tests estadísticos. Los dos scripts de esta carpeta analizan datos propios sin llamar al juego ni inspeccionar sus componentes internos.

Al cerrar se revisó también el avance `3c1c993` de main (17:19 UTC), en particular [block3-generation.md](https://github.com/aleetreny/huawei/blob/3c1c993/lab/reports/historico/cloud-run-diagnostics/block3-generation.md). Se incorpora como actualización cualitativa; no se mezclan sus nuevas evaluaciones con los descriptivos de la base `917565c`.
