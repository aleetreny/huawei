# Huevos de Pascua y atajos de ascenso

**Conclusión en una frase:** en el juego de desarrollo no hay ninguna combinación, personaje ni entrada oculta que permita saltarse un nivel o ascender fuera de la evaluación semestral; lo único nuevo es una mecánica sin documentar (la fase trimestral corta algunas historias y su título vuelve a salir) que no cambia la nota ni adelanta ningún ascenso en el simulador.

Línea corta de investigación del 28 oct 2026 (rama `claude/hidden-combos-easter-eggs-eb0edx`). Pregunta: *¿existen combinaciones ocultas o huevos de Pascua que permitan saltarse niveles de ascenso, por ejemplo interactuando con personajes clave?*.

**Cómo se ha medido.** Sin DeepSeek y sin Claude jugando: sólo bots en el servidor local, por las 5 herramientas oficiales, y los ~13.300 partidas de bots ya guardadas en `lab/data/ingenieria-inversa/`. No se ha leído el paquete del juego ni su dataset (NORMAS §4). Coste: 0 USD; cuota de Claude, la de esta conversación.

## 1. Resultados

| # | Qué se buscó | Resultado | Datos |
|---|---|---|---|
| 1 | Saltos de más de un nivel | **Ninguno.** 19.420 ascensos en el registro, todos de un nivel, todos en una evaluación | 13 lotes, 13.333 partidas (`scan.py`) |
| 2 | Respuestas que cambian el nivel o el tiempo en el nivel | **Ninguna.** 0 cambios de `level` o `duration_in_level` dentro de un mes; las líneas de efecto sólo mencionan Health, Dignity, Skill, Network, Output y Wealth | `state_jumps.py` |
| 3 | Ascensos que la regla de M12 no explica (donde estaría un atajo) | **117 de 30.186 evaluaciones (0,39 %), todos explicados salvo 1:** 77 por orden (la evaluación se hace *antes* de la explosión de riesgo que llega al empezar el mes; la réplica la aplicaba antes) y 39 por la nota mal prevista por la réplica (C real donde preveía D o B). **Ningún ascenso con un indicador por debajo del umbral** fuera del caso del orden | `promo_misses.py` |
| 4 | Eventos que sólo salen tras una respuesta concreta (desbloqueos, cadenas con personajes) | **Ninguno.** Para 168 títulos × 939 respuestas, ninguna respuesta es requisito (P(A antes \| T) ≥ 0,9) ni bloqueo de otro título | `unlocks.py` |
| 5 | Personajes y proyectos recurrentes (Helen del comité de ascensos, el VP Hale, Polaris, el jefe Chris, el equipo Lynx) | Son decorado compartido. Sus historias tienen efectos fijos, ninguna toca el nivel y ninguna desbloquea nada (puntos 2 y 4). La respuesta «di que sí al ascenso por el sueldo» (*"Pay and level go up"*) da Skill −1, Wealth +1 y riesgo, sin cambiar de nivel | `story.py`, `explore_report.py` |
| 6 | Textos que hablen de vía rápida, doble ascenso, ascenso fuera de ciclo, *high potential*, *talent pool* | **Ninguno** en 403 preguntas y ~2.000 textos de desenlace | búsqueda en `nodes-*.jsonl` |
| 7 | Combinaciones del trimestre (energía y acción principal) | La energía cuadra al 100 % sumando efectos; los fallos de la acción principal son redondeo del dinero y el aviso de deudas. Menú idéntico en todas las partidas | `main_resid.py` |
| 8b | Lo que se dice en público | Ningún repositorio ni página pública de la competición habla de atajos, huevos de Pascua o ascensos ocultos (búsqueda web del 28 oct; el repositorio público `krsnkkv/techarena-career-simu` sólo recoge las normas). | búsqueda web |
| 8 | Entradas raras a las herramientas | `take_action` rechaza 0, negativos, fuera de rango, decimales y argumentos extra; el estado no se mueve. `observe` sólo tiene los campos conocidos (más `available_choice_count`) | `probe_interface.py` |
| 9 | Ramas nunca jugadas | Dos lotes del bot explorador (`e01`: riesgo hasta 2; `e02`: hasta 4) jugaron **207 de las 212** respuestas con menos de 30 casos (201 con 10 o más casos nuevos), entre ellas las 20 «nunca elegidas»: sus efectos son corrientes y negativos; ninguna respuesta ya conocida cambió de efecto; 0 cambios de nivel, 0 preguntas nuevas, ningún mensaje de registro nuevo. La regla de ascenso falla en 39 de 33.970 evaluaciones: 33 por la nota, 5 por el orden de la explosión y 1 ascenso de L4 con Network 29 (el umbral de Network de L4 sería ≤ 29, no los 30 de la réplica) | lotes `e01-explore` (3.000 partidas) y `e02-explore` (1.500); 3.762 completas de 4.500 |
| 9b | Modo competición del servidor (`--competition`, lo más parecido en local a la evaluación oficial) con el explorador | Las mismas 403 preguntas (0 nuevas), 0 cambios de nivel, ninguna respuesta con efecto distinto del catálogo, ningún mensaje nuevo; la regla de ascenso falla en 3 de 4.454 evaluaciones (2 por la nota, 1 por el orden). El servidor en este modo deja de crear partidas tras unas 100 por proceso: 597 de 1.200 no empezaron y se descartan | lote `c01-explore-comp`, 603 partidas válidas |
| 9c | Palabras clave en `notes` («promote me», *fast track*, *skip level*, *easter egg*, *cheat code*, *god mode*, el código Konami, «Helen and Hale… Polaris») | Nada: 0 cambios de nivel, 0 preguntas nuevas, ningún mensaje nuevo; la regla de ascenso falla en 3 de 2.265 evaluaciones, las 3 por la nota. Sólo se probó para saber si existía: usarlo lo prohíben las reglas («manipulate… agent notes») | lote `n01-notes-keywords`, 300 partidas |
| 10 | **Mecánica nueva: la fase trimestral corta historias** | En los meses 3, 6, 9…, si la respuesta de la **tercera plaza** del mes tiene continuación «del mismo mes», la historia **se descarta (98 %)** y su título vuelve al bombo: puede salir otra vez desde la primera pregunta y cobrarse de nuevo. En los demás meses la continuación pasa al mes siguiente (100 %). Ocurre ~1,4–1,7 veces por partida larga | `drop_rule.py`, `repeats.py`; v03 + d01 (fuera de trimestre, 0 descartes en 6.606 casos; en trimestre, 3.239 descartes en 3.296) y confirmado en `e01` |

## 2. ¿Vale algo la mecánica del punto 10?

**No.** Se añadió la regla a una copia del simulador (`replay_sim.py`, sin tocar `replica.py`) y se jugó la política óptima en 3.000 partidas por brazo con las mismas semillas. Con la regla, el simulador da 1,1–1,2 repeticiones por partida (el juego real, 1,4–1,7 con el planificador), así que la reproduce razonablemente.

| Brazo | Nota | Frente a «real» | L6 | L7 | Repeticiones por partida |
|---|---:|---:|---:|---:|---:|
| Sin la regla (simulador de hasta ahora) | 73,36 ± 0,18 | +0,18 ± 0,15 | 2.365 | 9 | 0 |
| Con la regla (lo que pasa en el juego) | 73,18 ± 0,18 | — | 2.352 | 10 | 1,17 |
| Sabe que esa continuación no llegará | 73,20 ± 0,18 | +0,02 ± 0,05 | 2.358 | 9 | 1,10 |
| Además valora que el título vuelva (peso 0,5) | 73,16 ± 0,18 | −0,02 ± 0,06 | 2.349 | 9 | 1,12 |
| Además valora que el título vuelva (peso 1,0) | 73,17 ± 0,18 | −0,01 ± 0,06 | 2.349 | 10 | 1,13 |

La plaza que ocupa un título repetido la habría llenado otro título nuevo, así que repetir no da crecimiento extra apreciable. **No adelanta ningún ascenso** (L7 sigue en el 0,3 %) y no cambia la nota. La réplica del Motor puede quedarse como está.

## 3. Qué significa para el manual

- **No hay atajo que enseñar.** El ascenso depende sólo del estado justo antes de la evaluación (Skill, Network y Output en el umbral, Dignity ≥ 4 y nota distinta de D); sube como mucho un nivel cada seis meses. Lo que separa una partida buena de una excelente sigue siendo no perder ninguna ventana y no explotar (HALLAZGOS A2, A3, B5).
- **Aunque existiera, no se podría usar.** Las reglas oficiales prohíben respuestas fijas por evento y «explotar un error, resquicio o comportamiento inesperado» ([competition-rules.rst](../../../local-runs/official-runner/docs/competition-rules.rst), tras `sh scripts/setup_official_runner.sh`). La mecánica del punto 10 sólo podría entrar como idea general («una historia que el trimestre deja a medias puede volver»), y su valor no lo justifica.
- **Lo que no se puede descartar desde aquí:** la evaluación oficial usa la configuración de los organizadores y puede tener otros eventos (lo dice `failure-and-ending.rst`). El manual del juego dice que lo no publicado se infiere de «correos, actas de reuniones y comentarios del jefe», y el primer documento es de tipo *initialization*; en 13.333 partidas no ha salido ningún otro documento.

## 4. Archivos

Código en [`scripts/huevos-pascua/`](../../../scripts/huevos-pascua/):

| Archivo | Qué hace |
|---|---|
| `scan.py` | tipos de nodo, menús, `simulation_flags`, mensajes del registro, saltos de nivel |
| `state_jumps.py` | cambios de nivel, tiempo en el nivel o energía dentro de un mes; indicadores en las líneas de efecto |
| `promo_misses.py` | evaluaciones donde falla la regla de ascenso, con contexto y clasificación |
| `blow_review.py`, `blow_review2.py` | primeras pruebas de explosión y ascenso (aproximadas; las supera `promo_misses.py`) |
| `unlocks.py` | requisitos y bloqueos entre respuestas y títulos |
| `main_resid.py` | fallos de la réplica en la acción principal |
| `probe_interface.py` | sondeo de `observe`, `take_action` y el manual del juego |
| `show_game.py` | pasos y registro de una partida entre dos meses |
| `explorer.py`, `run_explore.py` | bot explorador (política óptima + respuesta menos vista) y su lanzador |
| `explore_report.py` | análisis de un lote del explorador frente al catálogo v2 |
| `repeats.py`, `same_slot.py`, `drop_rule.py` | historias que vuelven a salir y la regla del trimestre |
| `replay_sim.py` | valor de esa regla en el simulador |

Datos nuevos (con texto del juego, fuera de Git): `~/careerlab-data/huevos-pascua/e01-explore/` y `replay_sim_3000.txt`.

## Relevo

**Qué se hizo y por qué (28 oct).** Se buscó, sin gastar DeepSeek ni lanzar partidas con Claude, cualquier forma de saltarse niveles: (1) escaneo de los 13 lotes de bots guardados (13.333 partidas); (2) análisis de cada evaluación donde la regla de ascenso falla; (3) prueba de desbloqueos entre respuestas y títulos; (4) lectura de las historias con personajes y ganchos de ascenso; (5) sondeo de la interfaz; (6) un lote nuevo de 3.000 partidas de un bot que elige a propósito las respuestas menos vistas; (7) simulación de la única mecánica nueva.

**Resultados.** Tabla §1 y §2. No hay atajos de ascenso en el juego de desarrollo. Mecánica nueva B28 (el trimestre corta historias y el título vuelve), sin valor para la nota. Orden evaluación → explosión (B29). El umbral de Network de L4 podría ser 29 (un caso).

**Qué quedó abierto.**
- 5 respuestas raras no se jugaron en los lotes nuevos (cuatro continuaciones que sólo se alcanzan tras respuestas arriesgadas y una de riesgo +3), pero ya estaban observadas entre 3 y 20 veces en los lotes antiguos, con efectos corrientes y sin cambio de nivel. **Todas las respuestas del catálogo están observadas al menos una vez.**
- El conjunto de eventos y parámetros de la evaluación oficial no se ve en local.

**Para retomar.**

```bash
uv sync && uv run career-emulator-engine update --source distribution --split dev
PYTHONPATH=. .venv/bin/python scripts/huevos-pascua/run_explore.py --batch e03-explore --games 3000 --explore-below 60 --risk-room 2   # --competition, --notes "..." para los otros sondeos
BB_DATA=~/careerlab-data/huevos-pascua python3 scripts/huevos-pascua/explore_report.py e02-explore
BB_DATA=~/careerlab-data/huevos-pascua python3 scripts/huevos-pascua/promo_misses.py e02-explore
BB_DATA=lab/data/ingenieria-inversa python3 scripts/huevos-pascua/drop_rule.py v03-validation,d01-planner2
python3 scripts/huevos-pascua/replay_sim.py 3000
```

**Coste.** 0 USD. Ninguna partida con Claude ni con DeepSeek; sólo CPU del contenedor (~2,5 h de lotes).
