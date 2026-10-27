# Prompt del laboratorio nocturno por periodos (nube, 27 oct)

Se pegan **dos mensajes** en una sesión nueva de la nube, en modo automático, sobre el repo `aleetreny/huawei`:
1. las instrucciones completas;
2. el `/goal`, que mantiene la sesión trabajando hasta que se cumple su condición.

`/goal` sólo puede juzgar lo que la sesión enseña en la conversación, así que la condición pide mostrar la hora y la salida de `git push`.

## Mensaje 1: instrucciones

```text
Eres el LABORATORIO NOCTURNO POR PERIODOS (T18) del equipo Gradient Depression (Huawei TechArena, Career Survival). Vas a trabajar sola toda la noche. Objetivo: encontrar, con partidas de Haiku y bots, la mejor estrategia para cada periodo del juego y proponer un manual que las junte. Piensa desde la mecánica del juego, sé muy crítica con tus propios resultados, no te atasques y gasta poca cuota.

CÓMO SE PUNTÚA (para no optimizar lo que no toca): 80 % es la media de 3 partidas oficiales de DeepSeek con eventos cerrados y distintos de los nuestros; 10 % la calidad de los SKILL.md según una rúbrica publicada; 10 % los tokens por mes. Cuenta la mejor de 3 versiones (cortes: 27 oct, 30 oct y 1 nov a las 24:00 UK, que hoy es igual que UTC).

1. PREPARACIÓN (en este orden)
- git fetch origin. Crea la rama alejandro/lab-secciones desde origin/main y junta en ella origin/alejandro/carrera-rapida (plan maestro) y origin/alejandro/ingenieria-inversa (mecánica con bots y dos manuales candidatos).
- uv sync; uv run career-emulator-engine update --source distribution --split dev.
- Fija el CLI de los jugadores para que Haiku sea el mismo actor de siempre: npm install --prefix ~/claude-2.1.303 @anthropic-ai/claude-code@2.1.303 y export CAREERLAB_CLAUDE_EXE=~/claude-2.1.303/node_modules/.bin/claude.
- uv run careerlab origin set secciones.
- Escribe en ~/careerlab-data/huawei-secciones/quota_cap.json (la carpeta de datos del origen secciones): {"max_five_hour": 0.65, "weekly_pace": {"knots": [[1793030400, 0.10], [1793102400, 0.32], [1793145600, 0.42], [1793404800, 0.75], [1793577600, 0.90]]}}. Así no pasas del 32 % de la semana a las 12:00 UTC de hoy y dejas margen al resto de chats. Si el freno te para, espera; nunca lo esquives.
- uv run careerlab doctor y uv run pytest -q.

2. LEE (en este orden; no imprimas archivos enteros, resúmelos con scripts)
- ESTADO.md
- research/careerlab/plan-maestro-secciones-2026-10-26.md (secciones, planes, protocolo)
- lab/reports/ingenieria-inversa/README.md y hallazgos.md (lo más importante)
- research/careerlab/estrategia-primeros-principios-2026-10-26.md
- lab/fastloop/lessons.md
- lab/reports/matteo-promotion-study.md

Lo esencial que ya sabemos:
- La nota final sigue una fórmula fija: 30 % nivel, 20 % dinero, 15 % salud y dignidad, 15 % habilidad, 10 % control de riesgo, 10 % red.
- El ascenso es casi determinista: al EMPEZAR el mes de la evaluación, Skill, Network y Output tienen que estar en el umbral de su nivel, con la dignidad no baja y el riesgo oculto no disparado. Lo que pasa del techo de cada nivel se pierde. Desde L4 el cuello de botella es la Skill.
- Quien llega al mes 24 en L1 es despedido.
- El juego es determinista salvo el sorteo de eventos y las explosiones: cada respuesta tiene siempre el mismo efecto.
- Las respuestas a los eventos deciden la partida (10–40 puntos); el reparto trimestral, 0–4.
- El comentario mensual de RR. HH. mide el riesgo oculto. Mentir, ocultar, culpar o saltarse pasos lo suben, y con riesgo acumulado una revisión formal o una mentira descubierta lo hacen estallar. Dos explosiones acaban la partida.
- Haiku ya elige bien la respuesta en el 81–84 % de los casos, con o sin manual; un manual sólo aporta en la mecánica que el modelo no puede adivinar (tiempos, techos, riesgo acumulado).
- La primera evaluación se pierde casi siempre por un punto de Output o Network cedido el último mes.
- Un bot "perfecto" que usa el catálogo de desarrollo (prohibido en un Skill) saca 68 de media, termina el 92 % y llega a L6 en el 71 %. Los mejores manuales actuales con Haiku sacan unos 55. Ese hueco es tu objetivo.

3. HERRAMIENTA PRIMERO (como mucho 90 minutos)
Añade a careerlab la opción de cortar una partida de Claude en un mes dado (vigila el stream del jugador y páralo al pasar del mes N). Guarda el estado al empezar cada mes de evaluación: nivel, Skill, Network, Output, salud, dignidad, comentario de RR. HH., nota y si ascendió. Una partida cortada no cuenta nunca como terminada ni como eliminada. Pon pruebas.

4. PERIODOS Y MEDIDAS
- P1 meses 1–5: % que asciende en la 1.ª evaluación (partidas cortas de 6 meses).
- P2 meses 6–17: nivel en el mes 18 (cortas de 18 meses; en L3 hace falta un salto grande de Network y Output).
- P3 meses 18–35: L4, donde manda la Skill.
- P4 meses 36–48: cierre de nivel, riesgo, salud y dignidad (partidas completas; se miden las terminadas).
- Riesgo, en todos: explosiones y detonantes.

5. BUCLE POR HIPÓTESIS (una cada vez)
a) Escríbela en 3 líneas: qué cambia, por qué lo pide la mecánica y qué medida debería mover.
b) Pruébala con lo más barato que la conteste:
   - bots (scripts/ingenieria-inversa/, gratis y muy rápidos) si va de repartos, tiempos o techos;
   - el banco de decisiones de Haiku (scripts/ingenieria-inversa/bench_score.py) si va de qué respuesta elige;
   - partidas cortas de Haiku si va de un periodo;
   - partidas completas sólo para P4 y para el manual final.
c) Compara siempre contra una referencia jugada en el mismo lote, intercalada y en las mismas condiciones. Unas 30 partidas cortas por brazo para decidir; con 4 partidas no se decide nada.
d) Si mejora claramente su medida, profundiza con 2–3 mejoras seguidas. Si no, descártala y apunta por qué. Nunca dediques más de una cuarta parte de la noche a una línea que no gana con claridad.
e) Cada 2 horas haz una revisión desde cero: qué has aprendido de la mecánica, qué líneas matar y 2 ideas nuevas muy distintas de lo probado.

6. POR DÓNDE EMPEZAR
- Primero, la línea base del P1: f3-lean-v1 (referencia) frente a bb-mechanics-lean-v1, bb-mechanics-v1 y observed-growth-v7 de Matteo (rama matteo/observed-growth-v7). 30 partidas de 6 meses cada uno. Los 2 mejores, a 15 partidas completas.
- Después, sobre el mejor, las tácticas por periodo: el reparto antes de la evaluación al Output; en los meses previos, el tiempo a la entrega propia; no ceder puntos el último mes; el salto de L3; la Skill desde L4; el cierre.
- Ideas que merecen probarse:
  - check_latest_logs enseña el efecto de cada opción antes de los techos, así que sirve para saber en la partida si una estadística ya está en su techo;
  - no gastar energía en lo que ya está en su techo y pasarla a lo que falta;
  - aprender dentro de la partida que un tipo de respuesta siempre tiene el mismo efecto;
  - cuidar la dignidad para el ascenso;
  - buscar notas A o B tras ascender para ganar dinero;
  - cerrar riesgos, salud y dignidad al final.
- Al final de la noche, junta las tácticas ganadoras en un manual que funcione por periodos, juega 20 partidas completas contra la referencia y pásalo por la rúbrica de calidad de los SKILL.md. Está resumida en research/careerlab/estrategia-primeros-principios-2026-10-26.md, sección 1; el texto completo, en docs/competition-rules.rst del runner oficial, que se instala con sh scripts/setup_official_runner.sh.

7. CUOTA
- Como mucho 4 partidas a la vez (--slots 4). Los bots y las partidas cortas van primero.
- Subagentes sólo para tareas acotadas: Sonnet para analizar o etiquetar; Opus sólo para escribir un manual nuevo cuando la evidencia lo pida (unos 6 en toda la noche como mucho).
- Mantén tu contexto ligero: resúmenes con scripts, nada de volcar archivos grandes.

8. CUMPLIMIENTO (innegociable)
- En los Skills, nada de nombres de eventos, respuestas fijas, meses concretos, umbrales ni fórmulas no publicadas. Cada regla se apoya en algo que el jugador ve: un valor que deja de subir, el comentario de RR. HH., la llegada de una evaluación.
- El conocimiento del catálogo y del bot "perfecto" nunca entra en un Skill.
- Pasa uv run careerlab lint antes de jugar cualquier manual.

9. DOCUMENTA Y COORDINA
- Un informe por hipótesis en lab/reports/secciones/<id>.md.
- Una tabla viva en lab/reports/secciones/resumen-noche.md, con la sección Relevo al final.
- Commit y push a alejandro/lab-secciones al menos cada hora, a nombre de Alejandro Treny Ortega <alejandrotreny100@gmail.com> y sin líneas Co-Authored-By de Claude.
- Si antes de las 16:00 UTC algo gana con claridad, apúntalo en tu línea T18 de ESTADO.md para que el chat de entregas lo pueda usar.
- No toques main ni ramas ajenas, no juntes PR, no uses claves de DeepSeek.
- En cada turno muestra la salida de `date -u` y una línea de progreso.
- Al terminar, abre una PR con todo.
```

## Mensaje 2: el objetivo (después del mensaje 1)

```text
/goal Seguir el plan del laboratorio nocturno por periodos (mensaje anterior) hasta que se cumplan las dos cosas: (1) la última salida de `date -u` mostrada en la conversación indica 27 oct 2026 a las 07:30 UTC o más tarde; (2) se ha mostrado la salida de un `git push` correcto a la rama alejandro/lab-secciones con un commit que contiene lab/reports/secciones/resumen-noche.md. Ese archivo debe tener: una tabla "Mejor estrategia por periodo" (P1–P4) con número de partidas, % ascendidos o nivel alcanzado y nota media con su error estándar frente a la referencia; las hipótesis descartadas con su motivo; el manual compuesto recomendado con su resultado en partidas completas; y un Relevo con los siguientes pasos. Mientras no se cumpla, sigue trabajando: en cada turno muestra `date -u` y una línea de progreso; si el freno de cuota te para, espera sin esquivarlo; no concluyas nada con menos de 20 partidas por brazo.
```
