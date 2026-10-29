# ESTADO del proyecto: léelo primero

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*. Actualizado: **29 oct 2026, noche** (línea Mejora juntada en `main`: candidato `mejora/mv-4`, C68–C72) (notas oficiales del corte 1; comprobante y exploración juntados en `main`; permiso de los organizadores para el bucle de fichas y los scripts en partida, también con estado en archivo, C60).

Si sólo puedes leer tres archivos: este, [HALLAZGOS.md](HALLAZGOS.md) (todo lo aprendido, por importancia) y [NORMAS.md](NORMAS.md) (cómo trabajamos).

## 1. El reto en cinco líneas

- Un juego de texto: una IA vive 48 meses de carrera en una empresa. Cada mes responde a 3 historias y cada trimestre reparte energía. Cada 6 meses hay una evaluación que puede subirla de nivel.
- Se pierde por no ascender (despido), por acumular riesgo oculto (crisis de confianza) o por agotamiento. Al final hay una nota de 0 a 100.
- **No jugamos nosotros:** entregamos un manual (Skills, en inglés) que lee **DeepSeek** (`deepseek-v4-flash`) dentro del programa oficial JiuwenSwarm.
- Nota de cada versión: 80 % la media de 3 partidas, 10 % la calidad de los SKILL.md y 10 % el ahorro de tokens. Cuenta la mejor versión.
- Los 10 mejores pasan a un jurado (vídeo y documentos de diseño), que vale el 30 % de la nota final.

## 2. Dónde vamos, en una frase

**Corte 1 oficial: 64,75, puesto 13** (el top 10 empieza en 68,17; el primero tiene 75,99; HALLAZGOS C45). Cuadra con lo esperado de v4: partidas de ~65 de media con algún hundimiento. El juego de la evaluación parece el de desarrollo.

**El manual de referencia es `comprobante/cp-v12`:** las reglas de cp-v5a más el bucle de dos llamadas por respuesta, que da una nota de fichas de ~95–100 con cualquier proveedor (C51–C59). Los organizadores lo permiten (C49). Con partidas como las de v4 daría ~68.

**Candidato para entregar: `mejora/mv-4` (línea Mejora, 29 oct, noche; [informe](lab/reports/mejora/README.md)).** Son las reglas de historias de v4 con la lectura de los costes ocultos en los meses de evaluación (banco de L1: pérdida 2,51 frente a 3,31–3,68 de v4), el trimestre y el freno de salud de ex-v1, y el bucle de cp-v12 copiado byte a byte. Fichas 95–100. En 10 partidas reales, 6 completas (media 68,1, una de 77,78 en L6) y 3 hundidas: no juega visiblemente mejor que v4, pero suma ~+3,5 de nota de versión por fichas y calidad. **No entregar `ex-v1` ni `ex-v3` tal cual: su bucle no empareja con DeepInfra (0 de 3 sondas).** Hallazgos C68–C72.

**Antes: candidato `exploracion/ex-v1`.** Es cp-v12 con trimestres mejores y un freno de salud, y el texto reescrito para la rúbrica. En la réplica calibrada con las partidas reales (C61) suma +1,8 de partidas (C64) y +8 de calidad con los jueces de Claude (C66). Antes de entregarlo hacen falta las sondas de la pareja y el banco de L1, ~0,2 USD: [plan-deepseek.md](lab/reports/exploracion/plan-deepseek.md).

**Lo que falta es percepción, no reglas ni scripts:**
- en la réplica calibrada, las reglas y los scripts mueven la media ±1–2 (C63, C64);
- el hueco con el planificador perfecto (~15) se concentra en el mes previo a cada evaluación, sobre todo en L1 (C62);
- la única regla nueva con señal es `exploracion/ex-v3`: lo discreto antes que plantarse en público en el mes previo de L1 (C65). Pendiente del banco de DeepSeek.

**Antes de nada, en un chat nuevo:** lee [pendientes.md](lab/reports/deepseek/pendientes.md) (candidatos y siguiente paso) y la cabecera de [comprobante.md](lab/reports/deepseek/comprobante.md).

## 3. Líneas activas (máximo 3)

| Línea | Pregunta | Rama | Carpeta | Estado (27 oct, 23:45) | Siguiente paso |
|---|---|---|---|---|---|
| **DeepSeek** | ¿Cómo sube la nota de DeepSeek a partir de los mejores manuales? | `alejandro/deepseek` (worktree `~/huawei-ds`) | [lab/reports/deepseek/](lab/reports/deepseek/) · `scripts/deepseek/` · manuales `lab/policies-src/deepseek/` · **datos [lab/data/deepseek/](lab/data/deepseek/README.md)** | `t13-read-v4` 71,67 y 70,22 sigue siendo el mejor. **28 oct** ([hacia-80](lab/reports/deepseek/hacia-80.md)): una media de 80 está por encima del techo (jugador perfecto 72,4); `t13-read-v8`, `t13-read-v9` y `perceive-v5` descartados en el banco (1,6 USD, sin partidas). **29 oct:** todo lo pagado de DeepSeek está en Git: 21 partidas (seis cortadas recuperadas, entre ellas v3 hasta el mes 48), `partidas.csv`, `decisiones.csv.gz`, bancos, etiquetas (NORMAS §1.6) | Candidatos pendientes en [pendientes.md](lab/reports/deepseek/pendientes.md) (los prueba otro chat); quien gaste DeepSeek vuelve a exportar con `scripts/deepseek/export_data.py` |
| **Entrega** | Vídeo, documentos de diseño y paquete de cada corte | `alejandro/deepseek` (documentos en `docs/entrega/cut1-t13-read-v4/`) | [docs/entrega/](docs/entrega/) | **Corte 1 entregado (27 oct):** `t13-read-v4`, ZIP en `~/careerlab-data/entrega/cut1/`, validación oficial OK, vídeo de 6 min 22 s. Matteo tiene un guion y una auditoría de cumplimiento en `matteo-review/cut1` | **Corte 2 (30 oct) preparado a falta del manual:** borradores en inglés con `TODO(manual)` en [docs/entrega/cut2/](docs/entrega/cut2/PREPARAR.md) y `scripts/entrega/build_cut.py`. El script valida, comprueba inglés, vídeo y títulos, avisa si es idéntico a un corte ya puntuado y crea el ZIP. Copia del corte 1 en iCloud Drive (`huawei-entrega-copia/`). Cuando el comprobador decida: rellenar los `TODO` y empaquetar |
| **Comprobante** | ¿Cuál es el mejor manual para DeepSeek? | `alejandro/comprobante` (worktree `~/huawei-comp`) | [lab/reports/deepseek/comprobante.md](lab/reports/deepseek/comprobante.md) · `scripts/comprobante/` · manuales `lab/policies-src/comprobante/` | **29 oct, 18:05 UTC. Base de entrega: `cp-v12`** = reglas de cp-v5a sin tocar + bucle de cp-v10 (pareja sembrada en «Continue», silencio opcional, menú del trimestre aprendido en la partida). Dos partidas completas, 56,80 y 62,83, pareja 100 %, fichas 100 con proveedores distintos; cp-v5a sigue valiendo si el proveedor sirve razonamiento. Las reglas nuevas de cp-v8 → cp-v11 quedan fuera (3 hundidas de 5; excepción de cp-v8 dudosa en pendientes) hasta calibrar la réplica con las 35 partidas reales. Familia: 19 partidas largas, 13 completas (65,2), 4 hundidas. Pauta recurrente en L1: compra Skill y Network en su tope mientras Output se queda a 0 (5 partidas). Gasto 11,1 USD | Calibrar la réplica con las partidas reales; sonda con historial para «no se mueve»; acortar la sección del bucle |
| **Mejora** (subtrabajo de DeepSeek) | ¿Qué manual saca más nota de versión que v4, partiendo de sus reglas? | `alejandro/mejora-v4` (worktree `~/huawei-mejora`) | [lab/reports/mejora/](lab/reports/mejora/README.md) · `scripts/mejora/` · manuales `lab/policies-src/mejora/` | **29 oct, 22:45 UTC. Candidato `mv-4`.** Banco de DeepSeek: mejor lectura del mes previo de L1 de 9 variantes, sin empeorar los controles. Sondas: el bucle de ex-v1 no empareja con DeepInfra y el de cp-v12 sí. 10 partidas: mv-3 68,64 · 77,78 (L6) · 66,06 · cortada por `max_continuations` (respuestas sin llamada; arreglado en mv-4); mv-4 63,35 · 69,62 · 37,06 · 18,98 · 63,27; control cp-v12 20,73. Gasto 3,23 USD | Adaptar `docs/entrega/cut2/` a mv-4 si se entrega. Para la media de partidas: los hundimientos, probando primero en el banco (informe §8) |


**En pausa, fuera del cupo:** Formato (`alejandro/formato`, [lab/reports/formato/](lab/reports/formato/)): mejor partida 76,87 pero media 49,9; sólo vuelve si una idea concreta gana en la réplica. Sus hallazgos ya están en HALLAZGOS (B27, C23).

**Cerradas y juntadas en `main`** (sus informes siguen en su carpeta): **Exploración** (`lab/reports/exploracion/`, rama `claude/gradient-depression-skills-k3b6u0`, 29 oct): réplica calibrada con las decisiones reales de DeepSeek, descomposición de los puntos, scripts con estado medidos, candidatos `ex-v1`/`ex-v3`/`ex-s1` y plan de pruebas para DeepSeek (C61–C67); **Suelo** (`lab/reports/suelo/`, B33–B35) y **Techo** (`lab/reports/techo/`, B36–B38), las dos el 28 oct; Motor (`lab/reports/ingenieria-inversa/`, réplica al 99,3 %), Categorías (`lab/reports/question-bank/`), Transmisión (`lab/reports/transmision/`), Palancas (`lab/reports/palancas/`), Mecánicas emergentes (`lab/reports/mecanicas-emergentes/`), la auditoría desde principios básicos (`lab/reports/deepseek/gpt-principios/`) el 28 oct, **Huevos de Pascua** (`lab/reports/huevos-pascua/`): no hay atajos de ascenso en el juego de desarrollo, pero la tercera evaluación en L1 se salva con el riesgo a cero (HALLAZGOS B28–B30); y **Calidad** (`lab/reports/calidad-skills/`): candidato `lab/policies-src/calidad/v4-c5`, +4,2 de calidad con las mismas elecciones que v4 en el banco con Haiku (C24, C25). Sólo bots y Claude, 0 USD.

**Pendiente para la línea DeepSeek (con la clave):** todo lo que falta confirmar está en [pendientes.md](lab/reports/deepseek/pendientes.md), con su coste, sus comandos y su regla de decisión.

**Apoyo a DeepSeek (actualización mv-3/mv-4, sin API):** [consistencia de 77,78](lab/reports/deepseek/gpt-principios/mv-3-mv-4-consistencia.md): revisadas nueve intentadas de Mejora desde su worktree; ocho puntuadas (58,095), seis completas (68,12), una L6. Prioridades: modo estricto realmente aplicado y adelantar ascensos sin crisis.

**Apoyo a DeepSeek (29 oct, diagnóstico sin API):** [estancamiento y vías de mejora](lab/reports/deepseek/gpt-principios/diagnostico-estancamiento.md): eficiencia mejorada, juego aún sin superioridad demostrada; control de política/bucle y evaluación de decisiones críticas antes de nuevas versiones.

**Apoyo a DeepSeek:** `alejandro/gpt-principios` (PR #23): [auditoría adversarial del corte 2](lab/reports/deepseek/gpt-principios/auditoria-cut2.md), handbook corregido y documentos cp-v5a actualizados; propuesta trimestral pendiente del comprobador, sin API.

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
