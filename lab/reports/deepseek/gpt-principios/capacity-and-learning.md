# Capacidad del modelo y aprendizaje con consecuencias

**Sonnet con el mismo v4 terminó en 49,95; una mayor capacidad general no bastó en esta carrera para acercarse a 75.** La prueba emparejada pequeña no acredita superioridad ni transferencia a DeepSeek.

## Capacidad, selección y transporte

Doce menús L1 seleccionados sin etiquetas verdaderas, seis antes de evaluación. Mismo Skill v4 sin modificar, panel actual y sin registros anteriores; orden de modelos alternado. Una admisión READY y 24 decisiones válidas, cada una con lectura del Skill y cero acciones inválidas. Los modelos reportados son Haiku5.5 y Sonnet5.5. Coinciden en9/12elecciones.

| Medida | Haiku | Sonnet |
|---|---:|---:|
| Riesgo positivo elegido |2|2|
| Pérdida de crecimiento |1|0|
| Pérdida evitable antes de evaluación |1|0|
| Riesgo positivo evitable |1|1|

La diferencia es una sola pérdida evitable, no un efecto poblacional demostrado. Gold sólo puntúa las decisiones después de recogerlas; no se usa para seleccionar menús ni se suministra al actor. Una primera invocación CLI falló antes de llegar al proveedor: `--allowedTools` consumía el prompt posicional. Fallo archivado, orden de flags corregido antes de repetir el mismo caso, sin sustituir una elección.

## Referencia de carrera completa

Una carrera Sonnet, v4 inalterado, admitida con cuota semanal40% y margen antes de llamar. Terminó los48meses,202acciones, cero rechazos, **Q49,95/L4**, una crisis enmes45. Es una referencia existencial de capacidad, no una comparación aleatorizada contra carreras anteriores ni estimación de estabilidad. No se repite por salir mal. Datos: `sonnet-reference-results.json`; ejecución privada en `~/careerlab-data/deepseek/gpt-sonnet-reference/run-1/`.

Entrega por CLI y cinco herramientas oficiales más lectura emulada del Skill. No reproduce las52herramientas reales deJiuwen, especialmente scripts/bashing. No extrapolar esta nota al runtimeDeepSeek. El costeUSD que reporta el modelo es equivalente de tarifa de lista; cuentaMax, no cargoAPI.

## Aprendizaje con experiencia real

Diseño separado de otra autocomprobación:16menúsL1 distintos, ocho antes de evaluación. Ambos brazos ven un episodio anterior de otro título en la misma carrera, su elección original, la predicción registrada y el panel anterior; sólo un brazo ve además el panel posterior real. El episodio produjo una pérdida visible de crecimiento no prevista. No se entregan etiquetas del catálogo, riesgo oculto, umbrales ni respuestas fijas.

Las16transiciones se verifican como una única acción aceptada entre paneles del mismo mes/nivel, sin aviso de crisis, y anteriores al menú objetivo. Selección congelada antes de llamadas. ActorHaiku5.5, mismoSkillv4;32decisiones máximo, orden alternado. Primario: pérdida evitable de crecimiento antes de evaluación y riesgo elegido. Un aumento de riesgo bloquea admisión. Es una pantalla de aprendizaje entre títulos distintos; no una nota de carrera ni un test general de toda forma posible de memoria.

Exploracion terminada:32/32decisiones validas, lecturaSkill en todas, sin rechazos/errores. Perdidas6→4, evitablesantesdeevaluacion1→0, riesgo1→1;13/16elecciones iguales. No acredita eficacia con n16. Se fija contraste sobre los43objetivos restantes (7antesdeevaluacion), sin modificar metodo ni elegir casos por resultado. Comparten episodios docentes y carreras; no es replica de corpus independiente. Max86decisiones, sin carreras nuevas. No iniciar juegos completos por una mejora aislada de este banco.

## Relevo

Reanálisis sin llamadas: `uv run python scripts/deepseek/gpt_capacity_score.py` y `uv run python scripts/deepseek/gpt_learning_score.py`. Preparar/verificar los planes no llama a modelos. No repetir `gpt_sonnet_reference.py --run`: la carrera terminó y se conserva su resultado. No reiniciar tandas por un timeout de observación; inspeccionar el proceso y los resultados existentes. Narrativa sólo fuera deGit. Ninguna llamada nueva aDeepSeek.
