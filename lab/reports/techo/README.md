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

## 4. Qué parte de la ventaja del planificador es regla (en curso) — `data/diag-signplanner-exact.txt`

(se rellena)

## Relevo

(se rellena al final)
