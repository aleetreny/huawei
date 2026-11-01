# Tramos fieles de la línea Corte 3 (1 nov)

DeepSeek (`deepseek-v4-flash`, clave de la competición, OpenRouter sin elegir proveedor; casi todo servido por Baidu) juega el principio de una partida oficial con la petición exacta de JiuwenSwarm (`scripts/tramos/fiel.py`), contra el motor oficial y hasta salir de L1 (`--stop-month 18`, o 12 en `c3r4`). Coste total ~5,1 USD. Cada tramo: `<brazo>-<n>.json.gz` (decisiones, notas, estado, parada, coste) y `<brazo>-<n>.messages.json.gz` (los mensajes, con texto del juego); `calls.jsonl.gz`, una línea por llamada (proveedor, fichas, coste, sin texto del juego).

| Tanda | Brazos (manual) | Tramos | USD |
|---|---|---:|---:|
| `c3r1` | v4loop (`mejora/v4-loop`), c3k (`corte3/c3-k`), c3a (`corte3/c3-a`) | 47 | 1,44 |
| `c3r2` | v4loop, c3k2 (`corte3/c3-k2`), c3a2 (`corte3/c3-a2`) | 38 | 2,01 |
| `c3r3` | c3k2, c3k3 (`corte3/c3-k3`) | 9 | 1,01 |
| `c3r4` | c3k4 (`corte3/c3-k4`), hasta el mes 12 | 24 | 0,66 |

Resúmenes: `python3 scripts/corte3/tramos_l1.py <carpeta>` (salida de L1, muertes) y `scripts/corte3/tramos_ventana.py` (pérdidas de N/O en los meses 4–5). Informe: [lab/reports/corte3/](../../../../reports/corte3/README.md). Nada de esta carpeta puede ir a un Skill.
