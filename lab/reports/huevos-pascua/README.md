# Huevos de Pascua y atajos de ascenso

**Conclusión en una frase:** en el juego de desarrollo no hay ninguna combinación, personaje ni entrada oculta que permita saltarse un nivel o ascender fuera de la evaluación semestral; lo único nuevo es una mecánica sin documentar (la fase trimestral corta algunas historias y su título vuelve a salir) que vale __REPLAY__ en el simulador.

Línea corta de investigación del 28 oct 2026 (rama `claude/hidden-combos-easter-eggs-eb0edx`). Pregunta: *¿existen combinaciones ocultas o huevos de Pascua que permitan saltarse niveles de ascenso, por ejemplo interactuando con personajes clave?* (en Discord se dijo que sí).

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
| 8 | Entradas raras a las herramientas | `take_action` rechaza 0, negativos, fuera de rango, decimales y argumentos extra; el estado no se mueve. `observe` sólo tiene los campos conocidos (más `available_choice_count`) | `probe_interface.py` |
| 9 | Ramas nunca jugadas | El bot explorador jugó __COVER__ de las 212 respuestas con menos de 30 casos (las 20 «nunca elegidas» incluidas): todas tienen efectos corrientes y negativos, ninguna toca el nivel | lote `e01-explore`, __N__ partidas |
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
- **Lo que no se puede descartar desde aquí:** la evaluación oficial usa la configuración de los organizadores y puede tener otros eventos (lo dice `failure-and-ending.rst`). Lo que se diga en Discord sobre ese conjunto no se puede comprobar en local. El manual del juego dice que lo no publicado se infiere de «correos, actas de reuniones y comentarios del jefe», y el primer documento es de tipo *initialization*; en 13.333 partidas no ha salido ningún otro documento.

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

__RELEVO__
