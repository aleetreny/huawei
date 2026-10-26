# IDEA-03 — aprender de decisiones aleatorias instrumentadas

**Sí es viable técnicamente; hay que precisar qué se aprende y qué se puede trasladar al manual.** La propuesta es registrar decisiones y sus contextos para descubrir hipótesis generales. No crear un banco de respuestas para reconocer eventos del dataset.

## Qué existe en la rama de Matteo

Revisado `origin/Matteo`, commit `b6e1d638c4f48ef6983f0834bea428783f19f084`:

- [Resumen publicado](https://github.com/aleetreny/huawei/blob/b6e1d638c4f48ef6983f0834bea428783f19f084/docs/experiments/random-baseline-summary.json): **73.858 partidas**, **1.563.578 acciones**, 4 horas, supervivencia media **5,91 meses**, máximo **24**, **0** carreras de 48 meses. Q media 11,78.
- [Informe](https://github.com/aleetreny/huawei/blob/b6e1d638c4f48ef6983f0834bea428783f19f084/docs/exploratory-findings.md): las opciones se muestrearon uniformemente; la semilla controla la selección de acciones, no los eventos del simulador. El propio informe declara que el lote conserva agregados y no trayectorias individuales ni análisis causal de decisiones.
- [Helper manual](https://github.com/aleetreny/huawei/blob/b6e1d638c4f48ef6983f0834bea428783f19f084/tools/local-game/manual_session.py): escribe observaciones en `.career-lab/runs/<session_id>/observations.jsonl`. Es otro flujo: no prueba que guardara el historial de 1,56 millones de acciones aleatorias.

**Conclusión verificable:** el repo prueba que la corrida existió, pero los artefactos publicados no bastan para estudiar repetición y efecto de cada decisión. Puede haber logs propios adicionales en la máquina que la ejecutó; no se ha comprobado su existencia. No se intenta recuperarlos leyendo archivos internos del simulador.

Tampoco debe mezclarse el lote automáticamente con CareerLab: el informe cita FastMCP 4.1.3 y el adapter anterior; CareerLab congela otra configuración. La equivalencia de entorno no está establecida. Los [400 bots T10](../../lab/reports/energy-bots/README.md) responden otra pregunta, sobre repartos de energía con una política de historias fija.

## Qué significa «contribuye al score»

Hay tres preguntas distintas:

1. **Repetición y cobertura:** qué situaciones aparecen, con qué opciones y en qué estados/niveles. Agrupar sólo por título puede mezclar fases o listas de opciones distintas.
2. **Cambio próximo:** cómo cambia el estado hasta la siguiente observación tras una opción. Debe distinguirse si cruza un mes o incluye evaluaciones u otros sucesos.
3. **Consecuencia posterior:** cómo cambia Q o la probabilidad de completar después de elegir una opción. Depende del contexto, de lo que ocurra después y de la política que siga jugando.

El Q terminal no se reparte de forma aditiva entre preguntas. Las acciones pueden tener efectos diferidos, modificar qué eventos llegan a verse o intercambiar salud por crecimiento. No hay un «valor fijo» de cada pregunta que pueda sumarse a los demás.

Si la elección está realmente aleatorizada entre opciones factibles y se registra su probabilidad, se pueden comparar sus resultados en la población de encuentros alcanzada por ese explorador. Los sucesos repetidos de una partida siguen relacionados: incertidumbre agrupada por partida y soporte por contexto, no millones de réplicas independientes. Un efecto bajo continuación aleatoria tampoco es automáticamente el efecto bajo un buen jugador.

## Cómo recoger datos que sí sirvan

Para **cada** decisión, guardar en un log externo propio de outputs oficiales:

- job, sesión, origen y configuración exacta del actor/entorno, además de semilla del selector y versión de código;
- una observación nueva antes de actuar, con estado visible, fase, texto/opciones recibidos y sus identificadores de llamada;
- conjunto realmente factible, opción seleccionada y probabilidad condicional conocida; si es uniforme, `1 / número de opciones factibles`;
- respuesta de la acción, rechazos/reintentos y una observación nueva posterior; sin reutilizar un estado viejo;
- resultado terminal de la carrera, supervivencia e interrupciones operativas por separado.

Un pseudocódigo de diseño, no un programa ejecutado:

```text
observar → registrar opciones y contexto → sortear una opción factible
→ registrar probabilidad → actuar → observar y registrar de nuevo
→ continuar con la política de continuación declarada → guardar resultado terminal
```

Una falta de energía no debe convertirse en una elección aplicada. La probabilidad registrada debe corresponder a la selección efectiva, incluyendo cualquier filtro o fallback. No se fabrican estados, clones ni semillas del motor: la interfaz pública no los ofrece.

Las historias completas, si se conservan para estudio, quedan en almacenamiento privado de investigación y fuera de la entrega. La tabla analítica puede usar hashes, categorías generales y números. La deduplicación exacta separa título, opciones y contexto; un agrupamiento semántico sólo etiqueta familias de situaciones, no produce un mapa de respuestas.

## Por qué no empezaría por miles de partidas totalmente ciegas

El lote de Matteo ya muestra el problema: la mayoría muere pronto. Más volumen de ese mismo tipo visita muchas veces el comienzo y casi nunca los niveles altos. Además, una continuación aleatoria puede destruir los beneficios tardíos de una decisión que sería útil en una buena estrategia.

Orden propuesto:

1. **Recuperar y auditar una muestra de logs propios existentes**, antes de repetir trabajo. Comprobar que contienen estado, opciones, acción y resultado enlazables; el resumen agregado no puede reconstruirlos.
2. Si falta información, **diseñar un piloto pequeño con instrumentación correcta**, y medir variedad de estados, opciones comparadas y cobertura tardía. Aumentar volumen sólo si añade información útil, con presupuesto de sesiones/tasa y alcance documental explícitos.
3. Como variante posterior, explorar algunas decisiones desde una estrategia base que sobreviva mejor, sorteando entre opciones disponibles en momentos predeclarados y registrando las probabilidades. Si hay restricciones de seguridad, la conclusión se limita a los estados/opciones donde se exploró; no se extrapola a los excluidos.
4. Agrupar observaciones por propiedades generales —entrega, colaboración, recuperación, transparencia, riesgo— y producir hipótesis, no respuestas por evento.
5. Probar la regla candidata como cambio de una instrucción en partidas nuevas, con un jugador real y Y completo. Confirmar después según v1.

Esta segunda variante es una política experimental distinta; debe tener identidad propia y no alterar silenciosamente la carrera ni sus probabilidades. No hay una acción recomendada ni un collector implementado en esta PR.

## Qué podemos afirmar sobre las reglas

Verificado el 26 oct en las fuentes oficiales de [fair play](https://github.com/RAI-Internal/techarena-career-sim/blob/main/docs/competition-rules.rst) y [MCP](https://github.com/RAI-Internal/techarena-career-sim/blob/main/docs/mcp.rst):

- Inspeccionar salidas propias y conectar otro cliente por stdio están contemplados.
- La entrega debe razonar con la información de la partida actual. No puede llevar respuestas memorizadas por evento ni reglas internas no publicadas presentadas como conocidas; reformularlas en prosa no elimina la prohibición.
- Las estrategias generales deben seguir siendo aplicables si cambian texto, orden o parámetros.
- Esas páginas no autorizan explícitamente lotes automatizados masivos. Para métodos no abordados, la norma remite a los organizadores. La decisión interna de ESTADO de no preguntar en Discord no equivale a autorización oficial; se conserva sin contactar a nadie.

Por tanto, no certificamos «miles de interacciones para recuperar reglas y luego escribirlas» como permitido sin más. Sí podemos documentar la propuesta y analizar outputs propios ya existentes, manteniendo aparte la incertidumbre sobre escala y conocimiento transferible. Un aprendizaje razonable para contrastar sería «compara costes de bienestar y progreso con el estado y feedback actuales»; no «reconoce esta trama y elige la opción aprendida».

## Qué debilitaría esta idea

- Los logs existentes no contienen decisiones individuales, o sus estados no se pueden alinear.
- Aumentar la muestra repite sólo estados iniciales y no mejora cobertura relevante.
- La acción depende de opciones/contextos sin solapamiento comparable, o sus probabilidades no están registradas correctamente.
- Una supuesta lección sólo funciona ante un evento concreto o requiere umbrales internos aprendidos.
- La regla general obtenida no mejora Y en partidas frescas con un jugador pertinente.

**Estado:** propuesta por investigar; no lanzada. El próximo paso es una auditoría de logs propios, no otra corrida de miles de juegos.
