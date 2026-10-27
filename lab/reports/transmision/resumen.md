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
| 4 | [contexto-largo.md](contexto-largo.md) | Las mismas reglas con 18 decisiones de historial antes | hecho: la obediencia no cae; la instrucción del manifest no añade nada |
| 5 | [partidas-g1.md](partidas-g1.md) | `t3-instr` frente a f3-lean-v1, partidas completas, entrega oficial | parado: −21 ± 8 puntos (7 + 7); la regla se salía de su contexto |
| 7 | [bloque-general.md](bloque-general.md) | Huella de las elecciones en historias fuera de las reglas | hecho: toda regla de historias cambia 1 de cada 5 historias |
| 8 | [ronda-8-10.md](ronda-8-10.md) | Sólo reparto trimestral (t8, t9) y una regla de historias tras una cuenta atrás (t10) | hecho |
| 6 | partidas `g2-full` | `t6-scoped-instr` (reglas acotadas) frente a f3-lean-v1, 30 + 30 | en marcha desde las 12:30 UTC |

## Relevo

**27 oct, 13:10 UTC.**
1. **Hecho.** Fase 0 ([fase0-carga-skills.md](fase0-carga-skills.md)); banco de 3.573 situaciones con verdad del simulador ([banco.md](banco.md)); rondas A–3 ([ronda-a.md](ronda-a.md)); partidas g1 paradas ([partidas-g1.md](partidas-g1.md)); bloque general y huella ([bloque-general.md](bloque-general.md)); modo `#official` del actor (`careerlab/actors/claude_cli.py`, lee también `reference/`).
2. **Conclusión de trabajo.** El reparto trimestral se transmite (Skill en L4 17 % → 85 %, cierre 62 % → 93 %, RR. HH. 18 % → 79–85 %); las reglas de historias se transmiten a medias y se cuelan en el resto de historias (1 de cada 5 cambia, con menos Skill y más riesgo), lo que hundió a t3-instr en partidas.
3. **En marcha.** Partidas `g4-full` (t9-quarter frente a f3-lean, 30 + 30; quedan 6 de g3 con t8). Banco: validación final `ids-V2` (control y t9/t8, ≥ 200 situaciones por regla con títulos reservados), t10-countdown (una sola regla de historias tras una cuenta atrás), contexto largo de t3.
4. **Siguiente.** Tabla final con los números de `ids-V2`; partidas de t10 si su huella general queda cerca del control; fase 3 (rúbrica con `scripts/transmision/rubric.py`, t3-instr sacó 60).
5. **Comandos.** `scripts/transmision/drive.sh <items> <ids> <slots> <brazo>=<bundle>`; `uv run python scripts/transmision/score.py --items ~/careerlab-data/transmision/items-final.jsonl --arms control,<brazo> --common`; `uv run python scripts/transmision/fingerprint.py --items ~/careerlab-data/transmision/items-gen.jsonl --arms control,<brazo>`; `uv run python scripts/transmision/games.py --batch g4-full`. Runner: `uv run careerlab run --kind claude-cli --continuous --slots 4 --max-five-hour 0.65 --stop-file ~/careerlab-data/huawei-transmision/STOP` (para pararlo, `touch` de ese archivo).
