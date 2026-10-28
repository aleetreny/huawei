# Objetivo y plan
Investigar cómo alcanzar 75 con DeepSeek sin ejecutar su API. Apoyo a la línea DeepSeek, rama alejandro/gpt-principios.

1. Reconstrucción de reglas y evidencia anterior: completa.
2. Investigación pública de leaderboard, repositorios y estrategias: barrido completado; sin atribución de75.
3. Intervenciones offline nuevas y validación de mecanismo: completas para este checkpoint.
4. Informe revisable, commit4cd5ac8, push y PR22: completos. No candidato superior ni justificación de partidas proxy todavía.
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

## Continuación
- Prueba decisional nativa/auditoría: completa,208 decisiones válidas; no mejora. No pasar a partidas completas ni repetir.
- Runtime: auditado un ensayo oficial interrumpido. Parche de idioma preparado y probado offline; no aplicado a instancias.
- Criterio de cierre del objetivo sigue siendo75 estable con DeepSeek; ninguna de estas comprobaciones lo certifica.

Siguiente mecanismo: corrección con efecto público de una acción elegida y prueba en una decisión nueva, con control sin ese feedback. Pendiente diseño; no nuevas llamadas en este checkpoint.

## Caracterización nativa completa, antes de partidas
El banco no resuelve si el control profesional llega a buenas carreras; no se ha comparado end-to-end. Cuatro partidas Haiku completas nuevas, secuenciales, actor y Skills congelados. Con SD orientativa10, SE de media5; admite detectar un salto grande (~20), no consistencia ni mejora estrecha. No sustituir derrotas. Cortes operacionales separados de Q. Herramientas oficiales y modo competition; sólo emulación de entrega Skills en Claude, no JiuwenSwarm/DeepSeek. Cuota0,65/0,45 vigilada durante cada partida, máximo4procesos compartidos. Sin hipótesis de ventaja causal contra un control histórico. El aprendizaje con feedback se pospone hasta observar un déficit end-to-end concreto.

Diagnóstico previo de contexto:34pares del mismo nodo,26con distinto nivel; el nativo cambia2elecciones. En6pares el heurístico privilegiado sin continuación y con riesgo actual fijo0 tiene óptimos disjuntos; el nativo no cambia enninguno. Es un indicador para investigar, no regret de Q ni verdad sobre una acción. No convertir caps/umbrales privados en Skill.

## Feedback de ganancias bloqueadas, diseño previo
600semillas nuevas202680270+; seis brazos fijados: baselineobservado+veto con expectativas DeepSeek congeladas; mismo con techo inferido tras1/2/3historias distintas que predijeron ganancia y dieron0 en la misma situación de mes/nivel; diagnóstico con signos perfectos baseline/aprendiz2. Se mantienen aprendizajes trimestrales existentes y HR retrasado. Si reaparece una ganancia por encima del supuesto techo, revocarlo; reiniciar pruebas tras ascenso. No leer efecto verdadero de la opción ni capreal para decidir en brazosDS. El capreal sólo mide falsas inferencias. No aprendizaje entre carreras ni tablaevento→respuesta; IDs distintos sólo evitan contar una misma evidencia repetida. No pasar a Haiku sin beneficio sólido frente al veto existente y tasa de inferencia razonable. Es un controlador de aprendizaje, distinto del calibrador semántico por grupos ya fallido.

## Replay de trayectorias reales, antes de ejecutar
Después de terminar el piloto, comparar cuartos alternativos con historias/elecciones reales fijas, sin pasarlas al ranking de acciones. No es política nativa ni pronóstico Q. Anclar mes3 para evitar rareza startup; riqueza visible intervalo+0..0,9; historial Output previo conservado. Tres brazos fijados: cuarto original, controlador observado existente, controlador que además aprende de ganancias publicadas de main cuando el cambio de mes no está confundido por condiciones persistentes. No mirar caps/umbrales para asignar cuartos. Antes de interpretar exigir baseline reproduzca resultado y Q real dentro de0,5 del intervalo; si el camino observado acaba y el contrafactual sigue vivo, no inventar continuación ni nota final. Este diagnóstico puede descartar gastar cuota en la nueva candidata de retornos observados; no la acredita por sí solo.

Ampliación exploratoria posterior al primer replay: añadir cuarto más prudente cuando HR público está por encima de tranquilo (antes el controlador esperaba nivel2), sin calendario fijo ni consultar riesgo vivo. Defuse si hay presupuesto y Health no está comprometida; mainLaylow sólo mientras persiste HR>0. Motivo: replay observado del tercer camino alcanzaL6/Q70,47–70,70 pero aún pierde por explosión. No se afina umbral ni pesos después; es una prueba de mecanismo posthoc, no preregistro. Reparar además etiqueta de censura: si la simulación ya murió al cambiar de mes, no llamar censura a que el registro no tenga eventos futuros.

Segunda ampliación exploratoria, antes de ejecutar: híbrido propuesta nativa guardada + información semántica DeepSeek ya existente, sin nuevas llamadas. Comparar guardia de riesgo sólo siHR>=2 con esa guardia más dominancia estimada tras descontar ganancias bloqueadas aprendidas. Signos visibles de una lectura congelada, riesgo unión de ambas; sin efectos verdaderos para elegir. Sólo nodos sin continuaciones en ninguna opción: así cambiar respuesta no invalida el camino futuro guardado; esta restricción usa estructura del catálogo y NO es una política entregable ni sabemos si el agente identificaría esos nodos. No se ven las futuras historias al elegir; todos los otros comportamientos nativos futuros se congelan. Si rescata la segunda carrera hasta donde acaba su traza, nota final nula. No llamar a esto75delmodelo aunque el replay dé75.

##28oct: crédito negativo de riesgo, diseño antes de ejecutar
Nuevaevidencia tras revalidarmain y cinco trazasDeepSeek propias: los advisors almacenan saldo de riesgo bajo0y recompensanR- sin riesgo estimado. Cuatro brazos fijos800semillas202610280+: baseline scriptv1entregado(hash coincide ganador76,87), sólo truncar saldo inferior0despuésdeacción, sólo valorar el efecto marginal deR- hasta0, ambos. Misma lecturaDScongelada, no variables verdaderas adicionales, misma interfazSimadv. No barrido de pesos. No nuevas partidas/etiquetas/API. Si no mejora, no promover. Si mejora, confirmar semillanueva antes de candidatura; el sesgo de lecturas en partida (R- falsos seleccionados) obliga a validar transporte antes de inferir estabilidad75.

Ampliaciónposthoc tras resultado nulo: separar valorsemántico deR- de cancelaciónderiesgo. Mantener recompensaoriginal completa deR- para escoger; para memoria sólo acciones trimestrales publicadas pueden reducir la estimación, o una observación mensual nueva que refrescaHR. La conjeturaR-de una historia no reduce deuda. También truncarsaldonegativo. Brazo verified_only frenteabaseline,800semillas nuevas202620280+, sin recalibrar lectura o parámetros. Es una hipótesis nueva posterior a fallar marginal/floor; no llamar confirmación del mismo experimento.

## Lecturas dentro/fuera de partida, antes de ejecutar
Hallazgo nuevo: v1ganador usa magnitudes dobles en2/381opciones; v3 usa196/386y214/374. El banco simadv normaliza todas a signo y no mide esa interfaz real. Comparar, porcadauna de5fuentes, mismo script realmente entregado y400semillas nuevas202630280+: etiquetasstandalone DSv3, reemplazo sólo en nodos cubiertos porlecturasinsitu normalizadas, reemplazoinsitu conmagnitudes originales. El resto siempreDSstandalone, nuncaoráculo. Hash exacto de nodo, sin combinar títulos ambiguos. Es posthoc y condicionado a una lectura por nodo; no es un manual ni se pueden entregar mapas por evento. No comparar versiones entre sí como ensayoaleatorizado. Diferencia full-sign sólo diagnostica transferencia de magnitudes; resultado no se atribuye a nuevo agente nativo.

## Transporte de HR: prueba local antes de parche
De las5trazas reales, dos infradeclaranHRfrente al comentario público contemporáneo (23y39filas); las otras no. Medir intervención de un solo campo, manteniendo memoria histórica real y todas las etiquetas. Cada llamada copia memoria previa y sustituyehrpor tono público; descartar memoria contrafactual antes de la siguiente entradareal. Describir cambios de opciones, riesgo/crecimientoinmediato sólo en historiascatalogadas; trimestres sólo conteo. No afirmar nota de carrera ni usar estado delmundodeotraacción como si fuera válido. Esta comprobación determina si merece diseñar transporte de feedback sin interpretación intermedia.

## Referencia completa Sonnet, antes de ejecutar
Tras24decisiones emparejadas, ambosmodelos cometen2riesgos; Sonnetevita1perdida de crecimiento evitable queHaikuno. n1referencia completa con v4sin modificar: pregunta existencial de capacidad, no diferencia media ni75estable. No hay potencia con una carrera y no se afirmara eficacia. Se cuenta toda terminacion; no se repite si sale mal. Max admitido una, cuota fresca semanal<=40% para margen de una carrera y5h<65%, max4procesos. Sigue la instruccion comun de no cortar partidas lanzadas por nota/saldo; no hay otra programada. No utilizaDeepSeek.

## Aprendizaje nativo con consecuencias reales, antes de llamadas
16menusL1 distintos,8pre-evaluacion y8otros, muestreo2026102810. Elegibilidad: existe un episodio anterior de otro titulo en la misma carrera con una perdida visible de crecimiento no prevista por la lectura original. La diferencia observada procede de una unica accion entre paneles del mismo mes/nivel, sin aviso de explosion. No se da la etiqueta verdadera del catalogo. Ambos brazos ven ese episodio, la eleccion original, su prediccion y el panel anterior; solo observed_outcome recibe el panel posterior real. Mismo Skillv4, actorHaiku5.5,32llamadas maximo (16x2), secuenciales con orden alternado. Sin nuevos juegos completos/DeepSeek, guardas0,65/0,45 y max4procesos. Datos narrativos solo fuera deGit.

Hipotesis: una consecuencia realmente observada puede corregir una creencia al elegir en otro evento, distinto de comprobar otra vez la misma respuesta o inferir techo de una subida imaginada. Primario: perdidas de crecimiento evitables antes de evaluacion y riesgo positivo elegido; no convertir la diferencia de una decision enQ. Un incremento de riesgo bloquea admision aunque baje una clase de perdida. N16 es pantalla exploratoria y no prueba media poblacional ni75.

## Contraste de feedback, antes de llamadas adicionales
Exploracion n16 deja6→4perdidas,1→0evitable pre-evaluacion,1→1riesgo;13/16opciones iguales. Sin modificar metodo, probar todos43menus restantes de la poblacion elegible59:7pre-evaluacion/36otros. Se excluyen objetivos iniciales y no se elige por etiqueta verdadera ni por donde funciono. Mismos episodios docentes/carreras pueden repetirse: independencia de objetivo no implica independencia estadistica de corpus. Max86decisionesHaikuMax, sin nuevas carreras niDeepSeek. Mantener endpoints y bloquear admision si aumenta riesgo. No afinar prompt ni parar por nota intermedia.

Resultado delcontraste: negativo paraadmision.43parescompletos, perdidas13→14, riesgo2→2; no se mantiene mejora. No ejecutar nuevos juegos de esta variante. Objetivo75abierto; proxima hipotesis debe separar identificabilidad delestado/control con herramientaspublicas de obediencia/formato yaauditados.
