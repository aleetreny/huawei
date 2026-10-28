# ESTADO del proyecto: léelo primero

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*. Actualizado: **28 oct 2026, noche** (corte 1 entregado; línea Techo añadida como subtrabajo de DeepSeek).

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
| **Suelo** (subtrabajo de DeepSeek) | ¿Cómo evitar que una de las 3 partidas se hunda? | `claude/linea-suelo-hundimientos-5xjrnm` (juntada en `main`) | [lab/reports/suelo/](lab/reports/suelo/) · `scripts/suelo/` · manuales `lab/policies-src/suelo/suelo-v1`, `suelo-v1-min` | **Cerrada el 28 oct (20:00 UTC) a falta de DeepSeek.** Réplica con B30: la mitad de las atascadas en L1 se salvan solas en el mes 18; con regla de rescate, riesgo a 0 en casi todas. «Si todo es arriesgado, el menor riesgo» baja las crisis a una séptima parte (B36–B38). Lint limpio; juez: `suelo-v1-min` 62/66 frente a 61/63 de v4-c5. Banco de trampas con Haiku: Haiku no cambia de elección con el texto (C44) | Chat local, ≈ 3,5 USD: juez con DeepSeek, banco de trampas con DeepSeek y 3 partidas; regla de decisión en [suelo §6](lab/reports/suelo/README.md) |

**Subtrabajo de la línea DeepSeek — Techo** (28 oct, noche; rama `alejandro/tender-franklin-3ap5yw`, carpeta [lab/reports/techo/](lab/reports/techo/), código `scripts/techo/`, candidatos `lab/policies-src/techo/v4-t0` y `v4-t1`): por qué las partidas completas se quedan en L5. Réplica: las reglas de v4 llegan a L4 en el mes 24 y a L5 en el 42 (planificador: 20 y 36); la ventana del 18 se pierde por Network en L3 y las del 30/36 por el ritmo de Skill en L4; la ventaja del planificador es sobre todo tolerar riesgo con el contador a 0, y eso **no se traslada** como regla escrita. Lo que aguanta: trimestre a Skill desde L4 (+0,5; L6 ×1,5 con lectura exacta), Dignity desde 7 (+0,4), Skill doble en historias desde L4 (+0,2); con la lectura de DeepSeek, L6 sigue en el 2–3 % (HALLAZGOS B36–B38). Siguiente paso, con la clave: banco de DeepSeek «Skill en L4» con `v4-t0` (~0,2 USD) y controles de historias con `v4-t1` (~0,5 USD), juez con DeepSeek, y 3 partidas del elegido ([plan](lab/reports/techo/README.md) §7).

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
- Cuota de Claude: sin topes de equipo desde el 28 oct. Las herramientas sólo esperan si la ventana de 5 horas pasa del 95 %, y el ritmo semanal ya no se aplica salvo que `quota_cap.json` lo pida (`weekly_pace`). Ojo: la semana de la cuenta se reinicia el 2 nov a las 16:00 UTC, después del último corte; si se agota antes, no queda Claude para nadie hasta el final del reto.
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
