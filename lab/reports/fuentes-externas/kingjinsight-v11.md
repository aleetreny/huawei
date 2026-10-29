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

## Otros repos públicos (búsqueda del 28 oct por la tarde)

| Repo | Qué hay | Nota publicada |
|---|---|---|
| `krsnkkv/KSL_TechArena` (= `krsnkkv/techarena-career-simu`, `ShriyaSaxena/techarena-career-simu`, `LRado-253/ksl-techarena`: el mismo equipo, KSL) | 3 Skills cortos (~1.200 palabras en total): estado, historias y trimestre | una partida de 57,38: 48 meses, L4, Skill 75, riesgo 2, 62,9 M de fichas (1,31 M por mes), 0,68 USD |
| `Artepace/slopathone_winningteam` | diseño preliminar y un `solution.zip` con 4 Skills y documentos de diseño | su primera versión, una partida local: 68,6, L5, ~54 M de fichas (1,1 M por mes); la versión actual, sin partidas |
| `peidi-L/preliminary` | un borrador | — |
| `Ray23257/techarena-career-sim`, `YuLong111/techarena-career-sim`, `bernardoguterres/huawei-gradient-depression` | ya no son públicos (piden credenciales) | — |

**Ninguno muestra una media estable por encima de 70 ni llega a L6.** Lo aprovechable de Artepace es la forma de su `decision_report.md`: apoya cada regla en un principio conocido (evitar la ruina, actualizar con lo observado, constancia entre las 3 partidas) y dice qué se ha validado y qué no. Sirve de modelo para nuestros documentos del jurado. Los repos se clonaron en sólo lectura fuera del repo; no se ejecutó nada suyo.

## Vigilancia periódica (desde el 28 oct)

- `scripts/fuentes-externas/vigilar.py` revisa cada repo de `fuentes.json` con `git ls-remote`. Si cambia, lo clona en `~/ext/` y saca las notas de sus `score_report.json`. El último estado visto queda en `estado.json`. No ejecuta nada de esos repos.
- Una revisión programada lo corre una vez al día (19:43, hora UK), busca repos nuevos y, si hay algo de valor, lo pasa a HALLAZGOS. Hay otra el 31 oct, tras el corte 2.
- **Clasificación oficial:** desde el 28 oct a las 19:30 UTC el dominio está permitido. `vigilar.py` la lee como JSON (cabecera `Accept: application/json`) y guarda sólo equipo, puesto y notas. El JSON de Hydro trae también correos, IP y códigos de invitación de cada equipo, y eso no se guarda. Los nombres de equipo que son un correo se guardan como «(correo)».
- El 28 oct había 227 equipos y ninguno tenía aún nota del corte 1.
- **Hay dos equipos llamados «Gradient Depression».** El nuestro es el creado el 21 oct; el otro se creó el 24 oct. Cada uno tiene tres miembros. `vigilar.py` distingue el nuestro por la fecha de creación.

## Barrido amplio (28 oct, 18:30 UTC)

En resumen, lo único con valor sigue siendo Kingjinsight (secciones 1–5, C37–C42). Lo demás está vacío o no tiene que ver con el reto.

- **Nuevas:** `rickyyyy-bit/TechArena-Huawei` («Jon8652's team») sólo tiene dos Skills preliminares genéricos, sin partidas, porque no tenían clave. `Colinfornia/Techarena-Project` sólo tiene un README vacío. Las dos se vigilan. `Sherlock-shy` y `QuantumBitstream` son forks del repo oficial sin cambios.
- **Sin cambios:** KSL (las cuatro copias), Artepace y peidi-L. Ray23257, YuLong111 y bernardoguterres siguen privadas. No hay versiones nuevas de los paquetes del motor en PyPI desde el 25 oct.
- **Kingjinsight coincide con nuestra réplica:**
  - Sus topes medidos en L1 (O3 N3 S9) cuadran con lo nuestro.
  - Su «Skill ≥ ~90 y nota A para pasar de L4 a L5» coincide con `THRESH[4]` (Skill 90).
  - Su escalera de frases de RR. HH. y su fórmula de nota leída del log no aportan nada que la réplica no tenga.
- **Sin resultado:**
  - GitHub: búsquedas por techarena, tech-arena, techarena-uk, jiuwenswarm, career survival y career sim, nombres de repo adivinados, y los forks y perfiles de los equipos conocidos.
  - Web, en inglés y en chino: LinkedIn, YouTube, Medium y Bilibili.
  - Sin relación con el reto: otros retos de TechArena (CTR y otros) y la edición 2025.
- **No accesibles desde la nube:** huggingface.co, gitee.com, gitlab.com, reddit.com, techarena-uk.hydro.ac y la documentación en readthedocs. La API de GitHub tampoco; se usan `git ls-remote` y clones.

## Primera revisión diaria (28 oct, 19:45 UTC)

No hay nada nuevo: los repos no han cambiado y la clasificación sigue sin notas.
- **Hugging Face** (modelos, datasets y spaces; búsquedas techarena, career-survival, jiuwen y career_emu): nada del reto.
- **Gitee** (API de búsqueda): nada. Algunas consultas cortan la conexión.
- **Reddit:** la API JSON no se puede usar desde la sesión, porque el clasificador de permisos la bloquea como bot, y el buscador web no indexa reddit.com. Queda sin cubrir.

## Revisión del 29 oct (madrugada)

Hay tres repos con commits nuevos y ninguno aporta nada:
- **Artepace** ha subido su v3 en un ZIP: cuatro Skills, documentos y nada de notas.
- **rickyyyy-bit** (Jon8652's team) tiene su v3: una partida local de 64,52 en L5, con 48,6 M de fichas. Les falta el vídeo para que la entrega sea válida.
- **peidi-L** ha refinado el preliminar.

La clasificación sigue sin notas.

**Fuente de datos sin explotar: las 13 partidas de Kingjinsight.** Son partidas reales de DeepSeek. Cada una trae `events-*.jsonl` con todas las llamadas (unas 790 `tool_call`/`tool_result` en una partida de 48 meses), las fichas de entrada y salida, y el registro de `check_latest_logs` con lo que cambió cada elección. Ejemplos de fichas:
- su v3.1: 45,6 M en total, de las que sólo 98 mil son de salida, 0,95 M por mes;
- nuestra v4: 1,35–1,47 M por mes.

Esos datos pueden servir para calibrar la lectura simulada de DeepSeek de las líneas Suelo y Techo y para medir de qué está hecho el historial. Son texto del juego: no van a Git.

## Notas oficiales del corte 1 (29 oct)

En resumen: quedamos 13.º con 64,75. Sólo 34 de los 227 equipos tienen nota mayor que 0, y el top 10 empieza en 68,17. Lo que nos separa de los primeros es sobre todo el juego (HALLAZGOS C45).

| Puesto | Equipo | Nota |
|---:|---|---:|
| 1 | ShenzhenFan01's team | 75,99 |
| 2 | gengyuan's team | 74,59 |
| 3 | ruifeng's team | 72,51 |
| 4 | aman_abdulsalam's team | 71,99 |
| 5 | ShanshanMao's team | 71,77 |
| 6 | PHP Security | 71,72 |
| 7 | MattKep7777's team | 70,88 |
| 8 | Yuanyuan's team | 70,59 |
| 9 | Sky's team | 69,87 |
| 10 | manocw's team | 68,17 |
| 11 | Chinese can fly | 67,40 |
| 12 | IQ2 Only | 65,86 |
| **13** | **Gradient Depression** (el nuestro, creado el 21 oct) | **64,75** |
| 17 | Saul Goodman (Kingjinsight) | 56,69 |
| 18 | KSL | 56,00 |
| 26 | Gradient Depression (el otro, homónimo) | 46,78 |

Lectura:
- **Nuestra nota.** Con calidad ~65 y fichas ~63 (v4), 64,75 implica una media de partidas de ~65. Es justo lo que esperábamos de v4 contando un hundimiento cada ~9 partidas, así que el juego de evaluación no parece muy distinto del de desarrollo.
- **Lo que hace falta para llegar arriba.** Para 75,99 hace falta una media de partidas de ~73–74 aunque las fichas y la calidad fueran casi perfectas. El líder juega mejor; no sólo gasta menos.
- **Con `cp-v10`.** Con fichas ~97 y las mismas partidas, quedaríamos en ~68: en el borde del top 10, que subirá tras el corte 2.
- **Kingjinsight.** Su v3.1 sacó 56,69 oficial, ~10 puntos de media de partidas por debajo de sus partidas locales: una partida oficial mala pesa mucho.

La búsqueda de los repos de los diez primeros está en marcha.

## BDCI: el mismo reto, antes, en China (29 oct)

En resumen: ninguno de los 12 equipos que nos superan en TechArena UK tiene repos públicos. Lo nuevo viene de **CCF BDCI 2026** (jul–oct de 2026), la misma competición de Huawei openJiuwen («Agent 职场长程生存与晋升挑战»). Usa el mismo motor `career-emulator`, DeepSeek V4 Flash y JiuwenSwarm, terminó el 5 oct, y varios equipos han publicado después sus análisis. Hallazgos C46–C48.

Fuentes (clonadas en `~/ext/`, sin ejecutar nada suyo):

| Repo | Equipo | Qué tiene |
|---|---|---|
| Xianmuyingyue/careersim-bdci26-postmortem | 悟空, 12.º el 5 oct | 3 Skills, documentos de diseño, 109 partidas locales; deduplicación por hash; mejor partida 76,28 (L6 en el mes 42) |
| YUMinRan/CareerSim-BDCI26 y smileDSG/CareerSim-BDCI26 | 熊起707 (oficial 56) | Truncado del Skill a ~60 k caracteres, motivos para un 0, libro de partidas con fichas (0,7–0,85 M al mes) |
| Winfred666/CareerSim-BDCI26 | winfred | Expertos por indicador con anclas −3…+3; el script decide sólo si su elección es estable con ruido de percepción |
| ShaFuFuDeLiu/Competitions-CareerSim-BDCI26 | — | Tablas de eventos descodificadas: es justo lo que daba un 0. Sólo como aviso |

**Cumplimiento.** Dos de estas guías sacan sus cifras de descodificar el dataset y el simulador de BDCI. No se lee el simulador de BDCI (`openJiuwen-ai/CareerSim-BDCI26`, NORMAS §4) y ninguna cifra suya pasa a un Skill. Además, los parámetros difieren de los nuestros: allí el bonus C/D es negativo.

**Lo buscado sin resultado:**
- Alias de los 12 primeros en GitHub: ShenzhenFan01, MattKep7777 y aman_abdulsalam no existen; los demás existen pero no tienen repos del reto, o son nombres demasiado genéricos.
- Búsqueda de código en GitHub (`show_employee_handbook`, `check_latest_logs`, «Defuse legacy risk», `career_emulator`).
- LinkedIn, Zhihu, CSDN, Bilibili y Hugging Face.

### BDCI: material oficial y premiados (29 oct)

- **Dónde se jugó.** El reto estaba en xir.cn (competition/1165), no en DataFountain.
- **Premiados.** 乃龙 63,31 · 我们两个真厉害 62,43 · 这次肯定队 62,2 · xx 61,29 · finewords 61,1, sobre 70 (63,31 ≈ 90 en nuestra escala).
  - Ninguno ha publicado su método. Tenían que subirlo a gitcode.com/openJiuwen/agent-store, y para este reto sigue vacío.
  - Tres equipos con mejor nota que el 4.º y el 5.º no entraron entre los finalistas. Probablemente, la revisión manual.
- **Formato.** Cada entrega se jugaba 3 veces, y la nota bailaba mucho: el primero sacó 63,31, 57,71 y 42,74 en días distintos. Un paquete idéntico conservaba la nota.
- **Los ceros.** 43 con motivo en las 7 actas diarias:
  - respuestas fijas en el Skill o el manifest, ~10;
  - modo de agente erróneo, 9;
  - paquete incompleto, 8;
  - consecuencias ocultas en tablas, 5;
  - leer estado oculto, 4;
  - descodificar el motor, 2.
- **Lo que dijeron los organizadores en su vídeo de dudas (28 jul):**
  - el simulador de la evaluación es el mismo que el de desarrollo; sólo cambia el juego de datos;
  - el nombre de cada opción coincide con su efecto, así que el agente puede deducir el efecto del texto;
  - el riesgo se acumula hasta un umbral, por lo que hay que planificar a largo plazo;
  - las fichas y el tiempo cuentan;
  - no hay que optimizar a lo bruto una sola dimensión.
- **Copias locales:** actas, transcripción del vídeo y documentación oficial en chino, en `/root/ext/bdci-web/`, en el contenedor de la nube y fuera de Git.
