# Línea Palancas

**Pregunta:** ¿cuánta nota vale cada herramienta o pista del juego que todavía no explotamos, y cómo se consigue que la IA la use?

Rama `alejandro/palancas`, código en [`scripts/palancas/`](../../../scripts/palancas/). Prompt de la línea: [prompt-palancas.md](../transmision/prompt-palancas.md). Primero el simulador (sin cuota), después el banco con Haiku y, sólo al final, partidas (con permiso de Alejandro).

## Conclusiones (27 oct, 17:30 UTC)

1. **Detectar el techo del nivel vale +8,8 puntos en el simulador**, el 78 % de lo que darían los techos exactos. La pista es que una subida anunciada no se mueve, y el techo se descubre en la partida, sin darle números. Aguanta si cambian los techos o los umbrales (+5 a +10). Recordarlo en la nota vale ~3 de esos puntos ([techos.md](techos.md)).
2. **Contar las respuestas arriesgadas desde el último comentario de RR. HH. vale +4,3** frente a fiarse sólo del comentario. Las cifras de riesgo del reparto trimestral, solas, valen +0,4 ([riesgo.md](riesgo.md)).
3. **Las dos juntas en una línea de estado de la nota** (techos vistos + contador de riesgo) valen +14 con el bot de reglas y +6 con un jugador con ruido, en los tres escenarios de techos ([nota-memoria.md](nota-memoria.md)). Es la palanca que pasa al banco.
4. **No valen la pena:** reaccionar a los avisos con 3 meses de margen (0 puntos; [avisos.md](avisos.md)) ni preparar la reputación antes de la evaluación (+0,1 con la regla exacta, −0,5 con la general; [reputacion.md](reputacion.md)).

## Tabla de palancas

| # | Palanca | Valor en el simulador | ¿Al banco? | Informe |
|---|---|---|---|---|
| 1 | Nota como memoria (línea de estado) | ver 2 + 5: +14,3 ± 0,3 (bot de reglas), +6,2 ± 0,2 (con ruido) | **sí** | [nota-memoria.md](nota-memoria.md) |
| 2 | Techo del nivel, detectado y apuntado | +8,8 ± 0,3 (memoria todo el nivel); +5,6 si se olvida al mes | **sí** | [techos.md](techos.md) |
| 3 | Avisos con 3 meses de margen | −0,00 ± 0,02 | no | [avisos.md](avisos.md) |
| 4 | Reputación antes de la evaluación | +0,07 ± 0,06 (exacta), −0,46 ± 0,17 (general) | no | [reputacion.md](reputacion.md) |
| 5 | Riesgo en cifras del reparto | +0,4; contar el signo de lo elegido, +4,3 | dentro de la 1 | [riesgo.md](riesgo.md) |
| 6 | Tokens por mes | pendiente | — | [tokens.md](tokens.md) |

El bot base es el de las 7 reglas generales ([motor M22](../ingenieria-inversa/motor-exacto.md)); cada palanca es una opción suya en [`scripts/palancas/sim.py`](../../../scripts/palancas/sim.py). Todas las comparaciones usan las mismas semillas, y las diferencias son emparejadas, ± error típico. Para poder enseñar los techos al bot se añadió a `rules.RuleBot` un método `cap()`, que no cambia su juego (mismas notas con la misma semilla).

## Relevo

**27 oct, 17:30 UTC.**
1. **Hecho.** Rama y carpeta abiertas, línea en ESTADO.md. Palancas 2 a 5 medidas en el simulador (4.000 partidas emparejadas por brazo y escenario).
2. **Resultados.** Tabla de arriba. Datos por partida en `~/careerlab-data/palancas/*.json` (se regeneran con los comandos de cada informe, ~40 s cada uno).
3. **A medias.** Banco con Haiku de la línea de estado (palancas 1 y 2) y tokens (palanca 6).
4. **Siguiente.** Construir el banco: situaciones donde una subida anunciada no se movió (¿lo apunta Haiku?) y situaciones dentro del mes con respuestas arriesgadas ya elegidas (¿las cuenta?). Medir con `t13-final` frente a una variante con la línea de estado y la huella en el bloque general.

```bash
python3 scripts/palancas/sim.py caps --games 4000
python3 scripts/palancas/sim.py notes --games 4000
```
