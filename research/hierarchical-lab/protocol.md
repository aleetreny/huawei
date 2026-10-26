# Protocolo para implementar, medir y explicar el laboratorio

Estado: diseño de investigación; **no hay una flota ejecutándose**. Los permisos, presupuesto y conexión de modelos necesarios para lanzarla no se han configurado. Los resultados de Matteo y la exploración manual previa siguen siendo evidencia separada.

## 1. Separar laboratorio y runtime evaluado

El laboratorio propuesto compara políticas en episodios independientes. La entrega final debe poder operar como un único agente en JiuwenSwarm `0.2.4b3`, con el modelo indicado por los organizadores, sin depender del orquestador externo ni de otros actores. La clave de competición no puede utilizarse para Claude.

La documentación admite otros clientes MCP durante desarrollo, pero no autoriza por ello cualquier flota, volumen o modelo. Antes de ejecutar esta arquitectura externa se necesita aclarar su alcance con los organizadores. El estudio y especificación actuales pueden continuar sin dar por resuelta esa cuestión. [Reglas](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html), [MCP](https://techarena-career-sim.readthedocs.io/en/latest/mcp.html).

La consulta pendiente debe describir exactamente: varios clientes independientes, un actor por episodio, modelos externos pagados por el equipo, ninguna cooperación dentro de la partida, sólo las cinco herramientas, propuestas generales entre episodios, ausencia de tablas por evento y límites concretos de concurrencia/tasa. Una respuesta general sobre “se puede usar IA” no resolvería todos esos puntos.

## 2. Modelos comprobados y límites de la comprobación

Las páginas individuales oficiales, consultadas el 26 de octubre de 2026, describen:

| Función propuesta | Modelo / ID publicado | Entrada / millón | Salida / millón |
|---|---|---:|---:|
| Orquestador | Opus 5.5 / `claude-opus-5-5` | USD 4 | USD 20 |
| Trabajador barato | Haiku 5.5 / `claude-haiku-5-5` | USD 0,10 | USD 0,50 |
| Trabajador alternativo | Sonnet 5.5 / `claude-sonnet-5-5` | USD 2 | USD 10 |

Para Haiku, los valores de la tabla corresponden a peticiones de hasta 100.000 tokens de entrada. La página publica USD 0,50 de entrada y USD 2,50 de salida por millón para peticiones mayores. Hay modalidades, caché, batch y restricciones de plataforma que cambian el coste; la tabla no es una oferta para una cuenta concreta. [Opus](https://www.anthropic.com/claude/opus), [Haiku](https://www.anthropic.com/claude/haiku), [Sonnet](https://www.anthropic.com/claude/sonnet).

La página general de modelos obtenida durante la consulta aún mostraba una tabla anterior; hemos usado las secciones de disponibilidad e ID de las páginas individuales. **No se ha probado acceso con una clave** ni se ha medido su rendimiento en este juego. Antes de implementar hay que comprobar de nuevo los modelos efectivamente disponibles, el precio aplicable y la configuración fijada.

El actor objetivo se resuelve a partir de las instrucciones de los organizadores, no de una elección del laboratorio. La documentación menciona `deepseek-v4-flash` como designación en su publicación; debe utilizarse exactamente el nombre que llegue por el canal oficial.

## 3. Coste ilustrativo, no estimación de una partida real

Si un episodio consumiera un millón de tokens de entrada acumulados y 100.000 de salida, con todas las peticiones Haiku en el tramo corto, el cálculo base sería:

| Actor | Coste ilustrativo del episodio |
|---|---:|
| Haiku | USD 0,15 |
| Sonnet | USD 3 |
| Opus | USD 6 |

Las cantidades de tokens están estipuladas para comparar precios. No se han medido en CareerSim y no incluyen caché, reintentos, análisis ni validación oficial. Un prompt que acumula todo el historial puede cambiar tanto consumo como tramo de precio.

Una llamada de Opus con 50.000 tokens de entrada y 3.000 de salida costaría USD 0,26 con esos precios base. Hacerla tras cada decisión podría dominar el gasto del trabajador; hacerla con un resumen útil tras un lote tiene otra economía. Necesitamos medir **coste total hasta una mejora validada**, no sólo precio por token ni coste del worker.

El presupuesto externo se configura explícitamente antes de lanzar trabajo. No equivale a los USD 50 de la clave oficial, que conserva sus restricciones propias. El programa debe reservar coste para confirmación y para auditorías del modelo objetivo.

## 4. Prueba inicial de la interfaz y aislamiento

Primero una sesión manual o un worker, después concurrencia progresiva si está autorizada. La interfaz de Matteo ha funcionado manualmente, pero su servidor usa un lock para serializar llamadas y eso no es un benchmark de muchas sesiones.

Cada worker necesita sesión identificada, contexto de actor separado y una política congelada. La independencia de los estados debe comprobarse por `new_game`, `observe` y acciones de esas sesiones, mediante un protocolo pequeño y soportado. No leer la base de datos para demostrar aislamiento ni asumir que cambiar el directorio garantiza un almacenamiento distinto.

Si se necesitan procesos/almacenamientos aislados, usar sólo opciones documentadas del servidor oficial. Si no puede demostrarse aislamiento por la interfaz permitida, serializar la evaluación hasta resolverlo. Separar sesiones evita mezclas accidentales, pero no prueba por sí solo todos los supuestos IID del análisis estadístico.

## 5. Piloto de fidelidad entre modelos

Antes de permitir que Haiku elimine direcciones:

1. Elegir una pequeña colección de políticas generales distintas, congeladas antes de medir.
2. Evaluar cada una con Haiku y con el actor objetivo en episodios nuevos. Añadir Sonnet para estudiar ejecución cuando haya una razón concreta o para una matriz más completa.
3. Registrar medias, resultados individuales, costes y errores de seguimiento por celda.
4. Comprobar acuerdo de ranking y falsos descartes; observar si la complejidad cambia la relación.
5. Mantener una auditoría de candidatas rechazadas y repetir calibración al entrar en una familia nueva.

Por ejemplo, seis políticas, dos actores y tres episodios por celda son 36 episodios: **un diseño de piloto, no una justificación de potencia estadística**. Si el presupuesto no permite esa matriz, reducirla y conservar el estado “fidelidad no establecida”; no convertir dos ejemplos favorables en una autorización de poda masiva.

Una etiqueta de “mejor con Sonnet” debe distinguir mayor rendimiento por mejor ejecución, cambio en las decisiones y coste. Cambiar de actor a mitad de un episodio define otra política de ejecución y no debe contaminar una celda de actor fijo.

## 6. Bucle operativo propuesto

```text
Cargar registro validado y resolver tareas realmente pendientes.
Comprobar presupuesto, permisos, versiones y capacidad de trabajadores.
Mientras quede presupuesto de investigación:
    incorporar resultados terminales y errores operativos sin sobrescribir originales
    actualizar estadísticas por política, actor y periodo experimental
    decidir si hace falta: calibrar, repetir, generar, especializar, reabrir o confirmar
    si se genera: obtener un cambio acotado, validar artefacto y asignar identificador nuevo
    elegir un trabajo cuyo resultado pueda cambiar una decisión importante
    congelar política y configuración; crear una tarea con propietario y vencimiento
    ejecutar un episodio independiente por la interfaz autorizada
    conservar trayectoria y resumen; no mezclar contexto de otras políticas
    volver al planificador al recibir resultados o alcanzar un punto de revisión
Congelar contendientes; ejecutar confirmación reservada; generar informe con incertidumbre.
```

El planificador puede ser asíncrono; la primera implementación debería facilitar una comparación por lotes. Los trabajos en curso afectan la capacidad disponible, no se convierten en notas cero ni en muestras terminadas.

## 7. Contrato del trabajador

Entrada inmutable: identificador/hash de política, actor, huella del protocolo, herramientas permitidas, identificador de episodio y límites operativos. La clave se resuelve fuera del registro.

Durante el juego, el worker usa sólo información de la partida y procedimientos congelados. Puede tomar notas y actualizar memoria **dentro del episodio**, pero no consultar experiencias de otras ramas para cambiar su política. La memoria de investigación se queda en el orquestador.

Salida: final real, pausa o fallo operativo; duración; puntuación terminal si existe; herramientas y costes; referencias a evidencia; resumen de avisos, compromisos, cambios de modo y situaciones inciertas. El resumen no sustituye los datos originales cuando algo relevante está en disputa.

Ante una respuesta ambigua a `take_action`, observar o leer logs antes de repetir. Un reintento puede duplicar una acción ya aplicada. Los límites de iteración detectan errores, pero no deben fabricar resultados ni ocultar episodios truncados.

## 8. Persistencia en el repositorio

Estructura propuesta de artefactos, separada de `solution/`:

```text
lab/
  protocol.json
  families/<family-id>.json
  policies/<policy-id>/policy.md
  policies/<policy-id>/record.json
  jobs/<job-id>.json
  events/<event-id>.json
  evaluations/<evaluation-id>.json
  decisions/<decision-id>.json
  reports/<batch-id>.md
local-runs/
  <evaluation-id>/...         # evidencia local permitida, fuera de Git por defecto
```

El directorio `lab/` es una **propuesta**, no un conjunto de políticas ya creadas. El contrato de registros está en [records.schema.json](records.schema.json).

El esquema valida la forma de los cinco tipos de registro. La implementación deberá comprobar además referencias entre registros, correspondencia de hashes, propiedad/vencimiento de tareas, transiciones de estado y límites de presupuesto. Los formatos de fecha requieren un validador con comprobación de `date-time` habilitada; no todos la incluyen por defecto. Ninguna de esas comprobaciones de formato demuestra que un proceso siga vivo.

Cada mutación produce un artefacto nuevo y enlaza sus padres. El hash se calcula sobre los bytes exactos del artefacto que se usó, incluida la configuración relevante del prompt. Un registro de evaluación no se puede reasignar a otra política tras ver su nota.

Los workers escriben en su propio espacio de salida. Un único integrador valida y añade eventos y resultados al registro compartido; Git no es una cola de trabajos ni un mecanismo de exclusión mutua. Hacer commits de metadatos y resúmenes por lote, sin subir claves, paquetes, bases de datos ni todos los logs a ciegas.

Si otro entorno debe continuar el estudio, proporcionar exportaciones permitidas de evidencia o un almacén compartido aprobado. Un hash de un archivo local que ese entorno no puede leer no basta para reproducir una conclusión.

## 9. Recuperación tras interrupción

Un checkpoint debe contener presupuesto gastado y reservado, políticas activas/dormidas, decisiones de asignación, trabajos lanzados y resultados aceptados. Al reanudar:

- Consultar el proceso o servicio real asociado a cada tarea, si existe; no inferir que sigue corriendo sólo porque un archivo diga “running”.
- Si existe la sesión, observar por la interfaz oficial antes de reintentar una mutación.
- Si no se puede recuperar, registrar un episodio incompleto con causa operativa; no inventar puntuación.
- Evitar trabajos duplicados mediante identificador, propietario y estado de aceptación.
- Mantener el contexto que dio origen a una hipótesis, pero recuperar sólo la parte relevante para la nueva decisión.

Una política puede reejecutarse desde su archivo. Reanudar el contexto de un investigador no equivale a restaurar cualquier estado anterior del simulador.

## 10. Cómo evaluar el método de búsqueda

Compararía al menos estas ideas, según presupuesto:

| Comparador | Pregunta que responde |
|---|---|
| Best-of-N, sin usar resultados para generar la siguiente política | ¿El feedback evolutivo aporta algo? |
| Refinar siempre al líder | ¿La exploración de ancestros y familias distintas mejora una base sencilla? |
| Árbol con dormancia, sin reapertura | ¿Se pierde valor al no volver a candidatos archivados? |
| Evaluación sólo en el objetivo | ¿Las fuentes baratas ahorran coste sin eliminar políticas buenas? |
| Método completo | ¿Compensa el coste de coordinación y complejidad? |

El lote aleatorio de Matteo es una referencia de **comportamiento al jugar**, no un baseline controlado del algoritmo que busca políticas. No mezclar ese lote con muestras de una política razonada o con réplicas de nuestro optimizador.

Hay dos experimentos distintos: evaluar asignadores sobre un catálogo de políticas congelado permite aislar la selección; comparar búsquedas completas incluye también generación, depuración y coordinación. Ambos deben usar presupuestos comparables y el mismo criterio final. Compartir sólo las mejores propuestas del método completo con los baselines sesgaría la comparación.

La unidad externa de replicación es una búsqueda completa. Muchas partidas dentro de una sola búsqueda no equivalen a muchas búsquedas independientes. Si sólo podemos hacer un piloto, se presenta como piloto.

## 11. Ablaciones que justifican la ingeniosidad

Retirar por separado la reapertura, la calibración por actor, la diversidad del archivo o los modos por contexto permite preguntar qué mecanismo contribuye. No retirar todo a la vez y atribuir el resultado al componente que más nos gusta.

Medidas del método:

- Mejor política **confirmada** al terminar un presupuesto fijo.
- Coste y tiempo hasta una mejora útil confirmada.
- Ganancias de ramas reabiertas que sobreviven a nuevas pruebas.
- Falsos descartes del worker barato detectados en auditoría.
- Número de familias realmente distintas exploradas y exposición a fases tardías.
- Fracción de propuestas inválidas, duplicadas, regresivas o no confirmadas.
- Coste de coordinación y repetición desperdiciada.

El éxito no es maximizar profundidad, nodos o número de agentes. Un resultado de una sola partida no permite atribuir una mejora a una mutación.

## 12. Qué explicar al jurado

La historia técnica defendible sería: “Buscamos políticas completas, mantuvimos alternativas, medimos incertidumbre por actor y comprobamos las ideas en episodios nuevos. Esta rama parecía mala por esta razón; este experimento cambió nuestra decisión; esta parte no funcionó”.

Separar tres niveles:

1. Antecedentes conocidos: árboles evolutivos, archivos, selección de alternativas y múltiples fuentes.
2. Adaptación del equipo: cómo se coordinan para este simulador, cómo se detecta una evaluación barata engañosa y cómo se convierten especialistas en una política general.
3. Resultado demostrado: mejora y límites observados bajo el protocolo, todavía pendiente de ejecución.

No afirmar novedad teórica sin una revisión y prueba que la sostengan. Tampoco hay una subpuntuación publicada de “número de ideas nuevas”: la documentación valora el enfoque, riesgos, evidencia de depuración, generalización y coherencia de las Skills/diseño/vídeo. [Entregables y revisión](https://techarena-career-sim.readthedocs.io/en/latest/submission.html).

El vídeo debe responder los cinco temas oficiales en orden y usar ejemplos reales de versiones. Recoger durante la ejecución un diagrama de linaje, una tabla de ablationes, una decisión de reapertura con evidencia y una comparación de transferencia entre modelos. Si un componente no ayuda, reconocerlo es más defendible que atribuirle ganancias inventadas.

## 13. Hitos de implementación, sin reactivar la propuesta retirada

1. Resolver permisos, presupuesto y conexiones; verificar aislamiento y registrar versiones.
2. Implementar el contrato de datos y un worker único con una política experimental nueva.
3. Medir coste y calibración entre actores con una colección pequeña.
4. Ejecutar árbol sencillo y archivo, con evaluación terminal y validación reservada.
5. Añadir expansión adaptativa, modos de contexto y reapertura basada en evidencia.
6. Comparar con baselines y ablationes; simplificar para la entrega oficial.

Cada hito tiene un resultado verificable. Ninguno obliga a mantener una arquitectura de dos Skills: el empaquetado final se decide después de saber qué procedimiento funciona.
