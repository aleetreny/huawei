# Datos del banco de obediencia (T20)

Llevan texto del juego de desarrollo: sólo para estudiar en este repo privado; nada de aquí va a una Skill.

| Archivo | Qué es |
|---|---|
| `bank-items.jsonl.gz` | 2.389 situaciones del banco: validación final (`ids-V2.txt`), diseño (`ids-A.txt`), bloque general (`ids-G1.txt`) y rondas de historias. Cada línea: `id`, `rule` vía `tags`, `holdout` (título reservado), `phase`, `month`, `state` (estado completo del simulador), `fx` (efecto y riesgo de cada opción), `q` (nota final media en el simulador por opción) y `serve` (los `observe` exactos desde el principio del mes y el registro visible en cada paso) |
| `haiku-answers.json.gz` | Elecciones de Haiku por brazo (`control`, `control-b`, `f3lean`, `t10-countdown`, `t13-final`, `t2-veto`, `t9-quarter`) e id de situación |
| `ids-*.txt` | Listas de situaciones por conjunto |
| `handbook.md` | Manual del empleado tal como lo devuelve `show_employee_handbook` |

Puntuar un brazo nuevo: `scripts/transmision/score.py` (regla, acierto, pérdida de nota) y `scripts/transmision/fingerprint.py` (huella en el bloque general). Para regenerarlo todo desde los lotes de bots: [banco.md](../../reports/transmision/banco.md).
