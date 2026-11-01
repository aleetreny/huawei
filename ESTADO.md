# ESTADO del proyecto: cerrado

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*. Actualizado: **1 nov 2026, noche**, después del último corte.

La competición ha terminado. Todas las ramas están juntadas en `main` y no queda ninguna línea activa. La historia del proyecto está en el [README](README.md); lo aprendido, por importancia, en [HALLAZGOS.md](HALLAZGOS.md).

## 1. Entregas

| Corte | Manual | Nota oficial | Paquete y documentos |
|---|---|---:|---|
| 1 · 27 oct | `t13-read-v4` | 64,75 (puesto 13) | [docs/entrega/cut1-t13-read-v4/](docs/entrega/cut1-t13-read-v4/) |
| 2 · 30 oct | `mv-5r` | 45,44 | [docs/entrega/cut2/](docs/entrega/cut2/) |
| 3 · 1 nov | `mv-3` | pendiente | [docs/entrega/cut3-mv3/](docs/entrega/cut3-mv3/), vídeo en [docs/entrega/cut3-video/](docs/entrega/cut3-video/README.md) |

Presentación final publicada en GitHub Pages: <https://aleetreny.github.io/huawei/> (la monta `.github/workflows/pages.yml` desde `docs/entrega/cut3-video/presentacion-c.html`).

## 2. Líneas de trabajo (todas cerradas)

Cada línea tiene su informe en `lab/reports/<línea>/` y su código en `scripts/<línea>/`. Índice: [lab/reports/README.md](lab/reports/README.md).

| Línea | Pregunta | Informe |
|---|---|---|
| Ingeniería inversa (Motor) | ¿Cómo funciona el juego por dentro? Réplica al 98,5 % | [ingenieria-inversa/](lab/reports/ingenieria-inversa/README.md) |
| Techo y Suelo | ¿Cuánto se puede sacar y dónde se hunden las partidas? | [techo/](lab/reports/techo/), [suelo/](lab/reports/suelo/) |
| DeepSeek | ¿Cómo sube la nota de DeepSeek? | [deepseek/](lab/reports/deepseek/) |
| Comprobante | El bucle de dos llamadas (fichas 95–100) | [comprobante.md](lab/reports/deepseek/comprobante.md) |
| Exploración | Réplica calibrada con las decisiones de DeepSeek | [exploracion/](lab/reports/exploracion/) |
| Mejora | Más nota de versión que v4 partiendo de sus reglas (`mv-*`) | [mejora/](lab/reports/mejora/README.md) |
| Tramos | Medir partes de una partida con DeepSeek | [tramos/](lab/reports/tramos/) |
| Corte 3 | Qué entregar el último día | [corte3/](lab/reports/corte3/README.md) |
| Auditoría desde principios básicos | Qué falta para 72+ frecuente | [gpt-principios/](lab/reports/deepseek/gpt-principios/README.md) |
| Calidad, Transmisión, Palancas, Categorías, Formato, Mecánicas emergentes, Huevos de Pascua, Fuentes externas | Ver el índice | [lab/reports/](lab/reports/README.md) |
| Estudios de Matteo y Leah | Crecimiento observado, primera evaluación, percepción de estadísticas | `lab/reports/*-study/`, `lab/reports/stat-perception/`, `docs/historico/research/matteo/` |

## 3. Qué está fuera de Git

En el Mac de Alejandro, `~/careerlab-data/` (1,7 GB tras la limpieza del 1 nov):

- `entrega/`: la carpeta `solution/` de cada corte, sin el vídeo (los vídeos y los ZIP se borraron el 1 nov; el Skill y los documentos están en Git);
- `reglas-oficiales/` y `literatura/`: las reglas del programa oficial y la bibliografía de competiciones parecidas;
- `ingenieria-inversa/`: lotes brutos de bots jugados en el Mac (se rehacen con bots);
- `palancas/`, `deepseek/`, `comprobante/`, `tramos/`…: bancos y registros intermedios que se rehacen con CPU; todo lo que costó dinero de DeepSeek está en [lab/data/deepseek/](lab/data/deepseek/README.md);
- `respaldo-git-2026-11-01.bundle`: copia de todas las ramas antes de juntarlas y de reescribir la autoría.

Las instalaciones del programa oficial (`target-slots`, `formato/slot-*`, `local-runs/`) se borraron: se rehacen con `sh scripts/setup_official_runner.sh`.

## 4. Decisiones que siguen valiendo

- **Dinero:** la clave de DeepSeek (50 USD) se gastó en las pruebas aprobadas por Alejandro; no queda nada pendiente.
- **Discord (29 oct):** los organizadores permitieron varias llamadas a herramientas por respuesta, scripts del Skill con lo que devuelve la partida en curso (también con estado en archivo), y describir lo observado como heurísticas propias (HALLAZGOS C49, C60).
- **Prohibido en un Skill:** tablas o datos del paquete del motor, y umbrales o fórmulas presentados como reglas del juego ([NORMAS.md](NORMAS.md) §4).
