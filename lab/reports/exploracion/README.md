# Línea Exploración: subir la nota global más allá de lo conocido

**Conclusión (29 oct, noche).** Con la réplica calibrada por primera vez con las decisiones reales de DeepSeek, **las reglas escritas y los scripts mueven la media de partidas ±1–2, no los 13 puntos que separan a DeepSeek del planificador con información perfecta**: casi todo ese hueco es percepción, y lo que más pesa es el mes previo a cada evaluación de L1. El mejor candidato, **`exploracion/ex-v1`** (cp-v12 con mejores trimestres, freno de salud y texto para la rúbrica), sube la versión esperada de ~62,2 a ~64,5 en la réplica (+1,8 de partidas, +8 de calidad con los jueces de Claude) y la probabilidad de pasar el corte del top 10 (68,17) de 32 % a 43 %. **`ex-v3`** añade una regla acotada al mes previo de L1 (lo discreto antes que plantarse en público) con +0,3 en la réplica y señal clara con Sonnet; sólo entra si gana en el banco de DeepSeek. Pasar de 75,99 exigiría una media de partidas de ~72,5, el nivel del planificador perfecto: **no hay ninguna medida que lo acerque**; la probabilidad con ex-v3 es ~1 % por corte.

Rama `claude/gradient-depression-skills-k3b6u0`, juntada con `main` al terminar. Carpetas: este informe, `scripts/exploracion/`, `lab/policies-src/exploracion/` (candidatos y su [README](../../policies-src/exploracion/README.md) con la nota esperada desglosada), `lab/data/exploracion/` (pesos del modelo, bancos con Sonnet). **Plan para el chat con DeepSeek: [plan-deepseek.md](plan-deepseek.md)** (~2–3 USD). Sin DeepSeek en esta línea: réplica, datos ya pagados y Claude.

## 1. La réplica calibrada con las partidas reales

**En una frase:** un modelo de elección ajustado a las 2.743 decisiones de historia reales de la familia v4/cp predice el 87 % de las elecciones de DeepSeek en partidas que no vio, y metido en la réplica reproduce las partidas reales: completas 65,4 (reales 65,3), ~17–20 % de hundimientos (reales 5 de 20), L5 hacia el mes 42–43 (reales ~44), primer ascenso en el mes 6 el 54 % (reales 52 %). Es el paso 1 de [pendientes.md](../deepseek/pendientes.md).

- **Datos.** `scripts/exploracion/calib_data.py` empareja cada decisión de `lab/data/deepseek/decisiones.csv.gz` con su nodo del catálogo de la réplica (2.289 por la tabla, 1.480 más por título, número de opciones y texto de la opción elegida: 3.769 de 3.769). Guarda, por decisión, las opciones con su efecto y riesgo verdaderos y las cuatro pasadas de lectura de DeepSeek (`etiquetas/ds-v1-*-full`, `ds-v3-*-full`). Lleva texto del juego: va a `~/careerlab-data/exploracion/calib.jsonl.gz`, fuera de Git (se rehace con CPU, NORMAS §1.6).
- **Modelo** (`choice_model.py`): logit condicional. Rasgos de cada opción:
  - ganancia útil y desperdiciada (por encima del techo) de Skill/Network/Output y sus pérdidas;
  - Health, Dignity y Wealth;
  - riesgo verdadero (lineal, «hay riesgo», «riesgo 2 o más»);
  - la lectura media de DeepSeek de cada indicador y del riesgo;
  - el contexto: mes previo, RR. HH. no amable, Health baja.
- **Validación** por partidas (6 de 23 fuera): acierto 87 %, log-verosimilitud −0,26 por decisión; sólo efectos verdaderos 84 %, sólo lecturas 87 %, azar 40 %. DeepSeek se repite a sí mismo el 90–94 % (B21, C54): 87 % es casi el techo. El modelo es algo más aleatorio que DeepSeek (autoacuerdo 86 %); con temperatura 0,7 coincide con él y todo sube ~1, sin cambiar el orden de los brazos.
- **Lo que dicen los pesos.** DeepSeek evita con fuerza lo que lee como pérdida de Skill (−4,6), Network (−2,2) y Output (−2,0); valora lo que lee como Health (+1,1), Dignity (+0,8) y «baja el riesgo» (+1,0); el riesgo verdadero pesa −0,6 por punto, −0,45 más si hay alguno y −1,0 más si es de 2 o más (en partida lo ve mejor que en las pasadas de lectura). No distingue una subida útil de una que cae sobre el techo.
- **Réplica** (`dssim.py`): historias con ese modelo (muestreado, con las lecturas reales), trimestres con las reglas escritas de cada manual (bots de `techo/`, `comprobante/` y `exploracion/`), y el parche B30 (la tercera evaluación de L1 sólo con el riesgo a 0), que la réplica de `main` no tenía: sin él, el 25 % se quedaba en L1; con él, el 12 %.

| Réplica (2.000 partidas) | Media | Completas | Media completas | Despido L1 | Salud | Crisis | L5 en el mes | L6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Réplica antigua, lectura «ruidosa» (techobot) | 41,1 | 41 % | — | 18 % | 7 % | 32 % | — | 1 % |
| **Calibrada, reglas de cp-v12** | **58,5** | 81 % | **65,4** | 10 % | 6 % | 3 % | 42,6 | 13 % |
| Partidas reales de la familia (20 con final) | ~56,6 | 75 % | 65,3 | 15 % | 5 % | 5 % | ~44 | 0 de 14 |

Error típico de cada media: ~0,35 con 2.000 partidas; las comparaciones usan las mismas semillas.

**¿Cuestan juego las reglas cp frente a v4?** Modelos ajustados por separado (`fit_subsets.py`; cada uno predice peor las decisiones del otro, 0,27 frente a 0,23 de log-verosimilitud, así que el manual sí cambia el comportamiento), con el mismo trimestre: v4 58,7, cp 58,0 (+0,7 ± 0,4). v4 evita más las pérdidas en el mes previo; cp persigue más Skill y tiene menos crisis. **Los 5 puntos de diferencia entre las completas reales (4 de v4 frente a 13 de cp) son sobre todo azar** (error típico de esa diferencia, ~2,7). Por eso los candidatos parten de cp-v12, que tiene el bucle validado.

## 2. Dónde están los puntos

**El planificador con información perfecta saca 74,4 en la réplica calibrada; DeepSeek con las reglas de cp-v12 + informes en L1, 59,4.** Cambiando quién decide sólo en una parte de la partida (`scriptbot.py`, `SwapBot`):

| El planificador decide sólo… | Media | Ganancia |
|---|---:|---:|
| (nadie) | 59,4 | — |
| las historias de L1 | 65,4 | **+6,0** |
| … sólo en los dos meses previos a cada evaluación de L1 | 64,2 | +4,8 |
| las historias de L2 / L3 / L4 / L5–L6 | 61,0 / 61,0 / 61,5 / 60,1 | +1,6 / +1,6 / +2,2 / +0,8 |
| los trimestres | 60,9 | +1,5 |
| todas las historias de los dos meses previos a cada evaluación | 67,6 | +8,2 |
| todas las historias | 73,1 | +13,7 |

En las partidas completas la diferencia (65,4 frente a 74,7) se reparte en nivel 2,6, dinero 2,3, Skill 1,7, Network 1,5 y riesgo ~1.

**Por qué pierde las evaluaciones** (`diag_reviews.py`):
- L1, el 51 %: Output en el 60 % de los casos, Network en el 40 %, por 1–2 puntos;
- L2, el 26 % (Output, Network);
- L3, el 40 %: Network y Output por 2–3 puntos;
- L4, el 72 %: Skill, mediana 22 puntos; Output, 3;
- L5, el 80 %: Skill 9, Output 4.

**El mes previo de L1, en las partidas reales** (120 decisiones):
- el 22 % elige una opción que pierde Network u Output; en 16 de esos 26 casos la única alternativa sin pérdida tenía riesgo, y en 10 había una segura que no vio;
- donde se aparta del planificador, casi siempre elige un **gesto de integridad en público**: negarse a hacer campaña, poner una B «justa», corregir en la sala, reconocimiento formal, el proceso largo. Todos dan Dignity +2 y quitan Network u Output (C58).
- Con Sonnet en el banco de L1 se ve por qué: rechaza «aclarar por escrito después de la reunión» (riesgo −1 en el catálogo) o «pedirlo en privado» (riesgo 0) por la lista de señales de riesgo («en privado», «después»).
- En el catálogo, las opciones redactadas en privado / después / por escrito llevan riesgo ≥ 2 sólo el 11 % de las veces y pierden Network u Output el 25 %. Plantarse en público, negarse o insistir las pierde el 46–64 %, y no son menos arriesgadas (riesgo > 0 el 43–54 %).

## 3. Lo que vale cada idea en la réplica calibrada

Base: reglas de cp-v12 + informes en el trimestre de L1, 59,4 (salvo que se diga otra cosa). Las cotas «oráculo» saben lo que DeepSeek no puede saber.

| Idea | Media | Δ | Lectura |
|---|---:|---:|---|
| **Trimestre por tramos** (búsqueda `qsearch.py`, 40 combinaciones): L1 informes; L2–3 informe, red, informe + proyecto clave; **L4+ Skill learning + informe** + rotación | 59,8 | +0,7 | L4 con informe en vez de red: +0,5; el resto, plano. El proyecto clave por defecto (idea china) gana en L1–L3; desde L4, la rotación |
| Recuperar Health en el trimestre con Health ≤ 5 / ≤ 6 | 59,9 / 60,0 | +0,5 / +0,6 | muertes por salud a la mitad |
| DeepSeek cuida el doble/triple la salud con Health ≤ 5 + lo anterior | 60,3 | +0,9 | muertes por salud 6,5 % → 1,1 % |
| Pérdidas de N/O en el mes previo de L1 el doble de graves | 60,0 | +0,6 | |
| Penalizar plantarse en público en el mes previo de L1 (`ex-v3`) | +0,3 | | igual en los meses previos de todos los niveles; en todos los meses −0,5 (más crisis) |
| Skill el doble desde L4 | 59,7 | +0,3 | |
| Más aversión al riesgo en todo (×1,5) / menos (×0,7) | 59,8 / 57,7 | +0,4 / −1,7 | no hay que tolerar más riesgo |
| Dignity sin valor cuando está en 9–10 (todos los meses / sólo en el mes previo de L1) | 56,7 / 59,9 | −2,7 / +0,5 | las opciones «íntegras» son también las que le alejan del riesgo |
| Defuse sólo con RR. HH. frowning o peor | 59,2 | −0,2 | se queda como está |
| Saber los techos en las historias / en el trimestre (cotas) | 59,3 / 59,8 | 0 / +0,4–0,6 | |
| **Detectar los techos en partida con el menú del trimestre** (lo que puede un script, `CapBot`) | 59,3 | **+0,0** | se detectan cuando ya se ha gastado en ellos |
| Veto oráculo a lo que pierde N/O en el mes previo de L1 (riesgo ≤ 1 permitido) | 62,7 | **+3,3** | la cota de la trampa de L1 |
| … el mismo veto con una pasada real de lecturas de DeepSeek | 59,5–60,0 | +0,1–0,6 | **las pérdidas que importan son justo las que no ve** |
| Revisar la opción elegida en el mes previo de L1, detectando el 50 % / 100 % de las pérdidas | 60,3 / 60,7 | +0,9 / +1,3 | con un 20 % de falsas alarmas, −3,7 |
| DeepSeek más constante (temperatura del modelo ×0,5) | 61,0 | +2,0 | no hay palanca conocida para conseguirlo |
| **Script que decide las historias con las lecturas de DeepSeek** (planificador de signos, con riesgo y umbrales exactos) | 54,9–56,2 | **−3 a −4,5** | crisis 15 %: confirma C23 |
| **Híbrido de Winfred** (el script decide sólo si su elección aguanta ≥ 70 % / ≥ 90 % de 20 perturbaciones de la lectura) | 57,1 / 59,4 | −3,0 / −0,7 | tampoco gana a DeepSeek |

## 4. Las zonas grises aprobadas (C49, C60), una por una

- **Varias llamadas por respuesta y escribir poco.** La nota de fichas ya está en 100 con el bucle de cp-v12 (370 y 492 mil fichas por mes en sus dos partidas completas, 455 mil en la de cp-v10 narrando). No queda nota que ganar por ese lado; sólo margen. El SKILL.md entero cuesta ~15 mil fichas por mes (está en el historial desde la primera llamada). Lo que hay que proteger es la pareja de llamadas: cualquier cambio en el bloque literal se prueba con sondas antes de jugar (plan, paso 1).
- **Scripts con estado (C49, C60).** Hecho y medido (`ex-s1`, `script/brief.py`):
  - el agente le pasa diez cifras en una tercera llamada de cada respuesta; el script guarda el registro en un archivo con el nombre del `session_id` (una partida nueva no abre el de otra) y devuelve una línea con:
    - Best del nivel;
    - los indicadores «llenos» (comprados en el trimestre sin que subieran; con el estado exacto antes y después del trimestre, los cambios de mes no lo ensucian porque las evaluaciones nunca caen justo después de un trimestre);
    - avisos de salud, arranque atascado y explosiones;
    - el plan del trimestre en números del menú (que en nuestras partidas sigue siempre el orden del handbook: 343 de 343).
  - Probado con las 23 partidas reales: 1.470 marcas de «lleno», ninguna falsa.
  - **Vale +0,0 en la réplica**, por tres razones:
    - (a) decidir historias con un script pierde (§3);
    - (b) las notas de DeepSeek ya llevan bien el estado: «Now» coincide con el estado real en 3.200 de 3.211 notas y «Review in N» en el 96 %;
    - (c) los techos se detectan cuando ya no sirven.
  - Respuesta para la pregunta 3 del vídeo: probamos un script con estado, lo validamos con trazas reales y medimos que no mejora a un texto bien escrito; por eso el manual entregado no lo lleva.
- **Observaciones propias («in our runs»).** Los candidatos dicen como observación nuestra:
  - el calendario de la evaluación, con su comprobación en partida («si el mes 6 empieza sin la charla, sigue protegiendo»);
  - que Output es lo que se queda atrás en el nivel inicial;
  - que Skill y luego Output frenan desde L4;
  - el orden de los menús;
  - que plantarse en público cuesta Network u Output la mitad de las veces (`ex-v3`).
  - Los márgenes de Health y Dignity se presentan como márgenes nuestros sobre el rango publicado 0–10.

## 5. Lo que dicen los organizadores y los equipos chinos (C48, C50), contrastado

| Idea | Lo que dice la réplica calibrada | Dónde está |
|---|---|---|
| El nombre de cada opción coincide con su efecto | La lectura de DeepSeek ya acierta riesgo y Network ~80 %; Output ~50 % (ambos sentidos), y ese es el hueco (§2). Las señales de lectura que sobrecargan «en privado / después» empujan en el mes previo a opciones que cuestan Network/Output | `ex-v3` |
| El riesgo se acumula y estalla tarde | Tolerar más riesgo baja la media (−1,7); el cierre de cp-v8–v11 ya estaba descartado | se queda como cp-v12 |
| El ascenso mira Skill, Network y Output a largo plazo | Las evaluaciones de L2–L3 se pierden por 1–3 puntos de N/O; el trimestre de v4 (informe, red, informe) es el mejor de 15 combinaciones | `ex-v1` |
| La energía que no se gasta se pierde | Todo el texto pide gastarla entera; el script la reparte en números | `ex-v1`, `ex-s1` |
| Freno de salud por carga de trabajo | +0,9 con recuperación desde Health 5 y freno en historias con Health ≤ 3 | `ex-v1` |
| Proyecto clave como acción principal por defecto | Gana en L1–L3; desde L4, rotación (+Skill) | `ex-v1` |
| Detectar techos con el menú | Funciona (sin falsos), pero vale +0,0 | `ex-s1` |
| Skills cortos | El juez castiga la longitud (Sonnet, claridad 4–5); `ex-v1` mide lo mismo que cp-v12 y saca +8 | `ex-v1` |

## 6. Calidad de los SKILL.md

Jueces de Claude con la rúbrica oficial (`scripts/calidad-skills/judge.py`, Sonnet y Opus × 2; datos en `data/j00.jsonl`–`j04.jsonl`):

| Manual | Opus | Sonnet | Media |
|---|---|---|---:|
| `deepseek/t13-read-v4` (corte 1) | 73 · 72 | 66 · 66 | 69 |
| `comprobante/cp-v12` | 73 · 72 | 66 · 66 | 69 |
| **`exploracion/ex-v1`** (texto final) | **84 · 83** | **72 · 71** | **77,5** |
| `exploracion/ex-v3` | 82 · 84 | 66 · 66 | 74,5 |
| `exploracion/ex-s1` | 80 · 80 | 70 · 66 | 74 |

Lo que subió la nota sin tocar decisiones:
- un plan de 48 meses por fases en tabla;
- una tabla «cerca de un límite»;
- el calendario de la evaluación como observación nuestra con comprobación en partida;
- el paso 2 en viñetas (modo estricto, tamaño del riesgo, excepción, arranque atascado);
- márgenes coherentes (Health 5 y 3, Dignity 4) declarados como nuestros;
- qué hacer con los números del menú (el orden del handbook, y qué hacer si `observe` enseña otra cosa).

Lo que sigue restando:
- Sonnet castiga el bloque del bucle y la longitud (claridad 4–5);
- los dos jueces señalan que el calendario es observación nuestra y no regla publicada.

Quitar el bloque literal rompe la pareja (C53, C59): se acepta ese coste.

## 7. Preguntas para Discord

No hay ninguna imprescindible: todo lo que usan los candidatos está dentro de C49 y C60. Una, opcional, por si una línea futura quiere atacar la percepción con código:
- *«May a Skill script score the wording of the options shown in the current run with general cues that we derived from statistics over our own development runs (for example, "refusing or correcting someone in public tends to lower Network"), the same cues that the Skill already states in prose as our observations? The script would contain no event titles, no per-event answers and no tables of outcomes.»* Valor: sólo si una puntuación así lee Output mejor que DeepSeek (hoy ~50 %); sin probar.

## 8. Qué haría falta para pasar de 75,99

Una media de partidas de ~72,5 con calidad 80 y fichas 100: es lo que saca el planificador que **ve los efectos exactos** (74,4 en la réplica, 72,4 en el juego real). Lo que falta es percepción, sobre todo de Output (~50 %) en los meses previos a una evaluación:
- en la réplica, ver las pérdidas de N/O en el mes previo de L1 vale +3,3;
- hacerlo bien en todos los meses previos, +8,2.

Ninguna regla escrita ni script probado aquí consigue esa percepción con las lecturas de DeepSeek. Lo que sí se puede probar barato con DeepSeek es si las reglas acotadas (`ex-v3`) cambian sus elecciones en el banco de L1. La varianza ayuda poco: con ex-v3, P(versión > 76) ≈ 1,3 % por corte.

## Relevo (29 oct, noche; cierre de la línea)

1. **Hecho y por qué.**
   - Réplica calibrada con las decisiones reales (§1), que faltaba para poder decidir reglas.
   - Descomposición de la distancia al planificador (§2).
   - Batería de ideas (§3): reglas, scripts, el híbrido de Winfred, techos, temperatura.
   - Búsqueda del trimestre por tramos.
   - Script con estado de C60 validado con trazas reales (§4).
   - Banco de L1 con Sonnet para tres textos.
   - Cuatro candidatos con su nota esperada ([README de candidatos](../../policies-src/exploracion/README.md)).
   - Juez de calidad (§6).
   - Plan para DeepSeek ([plan-deepseek.md](plan-deepseek.md)).
2. **Resultados y datos.**
   - `data/final_eval.json`: evaluación final, 4.000 partidas por brazo, T = 1 y T = 0,7.
   - `data/j0*.jsonl`: jueces.
   - `lab/data/exploracion/choice_beta*.json`: pesos del modelo.
   - `lab/data/exploracion/bancos-sonnet/`: bancos con Sonnet.
   - La tabla de calibración se rehace con `calib_data.py`.
3. **Qué falló o quedó a medias.**
   - La primera búsqueda del trimestre se cortó a las 2 h con la salida en búfer y se repitió más pequeña (una ronda, 40 combinaciones).
   - El modelo de elección no puede valorar mejoras de percepción (sus pesos están ajustados a la lectura que hay): por eso las ideas de percepción se prueban en el banco, no en la réplica.
   - Las sondas del bucle de ex-v1 y ex-s1 y los bancos con DeepSeek quedan para el chat local.
4. **Siguiente paso.** El chat local sigue [plan-deepseek.md](plan-deepseek.md):
   - sondas de ex-v1 (~0,06 USD) y su banco de L1 (~0,12);
   - el banco de ex-v3 (~0,12);
   - si pasan, ex-v1 (o ex-v3) al corte 2.

   Para repetir algo de la réplica:

   ```bash
   uv run python scripts/exploracion/calib_data.py
   ```

   ```bash
   uv run python scripts/exploracion/choice_model.py
   ```

   ```bash
   uv run python scripts/exploracion/final_eval.py --games 4000
   ```
