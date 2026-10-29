# Errores compartidos de DeepSeek

**Dos lecturas repiten la mayoría de los errores iniciales de Output y riesgo positivo: el desacuerdo no basta para detectar las decisiones que necesitan ayuda.**

Se compararon las dos pasadas v3 guardadas, sobre 956 opciones comunes, con el catálogo v2 como evaluador. En Output, la primera falla 285 veces y ambas coinciden en el mismo signo incorrecto 192 veces (67,4 % de esos fallos). En riesgo positivo, la primera falla 185 veces y ambas repiten el error 151 veces (81,6 %). En Network son 179 de 271; en Skill, 143 de 204. Los recuentos están en `shared-reading-errors.json`.

Esto mide opciones, no decisiones ni puntos de carrera. La distinción de riesgo positivo agrupa cero y reducción; el resultado de tres signos también está guardado, pero no debe confundirse con detectar peligro. Las pasadas proceden de `lab/data/deepseek/etiquetas/ds-v3-r{1,2}-full.json`. La verdad se obtiene con `Catalog.effect` y `Catalog.answer_risk` de nuestra réplica. No se llamó a ningún modelo.

## Implicación para el próximo salto

Un segundo lector del mismo tipo tiene poco margen si reproduce el mismo sesgo. La hipótesis nueva que merece un diagnóstico es cambiar de juicios absolutos sobre cada opción a comparaciones entre alternativas: qué compromisos concretos se abandonan y qué trabajo verificable queda completado en una frente a otra. Esto sigue sin estar demostrado y no equivale a añadir otra lista de palabras peligrosas. Antes de gastar cuota, hay que comprobar qué errores de las decisiones reales podrían corregirse con esa información y cuánto valen en una continuación de carrera.

No repetir el veto por desacuerdo, la revisión factual ya ensayada ni la memoria de retornos como si fueran intervenciones nuevas. El siguiente diseño deberá contrastar una comparación entre alternativas con un control de igual presupuesto, usar Sonnet y reservar los casos de riesgo como control de regresión. No hay candidato listo para partidas.

El 72,4 del planificador ajustado es un resultado observado, no una cota matemática del juego. Tampoco el 75,8 máximo de L5 demuestra que pueda sostenerse esa nota: requiere maximizar conjuntamente las demás dimensiones. El objetivo de 75 consistente permanece abierto.

## Relevo

Hecho: sincronización con main, lectura de los nuevos informes Suelo y Techo y diagnóstico de errores compartidos. C40 ya fue descartado por esas líneas, por lo que no se repetirá. Pendiente: ponderar estos errores por las decisiones reales y su valor de continuación, antes de redactar un candidato. La descomposición de fichas sigue pendiente y afecta a la nota automática, no directamente a la de partida.
