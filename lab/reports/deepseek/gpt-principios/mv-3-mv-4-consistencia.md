# mv-3 / mv-4: convertir el 77,78 en rendimiento repetible

> **Corrección posterior:** la denuncia anónima tenía riesgo +1 frente a +2 de la otra opción: no prueba incumplimiento del modo estricto. Para las prioridades actuales, usar [revisión para 78](revision-opus-78.md) y [encargo vigente](encargo-opus-78.md).

**Conclusión: 77,78 demuestra un recorrido alcanzable, no una política que lo garantice; faltan tanto ascensos tempranos como protección fiable frente a crisis. El objetivo práctico debe ser elevar la frecuencia de carreras de ese nivel y reducir la cola de pérdidas.**

## Alcance y fuentes

Revisión sin API ni partidas nuevas, siguiendo la prohibición de DeepSeek del usuario. Fuente actual localizada en `/Users/alejandrotreny/huawei-mejora`, rama `alejandro/mejora-v4`, commit `a160964`. Hay modificaciones documentales sin commit en ese worktree: el README y ESTADO se leen como actualización provisional, no como contenido necesariamente publicado en main. No se modificó ese worktree. `origin/main` de esta rama estaba actualizado pero aún no contenía mv; no se confunde el texto «juntada en main» con prueba de integración.

Fuentes primarias: `lab/data/deepseek/partidas/mv-3__e8cdf663-0000{0,1,2,3}/score_report.json`, `mv-4__0f4bf379-0000{0,1,2,3,4}/score_report.json`, `lab/data/deepseek/decisiones.csv.gz`, bundles mv-3 y mv-4. Fuente interpretativa: `lab/reports/mejora/README.md` §§5–8. Todas estas rutas relativas se refieren al worktree anterior.

## Qué cambió realmente

Los SKILL.md de mv-3 y mv-4 son idénticos. El manifest de mv-4 cambia el nombre y añade la exigencia de no terminar una respuesta sólo con texto, manteniendo llamadas reales hasta el final. Esto trata las interrupciones del runner; no es una nueva política de carrera. La mejora de paradas observada es una señal operativa, no garantía universal ni prueba de idéntico comportamiento de juego.

El banco de mv-3 mejora pérdida de L1 (2,51 frente a 3,31–3,68 de v4), con controles de riesgo/general sin empeoramiento según el informe. Es una sola pasada y fue seleccionado entre variantes sobre ese banco: necesita títulos reservados para acreditar generalización. No hay banco propio de mv-4.

## Todas las carreras, sin seleccionar sólo las completas

| Carrera | Juego | Ascensos a L2/L3/L4/L5/L6 (mes) |
|---|---:|---|
| mv-3 / 1 | 68,64 | 12 / 18 / 24 / 42 / — |
| mv-3 / 2 | **77,78** | **6 / 12 / 18 / 36 / 48** |
| mv-3 / 3 | 66,06 | 12 / 18 / 30 / 48 / — |
| mv-3 / 4 | sin nota, interrupción | — |
| mv-4 / 1 | 63,35 | 12 / 24 / 30 / 48 / — |
| mv-4 / 2 | 69,62 | 6 / 12 / 24 / 42 / — |
| mv-4 / 3 | 37,06, crisis | 6 / 12 / 18 / — / — |
| mv-4 / 4 | 18,98, despido L1 | — |
| mv-4 / 5 | 63,27 | 6 / 18 / 24 / 48 / — |

Se verificaron cambios de nivel con `d_nivel=True` del CSV: marca la acción previa al cambio de mes; los meses de evaluación de la tabla son los siguientes. Los campos de estado del CSV son ANTES de la acción: no tratar la última fila del mes como estado final previo a la evaluación sin aplicar transición.

Ocho carreras con nota: media **58,095**. Seis completas: **68,12**. Dos eliminadas por juego y una interrumpida por software. Una de ocho puntuadas llega a L6/77,78; una de nueve intentadas. No son estimaciones precisas de probabilidades futuras.

Corrección de recuento: la tabla y las transiciones muestran **4 de las 8 puntuadas** con ascenso en el mes 6 (mv-3/2, mv-4/2, /3 y /5), no los 3 de 8 del cierre del README. Si se incluye la interrumpida: 4 de 9. No usar esa discrepancia para inferir superioridad entre manuales.

## Qué compra los 77,78

Informe primario de mv-3/2: L6, riqueza **43,8**, Skill 134, Network 53, Health+Dignity 20 y riesgo 0. Componentes: nivel 18; riqueza 10,95; salud/dignidad 15; Skill 15; riesgo 10; red 8,83. Suman 77,78.

| Diferencia respecto a mv-4/2 (69,62) | Puntos |
|---|---:|
| Nivel L6 frente a L5 | +3,00 |
| Riqueza 43,8 frente a 25,5 | +4,57 |
| Salud+dignidad 20 frente a 19 | +0,75 |
| Skill (ambas saturan su componente) | 0 |
| Riesgo | 0 |
| Network (53 frente a 54) | −0,17 |

La suma redondeada de componentes es 8,15 frente a diferencia de notas 8,16 por redondeo. Riqueza depende también de gastos y bonos, no atribuir causalmente todo +4,57 a seis meses de salario. Skill sigue siendo necesaria para ascender, aunque su componente directo ya esté saturado.

Con el resto de componentes del 77,78 pero L5, serían 74,78: alcanzar L6 forma parte del mecanismo observado. No es prueba de que toda trayectoria posible de 77,78 necesite exactamente este calendario o estado final.

La ganadora llega a L4 en 18 y dedica 18 meses a ese nivel; alcanza L5 en 36 y dispone de 12 meses para el último ascenso. mv-4/2 entra en L4 seis meses después y llega a L5 en 42. Su registro previo a la última acción del mes 47 muestra S127/N54/O26: la brecha respecto al recorrido ganador incluye Output, no sólo Skill. Es un indicio de estado, no el estado exacto usado por la evaluación.

## Por qué el mismo manual no reproduce la ganadora

- Historias y decisiones distintas producen trayectorias distintas. La ganadora demuestra que estas reglas pueden aprovechar una trayectoria favorable; no separa cuánto fue lectura mejor y cuánto fue la secuencia de oportunidades.
- Hay errores potencialmente evitables, pero la denuncia anónima del mes 26 no los demuestra: la alternativa tenía más riesgo (+2 frente a +1). El fallback permite elegir el menor cuando todas son arriesgadas. El diagnóstico inicial de incumplimiento era incorrecto.
- Hay intercambios forzosos. El informe identifica en mv-4/1 una última historia de mes 5 con pérdida de Network o alternativas de riesgo +2/+3. No llamar error a toda pérdida del ascenso ni resolverlo aumentando indiscriminadamente tolerancia al riesgo.
- Hay retrasos previos al mes crítico: mv-3/3 llega al mes 5 con Skill 3 en la última observación preacción. Proteger sólo Network/Output al final no recupera toda la preparación perdida.
- Hay pérdidas posteriores a un arranque perfecto: mv-4/3 consigue L4 en 18 como la ganadora y termina en crisis en 27. Acelerar sin controlar riesgo no da consistencia.

Una de las correcciones del informe: mv-4/5 acaba con riesgo **1**, no 0 como su tabla resumida; su componente de riesgo es 9. Se priorizan los score reports.

## Plan priorizado para acercarnos a carreras de 77–78

1. **Conservar la corrección operativa de mv-4.** Volver a mv-3 sólo porque contiene el máximo observado recuperaría un defecto conocido sin prueba de mejor política.
2. **Prioridad histórica corregida:** auditar alternativas antes de atribuir fallos al modo estricto. El caso anónimo no sostiene una aclaración específica. El nuevo encargo evalúa riesgo innecesario anterior a la crisis y menús sin salida segura, con controles de crecimiento y falsas alarmas.
3. **Diagnóstico de preparación a lo largo de cada nivel.** Auditar la primera ventana perdida, no sólo la última decisión: qué indicador faltó, cuándo apareció el déficit y qué acciones seguras disponibles podían repararlo. En L1 incluir Skill temprana; en L2/L3, Network y Output; en L4/L5, Skill y Output. Sólo formular una regla nueva si varios fallos comparten un mecanismo y no una historia particular.
4. **Medir rutas a L6 y conservación, además de supervivencia.** Hitos descriptivos de referencia: L4 hacia 18, L5 hacia 36, L6 al final; no respuestas fijas ni umbrales ocultos trasladados al Skill. Reportar tasa de cada hito, crisis, eliminaciones, gasto patrimonial y componente de bienestar. Salvar una carrera de 19 llevándola a 65 sube la media, pero no cumple por sí solo el objetivo de 77,78.
5. **Validación nueva y aislada.** Reservar títulos completos; controles repetidos y agrupación por partida/historia; evaluar coste del error y cola mala. No mezclar las correcciones anteriores en otro manual antes de medir cada una. Con la prohibición actual, usar datos guardados y réplica para localizar mecanismos; cualquier nueva prueba del modelo real queda pendiente de autorización.

Criterio de éxito propuesto: maximizar P(juego ≥77,78), con tasas de L6 y hundimiento como diagnósticos y media como apoyo. No declarar éxito por un máximo ni garantizar todas las partidas: no hay evidencia de una política que domine la variación de menús y las decisiones del modelo. Tampoco hay una prueba matemática en estos datos de que sea imposible aumentar mucho esa frecuencia.

## Relevo

Leídos mv-3/mv-4 y sus actualizaciones, contrastados score reports, transiciones del CSV y la decisión de la crisis; calculadas medias y descomposición de 77,78 frente a 69,62. No modelos, API, partidas ni modificaciones de políticas. No se lee el interior del motor. Auditoría exhaustiva de alternativas y contrafactuales pendiente: no se simula que corregir una acción garantice el resto de la carrera.

Continuar con las fuentes de Alcance y el banco de modo estricto/primeras ventanas perdidas. Mantener prohibición de DeepSeek. Documentado en README y ESTADO de la línea de apoyo, validar diff, commit/push y solicitar integración en main. Las correcciones de recuento y riesgo se entregan como observaciones para el propietario de Mejora; no se editan sus archivos en trabajo.
