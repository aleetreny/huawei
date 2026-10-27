# Comprobar la propia decisión no mejoró este banco

**La variante obedeció el formato en92/92 pruebas, pero no eligió mejor: no pasa a partidas completas.** Es un resultado de Haiku en decisiones aisladas, no un techo de DeepSeek ni una refutación de todo aprendizaje o revisión con información nueva.

Se ejecutó el [diseño fijado](decision-audit-plan.md):48 títulos reservados,92 contextos, dos brazos y24 repeticiones de control. Ambos brazos usan el mismo Skill general de juicio profesional; el tratamiento añade propuesta, coste, alternativa y comprobación. No se incorporaron nuevas categorías ni respuestas de eventos. El texto quedó congelado antes de las llamadas; hashes y selección en [decision-audit-selection.json](decision-audit-selection.json).

## Resultados

| Medida inmediata | Directo | Con comprobación |
|---|---:|---:|
| Riesgo positivo |4/92|5/92|
| Riesgo positivo cuando existía una alternativa no positiva |1/92|2/92|
| Elección dominada en el vector de efectos inmediatosv2 |3/92|6/92|
| Alguna pérdida en Skill/Network/Output |31/92|32/92|
| Pérdida de crecimiento entre las35 decisiones del mes de preparación |9/35|9/35|
| Ganancia media de Skill, con límites de estado |+0,511|+0,511|
| Ganancia media de Network |+0,043|+0,011|
| Ganancia media de Output |−0,087|−0,130|

La diferencia de incidencia de riesgo positivo, promediando primero contextos por título, es **+1,04 puntos porcentuales**, IC bootstrap95%[0;3,13]. No hay evidencia de beneficio; la muestra no certifica un daño pequeño. El intervalo es condicional a los48 títulos observados, no una garantía sobre historias nuevas. Las pérdidas de crecimiento no son automáticamente errores: pueden comprar salud, seguridad u otro recurso. La dominancia también se refiere sólo al vector inmediato investigado, no a un valor de carrera completo.

La comprobación cambia la elección frente al control en sólo5/92 contextos. Sus notas declaran una revisión de propuesta en18/92; eso no demuestra18 mejoras ni equivale a la comparación contrafactual con el control. En92/92 notas escribe el formato y su Final coincide con la acción.

El control repetido elige lo mismo24/24 veces, en23 títulos. Es una muestra pequeña de estabilidad, no una tasa poblacional garantizada de100%. No interpretar el bootstrap degenerado[1;1] de esa submuestra como certeza sobre futuras repeticiones.

## Ejecución y medida

- 208 decisiones obtenidas;208 lecturas de Skill; cero acciones inválidas o errores registrados.
- Los208 streams identifican **claude-haiku-5-5**, CLI **2.1.303**. No hubo mezcla de estas versiones en el lote.
- Se sirve una observación objetivo con logs previos reales disponibles; no hay transiciones de prefijo forzadas que ignoren la elección del actor. Los identificadores de elección provienen del menú ofrecido.
- El analista usa catálogo **v2** y efectos acotados por el estado, con pérdidas de dinero escaladas. No usa el Q heredado del banco, ni simula una explosión/liquidación para atribuirla a una sola opción.
- Bootstrap por título, promediando sus contextos antes de remuestrear. No tratar92 contextos como92 títulos independientes.
- Cada CLI se termina después de registrar la decisión objetivo; el código143 es esperado y no significa que se haya completado una carrera. Los tokens guardados son los emitidos hasta ese corte: faltan los totales finales de la CLI. No convertirlos en factura o eficiencia de una partida completa.
- Cuota de cuenta observada:5h10%→11%, semana37%→38%, sin sobrepasar0,65/0,45. Son snapshots de cuenta compartida, no una atribución exacta de cuota a este lote. Cuenta Max y sin overage. **Sin API DeepSeek ni partidas oficiales nuevas.**

[Resultados y hashes](decision-audit-results.json), [transporte](decision-audit-transport.json), [filas numéricas comprimidas](decision-audit-rows.json.gz). Observaciones, notas y streams narrativos permanecen en `~/careerlab-data/deepseek/gpt-decision-audit/`.

## Qué cambia el siguiente paso

No llevar esta variante a partidas para perseguir una mejor puntuación por azar. Tampoco tomar el cumplimiento de una nota como prueba de que el modelo ya controla la decisión.

La siguiente hipótesis debe aportar información que esta revisión no tiene: **comparar una predicción propia con el efecto público de la acción elegida y comprobar si esa corrección mejora una decisión nueva**, con una condición sin ese feedback. Debe usar sólo consecuencias observables de la partida, sin decirle efectos de opciones no elegidas, sin memoria de eventos entre carreras y sin convertir hallazgos privados en reglas del Skill. La calibración numérica por grupos ya falló; una prueba del aprendizaje nativo debe distinguirse de ese calibrador y puede fallar también.

## Relevo

Hecho: prueba de208 decisiones, selección y texto congelados, control repetido, lectura bajo demanda, corrección de métricasv2 y análisis por título. Comprobaciones del analista: límites, copia inmutable, dinero por nivel y peso igual por título. Ambos paquetes pasan lint.

Resultado: ninguna mejora de la comprobación sin información nueva. No registrar ni promover estos paquetes como campeones; son comparadores de investigación. Objetivo75 abierto.

Reproducir análisis, sin llamadas: `uv run python scripts/deepseek/gpt_decision_score.py`. El runner `gpt_decision_audit.py` respeta resultados existentes, guardas de cuota y la selección congelada; no se necesita volver a ejecutarlo ahora. No usar un nombre nuevo para generar otra pasada accidental.
