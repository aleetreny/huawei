# Línea Techo: que las partidas que terminan no se queden en L5 con ~70

**Pregunta.** Las partidas completas de DeepSeek con `t13-read-v4` ascienden en los meses 6, 12, 24 y 42, acaban en L5 con Skill 103–122 y sacan ~70. ¿Qué reglas generales (sin umbrales, sin títulos) hacen que no pierda las ventanas del 18 y del 30/36 y llegue a L6, sin empeorar la protección del primer ascenso?

**Estado (28 oct, en curso).** Subtrabajo de la línea DeepSeek. Rama `alejandro/tender-franklin-3ap5yw`. Sólo réplica, bots y jueces de Claude: 0 USD. Datos en `lab/reports/techo/data/` (sin texto del juego).

**Conclusiones hasta ahora** (se actualizan abajo):
1. Con lectura perfecta, las reglas de v4 llegan a L6 el 14–16 % de las veces; el planificador óptimo, el 76 %. La diferencia es de **regla**, no sólo de lectura: el planificador asciende a L4 en el mes 20 (v4: 24) y a L5 en el 36 (v4: 42).
2. La ventana del **mes 18** se pierde en L3 por **Network** (227 de ~430 fallos del bot v4: Network corto al empezar el mes previo). Las del **30 y 36**, por el ritmo de Skill en L4 (3,1 al mes frente a 3,9 del planificador; el trimestre aporta 0,28 frente a 0,76).
3. Las palancas de trimestre solas mueven poco: Skill learning + rotación desde L4 da +0,5 y L6 del 16 % al 25 % (lectura exacta); desde L3 empeora (−1,7); techos conocidos (detección perfecta de estancamiento) +1,2. Coincide con Leah ([07](../../reports/historico/) en `leah/workspace`) y hacia-80 §7 (`alejandro/deepseek`).

## 1. Montaje

- `scripts/techo/techobot.py`: bot de la réplica que sigue **las reglas de `calidad/v4-c5` tal como están escritas** (supervivencia, riesgo estricto con la excepción del mes previo, bienestar, cierre de evaluación con Best, crecer contando signos; trimestre como lo juega DeepSeek: informes, red, informes, proyecto clave) sobre una **percepción imperfecta**:
  - `exact`: signos exactos (cota);
  - `noisy`: signos exactos degradados con las tasas medidas en DeepSeek (Skill↑ vista 78 %, Output↓ 47 %, Network↓ 79 %, riesgo 86 %, falsas alarmas de riesgo 22 %, «R−» de más 10 %). Es demasiado pesimista en crisis (32 % frente a ~9 % del LexBot con etiquetas reales de DeepSeek): el ruido real está correlacionado con las palabras, no es uniforme. Sirve para comparar brazos con las mismas semillas, no para cifras absolutas;
  - `haiku`: etiquetas reales de Haiku (`question-bank/stat-tags.json`), sin riesgo. Resulta inútil (21 % de muertes por salud): no se usa.
  
  Comprobación: con lectura exacta saca 59,1–59,4 y 36 crisis de 400, igual que el `LexBot` de la línea DeepSeek con los mismos flags (58,9; 33 crisis).
- `scripts/techo/diag.py`: por evaluación, cuántas partidas llegan vivas, cuántas ascienden y, si no, qué indicador falta y si ya faltaba al empezar el mes previo; ritmo de Skill por nivel y parte que aporta el trimestre; mes medio de cada ascenso. Brazos: `planner` (política óptima, efectos exactos), `sp` (planificador que sólo ve signos ±1 y marca de riesgo, con ablaciones) y cualquier flag de `techobot`.
- Semillas comunes entre brazos (`4242+i`); 1.000–2.000 partidas por brazo; error típico de la nota ≈ 0,35–0,45.

## 2. Diagnóstico (lectura exacta, 1.000 partidas) — `data/diag-exact.txt`

| | Planificador | Reglas v4 | v4 + techos conocidos | v4 + Skill en el trimestre desde L4 |
|---|---:|---:|---:|---:|
| Nota | 73,1 | 59,4 | 60,5 | 59,9 |
| L6 | 76 % | 14 % | 21 % | 23 % |
| Ascenso a L3 (mes medio) | 13,2 | 14,7 | 14,6 | 14,7 |
| Ascenso a L4 | 20,0 | 24,3 | 24,0 | 24,3 |
| Ascenso a L5 | 36,4 | 42,0 | 41,3 | 41,1 |
| Skill al mes en L3 / L4 / L5 | 3,1 / 3,9 / 3,7 | 2,2 / 3,1 / 3,1 | 2,3 / 3,4 / 3,1 | 2,2 / 3,6 / 3,5 |
| …del trimestre, L4 | 0,76 | 0,28 | 0,48 | 0,74 |

Por qué no asciende en cada ventana (bot v4):
- **m18:** L3 con Network corto al empezar el mes previo (106), Network y Output cortos (82), Skill y Network (39). Network empieza L3 bajo (el ascenso cuesta Network, y más si llega a los 6 meses) y las reglas de v4 cuentan los tres indicadores igual: una opción «Skill + Output» gana a una «Network».
- **m30 y m36:** L4 con Skill corto (382 y 508). Es un problema de ritmo: 48 puntos de Skill entre el techo de L3 y el umbral de L4.
- **m42 y m48:** L5 con Skill corto. Quien llega a L5 en el 42 no tiene tiempo.

## 3. Palancas probadas (2.000 partidas por brazo) — `data/battery1-*.txt`

| Palanca | exact: nota / L6 / Skill final | noisy: nota / L6 |
|---|---|---|
| v4 (base) | 59,4 / 16 % / 118 | 40,6 / 1 % |
| Skill en el trimestre desde L4 (`qskill=4`) | 59,8 / **25 %** / 127 | 40,9 / 2 % |
| … desde L3 | 57,7 / 13 % | 38,7 / 1 % |
| … desde L5 | 59,3 / 18 % | 40,6 / 1 % |
| Estancamiento por comparación trimestral (`qstall`) | 58,5 / 18 % | 39,8 / 1 % |
| Techos conocidos (`caps`, cota) | **60,5** / 23 % / 123 | 41,6 / 2 % |
| Detección de v4 (`detect`) | 59,4 / 19 % | 40,3 / 1 % |
| Skill doble en historias desde L4 (`sskill=4`) | 59,7 / 18 % | 40,8 / 1 % |
| Reconstruir primero el indicador que cayó al ascender (`pfall`) | 59,5 / 16 % | 40,5 / 1 % |
| C40: en L1 con RR. HH. «quiet», trimestre a crecer (`q3l1`) | 59,4 / 16 % | 40,5 / 1 % |
| `qskill=4+pfall` | 60,0 / 25 % | 40,8 / 2 % |

Lectura: ninguna regla de trimestre ni de prioridad pasa de +0,6 ni lleva L6 más allá del 25 % con lectura perfecta. **La detección de estancamiento por «no ha subido en el trimestre» es peor que nada** (marca indicadores que simplemente no tuvieron ocasión y deja de invertir en ellos; sube los despidos). El margen grande está en otra parte: en cómo elige las historias en L2–L4.

## 4. Qué parte de la ventaja del planificador es regla — `data/diag-signplanner-exact.txt`, `data/diag-sp-noprivilege-exact.txt`

Planificador ajustado (`politica_optima.json`) que en las historias **sólo ve signos ±1 y la marca de riesgo** (como DeepSeek con lectura perfecta), 1.000 partidas, lectura exacta:

| Variante | Nota | L6 | L4 en el mes | L5 en el mes |
|---|---:|---:|---:|---:|
| Planificador con efectos exactos | 73,1 | 76 % | 20,0 | 36,4 |
| Sólo signos (`sp`) | 69,1 | 60 % | 20,9 | 37,8 |
| … con magnitudes pero riesgo sólo como marca | 71,5 | 72 % | | |
| `sp` sin umbrales (usa los techos) | 63,9 | 46 % | 21,2 | 38,5 |
| `sp` sin refuerzo del mes previo | 65,8 | 48 % | 22,2 | 38,8 |
| `sp` sin valorar Health y Dignity | 66,7 | 56 % | | |
| `sp` con el mismo peso por encima y por debajo del umbral | 67,1 | 43 % | 22,3 | 39,6 |
| `sp` con el trimestre de v4 | 67,5 | 43 % | 21,4 | 39,4 |
| `sp` sin continuación de la historia | 68,6 | 61 % (crisis ×2) | | |
| **`sp` sin umbrales y con el trimestre de v4** (lo que puede saber DeepSeek) | **62,7** | **29 %** | 21,6 | 39,8 |
| … y además con el suelo de salud de v4 (4 en vez de 2) | **64,8** | **33 %** | 21,5 | 39,7 |
| … y además riesgo estricto (una marcada sólo si no hay otra) | 59,6 | 18 % | 24,8 | 41,8 |
| Reglas de v4 (`techobot` base) | 59,4 | 14 % | 24,3 | 42,0 |

**Lectura.**
- Sin información privilegiada (ni umbrales ni efectos exactos ni trimestre con techos), el planificador de signos sigue sacando **64,8 frente a 59,4** de las reglas de v4 y llega a L4 tres meses antes (21,5 frente a 24,3).
- **Casi toda esa diferencia es el riesgo:** al hacerlo estricto (como el paso 2 de v4), cae a 59,6, el ascenso a L4 vuelve al mes 24,8, y en L3 gana menos Skill (2,3 frente a 2,6 al mes) y menos Network (1,8 frente a 2,3). En L1 pasa del 78 % al 61 % de ascensos en el mes 6, casi todo por Network perdido en el mes previo (152 casos).
- El planificador toma una opción marcada **voluntariamente** 6,4 veces por partida (`data/riskwhen-sp.txt`): el 81 % con el contador de riesgo a 0, el 44 % en los dos meses previos a una evaluación, y casi siempre porque **la mejor opción segura perdía un indicador (1.250 casos) o no ganaba nada (1.201)** mientras la marcada ganaba uno o dos. Riesgo real medio de esas opciones: 1,6.
- El suelo de salud ajustado del planificador (2) es demasiado bajo para jugar con signos: con 4, +2,1 y la mitad de muertes por salud. El de v4 (4) está bien.
- La continuación de la historia (ver el siguiente paso) vale poco en nota pero **dobla las crisis** si falta. Una IA no puede verlo; sí puede desconfiar de opciones que llevan a situaciones sin salida.

## 5. Tolerancia al riesgo en el bot de v4 — `data/battery2-exact.txt`, `data/battery3-exact.txt`

Copiar la regla del planificador al bot de v4 **sin más** empeora: aceptar una opción marcada cuando RR. HH. está amable, no se ha tomado riesgo este mes y ninguna opción segura crece (`rt=safe0`) baja de 59,4 a 57,9 (crisis 179 → 221 de 2.000; despidos 175 → 183). Pedirle dos indicadores más de ventaja (`risktol=2`), 58,4. La diferencia con el planificador: éste sólo cuenta las subidas que **caben** (por debajo del techo) y sabe el contador vivo; el bot de v4 no sabe qué subidas valen nada y en L1 (Network y Output llenos casi siempre) toma riesgos por subidas inútiles. Comprobación en §6.

Otras: proteger Dignity desde 7 en vez de 4 (`dprot=7`), +0,4 y menos crisis (el aviso de la evaluación depende de Dignity; la Dignity alta evita el +1 de riesgo del aviso); proteger Health sólo desde 2, −0,4 y más muertes; contar doble las pérdidas, 0.

## 6. Lo que aguanta con las dos lecturas (2.000 partidas por brazo) — `data/battery4-exact.txt`, `data/battery5-*.txt`, `data/battery6-detect-exact.txt`

| Regla (sobre v4) | exact: nota / L6 / Skill final | noisy: nota / L6 / Skill final |
|---|---|---|
| v4 (base) | 59,4 / 16 % / 118 | 40,6 / 1 % / 101 |
| Trimestre a Skill desde L4 (`qskill=4`) | 59,8 / 25 % / 127 | 40,9 / 2 % / 108 |
| Dignity protegida desde 7 (`dprot=7`) | 59,8 / 17 % / 118 | 41,0 / 1 % / 100 |
| Las dos | 60,3 / 25 % / 127 | 41,3 / 2 % / 108 |
| Las dos + Skill doble en historias desde L4 (`sskill=4`) | **60,5 / 26 % / 128** | **41,5 / 2 % / 109** |
| Las dos + Skill learning sólo con Health > 6 | 60,6 / 26 % / 126 | 41,5 / 2 % / 107 |
| Las dos + marca Stalled anclada al valor (`detect`) | 60,6 / 26 % / 128 | — |
| Las dos + techos conocidos (cota) | 60,9 / 27 % / 128 | 42,3 / 3 % / 110 |
| Network doble en historias hasta L3 (`ndouble=3`) | 58,9 (peor) | 39,6 (peor) |
| Proteger S/N/O todos los meses de L1, tras el riesgo (`pl1=safe`) | 59,6 | 41,1 (igual) |
| … antes del riesgo (`pl1=first`) | 58,3, despidos 175 → 217 | — |
| Tolerancia al riesgo tipo planificador (`rt=safe0`, con o sin techos, desde L2 o L4) | 57,7–59,6, crisis +20–40 % | — |
| Tolerancia sólo para opciones que suben Network en L1–L3 (`rtn`, `data/battery7-rtn-exact.txt`) | 58,8–59,1, despidos 175 → 197 | — |

**Lectura.**
- Lo que sube con las dos lecturas y no toca L1: **trimestre a Skill desde L4, Dignity protegida desde 7 y Skill doble en las historias desde L4**: +1,1 (exacta) / +0,9 (ruidosa), L6 del 16 % al 26 % con lectura exacta, Skill final +10. Es poco en nota (una partida de 70 pasa a ~71) y **no basta para L6 con la lectura de DeepSeek** (1 % → 2–3 %).
- **La marca «Stalled» de v4 no vale nada tal como está definida** (se borra cuando el indicador «vuelve a subir», y como no sube nunca más en el nivel, lo que la rompe son las bajadas: una pérdida deja la marca puesta sobre un indicador que ya tiene hueco y el bot deja de invertir en él; 34 % de marcas falsas en Network de L1). **Anclada al valor** («Stalled: N at 7», se quita sólo cuando Now baja de ese valor o cambia el nivel) recupera casi todo lo que vale conocer los techos (+0,7 frente a +1,2 sobre v4). Vale para un script de línea de estado o para el texto; DeepSeek no la rellena (C18), así que en el texto es poco útil y la condición «nivel 4 o más» hace su trabajo en el caso que importa.
- **Descartado:** Network doble en L2–L3 (pierde Skill y no gana ascensos), proteger L1 todos los meses antes del riesgo (más despidos por explosiones) y cualquier tolerancia al riesgo escrita como regla.

## 7. Candidatos (`lab/policies-src/techo/`) y qué debe correr el chat local con DeepSeek

Los dos parten de `calidad/v4-c5` y pasan `careerlab lint` sin errores (sólo avisos de revisión, los mismos que c5 más los números de margen).

| Candidato | Cambios sobre v4-c5 | Réplica (lectura exacta / ruidosa) | Juez de calidad (Haiku / Sonnet, 3 lecturas) |
|---|---|---|---|
| `v4-t0` | Sólo la línea 5 del trimestre: **«nivel 4 o más, o Network y Output estancados» → Skill learning + Apply for rotation**, con la misma frase en la instrucción del manifest | +0,5 / +0,3; L6 16 % → 25 % (exacta); Skill final +9 | 3.ª ronda (misma tanda, 4 lecturas): 64,0 / 66,2 frente a 68,5 / 66,5 de c5; **4.ª ronda, texto final: 64,8 / 68,2 frente a 63,0 / 65,0 de c5** |
| `v4-t1` | t0 + Skill cuenta doble en el paso Crecer desde el nivel 4 + Dignity protegida desde 7 en Bienestar + «Stalled» anclado al valor y sin la mecánica `Expect` + párrafo del plan en «Los 48 meses» | +1,1 / +0,9; L6 16 % → 26 %; Skill final +10 | primera redacción: 62 / 68 frente a 66 / 70 de c5; segunda: 63 / 65 frente a 68 / 69 (los jueces leen la justificación empírica y los márgenes como mecánica inventada; corregida una frase falsa sobre las acciones que suben Skill); tercera (misma tanda, 4 lecturas): **65,0 / 67,2** frente a 68,5 / 66,5 de c5, dentro del ruido con Sonnet y −3,5 con Haiku; **cuarta redacción, texto final (frase de las acciones corregida otra vez, margen de Health unificado en 4): 65,5 / 66,5 frente a 63,0 / 65,0 de c5** (`data/j-techo-4.jsonl`). El juez se mueve ±3–5 entre tandas (c5: 63–68,5 con Haiku), así que la lectura honesta es «no baja»; lo que sí señala en los dos candidatos es lo heredado de c5 (línea de estado pesada, pistas de lectura como mecánica inventada) |

**Qué vale en una partida real de v4 que termina en L5 con Skill 105–122:** el trimestre desde L4 añade ~9 de Skill (15 % de la nota sobre 120: +1,1) y adelanta L5 unos 3 meses (sueldo 1,0 en vez de 0,7 y bonus: +0,2–0,3); en total ~+1,3 por partida completa, de 70 a ~71. **Lo que cambia de verdad en una partida** es el trimestre desde L4 (DeepSeek obedece las reglas de trimestre: B20, «Skill en L4» del 2 % al 65 % con t13-final). Lo demás vale décimas.

**Plan para el chat local (con la clave), por orden de coste:**

1. **Banco de DeepSeek, trimestre de L4** (~0,2 USD): las 40 situaciones «Skill en L4» de `ids-V2.txt` con `v4-t0` frente a `v4-c5`.
   ```bash
   uv run python scripts/deepseek/bench.py run --variant lab/policies-src/techo/v4-t0/bundle --name ds-t0 --ids <ids de la regla "Skill en L4" de ~/careerlab-data/deepseek/ids-ds1.txt>
   ```
   Confirma si elige Skill learning o Apply for rotation en ≥ 60 % (c5 y v4: ~2 %; t13-final: 65 %).
2. **Banco de DeepSeek, historias de control** (~0,5 USD): las 40 historias de control de hacia-80 (`ids-v9-all.txt`, serie de control) y las 29 de control de riesgo con `v4-t1`, comparadas con `ds-v4-full10` y `ds-v4-rep`. Confirma si la pérdida por decisión no sube más que entre dos pasadas de v4 (0,37) y no hay más elecciones con riesgo. Si t1 empeora las historias, entregar t0.
3. **Juez con DeepSeek** (~0,1 USD): `scripts/calidad-skills/ds_judge.py` con c5, t0 y t1, 5 lecturas. Entregar el que no baje de c5.
4. **Partidas completas** (0,7–0,8 USD cada una, sólo para confirmar): 3 partidas del candidato elegido. Lo que lo confirma: Skill learning o rotación en todos los trimestres desde L4 (leer `events-*.jsonl`), Skill final ≥ 120 (v4: 105–122), L5 antes del mes 42 en 2 de 3; y lo que lo refuta: un primer ascenso perdido más que con v4 (1 de 9) o una explosión nueva. **Una partida que llegue a L6 sería suerte, no la regla**: en la réplica con la lectura de DeepSeek, L6 pasa del 1 % al 2–3 %.

**Lo que no hay que probar con DeepSeek** (ya descartado en la réplica): tolerancia al riesgo escrita como regla, Network doble en L2–L3, proteger L1 todos los meses, estancamiento por «no ha subido en el trimestre», Skill en el trimestre desde L3.

**Sobre un script de línea de estado** (idea de C37): su valor en la réplica es el de conocer los techos, ≤ +0,7 sobre el texto (y 0 si DeepSeek sigue sin usar Stalled, porque la condición «nivel 4 o más» cubre el caso que importa). Con el coste de fichas de una llamada por decisión (C23: −3,6 puntos de versión) no compensa; sólo tendría sentido una llamada por trimestre, y entonces basta la condición de nivel. No se ha construido.

## Relevo (28 oct, noche)

1. **Qué se ha hecho y por qué.** La pregunta era por qué las partidas completas de DeepSeek se quedan en L5 y qué regla general las llevaría a L6. Se construyó un bot que sigue las reglas de v4-c5 tal como están escritas sobre una lectura imperfecta (`scripts/techo/techobot.py`), un diagnóstico por ventana de evaluación (`diag.py`) y un planificador que sólo ve signos con ablaciones, y se probaron ~40 variantes de regla en la réplica con semillas comunes (2.000 partidas por brazo). Después se escribieron dos candidatos desde v4-c5 y se pasaron por lint, juez de calidad y banco con Haiku.
2. **Resultados.** §2–§7 y HALLAZGOS B33–B35 más tres filas de X. En una frase: las ventanas se pierden por Network en L3 y por el ritmo de Skill en L4; la ventaja del planificador es tolerar riesgo con el contador a 0 y **no se traslada** a una regla escrita; lo que aguanta (trimestre a Skill desde L4, Dignity desde 7, Skill doble en historias desde L4) vale ~+1 y no lleva a L6 con la lectura de DeepSeek (1 % → 2–3 %). Datos en `data/` (sin texto del juego); banco con Haiku en `~/careerlab-data/techo/bank/runs/` de este contenedor (texto del juego, fuera de Git).
3. **Qué falló o quedó a medias.**
   - El modelo de lectura ruidosa (`noisy`) es demasiado pesimista en crisis (32 % frente a ~9 % con etiquetas reales de DeepSeek): el ruido real está correlacionado con las palabras. Sirve para comparar brazos, no para cifras absolutas. Las etiquetas reales de DeepSeek (`~/careerlab-data/deepseek/labels/`) sólo están en el Mac; con ellas habría que repetir `battery5` (`--labels` no está implementado en `techobot.py`; `groupbot.Perception` sirve de modelo).
   - **El juez de calidad** bajó las dos primeras redacciones (−4 a −5 con Haiku): leía la justificación empírica del plan de L4 como mecánica inventada y dos frases sobre las acciones que suben Skill eran falsas (Key project y Build a mentorship también la suben). Con el texto final (4.ª ronda, misma tanda) t0 y t1 quedan **por encima de c5** con los dos jueces (+1,5 a +3), pero el juez se mueve ±3–5 entre tandas: léase «no baja». Lección: toda frase nueva debe apoyarse en el manual publicado o declararse como plan nuestro, sin datos de nuestras partidas ni afirmaciones sobre las tablas que no sean literales.
   - No se construyó el script de línea de estado (§7): su valor en la réplica no compensa las fichas.
   - No se ha medido nada con DeepSeek: el plan está en §7.
4. **Siguiente paso.** El chat local con la clave sigue §7 por orden (banco «Skill en L4» con `v4-t0`, controles de historias con `v4-t1`, juez con DeepSeek, 3 partidas). Para repetir lo de aquí:

   ```bash
   # réplica: tandas (flags en la cabecera de techobot.py)
   uv run python scripts/techo/techobot.py --arms "base,qskill=4+dprot=7+sskill=4" --per exact --games 2000
   uv run python scripts/techo/diag.py --arms planner,base,sp+capthr+lexq+hfloor4 --per exact --games 1000
   # juez y banco (Claude, 0 USD)
   python3 scripts/calidad-skills/judge.py --out lab/reports/techo/data/j-x.jsonl --models haiku,sonnet --reps 4 lab/policies-src/calidad/v4-c5 lab/policies-src/techo/v4-t1
   TRANSMISION_DATA=~/careerlab-data/techo/bank CAREERLAB_CLAUDE_EXE=$(which claude) uv run python scripts/transmision/runbench.py run --items ~/careerlab-data/techo/bank/items.jsonl --variant lab/policies-src/techo/v4-t1/bundle --name hk-t1 --ids ~/careerlab-data/techo/bank/ids-calidad.txt --slots 4
   TRANSMISION_DATA=~/careerlab-data/techo/bank python3 scripts/calidad-skills/compare_bank.py --a hk-c5 --b hk-t1
   ```
   (`items.jsonl` sale de `gunzip -c lab/data/transmision/bank-items.jsonl.gz`; copiar también `lab/data/transmision/handbook.md` a esa carpeta.)
