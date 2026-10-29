# Revisión de Comprobante y nueva dirección

**Comprobante demuestra el salto de eficiencia y cambia la base propuesta a cp-v5a; el salto de partida sigue pendiente. Las prioridades nuevas son cierre con información atrasada, arbitraje de necesidades simultáneas y protocolos que DeepSeek pueda imitar.**

Lectura del 29 oct: rama `alejandro/comprobante`, informe completo y Relevo, CP1–CP5, pendientes §6, manual cp-v5a y diferencias de cp-v7/cp-v8, manifest cp-v8, las cuatro herramientas de scripts/comprobante, inventario de partidas y tramo final de la traza cp-v8. No se ejecutaron sondas ni partidas. Los detalles de todas las variantes y todos los mensajes de las nueve partidas declaradas no se han reanalizado exhaustivamente; ocho resultados distintos están enumerados en el informe y fueron localizados. No afirmar conocimiento exhaustivo del proyecto.

## Evidencia firme y límites

- cp-v5a tiene tres completas, 66,27 / 65,10 / 68,13, y 615–654 mil fichas por mes. El ahorro respecto a v4 se sostiene en partidas reales. No es una hipótesis que tengamos que volver a proponer.
- El bloque literal de tool_calls funciona donde distintas instrucciones en prosa fallaron. Esto demuestra sensibilidad al formato para esa conducta; no demuestra transferencia automática a percepción o decisiones.
- turnprobe avanza por observaciones grabadas aunque cambie la elección y responde éxito sintético. Su autor lo declara: prueba mecánica, no valor de carrera. El modelo falso demuestra orden de ejecución, no comprensión de DeepSeek.
- gametokens estima texto retenido como output menos reasoning y el resto como residuo. No es un tokenizado exacto de cada mensaje. Su contador de respuestas múltiples cuenta adyacencias de tool_call: una respuesta con tres llamadas puede aportar dos. La eficiencia total del score_report no depende de esa imprecisión del contador.
- La expresión cuadrática supone crecimiento por llamada fijo. Al agrupar herramientas, el crecimiento por respuesta sube: dividir N por dos no divide automáticamente el gasto por cuatro. Las mediciones reales son la referencia.
- El banco es compatible con elecciones parecidas, pero no demuestra equivalencia completa ni excluye regresión de carrera. En L1 cp-v5a pierde 4,42 frente a 3,31/3,68 de v4; que la diferencia se concentre en dos copias reduce la independencia de los casos, no elimina el riesgo de ese fallo.
- El informe contiene párrafos de etapas anteriores (cuatro completas y ningún hundimiento) junto al cierre posterior con una crisis. Usar las tablas finales. Dice nueve partidas, pero enumera ocho resultados; no inventar la novena.

## 1. Cierre con señal atrasada: prioridad inmediata

En la traza `deepseek-pilo-64fa828b-dff20f-00000-a1`, la observación inicial del mes 48 trae RR. HH. sonriente. Después hay tres historias; al llegar al trimestre el agente elige Health recovery, Mental recovery, Network maintenance y Report results to manager. El resultado final tiene riesgo 5. Los números del panel no permiten reconstruir un contador oculto exacto; la señal amistosa precede a acciones nuevas.

Hipótesis: el cierre debe reconocer que ya no habrá otro trimestre para reparar riesgo y que un comentario anterior no certifica el estado posterior. En el final, comparar explícitamente limpieza de riesgo con la utilidad marginal de recuperaciones y dinero. Posible seguro terminal con las acciones públicas de reducción, condicionado a la información disponible y a los otros costes. No trasladar un umbral privado al Skill. No prometer recuperar cinco puntos: una o dos reducciones pueden recuperar sólo parte del riesgo, y desplazan otras ganancias. Una alternativa es reducir riesgo antes de la última ventana; exige planificación, no magia al terminar.

Esto sustituye mi sospecha inicial de una simple colisión manifest/Skill por una explicación más precisa: el agente ejecutó una rama de cierre coherente con una observación posiblemente atrasada. Aún falta atribuir cuánto riesgo añadieron las historias posteriores.

## 2. Resolver necesidades simultáneas, no añadir otra excepción

cp-v7 expone una colisión Health/riesgo: la recuperación ocupa energía y aplaza limpieza. cp-v8 la corrige dando Defuse primero, pero una prioridad universal también puede fallar si la recuperación es urgente. Propuesta: plan trimestral conjunto de necesidades mínimas, costes publicados y urgencia. Determinar qué amenaza no admite esperar y qué acción satisface más de una necesidad; repartir el resto al crecimiento.

Base cp-v5a/cp-v8, no el híbrido v2. Diferencia de las pruebas previas de planificación conjunta: cambiar la representación de restricciones y su prioridad, no optimizar más exactamente la misma utilidad miope. No fijar simplemente riesgo por encima de salud para todos los estados. El caso de cp-v7 apoya investigar el conflicto, no demuestra la eficacia del remedio general.

## 3. Protocolos ejecutables e imitables

El hallazgo más transferible de Fable puede ser cómo conseguir una conducta: un formato literal breve, que después se repite en el historial. Proponer un protocolo de decisión con campos verificables y significado operativo: fase, amenaza inmediata, restricción activa, acción y condición de reparación. Ejemplo abstracto de estructura, sin historias, respuestas ni efectos privados. Conservar razonamiento oculto y nota mínima; no volver a una tabla larga por opción que infle el contexto.

No asumir que una nota rellenada implica obediencia: nuestra autocomprobación cumplía formato sin mejorar. El mecanismo que merece investigar es que el estado determine qué acciones quedan autorizadas, mediante un controlador o una comprobación efectiva. La presencia de un array literal enseñó una conducta mecánica; extrapolarlo a juicio estratégico es una hipótesis.

## 4. Gastar el ahorro en los pocos turnos que deciden la carrera

Conservar el bucle de cp-v5a y reservar una comprobación adicional para decisiones con alta sensibilidad: una pérdida que no puede repararse antes de evaluar, una acción que consume dinero visible agotado o un conflicto entre predicción y elección. No revisar todas las historias. Los turnos tempranos añaden contexto que se paga muchas veces; una salida breve importa además de limitar llamadas.

El ahorro no convierte dos lectores iguales en independientes. La segunda lectura debe resolver el supuesto que cambiaría la acción o usar otra representación. No pedir más razonamiento por sí solo: el silencio ya aumentó reasoning_tokens sin un salto demostrado en elecciones. Tampoco sacrificar las ganancias de fichas con un asesor en cada turno.

## 5. Coste de oportunidad acumulado de mantener la seguridad

Comprobante cumple Skill desde L4 y mejora el ritmo observado, pero pierde ventanas con RR. HH. inquieto y Health baja. Eso sugiere investigar las historias que obligan a gastar luego el trimestre en reparación. Una opción aparentemente segura puede dejar una deuda de salud que consume la oportunidad de aprender; una opción de crecimiento puede obligar a limpiar riesgo después.

Propuesta: valorar consecuencias por su factura futura de reparación, usando efectos publicados y experiencia propia, sin fórmulas privadas. Diferencia respecto a duplicar Skill o tolerar riesgo: el objetivo es preservar capacidad de inversión futura, no premiar crecimiento inmediato. Hipótesis de alto potencial, todavía sin evidencia causal. Puede fallar por predicciones erróneas o por castigar demasiado actividades útiles.

## 6. Mantener percepción y selección separadas, con menor prioridad que antes

Las líneas de traducción neutral, evidencia publicada/observada/inferida y aprendizaje de sorpresas siguen abiertas. Ahora deben vivir dentro del bucle eficiente de cp-v5a y justificar su coste incremental. No proponer de nuevo bancos de revisión factual, dos lecturas iguales o comparación por parejas como si no estuvieran hechos. La última comparación por parejas mantuvo tres pérdidas evitables en cada brazo.

## Relevo

Base recomendada para ideación: cp-v5a con su bloque literal intacto; cp-v8 es una variante por confirmar, no un nuevo campeón demostrado. Prioridad: cierre bajo observaciones atrasadas; conflictos simultáneos de salud y riesgo; protocolo de estados que el modelo imite y el controlador haga efectivo; revisión selectiva; planificación del coste de reparar. Otro modelo realizará las comprobaciones. Esta revisión corrige la dirección anterior, que no había incorporado Fable. No se ejecutaron nuevas hipótesis. Solicitar integración en main por PR #23; no se cambia la rama de Comprobante.
