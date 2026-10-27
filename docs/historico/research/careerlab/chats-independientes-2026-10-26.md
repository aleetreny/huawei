# Cómo trabajar con chats independientes (desde el 26 oct, noche)

Decisión de Alejandro (26 oct, ~22:45 UTC): se para la carrera automática de la nube y se trabaja con chats independientes. Por qué: [estrategia-primeros-principios-2026-10-26.md](estrategia-primeros-principios-2026-10-26.md). En resumen, entre manuales razonables el manual apenas cambia la nota (unos 2,5 puntos de diferencia real frente a 19 de azar por partida). Lo que más sube nuestra nota es lo seguro: tres versiones distintas, SKILL.md escritos para la rúbrica y vídeo y documentos.

## Reglas comunes (para cualquier chat, de cualquier persona)

1. **Una misión por chat**, con un entregable y una fecha. Si un chat se alarga mucho, deja el relevo escrito y abre otro.
2. **Antes de empezar, lee tres cosas:** `ESTADO.md`, el análisis de estrategia de arriba y `lab/fastloop/lessons.md`.
3. **Tu rama y tu origen.** Trabaja en `<persona>/<tarea>` y juega con tu propio origen de registro:

   ```bash
   uv run careerlab origin set <nombre>
   ```

   - Exporta con `uv run careerlab export`, que escribe en `lab/registry-origins/<nombre>/`.
   - Nunca toques `lab/registry/` ni la rama de otro.
4. **Cuota compartida** (todos usamos la misma cuenta Max):
   - como mucho **3 chats jugando partidas de Claude a la vez**;
   - como mucho **4 partidas a la vez por chat** (`--slots 4`);
   - límite de la ventana de 5 horas: `--max-five-hour 0.80` para el chat de entregas y `0.65` para los de exploración, para que las entregas tengan margen.

   El freno de cuota lee el uso de toda la cuenta, así que todos los chats se paran solos cuando hace falta.
5. **Disciplina con los números:**
   - compara siempre contra un manual de referencia jugado en el mismo chat y en las mismas condiciones;
   - con 4 partidas no se concluye nada;
   - para decidir, unas 20–30 partidas por manual, y sólo se ven diferencias grandes (unos 15 puntos con 20–30 partidas; 5 puntos necesitarían unas 180);
   - mira primero las señales baratas: si cambian las decisiones del jugador y si asciende antes del mes 12.
6. **Sin diseñadores automáticos ni consejos de agentes.** Usa subagentes sólo para tareas acotadas: puntuar con la rúbrica, leer partidas, escribir una variante concreta.
7. **Documenta en el repo:** informe con sección Relevo al terminar (o cada hora si es largo), tu línea de la tabla de `ESTADO.md` y una PR.
8. **Juntar con `main`:** cada chat abre su PR y la junta Alejandro desde GitHub, o el propio chat con `gh pr merge` si las pruebas pasan y no hay conflictos. Cada chat cambia sólo su línea de la tabla y su informe; así las PR casi nunca chocan.
9. **DeepSeek:** sólo las partidas acordadas antes de cada corte, desde el Mac de Alejandro (comandos en [carrera-rapida-2026-10-26.md](carrera-rapida-2026-10-26.md), Relevo).

## Chats propuestos

| Chat | Misión | Entregable | Fecha |
|---|---|---|---|
| **A. Entregas** (T15) | Versión 1: v7 si el chat B la confirma; si no, el mejor manual general. Reescrito para la rúbrica de calidad sin cambiar sus reglas; comprobar que no empeora; documentos de diseño; paquete validado | `lab/submissions/r1/`, informe y PR | **27 oct, antes de las 20:00 UK** |
| **B. Réplica del mecanismo del ascenso** (T16) | Comprobar con suficientes partidas el manual observed-growth-v7 de Matteo (PR #13), basado en su estudio del ascenso (PR #10): hay que tener las habilidades en el máximo del nivel en el momento de la evaluación y proteger red y resultados en los eventos de antes. Haiku, 25 partidas de v7 y 25 de un manual de referencia, en las mismas condiciones | informe y PR | **27 oct a las 14:00 UK** (a tiempo para la versión 1) |
| **C. Simulaciones brutas del juego** (T17) | El chat que ya tiene abierto Alejandro | lo que él decida | — |
| **Personas** (T7) | Vídeo en inglés, de 10 minutos como máximo, con las 5 preguntas oficiales | `presentation.mp4` | **27 oct** |
| **Decisión de cada corte** | Un chat corto nuevo antes de cada corte: elegir qué versión se sube con los informes de A, B y C, y juntar las PR terminadas | versión elegida y `ESTADO.md` al día | 27, 30 oct y 1 nov |

La línea de Matteo (mecánica del ascenso, sus PR #10–#13) es la más prometedora: ataca el primer año, que decide dos tercios de la nota. Más adelante, si queda cuota: un chat para "un primer año al estilo de los bots que llegaron al nivel 6" (proyecto clave cada trimestre, un punto de salud cada trimestre y limpiar el riesgo con los avisos). También lo puede coger Matteo o Leah.

## Prompts para pegar

**A. Entregas**

```text
Lee ESTADO.md, docs/historico/research/careerlab/estrategia-primeros-principios-2026-10-26.md y docs/historico/research/careerlab/chats-independientes-2026-10-26.md. Tu tarea es T15: la versión 1 para el corte del 27 oct a las 24:00 UK. Rama alejandro/entrega-v1; origen de registro "entregas" (uv run careerlab origin set entregas).
1. Elige el manual base: observed-growth-v7 de Matteo si el informe del chat B (T16, antes de las 14:00 UK) dice que es mejor. Si no, el que mejor cumpla la rúbrica oficial de calidad de los SKILL.md (local-runs/official-runner/docs/competition-rules.rst, "Document design quality") entre f3-lean-v1, observed-growth-v3, f3-balance-recombined-v1 y targeted-1026-201334, que rinden igual dentro del ruido.
2. Reescríbelo para esa rúbrica sin cambiar sus reglas: descripción con qué hace y cuándo usarlo; pasos con prioridades y criterios, también cerca de los límites; ventanas de ascenso y los 48 meses; todos los modos de fallo publicados; que valga si cambian los eventos. Nada de eventos con nombre, meses concretos ni umbrales no publicados. Pasa uv run careerlab lint.
3. Comprueba que no empeora: 10 partidas de Haiku del original y 10 de la reescrita, con --slots 4 y --max-five-hour 0.80. Si la reescrita termina claramente menos partidas, vuelve al texto original.
4. Escribe design/skills_design.md y design/decision_report.md en inglés, concretos y coherentes con los Skills que se suben. Empaqueta con careerlab package y valida con el programa oficial. Para validar desde una copia aparte, CAREERLAB_RUNNER_DIR tiene que apuntar a local-runs/official-runner y no hay que exportar UV_PROJECT_ENVIRONMENT. El paquete final espera al presentation.mp4 que graba el equipo.
5. Deja todo en lab/submissions/r1/, escribe un informe con Relevo, actualiza tu línea T15 de ESTADO.md y abre una PR.
```

**B. Réplica del mecanismo del ascenso**

```text
Lee ESTADO.md, docs/historico/research/careerlab/estrategia-primeros-principios-2026-10-26.md, docs/historico/research/careerlab/chats-independientes-2026-10-26.md, lab/reports/matteo-promotion-study.md y la PR #13 de Matteo (observed-growth-v7). Tu tarea es T16: comprobar con suficientes partidas si observed-growth-v7 mejora de verdad. Rama alejandro/replica-v7; origen de registro "replica" (uv run careerlab origin set replica).
1. Trae la carpeta del manual v7 desde la rama de la PR #13 (matteo/observed-growth-v7) y pásale uv run careerlab lint. El manual de referencia es f3-lean-v1 (5 de 5 terminadas, media 55,5 en 12 partidas de la carrera).
2. Juega 25 partidas de Haiku de cada uno, intercaladas y en las mismas condiciones (--slots 4, --max-five-hour 0.65).
3. Compara partidas terminadas, nota media con su error estándar, ascensos en el primer año y modo de fallo. A mitad de camino (unas 12 por manual), mira si v7 asciende antes del mes 12 más a menudo; esa señal llega antes que la nota.
4. Antes del 27 oct a las 14:00 UK, escribe un informe con Relevo y una recomendación clara para el chat de entregas (¿v7 es mejor, igual o peor?), actualiza tu línea T16 de ESTADO.md y abre una PR.
Ojo con el cumplimiento: v7 usa que las evaluaciones se aplican al principio de su mes, cosa que no dice el manual del juego publicado. Que el texto del Skill no contradiga las reglas publicadas (la rúbrica penaliza contradecir el juego); redáctalo como "ten las habilidades en su máximo antes de cualquier mes de evaluación".
```

La idea del procedimiento explícito para los eventos queda para después: v7 ya la incluye en parte (proteger red y resultados antes de una evaluación).

**Decisión de cada corte** | Un chat corto nuevo antes de cada corte: elegir qué versión se sube con los informes de A, B y C, y juntar las PR terminadas | versión elegida y `ESTADO.md` al día | 27, 30 oct y 1 nov |

La línea de Matteo (mecánica del ascenso, sus PR #10–#13) es la más prometedora: ataca el primer año, que decide dos tercios de la nota. Más adelante, si queda cuota: un chat para "un primer año al estilo de los bots que llegaron al nivel 6" (proyecto clave cada trimestre, un punto de salud cada trimestre y limpiar el riesgo con los avisos). También lo puede coger Matteo o Leah.

## Prompts para pegar

**A. Entregas**

```text
Lee ESTADO.md, docs/historico/research/careerlab/estrategia-primeros-principios-2026-10-26.md y docs/historico/research/careerlab/chats-independientes-2026-10-26.md. Tu tarea es T15: la versión 1 para el corte del 27 oct a las 24:00 UK. Rama alejandro/entrega-v1; origen de registro "entregas" (uv run careerlab origin set entregas).
1. Elige el manual base: observed-growth-v7 de Matteo si el informe del chat B (T16, antes de las 14:00 UK) dice que es mejor. Si no, el que mejor cumpla la rúbrica oficial de calidad de los SKILL.md (local-runs/official-runner/docs/competition-rules.rst, "Document design quality") entre f3-lean-v1, observed-growth-v3, f3-balance-recombined-v1 y targeted-1026-201334, que rinden igual dentro del ruido.
2. Reescríbelo para esa rúbrica sin cambiar sus reglas: descripción con qué hace y cuándo usarlo; pasos con prioridades y criterios, también cerca de los límites; ventanas de ascenso y los 48 meses; todos los modos de fallo publicados; que valga si cambian los eventos. Nada de eventos con nombre, meses concretos ni umbrales no publicados. Pasa uv run careerlab lint.
3. Comprueba que no empeora: 10 partidas de Haiku del original y 10 de la reescrita, con --slots 4 y --max-five-hour 0.80. Si la reescrita termina claramente menos partidas, vuelve al texto original.
4. Escribe design/skills_design.md y design/decision_report.md en inglés, concretos y coherentes con los Skills que se suben. Empaqueta con careerlab package y valida con el programa oficial. Para validar desde una copia aparte, CAREERLAB_RUNNER_DIR tiene que apuntar a local-runs/official-runner y no hay que exportar UV_PROJECT_ENVIRONMENT. El paquete final espera al presentation.mp4 que graba el equipo.
5. Deja todo en lab/submissions/r1/, escribe un informe con Relevo, actualiza tu línea T15 de ESTADO.md y abre una PR.
```

**B. Decisiones en eventos**

```text
Lee ESTADO.md, docs/historico/research/careerlab/estrategia-primeros-principios-2026-10-26.md, docs/historico/research/careerlab/chats-independientes-2026-10-26.md y lab/fastloop/lessons.md. Tu tarea es T16: comprobar si un procedimiento explícito para decidir en los eventos cambia lo que elige el jugador y, si lo cambia, si sube la nota. Rama alejandro/decisiones-eventos; origen de registro "eventos".
1. Escribe una variante del mejor manual (f3-lean-v1 u observed-growth-v3) que añada un procedimiento general para cada evento: valorar cada opción por lo que aporta a Skill, Network y Output frente a su coste en salud, dignidad, dinero y riesgo oculto, con criterios claros. Sin nombrar eventos. Pasa uv run careerlab lint.
2. Primero la señal barata: 8 partidas de Haiku de la variante y 8 del manual base (--slots 4, --max-five-hour 0.65). Con uv run careerlab digest compara, en los eventos que aparecen en las dos, si cambia la opción elegida. Si no cambia, la idea no funciona: documéntalo y para.
3. Si cambia: hasta 25 partidas por manual. Compara partidas terminadas, nota media con su error estándar y ascensos en el primer año. Nunca concluyas con 4 partidas.
4. Escribe un informe con Relevo, actualiza tu línea T16 de ESTADO.md y abre una PR.
```

**Decisión de cada corte**

```text
Lee ESTADO.md y los informes de T15, T16 y T17. Hoy es el corte <fecha>. Junta con main las PR terminadas (pruebas antes) y recomiéndame qué versión subimos: cuenta la mejor de nuestras 3 versiones, así que tiene que ser distinta de las ya subidas y la mejor que tengamos. Comprueba que el paquete es válido (vídeo, documentos, front matter) y actualiza ESTADO.md.
```
