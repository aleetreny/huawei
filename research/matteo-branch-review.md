# Revisión de la rama Matteo

Fecha: 26 de octubre de 2026. Rama revisada: `origin/Matteo`, commit `0eb09244468c24373b136face6160ccacc3c0ffb`.

## Qué contiene

- Una interfaz manual de navegador, Career Lab, en `tools/local-game/`.
- Un adaptador Starlette/FastMCP que conecta sus cinco operaciones con las cinco herramientas oficiales del juego. Arranca el ejecutable oficial por stdio y se sirve sólo en `127.0.0.1:8765`.
- Un informe metodológico, un plan de experimentos y un JSON con resultados agregados de partidas aleatorias.
- No incluye el controlador completo de las 73.858 partidas, ni sus trayectorias individuales, ni un benchmark del modelo oficial o de unas Skills.

Fuentes exactas: [informe del compañero](https://github.com/aleetreny/huawei/blob/0eb09244468c24373b136face6160ccacc3c0ffb/docs/exploratory-findings.md), [resumen JSON](https://github.com/aleetreny/huawei/blob/0eb09244468c24373b136face6160ccacc3c0ffb/docs/experiments/random-baseline-summary.json), [adaptador](https://github.com/aleetreny/huawei/blob/0eb09244468c24373b136face6160ccacc3c0ffb/tools/local-game/server.py). Son enlaces al repositorio privado y requieren acceso.

## Resultados que declara el compañero

| Métrica | Resultado publicado |
|---|---:|
| Partidas terminadas | 73.858 |
| Acciones | 1.563.578 |
| Tiempo acumulado | 14.400,19 s, aproximadamente cuatro horas |
| Supervivencia media | 5,9056 meses |
| Supervivencia máxima | 24 meses |
| Partidas que llegan a 48 | 0 |
| Puntuación media | 11,7842 / 100 |
| Puntuación máxima | 28,9 / 100 |
| Blackout | 40.496 |
| Trust crisis | 30.559 |
| Otras causas terminales | 2.803 |

He comprobado que las causas suman 73.858 y que Blackout + Trust crisis son el 96,2049% del total. El cociente es aproximadamente 21,17 acciones por partida. **No he reproducido el experimento masivo ni auditado sus transiciones**: éstos son resultados de la rama, no resultados obtenidos por mí.

El informe separa correctamente un piloto de treinta partidas del lote principal. La semilla `7_000_000 + run_index` controla las elecciones aleatorias del controlador, no el generador del simulador. No permite emparejar escenarios. Las observaciones numéricas del piloto sobre puntuación local no se han convertido aquí en reglas de estrategia.

## Qué demuestra y qué no

Demuestra, según sus registros, que elegir uniformemente entre las opciones disponibles funciona muy mal en esa configuración. Además orienta la primera exploración hacia sostenibilidad y feedback de riesgos.

No demuestra que salud y confianza tengan siempre la mayor importancia. Hay **riesgos que compiten**: si la partida acaba en el mes 4 por salud, ya no puede acabar en el mes 30 por falta de capacidad. La frecuencia de una causa terminal depende también de cuánto se consigue sobrevivir.

Tampoco proporciona una política ganadora, una comparación causal entre acciones, ni la distribución de puntuaciones. Con medias, mínimos y máximos no podemos reconstruir varianza, cuantiles, correlación supervivencia/puntuación o incertidumbre de las diferencias entre estrategias. La puntuación máxima y la duración máxima podrían pertenecer a partidas distintas.

La contribución del lote es una referencia aleatoria bastante precisa. Hacer otro lote igual reduciría una incertidumbre que ya no es la principal. Ahora interesa saber **qué intervención general mejora el comportamiento y qué coste tiene**.

## Qué he comprobado personalmente

He copiado únicamente los cuatro archivos de la interfaz revisada a `local-runs/matteo-preview/`, una carpeta ignorada por Git. No he cambiado la rama de Matteo ni fusionado sus documentos sobre la investigación local.

He instalado las versiones declaradas por él en un entorno aislado: Python 3.13, motor 1.0.6, datos 1.0.8 y FastMCP 4.1.3. He usado el comando público de actualización del dataset y el servidor MCP oficial, sin leer paquetes internos ni base de datos.

La interfaz ha creado una sesión y he jugado en pantalla hasta el inicio del mes 7. He comprobado la consulta del manual y del registro oficial, las elecciones narrativas, dos fases trimestrales y la aparición del primer feedback semestral. No se ha usado la clave de competición. Esto valida una vía de **juego manual**, no la configuración exigida de JiuwenSwarm ni una partida completa de 48 meses.

## Observaciones de mi sesión, todavía sin conclusión estadística

1. Algunas situaciones continúan en meses posteriores. Hace falta recordar compromisos y evaluar efectos diferidos.
2. Los logs describen cambios de una acción que no siempre coinciden con un incremento visible en el panel. La causa no se ha identificado: no debemos deducir una fórmula o un límite oculto de un solo ejemplo.
3. La asignación trimestral sigue mostrando acciones de coste dos cuando sólo queda un punto. Que una opción aparezca no basta: hay que comprobar asequibilidad con los costes públicos.
4. La recuperación y la prudencia mantuvieron la sesión viva, pero la primera evaluación fue C y el nivel siguió siendo L1. Supervivencia y progreso deben medirse juntos.
5. El feedback semestral apareció durante la transición al mes 6, antes de mi asignación de Energy de ese trimestre. Debemos registrar el orden real de feedback y acciones, en vez de suponer que una preparación tardía afecta retroactivamente a una evaluación ya recibida.

Estado al dejar la sesión: inicio del mes 7, L1, Health 7, Dignity 10, Skill 9, Network 3, Output 3, Wealth 2, Energy 0. Sesión incompleta y sin puntuación terminal. No se debe mezclar como un resultado terminado en las estadísticas.

La pestaña queda abierta para continuar y los detalles locales de la observación están en `local-runs/matteo-preview/manual-ui-observations.json`. Los ejemplos narrativos no se han convertido en un catálogo de respuestas para una entrega.
