# Auditoría adversarial del corte 2

**Conclusión: no empaquetar cp-v5a tal como está; corregir primero las afirmaciones sobre reglas no publicadas y los documentos, conservando como candidato de referencia sus tres partidas, sin atribuir sus resultados a una variante corregida.** No hay evidencia suficiente para preferir v4-c5 con el bucle nuevo sólo por el banco de L1.

29 de octubre de 2026. Auditoría de lectura y lint, sin llamadas a modelos ni partidas. No se abre una línea ni se modifica el candidato. Fuentes: `alejandro/comprobante`, commit `2a199cb66100528558dc3609b7327a8614f92ba9`, leído en `~/huawei-comp`; documentos de entrega y reglas públicas en `~/huawei`. Los números de línea siguientes corresponden a esa instantánea. El reglamento es la referencia; que una instrucción funcione en desarrollo no acredita que esté permitida.

## Cambios por gravedad

### Corrección: contadores publicados en el handbook de la partida

Retiro el P0 que calificaba ambos contadores de no publicados. `show_employee_handbook` sí publica «two weak half-year reviews» y «after a second blow-up»; copia en `lab/data/transmision/handbook.md:141–147`. Mi revisión inicial se limitó incorrectamente al resumen RST. La cita adecuada es: “Source: in-game employee handbook, returned by show_employee_handbook, Risk and failure → Ways people say a run ends.” Añadir la ruta de la copia en los documentos de diseño permite comprobarla sin añadir archivos al bundle.

Esto no acredita la equivalencia entre dos reviews sin promoción y dos reviews débiles, ni la frase «the next one is the last chance». Son inferencias adicionales del candidato: no atribuirlas al handbook. No se propone alterar el contador publicado ni el manual en este encargo.

### P0. Retirar la garantía de numeración futura y el trimestre ejecutado a ciegas

`SKILL.md:24,61`, también `manifest.json:5`: «The Energy choices and the main-action choices keep the same numbers every quarter» justifica enviar acciones de fases que aún no se han observado. Los documentos públicos describen las acciones y costes, pero no garantizan esos identificadores estables. La elección debe basarse en las opciones devueltas durante la partida, no en un patrón memorizado del entorno de desarrollo.

**Cambio:** conservar, sujeto al orden de ejecución del runner, la pareja de una acción actualmente ofrecida y su observación posterior. Obtener opciones actuales antes de elegir la siguiente acción de energía o la acción principal. No preemitir todo el trimestre basándose en números de otras fases. Si se conserva un lote más largo, debe acreditarse que todas sus elecciones y precondiciones están expuestas por la interfaz actual; la mera repetición en desarrollo no basta. Esta corrección puede reducir el ahorro de fichas: no reutilizar 94,58 como resultado medido de ella.

### P1. Corregir el calendario presentado como mecánica conocida

`SKILL.md:14,18,37,55,57–58,62`: las evaluaciones semestrales y el horizonte de 48 meses son públicos; que la evaluación ocurra al **entrar** en el mes, y que las decisiones del mes anterior sean las últimas que cuentan, no queda establecido por ello. El handbook enumera historias y trimestre antes de evaluación. «a single lost point ... can cost the promotion» no permite deducir distancia a un umbral de ascenso.

**Cambio:** describir preparación anticipada como política propia y reaccionar a las evaluaciones que efectivamente aparezcan. Eliminar ejemplos 6/12/18, 47 y el disparador concreto 48 del manual, usando horizonte final y feedback; mantener las constantes públicas sólo donde informan del horizonte y periodicidad. No presentar `6 - month mod 6` como reloj exacto del motor. La norma interna §4 es además más conservadora con los meses concretos que el reglamento.

### P1. Sustituir los documentos de entrega, que todavía explican v4

`docs/entrega/cut2/skills_design.md:3–5,25–34,48,52–59,71,75–84`; `decision_report.md:3,53,69,86–90`; README también contiene TODO.

**Cambios concretos:** identificar el paquete final; reemplazar `Stalled`, `Concerns this month` y `Expect` por la memoria que realmente quede; explicar la pareja de llamadas, la excepción de riesgo, la prioridad de Skill desde L4 y el tratamiento de recuperación; corregir «una acción y observar» frente al lote trimestral del original. No documentar una variante deseada como si fuera el archivo entregado. Quitar todos los TODO. Reservar «Cut 1» para v4 y poner cp-v5a en la tabla principal de resultados del candidato. Si se modifica por esta auditoría, nombrar la revisión y declarar que las tres carreras pertenecen al padre.

### P1. No presentar supuestos semánticos como una escala conocida de riesgo

`SKILL.md:43–49,54`: la introducción advierte que son hipótesis de lectura; eso ayuda, pero la frase «postponing ... is a smaller risk than ...» vuelve a afirmar magnitudes relativas como un hecho. El reglamento también alcanza paráfrasis y reglas indirectas.

**Cambio:** decidir entre opciones de riesgo incierto por reversibilidad, exposición y evidencia en la situación actual; eliminar la jerarquía fija de magnitudes. Revisar las listas de consecuencias para que sean preguntas sobre el texto y no una tabla disimulada de efectos del catálogo. No aparecen títulos, IDs ni tablas de respuestas para eventos concretos en los dos archivos inspeccionados; eso no certifica el origen lícito de todas las generalizaciones.

### P2. Aclarar márgenes de política y prioridad de instrucciones

`SKILL.md:63,66–67`: 4/10 y tres meses son márgenes propios explícitos, no una afirmación directa de umbral del juego. **No los califico automáticamente de infracción oficial.** Sin embargo, activan REVIEW y chocan con la petición interna de evitar umbrales y meses concretos. Cambio conservador: salud/dignidad bajas o en descenso sostenido, basadas en observaciones y avisos, sin corte numérico. L4 es un nivel público y su descripción permite una estrategia de desarrollo técnico; no prueba que sea el momento óptimo de cambiar ni un cuello de botella oculto. Explicar esa distinción.

`SKILL.md:21–24,32` y manifest: sustituir los absolutos «never», «exactly two», «no text» por la regla normal durante una decisión válida, con excepciones para arranque, lectura del Skill, recuperación, error, final y requisitos superiores del runner. El manifest parece exigir exactamente dos llamadas a toda situación antes de introducir su excepción trimestral. No prohibir consultar el handbook si hace falta resolver incertidumbre. «Sólo una respuesta permite mantenerse dentro del presupuesto» es una afirmación excesiva, no una restricción publicada.

### P2. Corregir las conclusiones de evidencia y reconciliar el informe fuente

- El banco de L1 es una señal desfavorable; retirar «no es una regresión ... es la moneda al aire» como conclusión demostrada. La alta coincidencia no mide el coste de las pocas discrepancias.
- El informe Comprobante §5.4 y §6.1 discrepa en ascensos de cp-v5a 3 (42 frente a 48), y contiene cierres antiguos de «ninguna hundida». No copiar esa cronología sin reconciliarla con las trazas.
- El Relevo aún enumera ocho notas mientras dice nueve carreras y mantiene cp-v8 con una sola pese a su segunda carrera en el cuerpo. Son errores de actualización del informe, no motivo para alterar las notas verificadas de cp-v5a.
- Eliminar «never on a single [reading]» de `decision_report.md:40`: no está acreditado para todos los brazos. Distinguir réplicas del control de repeticiones de cada candidato.
- No extrapolar calidad Claude a calidad oficial, ni +3,3 de nota automática a una comparación causal de políticas: es una cuenta condicional a igual juego y calidad comparable.

## Revisión de todo el manual y manifest contra las reglas

La tabla cubre las unidades del texto, incluidas las que no requieren cambio. Líneas del Skill salvo indicación.

| Texto | Juicio y acción |
|---|---|
| 1–6, front matter y descripción | Estructura e inglés correctos; un solo Skill. «failure limit» debe leerse como dirección de riesgo, no un umbral conocido. |
| 8–11, fases, relectura y procedencia | Separación de fases y feedback del juego correctos; el descargo de supuestos no ampara reglas ocultas posteriores. |
| 13–18, panorama | Horizonte y niveles públicos; corregir contadores, precisión temporal y consecuencias exactas (P0/P1). |
| 20–32, bucle y ejemplo | Sólo herramientas oficiales del juego. Pareja acción/observación defendible; lote con IDs futuros no; excepciones operativas necesarias. |
| 34–40, memoria | Now/Best son observaciones propias, no alteración de logs. Best=Now al perder memoria es recuperación conservadora; reiniciar contador a cero pierde historia. Revisar reloj y retirar disparador de despido. |
| 42–49, guía de lectura | Es legítimo inferir consecuencias del texto actual; no convertir correlaciones del catálogo en resultados garantizados. HR no debe llamarse «only gauge»: también hay avisos, eventos y cambios observados. |
| 51–52, cascada y supervivencia | Prioridad general permitida; cero de salud es dirección pública. |
| 53–55, riesgo | Evitar ocultación y priorizar reparación es estrategia general; quitar contador, escala fija y certeza del calendario. La excepción de riesgo es preferencia propia, no permiso para evadir reglas. |
| 56, bienestar | Direcciones públicas; riqueza negativa y Network cero son observables, no indican por sí solos muerte inmediata. |
| 57–58, proteger y crecer | Ponderar una señal observada es heurística propia; no son fórmulas del motor. Revisar calendario. No inventar una carencia explícita si la charla no la expresa. |
| 60–62, trimestre y cierre | Acciones y presupuesto públicos; quitar preejecución de opciones no observadas y fecha del último review. |
| 63, recuperación | Márgenes declarados propios, pero eliminar cifras para la entrega conservadora; Lay low por salud debe coincidir con efectos visibles/publicados. |
| 64, HR | Clasificación por tono es transferible si se hace desde texto actual; los ejemplos no deben convertirse en identificadores de plantilla. Quitar rescate condicionado a dos reviews. |
| 65, charla sobre carencia | Condicional admisible si la charla realmente lo dice; no interpretar feedback genérico como diagnóstico cuantitativo. |
| 66–67, Skill desde L4 | Nivel público, preferencia propia; no atribuir su eficacia a un umbral oculto ni omitir excepciones anteriores. |
| Manifest 1–6 | Modo agent, equipo y nombre correctos; sincronizar bucle y prioridad con el Skill corregido. La exclusión genérica de opciones privadas debe explicitar la excepción para evitar contradicción con su instrucción posterior. |

## El bloque literal y «decide en silencio»

**No encuentro una prohibición de agrupar llamadas o de omitir prosa en sí.** La prohibición precisa es explotar un error o comportamiento inesperado **para eludir la simulación o las reglas** (`competition-rules.rst:477–499`). Aquí una acción seguida de observar puede seguir aplicando exactamente las transiciones del servidor, con sus resultados y consumo real contabilizados. La eficiencia de fichas es un componente explícito de la evaluación (185–198). Reducir llamadas al modelo e historia redundante tiene una explicación legítima.

El disparo del formato por la palabra literal `tool_calls` no demuestra un exploit; tampoco demuestra autorización general para cualquier lote. La defensa debe apoyarse en mantener las interfaces, estado y contabilidad, no en «descubrimos que el runner lo tolera». Silencio significa no generar narración redundante, no ocultar errores, resultados o evidencias. La nota sigue describiendo lo observado y la razón breve. No pedir alterar uso de tokens, borrar historia, falsificar logs ni suprimir instrucciones superiores.

**Texto inglés propuesto para skills_design, sólo tras ajustar el candidato a esta descripción:**

> During ordinary story decisions, the agent requests an available action and a subsequent observation in one assistant response. The official runner executes the calls in order; each action still passes through the official MCP interface and its normal validation, state transition and logging. The observation reads the resulting state. “Decide silently” asks the model to omit redundant narrative, while retaining a concise action note and all tool results; it does not ask it to suppress errors, required completion messages or higher-priority instructions. We do not alter token accounting or evaluation artifacts. The saving comes from fewer model round trips and less repeated text. The agent observes the current options before choosing a later quarterly action and does not assume that option identifiers remain fixed across phases.

La ejecución ordenada está comprobada en las pruebas locales documentadas, no garantizada por una cláusula explícita de los documentos públicos inspeccionados. No presentar esta interpretación como una aprobación de los organizadores. Si la semántica del runner destino difiere, volver a acción y observación separadas; la nota de eficiencia debe corresponder a la ejecución real.

## Números del candidato verificados en los archivos de resultados

Fuente primaria: `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-255b856f-dff20f-0000{0,1,2}-a1/score_report.json`. Son resultados locales con runner y modelo designados, no evaluación emitida por la organización.

| Carrera | Partida | Meses | Nivel | Fichas totales | Fichas/mes | Eficiencia calculada |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 66,27 | 48 | 5 | 31.411.020 | 654.396,25 | 93,8242 |
| 2 | 65,10 | 48 | 5 | 29.509.546 | 614.782,21 | 95,4087 |
| 3 | 68,13 | 48 | 5 | 30.606.083 | 637.626,73 | 94,4949 |
| Media | **66,50** | 48 | 5 | | **635.601,73** | **94,5759** |

Tres de tres completadas; no prueba estabilidad poblacional. La contribución medida de juego y fichas es **62,6576**; la nota automática sería `62,6576 + 0,1 × calidad oficial`. Con calidad hipotética 65 sería 69,1576, no una nota oficial observada. No trasladar estos resultados a cambios del manual o a v4-c5 con el nuevo bucle.

## Decisión sobre el banco de L1

cp-v5a: pérdida 4,42, 59 % mejor opción, 27/90 elecciones que bajan Network u Output y 8/90 arriesgadas. v4: 3,31 y 3,68; 61 % y 60 %; 24 y 25 pérdidas de N/O; 7 y 6 arriesgadas. La diferencia de pérdida es **+1,11 / +0,74**, aproximadamente +0,925 frente a la media de controles. No son puntos de nota de carrera: es la métrica del banco. Dos copias de un evento explican gran parte; por tanto no son 90 observaciones independientes y la coincidencia 84/90 no descarta una regresión concentrada.

**Hay motivo para cautela, no para declarar ganador al híbrido v4-c5 + bucle.** El banco compara principalmente t13-read-v4, no carreras del híbrido propuesto. Cambiar a él a última hora mezcla redacción, memoria, política trimestral y protocolo. Además v4-c5 conserva el segundo estallido como contador, la precisión del calendario y el margen numérico: no es una salida automática al problema de cumplimiento.

Recomendación: conservar cp-v5a como padre con evidencia de tres carreras y aplicar únicamente correcciones exigidas por cumplimiento/documentación, con nombre de revisión y límites explícitos. No justificar entregar el original sin limpiar por su buen rendimiento. Si el equipo decide volver a v4-c5, hacerlo por una comparación concreta del paquete final, no porque 4,42 sea una prueba concluyente o porque el ahorro del bucle se pueda dar por garantizado. No se ejecuta ninguna comparación nueva en esta auditoría.

## Validación y Relevo

- Leídos ambos archivos del candidato, el manual v4-c5 para comprobar la alternativa, el informe Comprobante, los documentos de entrega y el reglamento/handbook público. No se leyó el paquete del motor.
- `uv run careerlab lint /Users/alejandrotreny/huawei-comp/lab/policies-src/comprobante/cp-v5a`: **0 ERROR, 12 REVIEW**, código 0. La CLI añade `/bundle`; pasar directamente esa subcarpeta produce falsos errores de manifest/skills ausentes. Aviso de Authlib preexistente.
- Recalculadas medias y eficiencia desde los tres score reports. No se verificó la cronología completa de ascensos; las contradicciones quedan señaladas para quien empaquete. No se inspeccionó un ZIP final, que no forma parte de este candidato documental.
- No se cambia política ni se gastan APIs. Sólo este informe, README y la línea de apoyo en ESTADO. Revisar diff, commit y push en `alejandro/gpt-principios`; pedir integrar el informe en main.
- Siguiente responsable: quien prepara el corte 2 debe resolver P0/P1, alinear documentos con el paquete corregido y volver a pasar el lint anterior. Las notas de cp-v5a permanecen como evidencia del padre; cualquier revisión debe declarar que aún no tiene sus propias carreras.

## Relevo actualizado: corrección y entrega documental

Los documentos de corte 2 ahora describen cp-v5a existente, sin TODO, con sus cifras verificadas y sus limitaciones. No se ha tocado el Skill ni el manifest. Esta corrección prevalece sobre las referencias anteriores a retirar ambos contadores publicados.

Propuesta mínima para que valore el comprobador, en Skill y manifest donde se exige el lote trimestral:

> Quarterly phase: use the choices returned by the current observe. Send one take_action followed by observe in the same reply. Read the returned menu before selecting the next Energy action or the main action. Use its current choice identifier; do not assume identifiers remain unchanged across phases or quarters.

Con 2–3 acciones de energía y una principal, pasar de un lote completo a parejas añade 2–3 respuestas del modelo y 2–3 observe por trimestre: 32–48 de cada uno en 16 trimestres. No añade acciones de juego. Es un techo frente al ideal de un lote por trimestre; cp-v5a ya hizo algunas acciones separadas, por lo que el incremento real puede ser menor. Si por “fase” se entiende sólo el cambio de energía a acción principal, el mínimo sería 16 respuestas adicionales, pero no protege cambios de menú entre acciones de energía.

Estimación orientativa, no medida: a 100–150 mil fichas de contexto medio, 32–48 respuestas añaden 3,2–7,2 millones de fichas de entrada por reenvío, más las observaciones adicionales que se vuelven a reenviar y salidas. Son 67–150 mil por mes antes de ese segundo efecto: pérdida de eficiencia de 2,7–6 puntos y de nota automática de 0,27–0,60. El contexto medio es un supuesto de sensibilidad, no una medición de las llamadas nuevas. No dar un máximo de coste total sin reproducir el historial; las observaciones insertadas tienen coste acumulativo.

Necesario para entregar con una defensa coherente: documentos fieles y sin pendientes; citar el handbook real; no atribuirle equivalencias o fechas que no publica; resolver la dependencia de identificadores futuros y la presentación de consecuencias internas como certezas. El comprobador decide la edición y valida sus efectos. Sólo prudencia: quitar todo número que sea un margen propio declarado, eliminar constantes de calendario realmente públicas, cambiar de familia por el banco de L1 o renunciar al bloque literal/silencio. No hay base para exigir esas últimas medidas como prohibiciones oficiales automáticas.

Validación: diff sin errores de espacios; ninguna API ni partida nueva. Solicito integrar los documentos y esta corrección en main.
