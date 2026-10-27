# Palanca 1. La nota como memoria: una línea de estado en cada `take_action`

**Conclusión:** Haiku escribe la línea de estado en el 100 % de las notas, con la cuenta atrás y los valores correctos. Arrastra lo apuntado tras un resumen (100 %) y no contamina las historias más que `t13-final`. En el simulador, lo que la línea permite recordar (techos vistos y respuestas arriesgadas del mes) vale +14 puntos con el bot de reglas y +6 con un jugador con ruido. En Haiku lo medible es la parte de los techos: con su 59 % de detección, ~+5.

27 oct 2026, 17:00–18:00 UTC. Simulador sin cuota; banco con Haiku (`claude-haiku-5-5`, CLI 2.1.303, entrega oficial del Skill), unas 700 sesiones cortas, un 3 % de la ventana de 5 horas.

## La línea

Candidato final, [`t18-status`](../../policies-src/palancas/t18-status/) (`t13-final` más la línea):

```
Review in N | Now S<Skill> N<Network> O<Output> | Stalled: none | Risky this month: 0
Review in N | Now S14 N5 O7 | Stalled: none | Risky this month: 0 | Expect S14 N5 O8     (reparto trimestral)
```

- `Review in N`: la cuenta atrás de `t13-final` (interruptor de la regla del mes previo, HALLAZGOS B12).
- `Now` y `Expect`: los valores antes de elegir y los que la acción del reparto debería dejar según sus `status_updates`. Si el panel siguiente queda por debajo de `Expect`, el indicador no recogió la subida y pasa a `Stalled` hasta el siguiente ascenso ([techos.md](techos.md)).
- `Risky this month`: cuántas historias del mes se han resuelto con una opción que puede enterrar un problema ([riesgo.md](riesgo.md)).
- Al retomar (sesión nueva o resumen), `check_latest_logs` con count 3 y se copian `Stalled`, `Expect` y `Risky this month` de la última nota. Las notas de hasta 1.000 caracteres vuelven enteras por el registro (comprobado el 26 oct; [findings](../../../docs/historico/findings.md)).

Versiones probadas: `t16-caps` (sólo techos, comparando con `Now`), `t16b-expect` (con `Expect`), `t16c-feedback` (techo redactado como señal de la partida), `t17b-status` (t16b más el contador de riesgo) y `t18-status` (t17b con “Stalled” en lugar de “Caps”).

## Valor en el simulador

| Brazo (mismas 4.000 semillas) | Juego de desarrollo | Techos +20 % | Techos −10 % | Con ruido (30 % al azar) |
|---|---:|---:|---:|---:|
| Sin memoria: techo olvidado al mes siguiente, riesgo sólo por el comentario de RR. HH. | 49,9 | 54,1 | 45,3 | 25,9 |
| + techos apuntados todo el nivel | +6,2 | +5,3 | +6,8 | |
| + contador de respuestas arriesgadas | +9,8 | +11,8 | +8,3 | |
| **Las dos (línea de estado)** | **+14,3 ± 0,3** | **+15,4** | **+13,2** | **+6,2** |
| Las dos, con techos detectados sólo en el reparto | +12,2 | | | |

Ojo: el jugador sin contador se arriesga mucho más que Haiku (41 % de crisis de confianza), así que la parte del contador está sobrevalorada para Haiku (ver abajo).

## En el banco con Haiku

**1. Rellena bien la línea** (`notecheck.py`, todas las notas de cada situación, también las de los pasos previos del mes):

| Manual | Notas | Con la línea | `Review in N` bien | `Now` bien | `Risky this month` > 0 | Caracteres (mediana) | Lecturas del registro por situación |
|---|---:|---:|---:|---:|---:|---:|---:|
| t16b-expect (bloque general) | 277 | 100 % | 100 % | 100 % | — | 296 | 1,00 |
| t17b-status (bloque general) | 277 | 100 % | 100 % | 100 % | 3 % | 286 | 0,98 |
| t16b-expect (banco de techos) | 132 | 100 % | 100 % | 98 % | — | 265 | 1,01 |

**2. Recuerda tras un resumen y obedece lo apuntado** (banco de techos, 132 situaciones del reparto servidas como sesión nueva; detalle en [techos.md](techos.md)): un techo apuntado se arrastra el 100 % de las veces y el gasto en él baja del 27 % (`t13-final`) al 3 %. Descubrirlo es más difícil: 59 % con `Expect`, 16 % sin él.

**3. No contamina las historias** (bloque general: 139 historias de meses 1–44 sin regla especial, contexto de mes; mismas situaciones que las respuestas guardadas de la línea Transmisión):

| Manual | Skill | Network | Output | Health | Dignity | Riesgo | Igual que el control | Acierto | Pérdida de nota |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| control | +0,82 | +0,53 | +0,09 | +0,01 | +1,09 | −0,19 | 100 % | 75 % | 1,42 |
| control repetido | +0,81 | +0,60 | +0,09 | +0,01 | +1,09 | −0,21 | 96 % | 75 % | 1,10 |
| t13-final | +0,74 | +0,72 | +0,16 | −0,10 | +0,99 | −0,13 | 81 % | 78 % | 1,01 |
| t16b-expect | +0,71 | +0,71 | +0,17 | −0,09 | +1,03 | −0,10 | 86 % | 78 % | 0,83 |
| t17b-status | +0,72 | +0,67 | +0,19 | −0,11 | +1,04 | −0,17 | 88 % | 79 % | 0,65 |

(Efecto medio anunciado de la opción elegida; acierto = a 0,5 puntos o menos de la mejor opción según el simulador; 132 situaciones decisivas.)

- La línea de estado deja la huella como la de `t13-final` o más cerca del control (86–88 % frente a 81 %). Escribir los números en cada nota no tiñe las historias.
- El contador de riesgo casi nunca se enciende (3 % de las notas): Haiku ya elige casi siempre opciones prudentes (HALLAZGOS B9). Baja algo el riesgo medio elegido (−0,17 frente a −0,10) y la pérdida (0,65 frente a 0,83), dentro del ruido (error típico de la pérdida ~0,2).

**4. Calidad del Skill** (rúbrica oficial con Sonnet, 3 lecturas): `t13-final` 65,3, `t16b-expect` 65,3, `t16c-feedback` 64,7, todo dentro del ruido (±6). El revisor señala en todas las versiones con “Caps” que el techo por nivel no está publicado (el manual dice “0–unbounded”) y que se puede leer como una mecánica oculta. Por eso `t18-status` lo llama `Stalled` y sólo describe lo que se ve: un indicador que no recogió una subida anunciada.

## Cuántas partidas harían falta para confirmarlo

Con Haiku, la nota de una partida tiene una desviación de ~17 puntos (t13-final: 57,2 ± 5,1 con 12 partidas). Para ver una mejora de +3 a +5 puntos con un 80 % de potencia hacen falta **180–500 partidas por brazo**, porque las partidas oficiales no admiten semilla común. No es viable con la cuota. La decisión tiene que apoyarse en el simulador y en el banco, y en las partidas sólo comprobar que nada se rompe (por ejemplo, 10 partidas: que la línea aparezca en todas las notas y que ninguna termine por una causa nueva).
