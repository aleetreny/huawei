# Palanca 5. El riesgo en cifras y el contador de respuestas arriesgadas

**Conclusión:** en el simulador, usar las cifras de riesgo del reparto trimestral como contador vale sólo **+0,4 puntos**. Lo que vale es **contar las respuestas arriesgadas elegidas desde el último comentario de RR. HH.**: +4,3 puntos frente a fiarse sólo del comentario de principio de mes.

27 oct 2026, 17:15 UTC. Simulador, sin cuota. Código: [`scripts/palancas/sim.py`](../../../scripts/palancas/sim.py) (`risk`).

## Qué se compara

El comentario de RR. HH. sale una vez al mes y muestra el riesgo oculto (0 a 4, M10). Dentro del mes, las respuestas lo cambian sin decirlo. Del reparto trimestral sí se ve la cifra (`HiddenRisk +1` en High-intensity work, `−1` en Defuse).

| Brazo | Qué sabe del riesgo al decidir |
|---|---|
| `live` | El riesgo exacto en cada momento (lo que usa el bot de reglas; ideal) |
| `stale` | Sólo el comentario del principio del mes |
| `quarter` | El comentario, más las cifras del reparto que él mismo elige |
| `sign` | El comentario, más el signo de cada respuesta que elige (+1 si es arriesgada, −1 si es prudente) |
| `sign+quarter` | Las dos cosas |

## Resultados (4.000 partidas emparejadas por brazo)

| Brazo | Nota | Diferencia con `live` | Crisis de confianza | L6 |
|---|---:|---:|---:|---:|
| `live` | 67,91 | — | 4,1 % | 51 % |
| `stale` | 62,37 | −5,54 ± 0,22 | 16,9 % | 38 % |
| `quarter` | 62,79 | −5,12 ± 0,22 | 16,9 % | 43 % |
| `sign` | 66,66 | −1,26 ± 0,14 | 6,6 % | 48 % |
| `sign+quarter` | 66,83 | −1,08 ± 0,13 | 7,1 % | 52 % |

## Lectura

1. **Las cifras del reparto ayudan poco** (+0,4) porque el reparto es lo último del mes: al mes siguiente el comentario de RR. HH. ya da el riesgo al día.
2. **El peligro está dentro del mes.** Un jugador que sólo mira el comentario encadena dos o tres respuestas arriesgadas en el mismo mes y explota: las crisis pasan del 4 % al 17 %. Llevar la cuenta del signo de lo elegido recupera casi todo (+4,3).
3. Por eso la línea de estado de la nota lleva `Risk: k risky since HR remark` ([nota-memoria.md](nota-memoria.md)). Exige que el modelo reconozca qué opción es arriesgada, que es justo lo que mide la línea DeepSeek; las categorías de respuesta lo aciertan un 78 % (HALLAZGOS B7).
4. Ojo con el tamaño: el bot sin contador se arriesga más que Haiku, que ya evita casi siempre los detonantes (HALLAZGOS B9). Con Haiku la ganancia real será menor.

## En el banco con Haiku

27 oct, 17:30–17:45 UTC. Manual `t17b-status` (línea de estado con `Risky this month`) en el bloque general: 139 historias jugadas desde el principio del mes, 277 notas. Cada historia elegida en los pasos previos del mes se busca en el catálogo por título y opciones, y se mira el riesgo oculto real de la respuesta elegida ([`scripts/palancas/riskcount.py`](../../../scripts/palancas/riskcount.py)).

| | |
|---|---:|
| Notas en las que el mes ya lleva alguna respuesta arriesgada | 8 % (21) |
| … y Haiku lo apunta | **19 %** (4 de 21) |
| Falsas alarmas (lo apunta sin respuesta arriesgada) | 1 % |
| Número exacto | 93 % (casi siempre por los ceros) |

**Lectura:** el contador se apunta bien de forma (siempre está en la nota), pero Haiku no reconoce cuándo una de sus respuestas era arriesgada. Es el cuello de botella de percepción de HALLAZGOS A6: el contador sólo vale lo que valga esa percepción. En el bloque general no estorba (huella 88 % igual al control) y baja un poco el riesgo medio elegido, dentro del ruido. Para DeepSeek hay que medir primero si reconoce las respuestas arriesgadas (línea DeepSeek).

## Cómo repetirlo

```bash
python3 scripts/palancas/sim.py risk --games 4000
```
