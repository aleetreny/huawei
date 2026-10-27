# Propuesta y comprobación: diseño antes de probar

**La mejora no está demostrada; se probará la decisión elegida, no el acierto de una taxonomía.**

Control: native-craft-v1, basado en el diseño B ya archivado, sin taxonomía ni mecánica oculta. Tratamiento: mismo cuerpo, nombre, descripción e instrucción, con una comprobación breve propuesta/coste/alternativa y una nota de decisión. No cambiar el texto durante el lote.

Banco: sólo historias de títulos reservados. Hasta dos situaciones por título, con contextos distintos cuando están disponibles; selección aleatoria estable, sin filtrar por la respuesta de ningún modelo. Un único paso servido con su observación y logs previos reales; no transiciones de prefijo independientes de la decisión. Sólo la observación, logs y handbook llegan al agente; ni etiquetas ni Q del banco.

Muestra fijada tras contar el banco y antes de llamadas: hay48 títulos reservados, no128. Se incluyen los48, hasta dos contextos por título (92 situaciones en total), ambos brazos y24 repeticiones de control para ruido. Selección definitiva y hashes antes de primera llamada. Piloto de transporte4 pares, incluido en la muestra; si falla el transporte se arregla y se excluye como piloto técnico, no se eligen resultados favorables. Orden de brazos alternado por índice. Hasta4 procesos Claude globales; techo5h0.65 y semana≤0.45. Sin dinero API, sin DeepSeek. Si la cuota real impide, parar lanzamientos y guardar estado; no alterar topes.

Primaria: cambio emparejado en riesgo positivo de la opción elegida, corregido con catálogo v2, especialmente cuando existe alternativa de riesgo no positivo. Secundarias: magnitud de riesgo, pérdidas de Skill/Network/Output y sus ganancias, pérdida preevaluación, dominancia de Pareto, elección repetida y coste de tokens. Reportar intervenciones de coste, no venderlo como mejora Q. Bootstrap emparejado por título; la muestra no sirve para confirmar cambios pequeños. Con sólo48 títulos independientes, interesa un efecto grande; reportar intervalos por título, no tratar≈96 decisiones como títulos independientes; no seguir gastando para perseguir2pp.

Admisión a partidas: efecto grande y claro en decisión, sin deterioro relevante de crecimiento, y transporte completo. Después haría falta comparar carreras completas bajo mismo actor. No inferir75 de Haiku ni target desde este banco.

Datos narrativos y respuestas: ~/careerlab-data/deepseek/gpt-decision-audit/. Relevo en README principal.

## Comprobaciones del analista antes de abrir resultados
Modelo real observado:claude-haiku-5-5, CLI2.1.303. El analista aplica límites de recursos y multiplica las pérdidas de dinero por nivel según la réplica; no simula explosiones ni liquidación para atribuirlas a una sola decisión. La incidencia preevaluación se reporta sobre toda la muestra, no como tasa condicional del subgrupo. Comprobaciones manuales: ganancias ya limitadas a10/techo→0; copia de estado no mutada; pérdida monetaria de1 enL5→3; bootstrap primero promedia contextos de cada título. Los208 resultados completos son obligatorios antes de escribir la comparación final.
