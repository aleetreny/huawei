# Calidad de los SKILL.md (10 % de la nota automática)

**Conclusión en una frase:** nuestro manual entregado (`t13-read-v4`) saca unos 60–64 con Haiku y Sonnet (72–74 con Opus). Una reescritura que no toca las decisiones (`calidad/v4-c5`) lo sube unos 4 puntos de media entre los tres jueces (+8 con Haiku, +4 con Sonnet, +0,5 con Opus), sin cambiar lo que elige Haiku en el banco más que repetir el propio v4. Son ≈ +0,4 de nota automática gratis; falta confirmarlo con DeepSeek (≈ 1,3 USD) antes del corte 2.

Línea abierta el 28 oct 2026. Pregunta: *¿cuánto saca nuestro SKILL.md en la nota de calidad y cómo subirla sin cambiar cómo juega DeepSeek?*

## 0. Lo que dicen las normas

- La nota automática de cada versión es 0,80 × partidas + **0,10 × calidad de los documentos** + 0,10 × fichas (`competition-rules.rst`).
- Cada `SKILL.md` se puntúa de 0 a 100 «como instrucciones para el agente», y la nota es **la media de los Skills** de la entrega. Los documentos de `design/` no cuentan aquí; sólo los lee el jurado.
- Una nota alta exige:
  - que el agente encuentre el Skill y sepa cuándo usarlo (descripción);
  - pasos ejecutables, con prioridades y criterios, y qué hacer cerca de un límite;
  - una estrategia que encaje con las reglas publicadas y mire los 48 meses;
  - que siga valiendo si cambian la redacción o el orden de los eventos.
- **Nota 0** si:
  - falta el *front matter* o es inválido;
  - el Skill está vacío o no tiene que ver con su descripción;
  - contradice el juego;
  - contiene conducta prohibida, como una respuesta fija para un evento con nombre.
- No se publica qué modelo puntúa. **No tenemos la nota de calidad del corte 1.**

**Cuánto vale:** 10 puntos de calidad son 1 punto de nota automática. Para sacar lo mismo jugando harían falta 1,25 puntos más de media en las partidas.

## 1. El juez

`scripts/calidad-skills/judge.py` le pasa a un modelo de Claude, por la CLI:
- la rúbrica oficial literal;
- las reglas publicadas (`handbook.rst`, `rules.rst`, `failure-and-ending.rst` y la parte de contenidos prohibidos de `competition-rules.rst`);
- el SKILL.md.

Pide una nota de 0 a 100, ocho subnotas de 0 a 10, las condiciones de nota 0 que vea y las tres debilidades que más restan. Es un **sustituto para comparar versiones**, no la nota oficial. Trabajo previo con un revisor de Sonnet: [transmision/fase3-rubrica.md](../transmision/fase3-rubrica.md) y [palancas/nota-memoria.md §6](../palancas/nota-memoria.md) (ruido de ±6 con 3 lecturas).

### Calibración (`data/j01-calibracion.jsonl`, 90 lecturas, Haiku y Sonnet × 3)

| Archivo | palabras | haiku (media ± dt, min–max) | sonnet (media ± dt, min–max) | ceros |
|---|---:|---:|---:|---|
| deepseek/t13-read-v1 → career-rules | 1155 | 64.7 ± 1.9 (62–66) | 69.0 ± 2.2 (66–71) |  |
| deepseek/t13-read-v7 → career-rules | 1670 | 60.0 ± 6.5 (52–68) | 70.0 ± 2.8 (66–72) |  |
| f1-steady-balance/f1-steady-balance-v1 → steady-balance | 486 | 62.7 ± 2.5 (60–66) | 64.0 ± 1.6 (62–66) |  |
| deepseek/t13-read-v4 → career-rules | 1609 | 62.0 ± 3.3 (58–66) | 62.0 ± 0.0 (62–62) |  |
| formato/script-v1 → career-advisor | 1063 | 61.0 ± 2.2 (58–63) | 54.0 ± 2.8 (52–58) |  |
| matteo-feedback-growth/observed-growth-v4 → observed-growth | 592 | 53.7 ± 1.2 (52–55) | 59.7 ± 2.4 (58–63) |  |
| transmision/t8-quarter → career-rules | 285 | 54.0 ± 1.4 (52–55) | 50.0 ± 1.6 (48–52) |  |
| f3-feedback-reactive/f3-lean-v1 → feedback-response | 250 | 45.3 ± 3.8 (40–48) | 52.0 ± 0.0 (52–52) |  |
| calibracion/umbral.md | 1632 | 39.0 ± 27.7 (0–62) | 42.7 ± 5.2 (38–50) | {'haiku:contradicts_game': 1} |
| deepseek/native-craft-v1 → career-craft | 326 | 42.7 ± 2.5 (40–46) | 32.0 ± 1.4 (30–33) |  |
| deepseek/decisional-check-v1 → career-craft | 453 | 37.7 ± 2.9 (34–41) | 33.0 ± 4.5 (27–38) |  |
| p0-minimal/p0-minimal-v1 → career-play | 137 | 24.0 ± 3.3 (20–28) | 14.0 ± 0.0 (14–14) |  |
| calibracion/contradice.md | 1630 | 0.0 ± 0.0 (0–0) | 7.3 ± 10.4 (0–22) | {'haiku:contradicts_game': 3, 'sonnet:contradicts_game': 3} |
| calibracion/plantilla.md | 27 | 0.0 ± 0.0 (0–0) | 3.0 ± 0.0 (3–3) | {'haiku:empty_or_unrelated': 3, 'sonnet:empty_or_unrelated': 5} |
| calibracion/evento-fijo.md | 1621 | 0.0 ± 0.0 (0–0) | 0.0 ± 0.0 (0–0) | {'haiku:prohibited_conduct': 3, 'sonnet:prohibited_conduct': 3} |

- **Los dos jueces ordenan igual los manuales.** Los largos y estructurados (t13-read, f1) sacan 60–70; los cortos sin pasos ejecutables (p0-minimal, native-craft), 14–43.
- **Aplican las condiciones de nota 0:**
  - una respuesta fija para un evento inventado saca 0 en las 6 lecturas;
  - una regla que contradice el manual publicado, 0–22;
  - la plantilla vacía, 0–3.
- **Un umbral de ascenso sin publicar presentado como regla no siempre va a 0:** se castiga hasta ~40, y sólo 1 de cada 6 lecturas lo pone a 0. El juez oficial puede ser más severo: no hay que arriesgarse.

## 2. Nuestro manual entregado y sus reescrituras

`data/j02-reescritura.jsonl`: Haiku y Sonnet × 3 y Opus × 2 por versión, en la misma tanda.

**Juez sin el manual del juego** (`j02`):

| Archivo | palabras | haiku (media ± dt, min–max) | opus (media ± dt, min–max) | sonnet (media ± dt, min–max) | ceros |
|---|---:|---:|---:|---:|---|
| calidad/v4-c2 → career-rules | 2023 | 70.0 ± 2.8 (66–72) | 72.0 ± 0.0 (72–72) | 70.7 ± 3.4 (66–74) |  |
| calidad/v4-c3 → career-rules | 2020 | 68.7 ± 5.2 (64–76) | 74.0 ± 0.0 (74–74) | 70.3 ± 1.7 (68–72) |  |
| calidad/v4-c4 → career-rules | 1731 | 63.0 ± 3.0 (60–66) | — | 71.5 ± 0.5 (71–72) |  |
| calidad/v4-c1 → career-rules | 1973 | 60.0 ± 5.9 (52–66) | 75.5 ± 1.5 (74–77) | 65.0 ± 1.4 (63–66) |  |
| deepseek/t13-read-v4 → career-rules | 1609 | 62.7 ± 2.5 (60–66) | 74.0 ± 0.0 (74–74) | 60.0 ± 1.6 (58–62) |  |
| calidad/v4-c4 → career-status-note | 451 | 46.5 ± 1.5 (45–48) | — | 23.0 ± 1.0 (22–24) |  |

**Juez con el manual que devuelve `show_employee_handbook`** (`j04`, el que queda por defecto en `judge.py`):

| Archivo | palabras | haiku (media ± dt, min–max) | opus (media ± dt, min–max) | sonnet (media ± dt, min–max) | ceros |
|---|---:|---:|---:|---:|---|
| calidad/v4-c2 → career-rules | 2023 | 72.7 ± 0.9 (72–74) | 73.5 ± 0.5 (73–74) | 68.3 ± 2.1 (66–71) |  |
| calidad/v4-c5 → career-rules | 2099 | 68.0 ± 3.5 (64–72) | 72.5 ± 0.5 (72–73) | 67.3 ± 1.9 (66–70) |  |
| deepseek/t13-read-v4 → career-rules | 1609 | 60.2 ± 3.0 (55–64) | 72.0 ± 0.0 (72–72) | 63.0 ± 2.8 (58–66) |  |

**Lectura:**
- **v4** saca 59–64 con Haiku y Sonnet y 72–74 con Opus. Lo que más le resta, en las 6 lecturas: presentar las pistas de lectura como reglas del juego («encaja con las reglas» ≈ 5,5–6) y la densidad del texto (claridad ≈ 4,6).
- **Los jueces encontraron errores reales de v4:**
  - N = 1 aparece con dos nombres;
  - «Repair a key relationship», que es una acción principal, está en una lista de energía;
  - en el último trimestre se gasta más energía de la que hay.
- **c2 sube +8 a +14 con Haiku, +4 a +11 con Sonnet y nada con Opus** (−2 a +1,5). Media de los tres jueces en las dos tandas: v4 65,3 → c2 71,2.
- **c2 tenía dos errores introducidos por la reescritura**, que también señalaron los jueces:
  - decía que desde el mes 46 no quedaba evaluación, cuando el mes 47 cuenta para la del 48;
  - presentaba la explosión de riesgo como hecho sin citar el manual del juego, que es donde se dice.
  
  **c5** los corrige, describe el momento de la evaluación tal como se ve en la partida y clasifica el comentario de RR. HH. por su tono. Con el juez definitivo (6 lecturas de Haiku y de Sonnet, 2 de Opus) saca 68,0 / 67,3 / 72,5 frente a 60,2 / 63,0 / 72 de v4: **+4,2 de media**. c2 sacaba algo más (72,7 / 68,3 / 73,5, +6,4), pero con dos errores. **c5 es el candidato**: correcto antes que dos puntos de juez.
- **c3 (reestructurado por Sonnet) no mejora a c2.** Con las decisiones congeladas, el techo está en ~70–74.
- **c4 (dos Skills) baja la media.** El Skill corto de la nota saca 23–46, porque se le exige la misma rúbrica de estrategia. **Un solo Skill.**

Qué cambia cada versión (todas en `lab/policies-src/calidad/`; ninguna añade una regla de historias):
- **v4-c1:** sólo arregla redacción.
  - Las pistas de lectura pasan a ser «nuestros supuestos de trabajo», no reglas del juego.
  - N = 1 se llama siempre «el último mes antes de una evaluación» (v4 lo llamaba también «el mes de la evaluación»).
  - Se separan las acciones de energía de las principales: v4 ponía «Repair a key relationship», que es principal, en una lista de energía.
  - Se aclara la energía del último trimestre (v4 listaba más de 3 puntos).
  - Se añade un resumen de los 48 meses y se explica para qué sirve la línea de estado y cómo rehacerla si se pierde.
- **v4-c2:** c1 más límites concretos.
  - Margen propio declarado para Health y Dignity: «4 o menos, no es un límite publicado».
  - Qué hacer con Wealth bajo cero y con Network a cero, que son rutas de derrota publicadas.
- **v4-c3:** c2 reestructurado por Sonnet con las decisiones congeladas.
- **v4-c4:** c2 con la línea de estado en un segundo Skill.

## 3. ¿Cambia lo que elige el modelo? (banco)

Banco de obediencia de la línea Transmisión (`lab/data/transmision/bank-items.jsonl.gz`) con Haiku (CLI 2.1.312) en la entrega oficial del Skill. 244 situaciones sin títulos reservados:
- 49 de antes de una evaluación;
- 55 detonantes;
- 32 de ruina temprana;
- 58 del bloque general;
- 30 repartos con salud baja;
- 20 repartos de cierre.

Brazos: v4, v4 repetido (v4b), c2 y c5. La pérdida es la nota final media del simulador de la mejor opción menos la de la elegida (`scripts/calidad-skills/compare_bank.py`, bootstrap 95 %). Datos en `~/careerlab-data/calidad-skills/bank/runs/` (llevan texto del juego; fuera de Git).

**c5 frente a v4:**

situaciones comunes: 244
| Tipo | n | misma eleccion hk-v4 vs hk-c5 | perdida hk-v4 | perdida hk-c5 | diferencia (IC 95 %) |
|---|---:|---:|---:|---:|---|
| closing/q | 20 | 60% | 0.11 | 0.10 | -0.01 (-0.06, +0.04) |
| early_ruin/e | 32 | 94% | 0.89 | 0.93 | +0.04 (-0.03, +0.14) |
| general/e | 58 | 95% | 0.58 | 0.56 | -0.02 (-0.19, +0.16) |
| low_health/q | 30 | 87% | 0.67 | 0.70 | +0.02 (-0.08, +0.15) |
| pre_review/e | 49 | 90% | 1.61 | 1.82 | +0.21 (-0.14, +0.79) |
| trigger/e | 55 | 93% | 1.93 | 1.65 | -0.27 (-1.06, +0.24) |
| **todas** | 244 | 89% | 1.11 | 1.09 | -0.02 (-0.23, +0.16) |

repeticion hk-v4 vs hk-v4b: 224/244 = 92% misma eleccion

**c2 frente a v4:**

situaciones comunes: 244
| Tipo | n | misma eleccion hk-v4 vs hk-c2 | perdida hk-v4 | perdida hk-c2 | diferencia (IC 95 %) |
|---|---:|---:|---:|---:|---|
| closing/q | 20 | 90% | 0.11 | 0.08 | -0.03 (-0.10, +0.00) |
| early_ruin/e | 32 | 94% | 0.89 | 0.93 | +0.04 (-0.03, +0.14) |
| general/e | 58 | 91% | 0.58 | 0.67 | +0.09 (-0.14, +0.34) |
| low_health/q | 30 | 97% | 0.67 | 0.72 | +0.05 (+0.00, +0.15) |
| pre_review/e | 49 | 94% | 1.61 | 1.79 | +0.18 (-0.12, +0.69) |
| trigger/e | 55 | 93% | 1.93 | 1.83 | -0.10 (-0.97, +0.58) |
| **todas** | 244 | 93% | 1.11 | 1.15 | +0.04 (-0.18, +0.23) |

- **Ninguna reescritura cambia lo que elige Haiku más que repetir v4.** Misma elección en el 89–93 %, frente al 92 % de v4 consigo mismo. La pérdida no cambia: −0,02 (IC −0,23 a +0,16) con c5 y +0,04 (IC −0,18 a +0,23) con c2.
- **Dónde se nota c5:**
  - en el cierre trimestral, con 60 % de coincidencia frente al 80 % de la repetición; son cambios entre acciones de igual valor (Prepare report materials ↔ Network maintenance);
  - en salud baja, 4 de 30 repartos cambian (la repetición, 0 de 30), sin coste.
  
  Es el efecto esperado de la línea «Near a limit».
- **Esto vale para Haiku.** DeepSeek ya se ha portado distinto con el mismo texto (HALLAZGOS C7, C3).

## 4. Qué hacer con los 3 USD de DeepSeek

Aquí no se ha gastado nada: este contenedor no tiene la clave, que sólo está en el `.env` del Mac de Alejandro. Lo que rinde cada dólar:

| Uso | Coste | Qué nos dice | ¿Merece la pena? |
|---|---:|---|---|
| Juez con DeepSeek (`ds_judge.py`): v4, c2 y c5, 5 lecturas | ≈ 0,2 USD | Si quien puntúa es el modelo designado, si también ve la mejora | **Sí**: barato y es el sustituto más fiel del juez oficial |
| Banco con DeepSeek: v4 y c5 sobre las 320 historias de `ids-ds1-events` | ≈ 1,1 USD (0,0017 USD por situación, [obediencia.md](../deepseek/obediencia.md)) | Si c5 cambia lo que elige DeepSeek. Ruido de referencia ya medido: DeepSeek repite el 91 % (B21), así que no hace falta pagar un brazo repetido | **Sí, antes de entregar c5**: la mejora vale ≈ +0,4 de nota y un cambio de juego podría costar más |
| Partidas completas | 0,4–0,8 USD cada una | Casi nada: ~4 partidas, y harían falta ~45 por brazo para ver 5 puntos | **No** |

**Total ≈ 1,3 USD de los 3 aprobados.** Comandos (en el Mac, en la carpeta del repo):

```bash
uv run python scripts/calidad-skills/ds_judge.py --out lab/reports/calidad-skills/data/j03-deepseek.jsonl --reps 5 --budget 0.40 lab/policies-src/deepseek/t13-read-v4 lab/policies-src/calidad/v4-c2 lab/policies-src/calidad/v4-c5
```

```bash
uv run python scripts/deepseek/bench.py run --variant lab/policies-src/deepseek/t13-read-v4/bundle --name ds-v4 --ids ~/careerlab-data/deepseek/ids-ds1-events.txt
```

```bash
uv run python scripts/deepseek/bench.py run --variant lab/policies-src/calidad/v4-c5/bundle --name ds-v4-c5 --ids ~/careerlab-data/deepseek/ids-ds1-events.txt
```

```bash
uv run python scripts/deepseek/paired.py --a ds-v4 --b ds-v4-c5 --phase e
```

**Regla de decisión:** entregar c5 en el corte 2 si DeepSeek elige lo mismo en ≥ 88 % de las historias (su repetición da 91 %) y la pérdida no empeora con un IC que excluya 0. Si empeora, volver a v4 y aplicar sólo los arreglos de errores (N = 1, Repair en la lista de energía, energía del último trimestre).

## 5. Conclusiones

1. **La calidad del documento es una palanca pequeña pero gratis.** Sube unos 4 puntos de calidad (c5), es decir, ≈ +0,4 de nota automática, sin tocar el juego. Con más reescritura de texto se puede llegar a +6 (c2), pero hay que vigilar no meter errores.
2. **El techo, con las decisiones actuales, es ~70–74.** Lo que falta hasta 100 es justo lo que hace jugar bien a DeepSeek: las pistas de lectura (que los jueces ven como mecánicas inventadas) y la línea de estado (que ven como pesada). No compensa quitarlas: el 80 % de la nota sale de las partidas.
3. **Un solo Skill.** Repartir en varios baja la media, porque cada Skill se juzga como estrategia completa, y además se pierden reglas al jugar (B13).
4. **Lo que más puntúa sin riesgo:**
   - decir qué es publicado y qué es supuesto nuestro;
   - concretar qué hacer cerca de cada límite publicado (Health, Dignity, Wealth bajo cero, Network a cero);
   - un resumen de los 48 meses que sea coherente con el resto del texto.
5. **Revisar con un juez encuentra errores reales del manual**, no sólo de estilo: en v4, tres (N = 1, Repair en la lista de energía, la energía del último trimestre); en la primera reescritura, dos que había metido yo (el final de carrera y una afirmación sin fuente). **Conviene pasar el juez a cada versión antes de entregarla.**
6. **No pongas nunca un número de umbral como regla.** El juez lo castiga hasta ~40 aunque no lo ponga a 0, y el oficial puede ser más duro.

## Archivos

| Archivo | Qué hace |
|---|---|
| `scripts/calidad-skills/judge.py` | juez con Claude (Haiku, Sonnet, Opus) sobre la rúbrica oficial |
| `scripts/calidad-skills/ds_judge.py` | el mismo juez con DeepSeek, con tope de gasto propio (sólo en el Mac de Alejandro) |
| `scripts/calidad-skills/summary.py` | tabla de notas, subnotas y condiciones de 0 |
| `scripts/calidad-skills/compare_bank.py` | compara brazos del banco: misma elección y pérdida por tipo de situación |
| `lab/reports/calidad-skills/calibracion/` | casos trampa del juez (nunca se entregan) |
| `lab/reports/calidad-skills/data/` | juicios en JSONL (sin texto del juego) |
| `lab/policies-src/calidad/` | reescrituras de `t13-read-v4` |

## Relevo

**Qué se hizo (28 oct).**
1. Juez de la rúbrica oficial con Claude, calibrado con 11 manuales y 4 casos trampa.
2. Nota del manual entregado (v4).
3. Cinco reescrituras (c1–c5) puntuadas con tres jueces.
4. Banco de comportamiento con Haiku: 4 brazos × 244 situaciones.
5. Plan de DeepSeek preparado.

**Resultados.** §1–§3. Candidato: `lab/policies-src/calidad/v4-c5` (mismas decisiones que v4, ≈ +4 de calidad, mismo comportamiento con Haiku).

**Qué falta.**
- Confirmar con DeepSeek (§4, ≈ 1,3 USD, en el Mac de Alejandro).
- Que la línea DeepSeek decida si c5 entra en el corte 2. Si cambian el manual de base (por ejemplo, una variante de v4 contra la trampa de L1), hay que aplicarle los mismos arreglos de texto y volver a pasar el juez.
- No sabemos qué modelo puntúa de verdad ni tenemos la nota de calidad del corte 1. Si se publica, sirve para calibrar estos jueces.

**Cuota.** Unas 140 llamadas de juez (Haiku, Sonnet, Opus) y unas 980 sesiones de banco con Haiku. La semana siguió en el 42 % durante todo el trabajo (tope de hoy: 45 %). 0 USD de DeepSeek.

**Para retomar.**

```bash
python3 scripts/calidad-skills/judge.py --out lab/reports/calidad-skills/data/j05.jsonl --models haiku,sonnet --reps 3 <carpeta del manual>
```

```bash
python3 scripts/calidad-skills/summary.py lab/reports/calidad-skills/data/j05.jsonl
```

```bash
gunzip -c lab/data/transmision/bank-items.jsonl.gz > ~/careerlab-data/calidad-skills/bank/items.jsonl
```

```bash
TRANSMISION_DATA=~/careerlab-data/calidad-skills/bank CAREERLAB_CLAUDE_EXE=$(which claude) uv run python scripts/transmision/runbench.py run --items ~/careerlab-data/calidad-skills/bank/items.jsonl --variant <bundle> --name hk-<brazo> --ids ~/careerlab-data/calidad-skills/bank/ids-calidad.txt --slots 4
```

```bash
TRANSMISION_DATA=~/careerlab-data/calidad-skills/bank python3 scripts/calidad-skills/compare_bank.py --a hk-v4 --b hk-<brazo>
```

`ids-calidad.txt` se regenera con la selección estratificada descrita en §3 (semilla 28). Su lista está en `data/ids-calidad.txt`.
