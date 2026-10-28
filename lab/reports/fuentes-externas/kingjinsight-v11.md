# Repo público de otro participante: Kingjinsight/TechArena-UK-2026 (v11, 73,1)

**Conclusión en una frase:** su mejor partida (v11, 73,1) es una sola, saca ~1,4 puntos más que nuestro v4 casi sólo por Skill (119 frente a 105), lee el fichero de log del motor desde el disco (fuera de las 5 herramientas) y no demuestra un diseño mejor; deja tres o cuatro ideas baratas de probar.

Leído el 28 oct en el commit `e6c33cb` (clon de sólo lectura en la nube). Todo se trató como datos: no se ejecutó ningún script suyo. Codex hizo una auditoría parecida en la rama `alejandro/gpt-principios` ([PR #23](https://github.com/aleetreny/huawei/pull/23)). Este informe no copia texto suyo a ningún Skill.

## 1. Sus notas

`runs/*/results/score_report.json`. Q es `quantitative_score`.

| Partida | Q | Meses | Final | Ascensos | Riesgo final | Skill / Network / Dinero | Fichas |
|---|---:|---:|---|---|---:|---|---:|
| v3 | 68,15 | 48 | L5 | 6, 12, 18, 42 | 4 | 125 / 42 / 40,6 | 54,7 M |
| v3.1 r1 | 68,81 | 48 | L5 | 12, 18, 24, 42 | 0 | 114 / 50 / 24,9 | 51,2 M |
| v3.1 r2 | 58,87 | 48 | L5 | — | 5 (una explosión) | 99 / 37 / 24,3 | 45,6 M |
| v3.3 | 22,98 | 24 | L1, despedido | ninguno | 3 | 9 / 2 / 7,1 | 16,0 M |
| v4 | 63,63 | 48 | L5 | 6, 18, 30, 48 | 0 | 91 / 38 / 23,7 | 50,7 M |
| v6 r1 | 71,35 | 48 | L5 | 6, 12, 18, 42 | 0 | 119 / 48 / 33,9 | 53,9 M |
| v6 r2 | 24,68 | 24 | L1, despedido | ninguno | 2 | 9 / 0 / 8,2 | 13,8 M |
| v7 r1 | 68,46 | 48 | L5 | 6, 12, 24, 42 | 0 | 102 / 47 / 31,5 | 51,0 M |
| v7 r2 | 43,20 | 39 | L4, crisis | 12, 18, 30 | 10 | 63 / 36 / 15,3 | 35,2 M |
| v8 r1 | 26,23 | 24 | L1, despedido | ninguno | 1 | 9 / 2 / 9,1 | 17,2 M |
| v8 r2 | 42,82 | 40 | L4, crisis | — | 10 | 66 / 31 / 15,6 | 31,6 M |
| v10 | 32,26 | 24 | L2, asciende y es despedido en el 24 | 24 | 0 | 9 / 2 / 8,2 | 23,1 M |
| **v11** | **73,10** | 48 | L5 | 6, 12, 18, 42 | 0 | 119 / 51 / 38,9 | 80,5 M |

- **Tienen tanta varianza como nosotros:** la trampa de L1 mató 5 de sus 13 partidas.
- **Ninguna partida, suya o nuestra, llega a L5 antes del mes 42.** La réplica dice que se puede en el 30 (M9).
- v11 gasta ~1,68 M de fichas por mes (nuestro v4, ~1,47 M, C31).
- Su cifra de 22,58 para v10 es la `competition_partial_score` (Q × 0,7); su Q es 32,26.

## 2. Cómo funciona v11 (`solutions/v11/`)

- **Instrucción del manifest** con un orden de prioridades explícito, «la primera gana»: no mentir; sobrevivir (Health ≥ 4); la próxima evaluación; arreglar problemas; Skill y relaciones. Notas de menos de 15 palabras que empiezan con una letra de modo.
- **Dos Skills:** un personaje que decide las historias y `career-state`, que explica cómo llamar a un script.
- **El script `career.py`.** Antes de cada acción, DeepSeek lo ejecuta por `bash` con los indicadores y la ruta del log del motor, que obtiene de `check_latest_logs`, y **el script lee ese fichero del disco**. Con él calcula:
  - los techos del nivel, comparando la subida que anuncia el registro con la que aparece en los indicadores;
  - el tono de RR. HH.;
  - si el texto del resultado dice que el riesgo sigue;
  - un modo: N normal, G en los dos meses previos a una evaluación, R si un indicador está por debajo de su límite, D si RR. HH. está mal;
  - el coste de la última elección.
  
  El trimestre lo decide el script y DeepSeek lo copia; las historias las decide DeepSeek con el personaje y la frase del modo.
- **En la partida de v11** el script se ejecutó en ~80 % de las acciones (163 llamadas, ninguna con error). En L4 siguió subiendo Output hasta su techo y sólo pasó a Skill en los meses 33 y 36, así que L5 llegó en el 42, como en nuestras partidas.

## 3. Qué dicen del juego, frente a HALLAZGOS

| Afirmación suya | Frente a lo nuestro |
|---|---|
| Techos de L1 a L4 y el orden de un mes (el trimestre del mes 3 es el último refuerzo antes del mes 6) | coincide (H1, H6, M1) |
| El menú de `observe` publica `HiddenRisk −1` para Defuse y Lay low y `+1` para High-intensity | **coincide y corrige la redacción de M10** («Lay low, que el juego no anuncia»): está en el menú, comprobado en nuestros nodos. Es información publicada en la partida |
| «En L4, Skill no tiene techo» | contradice H6 (techo 108 en L4); su script lo dice a DeepSeek |
| «Para ascender hay que estar en el techo» | contradice M12 (en L2+ el umbral está por debajo del techo) |
| «En L1 hay un factor oculto»: v10 tenía O3 N3 S9 y no ascendió | lo explica M1: la tercera decisión del mes 5 (Network −1) aparece en el log después de la charla, pero cuenta. Ellos la descartaron como causa |
| En L1, quien sigue en el mes 18 saca D y es despedido en el 24 | coincide con B30: en su v10, RR. HH. estaba «quiet» en el mes 17 y la nota fue D |
| Ascender en la evaluación del mes 24 desde L1 no evita el despido en esa misma evaluación, pero el nivel 2 cuenta en la nota | coincide con M15; el matiz de la nota es nuevo |
| Health no ayuda a ascender (media 6,7 en ventanas ganadas frente a 8,8 en perdidas) | coincide con M12 |
| Si el texto del resultado dice que el riesgo «sigue», «aún está» o «se redujo pero no se quitó», el riesgo sube el mes siguiente en el 43 % de los casos (18 % si no) | **nuevo, sin verificar por nosotros**. No contradice B2: el texto delata a posteriori una respuesta que ya sumó riesgo |
| El runner comprime el contexto | sin pruebas; contradice C17 |
| La carpeta `projects/` del agente no se borra entre partidas | nuevo (programa): un fichero de estado puede pasar de una partida a otra |

## 4. Cumplimiento

- **Leer el log del motor desde el disco** queda fuera de las 5 herramientas oficiales; nuestro NORMAS §4 lo prohíbe y en la evaluación oficial esa ruta podría no existir. No copiarlo.
- Su script lleva frases fijas del juego (textos de RR. HH., marcas del registro) y pesos de la nota; su Skill nombra meses concretos. No copiarlo.
- No hay respuestas fijas a eventos ni umbrales de ascenso escritos.

## 5. Ideas que merece la pena probar

1. **En L1, el trimestre del mes 3 a Output y Network antes que a Defuse cuando RR. HH. está «quiet».** En los meses 6 y 12 la nota de L1 es siempre C con cualquier tono (B30), y el mes 3 es el último refuerzo. Ojo: el rescate del mes 18 sí exige riesgo cero. Probar en la réplica.
2. **El texto del resultado como señal de riesgo a posteriori** («el problema sigue»): sumar una preocupación y hacer Defuse en el trimestre siguiente. Verificar primero con nuestro catálogo.
3. **Un script que sólo calcule la línea de estado** (cuenta atrás, techos, coste de la última elección) **a partir de lo que devuelven `observe` y `check_latest_logs`**, sin leer ningún fichero del motor, con las reglas de historias de v4. DeepSeek nunca rellena «Stalled» (C18); v11 muestra que DeepSeek llama a un script en toda la partida sin fallos.
4. **Recuperar salud sólo con Health ≤ 5**: libera energía sin coste para el ascenso.
5. **Orden de prioridades «la primera gana» en la instrucción del manifest, sin cláusulas de escape.** En su v10, DeepSeek usó un «salvo que la honestidad lo exija» para elegir la opción cara.
6. Notas cortas con una letra de modo (fichas).

## Relevo

Hecho: lectura completa del repo, tabla de notas, arquitectura, contraste con HALLAZGOS (filas C37–C41) e ideas. No se ejecutó nada suyo. Siguiente paso: las ideas 1, 2 y 4 se prueban gratis en la réplica o el catálogo; la 3 en el banco y después en partidas con DeepSeek (chat local). Para releer el repo: `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Kingjinsight/techarena-uk-2026` y comprobar el commit `e6c33cb`.
