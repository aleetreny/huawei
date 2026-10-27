# T20 Transmisión: resumen vivo

Rama `alejandro/transmision` (desde `origin/main`, con `main-1nddsg` y `alejandro/lab-secciones` juntadas), origen de registro `transmision`. Actor: Haiku (`claude-haiku-5-5`) por el CLI 2.1.303.

**El problema.** Ya sabemos qué hay que hacer (el simulador `replica.py` y el planificador, que saca 70,5 en el juego real). No sabemos cómo escribirlo para que un modelo pequeño lo obedezca. Este trabajo mide la obediencia en un banco de situaciones reales y busca la forma de escribir cada regla que más la sube.

## Tabla principal: regla → formulación ganadora → obediencia frente al control

*(en construcción; se rellena al terminar cada experimento)*

| Regla | Formulación ganadora | Situaciones | Acierto control | Acierto ganadora | Con títulos reservados |
|---|---|---:|---:|---:|---|

## Experimentos

| # | Informe | Qué mide | Estado |
|---|---|---|---|
| 0 | [fase0-carga-skills.md](fase0-carga-skills.md) | Cómo llega el Skill al modelo en el programa oficial | hecho |
| 1 | [banco.md](banco.md) | Construcción del banco y verdad del simulador | hecho (1.869 situaciones decisivas) |
| 2 | [ronda-a.md](ronda-a.md) | Rondas A y 2: dónde y cómo escribir cada regla (contexto corto) | hecho |
| 3 | ronda 3 | Prioridad explícita, ejemplos de cómo leer el coste de una opción, instrucción del manifest | en marcha |
| 4 | contexto largo | Las mismas reglas con 18 decisiones de historial antes | en marcha |
| 5 | partidas `g1-full` | `t3-instr` frente a f3-lean-v1, 40 + 40 completas, entrega oficial | en marcha desde las 11:48 UTC |

## Relevo

**27 oct, 11:50 UTC.**
1. Hecho: fase 0 (el programa oficial sólo pone nombre y descripción del Skill en el mensaje de sistema; el cuerpo se lee bajo demanda; la instrucción del manifest va siempre), banco de 1.869 situaciones con la respuesta del simulador, rondas A y 2 (ver [ronda-a.md](ronda-a.md)), modo `#official` en el actor de Haiku (`careerlab/actors/claude_cli.py`).
2. En marcha: ronda 3 del banco y contexto largo (`~/careerlab-data/transmision/drive*.log`), y el lote de partidas `g1-full` (runner de `careerlab run --continuous`, origen `transmision`, tope `quota_cap.json` con el ritmo semanal de ESTADO).
3. Siguiente: elegir por regla la formulación ganadora, validarla con títulos reservados (≥ 200 situaciones por regla) y comparar en partidas.
