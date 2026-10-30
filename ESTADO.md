# ESTADO del proyecto: léelo primero

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*. Actualizado: **30 oct 2026, tarde** (línea Mejora cerrada y juntada en `main`, C68–C79; auditoría de Codex C73).

Si sólo puedes leer tres archivos: este, [HALLAZGOS.md](HALLAZGOS.md) (todo lo aprendido, por importancia) y [NORMAS.md](NORMAS.md) (cómo trabajamos).

## 1. El reto en cinco líneas

- Un juego de texto: una IA vive 48 meses de carrera en una empresa. Cada mes responde a 3 historias y cada trimestre reparte energía. Cada 6 meses hay una evaluación que puede subirla de nivel.
- Se pierde por no ascender (despido), por acumular riesgo oculto (crisis de confianza) o por agotamiento. Al final hay una nota de 0 a 100.
- **No jugamos nosotros:** entregamos un manual (Skills, en inglés) que lee **DeepSeek** (`deepseek-v4-flash`) dentro del programa oficial JiuwenSwarm.
- Nota de cada versión: 80 % la media de 3 partidas, 10 % la calidad de los SKILL.md y 10 % el ahorro de tokens. Cuenta la mejor versión.
- Los 10 mejores pasan a un jurado (vídeo y documentos de diseño), que vale el 30 % de la nota final.

## 2. Dónde vamos, en una frase

**Corte 1 oficial: 64,75, puesto 13** (el top 10 empieza en 68,17; el primero tiene 75,99; C45). **El corte 2 cierra hoy, 30 oct, a las 24:00 (hora de Reino Unido).**

**Qué entregar.** La nota de versión es 0,8 × la **media** de 3 partidas + 0,1 × calidad + 0,1 × fichas, y cuenta la mejor versión entregada. Hay dos candidatos, los dos con las fichas resueltas: nota ~100 frente a ~64 de v4, es decir, +3,5 de nota de versión con las mismas partidas.

| Candidato | Qué es | Pruebas |
|---|---|---|
| **`mejora/mv-5r`** (recomendado) | reglas de v4 vía ex-v1 + trimestre por tramos y freno de salud + lectura de costes ocultos sólo en L1 + bucle de cp-v12 | sin defectos conocidos; partidas 22,65 · 69,00 · 24,51 |
| **`mejora/v4-loop`** | v4 tal cual + sólo el bucle de cp-v12 | fichas confirmadas (302 y 432 mil por mes); partidas 23,23 · 58,95 |

**No entregar:** `mv-3`, `ex-v1` ni `ex-v3`, por sus defectos del bucle (C69, C70).

**Qué sabemos** ([mejora](lab/reports/mejora/README.md), C68–C79):
- en el juego de historias, todas las versiones son v4 dentro del ruido;
- la trampa de L1 (pérdidas forzosas en el mes previo y riesgo acumulado pronto) sigue siendo el problema número uno;
- un manual más corto elige igual (C78);
- en la réplica, ningún mecanismo medido pasa de P(Q ≥ 72) 25 %.

Los 6 despidos en L1 de las últimas 14 partidas, con cualquier manual, están por confirmar (C79).

**Dinero: la clave queda en 14,44 USD**, por debajo de los 15 de reserva con permiso de Alejandro.

**Antes de nada, en un chat nuevo:** lee [pendientes.md](lab/reports/deepseek/pendientes.md) (candidatos y siguiente paso) y la cabecera de [comprobante.md](lab/reports/deepseek/comprobante.md).

## 3. Líneas activas (máximo 3)

| Línea | Pregunta | Rama | Carpeta | Estado (27 oct, 23:45) | Siguiente paso |
|---|---|---|---|---|---|
| **DeepSeek** | ¿Cómo sube la nota de DeepSeek a partir de los mejores manuales? | `alejandro/deepseek` (worktree `~/huawei-ds`) | [lab/reports/deepseek/](lab/reports/deepseek/) · `scripts/deepseek/` · manuales `lab/policies-src/deepseek/` · **datos [lab/data/deepseek/](lab/data/deepseek/README.md)** | `t13-read-v4` 71,67 y 70,22 sigue siendo el mejor. **28 oct** ([hacia-80](lab/reports/deepseek/hacia-80.md)): una media de 80 está por encima del techo (jugador perfecto 72,4); `t13-read-v8`, `t13-read-v9` y `perceive-v5` descartados en el banco (1,6 USD, sin partidas). **29 oct:** todo lo pagado de DeepSeek está en Git: 21 partidas (seis cortadas recuperadas, entre ellas v3 hasta el mes 48), `partidas.csv`, `decisiones.csv.gz`, bancos, etiquetas (NORMAS §1.6) | Candidatos pendientes en [pendientes.md](lab/reports/deepseek/pendientes.md) (los prueba otro chat); quien gaste DeepSeek vuelve a exportar con `scripts/deepseek/export_data.py` |
| **Entrega** | Vídeo, documentos de diseño y paquete de cada corte | `alejandro/deepseek` (documentos en `docs/entrega/cut1-t13-read-v4/`) | [docs/entrega/](docs/entrega/) | **Corte 1 entregado (27 oct):** `t13-read-v4`, ZIP en `~/careerlab-data/entrega/cut1/`, validación oficial OK, vídeo de 6 min 22 s. Matteo tiene un guion y una auditoría de cumplimiento en `matteo-review/cut1` | **Corte 2 (30 oct) preparado a falta del manual:** borradores en inglés con `TODO(manual)` en [docs/entrega/cut2/](docs/entrega/cut2/PREPARAR.md) y `scripts/entrega/build_cut.py`. El script valida, comprueba inglés, vídeo y títulos, avisa si es idéntico a un corte ya puntuado y crea el ZIP. Copia del corte 1 en iCloud Drive (`huawei-entrega-copia/`). Cuando el comprobador decida: rellenar los `TODO` y empaquetar |
| **Comprobante** | ¿Cuál es el mejor manual para DeepSeek? | `alejandro/comprobante` (worktree `~/huawei-comp`) | [lab/reports/deepseek/comprobante.md](lab/reports/deepseek/comprobante.md) · `scripts/comprobante/` · manuales `lab/policies-src/comprobante/` | **29 oct, 18:05 UTC. Base de entrega: `cp-v12`** = reglas de cp-v5a sin tocar + bucle de cp-v10 (pareja sembrada en «Continue», silencio opcional, menú del trimestre aprendido en la partida). Dos partidas completas, 56,80 y 62,83, pareja 100 %, fichas 100 con proveedores distintos; cp-v5a sigue valiendo si el proveedor sirve razonamiento. Las reglas nuevas de cp-v8 → cp-v11 quedan fuera (3 hundidas de 5; excepción de cp-v8 dudosa en pendientes) hasta calibrar la réplica con las 35 partidas reales. Familia: 19 partidas largas, 13 completas (65,2), 4 hundidas. Pauta recurrente en L1: compra Skill y Network en su tope mientras Output se queda a 0 (5 partidas). Gasto 11,1 USD | Calibrar la réplica con las partidas reales; sonda con historial para «no se mueve»; acortar la sección del bucle |

| **Tramos** (subtrabajo de DeepSeek) | ¿Se puede saber antes de jugar partidas enteras si un manual hace jugar mejor a DeepSeek? | `alejandro/tramos` (worktree `~/huawei-tramos`) | [lab/reports/tramos/](lab/reports/tramos/README.md) · `scripts/tramos/` · datos `lab/data/deepseek/tramos/` | **30 oct, 16:00 UTC.** El banco no pregunta en las condiciones de la partida. Arnés `fiel.py`: motor oficial y petición exacta de JiuwenSwarm, validado contra las partidas reales. JiuwenSwarm devuelve el razonamiento al historial y manda `top_p` 0,1 (tramos-1). Ascenso en el mes 6: fiel, v4 1 de 4 y v4-loop 3 de 4; sin razonamiento, 2 de 12 y 11 de 14 (tramos-3). **17:00:** lo que decide es salir de L1 antes del mes 12 (si no, despido en 10 de 11 partidas reales) y el arnés ya lo mide; los tramos sirven de puerta y diagnóstico, no para afinar (tramos-4). Gasto 1,92 USD | **Corte 2:** mv-5r frente a v4-loop hasta el mes 12, 15 tramos por brazo (~1,5 USD, falta el permiso) |

**En pausa, fuera del cupo:** Formato (`alejandro/formato`, [lab/reports/formato/](lab/reports/formato/)): mejor partida 76,87 pero media 49,9; sólo vuelve si una idea concreta gana en la réplica. Sus hallazgos ya están en HALLAZGOS (B27, C23).

**Cerradas y juntadas en `main`** (sus informes siguen en su carpeta): **Mejora** (`lab/reports/mejora/`, rama `alejandro/mejora-v4`, cerrada el 30 oct). Candidatos `mv-5r` y `v4-loop` (§10–§12), mapa de pérdidas por evaluación, banco reservado de riesgo, versiones corta y de calidad descartadas, y 17 partidas de DeepSeek (C68–C79). **Exploración** (`lab/reports/exploracion/`, rama `claude/gradient-depression-skills-k3b6u0`, 29 oct): réplica calibrada con las decisiones reales de DeepSeek, descomposición de los puntos, scripts con estado medidos, candidatos `ex-v1`/`ex-v3`/`ex-s1` y plan de pruebas para DeepSeek (C61–C67); **Suelo** (`lab/reports/suelo/`, B33–B35) y **Techo** (`lab/reports/techo/`, B36–B38), las dos el 28 oct; Motor (`lab/reports/ingenieria-inversa/`, réplica al 99,3 %), Categorías (`lab/reports/question-bank/`), Transmisión (`lab/reports/transmision/`), Palancas (`lab/reports/palancas/`), Mecánicas emergentes (`lab/reports/mecanicas-emergentes/`), la auditoría desde principios básicos (`lab/reports/deepseek/gpt-principios/`) el 28 oct, **Huevos de Pascua** (`lab/reports/huevos-pascua/`): no hay atajos de ascenso en el juego de desarrollo, pero la tercera evaluación en L1 se salva con el riesgo a cero (HALLAZGOS B28–B30); y **Calidad** (`lab/reports/calidad-skills/`): candidato `lab/policies-src/calidad/v4-c5`, +4,2 de calidad con las mismas elecciones que v4 en el banco con Haiku (C24, C25). Sólo bots y Claude, 0 USD.

**Pendiente para la línea DeepSeek (con la clave):** todo lo que falta confirmar está en [pendientes.md](lab/reports/deepseek/pendientes.md), con su coste, sus comandos y su regla de decisión.

**Apoyo — revisión para Opus, 30 oct (integración selectiva):** [encargo 72+ frecuente / 78 automático](lab/reports/deepseek/gpt-principios/encargo-opus-78.md), [evidencia](lab/reports/deepseek/gpt-principios/revision-opus-78.md), C73. Con eficiencia 100, calidad 80 exige juego medio 75. Prioridades propuestas: ventanas de evaluación perdidas, riesgo innecesario y calidad por separado. Sólo documentación y auditorías offline; candidato y operación intactos. Opus puede valorar qué aporta a su trabajo actual. Sin DeepSeek ni partidas nuevas; no hay garantía de 78 consistente.

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
- **Discord (29 oct):** el reglamento obliga a preguntar en Discord antes de usar un método dudoso (*"the absence of an express prohibition is not permission"*), así que se pregunta. Los organizadores dijeron que sí a tres preguntas (HALLAZGOS C49):
  1. varias llamadas a herramientas en una misma respuesta, y pedir al agente que escriba poco;
  2. scripts del Skill que usan sólo lo que devuelve la partida en curso;
  3. describir lo observado en nuestras partidas como observaciones y heurísticas propias.
  4. (después) que un script guarde un archivo de datos durante la partida para recordar entre llamadas; dura sólo esa partida (C60).
  Lo que sigue prohibido: tablas o datos sacados del paquete del motor, y umbrales o fórmulas presentados como reglas del juego.
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
