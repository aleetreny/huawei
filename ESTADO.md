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
| **DeepSeek** | ¿Cómo sube la nota de DeepSeek a partir de los mejores manuales? | `alejandro/deepseek` (worktree `~/huawei-ds`) | [lab/reports/deepseek/](lab/reports/deepseek/) · `scripts/deepseek/` · manuales `lab/policies-src/deepseek/` | `t13-read-v4` 71,67 y 70,22; `t13-read-v7` 67,27; `t13-read-v5` 66,71. Una tercera de v4 se quedó en L1 y murió por un choque de puertos. [Informe](lab/reports/deepseek/mejora-nota.md). Clave: quedan 35,8 USD (23:30) | Variantes de v4 contra la trampa de L1, primero en la réplica y el banco; partidas sólo para confirmar |
| **Entrega** | Vídeo, documentos de diseño y paquete de cada corte | `alejandro/deepseek` (documentos en `docs/entrega/cut1-t13-read-v4/`) | [docs/entrega/](docs/entrega/) | **Corte 1 entregado (27 oct):** `t13-read-v4`, ZIP en `~/careerlab-data/entrega/cut1/`, validación oficial OK, vídeo de 6 min 22 s. Matteo tiene un guion y una auditoría de cumplimiento en `matteo-review/cut1` | Corte 2 (30 oct): mismo proceso con el mejor manual de DeepSeek; revisar los documentos frente a los Skills entregados |

**En pausa, fuera del cupo:** Formato (`alejandro/formato`, [lab/reports/formato/](lab/reports/formato/)): mejor partida 76,87 pero media 49,9; sólo vuelve si una idea concreta gana en la réplica. Sus hallazgos ya están en HALLAZGOS (B27, C23).

**Cerradas y juntadas en `main`** (sus informes siguen en su carpeta): Motor (`lab/reports/ingenieria-inversa/`, réplica al 99,3 %), Categorías (`lab/reports/question-bank/`), Transmisión (`lab/reports/transmision/`), Palancas (`lab/reports/palancas/`), Mecánicas emergentes (`lab/reports/mecanicas-emergentes/`), la auditoría desde principios básicos (`lab/reports/deepseek/gpt-principios/`) el 28 oct, **Huevos de Pascua** (`lab/reports/huevos-pascua/`): no hay atajos de ascenso en el juego de desarrollo, pero la tercera evaluación en L1 se salva con el riesgo a cero (HALLAZGOS B28–B30); y **Calidad** (`lab/reports/calidad-skills/`): candidato `lab/policies-src/calidad/v4-c5`, +4,2 de calidad con las mismas elecciones que v4 en el banco con Haiku (C24, C25). Sólo bots y Claude, 0 USD.

**Pendiente para la línea DeepSeek (con la clave):** confirmar `v4-c5` con el juez y el banco de DeepSeek (≈ 1,3 USD; comandos y regla de decisión en [calidad-skills §4](lab/reports/calidad-skills/README.md)) y llevar B30 al manual.

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

**Apoyo gpt-principios:**PR23/alejandro/gpt-principios, informes propios preservados tras merge de main. Preferencia deAlejandro:priorizarSonnet como proxy en proximas pruebasLLM, sin inferir equivalenciaDeepSeek. Pruebasrecientes yaSonnet; modoslocalesbot completados dev60validas ycompetition32validas/28KeyError(session_id), comparacioncondicionada no concluyente. Sin nuevosmodelos/API.

**B30revisado:**terceraoportunidadL1existe;probedegrade replica compatible en3estadossinteticos. No Skillconmesesprivados. Proxima pantalla:feedbackHRtrasestancamiento, sin llamadas actuales.

**Recuperacionstall offlinecerrada:**600semillas porbrazo,49,643→49,628,deltaCIincluye0;1072reparaciones sinmejora. NoadmisionSonnet. Sin llamadas.

**Nueva fuente publica:**Kingjinsightv11raw73,1verificado n1, modelopendiente. Commit e6c33cb; auditarSkills/procedencia antesdeprobar. No75estable demostrado.

**Publicv11auditado:**modeloDSflashreportado(2usage,2unknown);scriptlee logMCP,modosN/G/R/D,trimestresdeterministas,LLMhistorias. n1raw73,1,scriptsemantica/compliancependiente. No copiarSkillnumerico.

**V11helper:**3pruebas aisladas de ledger pasan; usa efectosregistradosvsestado. Trimestres/modos contienenconstantesnoportables sin revision. No candidata75ni llamadas.
