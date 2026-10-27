# Objetivo y plan
Investigar cómo alcanzar 75 con DeepSeek sin ejecutar su API. Apoyo a la línea DeepSeek, rama alejandro/gpt-principios.

1. Reconstrucción de reglas y evidencia anterior: completa.
2. Investigación pública de leaderboard, repositorios y estrategias: barrido completado; sin atribución de75.
3. Intervenciones offline nuevas y validación de mecanismo: completas para este checkpoint.
4. Informe revisable y push: en curso. No candidato superior ni justificación de partidas proxy todavía.
5. Objetivo75: abierto; siguiente intervención debe medir decisión nativa/auditoría, no repetir estas variantes.

## Restricciones
No API DeepSeek; no interiores del motor; no eventos concretos ni números privados en Skills. No nuevas partidas de Claude antes de registrar tamaño y topes en ESTADO. No abrir otra línea activa.

## Errores
create_goal rechazó duplicado: el objetivo ya estaba activo; se conserva. Salidas de búsquedas demasiado grandes: resumir structuredContent y conservar evidencia local.

## Diseño antes de ejecutar incertidumbre
600 semillas nuevas 202610270+, seis brazos fijos: observed, hard_risk (una lectura), dual_risk (veto unión de dos lecturas), dual_average (riesgo unión y signos medios), dual_pessimistic (mínimo de cada signo), dual_loss (mínimo sólo crecimiento). Misma política trimestral. No pesos nuevos. Controla si robustez al desacuerdo aporta algo más que veto de una lectura. Intervalos condicionales a dos lecturas congeladas, sin inferir obediencia del modelo.

## Diseño diagnóstico de objetivos (antes de ejecutar)
Comparar control hard_risk con una intervención de preferencia por bienestar a partir de L3/L4/L5/L6 (aspiraciones públicas; sólo investigación). Sin cambiar etiquetas ni añadir información oculta. Peso fijo 5 a Health/Dignity respecto al valor original para probar sacrificio de carrera versus conservación. No afinarlo con resultados. Distinguir media total y media de completadas: no sirve aumentar sólo la segunda ignorando las derrotas. No convertir un breakpoint de réplica en Skill.

## Representación frente a planificación
800 semillas nuevas202640270+, mismo Planner sin futuro de historias: efectos exactos; signos perfectos; signos DeepSeek; signos DeepSeek + riesgo verdadero; signos DeepSeek con magnitud verdadera. Todos con contexto privilegiado (riesgo/caps/umbrales). Sólo diagnóstico de pérdida de información; no previsión de nota ni lógica para incluir en Skill.

## Factorial de magnitud del riesgo, antes de ejecutar
800 semillas nuevas202650270+. Separar efectos visibles exactos/signos y riesgo exacto/signo (cuatro brazos), más veto duro con signos perfectos, y predicción DeepSeek con/sin veto. Contexto privilegiado idéntico. Hipótesis surgida de representation-screen, no preregistro inicial: la magnitud de riesgo perdida explica las crisis. No afirmar que signos son malos independientemente del controlador.

## Corrección factorial
signs_veto pasó riesgo exacto a la función de valor antes del veto, cuando debía pasar sólo signo. No cambia los otros seis brazos. Guardado resultado inicial como superseded para ese brazo; corregir y reproducir mismos800 seeds en risk-factorial-corrected.json antes de interpretar veto.

## Precio prudente del riesgo, antes de ejecutar
600 semillas nuevas202660270+, seis brazos fijos: signos perfectos o guardados DeepSeek, con cada “riesgo+” estresado como1/2/3, reducciones como−1. No se lee magnitud verdadera de opciones para esa intervención. Contexto Planner sigue privilegiado. No seleccionar el mejor peso y afirmar score futuro: pantalla de mecanismo. Sirve para distinguir “hace falta clasificar magnitud” de “el controlador puede robustecerse sin otra clasificación”.

## Quitar privilegios antes de proponer traslado
2000 semillas nuevas202670270+: RuleBot observado, mismo bot con riesgo+ estresado como3, y veto. Caps aprendidos y HR retrasado; no umbrales de ascenso. No extrapolar el +6.4 del Planner privilegiado. Esta prueba es obligatoria antes de pasar a un manual/Haiku.

Error de revisión: csv.writer emitió CRLF y diff --check lo marcó como whitespace; normalizado a LF. Datos por semilla comprimidos sin pérdida con SHA para no introducir medio millón de líneas numéricas en el diff.
