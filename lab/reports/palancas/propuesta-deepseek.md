# Propuesta para la línea DeepSeek: medir la línea de estado

**Conclusión:** tres medidas baratas con DeepSeek (unos 0,6 USD en total, con el coste por situación del banco de la línea DeepSeek) dirían si la palanca de los techos y el contador de riesgo funcionan con el modelo de la competición. Esta línea no gasta DeepSeek: lo decide y lo lanza la línea DeepSeek, con el visto bueno de Alejandro.

27 oct 2026, 18:00 UTC.

## Por qué con DeepSeek

- Con Haiku, la línea de estado se rellena y se recuerda bien, pero el techo se detecta en un 49–59 % y el contador de riesgo casi no se enciende, porque Haiku no reconoce sus respuestas arriesgadas (19 %).
- DeepSeek ve mejor el riesgo (83–92 %; HALLAZGOS B17), así que el contador podría servirle (+4,3 en el simulador para un jugador que se arriesga).
- La cuenta atrás `Review in N` aísla peor con DeepSeek (HALLAZGOS C7). Hay que comprobar que la línea completa no le tiñe las historias.

## Las tres medidas

| # | Qué | Situaciones | Brazos | Coste estimado |
|---|---|---:|---|---:|
| 1 | Banco de techos: ¿detecta, arrastra y respeta el techo? | 132 (un turno cada una) | `t13-final` frente a `t19-final` | ~0,2 USD |
| 2 | Bloque general: huella, pérdida y contador de riesgo (¿cuenta bien sus respuestas arriesgadas?) | 139 (mes desde el principio) | `t19-final` (control y `t13-final` ya están hechos en esa línea) | ~0,2 USD |
| 3 | Tokens por mes en las partidas oficiales que ya se vayan a jugar | — | `total_tokens / meses` con el manual que se juegue | 0 extra |

Coste: la línea DeepSeek gastó 1,20 USD en 918 situaciones del banco (~0,0013 USD cada una), y las del bloque general son más largas. Con margen, ~0,6 USD para 1 y 2.

`t19-final` es `t13-final` más la línea de estado ([nota-memoria.md](nota-memoria.md)). Si la línea DeepSeek prefiere su `t13-read-v1`, la línea de estado se puede añadir igual: son las secciones “Status line” y la regla “Wherever a line names an action for a stat in Stalled…” del reparto.

## Cómo

Las situaciones del banco de techos tienen el formato de `bank-items` (campo `serve`), pero uno de sus ids coincide con una situación del banco general. Por eso conviene una carpeta aparte:

```bash
mkdir -p ~/careerlab-data/palancas/ds
cp ~/careerlab-data/palancas/items-caps-t13.jsonl ~/careerlab-data/palancas/ds/items-t13.jsonl
cp ~/careerlab-data/palancas/items-caps-stalled.jsonl ~/careerlab-data/palancas/ds/items-stalled.jsonl
# bench.py lee DEEPSEEK_DATA/items.jsonl: copiar el que toque como items.jsonl antes de cada brazo
python3 -c "import json; print('\n'.join(json.loads(l)['id'] for l in open('$HOME/careerlab-data/palancas/caps-bank.jsonl')))" > ~/careerlab-data/palancas/ds/ids-caps.txt
cp ~/careerlab-data/palancas/ds/items-stalled.jsonl ~/careerlab-data/palancas/ds/items.jsonl
DEEPSEEK_DATA=~/careerlab-data/palancas/ds uv run python scripts/deepseek/bench.py run --variant lab/policies-src/palancas/t19-final/bundle --name ds-caps-t19 --ids ~/careerlab-data/palancas/ds/ids-caps.txt
cp ~/careerlab-data/palancas/ds/items-t13.jsonl ~/careerlab-data/palancas/ds/items.jsonl
DEEPSEEK_DATA=~/careerlab-data/palancas/ds uv run python scripts/deepseek/bench.py run --variant lab/policies-src/transmision/t13-final/bundle --name ds-caps-t13 --ids ~/careerlab-data/palancas/ds/ids-caps.txt
TRANSMISION_DATA=~/careerlab-data/palancas/ds python3 -I scripts/palancas/capbank.py score --bank ~/careerlab-data/palancas/caps-bank.jsonl --arms ds-caps-t13,ds-caps-t19
```

Para el bloque general, con los ficheros de la línea DeepSeek: `bench.py run --variant lab/policies-src/palancas/t19-final/bundle --name ds-g1-t19 --ids lab/data/transmision/ids-G1.txt`, y después `fingerprint.py` y `score.py` como en [obediencia.md de DeepSeek](../deepseek/obediencia.md). El contador de riesgo se puntúa con [`riskcount.py`](../../../scripts/palancas/riskcount.py), que necesita el `record.jsonl` de cada situación (`bench.py` guarda la lista de herramientas, no las notas de los pasos previos; habría que guardarlas también).

## Qué decidiría cada resultado

- Si DeepSeek detecta el techo en más del 50 % y lo respeta, la línea de estado entra en el manual del corte siguiente.
- Si el contador marca bien sus respuestas arriesgadas (más del 60 %) y baja el riesgo elegido sin tocar el resto de la huella, se queda; si no, se quita, porque cuesta 120 palabras del Skill y no aporta.
- Si la huella del bloque general se aleja del control más que la de `t13-final`, la línea de estado se queda sólo en el reparto trimestral.
