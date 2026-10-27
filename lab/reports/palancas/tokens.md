# Palanca 6. Tokens por mes

**Conclusión:** la línea de estado no cambia el gasto de tokens que se puede medir (32k por situación con y sin ella, y una sola lectura del registro por situación en los dos casos). Toda la parte de tokens vale como mucho **+0,7 puntos** de nota final: la única partida oficial con DeepSeek gastó ~667.000 tokens por mes, y el máximo se alcanza con 500.000.

27 oct 2026, 17:35 UTC. Sin cuota nueva: números del banco de esta línea y de partidas anteriores.

## La regla

`tokens_per_month = total_tokens / meses sobrevividos`: 100 puntos con 500.000 o menos, 0 con 3 millones o más, lineal en medio; una partida que no llega al mes 48 tiene esta parte limitada a 50 (reglas oficiales, `local-runs/official-runner/docs/competition-rules.rst`, fuera de Git: `sh scripts/setup_official_runner.sh`). Pesa el 10 % de la nota de cada versión.

## Lo que sabemos del gasto real

| Partida | Tokens | Meses | Tokens por mes | Nota de tokens si terminara |
|---|---:|---:|---:|---:|
| DeepSeek, programa oficial, manual F1 (26 oct; [histórico](../../../docs/historico/ESTADO-2026-10-26-carrera.md), T6) | 16,0 M de entrada | 24 | ~667.000 | ~93 |
| Haiku por el CLI, manual P0 (26 oct; [findings](../../../docs/historico/findings.md)) | 31,4 M (casi todo caché) | 48 | ~657.000 | ~94 |

- **Lo que se puede ganar:** pasar de ~93 a 100 en ese 10 % son **+0,7 puntos** de nota final, y sólo en partidas que terminan. Terminar la partida vale mucho más: sin terminar, ese término se queda en 50 (−4,3 puntos frente a 93).
- **De dónde sale el gasto:** cada llamada reenvía el historial de la conversación. Lo que más pesa son los `observe` (el texto de cada historia) y el número de llamadas por decisión, no la longitud de las notas.

## Lo que añade la línea de estado

| Medida | `t13-final` | `t16b-expect` (línea de estado) | Fuente |
|---|---:|---:|---|
| Tokens por situación de un turno (banco de techos, 132 situaciones) | 32k | 32–33k | [techos.md](techos.md) |
| Lecturas del registro por situación | 0,97 | 1,01 | `notecheck.py` |
| Caracteres por nota (mediana) | 194 | 265–297 | `notecheck.py` |

- **Unos 80 caracteres más por nota** (~20 tokens). Con ~5 decisiones al mes, aunque cada nota se reenviara en las 30 llamadas siguientes, serían ~3.000 tokens por mes: menos del 0,5 % de 667.000.
- **No añade llamadas:** el registro se lee sólo al retomar, como ya hacía `t13-final`.

## Qué haría falta para saberlo de verdad

Los tokens del programa oficial con DeepSeek no se pueden medir con Haiku (el agente, el prompt y la gestión del contexto son otros). Lo tiene que medir la línea DeepSeek en sus partidas oficiales: `total_tokens` por mes con `t13-final` y con `t16b-expect`. Si pasan de 500.000, lo primero es recortar llamadas por decisión (no leer el manual del empleado ni el registro sin necesidad), no las notas.
