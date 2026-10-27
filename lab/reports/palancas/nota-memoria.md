# Palanca 1. La nota como memoria: una línea de estado en cada `take_action`

**Conclusión:** Haiku escribe la línea de estado en el 100 % de las notas, con la cuenta atrás y los valores correctos. Recupera lo apuntado tras un resumen (97–100 %) y no tiñe las historias más que `t13-final`. En el simulador, lo que la línea permite recordar vale +14 puntos con el bot de reglas y +6 con un jugador con ruido. En Haiku sólo funciona la parte de los techos: con su ~60 % de detección, unos +5. El contador de riesgo no se enciende, porque Haiku no reconoce sus respuestas arriesgadas.

27 oct 2026, 17:00–18:10 UTC. Simulador sin cuota. Banco con Haiku (`claude-haiku-5-5`, CLI 2.1.303, entrega oficial del Skill): unas 2.000 sesiones, casi todas cortas, y 15 lecturas de Sonnet para la rúbrica. La ventana de 5 horas iba por el 3–4 %.

## La línea

Candidato final, [`t19-final`](../../policies-src/palancas/t19-final/) (`t13-final` más la línea):

```
Review in N | Now S<Skill> N<Network> O<Output> | Stalled: none | Risky this month: 0
Review in N | Now S14 N5 O7 | Stalled: none | Risky this month: 0 | Expect S14 N5 O8     (reparto trimestral)
```

- `Review in N`: la cuenta atrás de `t13-final` (interruptor de la regla del mes previo, HALLAZGOS B12).
- `Now` y `Expect`: los valores antes de elegir y los que la acción del reparto debería dejar según sus `status_updates`. Si el panel siguiente queda por debajo de `Expect`, el indicador no recogió la subida y pasa a `Stalled` hasta el siguiente ascenso ([techos.md](techos.md)). `Now` es un registro, no una clasificación: los tres indicadores crecen en escalas distintas.
- `Risky this month`: cuántas historias del mes se han resuelto con una opción que puede enterrar un problema ([riesgo.md](riesgo.md)).
- Al retomar (sesión nueva o resumen), `check_latest_logs` con count 3 y se copian `Stalled`, `Expect` y `Risky this month` de la última nota. Las notas de hasta 1.000 caracteres vuelven enteras por el registro (comprobado el 26 oct; [findings](../../../docs/historico/findings.md)); las de Haiku rondan los 300.

| Versión | Qué cambia | Por qué se cambió |
|---|---|---|
| `t16-caps` | `t13-final` + `Review in N \| Now S N O \| Caps` | detectaba el techo sólo el 16 % de las veces |
| `t16b-expect` | + `Expect` en el reparto | detecta el 59 %; pero “Caps” suena a mecánica oculta (rúbrica) |
| `t16c-feedback` | `t16b` con el techo redactado como señal de la partida | el revisor sigue leyendo “Caps” como regla oculta |
| `t17b-status` | `t16b` + `Risky this month` | — |
| `t18-status` | `t17b` con `Stalled` en vez de `Caps` | en el reparto de L4, Haiku comparaba los números de `Now` entre sí y dejaba Skill por Output |
| **`t19-final`** | `t18` + “`Now` no es una clasificación” + el cambio a Output en L4 sólo si la evaluación lo pide | **candidato** |

## Valor en el simulador

| Brazo (mismas 4.000 semillas, réplica corregida) | Juego de desarrollo | Techos +20 % | Techos −10 % |
|---|---:|---:|---:|
| Sin memoria: techo olvidado al mes siguiente, riesgo sólo por el comentario de RR. HH. | 50,1 | 54,2 | 45,4 |
| + techos apuntados todo el nivel | +6,3 | +5,4 | +6,9 |
| + contador de respuestas arriesgadas | +9,9 | +11,9 | +8,4 |
| **Las dos (línea de estado)** | **+14,4 ± 0,3** | **+15,5** | **+13,3** |
| Las dos, jugador con ruido (30 % de historias al azar) | +6,2 | +7,3 | +5,4 |

Ojo: el jugador sin contador se arriesga mucho más que Haiku (41 % de crisis de confianza), así que la parte del contador está sobrevalorada para Haiku. En el banco, además, Haiku no lo usa (abajo).

## En el banco con Haiku

**1. Rellena bien la línea** (`notecheck.py`: todas las notas de cada situación, también las de los pasos previos del mes):

| Manual | Notas | Con la línea | `Review in N` bien | `Now` bien | Caracteres (mediana) | Lecturas del registro por situación |
|---|---:|---:|---:|---:|---:|---:|
| t13-final (bloque general, local) | 277 | — | — | — | 220 | 0,99 |
| t16b-expect | 277 | 100 % | 100 % | 100 % | 296 | 1,00 |
| t18-status | 277 | 100 % | 100 % | 100 % | 295 | 0,97 |
| t19-final | 277 | 100 % | 100 % | 100 % | 301 | 0,98 |

**2. Recuerda tras un resumen y obedece lo apuntado** (banco de techos: 132 situaciones del reparto servidas como sesión nueva; detalle en [techos.md](techos.md)):

| Manual | Descubre el techo | Arrastra el techo apuntado | Gasta en un techo apuntado | Falsas alarmas sin techo |
|---|---:|---:|---:|---:|
| t13-final | — | — | 27 % | — |
| t16b-expect | 59 % | 100 % | 3 % | 0 % |
| t18-status | 49 % | 97 % | 6 % | 2 % |
| t19-final | **63 %** | **97 %** | 9 % | 2 % |

**3. No contamina las historias** (bloque general: 139 historias de los meses 1–44 sin regla especial, jugadas desde el principio del mes; las respuestas de control, control repetido y `t13-final` son las que grabó la línea Transmisión, y `t13-final` local se volvió a jugar aquí para comprobar el arnés):

| Manual | Skill | Network | Output | Health | Dignity | Riesgo | Igual que el control | Acierto | Pérdida de nota | Tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| control | +0,82 | +0,53 | +0,09 | +0,01 | +1,09 | −0,19 | 100 % | 75 % | 1,42 | |
| control repetido | +0,81 | +0,60 | +0,09 | +0,01 | +1,09 | −0,21 | 96 % | 75 % | 1,10 | |
| t13-final (Transmisión) | +0,74 | +0,72 | +0,16 | −0,10 | +0,99 | −0,13 | 81 % | 78 % | 1,01 | |
| t13-final (local) | +0,78 | +0,60 | +0,14 | −0,07 | +1,01 | −0,21 | 85 % | 79 % | 1,04 | 66k |
| t16b-expect | +0,71 | +0,71 | +0,17 | −0,09 | +1,03 | −0,10 | 86 % | 78 % | 0,83 | 63k |
| t17b-status | +0,72 | +0,67 | +0,19 | −0,11 | +1,04 | −0,17 | 88 % | 79 % | 0,65 | 65k |
| t18-status | +0,73 | +0,66 | +0,17 | −0,10 | +1,07 | −0,16 | 86 % | 80 % | 0,63 | 66k |
| t19-final | +0,77 | +0,68 | +0,16 | −0,07 | +1,09 | −0,20 | **89 %** | 79 % | 0,90 | 65k |

(Efecto medio anunciado de la opción elegida. Acierto: a 0,5 puntos o menos de la mejor opción según el simulador, en 132 situaciones decisivas. Error típico de la pérdida, ~0,2.)

- El arnés local reproduce a Transmisión: `t13-final` local y el grabado empatan en acierto (79 % y 78 %) y pérdida (1,04 y 1,01).
- La línea de estado deja la huella como la de `t13-final` o más cerca del control (86–89 % frente a 81–85 %). Escribir los números en cada nota no tiñe las historias.
- Pierde algo menos de nota que `t13-final` (0,63–0,90 frente a 1,01–1,04), pero dentro del ruido.

**4. Las reglas del reparto siguen funcionando** (conjunto A de Transmisión; acierto %, mismas situaciones):

RESULTADOS_A

**5. Contexto largo** (las 18 decisiones anteriores de la misma partida antes de la situación, como en [contexto-largo.md](../transmision/contexto-largo.md); 30 historias de partidas `v02`):

RESULTADOS_LARGO

**6. Calidad del Skill** (rúbrica oficial con Sonnet, 3 lecturas por manual):

| Manual | Media | Lecturas |
|---|---:|---|
| t13-final | 65,3 | 58, 72, 66 |
| t16b-expect | 65,3 | 62, 62, 72 |
| t16c-feedback | 64,7 | 58, 68, 68 |
| t18-status | 70,7 | 74, 72, 66 |
| t19-final | 66,7 | 62, 66, 72 |

Todo cabe en el ruido (±6): la línea no baja la nota de calidad. Pero el revisor la señala en todas las versiones. Con “Caps” dice que es una mecánica sin publicar (el manual dice “0–unbounded”); con “Stalled” dice que la idea “parece sacada de las partidas de desarrollo” y que la línea es pesada. Las normas permiten la estrategia basada en lo que la partida devuelve, y el Skill no da ningún número ni afirma ningún techo; sólo dice qué hacer si una subida anunciada no aparece. **Es un riesgo de interpretación que tiene que aceptar Alejandro.**

## Cuántas partidas harían falta para confirmarlo

Con Haiku, la nota de una partida tiene una desviación de ~17 puntos (t13-final: 57,2 ± 5,1 con 12 partidas). Para ver una mejora de +3 a +5 puntos con un 80 % de potencia hacen falta **180–500 partidas por brazo**, porque las partidas oficiales no admiten semilla común. No es viable con la cuota. La decisión tiene que apoyarse en el simulador y en el banco; las partidas sólo servirían para comprobar que nada se rompe (unas 10: que la línea salga en todas las notas y que ninguna partida termine por una causa nueva).
