# Palanca 4. Llegar a la evaluación con la Dignity alta y el riesgo bajo

**Conclusión:** en el simulador preparar la evaluación para evitar la charla de aviso vale **+0,1 puntos con la regla exacta y −0,5 con la regla general**. No pasa al banco.

27 oct 2026, 17:15 UTC. Simulador, sin cuota. Código: [`scripts/palancas/sim.py`](../../../scripts/palancas/sim.py) (`rep`).

## Qué se compara

En el último trimestre antes de cada evaluación (el reparto del mes 3 del semestre y las historias de los meses 4 y 5):

| Brazo | Qué hace |
|---|---|
| `base` | Bot de reglas generales |
| `general` | Regla sin números: si la Dignity no está al máximo o el comentario de RR. HH. no es el amable, la energía va primero a Defuse y Mental recovery, y en las historias pesa más la Dignity y menos el riesgo |
| `exact` | Igual, pero sólo cuando la regla exacta de M24 (4·Dignity + Health frente a 22 + 8·riesgo + 16·explosiones, con margen) predice charla de aviso |

## Resultados (4.000 partidas emparejadas por brazo)

| Jugador | Brazo | Nota | Diferencia | Despedido en L1 | Crisis |
|---|---|---:|---:|---:|---:|
| Bot de reglas | `base` | 67,91 | — | 6,3 % | 4,1 % |
| | `general` | 67,45 | −0,46 ± 0,17 | 7,7 % | 2,8 % |
| | `exact` | 67,98 | +0,07 ± 0,06 | 6,5 % | 3,5 % |
| Con ruido (30 % al azar) | `base` | 35,78 | — | 15,1 % | 50,2 % |
| | `general` | 36,11 | +0,33 ± 0,20 | 18,1 % | 45,8 % |
| | `exact` | 36,00 | +0,22 ± 0,12 | 16,3 % | 47,8 % |

## Lectura

1. **La charla de aviso es rara y barata.** Sólo puede salir con nota C o D. Con el bot de reglas hay 0,17 por partida, casi todas con D en L1, que siempre trae aviso y no se arregla con reputación. Cuesta Health −1, Dignity −2 y riesgo +1.
2. **La regla general cuesta más de lo que ahorra:** gasta trimestres en recuperar Dignity justo cuando hacen falta para el ascenso (los despidos en L1 suben del 6,3 % al 7,7 %). Baja algo las crisis porque frena el riesgo, pero eso ya lo hace la regla del comentario de RR. HH.
3. Lo útil de M24 ya está en otras reglas: tener el riesgo bajo (regla de RR. HH.) y no dejar caer la Dignity (regla de salud y dignidad de `t13-final`).

**Réplica corregida.** Repetido a las 17:45 UTC con la réplica de `main`, que liquida el mes 48 al terminar (HALLAZGOS B16): las diferencias cambian 0,12 puntos o menos y las conclusiones no cambian. Datos en `~/careerlab-data/palancas/*-4k-v2.json`.

## Cómo repetirlo

```bash
python3 scripts/palancas/sim.py rep --games 4000
```
