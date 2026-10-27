# Mejora de la nota de DeepSeek: análisis desde los fundamentos y manuales t13-read-v2 a v4

**Conclusión (provisional, 27 oct por la noche).** Con DeepSeek, la nota la decide sobrevivir: las tres partidas oficiales anteriores (f1 y dos de t13-read-v1) acabaron eliminadas, dos de ellas por perder el primer ascenso. En el simulador, con la lectura real de DeepSeek, lo que más puntos mueve es **proteger Skill, Network y Output en el mes previo a la evaluación por delante de un riesgo leve, mientras el comentario de RR. HH. esté tranquilo** (+1,6 y despidos −24 %). Las demás ideas (riesgo primero, limpieza preventiva, ventanas más largas, detectar techos en las historias) no mueven al bot. Las partidas de `t13-read-v2`, `v3` y `v4` están en juego; resultados abajo.

27 oct 2026, rama `alejandro/deepseek` (worktree `~/huawei-ds`). Encargo de Alejandro: subir la nota de DeepSeek pensando desde los fundamentos, hasta 10 USD hoy.

## 1. De dónde salen los puntos

- **La nota final:** nivel 30 %, dinero 20 %, Health + Dignity 15 %, Skill 15 %, control de riesgo 10 %, Network 10 % (A1). Normalizaciones vistas en los informes oficiales: nivel = 10 × L, dinero sobre 80, Health + Dignity sobre 20, Skill sobre 120, Network sobre 60, riesgo 0 = 100. Para llegar a 70 hay que acabar los 48 meses en L6, con riesgo 0 y Health y Dignity llenos.
- **La nota de cada partida oficial es su `quantitative_score`** (la media de 3 partidas da el 80 % de la versión). La `competition_partial_score` de los informes es siempre esa nota × 0,7 y no se usa para la clasificación (corregido: no es un castigo por eliminación). Una partida eliminada pierde los meses que no juega: nivel, dinero y lo que habría crecido.
- **Las dos formas de perder con DeepSeek, vistas en partidas:**
  1. **Perder el primer ascenso.** En L1 el umbral de Network y Output coincide con lo máximo que admite el nivel. Un punto perdido en las historias justo antes de la evaluación cuesta el ascenso (f1 lo perdió así dos veces: Network en el mes 5 y Output en el 11). En L1, quien no asciende para el mes 12 acaba despedido en el mes 24.
  2. **La crisis de confianza**, por opciones que parecen constructivas (en privado, anónimas, por fases).
- **El simulador con la lectura de DeepSeek** (bot de regla escrita, dos pasadas de etiquetas, 2.000 partidas) dice que el despido pesa mucho más que la crisis: 26 % de despidos frente a 6 % de crisis.

## 2. Qué se probó en el simulador (gratis)

Base: regla escrita "estricta" con la lectura v3 de DeepSeek, 53,9.

| Cambio | Nota | Despidos | Crisis |
|---|---:|---:|---:|
| Base (descarta lo arriesgado; protege el mes previo después) | 53,9 | 518 | 121 |
| Si RR. HH. no está tranquilo, sólo opciones que bajan el riesgo | 54,1 | 525 | 102 |
| Lo mismo siempre | 54,2 | 524 | 92 |
| Limpiar riesgo en el trimestre en cuanto RR. HH. no sonríe | 54,0 | 519 | 105 |
| Además, "Lay low" en cuanto no sonríe | 53,7 | 534 | 90 |
| **Mes previo: proteger el ascenso antes que el riesgo leve, si RR. HH. está tranquilo o "quiet"** | **55,5** | **396** | 151 |
| Lo mismo con cualquier riesgo | 53,1 | 360 | 297 |
| Lo mismo, dos o tres meses antes | 53,5 / 51,2 | 422 / 442 | 213 / 238 |
| Proteger también los dos meses previos, después del riesgo | 55,1 | 410 | 161 |
| Sin conocer los techos (como DeepSeek) | 54,4 | 413 | 161 |
| … y detectándolos en las historias | 54,3 | 441 | 143 |

Con etiquetas perfectas, el mismo cambio sube de 60,7 a 62,2. El oráculo saca 68,1.

**Por qué el mes previo es un dilema:** en el 10 % de las preguntas todas las opciones bajan Skill, Network u Output, y en el 26 % todas bajan alguno o son arriesgadas. Con tres historias en ese mes, hay un 27 % de opciones de que la pérdida sea inevitable si no se acepta algo de riesgo.

**Lo que el bot no puede ver:** DeepSeek persigue subidas que ya no caben (una partida de t13-read-v2 perdió dos puntos de Output con `Review in 2` para ganar Network, que ya estaba en su máximo) y casi no consulta el registro. El bot conoce los techos en el trimestre; DeepSeek no.

## 3. Los manuales

| Manual | Qué cambia | Por qué |
|---|---|---|
| `t13-read-v2` | t13-read-v1 + protección del mes previo en el cuerpo y en la instrucción del manifest; separación estricta trimestre/historias; paso de riesgo más duro si RR. HH. no está tranquilo; línea de estado con techos observados; sin umbrales numéricos | Las partidas: DeepSeek lee el Skill sólo dos veces y no vuelve a abrir la referencia; la regla trimestral se coló en las historias; el riesgo "constructivo" mató una partida |
| `t13-read-v3` | v2 + en el mes previo, con RR. HH. tranquilo o "quiet", el ascenso va antes que el riesgo leve | Simulador: +1,6, despidos −24 % |
| `t13-read-v4` | v3 + "Best" (mejor valor de cada indicador en el nivel), protección de Network y Output los dos últimos meses con reparación inmediata, detección de techos también en historias | Ideas de `observed-growth-v10` de Matteo y el fallo de la partida 1 de v2 |

Todos pasan `careerlab lint` sin errores.

## 4. Partidas oficiales

### t13-read-v2 (3 partidas en paralelo, 27 oct desde las ~18:00 UTC)

Lo visto mientras juegan:
- **Ascensos:** dos partidas ascienden a L2 en el mes 6 y la tercera en el mes 12. Una llega a L3 en el mes 18 y otra en el 24. Ninguna se pierde en L1, frente a 2 de 3 eliminadas así con los manuales anteriores.
- **Riesgo:** el comentario de RR. HH. está tranquilo casi todo el tiempo; una sola explosión en tres partidas hasta el mes 24.
- **La línea de estado se rellena siempre, pero "Stalled" nunca** (0 de 160 notas), aunque Skill, Network y Output estén justo en lo máximo del nivel. DeepSeek no compara una nota con la anterior. Sin esa detección, la regla "Network y Output estancados → Skill" nunca se activa.
- **Ascensos perdidos y por qué:**
  - Mes 6: con Review in 2 eligió prepararse a fondo para una revisión de otro equipo (Output −2) para ganar Network, que ya estaba en su máximo.
  - Mes 12: con Review in 1 eligió "asumirlo e impulsar una norma de equipo" (Output −1) y llegó con Output un punto por debajo.
  - Mes 9: en el trimestre previo gastó 2 de energía en limpiar riesgo con RR. HH. tranquilo, en vez de llenar Output (en L2 el máximo deja un punto de margen).
- **Incidente:** la primera partida (hueco 0) se lanzó en modo normal con tope de 1,2 USD. El vigilante mide el gasto de toda la clave y, con las otras dos partidas en paralelo, la cortó en el mes 26, en L3, sin explosiones. Lección: en paralelo, tope alto y coste por partida desde el informe del programa.

### Siguiente lote

Una partida de cada uno: `t13-read-v3`, `t13-read-v4` y `t13-read-v5`. v5 recoge lo aprendido de v2: llenar los tres indicadores en el trimestre previo, quedarse en la propia entrega con la evaluación cerca, Skill primero desde L4, sin "Stalled".

## 5. Infraestructura nueva

- `careerlab/target.py`: modo paralelo (`CAREERLAB_TARGET_PARALLEL=1`). Partidas en huecos distintos a la vez; su coste se lee del informe del programa (`total_cost`), no de la diferencia de saldo.
- `scripts/deepseek/gameloop.sh`: una partida tras otra en un hueco, hasta un tope de gasto de la clave; nunca corta una partida.
- `scripts/deepseek/watch.py`: avisa de ascensos, explosiones, eliminaciones y finales.
- `scripts/deepseek/promo.py`: por qué el bot no asciende (le falta un indicador antes del mes previo, o lo pierde en él).
- `scripts/deepseek/groupbot.py`: modos nuevos de la regla escrita (`rvc`, `pw`, `pl1`, `dq`, `ll`, `blind`, `detect`, `ps`).
