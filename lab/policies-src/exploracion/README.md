# Candidatos de la línea Exploración

**En una frase:** `ex-v1` es el candidato para entregar (cp-v12 con mejores trimestres, freno de salud y texto reescrito para la rúbrica); `ex-v3` es `ex-v1` con una regla para el mes previo de L1 que sólo debe entrar si gana en el banco de DeepSeek; `ex-s1` demuestra el script con estado de C60 y no se espera que suba la nota.

Todos son un solo Skill (`career-rules`) y comparten el bucle de turno de cp-v12 (pareja `take_action` + `observe` sembrada en la pantalla «Continue»). Lint sin errores (sólo avisos REVIEW, como cp-v12). Informe y datos: [lab/reports/exploracion/](../../reports/exploracion/README.md); plan de pruebas: [plan-deepseek.md](../../reports/exploracion/plan-deepseek.md).

## Nota global esperada

Nota de versión = 0,8 × partidas + 0,1 × calidad + 0,1 × fichas. **Partidas:** media en la réplica calibrada con las 2.743 decisiones reales (4.000 partidas por brazo, error típico 0,25; README §1, `data/final_eval.json`). **Calidad:** jueces de Claude con la rúbrica oficial (`scripts/calidad-skills/judge.py`, Opus y Sonnet × 2). **Fichas:** las partidas completas de cp-v12 gastaron 370 y 492 mil por mes (100); una partida que no termina queda en 50.

| Manual | Partidas (réplica) | Muertes por salud / despidos en L1 / crisis | Calidad (Opus · Sonnet) | Fichas | Versión media (réplica) | P(versión > 68,17) | P(> 76) |
|---|---:|---|---|---:|---:|---:|---:|
| `comprobante/cp-v12` (referencia) | 58,1 | 6,5 % / 10,5 % / 3,3 % | 72,5 · 66 | ~98 | 62,2 | 32 % | 0,3 % |
| **`ex-v1`** | **59,9** (+1,8) | 1,1 % / 11,3 % / 3,3 % | **83,5 · 71,5** | ~98 | **64,5** (+2,2; +0,3 más por la calidad medida) | 43 % | 1,2 % |
| `ex-v3` | 60,2–60,3 (+2,2) | 1,1 % / 10,7 % / 3,3 % | 83 · 66 | ~98 | 64,8 | 44 % | 1,3 % |
| `ex-s1` | ≈ ex-v1 (el script suma +0,0) | — | 80 · 68 | ~96 | ≈ 64,3 | — | — |
| `ex-v2` | ≈ ex-v1 | — | — | — | **descartado** (Sonnet: sin efecto) | | |

Cómo leer la tabla: la réplica calibrada reproduce las partidas reales de la familia (completas 65,4 frente a 65,3; ~20 % de hundimientos), así que las **diferencias** entre brazos son la parte fiable; el nivel absoluto lleva el error del modelo. Que tres partidas oficiales salgan completas sube cualquiera de estas versiones a ~69–70.

## Qué cambia cada uno y qué lo respalda

### `ex-v1` (padre: cp-v12)
- **Trimestre** (DeepSeek obedece el trimestre, B20):
  - nivel inicial: toda la energía libre a Prepare report materials (si los informes del trimestre anterior no movieron Output, a Network maintenance); proyecto clave;
  - L2–L3: informe, red, informe y proyecto clave, sin Skill learning (el orden de v4; búsqueda por tramos: el mejor de 15 combinaciones);
  - desde L4: Skill learning + Prepare report materials (no Network maintenance) y rotación (búsqueda: +0,5);
  - Health recovery con Health ≤ 5 (antes ≤ 4); la acción principal sólo cambia con Health o Dignity ≤ 4.
  - Réplica: **+1,3** (sólo trimestre).
- **Historias:** con Health ≤ 3, fuera toda opción que la baje, también en el mes previo. Réplica: +0,5 más; las muertes por salud pasan del 6,5 % al 1,1 %. Es la parte que depende de que DeepSeek obedezca; el banco de L1 no la ve.
- **Texto:** plan de 48 meses por fases, tabla «cerca de un límite», calendario de la evaluación y márgenes marcados como observaciones nuestras con su comprobación en partida, paso 2 en viñetas, línea de estado sin «Reviews here» (el arranque atascado se lee de «Months at current level»). Juez: Opus 73 → 84, Sonnet 66 → 72.
- **Bucle:** el de cp-v12; sólo cambia la nota del ejemplo literal (un campo menos). Hay que comprobar la pareja con sondas (plan, paso 1).

### `ex-v3` (padre: ex-v1)
- **Una regla de historias en el mes previo de L1:** con RR. HH. amable o quiet y sin otra elección arriesgada en el mes, tratar el problema de forma discreta (en privado con la persona, o por escrito después de la reunión) en vez de corregir, negarse o plantarse en público.
- **Respaldo:**
  - en el mes previo de L1, DeepSeek pierde un punto de Network u Output en el 22 % de sus decisiones reales; donde se aparta del planificador perfecto, elige gestos de integridad en público;
  - en el banco, Sonnet rechaza «aclarar por escrito después» y «pedirlo en privado» como riesgo oculto (sus notas lo dicen);
  - en el catálogo, las opciones redactadas en privado / después / por escrito llevan riesgo ≥ 2 sólo el 11 % de las veces y pierden Network u Output el 25 %; plantarse en público, negarse o insistir las pierde el 46–64 %, sin ser menos arriesgado.
  - Réplica: +0,35 (sólo en el mes previo de L1; en todos los meses, −0,5 por más crisis).
  - Sonnet en el banco de L1 (78 situaciones comunes): pérdida por decisión 4,71 → 3,90, y cambia justo las decisiones previstas.
- **Pendiente:** banco de L1 con DeepSeek (plan, paso 3). Tercer intento en una dirección parecida (t13-read-v9, cp-v9 no movieron el banco), pero por otro mecanismo: no es una pista de lectura, sino una preferencia acotada a un mes y a un nivel.

### `ex-s1` (padre: ex-v1): el script con estado (C49, C60)
- `script/brief.py`: el agente le pasa, en una tercera llamada de cada respuesta, diez cifras del `observe` que acaba de contestar; el script guarda el registro de la partida en un archivo con el nombre del `session_id` (una partida nueva no abre el de otra) y devuelve una línea:
  - Best del nivel y qué está por debajo;
  - indicadores «llenos» (comprados en el trimestre sin que subieran, anclados a su valor, B38);
  - avisos de salud, arranque atascado y explosiones;
  - en los meses de trimestre, el plan en números del menú.
- **Probado sin DeepSeek:**
  - con las 23 partidas reales de la familia (`scripts/exploracion/test_brief.py`), 1.470 marcas de «lleno» y ninguna falsa;
  - réplica: detectar techos así vale **+0,0** (+0,6 sólo si se conocieran de antemano, que en partida no se puede);
  - las notas de DeepSeek ya llevan bien el estado («Now» correcto en 3.200 de 3.211 notas), así que la memoria del script no arregla nada medible.
- **Para qué sirve:** responder con datos a la pregunta 3 del vídeo («¿por qué scripts o por qué no?») y tener el bucle de tres llamadas probado por si una idea futura necesita estado.
- **Riesgo:** la tercera llamada puede romper la pareja. No entregar sin sondas (plan, paso opcional).

### `ex-v2` (padre: ex-v1): descartado
Revisión de la opción elegida en el mes previo de L1 («¿podría molestar o quitar tiempo o mérito?»). Sonnet en el banco de L1: 24 frente a 24 elecciones que bajan Network u Output. La réplica ya decía que una revisión con falsas alarmas resta (−3,7 con un 20 %). No probar con DeepSeek.
