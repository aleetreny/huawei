# ESTADO del proyecto: léelo primero

Equipo **Gradient Depression**, Huawei TechArena UK 2026, reto *Career Survival*.
Última actualización: **26 oct 2026, 15:33 UTC**, chat organizador (rama `main`).

Este documento es el punto de partida de cualquier persona o agente: dónde vamos, qué falta, qué está decidido y cómo trabajamos. Si un chat nuevo sólo puede leer un archivo, que sea este.

## 1. El reto en cinco líneas

- Un juego de texto: una IA vive 48 meses de carrera en una empresa. Cada mes reparte energía y elige opciones ante eventos.
- Se pierde por dos evaluaciones semestrales malas (despido), por una "crisis de confianza" o por agotamiento. Al final hay una nota de 0 a 100.
- **No jugamos nosotros.** Entregamos un manual (*Skills*, texto en inglés) que lee **DeepSeek** (`deepseek-v4-flash`) dentro del programa oficial JiuwenSwarm.
- Nota de cada versión: 80 % la media de 3 partidas, 10 % la calidad de los documentos de diseño y 10 % el ahorro de tokens. Cuenta la mejor de nuestras versiones.
- Los 10 mejores equipos pasan a un jurado con vídeo, que vale el 30 % de la nota final.

## 2. Dónde vamos

**El laboratorio funciona.** Juega partidas por la vía oficial, muchas a la vez, se recupera de fallos y guarda todo. Las instrucciones están en [lab/README.md](lab/README.md).

Llevamos 99 partidas con IA (modelos de Claude haciendo de DeepSeek) y 150 con bots. Además hay 753.580 partidas en un juego de juguete que sirven para comprobar el método de elección.

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

**Lo que aún no sabemos:**
- Cómo juega DeepSeek con nuestros manuales. Hace falta la clave de la API (tarea T5).
- Cuál es el techo del juego, es decir, si queda mucho margen o ya estamos cerca (tarea T13).

**Cuota de Claude (cuenta Max):**
- Se renueva hoy, 26 oct, a las 16:00 hora UK, y esa semana tiene que durar hasta el 1 nov.
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
| T1 | Carrera continua de manuales (jugar, decidir, generar hijas) | nube | en marcha | rama `cloud-lab-run`: `lab/reports/cloud-run-status.md`, cada hora |
| T2 | Destilar las partidas ganadoras de Opus en hijas de F3, sólo reglas generales | nube | escrita a las 15:03 (reglas y 2 hijas de F3); se juegan tras la tanda 1 | `cloud-lab-run`: `lab/reports/teacher-digests/distilled-rules.md`, `lab/policies-src/f3-feedback-reactive/` |
| T3 | Familia nueva "sobrevivir y crecer" (buscar ascensos y dinero cuando todo va bien) | nube | manual F8 escrito a las 15:03; se juega tras la tanda 1 | `cloud-lab-run`: `lab/policies-src/` (f8-secure-growth-v1) |
| T4 | Ideas de fuera: manuales nuevos escritos sin mirar los nuestros, con otro modelo u otra cuota | nube (agente que no ve nuestros manuales) y Matteo si quiere | nube: en cola; Matteo: value-conversion-v1 lista; síntesis observed-growth-v1 tras leer F3/F8 (no ciega); ambos lint OK, 225 tests OK; usuario pide prueba cloud con mismo actor, aún no encolada | Matteo: `matteo-t4-growth`, informes `lab/reports/matteo-t4-value-conversion.md` y `lab/reports/matteo-observed-growth.md`; nube: rama `<persona>/ideas-fuera` |
| T5 | Envío preliminar y clave de la API | Alejandro | pendiente | apuntar aquí la fecha en que llegue la clave |
| T6 | Piloto con DeepSeek: 2 partidas para medir coste y tokens ([target-budget.md](research/careerlab/target-budget.md)) | organizador | espera a T5 | `lab/reports/target-pilot/` |
| T7 | Vídeo `presentation.mp4` para el corte 1, en inglés, máximo 10 minutos y respondiendo a las 5 preguntas oficiales | equipo (personas) | pendiente | guion base en [jury-story.md](research/careerlab/jury-story.md) |
| T8 | Documentos de diseño del corte 1 (`skills_design.md`, `decision_report.md`) | nube (organizadora), revisa el equipo | **no empezar hasta el 27 oct** (decisión de Alejandro) | `cloud-lab-run`: `lab/submissions/r1-draft/design/` |
| T9 | Elegir el manual del corte 1 (el líder de la última decisión), empaquetar y validar con `careerlab package` | nube (organizadora) | espera a T7 y T8 | `lab/submissions/r1/` |
| T10 | Bots sin IA para estudiar el reparto de energía (opcional, no gasta cuota) | nube, en segundo plano | opcional | `lab/reports/energy-bots/` |
| T11 | Permitir que varios ordenadores jueguen a la vez sin pisarse los resultados | organizador | sólo si alguien más va a jugar | código en `careerlab/` |
| T12 | Juntar `cloud-lab-run` con `main` después de cada tanda | nube (organizadora) | cada día | `main` |
| T13 | Techo del juego: 4–6 partidas de Opus al máximo esfuerzo con todo lo que sabemos en general. Nada de resúmenes de eventos concretos. No es una entrega: mide cuánto margen queda | nube | pedida | `cloud-lab-run`: `lab/reports/opus-ceiling/` |

## Relevo del organizador (26 oct, 15:33 UTC)

**Desde el 26 oct a las 16:00 UTC, la organizadora es la sesión de la nube "CareerLab continuous race in the cloud"** (rama `cloud-lab-run`). Juega las partidas y, además, hace de organizadora:
- junta sus resultados con `main` (T12);
- mantiene este archivo al día;
- más adelante, prepara la entrega (T8 y T9 a partir del 27 oct).

Todo se hace en la nube, así que el Mac puede estar apagado. **Para hablar con ella**, abre esa sesión en claude.ai/code o en la app y escríbele directamente. No hace falta otro chat. Si se parase, su relevo (al final de `lab/reports/cloud-run-status.md`) trae un prompt listo para abrir otra sesión de nube que haga lo mismo. Nunca debe haber dos a la vez.

**Hecho hoy por el primer chat organizador (local)**
- El laboratorio funciona.
- 99 partidas con IA y 150 con bots. El método se ha comprobado en el juego de juguete.
- El freno semanal de cuota está en marcha, y este archivo existe con sus reglas.

**Mensajes que ese chat envió a la nube**
- 14:38: destilar las partidas de Opus (T2).
- 14:45: freno semanal y familia "sobrevivir y crecer" (T3).
- 15:06: no editar ESTADO.md (ya no vale: ahora es la organizadora).
- 15:11: techo de Opus (T13).
- 15:15: tope al 0,97 hasta las 16:00 y después volver al 0,80.
- 15:20: escribir el relevo completo antes de terminar.
- 15:33: pasar a ser también la organizadora, sin documentos de entrega hasta el 27 oct.

**Prioridades de la nube hasta el 27 oct:** sólo pruebas.
- La carrera (T1), con las hijas de T2 y la familia de T3 dentro.
- El techo de Opus (T13).
- Ideas de fuera (T4), escritas por un agente que no ve nuestros manuales.
- Bots sin IA (T10), que no gastan cuota.
- Todo dentro del freno semanal y documentando cada hora.

## 5. Decisiones ya tomadas (no hace falta volver a discutirlas)

- **26 oct, Alejandro:** se permiten partidas con modelos de Claude como sustitutos de DeepSeek, y los bots no tienen límite.
- **26 oct, Alejandro:** no preguntamos en Discord; si las reglas no lo prohíben, lo hacemos. Riesgo conocido: la norma oficial dice *"the absence of an express prohibition is not permission"*. Si cambiamos de idea, hay un borrador del mensaje en [organiser-questions.md](research/organiser-questions.md) §0.
- **Dinero:** sólo los 50 USD de la clave. Cualquier otro gasto en APIs necesita un presupuesto confirmado por Alejandro.
- **Método:** las reglas estadísticas se fijaron antes de ver resultados ([prereg-v1.md](lab/protocol/prereg-v1.md)). No se editan; si hay que cambiarlas, se crea una versión nueva.
- **Quién juega:** de momento sólo la nube juega partidas (ver la regla de partidas en la sección 6).

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
- **Sólo la nube lanza partidas** (`careerlab run`). Si dos ordenadores juegan a la vez, sus resultados se numeran igual y se pisan al juntarlos. Para jugar desde otro sitio, primero hay que hacer T11.
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
- No lances partidas desde tu ordenador hasta que esté hecha T11.
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
