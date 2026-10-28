# Capacidad y aprendizaje a partir de consecuencias

**Sonnet con el mismo v4 terminó en 49,95. La pequeña mejora inicial de feedback no se mantuvo en los43menús restantes: pérdidas13→14, riesgo2→2. No se admite esta variante a carreras completas.** Ningún resultado demuestra75consistente ni transferencia aDeepSeek.

## Capacidad del modelo

Doce menús L1 elegidos sin consultar sus efectos verdaderos, seis antes de evaluación. Mismo Skill v4, panel actual y sin registros anteriores. Orden de modelos alternado. Se completaron 24 decisiones válidas: todos leyeron el Skill, sin errores ni acciones inválidas. Modelos reportados: Haiku 5.5 y Sonnet 5.5; coinciden en 9/12 elecciones.

| Medida | Haiku | Sonnet |
|---|---:|---:|
| Riesgo positivo elegido | 2 | 2 |
| Pérdida de crecimiento | 1 | 0 |
| Pérdida evitable antes de evaluación | 1 | 0 |
| Riesgo positivo evitable | 1 | 1 |

La diferencia de una decisión no acredita superioridad poblacional. El catálogo sólo puntúa después de recoger elecciones. Una invocación falló antes de llamar al proveedor: el argumento variádico `--allowedTools` consumía el prompt. Se archivó el fallo de transporte, se corrigió el orden de flags y se repitió el mismo caso, sin sustituir ninguna elección.

Se admitió además **una carrera completa Sonnet**, v4 inalterado: Q49,95, L4, 48 meses, 202 acciones y cero rechazos; una crisis en el mes45. No se repitió por salir mal. Es una referencia de capacidad, no una comparación aleatorizada contra partidas anteriores. El costeUSD reportado es equivalente de tarifa de lista; se usó la cuentaMax, sin cargoAPI. Datos numéricos: `sonnet-reference-results.json`.

La entrega por CLI emula cinco herramientas de juego y la lectura del Skill. No reproduce las52herramientas deJiuwen, especialmente bash/code; no extrapolar esa nota al runtimeDeepSeek.

## Diagnóstico de la carrera Sonnet

Las llamadas trimestrales encadenadas dejaron menús desactualizados para el parser de auditoría. Se corrigieron 12 atribuciones de fase/acción mediante el registro oficial público: **201 elecciones numéricas emparejadas exactamente**, más un documento inicial sin líneaChose que precede al anclaje del replay. El primer intento de reconstrucción falló una guardia de energía; no era una acción rechazada del actor.

Con las historias y respuestas reales fijas, el baseline reconstruye Q49,83–50,05, compatible con49,95. Sustituir sólo los trimestres produce25,52–25,74 (control observado, derrota por salud),51,92–52,15 (aprendizaje de retornos trimestrales) y52,42–52,65 (más limpieza). Ninguno rescata esa trayectoria a75. Los rangos corresponden al saldo inicial mostrado truncado, no a intervalos estadísticos. El controlador no recibe las historias futuras. Una trayectoria fija no predice las decisiones que tomaría de nuevo el modelo.

En144historias catalogadas, Sonnet eligió18riesgos positivos y39pérdidas de crecimiento. Dos pérdidas eran evitables antes de evaluación, en los meses5y11. Son diagnósticos posteriores; el actor no recibe el catálogo.

La misma alineación por registro no cambia ninguna atribución de las tres carrerasHaiku anteriores. La primera sigue sin validar el baseline (65,71–65,93frente66,86): sus efectos contrafactuales siguen excluidos. Se conserva el archivo original y se añade `native-quarter-replay-aligned.json`. DatosSonnet: `sonnet-quarter-replay.json`.

## Feedback con experiencia real

Ambos brazos ven el mismo episodio anterior de otro título en la misma carrera: menú, elección original, predicción registrada y panel anterior. Sólo un brazo recibe además el panel posterior real. Se seleccionan episodios con una pérdida visible de crecimiento no anticipada. **La predicción es de la traza fuente, no una predicción creada porHaiku en este estudio.** No se fuerza una acción contrafactual ni se proporciona el efecto verdadero del catálogo, riesgo oculto o información futura.

Las16transiciones iniciales se verificaron como una sola acción aceptada entre paneles del mismo mes/nivel, sin aviso de crisis y anterior al menú objetivo. ActorHaiku5.5, mismoSkillv4; orden de brazos alternado. Primarios: pérdida evitable antes de evaluación y riesgo elegido; un aumento de riesgo bloquea admisión.

| Exploración,16pares | Historia previa | Más resultado observado |
|---|---:|---:|
| Pérdidas de crecimiento | 6 | 4 |
| Pérdidas evitables antes de evaluación | 1 | 0 |
| Riesgo positivo elegido | 1 | 1 |

32/32decisiones válidas;13/16elecciones iguales. Es una señal pequeña. Se fijó antes de nuevas llamadas un contraste sobre **todos los43objetivos restantes**, siete antes de evaluación, sin modificar método ni elegir casos por resultado. Comparten carreras y episodios docentes: no es una réplica de corpus independiente. Max86decisiones, sin nuevas carreras.

Se añadieron comprobaciones de recursos después del piloto y antes de acabar el contraste: salud/dignidad a cero y gasto con dinero mostrado no positivo. No sustituyen los endpoints originales. El saldo mostrado está truncado: esa última señal no equivale a una quiebra observada. El piloto no introduce ninguna de esas señales en ningún brazo.

## Relevo

Contraste terminado:86/86decisiones válidas, modeloHaiku5.5, lecturaSkill en todas y cero errores/acciones inválidas. Coinciden39/43elecciones. Pérdidas13→14 (una mejora y dos empeoramientos), evitablesantesdeevaluación0→0 y riesgo2→2. Las comprobaciones adicionales de recursos dan cero señales en ambos brazos. El contraste no conserva la señal inicial: **no promover a carreras completas ni construir el transporte como candidato**. No prueba que toda forma de memoria sea inútil; descarta la admisión de esta intervención por la evidencia recogida. El diseño `experience-transport-spec.md` queda archivado como propuesta no admitida.

En ambos estudios se completaron118decisiones, sin sustituir resultados. No mezclar piloto y contraste como confirmación independiente: comparten fuentes y episodios docentes. Quota compartida observada durante el bloque:5h1→3%, semana40→40%, redondeada; no atribución de consumo individual. La referenciaSonnet y todas las tandas están terminadas. No quedan actores de esta prueba que reanudar.

Reanálisis sin llamadas: `uv run python scripts/deepseek/gpt_capacity_score.py`, `uv run python scripts/deepseek/gpt_learning_score.py` y el último con `--holdout`. No volver a ejecutar `gpt_sonnet_reference.py --run`: terminó y se conserva su resultado. Antes de retomar cualquier tanda, inspeccionar proceso y resultados; un timeout de observación no autoriza reiniciarla.

Narrativa sólo en `~/careerlab-data/deepseek/gpt-{capacity-probe,sonnet-reference,learning-feedback,learning-feedback-holdout}/`. Ninguna llamada nueva aDeepSeek. Objetivo75consistente abierto.
