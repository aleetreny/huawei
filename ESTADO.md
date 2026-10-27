# ESTADO del proyecto: léelo primero

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*.
Última actualización: **26 oct 2026, 16:20 UTC**, sesión de la nube (organizadora).

Este documento es el punto de partida de cualquier persona o agente: dónde vamos, qué falta, qué está decidido y cómo trabajamos. Si un chat nuevo sólo puede leer un archivo, que sea este.

## 1. El reto en cinco líneas

- Un juego de texto: una IA vive 48 meses de carrera en una empresa. Cada mes reparte energía y elige opciones ante eventos.
- Se pierde por dos evaluaciones semestrales malas (despido), por una "crisis de confianza" o por agotamiento. Al final hay una nota de 0 a 100.
- **No jugamos nosotros.** Entregamos un manual (*Skills*, texto en inglés) que lee **DeepSeek** (`deepseek-v4-flash`) dentro del programa oficial JiuwenSwarm.
- Nota de cada versión: 80 % la media de 3 partidas, 10 % la calidad de los documentos de diseño y 10 % el ahorro de tokens. Cuenta la mejor de nuestras versiones.
- Los 10 mejores equipos pasan a un jurado con vídeo, que vale el 30 % de la nota final.

## 2. Dónde vamos

**El laboratorio funciona.** Juega partidas por la vía oficial, muchas a la vez, se recupera de fallos y guarda todo. Las instrucciones están en [lab/README.md](lab/README.md).

Llevamos 124 partidas con IA (modelos de Claude haciendo de DeepSeek) y 550 con bots. Además hay 753.580 partidas en un juego de juguete que sirven para comprobar el método de elección.

**Clasificación actual** (Claude Haiku jugando; decisión del 26 oct a las 14:07):

| Manual | Nota estimada | Estado |
|---|---:|---|
| F3 reacciona al feedback | 60,2 | líder |
| f3 recombinada (F3 + F1) | 58,9 | sigue en juego |
| f3 ligera | 57,5 | sigue en juego |
| F7 tres skills | 50,0 | sigue en juego |
| F1 equilibrio | 49,3 | sigue en juego |
| P0 mínimo, M3 (diseño de Matteo) | 39,4 y 38,0 | dormidos (se pueden despertar) |

**Lo que hemos aprendido:**
- Hay dos formas de perder: dos evaluaciones malas seguidas (despido en el mes 24) o una crisis de confianza tras acumular riesgo. Todas las partidas empiezan con una C.
- **Sabemos sobrevivir, pero no crecer.** En las 48 partidas terminadas faltan unos 40 puntos: 16 se pierden en nivel (ascensos) y 13 en dinero. Ningún manual busca ascender y ganar dinero cuando las cosas van bien.
- Qué modelo juega importa:
  - Haiku termina 30 de 59 partidas y Sonnet 10 de 26.
  - Opus con memoria corta termina 5 de 6. Opus jugando casi sin manual saca entre 62 y 67, así que sirve de "maestro".
- Los bots que eligen al azar mueren hacia el mes 6. De las 73.858 partidas de Matteo, ninguna llegó al final.

**Novedades de la tarde (26 oct, nube; provisional, con 3–4 partidas por manual, antes de la decisión de la tanda 1):**
- Media de la nota (Q) con Haiku: f3 recombinada 60,6 (4 de 4 terminadas), F3 55,3, f3 ligera 55,1, hija destilada "defuse antes de la evaluación" 51,0, F8 crecer 49,3, o1 hueco de ascenso 44,0, o2 a tope 36,2, hija destilada completa 31,7.
- La mayoría de las derrotas siguen siendo el despido en el mes 24. La hija destilada completa, que quita el plan de recuperación tras una evaluación mala, cae ahí 2 de 3 veces.
- El techo de Opus (T13) empezó mal: su primera partida también cayó despedida en el mes 24 (nota 24,5). Quedan 3; se interpretará con los umbrales escritos de antemano.
- Bots de energía (T10, 400 partidas, sin cuota): la salud es el primer límite. Sin un punto de recuperación cada trimestre, todos los bots se agotan. Recuperar sólo cuando la salud ya está baja llega tarde. La mejor mezcla es "desactivar riesgo + salud". Ninguna mezcla de energía evita la C de la primera evaluación.

**Lo que aún no sabemos:**
- Cómo juega DeepSeek con nuestros manuales. Hace falta la clave de la API (tarea T5).
- Cuál es el techo del juego, es decir, si queda mucho margen o ya estamos cerca (tarea T13).

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

| # | Tarea | Quién | Estado | Dónde queda el resultado |
|---|---|---|---|---|
| T1 | Carrera continua de manuales (jugar, decidir, generar hijas) | nube | en marcha: tanda 1 (44 partidas) en juego desde las 16:00; decisión al acabarla | rama `cloud-lab-run`, informe `lab/reports/cloud-run-status.md` cada hora; se junta con `main` |
| T2 | Destilar las partidas ganadoras de Opus en hijas de F3, sólo reglas generales | nube | hecha: reglas en `distilled-rules.md`; 2 hijas registradas y jugando (resultados provisionales en la sección 2) | `lab/reports/teacher-digests/distilled-rules.md`, `lab/policies-src/f3-feedback-reactive/` |
| T3 | Familia nueva "sobrevivir y crecer" (buscar ascensos y dinero cuando todo va bien) | nube | hecha: F8 (`f8-secure-growth-v1`) registrada y jugando | `lab/policies-src/f8-secure-growth/` |
| T4 | Ideas de fuera: manuales nuevos escritos sin mirar los nuestros, con otro modelo u otra cuota | nube (agente que no ve nuestros manuales) y Matteo | nube: o1 hueco de ascenso y o2 a tope jugando; o3 "padrinos" en espera (se parece a F4 + F5). Matteo: `value-conversion-v1` juntada con `main` y en cola (4 partidas); `observed-growth-v1` (síntesis tras leer F3/F8, no ciega) lista para registrar, lint OK; piloto local aislado con Haiku: 64,78, L5, 48 meses; 4 partidas Haiku más (origen `matteo`, fuera de las decisiones): Q media 40,85, 1 de 4 terminada (70,94, L5 en el mes 42), 3 despedidas en el mes 24 ; investigación black-box pedida por Matteo: 1.961 experimentos de seis meses resueltos (+31 interrupciones técnicas), 89 escenarios/212 preguntas, 503/508 respuestas probadas; bot empírico 336/512 ascensos y 328/512 ascenso con supervivencia; borrador general sin validar con agentes; sin cuota IA ni registros cloud ; prueba de transferencia autorizada por Matteo: bloque 4+4 Haiku Pro personal congelado y preparado, sin lookup; 0 partidas iniciadas por cuota agotada (429); Matteo elige reanudar manualmente, sin automatización; 242 tests OK; `lab/reports/first-review-transfer/README.md` ; cierre del catálogo conocido: +597 simulaciones sin IA, 510/510 respuestas narrativas (213 fases/89 títulos), 528/528 incluyendo acciones públicas; sin pendientes; auditoría independiente de 2.589 registros (31 interrupciones históricas) ; análisis de patrones: 6 familias, 25/89 títulos sólo tras la primera revisión; revisión C en 1.940/1.940; un contraejemplo invalida el separador numérico exacto previo (ver informe), sin nuevas partidas  ; manual operativo `promotion-readiness-v2` guardado (sin validar), auditoría pre-review de observabilidad: 61 grupos con mismo estado y resultado distinto, 0 al fijar también acción (84 grupos repetidos); método de falsificación/intervención documentado, meses 7–12 aún no iniciados; 253 tests OK  ; exploración Matteo meses 7–12 completada sin IA: 1.183 partidas resueltas, 126 títulos/264 fases, 642/642 respuestas narrativas y 659/659 totales con auditoría independiente; 443 segundas promociones, 394 con supervivencia; 783 entran promovidos y vivos al mes 7; consecuencias entre semestres y fricción social tras ascenso documentadas; origen aislado `matteotwelve`, workers terminados, comparación IA sigue parada; 260 tests OK  ; 27 oct Matteo: riesgo acumulado completado sin IA, 713 intentos/512 asignaciones aleatorias resueltas (8 combinaciones); guardia memoria+lookup reduce crisis 20/256 a 4/256 y ascenso con supervivencia 174/256 a 194/256; solo cambiar limpieza no muestra ventaja clara; 46/50 muertes por insolvencia ya tenían Wealth<=0 al asignar; +10 bots cierran fase nueva, catálogo extendido 644/644 narrativas y 661/661 totales; borrador general primer año, origen `matteotrust`, workers terminados, 267 tests OK  ; Matteo 27 oct: estudio económico completado sin IA, 2×512 partidas desde new_game con controles independientes; reserva fuerte: insolvencias 26→2 pero ascenso+supervivencia 160→152; calibración ligera: insolvencias 35→5 y ascenso+supervivencia 125→166 (256 por brazo); sin comparación directa entre intensidades ni garantía; +73 bots cierran fase nueva, catálogo 646/646 narrativas y 663/663 totales; 50.356 decisiones reproducidas, origen `matteocash`, workers terminados, 273 tests OK  ; Matteo: gaps completado sin IA, 80 casos (53 fallan primero, 27 estancados L2); 768 partidas: ascenso+vivo control131/192, skill131, network92, output108; seguimiento conjunto384: 107→116/192 pero supervivencia182→169, no adoptar variantes; 57.289 decisiones reproducidas, sin nuevos nodos/catálogo663 intacto; origen `matteogaps`, workers terminados, 280 tests OK ; Matteo: filtro de sostenibilidad completado sin IA, diagnóstico101 en68 carreras y576 partidas nuevas (192/brazo); ascenso+vivo control122/conjunto120/filtrado122, supervivencia190/165/181, crisis0/19/6; filtro recupera parte del daño pero no supera control, no adoptar;28.523 decisiones y9.590 restricciones verificadas, cero nuevos nodos, origen matteofilter, workers terminados,287 tests OK; commit local completo, push pendiente por fallos TLS/HTTP408 (ver Relevo) | `lab/policies-src/o*-*/`, `lab/policies-src/matteo-value-conversion/`, `lab/policies-src/matteo-feedback-growth/`, informes `lab/reports/matteo-t4-value-conversion.md`, `lab/reports/matteo-observed-growth.md` y `lab/reports/matteo-observed-growth-haiku-4.md`; datos en `lab/registry-origins/matteo/` ; `lab/reports/first-review-search/README.md` ; `lab/reports/known-catalogue-closure/README.md` ; `lab/reports/scenario-patterns/README.md`  ; `lab/reports/promotion-strategy/README.md`, `lab/policies-src/matteo-first-review/promotion-readiness-v2/`  ; `lab/reports/second-review-search/`  ; `lab/reports/trust-risk-study/`  ; `lab/reports/financial-reserve-study/`  ; `lab/reports/growth-gap-study/` ; `lab/reports/constrained-growth-study/` |
| T5 | Envío preliminar y clave de la API | Alejandro | pendiente | apuntar aquí la fecha en que llegue la clave |
| T6 | Piloto con DeepSeek: 2 partidas para medir coste y tokens ([target-budget.md](research/careerlab/target-budget.md)) | organizador | espera a T5 | `lab/reports/target-pilot/` |
| T7 | Vídeo `presentation.mp4` para el corte 1, en inglés, máximo 10 minutos y respondiendo a las 5 preguntas oficiales | equipo (personas) | pendiente | guion base en [jury-story.md](research/careerlab/jury-story.md) |
| T8 | Documentos de diseño del corte 1 (`skills_design.md`, `decision_report.md`) | nube (organizadora), revisa el equipo | **no empezar hasta el 27 oct** (decisión de Alejandro) | `cloud-lab-run`: `lab/submissions/r1-draft/design/` |
| T9 | Elegir el manual del corte 1 (el líder de la última decisión), empaquetar y validar con `careerlab package` | nube (organizadora) | espera a T7 y T8 | `lab/submissions/r1/` |
| T10 | Bots sin IA para estudiar el reparto de energía (no gasta cuota) | nube | hecha (400 partidas; lecciones en la sección 2) | `lab/reports/energy-bots/README.md` |
| T11 | Permitir que varios ordenadores jueguen a la vez sin pisarse los resultados | Leah | hecha y juntada con `main` (26 oct, 16:20; 230 tests OK). La nube ya usa el registro migrado | código en `careerlab/`; informe en [lab/reports/t11-multi-machine](lab/reports/t11-multi-machine/README.md) |
| T12 | Juntar `cloud-lab-run` y las ramas terminadas con `main` | nube (organizadora) | en marcha: tras cada tanda y cada resultado importante (1ª vez: 26 oct, 16:20) | `main` |
| T13 | Techo del juego: 4–6 partidas de Opus al máximo esfuerzo con todo lo que sabemos en general. Nada de resúmenes de eventos concretos. No es una entrega: mide cuánto margen queda | nube | en marcha: umbrales escritos antes de jugar; 1 de 4 partidas hecha (despedido en el mes 24, nota 24,5) | `lab/reports/opus-ceiling/README.md` |

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

**Siguiente:** decisión de la tanda 1 hacia las 17:00 UTC y regla de estancamiento. El techo de Opus se mide contra sus umbrales. Los documentos de entrega (T8 y T9) empiezan el 27 oct a primera hora (UK).

## 5. Decisiones ya tomadas (no hace falta volver a discutirlas)

- **26 oct, Alejandro:** se permiten partidas con modelos de Claude como sustitutos de DeepSeek, y los bots no tienen límite.
- **26 oct, Alejandro:** no preguntamos en Discord; si las reglas no lo prohíben, lo hacemos. Riesgo conocido: la norma oficial dice *"the absence of an express prohibition is not permission"*. Si cambiamos de idea, hay un borrador del mensaje en [organiser-questions.md](research/organiser-questions.md) §0.
- **Dinero:** sólo los 50 USD de la clave. Cualquier otro gasto en APIs necesita un presupuesto confirmado por Alejandro.
- **Método:** las reglas estadísticas se fijaron antes de ver resultados ([prereg-v1.md](lab/protocol/prereg-v1.md)). No se editan; si hay que cambiarlas, se crea una versión nueva.
- **Quién juega:** la carrera la juega la nube. Desde T11, otro ordenador puede jugar con su propio origen (ver *Partidas* en la sección 6).
- **26 oct, Alejandro:** Claude no debe aparecer como contribuidor en GitHub. Los commits van a nombre de una persona y sin líneas `Co-Authored-By` de Claude. La nube hace los suyos a nombre de Alejandro.
- **26 oct, Alejandro:** la nube hace push a `main` como organizadora (tras pasar los tests).

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
  | `leah/workspace` | T11 de Leah | juntada con `main` el 26 oct, 16:20 |
  | `matteo-t4-growth` | T4 de Matteo (value-conversion) | juntada con `main` el 26 oct, 16:20; en la carrera |
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
