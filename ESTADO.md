# ESTADO del proyecto: léelo primero

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*.
Última actualización: **26 oct 2026, 21:38 UTC**, sesión de la nube (organizadora).

Este documento es el punto de partida de cualquier persona o agente: dónde vamos, qué falta, qué está decidido y cómo trabajamos. Si un chat nuevo sólo puede leer un archivo, que sea este.

## 1. El reto en cinco líneas

- Un juego de texto: una IA vive 48 meses de carrera en una empresa. Cada mes reparte energía y elige opciones ante eventos.
- Se pierde por dos evaluaciones semestrales malas (despido), por una "crisis de confianza" o por agotamiento. Al final hay una nota de 0 a 100.
- **No jugamos nosotros.** Entregamos un manual (*Skills*, texto en inglés) que lee **DeepSeek** (`deepseek-v4-flash`) dentro del programa oficial JiuwenSwarm.
- Nota de cada versión: 80 % la media de 3 partidas, 10 % la calidad de los documentos de diseño y 10 % el ahorro de tokens. Cuenta la mejor de nuestras versiones.
- Los 10 mejores equipos pasan a un jurado con vídeo, que vale el 30 % de la nota final.

## 2. Dónde vamos

**El laboratorio funciona.** Juega partidas por la vía oficial, muchas a la vez, se recupera de fallos y guarda todo. Las instrucciones están en [lab/README.md](lab/README.md).

**Cambio de sistema (26 oct, noche): carrera rápida.** Decisión de Alejandro: ir más rápido. Hay un campeón y los manuales nuevos suben una escalera de 2, 4, 8 y 12 partidas. Tras cada escalón se calcula la probabilidad de que el aspirante sea mejor que el campeón: si es baja, el manual se descarta y no juega más; si con 8 o 12 partidas es alta, pasa a ser campeón. Un diseñador automático (Opus) lee las peores partidas del campeón y escribe variantes, y cuando nos atascamos escribe ideas valientes. Explicación sencilla: [lab/fastloop/README.md](lab/fastloop/README.md). Estado en directo: [lab/reports/carrera-rapida.md](lab/reports/carrera-rapida.md) (tarea T14).

Llevamos 150 partidas con IA (modelos de Claude haciendo de DeepSeek) y 550 con bots. Además hay 753.580 partidas en un juego de juguete que sirven para comprobar el método de elección.

**Desde las 19:39 UTC juega la carrera rápida (fastloop-v2, T14)**, por decisión de Alejandro:
- Campeón inicial: F1 equilibrio. Aspirantes: f1 línea de estado, f3 línea de estado, f3 ligera, f3 recombinada, observed-growth-v3 (Matteo), f1 señal de riesgo y f1 núcleo.
- 8 huecos y tope 0,85. Ritmo semanal adelantado: 45 % el 28 oct, 75 % el 31 oct y 90 % al final.
- Diseñadores automáticos con Opus.
- La tanda en curso se cortó: sus 6 partidas quedaron interrumpidas, sin nota, y la cola anterior se canceló.
- Estado en directo: [lab/reports/carrera-rapida.md](lab/reports/carrera-rapida.md). Lecciones para los diseñadores: [lab/fastloop/lessons.md](lab/fastloop/lessons.md).

**Segunda hora de la carrera rápida (21:38 UTC):**
- **Campeón nuevo desde las 21:29: `targeted-1026-201334`**, escrito por un diseñador automático. Es f3 recombinada más una regla: hasta el primer ascenso, no ceder Output ni Network en las historias. Lleva 10 de 12 terminadas, nota media 53,9 y P(mejor que f3 recombinada) 0,61.
- No funcionaron:
  - cambiar "pasar desapercibido" por acciones de resultados cuando el riesgo escala (4 de 8);
  - proteger Skill, Network y Output en todas las historias (2 de 4), más amplio que la regla del campeón;
  - observed-growth-v6 (5 de 8).
- En juego: una variante (3 de 4, 52,9) y las primeras ideas "ambiciosa" y "valiente".
- Cuota: la ventana de 5 horas se renovó a las 21:00 y va por el 9 %. La semana va por el 14 %, con un 16 % permitido a esta hora.

**Primera hora de la carrera rápida (20:40 UTC):**
- **Campeón nuevo desde las 20:03: f3 recombinada**, con 10 de 12 terminadas, nota media 54,6 y P(mejor que F1) 0,74.
- Se quedaron a las puertas f3 ligera (11 de 12, 55,5) y observed-growth-v3 (10 de 12, 55,4). Les faltó poco: 0,55 y 0,59 frente al 0,60 exigido.
- **Corrección: el formato "línea de estado" no se confirma.** f1 línea de estado bajó a 5 de 8 terminadas (52,7) y su prueba de transferencia, f3 línea de estado, quedó en 3 de 8 (39,5). El 4 de 4 inicial fue suerte, igual que el 71,4 de la v3 de Matteo en su ordenador.
- Descartadas: f1 núcleo (1 de 4) y f1 señal de riesgo (1 de 4).
- Los diseñadores automáticos ya han metido sus primeros manuales: `stretch-1026-200334` y `targeted-1026-201334`.

**El nivel 6 es alcanzable (comprobado en los datos de los bots, T10):** 4 de 400 bots llegaron a L6 y terminaron con Q de 67 a 76. Los cuatro ascendieron en cada una de las tres primeras evaluaciones, aunque la primera fue una C, y acabaron con Skill al máximo. Ninguna partida con IA ha pasado de L5.

**Última clasificación del sistema anterior** (prereg-v1; Claude Haiku; decisión del 26 oct a las 19:31 UTC, registro #157):

| Manual | Nota estimada (partidas) | Estado |
|---|---:|---|
| **f1 línea de estado** (F1 con una línea de estado fija) | **56,1 (4)** | **nuevo líder ("promover", P(mejor) 0,45)**: 4 de 4 terminadas (57, 66, 70, 65) |
| F1 equilibrio | 52,8 (12) | sigue en juego |
| f3 recombinada · f3 ligera | 51,2 (7) · 51,1 (5) | siguen en juego |
| F3 · hija destilada "defuse antes de la evaluación" | 50,1 · 50,0 | siguen en juego |
| f2 convertir tras evaluación · f1 revisión de riesgo | 48,4 · 46,9 | siguen en juego |
| F7 tres skills y sus hijas, l1-review-clock, F8, value-conversion, observed-growth | 42–45 | siguen en juego, por debajo |

**(Corregido a las 20:40: no se confirmó con más partidas.)** **Hallazgo de la tarde: cómo se escribe el manual importa.** `f1 línea de estado` usa las mismas reglas que sus dos hermanas, pero obliga a rellenar antes de cada decisión una línea fija `Act | Risk | Weakest` y a servir la primera necesidad. Ella terminó 4 de 4 partidas; sus hermanas, escritas en prosa, 1 de 4 cada una. Con 4 partidas es una pista, no una prueba. Por eso se juegan más partidas de ella, y la prueba de transferencia `f3 línea de estado` (las reglas exactas de f3 recombinada en el mismo formato) dirá si el formato ayuda también a otra familia. Si se confirma, es justo lo que necesita un modelo más débil como DeepSeek.

El observed-growth-v3 de Matteo sacó en la carrera 61, 19, 52 y 64 (3 de 4 terminadas): no repite el 71,4 de su ordenador.

**Techo de Opus (T13), terminado:** 6 partidas de Opus al máximo esfuerzo con todo lo que sabemos en general. Nota media Y = 54,2 (Q 56,2): 5 de 6 terminadas, una despedida en el mes 24. Según los umbrales escritos antes de jugar, estamos **"cerca del techo"**. Hay que dedicar el esfuerzo a la **fiabilidad** (evitar el despido del mes 24) y al **ahorro de tokens**, no a buscar más estrategia. Ni Opus mueve el nivel ni el dinero: pierde 16,2 puntos en nivel y 12,8 en dinero, igual que todos los demás. Hay incertidumbre: el intervalo va de 41,6 a 66,7 ([informe](lab/reports/opus-ceiling/README.md)).

**Problema A (¿Haiku y Opus eligen lo mismo?):** sólo en parte. Los dos ponen F1 arriba, pero Opus con memoria corta juega mal los manuales de la familia F3: terminó 2 de 6 partidas, con unos 38–39 de nota, frente a 61–66 con F1 y P0. Haiku los pone en la zona media. Por eso la clasificación de Haiku no se puede trasladar tal cual a un modelo más fuerte, y hará falta DeepSeek (T6).

**Lo que hemos aprendido:**
- Hay dos formas de perder: dos evaluaciones malas seguidas (despido en el mes 24) o una crisis de confianza tras acumular riesgo. Todas las partidas empiezan con una C.
- **Sabemos sobrevivir, pero no crecer.** En las 48 partidas terminadas faltan unos 40 puntos: 16 se pierden en nivel (ascensos) y 13 en dinero. Ningún manual busca ascender y ganar dinero cuando las cosas van bien.
- Qué modelo juega importa:
  - Haiku termina 30 de 59 partidas y Sonnet 10 de 26.
  - Opus con memoria corta termina 5 de 6. Opus jugando casi sin manual saca entre 62 y 67, así que sirve de "maestro".
- Los bots que eligen al azar mueren hacia el mes 6. De las 73.858 partidas de Matteo, ninguna llegó al final.

**Novedades de la tarde (26 oct, nube; provisional, con 3–4 partidas por manual, antes de la decisión de la tanda 1):**
- Media de la nota (Q) con Haiku: f3 recombinada 60,6 (4 de 4 terminadas), F3 55,3, f3 ligera 55,1, hija destilada "defuse antes de la evaluación" 51,0, F8 crecer 49,3, o1 hueco de ascenso 44,0, o2 a tope 36,2, hija destilada completa 31,7.
- **Cómo se pierde en el mes 24:** los 14 despidos vinieron tras cuatro evaluaciones malas seguidas (C C D D, C C C C o C C D C). Toda partida con al menos una B en sus cuatro primeras evaluaciones pasó del mes 24. La palanca es cortar la racha de C pronto, y eso va de **ascender**, no de la nota: ninguna partida sacó una B mientras seguía en el nivel 1 tras su primera evaluación. Quien asciende en la primera evaluación saca de media 57; quien no ha ascendido en la segunda, 22 ([diagnóstico](lab/reports/cloud-run-diagnostics/block3-generation.md)).
- La mayoría de las derrotas siguen siendo el despido en el mes 24. La hija destilada completa, que quita el plan de recuperación tras una evaluación mala, cae ahí 2 de 3 veces.
- Bots de energía (T10, 400 partidas, sin cuota): la salud es el primer límite. Sin un punto de recuperación cada trimestre, todos los bots se agotan. Recuperar sólo cuando la salud ya está baja llega tarde. La mejor mezcla es "desactivar riesgo + salud". Ninguna mezcla de energía evita la C de la primera evaluación.

**Lo que aún no sabemos:**
- Cómo juega DeepSeek con nuestros manuales. Hace falta la clave de la API (tarea T5).

**Cuota de Claude (cuenta Max):**
- Se renovó el 26 oct a las 16:00 UTC. A las 16:16 la ventana de 5 horas iba por el 7 % y la semana por el 1 %.
- Antes del reinicio, a petición de Alejandro, se gastó lo que quedaba de la ventana anterior (tope 0,97 hasta las 16:00, con 10 partidas a la vez).
- El laboratorio se frena solo: gasta como máximo un 12–13 % de la semana al día y deja un 10 % para los chats del equipo.

## 3. Fechas (hora UK)

| Fecha | Qué hay |
|---|---|
| 27 oct, 24:00 | Corte 1. La primera entrega final necesita el vídeo `presentation.mp4`, los documentos de diseño y las Skills. |
| 30 oct, 24:00 | Corte 2 |
| 1 nov, 24:00 | Corte 3, el último. El freno de cuota del laboratorio está calculado hasta esta fecha. |

## 4. Tareas pendientes

Cada uno actualiza **su propia línea** al empezar y al acabar. Las tareas nuevas las añade el organizador.

Revisión informativa solicitada por Alejandro: **Codex — `alejandro/explicacion-repo` — terminada, pendiente de integrar mediante PR**. Explicación de estructura, tareas y resultados con Relevo en [este informe](research/careerlab/explicacion-repo-2026-10-26.md); 230 tests OK, sin partidas ni cambios del laboratorio. No añade una tarea de desarrollo a T1–T13.

Línea de investigación solicitada por Alejandro: **Codex — `alejandro/investigacion-decisiones` — primera exploración y estructura continua preparadas; PR #3 para integrar**. [Informe e insights](lab/reports/decision-research/cycles/002/interpretation.md), [continuar en este chat](research/careerlab/decision-research/CONTINUAR.md) y [Relevo](lab/reports/decision-research/README.md). Snapshot `9b8fbe9`: 204 terminales Claude, 99 trazas locales y 105 no localizadas aquí; regresión de estados del Haiku principal en 53 partidas, validada reservando políticas/familias. El estancamiento es una señal de riesgo, no un efecto causal: al segundo corte completan 2/14 aún L1 frente a 26/38 promovidas. No se ajustan modelos de comportamientos por sólo 20/17 prefijos completos. Ciclos con hashes/linaje, insights y cola de hipótesis; siguiente paso: recuperar trazas en nube. Sin nuevas partidas ni cambios de manuales/protocolo. No reasigna T1–T13.
Diagnóstico solicitado por Alejandro: **Codex — `alejandro/diagnostico-estrategias` — terminado, [PR #4](https://github.com/aleetreny/huawei/pull/4) pendiente de integrar**. [Diagnóstico y Relevo](research/careerlab/diagnostico-2026-10-26/README.md), con cálculos reproducibles, sensibilidad del ranking, fallo de robustez reproducido y experimentos priorizados; 230 tests OK. Sin partidas ni cambios de la carrera; no añade tareas a T1–T13.

Sección de ideas solicitada por Alejandro: **Codex — `alejandro/ideas-por-probar` — preparada para PR nueva**. [Índice](research/ideas/README.md) y [exploración aleatoria instrumentada](research/ideas/exploracion-aleatoria.md): revisión de la corrida de Matteo (73.858 partidas, resumen agregado sin decisiones individuales publicadas), diseño de logs por decisión y límites de inferencia/conformidad. No se han lanzado partidas ni contactado organizadores. Relevo y siguiente paso de auditoría en la sección; no reasigna T1–T13.

| # | Tarea | Quién | Estado | Dónde queda el resultado |
|---|---|---|---|---|
| T1 | Carrera continua de manuales (jugar, decidir, generar hijas) | nube | **sustituida por T14** el 26 oct a las 19:39 UTC. Su última decisión fue la #157 (líder f1 línea de estado, 56,1) | `lab/reports/cloud-run-status.md` (histórico y relevo de la nube) |
| T2 | Destilar las partidas ganadoras de Opus en hijas de F3, sólo reglas generales | nube | hecha: reglas en `distilled-rules.md`; 2 hijas registradas y jugando (resultados provisionales en la sección 2) | `lab/reports/teacher-digests/distilled-rules.md`, `lab/policies-src/f3-feedback-reactive/` |
| T3 | Familia nueva "sobrevivir y crecer" (buscar ascensos y dinero cuando todo va bien) | nube | hecha: F8 (`f8-secure-growth-v1`) registrada y jugando | `lab/policies-src/f8-secure-growth/` |
| T4 | Ideas de fuera: manuales nuevos escritos sin mirar los nuestros, con otro modelo u otra cuota | nube (agente que no ve nuestros manuales) y Matteo | nube: o1 hueco de ascenso y o2 a tope jugando; o3 "padrinos" en espera (se parece a F4 + F5). Matteo: `value-conversion-v1` juntada con `main` y en cola (4 partidas); `observed-growth-v1` (síntesis tras leer F3/F8, no ciega) lista para registrar, lint OK; piloto local aislado con Haiku: 64,78, L5, 48 meses; 4 partidas Haiku más (origen `matteo`, fuera de las decisiones): Q media 40,85, 1 de 4 terminada (70,94, L5 en el mes 42), 3 despedidas en el mes 24; `observed-growth-v2` (rama `matteo/observed-growth-v2`, 4 partidas Haiku, mismo actor): Q media 43,18, 2 de 4 terminadas, 0 despidos y 2 crisis de confianza (casi no usa Defuse); `observed-growth-v3` (rama `matteo/observed-growth-v3`, limpieza de riesgo restaurada, 4 partidas Haiku, mismo actor): Q media 71,43, 4 de 4 terminadas en L5, 0 despidos y 0 crisis; **corrección:** 4 partidas nuevas de v3 dan 1 de 4 y Q media 30,65, así que v3 con 8 partidas queda en Q media 51,04 y 5 de 8 terminadas (el primer lote tuvo suerte); `observed-growth-v4`: Q media 32,76, 1 de 4; `observed-growth-v5` (v3 + preferencia por dinero, rama `matteo/observed-growth-v5`): Q media 30,32, 1 de 4; ninguna se propone; estudio de ascensos (rama `matteo/promotion-study`, PR #10, bots sin cuota): la evaluación se aplica al empezar el mes, antes de sus eventos y su reparto, y asciende quien está en el techo visible de su nivel en ese momento (bots 55 % frente a 3,5 %; Haiku 9/13 frente a 0/11); `observed-growth-v6` (rama `matteo/observed-growth-v6`, con esas reglas): 8 partidas Haiku, 6 terminadas (2 reanudadas tras el límite de la cuenta de Matteo), 2 perdidas en L1; Q media 50,08, no se distingue de v3; **`observed-growth-v7`** (rama `matteo/observed-growth-v7`, reglas de v6 con línea de estado fija, 455 palabras): 8 partidas Haiku con el mismo actor, **7 terminadas, Q media 61,27, 8 de 8 fuera de L1 en el primer año, 6 en L5**; propuesta para la carrera rápida | `lab/policies-src/o*-*/`, `lab/policies-src/matteo-value-conversion/`, `lab/policies-src/matteo-feedback-growth/`, informes `lab/reports/matteo-t4-value-conversion.md`, `lab/reports/matteo-observed-growth.md`, `lab/reports/matteo-observed-growth-haiku-4.md`, `lab/reports/matteo-observed-growth-v2.md`, `lab/reports/matteo-observed-growth-v3.md`, `lab/reports/matteo-observed-growth-v5.md`, `lab/reports/matteo-promotion-study.md`, `lab/reports/matteo-observed-growth-v6.md` y `lab/reports/matteo-observed-growth-v7.md`; datos en `lab/registry-origins/matteo/` |
| T5 | Envío preliminar y clave de la API | Alejandro | **hecha**: clave recibida el 26 oct (OpenRouter, 50 USD, 0 gastados a las 19:05 UTC). Está sólo en el `.env` del programa oficial en el Mac de Alejandro, fuera de Git | — |
| T6 | DeepSeek sólo en las puertas de [fastloop-v2](lab/protocol/fastloop-v2.md): 1 partida del campeón para comprobar el programa oficial y el coste; 2 antes de cada corte si el campeón ha cambiado | Alejandro (su Mac, chat `alejandro/carrera-rapida`) | **puerta 1 hecha** (26 oct, 19:51–20:11 UTC): F1 con DeepSeek por la vía oficial. El programa oficial funciona de punta a punta con nuestro manual. Resultado: despedido en el mes 24, sin salir del nivel 1 (nota 18,8). Coste exacto 0,185 USD (16 millones de tokens de entrada en 24 meses); quedan 49,81 USD. Una partida es una anécdota. **Decisión de Alejandro (26 oct, 20:18 UTC): de momento sólo las partidas previstas antes de cada corte.** Próxima: el 27 oct por la tarde (UK), antes del corte 1, 2 partidas del campeón si ya no es F1. Las lanza Alejandro desde su Mac (comandos en [el informe](research/careerlab/carrera-rapida-2026-10-26.md), Relevo) | origen `deepseek`: `lab/registry-origins/deepseek/` |
| T7 | Vídeo `presentation.mp4` para el corte 1, en inglés, máximo 10 minutos y respondiendo a las 5 preguntas oficiales | equipo (personas) | pendiente | guion base en [jury-story.md](research/careerlab/jury-story.md) |
| T8 | Documentos de diseño del corte 1 (`skills_design.md`, `decision_report.md`) | nube (organizadora), revisa el equipo | **no empezar hasta el 27 oct** (decisión de Alejandro) | `cloud-lab-run`: `lab/submissions/r1-draft/design/` |
| T9 | Elegir el manual del corte 1 (el líder de la última decisión), empaquetar y validar con `careerlab package` | nube (organizadora) | espera a T7 y T8 | `lab/submissions/r1/` |
| T10 | Bots sin IA para estudiar el reparto de energía (no gasta cuota) | nube | hecha (400 partidas). Comprobado a las 19:41: 4 bots llegaron a L6 | `lab/reports/energy-bots/README.md`; detalle en `lab/fastloop/lessons.md` (Frontier) |
| T11 | Permitir que varios ordenadores jueguen a la vez sin pisarse los resultados | Leah | hecha y juntada con `main` (26 oct, 16:20; 230 tests OK). La nube ya usa el registro migrado | código en `careerlab/`; informe en [lab/reports/t11-multi-machine](lab/reports/t11-multi-machine/README.md) |
| T12 | Juntar `cloud-lab-run` y las ramas terminadas con `main` | nube (organizadora) | en marcha: tras cada tanda y cada resultado importante (1ª vez: 26 oct, 16:20) | `main` |
| T13 | Techo del juego: 4–6 partidas de Opus al máximo esfuerzo con todo lo que sabemos en general. Nada de resúmenes de eventos concretos. No es una entrega: mide cuánto margen queda | nube | **hecha** (26 oct, 17:55): Y media 54,2, 5 de 6 terminadas → "cerca del techo"; el esfuerzo pasa a fiabilidad y tokens | `lab/reports/opus-ceiling/README.md`; resúmenes en `lab/reports/teacher-digests/opus-ceiling/` |
| T14 | Carrera rápida (fastloop-v2): campeón y aspirantes, diseñadores automáticos, ideas valientes al atascarse. Sustituye a T1 | nube (organizadora), diseñada por el chat `alejandro/carrera-rapida` | en marcha desde las 19:39 UTC; campeón **targeted-1026-201334** (de un diseñador) desde las 21:29; antes, f3 recombinada (20:03) (nube) | `lab/reports/carrera-rapida.md`, `lab/fastloop/` (estado, historial, lecciones) |

## Relevo del organizador (26 oct, 16:20 UTC)

**La organizadora es la sesión de la nube "CareerLab continuous race in the cloud"** (rama `cloud-lab-run`). Juega las partidas, junta las ramas terminadas con `main` y mantiene este archivo. Para hablar con ella, abre esa sesión en claude.ai/code o en la app. Si se parase, su relevo completo (al final de `lab/reports/cloud-run-status.md`) trae un prompt para abrir otra sesión de nube que haga lo mismo. Nunca debe haber dos a la vez.

**Cómo nos coordinamos sin pisarnos**
- Cada persona o agente trabaja en su rama (`<persona>/<tarea>`) y sólo cambia **su línea** de la tabla de la sección 4. Al terminar, deja su relevo, hace push y pide que se junte (Pull Request o aviso aquí).
- La organizadora junta las ramas terminadas en `main` cada hora o tras cada tanda: primero trae `main`, pasa los tests y nunca fuerza el push a `main`. Si hay un conflicto en una línea ajena, se queda la versión de su dueño.
- Sólo la nube escribe `lab/registry/*.jsonl`. Otros ordenadores que jueguen exportan a `lab/registry-origins/<origen>/` (T11) y la organizadora lo importa.
- Las secciones 2, 4 (líneas de la nube) y este relevo los escribe la organizadora.
- Los commits van a nombre de una persona y **sin líneas `Co-Authored-By` de Claude** (decisión de Alejandro, sección 5).

**Hecho esta tarde (nube)**
- Carrera en marcha. Candidatos nuevos en juego: 2 hijas destiladas de F3 (T2), F8 (T3), o1 y o2 (T4) y value-conversion de Matteo (T4).
- Bots de energía terminados (T10). Techo de Opus en marcha (T13).
- Juntadas con `main`: `cloud-lab-run`, `leah/workspace` (T11) y `matteo-t4-growth` (T4).

**Siguiente:** la carrera rápida juega sola. La organizadora sigue la rutina de `scripts/fastloop/README.md` cada hora: juntar ramas, `ladder add` para los manuales del equipo, export, `ladder status --write`, commit y push, y lecciones tras cada campeón nuevo o cada 3 horas. Los documentos de entrega (T8 y T9) empiezan el 27 oct a primera hora (UK), con el campeón de ese momento.

## 5. Decisiones ya tomadas (no hace falta volver a discutirlas)

- **26 oct, Alejandro:** se permiten partidas con modelos de Claude como sustitutos de DeepSeek, y los bots no tienen límite.
- **26 oct, Alejandro:** no preguntamos en Discord; si las reglas no lo prohíben, lo hacemos. Riesgo conocido: la norma oficial dice *"the absence of an express prohibition is not permission"*. Si cambiamos de idea, hay un borrador del mensaje en [organiser-questions.md](research/organiser-questions.md) §0.
- **Dinero:** sólo los 50 USD de la clave. Cualquier otro gasto en APIs necesita un presupuesto confirmado por Alejandro.
- **Método:** las reglas estadísticas se fijaron antes de ver resultados ([prereg-v1.md](lab/protocol/prereg-v1.md)). No se editan; si hay que cambiarlas, se crea una versión nueva.
- **Quién juega:** la carrera la juega la nube. Desde T11, otro ordenador puede jugar con su propio origen (ver *Partidas* en la sección 6).
- **26 oct, Alejandro:** Claude no debe aparecer como contribuidor en GitHub. Los commits van a nombre de una persona y sin líneas `Co-Authored-By` de Claude. La nube hace los suyos a nombre de Alejandro.
- **26 oct, Alejandro:** la nube hace push a `main` como organizadora (tras pasar los tests).
- **26 oct (noche), Alejandro:** carrera rápida. [fastloop-v2](lab/protocol/fastloop-v2.md) sustituye las reglas de reparto y elección de prereg-v1 para la carrera de Haiku; prereg-v1 no se edita y sus datos se reutilizan. Se descartan pronto los manuales que no funcionan, las partidas van a los aspirantes con opciones, y cuando nos atascamos se prueban ideas valientes. El ritmo semanal de cuota se adelanta: hasta un 45 % de la semana el 28 oct, un 75 % el 31 oct y un 90 % el 2 nov.
- **26 oct (noche), Alejandro:** la clave de DeepSeek sólo se usa cuando sea seguro que aporta algo: las puertas de fastloop-v2, con el gasto exacto medido en cada partida y 15 USD de reserva para el último corte. Nunca para explorar. Confirmado el 26 oct a las 20:18 UTC, después de la primera partida (0,185 USD): no se amplía a comparar los mejores manuales con DeepSeek; sólo las partidas previstas antes de cada corte.

## 6. Reglas de trabajo

**Empezar un chat nuevo.** Basta con escribir: *"Lee ESTADO.md y haz la tarea T4"*. Un chat por tarea. Si un chat se alarga mucho, deja lo hecho por escrito y abre otro: los chats largos gastan más cuota en cada mensaje.

**Ramas**
- `main` contiene lo común y comprobado. Sólo el organizador escribe directamente en `main` (ahora, la sesión de la nube), para actualizar este archivo y juntar ramas terminadas.
- Cada tarea va en su propia rama:
  - Si la app de Claude abre el chat en una copia aparte del proyecto (*worktree*), crea la rama sola con el prefijo de cada persona: en la app de Alejandro, `alejandro/...` (cambiado el 26 oct). Matteo puede poner `matteo` en **Ajustes → Claude Code → Branch prefix**. Usa esa rama tal cual.
  - Si no, créala con el nombre `<persona>/<tarea>`; por ejemplo `matteo/ideas-fuera` o `alejandro/video-r1`.
- **El chat organizador es la excepción:** se abre directamente en la carpeta del proyecto, en `main`, sin copia aparte, porque es quien junta las ramas y edita este archivo.
- Ramas que existen ahora:

  | Rama | Para qué | Estado |
  |---|---|---|
  | `main` | lo común y comprobado | — |
  | `cloud-lab-run` | la carrera de la nube | activa; el organizador la junta con `main` cada día |
  | `Matteo` | trabajo antiguo de Matteo (su diseño ya está en la carrera como M3) | se deja como está |
  | `cloud-portability-test` | prueba de la nube, terminada | juntada con `main` el 26 oct; se puede borrar |
  | `leah/workspace` | T11 y trabajo propio de Leah (manual l1-review-clock v1–v3, panel de resultados) | juntada con `main` el 26 oct (16:20, 16:55 y 17:57); v1–v3 en la carrera; sus partidas de origen `leah` importadas |
  | `matteo-t4-growth` | T4 de Matteo (value-conversion, observed-growth) | juntada con `main` el 26 oct (16:20 y 16:55); los dos manuales están en la carrera |
  | `matteo/observed-growth-v3` | observed-growth-v3 de Matteo | juntada con `main` el 26 oct, 18:15; en la carrera (4 partidas); su piloto en casa: 4 de 4 terminadas, Q media 71,4 (otra celda; se comprueba en la carrera) |
  | `alejandro/investigacion-decisiones` | línea de investigación de decisiones (Codex), sólo analiza exports | juntada con `main` el 26 oct, 18:32 (PR #3) |
  | `alejandro/carrera-rapida` | carrera rápida (T14) y partidas de DeepSeek (T6) | pendiente de juntar; la nube la junta y cambia de sistema |
  | `matteo/observed-growth-v4` y `-v5` | iteraciones de Matteo | juntadas con `main` el 26 oct, 19:06 como fuente. v4 no se juega (su propio piloto la dejó por debajo de v3); v5 en espera del resultado de v3 en la carrera |
  | `alejandro/laboratorio-adaptativo` | laboratorio adaptativo y presupuesto (Alejandro) | **sin juntar**: está marcada WIP y cambia módulos del núcleo (`decisions.py`, `cli.py`); se junta cuando esté terminada |
  | `matteo/observed-growth-v2` | observed-growth-v2 de Matteo | juntada con `main` el 26 oct, 17:57; en la carrera (4 partidas); sus partidas de origen `matteo` importadas |
  | `alejandro/explicacion-repo` | explicación del repositorio (Codex) | juntada con `main` el 26 oct, 16:55 |
- Al terminar una tarea:
  1. Las pruebas tienen que pasar (`uv run pytest -q`).
  2. El resultado queda donde dice la tabla.
  3. Actualiza tu línea en la tabla.
  4. Pide en GitHub que se junte con `main` (*Pull Request*).

**Documentar siempre (obligatorio)**

Lo que sólo está en un chat se pierde cuando el chat termina, se queda sin cuota o se resume. Por eso cualquier chat o sesión, incluida la nube, documenta en el repo:
- **Antes de terminar.** También si se va a quedar sin cuota o sin contexto: en cuanto lo veas venir, documenta primero y sigue después.
- **Cada hora** si es un trabajo largo, con commit y push.

Qué hay que dejar escrito, en una sección **Relevo** al final del informe de tu tarea (o de `lab/reports/cloud-run-status.md` en la nube):
1. Qué has hecho y por qué: las decisiones, con su motivo.
2. Los resultados con números, y dónde están los datos.
3. Lo que falló o quedó a medias, y cómo lo dejaste.
4. Qué queda pendiente y cuál es el siguiente paso concreto, con los comandos para retomarlo.
5. Tu línea de la tabla de tareas actualizada.

Después, commit y push a tu rama. Una tarea no está terminada hasta que su relevo está en GitHub.

**Partidas**
- **La carrera la juega la nube.** Desde T11 (Leah), otro ordenador puede jugar sin pisarla. Primero `uv run careerlab origin set <nombre>`, y después se exporta a `lab/registry-origins/<nombre>/`; la organizadora lo importa con `careerlab import --dir lab/registry-origins/<nombre>`. Las partidas con Claude en la cuenta Max comparten el freno semanal, así que avisa antes en tu línea de la tabla. Los bots sin IA no gastan cuota.
- Para proponer un manual nuevo:
  1. Copia la carpeta [f3-lean-v1](lab/policies-src/f3-feedback-reactive/f3-lean-v1/) como plantilla dentro de `lab/policies-src/<familia>/<nombre>-v1/`.
  2. Rellena `policy.json`: la idea (`hypothesis`), qué esperas ver (`predicted_behaviour`) y qué demostraría que es mala (`refutation`).
  3. Escribe el manual en `bundle/skills/<skill>/SKILL.md`, en inglés.
  4. Compruébalo con `uv run careerlab lint lab/policies-src/<familia>/<nombre>-v1`, que no debe dar errores.
  5. Cuando esté en `main`, la nube lo registra y lo juega.

**Lo que nunca se hace**
- Poner claves o secretos en el repo. La clave de la API va sólo en el `.env` del programa oficial.
- Leer el interior del simulador: su paquete, su base de datos o sus archivos internos. Sólo se usan las 5 herramientas oficiales.
- Poner en los manuales títulos de eventos, respuestas fijas a eventos, meses concretos o umbrales no publicados. `careerlab lint` lo vigila.
- Tocar la rama de otro o editar el protocolo congelado.
- Los resúmenes de partidas en `lab/reports/teacher-digests/` contienen texto del juego de desarrollo. Sirven para estudiar, pero no se copian frases a los manuales, y por eso el repo tiene que seguir siendo **privado**.
- **Datos con texto del juego:** `lab/reports/first-review-search/` (Matteo, 38,8 MB) contiene un catálogo de eventos de desarrollo con sus opciones y resultados. Es material de estudio en el repo privado, como los resúmenes de partidas. **No se pasa nunca a los diseñadores ni se copia a un manual**: las respuestas por evento están prohibidas, se escriban como se escriban.

**El organizador.** Es un papel, no un chat fijo. Desde el 26 oct lo hace la sesión de la nube que juega. Entre sus tareas:
- juntar las ramas terminadas con `main`;
- actualizar este archivo;
- decidir lo siguiente y escribir su relevo.

Si algún día se vuelve a separar en un chat local, ese chat se abre en la carpeta del proyecto, en `main`, sin copia aparte. El diario técnico, en inglés, está en [task_plan.md](task_plan.md), [findings.md](findings.md) y [progress.md](progress.md).

## 7. Para Matteo

- Tu diseño de tres Skills entró en la carrera como **M3**. Con Haiku está dormido (38 frente a 60 del líder), pero se puede despertar y el laboratorio lo revisa de vez en cuando.
- La tarea que mejor encaja con tu cuota es **T4**: proponer manuales que no se nos hayan ocurrido, sobre todo de crecimiento (ascensos y dinero) y sin copiar los nuestros.
- T11 ya está hecha: si quieres jugar desde tu ordenador, pon tu origen (`careerlab origin set matteo`) y exporta a `lab/registry-origins/matteo/`. Tu `value-conversion-v1` ya está en la carrera, con 4 partidas de Haiku en cola.
- En la app de Claude, pon `matteo` como prefijo de ramas (**Ajustes → Claude Code → Branch prefix**). Así tus ramas se llamarán `matteo/...` y se sabrá de quién es cada una.

## 8. Mapa de documentos

| Para | Documento |
|---|---|
| Instalar y usar el laboratorio | [lab/README.md](lab/README.md) · nube: [lab/CLOUD_RUNBOOK.md](lab/CLOUD_RUNBOOK.md) |
| Por qué este método y cómo decide | [method-decision.md](research/careerlab/method-decision.md) · reglas congeladas: [prereg-v1.md](lab/protocol/prereg-v1.md) |
| Cómo gastar los 50 USD de DeepSeek | [target-budget.md](research/careerlab/target-budget.md) |
| Guion del vídeo y la historia para el jurado | [jury-story.md](research/careerlab/jury-story.md) |
| Hallazgos técnicos con fecha | [findings.md](findings.md) |
| Resúmenes de partidas de Opus | [lab/reports/teacher-digests/opus/index.md](lab/reports/teacher-digests/opus/index.md) |
| Prueba del método en el juego de juguete | [synthetic-method-comparison](lab/reports/synthetic-method-comparison/results.md) |

**Instalar en otro ordenador:** sigue el apartado *Install* de [lab/README.md](lab/README.md).

Si el repo está en iCloud y aparece `No module named 'careerlab'`, hay dos arreglos:

```bash
chflags nohidden .venv/lib/python3.13/site-packages/*.pth
```

```bash
export UV_PROJECT_ENVIRONMENT="$HOME/venvs/huawei"
```

El primero sirve en el momento. El segundo, que saca el entorno fuera de iCloud, es la solución definitiva.
