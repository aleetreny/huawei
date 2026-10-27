# P4-bots: ¿limpiar el riesgo en el último año sube la nota final? (bots, sin cuota)

**Hipótesis.** En el último año, gastar la energía en Defuse legacy risk (aunque RR. HH. esté tranquilo) y en recuperación baja el riesgo oculto final y sube el control de riesgo, que pesa un 10 % en la nota. Medida: dimensiones finales y nota de las partidas que llegan al último año.

**Diseño.** `scripts/secciones/close_bots.py`, 200 partidas por brazo, intercaladas, 27 oct 01:09–01:18 UTC, datos en `~/careerlab-data/secciones-bots/` (fuera de Git). Bots de energía de T10: historias con la primera opción y acción principal "proyecto clave" (recursos de laboratorio, nunca contenido de un Skill). Los brazos sólo difieren en la energía del último año:
- **base**: Health recovery, Mental recovery y Prepare report materials toda la partida;
- **close**: igual, y en el último año Defuse legacy risk + Health recovery;
- **close-mind**: igual, y en el último año Defuse legacy risk + Mental recovery.

## Resultado

| Brazo | Llegan al último año | Terminan (de ellos) | Q de los que llegan | Q de las terminadas | Control de riesgo | Salud+dignidad | Red | Skill |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | 31 | 25 | 57,0 ± 2,0 | 61,0 ± 1,5 | 67 ± 5 | 94 ± 2 | 68 ± 3 | 84 ± 4 |
| close | 32 | 25 | 57,2 ± 1,7 | 60,2 ± 1,5 | 65 ± 6 | 94 ± 2 | 69 ± 3 | 83 ± 3 |
| close-mind | 24 | 11 | 57,8 ± 1,6 | 64,2 ± 2,0 | 88 ± 6 | 79 ± 4 | 78 ± 5 | 90 ± 6 |

(media ± error estándar; dimensiones normalizadas de 0 a 100)

- **Defuse "por si acaso" en el último año no mueve nada**: ni el control de riesgo final ni la nota. Las crisis de confianza del último año tampoco bajan (7 frente a 4). El riesgo que pesa al final lo crean las respuestas a los eventos, no lo borra un Defuse sin señal.
- **Quitar la recuperación de salud en el último año es caro**: 13 de 24 se agotan. El control de riesgo más alto de *close-mind* es un sesgo de supervivencia (sólo terminan 11).

## Decisión

- **Descartada** la limpieza preventiva del último año como regla de energía. Se mantiene la regla general: Defuse tras cualquier señal de riesgo (G1) y recuperar salud de forma preventiva hasta el final (G2).
- El módulo `closing` se reescribe sin "Defuse en cada trimestre aunque RR. HH. esté tranquilo"; queda lo que sí apoya la mecánica: salud y dignidad en la mitad alta y ninguna respuesta que esconda o aplace nada.
- Límite: son bots con historias al azar; Haiku elige mucho mejor las respuestas. La medida de verdad del P4 son las partidas completas de Haiku (lote `full-base`).
