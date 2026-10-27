# Línea Palancas

**Pregunta:** ¿cuánta nota vale cada herramienta o pista del juego que todavía no explotamos, y cómo se consigue que la IA la use?

Rama `alejandro/palancas`, código en [`scripts/palancas/`](../../../scripts/palancas/), manuales en [`lab/policies-src/palancas/`](../../policies-src/palancas/). Prompt de la línea: [prompt-palancas.md](../transmision/prompt-palancas.md). Primero el simulador (sin cuota), después el banco con Haiku, y partidas sólo con permiso de Alejandro (no se ha jugado ninguna).

## Conclusiones (27 oct, 18:10 UTC)

1. **La palanca buena es la nota como memoria, con una línea de estado fija** (`Review in N | Now S N O | Stalled | Risky this month`, y `Expect` en el reparto). Haiku la rellena bien el 100 % de las veces (99 % con 18 decisiones de historial), la recupera tras un resumen, obedece lo que apunta, no tiñe las historias y no rompe las reglas del reparto. Manual candidato: [`t19-final`](../../policies-src/palancas/t19-final/), que es `t13-final` más la línea ([nota-memoria.md](nota-memoria.md)).
2. **Lo que más vale apuntar es el techo del nivel**, descubierto en la partida cuando una subida anunciada no se mueve, nunca dado como número. En el simulador vale +8,8 puntos, y +4,9 con la detección que consigue Haiku (49–63 %). Haiku lo arrastra el 97–100 % de las veces y deja de gastar en él (del 27 % al 3–9 %) ([techos.md](techos.md)).
3. **Contar las respuestas arriesgadas dentro del mes** vale +4,3 en el simulador para un jugador que se arriesga. Haiku apunta el contador, pero sólo reconoce el 19 % de sus respuestas arriesgadas, así que no cambia nada medible. Se deja porque no estorba; con DeepSeek está por medir ([riesgo.md](riesgo.md)).
4. **No valen la pena:** reaccionar a los avisos con 3 meses de margen (0 puntos; [avisos.md](avisos.md)), preparar la reputación antes de la evaluación (+0,1 o −0,5; [reputacion.md](reputacion.md)) ni las cifras de riesgo del reparto como contador (+0,4).
5. **Tokens:** valen como mucho +0,7 de nota final, y la línea de estado no añade tokens medibles ([tokens.md](tokens.md)).
6. **No se puede confirmar con partidas a un coste razonable:** para ver +3 a +5 puntos con Haiku harían falta 180–500 partidas por brazo. La decisión se apoya en el simulador y en el banco.
7. **Riesgo que tiene que aceptar Alejandro:** el revisor de la rúbrica no baja la nota (65,3 `t13-final`, 66,7 `t19-final`), pero lee el mecanismo `Stalled` como algo “sacado de las partidas de desarrollo”. El Skill no da ningún número ni afirma ningún techo; sólo dice qué hacer si una subida anunciada no aparece, que es estrategia basada en lo que devuelve la partida.

## Tabla de palancas

| # | Palanca | Valor en el simulador | Banco con Haiku | Informe |
|---|---|---|---|---|
| 1 | Nota como memoria (línea de estado) | +14,4 ± 0,3 (bot de reglas), +6,2 ± 0,2 (con ruido) | se rellena 100 %; vuelve tras un resumen 97–100 %; huella 86–89 % igual al control (`t13-final` 81–85 %) | [nota-memoria.md](nota-memoria.md) |
| 2 | Techo del nivel, detectado y apuntado | +8,8 ± 0,3; **+4,9** con la detección de Haiku | detecta 49–63 % (16 % sin `Expect`); arrastra 97–100 %; gasto en techo apuntado 27 % → 3–9 % | [techos.md](techos.md) |
| 3 | Avisos con 3 meses de margen | −0,00 ± 0,02 | no pasa | [avisos.md](avisos.md) |
| 4 | Reputación antes de la evaluación | +0,07 ± 0,06 (exacta), −0,46 ± 0,17 (general) | no pasa | [reputacion.md](reputacion.md) |
| 5 | Riesgo en cifras del reparto | +0,4; contar el signo de lo elegido, +4,3 | apunta el contador siempre, pero reconoce sólo el 19 % de sus respuestas arriesgadas; sin efecto medible | [riesgo.md](riesgo.md) |
| 6 | Tokens por mes | máximo +0,7 de nota final | 63–66k por mes jugado con y sin línea; ~1 M con 18 decisiones de historial, igual que `t13-final` | [tokens.md](tokens.md) |

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
| `t16c-feedback` | `t16b` con el techo redactado como señal de la partida | sólo rúbrica (64,7); no se probó en el banco |
| `t17b-status` | `t16b` más `Risky this month` | huella 88 %; pérdida 0,65 frente a 1,01 de `t13-final` |
| `t18-status` | `t17b` con `Stalled` en lugar de `Caps` (no afirma ninguna mecánica oculta) | detecta 49 %; en L4 compara los números de `Now` entre sí |
| **`t19-final`** | `t18` + “`Now` no es una clasificación” + cambio a Output en L4 sólo si la evaluación lo pide | **candidato**: detecta 63 %, arrastra 97 %, huella 89 %, reglas del reparto como `t13-final`, contexto largo 99 %, rúbrica 66,7 |

## Relevo

**27 oct, 18:10 UTC.**
1. **Hecho, y por qué.**
   - Rama, carpeta y fila en ESTADO.md. Juntado `origin/main` (con la réplica corregida); 313 tests en verde.
   - Palancas 2 a 5 en el simulador, primero porque es gratis: 4.000 partidas emparejadas por brazo y escenario, repetidas con la réplica corregida.
   - Las dos que pasaban de 1 punto (techos y contador de riesgo) se juntaron en una línea de estado, y se llevaron al banco con Haiku:
     - banco de techos nuevo: 132 situaciones del reparto servidas tras un resumen;
     - bloque general (139), para la huella;
     - reglas del reparto (conjunto A);
     - contexto largo (30 historias con 18 decisiones previas);
     - comprobador de notas y del contador de riesgo;
     - rúbrica.
   - Seis redacciones, hasta `t19-final`.
   - HALLAZGOS: B22, B23, C9, C10 y tres filas de X. Propuesta para la línea DeepSeek: [propuesta-deepseek.md](propuesta-deepseek.md).
2. **Resultados.** Tablas de arriba y de cada informe.
   - Datos (fuera de Git, con texto del juego), en `~/careerlab-data/palancas/`:
     - partidas del simulador: `*-4k.json` y `*-4k-v2.json` (réplica corregida);
     - banco de techos: `caps-bank.jsonl` e `items-caps-*.jsonl`;
     - situaciones de contexto largo: `items-long.jsonl`;
     - respuestas de Haiku, con el `record.jsonl` de cada situación: `bench/runs/<brazo>/`;
     - rúbricas: `rubric-*.json`.
   - Cuota: ~1.900 sesiones de Haiku (casi todas cortas) y 15 lecturas de Sonnet. A las 18:05 UTC, la ventana de 5 horas iba por el 7 % y la semana por el 37 %. Menos del 2 % de la semana en el día, por debajo del aviso del 5 % de NORMAS §5.
3. **Qué falló o quedó a medias.**
   - No se ha jugado ninguna partida, ni se ha usado DeepSeek.
   - Con Haiku, el contador de riesgo no sirve: no reconoce sus respuestas arriesgadas (0–19 %). Se deja en `t19-final` hasta que DeepSeek diga si a él le sirve.
   - En el banco con pasos previos del reparto, el servidor de imitación no sigue la acción que elige el modelo, y eso provoca falsos `Stalled` (5 de 60 en Skill en L4). Para medir el reparto con varios pasos habría que recalcular el estado tras cada acción del modelo.
   - **Trampa del arnés:** `scripts/transmision/select.py` tapa el módulo `select` de Python, y `bank.py` y `runbench.py` fallan al importar `multiprocessing` o `asyncio`. Hay que lanzarlos con `python -I`, como abajo. Arreglarlo es renombrar ese archivo, que es de la línea Transmisión.
   - El CLI oficial no está en `~/claude-2.1.303/`: se usa `~/.local/bin/claude` (2.1.303) con `CAREERLAB_CLAUDE_EXE`.
4. **Siguiente.**
   - Línea DeepSeek: el banco de techos y el bloque general con `t19-final` (~0,4 USD; [propuesta-deepseek.md](propuesta-deepseek.md)). Decide Alejandro.
   - Si sale bien, añadir la línea de estado al manual del corte: a `t19-final` o, si DeepSeek se queda con `t13-read-v1`, a ése.
   - Con permiso de Alejandro, unas 10 partidas de Haiku con `t19-final` sólo para comprobar que nada se rompe.

```bash
export BB_DATA=$PWD/lab/data/ingenieria-inversa TRANSMISION_DATA=~/careerlab-data/palancas/bench CAREERLAB_CLAUDE_EXE=~/.local/bin/claude
python3 scripts/palancas/sim.py caps --games 4000            # también caps-noisy, warn, rep, risk, notes
python3 -I scripts/transmision/bank.py extract --batches v02-validation --max-games 150 --out ~/careerlab-data/palancas/sit-v02.jsonl
python3 -I scripts/transmision/bank.py extract --batches b00-random-safe --max-games 300 --out ~/careerlab-data/palancas/sit-b00.jsonl
python3 -I scripts/palancas/capbank.py build --sit ~/careerlab-data/palancas/sit-v02.jsonl,~/careerlab-data/palancas/sit-b00.jsonl --out ~/careerlab-data/palancas/caps-bank.jsonl --rollouts 16
python3 -I scripts/palancas/capbank.py serve --bank ~/careerlab-data/palancas/caps-bank.jsonl
uv run python -I scripts/transmision/runbench.py run --items ~/careerlab-data/palancas/items-caps-stalled.jsonl --variant lab/policies-src/palancas/t19-final/bundle --name caps-t19 --slots 6
python3 -I scripts/palancas/capbank.py score --bank ~/careerlab-data/palancas/caps-bank.jsonl --arms caps-t13,caps-t16b,caps-t18,caps-t19
uv run python -I scripts/transmision/runbench.py run --items ~/careerlab-data/palancas/bench/items.jsonl --ids lab/data/transmision/ids-G1.txt --variant lab/policies-src/palancas/t19-final/bundle --name g1-t19-final --slots 6
python3 -I scripts/transmision/fingerprint.py --items ~/careerlab-data/palancas/bench/items-g1.jsonl --arms control,control-b,t13-final,g1-t19-final
python3 -I scripts/palancas/notecheck.py --items ~/careerlab-data/palancas/bench/items.jsonl --arms g1-t19-final
python3 -I scripts/palancas/riskcount.py --items ~/careerlab-data/palancas/bench/items.jsonl --arms g1-t19-final
```

`bench/items.jsonl` es `lab/data/transmision/bank-items.jsonl.gz` descomprimido, y `bench/runs/{control,control-b,t13-final}` salen de `haiku-answers.json.gz` (las respuestas grabadas por Transmisión).
