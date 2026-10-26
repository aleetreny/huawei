# Relevo — línea de investigación de decisiones

26 oct 2026 · Codex · rama `alejandro/investigacion-decisiones` · base `3c1c993`.

## Qué se ha hecho y por qué

Alejandro pidió abrir una línea robusta para averiguar qué decisiones mejoran el score y convertirlas en mejores estrategias. Se ha preparado el [protocolo de trabajo](../../../research/careerlab/decision-research/README.md) y una auditoría reproducible antes de ajustar regresiones: confundir trazas disponibles con todas las partidas puede cambiar las conclusiones.

El protocolo separa descubrimiento, ensayo aleatorio de una regla y confirmación. Respeta el protocolo v1 congelado, trata la partida como unidad independiente, conserva las eliminaciones y distingue las interrupciones. Prioriza crecimiento seguro (H1) y después protección de entrega en historias (H2), aprovechando candidatas existentes tras verificar sus diferencias.

No se han lanzado partidas, encolado trabajos, gastado APIs, cambiado manuales ni modificado el selector. El script nuevo no importa CareerLab ni el motor; sólo lee exports y archivos de respuestas oficiales ya guardados.

## Resultados y datos

| Fuente | Evaluaciones | Terminales válidas | Interrumpidas con evaluación | Trazas Claude terminales en este Mac |
|---|---:|---:|---:|---|
| Canónica | 322 | 316 (166 Claude + 150 bots) | 6 | 99 con hash primario verificado; 67 ausentes |
| Leah (separada) | 7 | 1 | 6 | 1 sin comprobar |

- Las 99 trazas locales verificadas contienen observaciones oficiales: 48 partidas completadas y 51 eliminadas. Las 67 no localizadas corresponden a 32 completadas y 35 eliminadas. No se deduce su ausencia en la nube.
- Los 383 jobs canónicos no tienen campos explícitos para `epoch`, `block_id`, `analysis_role` o `assignment_probability`. Debe recuperarse su procedencia o declararse desconocida. La auditoría no presupone que falten en cualquier otra fuente del laboratorio.
- Hay 61 trabajos sin evaluación, distintos de las 322 evaluaciones: 22 interrupted, 16 leased, 15 queued y 8 running. No se puntúan.
- Archivos: [audit-canonical.json](audit-canonical.json), [audit-leah.json](audit-leah.json). Incluyen hashes de los cinco exports, separación por actor/entorno y cobertura por job, sin texto de eventos ni razonamientos del actor. Las medias incluidas son descriptivas, no comparaciones causales entre modelos.
- El registro principal fija hash de `stream-0.jsonl` o `trajectory.jsonl`; si hay continuaciones, el script calcula hashes adicionales y deja explícito que el registro no los autentica. Verificar hash no certifica completitud ni alineación de decisiones.

## Qué queda a medias

No se ha ajustado regresión ni implementado el conjunto de decisiones. Antes se necesita extracción temporal con IDs, etiquetas de comportamiento revisadas sin ver resultados, cobertura de las trazas de nube y metadatos de experimentos. No hay una estimación causal nueva ni una estrategia declarada superior.

El fetch general encontró una colisión local de nombres `Matteo` / `matteo/...` por mayúsculas en macOS. Main y cloud sí se actualizaron; no se borraron ni reescribieron ramas ajenas. Para traer sólo las ramas comunes se puede usar `git fetch origin main cloud-lab-run`.

## Siguiente paso concreto

El organizador integra esta PR y reserva la implementación de extracción. No crear una segunda carrera ni reencolar el histórico. Ejecutar la auditoría en la nube sobre el mismo snapshot para resolver la cobertura, o repetirla sobre un snapshot nuevo con sus propios hashes:

```bash
python3 scripts/decision_research_audit.py \
  --export-dir lab/registry \
  --runs-root "$HOME/careerlab-data/huawei/runs" \
  --output lab/reports/decision-research/audit-canonical.json

python3 scripts/decision_research_audit.py \
  --export-dir lab/registry-origins/leah \
  --output lab/reports/decision-research/audit-leah.json

uv run pytest -q
```

Sin `--runs-root`, la cobertura queda `not_checked`; no se buscan rutas automáticamente. Dar a cada origen su carpeta correcta. No sobrescribir resultados canónicos con los de otro origen. Los exports que sustentan este informe son los de `3c1c993`; repetir sobre otro commit produce una auditoría diferente y debe identificarse como tal.

Después: congelar el esquema de extracción del protocolo, generar tabla numérica de estados previos/decisiones y revisar etiquetas. Si hay datos comparables suficientes, ajustar modelos predictivos pequeños con validación por partidas/familias. Si no, pasar directamente de diagnóstico a un ensayo nuevo de una regla.

Para H1, el organizador congela hashes de padre/variante y el manifiesto de asignación antes de gastar partidas. La primera tanda propuesta es de 4 por brazo para instrumentación; el tamaño posterior depende de la variabilidad y cuota, con Δ = 4 Y. La confirmación se reserva después de congelar finalistas según v1. Este informe no autoriza otra máquina a jugar.

## Validación y estado

Auditorías ejecutadas sin conexión al juego. Validación final: **243 tests pasan** en 31,22 s, con una advertencia previa de deprecación de Authlib. `git diff --check`, compilación del script y enlaces locales de los dos informes comprobados. La suite usa el entorno existente con `UV_PROJECT_ENVIRONMENT` y `uv run --no-sync pytest -q`, sin reinstalar dependencias ni leer el interior del motor.

Línea propia añadida a `ESTADO.md`; no se reasignan T1–T13 ni se crea un número de tarea del organizador. Se solicita integrar en main mediante PR. La extracción, regresión y partidas son la siguiente fase de investigación, no entregables que se anuncien como hechos.
