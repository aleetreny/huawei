# Carrera rápida: rediseño del 26 oct (chat `alejandro/carrera-rapida`)

Petición de Alejandro (26 oct, ~19:00 UTC): "vamos muy lento; si un manual no funciona no lo usamos; descubrir más rápido y probar sólo sobre lo que funciona; poner recursos donde hay valor; ideas valientes cuando nos atascamos; DeepSeek sólo cuando sea seguro que es útil".

## Qué había y por qué iba lento

- Unas 450 partidas de Haiku repartidas entre 40 manuales, casi todos con 3 a 10 partidas. Las reglas de prereg-v1 casi nunca descartaban (sólo 2 manuales dormidos), así que las partidas se diluían.
- Las hijas se escribían desde tablas resumen, y ninguna superó a su madre. La familia se estimaba junta, así que las hijas malas hundían a su madre (F7).
- Los manuales nuevos esperaban en una cola por tandas detrás de manuales flojos. Las ideas de Matteo entraban como manuales, pero no como lecciones para quien escribía los siguientes.
- La suerte engaña: la nota del líder bajó de 61 a 55 al acumular partidas, y la v3 de Matteo pasó de 71,4 (4 partidas) a 51,0 (8 partidas).

## Qué se ha hecho

| Pieza | Dónde |
|---|---|
| Escalera campeón-aspirantes (2/4/8/12 partidas; descarte por probabilidad de ser mejor) | `careerlab/ladder.py`, comando `careerlab ladder` |
| Planificador continuo (una partida por hueco libre, siempre la de más prioridad) | `careerlab/scheduler.py`, `careerlab run --continuous` |
| Retirar partidas en cola de un manual descartado | `Registry.cancel_queued` en `careerlab/store.py` |
| Diseñador automático (Opus, sin terminal) y sus instrucciones: variante, ambiciosa, valiente, reparación | `scripts/fastloop/design.py`, `lab/fastloop/briefs/` |
| Driver que une todo y escribe el estado cada 10 minutos | `scripts/fastloop/driver.py` |
| Lecciones con evidencia para los diseñadores | `lab/fastloop/lessons.md` |
| Ritmo semanal adelantado (por tramos) | `weekly_allowance` con `knots`; el driver lo escribe en `quota_cap.json` |
| Protocolo y calibración | `lab/protocol/fastloop-v2.md`, `scripts/fastloop/calibrate.py` |
| Explicación para el equipo y guía para la nube | `lab/fastloop/README.md`, `scripts/fastloop/README.md` |

**Decisiones y motivo**
- **Probabilidad de ser mejor, no la media.** El juego tiene dos resultados típicos (terminar con unos 61 o caer con unos 29), así que el modelo separa la tasa de terminar de la nota al terminar. Con la media sola se coronaban demasiados manuales con suerte.
- **Umbrales 0,05 / 0,15 / 0,60 (ampliar entre 0,35 y 0,60).** De las cinco variantes simuladas, esta es la que descarta rápido sin coronar con 4 partidas. Las cifras están en la tabla de calibración del protocolo.
- **Diseñador que lee partidas enteras.** Es lo que hacía bien Matteo, y además está escrito para que no dependa de que el chat de la nube esté atento.
- **Ritmo semanal adelantado.** A las 19:00 la semana iba por el 7 % con 6,8 días por delante, y los descubrimientos tempranos valen para los tres cortes.

## Resultados

- Pruebas: `uv run pytest -q` da 264 OK, 9 de ellas nuevas en `tests/test_ladder.py`.
- Calibración (simulada con las partidas reales): uno claramente mejor gana el título el 94 % de las veces en unas 8 partidas. Uno mucho peor queda fuera tras unas 2,3 partidas de media, y uno algo peor se cuela el 13 % de las veces.
- Copia del registro real (e17b598): el campeón inicial es F1, con 56,1 de media en 12 partidas (10 terminadas). Le siguen f3-balance-recombined (56,5 en 7) y f3-lean (56,7 en 5). F7 baja a 49,3 en 16.
- Diseñador de punta a punta, con Sonnet en esfuerzo bajo sólo para probar la tubería: tardó 0,6 minutos y su manual pasó el lint, se registró y entró en la escalera. La carpeta de prueba se borró.
- No se ha jugado ninguna partida de Claude desde este Mac.
- **DeepSeek, puerta 1 (26 oct, 19:51–20:11 UTC):** F1 por la vía oficial. El programa oficial funciona de punta a punta con nuestro manual. DeepSeek fue despedido en el mes 24 sin salir del nivel 1 (nota 18,8), el mismo fallo que las partidas malas de Haiku. Coste exacto: 0,185 USD (16 millones de tokens de entrada, 374 llamadas, 20 minutos); quedan 49,81 USD. Una partida completa costaría unos 0,4–0,8 USD, así que la clave da para 45–90 partidas después de la reserva.

## Lo que falló o quedó a medias

- **No hay canal directo con la sesión de la nube** desde este chat: no aparece entre las sesiones a las que se puede escribir. Además, ya bloqueó una petición de otro chat esta tarde. Las instrucciones van en mensajes que Alejandro pega en esa sesión (dos mensajes el 26 oct, ~19:05 y ~19:45 UTC).
- **PR #7 (`alejandro/laboratorio-adaptativo`, de Codex)** rediseña lo mismo con otra filosofía (más guardas), está a medias y toca los mismos archivos. Recomendación: no juntarla; aprovechar sus ideas útiles (no reutilizar un `score_report` viejo, comprobar credenciales sin mostrarlas) en el código de DeepSeek de esta rama.
- **Bots en nivel 6:** el informe de los bots de energía dice que algunos llegaron a "nivel 40–60" con Q de hasta 76. Ninguna partida con IA ha pasado del nivel 5, y esos datos no están en el repo. Se ha pedido a la nube que lo compruebe.
- **Código de DeepSeek** (`careerlab/target.py`): hecho, con 31 pruebas. Pendiente de decidir: el programa oficial se monta en chino cuando no hay nadie delante (como probablemente en la evaluación oficial). Las instrucciones del juego y los manuales van en inglés.

## Relevo

1. **Hecho:** el sistema de la tabla de arriba, en la rama `alejandro/carrera-rapida` (PR #8), con pruebas y documentación. ESTADO.md: T5 hecha (clave recibida), T6 replanteada (puertas de DeepSeek) y T14 nueva (carrera rápida), más dos decisiones en la sección 5.
2. **Datos:** calibración en `lab/protocol/fastloop-v2.md`; comprobación sobre una copia del registro e17b598 (en la carpeta temporal del chat, no versionada).
3. **A medias:** nada interrumpido. La nube corre la carrera rápida desde las 19:39. DeepSeek: sólo la puerta 1 jugada.
4. **Siguiente paso:** la nube corre la carrera rápida (estado en `lab/reports/carrera-rapida.md`; registro del driver en la nube, `~/careerlab-data/huawei/fastloop/driver.log`). DeepSeek, por decisión de Alejandro (26 oct, 20:18 UTC), sólo en las partidas previstas antes de cada corte. **Antes del corte 1 (27 oct, por la tarde UK):** si el campeón de `lab/reports/carrera-rapida.md` ya no es F1, jugar 2 partidas suyas con DeepSeek desde el Mac de Alejandro: `export UV_PROJECT_ENVIRONMENT=$HOME/venvs/huawei-fast CAREERLAB_ORIGIN=deepseek CAREERLAB_RUNNER_DIR=<repo>/local-runs/official-runner`; `uv run python -m careerlab.target register <carpeta del manual>`; `uv run python -m careerlab.target play --policy <nombre> --dry-run` y, si sale bien, `--spend --games 2`; después `uv run careerlab export` (escribe `lab/registry-origins/deepseek/`), commit y push.
5. **Líneas de ESTADO.md:** T5, T6 y T14 actualizadas en esta rama.
