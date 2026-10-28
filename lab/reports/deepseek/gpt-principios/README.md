# Desde principios básicos: qué falta para 75 de partida con DeepSeek

**Todavía no hemos reproducido 75 consistente ni identificado la técnica de los equipos que lo consiguen. Sí hemos encontrado un fallo causal del controlador: tratar todo aumento de riesgo como un único punto puede destruir carreras incluso con percepción perfecta.** No presentar esta auditoría como una solución ya probada con DeepSeek.

Objetivo confirmado por Alejandro: **nota de partida ≈75, repetible, con DeepSeek**, no nota ponderada de entrega. Restricción: ninguna llamada nueva a la API de DeepSeek. Esta carpeta apoya la línea DeepSeek; rama `alejandro/gpt-principios`. No abre otra línea activa ni reemplaza t13-read-v2.

## 1. Qué entregamos y qué problema estamos resolviendo

La entrega son Skills ingleses para un agente JiuwenSwarm `0.2.4b3`, modo `agent`, modelo designado `deepseek-v4-flash`. El agente juega una carrera de 48 meses: historias mensuales, presupuesto trimestral y evaluación semestral. Debe progresar sin destruir salud, dignidad, relaciones, patrimonio o confianza. Sólo las cinco herramientas oficiales y su información de la partida sirven para interactuar y aprender.

Fuentes primarias: [reglas oficiales](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html), [manual](https://techarena-career-sim.readthedocs.io/en/latest/handbook.html), [runner público](https://github.com/RAI-Internal/techarena-career-sim). Reglas online contrastadas el 27 oct. No se han leído los paquetes internos del motor ni el dataset empaquetado.

El 80/10/10 explica la puntuación de entrega, **pero no explica el 75 de partida que describe el usuario**. No volver a usarlo como respuesta a este objetivo.

Desde control básico, hay cuatro problemas distintos:

1. **Estado e información:** qué acaba de cambiar, qué observaciones llegan con retraso y qué se conserva tras un resumen.
2. **Consecuencias:** qué beneficios y daños plausibles tiene cada opción.
3. **Decisión:** qué intercambios admitimos; una buena clasificación no obliga a elegir bien.
4. **Ejecución:** que el agente aplique la regla correcta en la fase correcta y aprenda del resultado.

La investigación anterior demuestra errores de percepción, pero no demuestra que arreglar una etiqueta aislada sea la intervención que más mejora al agente completo. Tampoco demuestra que el mejor planificador medido sea óptimo globalmente.

## 2. Qué encontramos fuera

Se buscaron el reto, DeepSeek, 75, Skills y soluciones en Exa y GitHub, incluyendo búsquedas `in:readme`, código y forks. Las búsquedas por nombre solas omitían repositorios con nombres distintos; ampliar a README encontró candidatos adicionales. El conector GitHub leyó archivos; `gh api` se usó para listar árboles y forks cuando la búsqueda de código no daba rutas.

| Fuente pública | Qué se pudo comprobar | Qué no demuestra |
|---|---|---|
| [Kingjinsight/TechArena-UK-2026](https://github.com/Kingjinsight/TechArena-UK-2026/tree/main/preliminary) | Tres Skills preliminares: estado, filtro de integridad, trimestre | No aporta puntuaciones repetidas ni identidad del equipo de 75 |
| [ShriyaSaxena/techarena-career-simu](https://github.com/ShriyaSaxena/techarena-career-simu/tree/main/preliminary) | Tres Skills generales; riesgo, prioridad y crecimiento | No aporta validación de 75 |
| [YuLong111/techarena-career-sim](https://github.com/YuLong111/techarena-career-sim/tree/main/preliminary) | Un Skill con feedback, incertidumbre y continuidad | No aporta validación de 75 |
| [krsnkkv/KSL_TechArena](https://github.com/krsnkkv/KSL_TechArena/tree/main/preliminary) | El Skill de historias coincide por SHA con el de Shriya | No es evidencia independiente de otra estrategia |
| [Artepace/slopathone_winningteam](https://github.com/Artepace/slopathone_winningteam) | Su README dice que el diseño preliminar no se ha probado | El nombre del repo no acredita una victoria |
| [peidi-L/preliminary](https://github.com/peidi-L/preliminary) | Un borrador general | No aporta pruebas de rendimiento |

Se leyeron nueve Skills distintos, más la copia coincidente de KSL. Rutas y SHA en [public-search.json](public-search.json). No se ejecutó código ajeno ni se buscaron claves. Los resultados chinos de CareerSim-BDCI26 tienen reglas/plataformas distintas; no se toman como evidencia del reto UK.

El [scoreboard público](https://techarena-uk.hydro.ac/contest/6aad0b0020562bf065d1654f/scoreboard), abierto en navegador hacia las 18:58 UTC del 27 oct, mostraba puntuaciones 0 y cortes vacíos. Eso **no refuta** las partidas locales que describe Alejandro. No tenemos aún un repo o una traza atribuible a esos equipos. No afirmar que sabemos cómo lo hacen, que mienten o que usan métodos prohibidos.

## 3. Qué hemos probado ya y qué conclusiones sobreviven

Orientación: ESTADO, NORMAS, HALLAZGOS y los informes motor/transmisión/categorías/DeepSeek/palancas. También se recuperó trabajo sin commit de esta misma rama: [análisis de trazas](../independent-designs/principles-evidence/phase-1.md), [auditoría de creencias](../independent-designs/principles-evidence/phase-2.md) y tres experimentos. No es una revisión ciega: había conocimiento histórico y se leyeron los archivos de orientación obligatorios.

- El mejor planificador real medido promedia **72,39** en 360 partidas, mediana **74,9**. Es un resultado fuerte, no una prueba de que 75 sea imposible. M17 y M21 documentan búsquedas finitas de parámetros, no un certificado de optimalidad.
- Las reglas de historias pueden contaminar otras decisiones; mejorar obediencia no basta si la interpretación es falsa.
- Los tipos gruesos y los signos imperfectos pierden información; medir sólo recall de riesgo o Skill no mide el daño de la opción finalmente elegida.
- Los dos fracasos históricos de DeepSeek no establecen su capacidad máxima. La revisión de trazas identifica pérdidas de promoción antes de la primera explosión y notas que obedecen una regla mientras describen mal su consecuencia.
- La frase de A2 sobre todos los techos de L1 era demasiado fuerte: en la réplica Skill tiene margen; Network y Output son los frágiles sin margen. No trasladar sus números a un Skill.
- Riesgo y no ascender son rutas dominantes en ciertos bots, no las únicas formas de perder. Salud y ruina también aparecen.
- **Sobrevivir no basta:** deduplicando registros exportados por `job_id`, t13-final Haiku oficial tiene n=12, media57,24 y diez carreras completas de media64,53; f3-lean oficial n=43, media50,52 y treinta completas de media60,37. Ninguna de esas carreras alcanza75. También falta calidad entre las completadas.

Las pruebas recuperadas comparan distintos controladores con dos lecturas DeepSeek **ya guardadas**, no al modelo ejecutando decisiones. El baseline observado da47,89; conocer todos los signos reales da53,92; imponer primero un veto de riesgo da53,43; signos reales más veto59,91; contexto ideal más signos reales67,05. En 2.000 semillas. Son resultados condicionales al controlador, no límites universales ni una predicción del agente.

Auditamos la recuperación: cuatro brazos ×300 semillas coinciden fila a fila con sus resultados originales. Los primeros archivos recuperados no guardaban hash del script; no ocultar esa limitación.

## 4. Pruebas nuevas: no repetir la carrera de manuales

**Primer checkpoint offline:** ninguna partida oficial, llamada de modelo ni gasto nuevo. Sólo réplica y lecturas congeladas. La continuación con208 decisionesHaiku está documentada al final. Todos los brazos de un experimento parten de las mismas semillas; las trayectorias pueden divergir después de elegir. Los intervalos son incertidumbre sobre carreras simuladas **condicionada a dos lecturas fijas**, no sobre nuevas lecturas, nuevos eventos ni transferencia a otro modelo. No sumar ganancias de experimentos distintos.

| Intervención | Datos | Resultado y decisión |
|---|---|---|
| Usar desacuerdo de dos lecturas para riesgo | 600 semillas/brazo | Veto con una lectura51,92; con dos52,95. Δ+1,03, IC95%[−0,14;+2,20]. No justifica un gran salto ni otra llamada |
| Ser pesimista con todos los signos | Mismo experimento |50,82; peor que usar el desacuerdo sólo en riesgo. No llevarlo al modelo |
| Planificar todo el trimestre con la misma utilidad miope |400/brazo |55,46→52,76; Δ−2,70[−3,88;−1,51]. Fallos de salud6→41. Optimizar el objetivo equivocado empeora; no refuta toda planificación conjunta |
| Aumentar bienestar desde distintos niveles |800/brazo |Control53,69; desde L3 52,49; L4 53,07; L5 53,70; L6 53,68. Esta regla no resuelve el objetivo |
| Calibración online por grupos, recuperada |2.000/brazo |47,89→47,82; sin mejora. Sólo refuta ese calibrador estrecho, no todo aprendizaje en partida |
| Mantenimiento fijo de riesgo, recuperado |2.000/brazo |47,89→42,23; gastar en limpieza a calendario no sustituye buen control |

Archivos: [resumen numérico](summary.csv), `uncertainty-screen.json`, `quarter-screen.json`, `objective-screen.json`; scripts correspondientes `gpt_incertidumbre.py`, `gpt_trimestre.py`, `gpt_objetivo.py` bajo `scripts/deepseek/`.

## 5. Hallazgo nuevo: signo de riesgo no equivale a magnitud

Se aisló la representación usando **el mismo Planner**, sin mirar la continuación futura de una historia. Todos los brazos disponen de contexto privilegiado: riesgo actual, techos y umbrales verdaderos, y efectos trimestrales conocidos. Este control es un diagnóstico de información; **no puede entregarse como Skill ni presentarse como nota esperable de DeepSeek**.

Factorial de800 semillas por brazo:

| Efectos visibles de historias | Riesgo de historias | Q media | Finalizan | Crisis |
|---|---|---:|---:|---:|
| Magnitudes exactas | Magnitud exacta |71,10|93,6%|23|
| Magnitudes exactas | Sólo signo |53,95|54,1%|353|
| Signos perfectos | Magnitud exacta |70,69|94,4%|9|
| Signos perfectos | Sólo signo |58,11|66,8%|244|
| Signos perfectos | Signo, con veto previo |64,13|85,5%|7|
| Signos DeepSeek guardados | Signo DeepSeek |49,95|55,6%|228|
| Signos DeepSeek guardados | Signo DeepSeek, con veto |55,14|69,8%|27|

Manteniendo signos visibles perfectos, recuperar la magnitud del riesgo añade **12,58 puntos**, IC95%[11,18;13,97]. Con riesgo exacto, pasar de magnitudes visibles exactas a signos perfectos cambia−0,41[−1,20;+0,39]. No demuestra equivalencia, pero señala claramente dónde se concentra esta pérdida para este controlador.

**La interpretación correcta no es que ahora necesitemos otra taxonomía.** La política admitía riesgos como si todo “+” fuera pequeño. Un controlador que recibe signos debe tratar la magnitud desconocida como incertidumbre, no como un coste exacto de un punto.

Pantalla posterior de600 semillas nuevas: valorar conservadoramente cada riesgo positivo recupera, con signos perfectos,56,54→68,66/69,09; con signos DeepSeek,50,34→56,73/56,40. Para la variante intermedia, Δ+6,39[4,92;7,86]. No lee la magnitud verdadera de cada opción. Sigue usando contexto privilegiado del Planner; aún no es una vía a75.

Datos: [factorial corregido](risk-factorial-corrected.json), [pantalla de márgenes](risk-margin-screen.json). El primer `risk-factorial.json` utilizaba magnitud exacta en el brazo `signs_veto` antes de aplicar el veto. Está marcado como sustituido para ese brazo; se corrigió y se reprodujeron todos los brazos. No usar su65,14 como resultado del veto con sólo signos.

La prueba sin privilegios ya está terminada:2.000 semillas nuevas, controlador observado48,83; margen prudente51,37 (Δ+2,54, IC95%[1.77;3.31]); veto52,99. Caps aprendidos en la carrera y HR retrasado. No supera al veto ya conocido ni abre una vía demostrada a75. **No trasladar esta variante a Haiku como candidata prometedora.** Datos: [risk-margin-observed.json](risk-margin-observed.json).

## 6. Qué NO sabemos y qué debe cambiar a continuación

No hay evidencia para atribuir a los equipos una técnica concreta. Los Skills públicos leídos no aportan la demostración que buscamos. Las etiquetas guardadas y los bots muestran mecanismos; no sustituyen al agente completo. Más semillas sobre dos lecturas tampoco aportan más independencia del modelo.

La vía que merece continuar es **medir la elección y su margen de daño**, no seguir optimizando acierto de etiquetas aisladas. Hace falta separar:

- riesgo inadvertido de la opción elegida;
- riesgo reconocido pero admitido por perseguir crecimiento;
- errores de preservación antes de una evaluación;
- retrasos de promoción y calidad final entre las carreras que sobreviven;
- pérdidas por memoria, alcance de regla o ejecución.

Antes de gastar cuota en un nuevo manual, exigir que una intervención sobreviva sin estado ideal. Si pasa, escribir una variante inglesa general con comprobación breve de la decisión propuesta, sin tablas de eventos, umbrales internos ni pesos investigados. Contrastar contra un control contemporáneo con el mismo actor y transporte. No vender una mejora de banco o Haiku como75 de DeepSeek. La verificación target queda pendiente mientras siga vigente la instrucción de no usar su API.

## Relevo

- **Hecho y por qué:** reconstrucción desde reglas públicas y trazas; auditoría de lo ya probado; búsqueda pública ampliada; recuperación reproducida; intervenciones sobre incertidumbre, objetivo, planificación e información. El objetivo sigue abierto.
- **Resultados:** el factorial identifica el coste de comprimir magnitud de riesgo; una precaución derivada mejora el bot privilegiado, pero no alcanza75. Los demás intentos nuevos no justifican partidas con IA. Detalle y límites arriba; los JSON guardan resúmenes y hashes; cada `.json.gz` conserva el JSON original completo con resultados por semilla. Se comprimen para mantener revisable el diff.
- **Datos:** no se han añadido textos de eventos ni claves a esta carpeta. Lecturas originales en `~/careerlab-data/deepseek/labels/ds-v3-r{1,2}-full.json`; datos narrativos siguen fuera del repo. Las tablas de esta carpeta son investigación, no archivos que deba leer el jugador.
- **Coste:** cero API DeepSeek, cero partidas Claude, cero subagentes. No se han modificado candidatos actuales ni enviado entregas.
- **Validación:** recuperación4×300 coincide exactamente; suite del repo313 tests pasa. Reproducir con `uv run python scripts/deepseek/gpt_riesgo.py --out /tmp/risk-factorial.json` y `uv run python scripts/deepseek/gpt_margen.py --out /tmp/risk-margin.json`. No apuntar `--out` a resultados congelados si se quiere conservarlos.
- **Pendiente inmediato:** no repetir las variantes de esta carpeta. La precaución no mejora al veto observado. Investigar por separado la calidad de la decisión nativa del modelo, la compresión de consecuencias y los errores de ejecución: propuesta seguida de comprobación breve antes de actuar, con un control contemporáneo y consecuencias de la opción elegida como medida. Sólo pasar a partidas si una prueba de banco lo justifica; anunciar número y topes en ESTADO antes de lanzarla. Si se obtiene evidencia de los equipos75, contrastar versión, configuración, muestra y trazas públicas.
- **Integración:** commit `4cd5ac8` publicado en `alejandro/gpt-principios`; [PR22](https://github.com/aleetreny/huawei/pull/22) abierto para revisión y unión a main. No marcar el objetivo como completado ni reemplazar automáticamente la entrega vigente.

### Formato de los datos congelados

Cada JSON de experimento es un resumen revisable con enlace y hash de su `.json.gz`. El archivo comprimido conserva todos los campos originales, incluidas las filas por semilla. Para comprobar o recuperar: `gzip -dc lab/reports/deepseek/gpt-principios/risk-margin-observed.json.gz > /tmp/risk-margin-observed-full.json`. Los hashes `uncompressed_sha256` se refieren a esos bytes originales. `summary.csv` conserva también el factorial inicial para trazabilidad: usar `risk-factorial-corrected.json` para `signs_veto`. No contar duplicados de reproducción como experimentos independientes.

## Continuación: decisión nativa y entorno de ejecución

La prueba [propuesta + comprobación](decision-audit.md) ha terminado con Haiku5.5, actor real identificado en sus streams:92 situaciones de48 títulos, ambos brazos y24 repeticiones de control. Selección y hashes en `decision-audit-selection.json`. No son carreras completas. Ambas variantes pasan lint y las208 pruebas cargaron el Skill, sin acciones inválidas. La comprobación no mejoró: riesgo4→5/92, dominadas3→6/92, con cumplimiento92/92. No pasará a partidas. Datos narrativos fuera del repo en `~/careerlab-data/deepseek/gpt-decision-audit/`.

Además, [la auditoría del runtime](runtime-audit.md) descubre una traza oficial de DeepSeek viva enmes33/L2 al terminar por `max_continuations`, con42 negativas genéricas en chino. Las tres preferencias actuales de idioma son `zh`. El parche inglés está preparado y probado con33 tests offline, sin aplicarlo a instancias ni tocar el ejecutor común de forma permanente. No prueba causalidad ni una nota mejor.

**Relevo de la continuación:** proceso terminado con208 resultados; no reanudar ni repetir. Para reproducir sólo el análisis, `uv run python scripts/deepseek/gpt_decision_score.py` exige que estén los208 resultados y usa efectosv2, sin Q antiguo. Si hay un fallo de transporte o tope de cuota, inspeccionar el resultado concreto antes de reintentar; no reiniciar por tiempo de observación agotado. No interpretar el banco como75 ni llamar a DeepSeek.

**Cierre del segundo checkpoint:** la prueba negativa de autocomprobación separa adherencia de calidad. La siguiente prueba requiere feedback público nuevo y debe distinguir aprendizaje nativo del calibrador por grupos que ya falló. [Diseño y datos](decision-audit.md). El runtime en chino es una discrepancia concreta con parche revisable; la causalidad y el75 siguen sin demostrar. No se alteró ninguna instancia ni se inició una partida DeepSeek.

## Checkpoint28oct: carreras nativas y nuevo estado del equipo

[Caracterización completa](native-pilot.md): tresHaiku reales66,86/18,23/64,15; cuarta cancelada antes de empezar, sin sustituir derrotas. El banco limitado no predecía fiabilidad. [Aprendizaje de ganancias](feedback-caps.md): no mejora clara con expectativasDScongeladas; no repetir. [Replay](native-quarter-replay.md): un reparto mejor puede llevar un camino aL6/~70,6, pero no75ni rescatar otro.

**Relevo:** todos los procesos de este checkpoint terminaron; datos narrativos fuera deGit. `gpt_native_pilot.py --run` no debe retomarse. Prototipo observable-allocation-v1 sólo lint, sin admisión. Verificados11tests de truncation/completion, compilación de scripts y guardas sintéticas de aprendizaje. Cuota compartida5h11→14%, semana38→38%; ninguna llamadaDeepSeek.

El28oct al revalidar `origin/main` aparece evidencia posterior deotraslíneas: v4DeepSeek71,67/70,22 y un script oficial76,87, con media de familia mucho menor. Formato midió52herramientas reales incluidasbash/code; nuestroproxy5herramientas+Skillno reproduce ese ámbito. Cambiar la siguiente investigación aesas trazas yevitar duplicar su veto híbrido. Esto es progreso de evidencia, no75estable ni atribución a equipos externos. Solicitar integración del checkpoint conmain enPR22.
