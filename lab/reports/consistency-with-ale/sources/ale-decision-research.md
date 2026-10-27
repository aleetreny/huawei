# Primera exploración: señales de estancamiento y qué podemos aprender de las acciones

26 oct 2026 · Codex · rama `alejandro/investigacion-decisiones` · datos de main `9b8fbe9`.

**La señal más útil es detectar una carrera que no progresa para ensayar una recuperación concreta. Todavía no sabemos qué cambio de acción causa la mejora.** La regresión ya puede predecir parcialmente desde estados tempranos; los registros actuales no sostienen una regresión fiable de todos los comportamientos.

## Muestra y alcance

El snapshot tiene 204 partidas Claude terminales elegibles. Este Mac dispone de 99 trazas verificadas (105 no están aquí). Para separar al jugador de la estrategia, el análisis predictivo usa sólo el actor Haiku `08e9167a965ed82c`: 53 trazas locales de sus 129 partidas terminales. Las demás configuraciones no se mezclan como réplicas.

Los cortes se fijaron antes de ajustar: primera observación fresca previa a una acción en los meses 6 y 12, y sólo acciones anteriores para resumir comportamientos. Son puntos de análisis, no reglas para una Skill. Los modelos son ridge regularizados, con cinco variables de estado (nivel, Output, Network, salud y dignidad). El algoritmo aprende escala, imputación y penalización dentro de entrenamiento, y reserva manuales o familias completas para evaluar.

Las decisiones históricas ya fueron adaptativas y la muestra local es incompleta. Esto es descubrimiento, no confirmación ni identificación causal. Las familias del registro pueden compartir ancestros por recombinación; reservar una familia es una comprobación útil, no independencia absoluta de todo el proceso de diseño.

## 1. El estancamiento temprano es una alarma, no una sentencia

| Corte | Estado | Partidas | Completan | Q media |
|---|---|---:|---:|---:|
| 6 | Todavía L1 | 27 | 10 (37 %) | 35,90 |
| 6 | Ya promovido | 26 | 18 (69 %) | 55,41 |
| 12 | Todavía L1 | 14 | 2 (14 %) | 26,24 |
| 12 | Ya promovido | 38 | 26 (68 %) | 53,07 |

En el segundo corte falta una partida que terminó antes de tener una decisión allí; el denominador pasa de 53 a 52. Las diferencias son condicionales a seguir activo y observado en ese corte. No estamos comparando una promoción asignada al azar: políticas, riesgo acumulado, eventos y decisiones previas pueden explicar parte de la diferencia.

**Implicación:** priorizar un ensayo de recuperación cuando el feedback indique estancamiento, con seguridad conservada. Evitar tanto resignarse a la derrota como tratar un ascenso temprano como garantía de éxito. No introducir «si mes 12...» en un manual.

## 2. Los estados anticipan parte del resultado, con mucho ruido restante

| Corte | Partidas | RMSE al reservar familias | Referencia: media del entrenamiento |
|---|---:|---:|---:|
| 6 | 53 | 16,04 | 18,46 |
| 12 | 52 | 14,94 | 18,37 |

Al reservar políticas, los errores son 15,93 y 14,52, respectivamente. La mejora frente a la media se mantiene en ambas particiones, pero no se presenta como una diferencia estadísticamente confirmada. Un error de unos 15 puntos Q sigue siendo demasiado grande para tratar estas predicciones como una selección fiable de manuales. No están validadas prospectivamente ni con DeepSeek, y no cumplen la puerta para selección por episodios parciales de v1 §9.

En los cinco ajustes externos por familias, nivel y Network tienen coeficientes positivos en ambos cortes. Output es positivo en los cinco del primero y cambia de signo en el segundo. Son coeficientes condicionados y regularizados con variables relacionadas: **no** significan «una unidad de Network causa X puntos» ni que Output deje de importar. Refuerzan la pregunta de si conviene responder al contexto del progreso, en vez de maximizar un indicador aislado.

## 3. Crecer sigue siendo el mayor hueco entre quienes completan

En 28 carreras completadas del actor principal faltan, de media, unos 40,4 puntos Q: **16,18 en nivel y 13,28 en riqueza**, aproximadamente el 73 % del hueco. Salud/dignidad sólo pierde 0,21.

Esto confirma la prioridad de investigar crecimiento con protección. No prueba que aumentar agresividad añada 29 puntos, ni que proteger la salud sea innecesario: precisamente las políticas que la protegen pueden haber permitido llegar al final. Tampoco sabemos si el techo se debe a los manuales, al jugador, al azar o al entorno.

## 4. No tenemos aún suficientes historiales completos para atribuir valor a comportamientos

En las 53 partidas principales hay 8.324 llamadas de acción; **594 carecen de una observación nueva anterior**. A menudo el jugador aplica varias decisiones seguidas. La respuesta oficial de `take_action` sólo indica éxito/error, así que no podemos reconstruir el estado intermedio.

El extractor consume cada observación una sola vez. Quedan sólo **20 prefijos completos al primer corte y 17 al segundo**. Se mantiene el mínimo exploratorio de 30 y los modelos de comportamiento quedan `insufficient_support`; no se rebajó para obtener un resultado. Por tanto, este ciclo no puede responder honestamente «cuánto score añade defuse, preparar informes o recuperar salud».

**Implicación:** recuperar primero las 105 trazas de nube o ejecutar el pipeline allí. Medir cuántas aportan prefijos completos antes de gastar partidas. Si siguen faltando observaciones, un cambio futuro de instrumentación debe tener configuración de actor nueva, conservando las células anteriores.

## 5. Las historias pueden erosionar lo conseguido, pero una pérdida no demuestra una mala decisión

De 4.701 transiciones de historia con estado anterior y siguiente observación en el mismo mes, **1.177 (25 %) coinciden con una caída de Output o Network**. Puede haber costes necesarios para evitar daño, efectos diferidos o cambios que no sean un efecto aislado de la última elección.

El denominador son decisiones dentro de 53 carreras, no miles de carreras independientes. Este dato propone auditar ejemplos sin ver Q y después probar un recordatorio general de protección de entrega/relaciones. No justifica copiar respuestas a eventos ni etiquetar esas 1.177 decisiones como errores.

## Próximas pruebas priorizadas

1. **MEASURE-01:** ejecutar el extractor en nube con el mismo esquema y recuperar cobertura; revisar qué comportamientos tienen variación comparable.
2. **H-DR-01:** padre frente a una variante que responde explícitamente al estancamiento con entrega y apoyo al ascenso cuando es seguro, manteniendo las protecciones. Asignación aleatoria por partida, Y completo y supervivencia como diagnóstico. Primero auditar candidatas existentes para no duplicarlas.
3. **H-DR-02:** auditar pérdidas de Output/Network sin conocer Q; ensayar una regla de una sola frase sólo si se identifican pérdidas plausiblemente evitables.

El registro vivo está en `research/careerlab/decision-research/insights.jsonl` y la cola en `hypotheses.json`. Este chat continúa los ciclos y sube conclusiones; los experimentos siguen en la nube dentro de su cuota y protocolo.

## Relevo

**Hecho y motivo:** implementados extractor con alineamiento por llamadas/sesión, tablas numéricas comprimidas sin razonamientos ni texto de historias, validación ridge anidada por grupos, ciclos inmutables con hashes y registro de conclusiones. Se separa estado predictivo de comportamiento insuficientemente medido para evitar atribuciones falsas.

**Datos:** ciclo `001` conserva la primera ejecución. `002` corrige sólo el inventario de soporte de variables parciales y añade linaje: 99 partidas reutilizadas, **0 nuevas**, mismas filas de episodios y mismas predicciones. No es una segunda confirmación. `manifest.json` registra hashes de exports, código, especificación y archivos oficiales. `tables.md`, `analysis.json` y `predictions.jsonl` contienen los números auditables.

**Incidencias/límites:** observaciones ausentes en acciones consecutivas; 105 trazas no localizadas en el Mac; metadatos de época/bloque no explícitos en exports; una traza Sonnet presenta discrepancia de sesión y queda fuera de sus futuros análisis predictivos. No se ha ajustado logística de completar ni un modelo causal de acciones. Los modelos de comportamiento se detienen por falta de soporte.

**Siguiente paso:** seguir `research/careerlab/decision-research/CONTINUAR.md`; ejecutar `uv run python scripts/explore_decisions.py --cycle 003 --runs-root "$HOME/careerlab-data/huawei/runs"` allí donde estén las trazas. Revisar cobertura y linaje antes de interpretar cambios. Mantener descubrimiento y confirmación separados.

**Estado y publicación:** nuestra línea de ESTADO refleja esta exploración; resultados, tests y relevo se suben a `alejandro/investigacion-decisiones` y a la PR #3. No se han lanzado partidas, solicitado trabajos a la nube ni cambiado manuales o protocolo congelado. Validación final y commit constan en `research/careerlab/decision-research/progress.md`.
