# ESTADO del proyecto: léelo primero

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*. Actualizado: **27 oct 2026, 23:45 UTC** (corte 1 entregado; ramas juntadas; repo fuera de iCloud).

Si sólo puedes leer tres archivos: este, [HALLAZGOS.md](HALLAZGOS.md) (todo lo aprendido, por importancia) y [NORMAS.md](NORMAS.md) (cómo trabajamos).

## 1. El reto en cinco líneas

- Un juego de texto: una IA vive 48 meses de carrera en una empresa. Cada mes responde a 3 historias y cada trimestre reparte energía. Cada 6 meses hay una evaluación que puede subirla de nivel.
- Se pierde por no ascender (despido), por acumular riesgo oculto (crisis de confianza) o por agotamiento. Al final hay una nota de 0 a 100.
- **No jugamos nosotros:** entregamos un manual (Skills, en inglés) que lee **DeepSeek** (`deepseek-v4-flash`) dentro del programa oficial JiuwenSwarm.
- Nota de cada versión: 80 % la media de 3 partidas, 10 % la calidad de los SKILL.md y 10 % el ahorro de tokens. Cuenta la mejor versión.
- Los 10 mejores pasan a un jurado (vídeo y documentos de diseño), que vale el 30 % de la nota final.

## 2. Dónde vamos, en una frase

**DeepSeek ya termina carreras:** `t13-read-v4` saca 71,67 y 70,22 en partidas completas (L5, riesgo 0), y es lo que se entregó en el corte 1. El trabajo ahora es partir de los mejores manuales y cambiar una cosa cada vez para subir hacia 75. Lo que más resta es la trampa del primer ascenso (L1), que es sobre todo de percepción.

## 3. Líneas activas (máximo 3)

| Línea | Pregunta | Rama | Carpeta | Estado (27 oct, 23:45) | Siguiente paso |
|---|---|---|---|---|---|
| **DeepSeek** | ¿Cómo sube la nota de DeepSeek a partir de los mejores manuales? | `alejandro/deepseek` (worktree `~/huawei-ds`) | [lab/reports/deepseek/](lab/reports/deepseek/) · `scripts/deepseek/` · manuales `lab/policies-src/deepseek/` | `t13-read-v4` 71,67 y 70,22; `t13-read-v7` 67,27; `t13-read-v5` 66,71. Una tercera de v4 se quedó en L1 y murió por un choque de puertos. [Informe](lab/reports/deepseek/mejora-nota.md). Clave: quedan 35,8 USD (23:30) | Variantes de v4 contra la trampa de L1, primero en la réplica y el banco; partidas sólo para confirmar. Apoyo gpt-principios: [capacidad/feedback](lab/reports/deepseek/gpt-principios/capacity-and-learning.md), contraste43menus terminado sin mejora (13→14perdidas), no candidato; [ideas del usuario](lab/reports/deepseek/gpt-principios/user-ideas.md): tres pruebas terminadas sin mejora; sin DeepSeek nuevo |
| **Formato** | ¿Dar el manual de otra forma (script del Skill que decide) acerca a 75? | `alejandro/formato` (worktree `.claude/worktrees/formato`) | [lab/reports/formato/](lab/reports/formato/) · `scripts/formato/` · manuales `lab/policies-src/formato/` | **En pausa.** Mejor partida de DeepSeek (76,87, L6), pero media 49,9 en 5 partidas frente a ~71 de v4, y ~2,3 M fichas por mes. Hallazgos útiles: el agente oficial tiene `bash`/`code`, el mensaje de sistema va en chino | Sólo si una idea concreta (veto del script sobre v4) gana en la réplica antes de jugar |
| **Entrega** | Vídeo, documentos de diseño y paquete de cada corte | `alejandro/deepseek` (documentos en `docs/entrega/cut1-t13-read-v4/`) | [docs/entrega/](docs/entrega/) | **Corte 1 entregado (27 oct):** `t13-read-v4`, ZIP en `~/careerlab-data/entrega/cut1/`, validación oficial OK, vídeo de 6 min 22 s. Matteo tiene un guion y una auditoría de cumplimiento en `matteo-review/cut1` | Corte 2 (30 oct): mismo proceso con el mejor manual de DeepSeek; revisar los documentos frente a los Skills entregados |

**Cerradas y juntadas en `main`** (sus informes siguen en su carpeta): Motor (`lab/reports/ingenieria-inversa/`, réplica al 99,3 %), Categorías (`lab/reports/question-bank/`), Transmisión (`lab/reports/transmision/`), Palancas (`lab/reports/palancas/`), Mecánicas emergentes (`lab/reports/mecanicas-emergentes/`), la auditoría desde principios básicos (`lab/reports/deepseek/gpt-principios/`) y, el 28 oct, **Huevos de Pascua** (`lab/reports/huevos-pascua/`): no hay atajos de ascenso en el juego de desarrollo; sólo bots, 0 USD (HALLAZGOS B28, B29).

**Apoyo a DeepSeek,28oct:** auditoría `alejandro/gpt-principios`, [checkpoint](lab/reports/deepseek/gpt-principios/native-pilot.md). Tres carrerasHaiku nativas66,86/18,23/64,15; cuarta cancelada sin empezar, no75estable. Auditoria del76,87terminada (750salidas/747acciones/5memorias exactas); correcciones de riesgo/HR no mejoran. CapacidadSonnet49,95/L4terminada. Feedback real16pares con pequena senal que no se mantiene en43objetivos restantes (13→14perdidas, riesgo2→2);118decisiones validas. Todo terminado, sin nuevo manual admitido. No APIDeepSeek de esta auditoría; no duplicar el veto híbrido deFormato. El objetivo externo de75repetible permanece abierto y no crea una cuarta línea.

**Diagnóstico de capacidad anunciado28oct:** apoyo de `alejandro/gpt-principios`: hasta25llamadasMax (una admisión READY/Sonnet +12menúsL1 por Haiku/Sonnet), mismo manualv4 congelado. No partidas completas ni APIDeepSeek. Selección sin etiquetas, diseño en capacity-probe-plan.json; límites0,65/0,45, secuencial y máximo4procesos. Primero obtener cuota actual; si supera topes, no abrir la tanda.

**Referencia Sonnet anunciada28oct:** una carrera nueva con v4sin modificar, misma entregaCLIemulada y herramientas oficiales. Diagnostico de capacidad, no ensayo de estabilidad: doce menus previos dieronSonnet0vsHaiku1perdida de crecimiento evitable, riesgo2ambos. Maximo1carrera, sin reemplazar resultados, sin APIDeepSeek; admision con semana<=40% y guardas0,65/0,45, maximo4procesos. No interrumpir una carrera lanzada por nota/cuota; no se programa otra. Datos propios en gpt-sonnet-reference/.

**Aprendizaje anunciado28oct:** hasta32decisionesHaikuMax sobre16menusL1con el mismo v4, historia previa identica y diferencia unica: un brazo ve el panel posterior real del episodio anterior. Seleccion congelada, eventos de distinto titulo, sin efectos privados ni nuevas partidas/DeepSeek. Fuente son nuestras herramientas publicas; texto fuera deGit. Cuota actual5h3%, semana40%, limites0,65/0,45 y maximo4procesos. Diagnostico de revision de creencias, no nueva taxonomia ni calibrador numerico de techos.

**Ampliacion de feedback anunciada28oct:** completadas32decisionesHaiku: perdidas6→4, evitablespre-evaluacion1→0, riesgo1→1; n16no demuestra eficacia. Contraste fijado antes de nuevas llamadas: los43menus elegibles restantes, sin solapar objetivos, mismos brazos/Skill/criterios,86decisionesHaikuMax como maximo. Comparten carreras y episodios docentes, no es replica en corpus independiente. Secuencial, cuota5h3%/semana40%, guardas0,65/0,45, max4procesos. Cero partidas nuevas/DeepSeek. Sonnetreferencia ya termino49,95/L4/48meses, sin repetir. **Cerrado:**86/86decisiones delcontraste validas,13→14perdidas y2→2riesgos; no admitir a carreras.

**Ablacion de narrativa anunciada28oct:** apoyo gpt-principios, mismo v4/Haiku5.5:32menusL1(16antesdeevaluacion),64decisionesMaxmaximo. Un brazo recibe observacioncompleta; otro conserva estado/opciones/avisos y omite solo titulo/narracion. Seleccion sin catalogo, planes/hashes previos, sin registrosanteriores ni juegos nuevos/DeepSeek. Cuota fresca5h3%/semana40%, guardas0,65/0,45 y max4procesos, secuencial. Riesgo mayor bloquea admision; medir perdidas evitables y recursos. No prometerQ por un banco.

**Segunda lectura con evidencia anunciada28oct:** a raiz de lasideasdeAlejandro,16lecturasindependientesHaikuMax maximo sobre los16menuspre-evaluacion ya congelados en ablacion. El revisor no ve eleccion/notas iniciales; responde4preguntas factuales con cita literal de la accion o unclear, y recomienda opcion usando v4. Regla de combinacion fijada antes: solo reemplazar si hay coste explicito en la primera y la recomendada no tiene ninguno ni incertidumbre en crecimiento/riesgo (y dinero si saldo mostrado<=0). Sin juegos nuevos/DeepSeek. Cuota fresca5h4%/semana40%, guardas0,65/0,45, max4procesos. Una lectura de transporte primero; fallos se conservan, no se sustituyen.

**Contexto fresco anunciado28oct:**24relecturasSonnetMax maximo de todas lashistorias justoantesdeevaluacion de su carrera v4ya terminada. Mismo modelo5.5, Skill y systemprompt originalexacto; paneloriginal + ultimas3notas previas, sin mostrar eleccionactualoriginalni futuro. Compara con24elecciones de la carrera real; no se eligen solo errores. Sin partidas nuevas/DeepSeek. Cuota fresca5h4%/semana40%, guardas0,65/0,45, max4procesos, secuencial. Diagnostico de contexto, no nota ni ensayoaleatorizado de carrera. Ablacion64ycritico16ya terminados sin candidato superior.

**Cierre de ideas28oct:**104lecturasCLI nuevas (64ablacion/16criticas/24contextofresco), cero juegosnuevos/DeepSeek. Ablacion empeora1→3riesgos/0→3evitables; factgate0cambios; contextofresco conserva22/24elecciones y2evitables/3riesgos originales. No nuevoSkilladmitido. Todosprocesosterminados, cuota compartida5h4%/semana40%; informe user-ideas.md yPR23.

**Otras ramas.** Las de Matteo (`matteo/...`, `matteo-review/cut1`, `matteo-t4-growth`) y la de Leah (`leah/workspace`) las gestionan ellos.

**Coordinación entre chats (27 oct).** La clave es compartida: medir el coste de cada partida con `total_cost` del informe, nunca con la diferencia de saldo; el vigilante de `careerlab.target` sólo apunta (`CAREERLAB_TARGET_NEVER_STOP=1`) y **ninguna partida lanzada se corta**. Arrancar instancias de JiuwenSwarm de una en una, con `lsof` antes: dos a la vez chocan en los puertos. No tocar `local-runs/official-runner/.env`.

## 4. Fechas (hora UK)

| Fecha | Qué hay |
|---|---|
| 27 oct, 24:00 | Corte 1: **entregado** `t13-read-v4` |
| **30 oct, 24:00** | **Corte 2** |
| 1 nov, 24:00 | Corte 3, el último |

## 5. Decisiones en vigor

- Se permiten partidas con modelos de Claude como sustitutos de DeepSeek; los bots no tienen límite.
- **Dinero:** sólo los 50 USD de la clave de DeepSeek (OpenRouter), en el `.env` del Mac de Alejandro. Quedan ~35,8 USD (27 oct, 23:30). Hay una clave propia de OpenRouter preparada y sin comprar ([clave-propia.md](lab/reports/deepseek/clave-propia.md)). DeepSeek sólo en pruebas aprobadas por Alejandro, con 15 USD de reserva para el último corte. Presupuesto: [docs/entrega/target-budget.md](docs/entrega/target-budget.md).
- No preguntamos en Discord. Riesgo conocido: la norma dice *"the absence of an express prohibition is not permission"*.
- Claude no aparece como contribuidor en GitHub.
- Cuota: ritmo semanal de [NORMAS.md](NORMAS.md) §5. A las 15:00 del 27 oct la semana iba por el 34 %.
- Manual de referencia para comparar en partidas: `f3-lean-v1` (~51 de nota con Haiku, 30 partidas).

## 6. Mapa

| Para | Dónde |
|---|---|
| Dónde está el repo | `~/huawei` (fuera de iCloud desde el 27 oct; la ruta antigua de iCloud es un enlace a esta). Copias duplicadas de iCloud apartadas en `~/huawei-icloud-duplicados/` |
| Todo lo aprendido, por importancia | [HALLAZGOS.md](HALLAZGOS.md) |
| Cómo trabajamos | [NORMAS.md](NORMAS.md) |
| Índice de informes (activos e históricos) | [lab/reports/README.md](lab/reports/README.md) |
| Instalar y usar el laboratorio (partidas, bots, registro) | [lab/README.md](lab/README.md) |
| Reglas oficiales | `sh scripts/setup_official_runner.sh`, después `local-runs/official-runner/docs/` |
| Entrega: guion del vídeo, presupuesto de DeepSeek | [docs/entrega/](docs/entrega/) |
| Historia del proyecto hasta el 26 oct (carrera de manuales, ESTADO antiguo, investigación inicial) | [docs/historico/](docs/historico/README.md) |

**Revision factual de carrera anunciada28oct:**24lecturasSonnetMax maximo, mismas preguntas y gate anteriores sobre todos24turnoscriticos reales, sin elegir por errores. Sin juegos/DeepSeek. Cuota fresca5h4%/semana40%, topes0,65/0,45 y4procesos. No reparar/repetir citas no literales; fallbackprimera. Plan fact-career-plan.json.

**Revision factual real cerrada:**24/24validas;gate2cambios,riesgo3→4,evitables2→2. No admitir a carreras. Proceso terminado, sin nuevos juegos/DeepSeek. Resultado fact-career-results.json en apoyo gpt-principios.

**Diagnostico factual:** ambos errores reales sin flags de coste; unflag sobre opcionsegura causa cambioarriesgado. No afinar gate por esoscasos. Analisisoffline fact-bottleneck.json, sin llamadas adicionales.

**Suficiencia factual:**3/24menus contienen opciones con lasmismas4respuestas y diferentescostes/riesgo. Analisisoffline fact-sufficiency.json; no otra candidatura ni llamadas.

**Apoyo gpt-principios actualizado:**main e332b14 integrado; revisada lineaLeah532d672.74,3delean esrubrica,noQ; no candidato75nuevo ni llamadas. No duplicar lean ni atajos cerrados.

**Hipotesis runtime pendiente:**auditar thinking/esfuerzo en solicitudes reales, sinAPIninuevaspartidas. API directaDeepSeek no implica defaultsOpenRouter/Jiuwen; ausencia en transcript no prueba desactivacion. Apoyo gpt-principios.

**Auditoria reasoning:**traza76,87sin metadatos de razonamiento yconfigsactualesFormato sin campos thinking/effort; modo efectivo indeterminado, no disabled demostrado. Proximo:adaptador publicoJiuwen. Sin llamadas/cambiosslots.
