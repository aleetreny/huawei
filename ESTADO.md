# ESTADO del proyecto: léelo primero

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*. Actualizado: **27 oct 2026, 16:00 UTC** (reorganización del repo).

Si sólo puedes leer tres archivos: este, [HALLAZGOS.md](HALLAZGOS.md) (todo lo aprendido, por importancia) y [NORMAS.md](NORMAS.md) (cómo trabajamos).

## 1. El reto en cinco líneas

- Un juego de texto: una IA vive 48 meses de carrera en una empresa. Cada mes responde a 3 historias y cada trimestre reparte energía. Cada 6 meses hay una evaluación que puede subirla de nivel.
- Se pierde por no ascender (despido), por acumular riesgo oculto (crisis de confianza) o por agotamiento. Al final hay una nota de 0 a 100.
- **No jugamos nosotros:** entregamos un manual (Skills, en inglés) que lee **DeepSeek** (`deepseek-v4-flash`) dentro del programa oficial JiuwenSwarm.
- Nota de cada versión: 80 % la media de 3 partidas, 10 % la calidad de los SKILL.md y 10 % el ahorro de tokens. Cuenta la mejor versión.
- Los 10 mejores pasan a un jurado (vídeo y documentos de diseño), que vale el 30 % de la nota final.

## 2. Dónde vamos, en una frase

Sabemos casi exactamente cómo funciona el juego (simulador al 99 %) y qué habría que hacer (la política óptima saca 72 en el juego real), pero **la IA no sabe ver qué indicador sube o baja cada respuesta**, y los manuales con IA siguen en ~50. El trabajo de ahora es esa percepción: categorías de respuestas que la IA reconozca y reglas que obedezca sin estropear el resto.

## 3. Líneas activas (máximo 3)

| Línea | Pregunta | Rama | Carpeta | Estado (27 oct, 16:00) | Siguiente paso |
|---|---|---|---|---|---|
| **Motor** | ¿Cómo funciona el juego por dentro y cuál es la jugada óptima? | `main-1nddsg` | [lab/reports/ingenieria-inversa/](lab/reports/ingenieria-inversa/) · código `scripts/ingenieria-inversa/` · datos `lab/data/ingenieria-inversa/` | Simulador validado (99,3 %); política óptima 72,4 en 360 partidas reales; 7 reglas generales; la función de valor no mejora al planificador (M29) | Pasar las reglas que aguantan a principios generales; medir si DeepSeek detecta las respuestas arriesgadas |
| **Categorías** | ¿Se pueden agrupar las respuestas en tipos que la IA reconozca, con una respuesta buena por tipo? | `alejandro/optimistic-gauss-edyw1j` | [lab/reports/question-bank/](lab/reports/question-bank/) · `scripts/question-bank/` | **En pausa, sustituida por DeepSeek (27 oct)**. 10 tipos etiquetados a ciegas: separan el riesgo (78 %); un bot que sólo ve el tipo saca 47 frente a 68; lo que falta es saber qué indicador mueve cada respuesta | Mejorar la detección de Skill en la taxonomía; medir cómo etiqueta DeepSeek (~0,02 USD, si lo aprueba Alejandro) |
| **Transmisión** | ¿Cómo se escribe una regla para que la IA la obedezca? | `alejandro/transmision` | [lab/reports/transmision/](lab/reports/transmision/) · `scripts/transmision/` · manuales `lab/policies-src/transmision/` | **En pausa, sustituida por DeepSeek (27 oct, 16:00)** ([prompt](lab/reports/transmision/prompt-deepseek.md)). Banco de 3.573 situaciones; el reparto trimestral obedece, las reglas de historias contaminan; el interruptor “Review in N” aísla una regla; manual recomendado `t13-final` (73 en la rúbrica; 57,2 frente a 50,5 de f3-lean en partidas de Haiku, 12 frente a 43) | Banco y percepción con DeepSeek |
| **DeepSeek** | ¿Qué entiende DeepSeek de cada respuesta (indicador que mueve y riesgo) y qué categorías y reglas obedece? | `alejandro/deepseek` | [lab/reports/deepseek/](lab/reports/deepseek/) · `scripts/deepseek/` · manual `lab/policies-src/deepseek/t13-read-v1/` | **Banco y simulador hechos (27 oct, 17:15)**. DeepSeek ve el riesgo (83–92 %) y no Skill ni Output (45–49 %); la mejor categorización es leer seis signos + riesgo (bot 56,0 frente a 46,7 de los tipos de Haiku); lee y obedece t13-final; `t13-read-v1` arregla los detonantes y empata en historias. Gastado 1,98 de 5 USD. [Diseños independientes](lab/reports/deepseek/independent-designs/README.md): 3 alternativas, guía y crítica; recomendado A, sin probar ni gastar. [Revisión 2](lab/reports/deepseek/independent-designs/review-2.md): fallos priorizados, parche propuesto y auditoría de medición; sin cambios de código ni partidas | Partidas oficiales de `t13-read-v1` sólo con el visto bueno de Alejandro |
| **Palancas** | ¿Cuánta nota vale cada herramienta o pista del juego que no usamos (nota como memoria, techos, avisos, reputación antes de la evaluación, riesgo en cifras, tokens) y cómo hacer que la IA la use? | `alejandro/palancas` | [lab/reports/palancas/](lab/reports/palancas/) · `scripts/palancas/` · manuales `lab/policies-src/palancas/` | **27 oct, 18:10.** La palanca buena es una línea de estado fija en la nota; lo que más vale apuntar es el techo del nivel, descubierto en la partida: +8,8 en el simulador, +4,9 con la detección de Haiku (49–63 %). Haiku arrastra la línea tras un resumen y no tiñe las historias. Candidato `t19-final` (= `t13-final` + línea). Avisos, reputación y cifras de riesgo: ~0. Tokens: máximo +0,7. Sin partidas ni DeepSeek | Que la línea DeepSeek mida la línea de estado (¿detecta el techo?, tokens por mes); con permiso, ~10 partidas de Haiku sólo para comprobar que nada se rompe |
| **Formato** | ¿Cambiando la forma de dar el manual (qué recibe el agente, cuándo, qué puede hacer con ello) se acerca DeepSeek a 75? | `alejandro/formato` | [lab/reports/formato/](lab/reports/formato/) · `scripts/formato/` · manuales `lab/policies-src/formato/` | **27 oct, 21:00.** El agente oficial tiene `bash` y `code` y puede ejecutar un script del Skill en partida (probado con un modelo falso, coste 0). Manual `script-v1`: DeepSeek sólo lee y etiqueta cada opción; el script decide con memoria propia. Simulador con lecturas de DeepSeek: 51,5 (lecturas exactas 63,4). **Lanzando partidas oficiales con DeepSeek (tope de la línea 8 USD, máx. 2 a la vez, slots propios en `~/careerlab-data/formato/`)** | Partidas de `script-v1`; si se sostiene, mejorar lectura y regla |

**Trabajo de motor terminado y juntado en main (27 oct, 17:05):** `alejandro/mecanicas-emergentes` ([PR #20](https://github.com/aleetreny/huawei/pull/20)), [informe y Relevo](lab/reports/mecanicas-emergentes/README.md): cierre +0,552 Q (IC 95% [0,298; 0,805], 600 partidas oficiales); corrección de nómina terminal; sin IA de pago. No abre una cuarta línea activa.

**Otras ramas.** Las de Matteo (`matteo/...`, `Matteo`, `matteo-t4-growth`) y la de Leah (`leah/workspace`) las gestionan ellos.

**Apoyo de entrega documentado (27 oct):** borradores ingleses de [diseño](docs/entrega/skills_design-draft.md) y [decisiones](docs/entrega/decision_report-draft.md), más [nota de cumplimiento t19](docs/entrega/t19-compliance.md), en `alejandro/entrega`. Pendiente resolver `TODO(final)` contra t13-read-v2 congelado y copiar los documentos aprobados al paquete. Sin partidas ni API; no abre otra línea de investigación.

## 4. Fechas (hora UK)

| Fecha | Qué hay |
|---|---|
| **27 oct, 24:00** | **Corte 1.** La entrega necesita `presentation.mp4`, `design/skills_design.md`, `design/decision_report.md` y las Skills. **Pendiente: vídeo (equipo), documentos de diseño y paquete.** Guion base: [docs/entrega/jury-story.md](docs/entrega/jury-story.md) |
| 30 oct, 24:00 | Corte 2 |
| 1 nov, 24:00 | Corte 3, el último |

## 5. Decisiones en vigor

- Se permiten partidas con modelos de Claude como sustitutos de DeepSeek; los bots no tienen límite.
- **Dinero:** sólo los 50 USD de la clave de DeepSeek (OpenRouter), en el `.env` del Mac de Alejandro. Quedan ~49,8 USD. DeepSeek sólo en pruebas aprobadas por Alejandro, con 15 USD de reserva para el último corte. Presupuesto: [docs/entrega/target-budget.md](docs/entrega/target-budget.md).
- No preguntamos en Discord. Riesgo conocido: la norma dice *"the absence of an express prohibition is not permission"*.
- Claude no aparece como contribuidor en GitHub.
- Cuota: ritmo semanal de [NORMAS.md](NORMAS.md) §5. A las 15:00 del 27 oct la semana iba por el 34 %.
- Manual de referencia para comparar en partidas: `f3-lean-v1` (~51 de nota con Haiku, 30 partidas).

## 6. Mapa

| Para | Dónde |
|---|---|
| Todo lo aprendido, por importancia | [HALLAZGOS.md](HALLAZGOS.md) |
| Cómo trabajamos | [NORMAS.md](NORMAS.md) |
| Índice de informes (activos e históricos) | [lab/reports/README.md](lab/reports/README.md) |
| Instalar y usar el laboratorio (partidas, bots, registro) | [lab/README.md](lab/README.md) |
| Reglas oficiales | `sh scripts/setup_official_runner.sh`, después `local-runs/official-runner/docs/` |
| Entrega: guion del vídeo, presupuesto de DeepSeek | [docs/entrega/](docs/entrega/) |
| Historia del proyecto hasta el 26 oct (carrera de manuales, ESTADO antiguo, investigación inicial) | [docs/historico/](docs/historico/README.md) |
