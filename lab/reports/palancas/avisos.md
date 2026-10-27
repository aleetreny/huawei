# Palanca 3. Reaccionar a los avisos con 3 meses de margen

**Conclusión:** en el simulador reaccionar a los avisos de dinero, aislamiento y dignidad agotada vale **0 puntos** (−0,00 ± 0,02 con el bot de reglas; +0,02 ± 0,02 con un jugador con ruido), y el aviso de la tercera evaluación en L1 llega cuando ya no se puede hacer nada. No pasa al banco.

27 oct 2026, 17:15 UTC. Simulador, sin cuota. Código: [`scripts/palancas/sim.py`](../../../scripts/palancas/sim.py) (`warn`).

## Qué se compara

| Brazo | Qué hace |
|---|---|
| `base` | Bot de reglas generales, sin regla para los avisos |
| `warning` | En cuanto sale el aviso (tercer mes de la condición, M15), da mucho peso a salir de ella: dinero, Network o Dignity, y Network maintenance o Mental recovery en el trimestre |
| `condition` | Lo mismo, pero desde que la condición se ve en el panel (dinero negativo, Network 0, Dignity 1 o menos) |

Los tres, también con un jugador que elige el 30 % de las historias al azar. 4.000 partidas emparejadas por brazo.

## Resultados

| Jugador | Brazo | Nota | Diferencia | Ruina | Aislado | Agotado |
|---|---|---:|---:|---:|---:|---:|
| Bot de reglas | `base` | 67,91 | — | 0,1 % | 0,0 % | 0,1 % |
| | `warning` | 67,91 | −0,00 ± 0,02 | 0,0 % | 0,0 % | 0,1 % |
| | `condition` | 67,81 | −0,10 ± 0,06 | 0,0 % | 0,0 % | 0,1 % |
| Con ruido | `base` | 35,78 | — | 1,8 % | 0,0 % | 9,4 % |
| | `warning` | 35,80 | +0,02 ± 0,02 | 1,5 % | 0,0 % | 9,4 % |
| | `condition` | 35,53 | −0,25 ± 0,09 | 1,2 % | 0,0 % | 9,6 % |

## Lectura

1. **Las derrotas por condición casi no ocurren** con un jugador que mira el panel: ruina 0,1 %, aislamiento 0 %. Con ruido, la ruina es el 1,8 % y reaccionar la baja al 1,5 %, pero no cambia la nota. Lo que acaba con el jugador con ruido es la crisis de confianza (50 %) y la salud (9 %), no los avisos.
2. **El aviso de la tercera evaluación en L1 no tiene arreglo.** Con 17 meses en L1 la nota es D siempre, y con D no se asciende. Las partidas despedidas se deciden en las evaluaciones de los meses 6 y 12, casi siempre por **un punto de Output o de Network** (en L1 el umbral es el techo). Eso es la palanca 2 ([techos.md](techos.md)), no la 3.
3. Lo que ya dice `t13-final` (“si Network o el dinero están cerca de cero durante meses, arréglalo primero”) basta. Con Haiku hubo 2 ruinas en 43 partidas de f3-lean; si DeepSeek se arruina más, convendrá revisar por qué gasta (multiplicador de pérdidas en niveles altos), no añadir una regla de avisos.

**Réplica corregida.** Repetido a las 17:45 UTC con la réplica de `main`, que liquida el mes 48 al terminar (HALLAZGOS B16): las diferencias cambian 0,12 puntos o menos y las conclusiones no cambian. Datos en `~/careerlab-data/palancas/*-4k-v2.json`.

## Cómo repetirlo

```bash
python3 scripts/palancas/sim.py warn --games 4000
```
