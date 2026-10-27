# Experimento 1. El banco de obediencia

27 oct 2026. Scripts en `scripts/transmision/`. Los datos llevan texto del juego de desarrollo y se quedan fuera de Git, en `~/careerlab-data/transmision/` (se regeneran con los comandos de abajo).

## Qué es una situación

Un momento real de una partida grabada de bot (lotes de `lab/data/ingenieria-inversa/`: `c02-planner-real`, `v02-validation`, `b01-oracle-eps`, `c01-greedy-real`; 1.633 partidas, 264.002 decisiones):

- **Lo que ve el jugador:** la respuesta exacta de `observe` en ese paso (mismo formato JSON que el juego, comprobado contra el servidor real) y las entradas del registro oficial escritas hasta entonces, para `check_latest_logs`.
- **El estado completo del simulador:** el estado visible y lo oculto, reconstruido igual que `replica.py validate` (riesgo sincronizado con el comentario de RR. HH., intervalo del dinero, historia del Output, contadores de ruina, aislamiento y dignidad).
- **La respuesta correcta:** para cada opción, la nota final media en el simulador si se elige esa opción y el planificador ajustado (`search_top.json`, el que saca 70,5 en el juego real) juega el resto de la carrera. 32 partidas simuladas por opción, con los mismos números aleatorios para todas las opciones (así la diferencia entre opciones tiene poco ruido).

## Qué regla prueba cada situación

| Regla | Situaciones candidatas | Respuesta correcta |
|---|---|---|
| `pre_review`: no ceder puntos antes de la evaluación | decisión de historia en el mes previo a una evaluación, L1–L3, con alguna opción que baja Skill, Network u Output estando en el umbral o cerca | la mejor según el simulador (a 0,5 puntos o menos de la mejor) |
| `skill_l4`: Skill en L4 | reparto trimestral (energía o acción principal) en L4–L5, riesgo bajo | Skill learning (o Health recovery si la salud ya no aguanta) y Apply for rotation |
| `hr_risk`: reaccionar al comentario de RR. HH. | reparto trimestral con el riesgo oculto en 2 o más (comentario con el ceño fruncido o peor) | Defuse legacy risk y Lay low and reduce risk |
| `trigger`: evitar detonantes | decisión de historia con riesgo 2 o más y alguna opción que lo lleva a explotar | la mejor según el simulador |
| `early_ruin`: no arruinarse al principio | decisión de historia en L1–L2 con poco dinero y alguna opción que cuesta dinero | la mejor según el simulador |
| `closing`: el cierre | cualquier decisión de los meses 45–48 | la mejor según el simulador (0,15 puntos de margen en el reparto) |

Sólo entran situaciones **decisivas**: la diferencia entre la mejor y la peor opción es de al menos 2 puntos de nota final (0,4 en el reparto del cierre) y no todas las opciones son correctas. Como mucho 8 situaciones por título de evento (32 en `early_ruin`, que tiene pocos títulos), para que ningún evento domine.

**Títulos reservados.** Un 30 % de los títulos (por hash del título) quedan reservados: las formulaciones se eligen con el resto y se comprueban después en esos. Así se imita la evaluación oficial, que usa otros eventos.

## Cómo se pregunta a Haiku

Igual que en una partida oficial (ver [fase 0](fase0-carga-skills.md)):

- Mensaje de sistema: `IDENTITY.md` oficial con la instrucción del manifest y la sección de Skills de JiuwenSwarm (`N. nombre: descripción`). El cuerpo del SKILL.md sólo llega si Haiku llama a `skill_tool`.
- Mensaje de usuario: el mensaje oficial de continuación (“Call check_latest_logs… Call observe… continue”).
- Herramientas: un servidor MCP falso con las 5 herramientas oficiales y sus firmas exactas. Sirve los pasos grabados **desde el principio del mes** de la situación (así Haiku ve el comentario de RR. HH. del mes en el primer `observe`, como en la partida) y anota la elección en la situación objetivo. En la condición **larga**, sirve además las ~18 decisiones anteriores.
- Medidas por brazo y regla: % de respuestas correctas (intervalo de Wilson al 95 %), % de fallos propios de la regla (perder un punto necesario, explotar, gastar dinero, no seguir la acción de la regla), pérdida media de nota frente a la mejor opción (puntos, simulador), % de veces que lee el Skill, % que mira el registro y tokens.

## Comandos

```bash
export BB_DATA=$PWD/lab/data/ingenieria-inversa
D=~/careerlab-data/transmision
python3 scripts/transmision/bank.py extract --batches c02-planner-real,v02-validation,b01-oracle-eps,c01-greedy-real --out $D/sit.jsonl
python3 scripts/transmision/bank.py truth --sit $D/sit.jsonl --out $D/bank-raw.jsonl --rollouts 32 --per-tag 900
python3 scripts/transmision/select.py --raw $D/bank-raw.jsonl --out $D/bank.jsonl --cap 360
uv run python scripts/transmision/runbench.py assemble --bank $D/bank.jsonl --sit $D/sit.jsonl --out $D/items.jsonl
scripts/transmision/drive.sh $D/items.jsonl $D/ids.txt 10 control=control <brazo>=<carpeta bundle> ...
uv run python scripts/transmision/score.py --items $D/items.jsonl --arms control,<brazo> --split dev|holdout --common
```
