# Evidencia para la sección de ideas

- PR #3 integrada en main el 26 oct, 18:33:34 UTC; nueva rama basada en main `305762a`.
- `origin/Matteo` (`b6e1d63`) conserva el informe `docs/exploratory-findings.md`: 73.858 partidas, 1.563.578 acciones, 0 completadas, supervivencia media 5,91 meses y máximo 24. Muestra principalmente situaciones iniciales, no carreras completas.
- El informe dice explícitamente que el lote principal conserva agregados, no trayectorias individuales ni atribución causal de acciones. El helper de partidas manuales sí escribe `observations.jsonl`, pero eso no demuestra que se conservaran las acciones del lote aleatorio.
- Los bots T10 ya exploran repartos de energía: 400 partidas, historias con primera opción y resultados muy dependientes de esa política. Evitar repetir esa pregunta sin una hipótesis nueva.
- Reformular hallazgos como prosa no basta por sí solo para cumplir reglas: verificar la frontera entre lecciones generales y conocimiento específico/umbrales antes de afirmar conformidad.

## Reglas verificadas de nuevo

- Fuente primaria accesible: GitHub oficial `RAI-Internal/techarena-career-sim`, `docs/competition-rules.rst` (blob `1c419d95c0dcac690e0d3a966b3e8f39cb7ad340`) y `docs/mcp.rst` (blob `3c11a7e4a5230d6d36765bffb65eb14c4f3f33c8`), consultados el 26 oct 2026.
- Se permite inspeccionar outputs propios y usar otro cliente MCP por stdio en desarrollo. No hay en esas páginas autorización explícita para miles de juegos automatizados ni un límite de tasa; la norma indica consultar métodos no abordados con organizadores. ESTADO recoge la decisión previa de no preguntar en Discord: no se manda mensaje ni se transforma esa decisión interna en aprobación oficial.
- No se permiten mapas de eventos/respuestas, reconstrucciones del dataset ni lógica que reconozca un evento y devuelva una respuesta fija; tampoco reglas internas no publicadas presentadas como conocidas. La prohibición no depende de cómo se haya obtenido o redactado el conocimiento. Estrategias generales deben apoyarse en documentación pública e información/feedback de la partida actual.
- La propuesta es técnicamente viable y metodológicamente útil si mide aleatorización, estado y cobertura. Su escala masiva y cualquier transferencia de conocimiento específico no se certifican como conformes. En esta tarea sólo se documenta, sin ejecutar ni contactar organizadores.
