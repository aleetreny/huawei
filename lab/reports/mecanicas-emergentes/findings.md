# Contexto y hallazgos

Base reciente: `origin/alejandro/transmision@4cec65d`. H25 (68 puntos, sin L7) quedó superado por M16–M17: L7 observado y planificador real 70,5. M10 sustituye la hipótesis de explosiones aleatorias por contador determinista. No presentar ninguno de ellos como descubrimiento nuevo.

Posibles sesgos del planificador: crédito a `dr<0` aun con riesgo cero; al cerrar elimina el peso de progreso bajo umbral, aunque queda la evaluación 48. La réplica está validada por transiciones, no reproduce perfectamente distribución conjunta de historias, riesgo de opciones escasas ni trayectoria completa.

## Descubrimiento durante la comprobación oficial (smoke, 4/4)
La partida termina con current_month=49 y duración de nivel +1; después de la última acción del mes 48 paga otra nómina (+1,5 en L6 en los cuatro ejemplos). `replica.play` y `game.Game._advance` paran ANTES de esta transición. No hay mes 49 jugable: son 48 nóminas frente a 47 modeladas. Error de cierre de 0,25×salario en Q, además del redondeo del dinero visible. Se comprobará en todas las completadas del lote oficial ya fijado; no cambia ninguna elección de terminal_q porque esa nómina es constante entre sus acciones. Esto no aparecía en M1–M23.
