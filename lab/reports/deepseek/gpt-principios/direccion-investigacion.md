# Dirección de investigación a partir de las tiradas disponibles

**La apuesta de mayor interés es conservar las decisiones útiles de v4 y cambiar cómo se representan, verifican y autorizan sus excepciones. Ninguna propuesta de este documento está validada.**

Revisión del 29 oct: inventario completo de 21 partidas en `lab/data/deepseek/partidas.csv`, informes DeepSeek y Sustitutos, Formato, Suelo, Techo, pendientes, fuentes externas y experimentos de esta carpeta. Se revisaron inventarios e informes; no se ha vuelto a leer íntegramente cada mensaje de las 21 trazas. No se ejecutaron pruebas nuevas. Las seis partidas sin informe final no tienen nota imputada.

## Qué conservar de cada familia

- **v4 / v4-c5:** referencia para historias y disciplina de riesgo; 71,67 y 70,22 son dos carreras completas, no una media poblacional. La tercera v4 quedó cortada en L1. c5 cambia presentación y calidad; transferencia pendiente.
- **script-v1/v3:** ejecución y estado reproducibles, capacidad observada de L6, sensibilidad peligrosa a signos equivocados y dinero redondeado. No asumir que el 76,87 representa un efecto causal del script: cambian los caminos de las carreras.
- **script-v2:** advertencia contra un híbrido ingenuo. Dejar historias a DeepSeek y trimestre al script ya falló. Una nueva combinación necesita un mecanismo diferente y verificar contaminación de las historias.
- **Suelo y Techo:** mejoras locales con mecanismo conocido; útiles como base, insuficientes para prometer un salto grande. No repetir C40 ni tolerancia general al riesgo.
- **Sonnet:** proxy preferente para errores, pero el estudio de similitud usa Sonnet 5 y nuestras últimas pruebas registran 5.5. No afirmar equivalencia entre versiones ni con DeepSeek. Haiku puede servir como contraste de percepción, no como garantía de transferencia.

## A. Asesor con autoridad limitada y justificación verificable

**Base:** v4-c5, con piezas de Techo/Suelo sólo tras sus verificaciones. **Mecanismo:** v4 propone; el asesor sólo puede vetar o sustituir si existe una contradicción concreta entre la acción, el estado observado y una restricción explícita. Ejemplos abstractos: dinero visible agotado y gasto personal previsto; una inversión con ganancia publicada que repetidamente no se materializa; una propuesta que contradice su propia predicción de pérdida antes de evaluar. No imponer el voto del asesor por tener más confianza.

Es distinto del v2: no delega un dominio entero ni abre una autorización general a riesgos pragmáticos. El asesor devuelve qué observación sostiene el veto y qué alternativa evita ese daño. Si depende sólo de una etiqueta incierta, su autoridad es menor. Potencial: evitar que una lectura errónea se convierta en una decisión irreversible, conservando el juicio global de v4. Fracaso posible: certificados que sólo repiten errores del lector, o demasiadas intervenciones. Evaluador: medir cobertura de errores caros y regresiones fuera de ellos, además del coste de las llamadas.

## B. Un modelo de consecuencias que pueda contradecir al agente

**Base:** lector de Formato, antes de decidir. Sustituir la casilla única por tres tipos de información: efecto publicado, consecuencia observada en esta carrera y predicción no confirmada. Evitar que un R− supuesto se contabilice con la misma autoridad que una reducción anunciada por el menú. Mantener hipótesis e intervalos cualitativos, no fingir el valor exacto del riesgo.

No es volver a corregir créditos negativos, que ya falló. Cambia quién puede usar una inferencia como si fuera evidencia. Potencial: gestionar conjuntamente falsas alarmas y riesgos no vistos. Un veto de toda duda sería una regresión: la incertidumbre debe afectar cuánto se confía, no convertir todo en peligro. Evaluador: comprobar primero que esta distinción cambia errores relevantes; si sólo produce más texto, abandonar.

## C. Traducir las opciones a transacciones de recursos

**Base:** percepción v3, manteniendo la narración original. Antes de juzgar honestidad o prudencia, representar quién hace qué, quién recibe el crédito, de quién sale el tiempo, qué entrega queda pendiente y quién conoce el problema. Después predecir efectos. Conservar condiciones temporales y destinatarios; no borrar título e historia, intervención que empeoró.

No es otra lista sí/no ni una simple comparación por parejas: el objeto intermedio es una descripción causal neutral y reversible a la opción original. Ejemplo abstracto inventado: ayudar puede transferir tiempo propio a entrega ajena; informar puede compartir información sin completar trabajo. No convertir esos ejemplos en reglas universales de signos. Riesgo: el traductor pierde detalles o añade implicaciones. Evaluador: fidelidad semántica y corrección de errores compartidos, controlando longitud y presupuesto.

## D. Aprender de predicciones fallidas, con atribución explícita

**Base:** memoria de retornos, pero con otra función. Registrar una predicción antes de actuar; al observar el resultado, distinguir efecto de acción, liquidación, cambio de nivel y saturación. Actualizar una hipótesis transferible sólo cuando la atribución sea defendible. Guardar contradicciones y evidencia insuficiente.

La memoria anterior no produjo mejora de elecciones de Sonnet. Por tanto, entregar más ejemplos no basta: esta línea requiere que una sorpresa cambie la interpretación de una situación posterior diferente. No incorporar respuestas del catálogo a un Skill ni llevar memoria de eventos entre carreras. Aprendizaje activo queda como extensión de baja prioridad: buscar información sólo entre acciones casi equivalentes y seguras. La carrera puede ser demasiado corta para amortizarlo.

## E. Planificar la reparación, además del crecimiento

**Base:** Techo y planificador. Valorar una pérdida por si queda una oportunidad real de repararla antes del siguiente ascenso. El recurso escaso puede ser una ventana temporal, no un atributo. El plan debe mantener próximo cuello de botella, oportunidades públicas de reparación y señales que lo invalidan.

Distinguir pérdida inevitable de pérdida evitable: si todas las respuestas cuestan algo, más relectura no crea una alternativa buena. Esto no autoriza más riesgo globalmente: esa línea ya falló. La novedad sería coordinar historia y reparación posterior sin usar umbrales ocultos ni futuro de historias. Las evaluaciones fallidas aportan restricciones sobre el cuello de botella; una nota A no identifica por sí sola el indicador que falta. Evaluador: contrastar contra las reglas Techo ya preparadas, no contra una referencia débil.

## F. Revisión selectiva del supuesto que decide la elección

**Base:** v4 más asesor. El controlador identifica qué supuesto, si fuera falso, cambiaría su elección. Sólo entonces solicita una lectura de ese supuesto: por ejemplo, si la opción realmente exige abandonar una entrega, no volver a puntuar todas las dimensiones. Activación por sensibilidad de la decisión y daño potencial; no por la confianza verbal del modelo ni por acuerdo de dos lectores.

Dos pasadas repiten el 67 % de los errores iniciales de Output y el 82 % de riesgo positivo en nuestro diagnóstico. La revisión factual y las segundas lecturas anteriores no rescataron las decisiones. Esta línea sólo merece comprobarse si formula una pregunta distinta y relevante para la acción; de otro modo es repetir lo descartado.

## G. Decisiones reversibles en el controlador: cambiar sólo cuando compensa

**Base:** política v4 congelada como referencia. Una propuesta nueva debe mostrar qué daño evita y qué riesgo adicional introduce. Si la mejora sólo depende de inferencias frágiles, mantener la decisión de referencia. Puede permitir aprovechar crecimiento del asesor en unos estados y conservar el comportamiento conservador en otros.

No seleccionar a posteriori el ganador por evento: eso sería una tabla de respuestas encubierta. El criterio de intervención debe ser general, observable y evaluado en historias reservadas. Es complementario a A; no es una promesa de combinar automáticamente el techo del script con el suelo de v4. La contaminación de contexto puede cambiar incluso decisiones donde el asesor no interviene.

## H. Estado mínimo que el código mantenga y el modelo utilice

**Base:** contabilidad de Formato, sin exigir Stalled manual. Separar observación, predicción y decisión pendiente; actualizar sólo lo necesario para la siguiente acción. Mantener tareas de reparación y contradicciones pendientes, no una autobiografía de decisiones justificadas. Exponer al modelo un resumen corto con procedencia.

El script ya ejecuta fielmente; el cuello es qué memoria se calcula y si cambia la decisión. Evitar una llamada adicional por historia cuando basta actualizar en un trimestre o una evaluación. No asumir que escribir un resumen comprime el historial oficial: no lo hace. La reducción de fichas afecta a la nota automática; no equivale a alcanzar 75 de partida.

## Prioridad para el modelo evaluador

1. **C + B:** cambiar la representación y el estatus de la evidencia; mayor potencial y mayor incertidumbre.
2. **A + F + G:** convertir mejoras de percepción en intervenciones selectivas sobre v4. Compartir diseño, pero medir componentes por separado.
3. **E + H:** planificación y ejecución con estado observable; más cercanas a nuestra infraestructura, con riesgo de duplicar Techo si no se exige algo nuevo.
4. **D:** apuesta de aprendizaje más ambiciosa, condicionada a observaciones atribuibles y suficientes oportunidades de transferencia.

Para un corte cercano, conservar la ruta de candidatos ya preparados en pendientes.md. Estas líneas son investigación adicional y no justifican saltarse sus filtros. No sumar ganancias de experimentos distintos ni llamar techo al 72,4 observado de un planificador ajustado.

## Relevo

Encargo: dirección creativa e inteligencia, sin ejecutar hipótesis. Propuestas basadas en el inventario de todas las tiradas disponibles y sus auditorías, con límites de cobertura explícitos. La comparación por parejas terminó sin reducir pérdidas evitables: no presentarla como candidata validada. Otro modelo debe decidir qué pruebas discriminan cada mecanismo. Solicitar integración del documento en main. Objetivo de 75 consistente todavía abierto; no se conoce el método privado de los competidores.
