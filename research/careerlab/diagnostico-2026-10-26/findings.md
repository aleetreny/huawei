# Evidencia del diagnóstico

## Fuente y alcance

- Base `917565c`, ESTADO.md de las 16:55 UTC. Las cifras son una fotografía guardada y pueden avanzar durante este diagnóstico.
- La última decisión #114 cambia el líder de F3 a F7 tres skills; F7 Y=55,2 frente a F3 recombinada Y=50,9, sin separación clara. La cifra anterior F3 Y=60,2 no describe la última tanda.
- El estado indica 150 partidas con IA y 550 bots; validación con DeepSeek todavía pendiente. Se contrastarán los recuentos y su alcance.
- T13 tiene ahora tres resultados: Q=24,5 (eliminada), 53,6 y 62,0 (completadas), y amplía a seis por su regla ya escrita. No se interpreta como cota matemática.

## Preguntas a resolver

1. ¿Cuánto vale aumentar supervivencia frente a mejorar puntuación de quienes sobreviven?
2. ¿Qué evidencia permite trasladar resultados de Claude al jugador oficial?
3. ¿Se observan acciones y estados con suficiente fidelidad para inferir mecanismos?
4. ¿El asignador implementa lo prometido por el método y el protocolo?
5. ¿Cómo distinguir ruido, un manual malo y un jugador que no lo ejecuta?
6. ¿Qué experimento cambia una decisión al menor coste de cuota y tiempo?

## Primer contraste externo y metodológico

- Fuente oficial leída en directo: página principal del reto. Objetivo: media de tres partidas (80%), diseño (10%), eficiencia de tokens (10%); Stage 2 para top 10, 70% Stage 1 + 30% jurado. La salida final es un único agente en JiuwenSwarm 0.2.4b3.
- GEPA (artículo original, arXiv 2507.19457v2 y repositorio de autores) respalda como mecanismo transferible la reflexión sobre trazas y la mutación dirigida; no prueba que ese método gane este juego ni que los rankings se transfieran entre modelos.
- Primera búsqueda de documentación produjo resultados de otros eventos TechArena: excluidos. Para las reglas se usarán URLs del dominio oficial ya referenciadas por el repo.
- El protocolo ya contempla separación por actor, episodios completos y confirmación: una recomendación no se considerará nueva sólo por repetir esas reglas. Se verificará qué está realmente implementado y aplicado.

## Recuento y primera lectura de los datos

- 308 filas exportadas: 302 desenlaces terminales y seis interrupciones importadas sin nota. Excluir las interrupciones no es tratarlas como derrotas. Hay 150 episodios centrales de IA, uno terminal adicional de Leah y un smoke de infraestructura; 150 bots de infraestructura más 400 de T10 en su propio registro.
- Haiku principal, excluido el smoke: 91 episodios, 45 completados (49,5%), Q media 43,93; entre completados Q=59,81 y entre eliminados Q=28,40. 25 de las 46 eliminaciones llegan al mes 24. Datos mezclados de distintas políticas: descripción, no efecto causal de una intervención.
- Sólo 1 acción rechazada en 13.821 acciones de Haiku. Usar correctamente la herramienta ya no parece el principal límite de este actor.
- Haiku completado: mediana 726,56 s, 197 acciones, 32,32 M tokens contabilizados con caché; 99,2% son lecturas de caché y el tiempo reportado de API representa 98,6% del tiempo de ejecución. Optimizar milisegundos del MCP tiene poco techo frente a llamadas y contexto del modelo.
- Ninguna ruta de traza exportada existe en esta máquina. No implica pérdida: los originales pueden estar en la nube/u otra máquina. Sí limita revisar fallos desde una nueva sesión: se dispone de agregados y de los 14 digests de Opus.
- La comparación guardada Haiku/Opus~100k ya informa Spearman -0,26 en seis políticas. Es una señal de transferencia dudosa con muestras pequeñas, no una correlación estimada con precisión.

## Restricciones útiles para diseñar experimentos

- Las reglas públicas dan costes, efectos direccionales, calendario y salarios; no publican la fórmula de ascenso. El MCP documentado no ofrece semilla, clonación, retroceso o intervención arbitraria en el estado. Un MCTS con ramificaciones exactas no está disponible mediante ese contrato.
- Los salarios publicados crecen de 0,3 por mes en L1 a 1,0 en L5 y 9,1 en L10: una promoción temprana puede aportar ingresos durante meses posteriores. Su valor neto depende de supervivencia y efectos no publicados, no sólo de la recompensa final.
- La puntuación automática de diseño evalúa el promedio de los SKILL.md; los documentos design/ cuentan para el jurado. Son objetivos distintos que ESTADO.md resume de forma imprecisa.
- Cada actor observado usa skills_mode=inline. El cuerpo de todas las Skills se añade al system prompt en `render_system_prompt`; eso reduce la fidelidad de experimentos sobre descubrimiento/carga de Skills respecto al sistema objetivo.
- `block_decision` calcula robustez, pero no transforma acciones en INCONCLUSIVE cuando falla; tampoco invoca alarmas de interrupción ni comprueba que el actor tenga autoridad de selección. El driver registra ese resultado. La última decisión #114 sí indica robustez positiva: el riesgo detectado en el código no demuestra que esa decisión concreta sea incorrecta.

## Sensibilidad y precisión

- Reproducción offline del ranking con las exportaciones: la agrupación registrada devuelve exactamente F7 Y=55,2059, F3 recombinada Y=50,8966 y dos dormidos. Usando una familia por política, F3 recombinada pasa a Y=58,49 y F7 a 57,77; aparecen ocho dormidos. Una sola familia común deja cero dormidos. Es sensibilidad a supuestos, no evidencia de que la alternativa sin agrupación sea mejor.
- Con la dispersión observada dentro de las políticas de Haiku, SD de Y≈16,14, el cálculo aproximado del protocolo para distinguir Δ=4 con potencia 80% y alfa unilateral 10% pide unas 147 partidas por brazo. Sirve para planificar, no como regla de parada; cuatro o cinco partidas son exploración.
- Para Haiku agrupado, un escenario que suba supervivencia 10 puntos porcentuales manteniendo las medias condicionales daría +3,14 Q; subir 5 Q sólo a los supervivientes daría +2,47 Q. No son efectos causales: las carreras rescatadas pueden diferir de las observadas.
- Reproducción del fallo de integración usando el caso de colapsos de `tests/test_stats.py`: el cálculo devuelve robust=false y, simultáneamente, DORMANT para X. Sólo se sustituye la carga de datos por un objeto en memoria; el cálculo real de robustez se ejecuta con semilla 0, sin registro ni juego. Resultado guardado en model-sensitivity.json.
- El módulo de búsqueda sintética sí consulta la robustez antes de aplicar ciertas decisiones. El camino cloud pasa por otro módulo (`decisions.block_decision`): los resultados del juguete y sus tests no garantizan la misma protección de extremo a extremo en producción.

## Actualización al cerrar, sin mezclar cohortes

- Main avanzó a `3c1c993` (17:19 UTC). Se leyó su diagnóstico de 38 digests y diff; no cambia los módulos de robustez, registro o actor revisados. Las tres hijas F7 propuestas por la nube ya cubren tendencias, historias de entrega y búsqueda de ascensos: priorizar sus contrastes, sin duplicarlos.
- La separación por primer ascenso es observacional. La variable «good review» incluye B o ascenso; varias revisiones de una partida están correlacionadas. El máximo del diagnóstico utiliza toda la muestra por nivel, mientras que el manual propone un máximo reciente propio: comprobar que la intervención sigue el mecanismo.
- La misma actualización corrige implícitamente la idea de que una B evita cualquier salida al mes 24: hay una crisis de confianza en una carrera con B. Su cohorte contiene 11 despidos, frente a los 14 citados en ESTADO.md. Documentar causa, denominador y cohorte antes de convertirlo en una regla general.
