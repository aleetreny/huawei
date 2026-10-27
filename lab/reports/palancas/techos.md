# Palanca 2. Detectar el techo del nivel y apuntarlo en la nota

**Conclusión:** en el simulador, detectar el techo durante la partida (una subida anunciada que no se mueve) y recordarlo todo el nivel vale **+8,8 puntos** frente a no saber que existe, el 78 % de lo que daría conocer los techos exactos (+11,3). Si se olvida al mes siguiente, sólo quedan +5,6: **apuntarlo en la nota vale unos 3 puntos**.

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

## Límites

- El bot percibe sin error el efecto de cada opción antes de elegir. El modelo real no (HALLAZGOS A6), y además tiene que notar que la subida no se registró. Eso lo mide el banco con Haiku: [nota-memoria.md](nota-memoria.md).
- El techo de Health y Dignity (10) está publicado en el manual y el bot ya lo usa; aquí sólo se miden los techos no publicados de Skill, Network y Output.

## Cómo repetirlo

```bash
python3 scripts/palancas/sim.py caps --games 4000 --json ~/careerlab-data/palancas/caps-4k.json
python3 scripts/palancas/sim.py caps-noisy --games 4000
```
