# Línea Palancas

**Pregunta:** ¿cuánta nota vale cada herramienta o pista del juego que todavía no explotamos, y cómo se consigue que la IA la use?

Rama `alejandro/palancas`, código en [`scripts/palancas/`](../../../scripts/palancas/), manuales en [`lab/policies-src/palancas/`](../../policies-src/palancas/). Prompt de la línea: [prompt-palancas.md](../transmision/prompt-palancas.md). Primero el simulador (sin cuota), después el banco con Haiku, y partidas sólo con permiso de Alejandro (no se ha jugado ninguna).

## Conclusiones (27 oct, 18:00 UTC)

1. **La palanca buena es la nota como memoria, con una línea de estado fija** (`Review in N | Now S N O | Stalled | Risky this month`, y `Expect` en el reparto). Haiku la rellena bien el 100 % de las veces, la recupera tras un resumen, obedece lo que apunta y no tiñe las historias. Manual candidato: [`t18-status`](../../policies-src/palancas/t18-status/), que es `t13-final` más la línea ([nota-memoria.md](nota-memoria.md)).
2. **Lo que más vale apuntar es el techo del nivel**, descubierto en la partida cuando una subida anunciada no se mueve, nunca dado como número. En el simulador vale +8,8 puntos, y +4,9 con la detección que consigue Haiku (59 %). Haiku lo arrastra el 100 % de las veces y deja de gastar en él (del 27 % al 3 %) ([techos.md](techos.md)).
3. **Contar las respuestas arriesgadas dentro del mes** vale +4,3 en el simulador para un jugador que se arriesga. Haiku apunta el contador, pero sólo reconoce el 19 % de sus respuestas arriesgadas, así que no cambia nada medible. Se deja porque no estorba; con DeepSeek está por medir ([riesgo.md](riesgo.md)).
4. **No valen la pena:** reaccionar a los avisos con 3 meses de margen (0 puntos; [avisos.md](avisos.md)), preparar la reputación antes de la evaluación (+0,1 o −0,5; [reputacion.md](reputacion.md)) ni las cifras de riesgo del reparto como contador (+0,4).
5. **Tokens:** valen como mucho +0,7 de nota final, y la línea de estado no añade tokens medibles ([tokens.md](tokens.md)).
6. **No se puede confirmar con partidas a un coste razonable:** para ver +3 a +5 puntos con Haiku harían falta 180–500 partidas por brazo. La decisión se apoya en el simulador y en el banco.

## Tabla de palancas

| # | Palanca | Valor en el simulador | Banco con Haiku | Informe |
|---|---|---|---|---|
| 1 | Nota como memoria (línea de estado) | +14,3 ± 0,3 (bot de reglas), +6,2 ± 0,2 (con ruido) | se rellena 100 %; vuelve tras un resumen 100 %; huella 86–88 % igual al control (`t13-final` 81 %) | [nota-memoria.md](nota-memoria.md) |
| 2 | Techo del nivel, detectado y apuntado | +8,8 ± 0,3; **+4,9** con la detección de Haiku | detecta 59 % (16 % sin `Expect`); arrastra 100 %; gasto en techo apuntado 27 % → 3 % | [techos.md](techos.md) |
| 3 | Avisos con 3 meses de margen | −0,00 ± 0,02 | no pasa | [avisos.md](avisos.md) |
| 4 | Reputación antes de la evaluación | +0,07 ± 0,06 (exacta), −0,46 ± 0,17 (general) | no pasa | [reputacion.md](reputacion.md) |
| 5 | Riesgo en cifras del reparto | +0,4; contar el signo de lo elegido, +4,3 | apunta el contador siempre, pero reconoce sólo el 19 % de sus respuestas arriesgadas; sin efecto medible | [riesgo.md](riesgo.md) |
| 6 | Tokens por mes | máximo +0,7 de nota final | 32k por situación con y sin línea | [tokens.md](tokens.md) |

**Cómo se mide.**
- El bot base es el de las 7 reglas generales ([motor M22](../ingenieria-inversa/motor-exacto.md)), y cada palanca es una opción suya en [`scripts/palancas/sim.py`](../../../scripts/palancas/sim.py). Mismas semillas en todos los brazos; diferencias emparejadas, ± error típico.
- Para enseñar los techos al bot se añadió a `rules.RuleBot` un método `cap()`, que no cambia su juego (misma nota con la misma semilla).
- El banco de techos ([`capbank.py`](../../../scripts/palancas/capbank.py)) sirve 132 situaciones reales del reparto como primer turno de una sesión nueva.
- El bloque general y el conjunto de reglas A son los de la línea Transmisión, con sus respuestas guardadas de control, control repetido y `t13-final`.

## Manuales de esta línea

| Manual | Qué añade a `t13-final` | Estado |
|---|---|---|
| `t16-caps` | Línea `Review in N \| Now S N O \| Caps`; techo por comparación con `Now` | superado: detecta el 16 % |
| `t16b-expect` | Más `Expect` en el reparto | detecta el 59 %, arrastra el 100 %; huella 86 % |
| `t16c-feedback` | `t16b` con el techo redactado como señal de la partida | rúbrica 64,7 (igual); no se probó en el banco |
| `t17b-status` | `t16b` más `Risky this month` | huella 88 %; pérdida 0,65 frente a 1,01 de `t13-final` |
| **`t18-status`** | `t17b` con `Stalled` en lugar de `Caps` (no afirma ninguna mecánica oculta) | **candidato** |

## Relevo

**27 oct, 18:00 UTC.**
1. **Hecho.**
   - Rama, carpeta y fila en ESTADO.md.
   - Palancas 2 a 5 en el simulador (4.000 partidas emparejadas por brazo y escenario).
   - Banco de techos (132 situaciones) con `t13-final`, `t16`, `t16b` y `t18`; bloque general (139) con `t16b`, `t17b` y `t18`; reglas A (385) con `t16b`; rúbrica de `t13-final`, `t16b`, `t16c` y `t18`.
   - HALLAZGOS: B15, B16, C5, C6 y tres filas de X.
2. **Resultados.** Tablas de arriba y de cada informe.
   - Datos (fuera de Git, con texto del juego): `~/careerlab-data/palancas/`, con las partidas del simulador `*-4k.json`, el banco de techos `caps-bank.jsonl` e `items-caps-*.jsonl`, y las respuestas de Haiku en `bench/runs/<brazo>/`.
   - Cuota: unas 1.300 sesiones cortas de Haiku y 12 lecturas de Sonnet; la ventana de 5 horas iba por el 3 % y la semana por el 36 % (18:00 UTC).
3. **A medias o con cuidado.**
   - No se ha jugado ninguna partida con `t18-status`.
   - **Trampa del arnés:** `scripts/transmision/select.py` tapa el módulo `select` de Python, y `bank.py` y `runbench.py` fallan al importar `multiprocessing` o `asyncio`. Hay que lanzarlos con `python -I`, como abajo.
4. **Siguiente.**
   - Proponer a la línea DeepSeek medir `t18-status` frente a `t13-final` en el banco de techos y en el bloque general: si DeepSeek detecta el techo, y sus tokens por mes.
   - Si Alejandro lo aprueba, unas 10 partidas de Haiku con `t18-status` sólo para comprobar que nada se rompe.

```bash
export BB_DATA=$PWD/lab/data/ingenieria-inversa TRANSMISION_DATA=~/careerlab-data/palancas/bench CAREERLAB_CLAUDE_EXE=~/.local/bin/claude
python3 scripts/palancas/sim.py caps --games 4000            # también warn, rep, risk, notes, caps-noisy
python3 -I scripts/transmision/bank.py extract --batches v02-validation --max-games 150 --out ~/careerlab-data/palancas/sit-v02.jsonl
python3 -I scripts/palancas/capbank.py build --sit ~/careerlab-data/palancas/sit-v02.jsonl,~/careerlab-data/palancas/sit-b00.jsonl --out ~/careerlab-data/palancas/caps-bank.jsonl --rollouts 16
python3 -I scripts/palancas/capbank.py serve --bank ~/careerlab-data/palancas/caps-bank.jsonl
uv run python -I scripts/transmision/runbench.py run --items ~/careerlab-data/palancas/items-caps-stalled.jsonl --variant lab/policies-src/palancas/t18-status/bundle --name caps-t18 --slots 6
python3 -I scripts/palancas/capbank.py score --bank ~/careerlab-data/palancas/caps-bank.jsonl --arms caps-t13,caps-t16b,caps-t18
python3 -I scripts/transmision/fingerprint.py --items ~/careerlab-data/palancas/bench/items-g1.jsonl --arms control,control-b,t13-final,g1-t18-status
python3 -I scripts/palancas/notecheck.py --items ~/careerlab-data/palancas/bench/items.jsonl --arms g1-t18-status
```
