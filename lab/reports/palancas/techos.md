# Palanca 2. Detectar el techo del nivel y apuntarlo en la nota

**Conclusión:** en el simulador, detectar el techo durante la partida (una subida anunciada que no se mueve) y recordarlo todo el nivel vale **+8,8 puntos** frente a no saber que existe, el 78 % de lo que daría conocer los techos exactos (+11,3). Si se olvida al mes siguiente, sólo quedan +5,6: **apuntarlo en la nota vale unos 3 puntos**. En el banco, Haiku con la línea de estado lo detecta el 59 % de las veces y lo arrastra y respeta casi siempre; con esa detección, el simulador da **+4,9**.

27 oct 2026, 17:00–17:20 UTC. Simulador `replica.py` con el catálogo v2, sin cuota. Código: [`scripts/palancas/sim.py`](../../../scripts/palancas/sim.py) (`caps` y `caps-noisy`). Datos por partida: `~/careerlab-data/palancas/caps-4k.json`.

## Qué se compara

El jugador es el bot de reglas generales (`rules.RuleBot`, 68 en el simulador). Ve el efecto de cada opción, el signo del riesgo y el comentario de RR. HH., como un agente que percibe bien. Lo único que cambia entre brazos es lo que sabe de los techos:

| Brazo | Qué sabe del techo de Skill, Network y Output |
|---|---|
| `blind` | Nada: cree que no hay techo (el manual dice “0–unbounded”) |
| `detect` | Lo descubre cuando una subida anunciada no se mueve entera, y lo recuerda hasta ascender (como si lo apuntara en la nota) |
| `detect-3m` | Igual, pero lo olvida a los 3 meses |
| `detect-1m` | Igual, pero lo olvida al mes siguiente (sin nota) |
| `fixed-dev` | Cree los techos de desarrollo aunque el juego los cambie (lo que pasaría si se los diéramos como números, que además está prohibido) |
| `exact` | Los techos reales del juego en el que juega |

Mismas 4.000 semillas en todos los brazos; diferencia emparejada partida a partida, ± error típico.

## Resultados

| Escenario | `blind` | `detect` | `detect-3m` | `detect-1m` | `fixed-dev` | `exact` |
|---|---:|---:|---:|---:|---:|---:|
| Juego de desarrollo | 56,6 | **+8,8 ± 0,3** | +8,7 | +5,6 | +11,3 | +11,3 |
| Techos +20 % | 66,2 | **+5,1 ± 0,2** | +4,9 | +3,1 | +8,1 | +7,3 |
| Techos −10 % | 49,3 | **+10,3 ± 0,3** | +10,3 | +6,7 | +7,4 | +12,4 |
| Umbrales −10 % | 59,9 | **+8,5 ± 0,3** | +8,4 | +5,6 | +11,3 | +11,3 |
| Jugador con ruido (30 % de historias al azar) | 27,4 | **+5,7 ± 0,3** | | +2,9 | | +8,4 |

Qué cambia, en el juego de desarrollo:

| | `blind` | `detect` | `exact` |
|---|---:|---:|---:|
| Despedido en L1 | 14,8 % | 7,5 % | 6,3 % |
| Crisis de confianza | 9,8 % | 6,1 % | 4,1 % |
| Charlas de aviso por partida | 0,55 | 0,21 | 0,17 |
| Llega a L6 | 12 % | 43 % | 51 % |

## Lectura

1. **La palanca es grande y aguanta si cambian los parámetros:** +5 a +10 en todos los escenarios. Sirve por dos vías:
   - **en L1 el umbral coincide con el techo**, así que ver que un indicador ya no sube es ver que ya cumple: el jugador deja de gastar en él y empuja el que falta (los despidos en L1 bajan a la mitad);
   - **una subida por encima del techo no vale nada, pero su riesgo sí cuenta**: el jugador que no lo sabe acepta opciones arriesgadas por puntos que se pierden (las crisis bajan de 9,8 % a 6,1 %).
2. **La memoria es la mitad del valor de la nota.** Recordarlo tres meses o todo el nivel da lo mismo; olvidarlo al mes siguiente pierde ~3 puntos. Es la razón para escribirlo en la nota (`Cap seen: Network at L1`), que sobrevive a los resúmenes del contexto.
3. **Dar los números sería peor además de prohibido.** Con los techos un 10 % más bajos, el bot que cree los de desarrollo (`fixed-dev`) saca 56,7 y el que los detecta 59,6. Detectarlos se adapta solo.
4. Con un jugador que elige peor (30 % al azar) la palanca sigue valiendo +5,7.

## Detectar sólo en el reparto, y no siempre

El efecto anunciado de una historia sólo se ve en el registro (`take_action` devuelve sólo `success`). En el reparto trimestral, en cambio, el menú enseña los `status_updates` antes de elegir y el panel siguiente dice si se aplicaron. Por eso la versión barata detecta sólo ahí:

| Brazo | Juego de desarrollo | Techos +20 % | Techos −10 % |
|---|---:|---:|---:|
| `detect` (en todas las decisiones) | +8,8 | +5,1 | +10,3 |
| `detect-q` (sólo en el reparto) | +7,0 | +4,0 | +8,5 |
| `detect-q-60` (sólo en el reparto, y lo nota el 60 % de las veces, como Haiku en el banco) | **+4,9 ± 0,3** | +3,3 | +6,4 |

## En el banco con Haiku

27 oct, 17:15–17:30 UTC. 132 situaciones reales del reparto trimestral (lotes `v02-validation` y `b00-random-safe`), servidas como el primer turno de una sesión nueva (mensaje oficial de continuación). La única memoria es el registro, con las notas anteriores escritas en el estilo de cada manual. Tres tipos de situación:
- `detect`: la acción anterior anunciaba subir un indicador que no se movió, y ninguna nota lo dice aún;
- `carry`: el techo salió antes en este nivel y la última nota ya lo apunta;
- `nocap`: no hay techo (para ver si hay falsas alarmas).

Manuales: `t13-final` (control) y [`t16b-expect`](../../policies-src/palancas/t16b-expect/), que es t13-final más la línea de estado `Review in N | Now S N O | Caps: … | Expect S N O`. Código: [`scripts/palancas/capbank.py`](../../../scripts/palancas/capbank.py).

| Manual | Tipo | n | Apunta el techo bien | Falsa alarma | Gasta en un techo ya visto | Gasta en cualquier techo | Pérdida de nota | Tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| t13-final | detect | 49 | — | — | 16 % | 31 % | 0,20 | 32k |
| t16b-expect | detect | 49 | **59 %** | 14 % | 14 % | 29 % | 0,20 | 32k |
| t13-final | carry | 33 | — | — | 27 % | 39 % | 0,35 | 32k |
| t16b-expect | carry | 33 | **100 %** | 9 % | **3 %** | 42 % | 0,34 | 32k |
| t13-final | nocap | 50 | — | — | 0 % | 0 % | 0,40 | 32k |
| t16b-expect | nocap | 50 | 100 % (escribe `none`) | 0 % | 0 % | 0 % | 0,36 | 33k |
| t18-status (`Stalled`) | detect | 49 | 49 % | 14 % | 16 % | 33 % | 0,20 | 36k |
| t18-status | carry | 33 | 97 % | 12 % | 6 % | 42 % | 0,36 | 35k |
| t18-status | nocap | 50 | 98 % | 2 % | 0 % | 0 % | 0,34 | 35k |

(Pérdida de nota = puntos de nota final perdidos frente a la mejor opción, según el simulador con el planificador. Por decisión es pequeña: la ventaja de la palanca se acumula en la partida.)

**Lectura:**
1. **La nota funciona como memoria.** Un techo apuntado se arrastra el 100 % de las veces tras un resumen y se obedece: el gasto en ese indicador baja del 27 % al 3 %.
2. **Descubrirlo es lo difícil.** La primera redacción (`t16-caps`, “compara con `Now` de tu última nota”) sólo lo detectaba el 16 % de las veces (19 casos). Escribir en la nota lo que se espera tras la acción (`Expect`) y comparar un solo número lo sube al 59 %. Aun así, tras detectarlo, Haiku a veces gasta en él en la misma decisión (14 % frente a 16 %).
3. **Lo que queda de gasto en techos son techos aún no descubiertos** (por ejemplo, Skill en L1 cuando ninguna acción la ha topado todavía). Es lo mismo que supone el simulador en `detect`.
4. **No cuesta tokens:** 32k por situación en los dos manuales.
5. Con lo medido (60 % de detección, sólo en el reparto), el simulador da **+4,9 puntos** a la palanca.
6. **Llamarlo `Stalled` en vez de `Caps`** (para no afirmar una mecánica oculta, ver [nota-memoria.md](nota-memoria.md)) funciona casi igual: detecta el 49 % (59 % con `Caps`; con 49 casos, la diferencia cabe en el ruido), arrastra el 97 % y gasta en un techo apuntado el 6 %.

## Límites

- El bot del simulador percibe sin error el efecto de cada opción antes de elegir; el modelo real no (HALLAZGOS A6). El banco mide la detección y la memoria del techo, no la percepción de las historias.
- El banco de techos sólo prueba decisiones del reparto. Que la regla no estropee las historias se mide en el bloque general ([nota-memoria.md](nota-memoria.md)).
- El techo de Health y Dignity (10) está publicado en el manual y el bot ya lo usa; aquí sólo se miden los techos no publicados de Skill, Network y Output.
- Ningún número de techo va al manual: el ejemplo de la nota usa valores que no son el techo de ningún nivel.

**Réplica corregida.** Repetido a las 17:45 UTC con la réplica de `main`, que liquida el mes 48 al terminar (HALLAZGOS B16): las diferencias cambian 0,12 puntos o menos y las conclusiones no cambian. Datos en `~/careerlab-data/palancas/*-4k-v2.json`.

## Cómo repetirlo

```bash
python3 scripts/palancas/sim.py caps --games 4000 --json ~/careerlab-data/palancas/caps-4k.json
python3 scripts/palancas/sim.py caps-noisy --games 4000
```
