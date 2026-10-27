# Banco de preguntas, categorías y objetivos por etapa

27 oct 2026, chat de Alejandro (rama `alejandro/optimistic-gauss-edyw1j`). Sólo bots y el simulador del otro chat. **No se ha jugado ninguna partida con Claude ni con DeepSeek** (cuota 0). La única cuota usada es la de 5 tareas de etiquetado con Haiku, de unas 115 mil fichas cada una.

Las preguntas de partida, de Alejandro:

1. Para cada pregunta, ¿hay siempre una respuesta que nos beneficia más? ¿Se puede hacer un banco de todas las preguntas?
2. ¿Se pueden agrupar las respuestas en categorías que DeepSeek reconozca fácilmente, con una política óptima por categoría?
3. ¿Cuál es el miniobjetivo que hay que perseguir en cada etapa?

**Datos usados**
- **Bots propios** (`scripts/question-bank/run.py`): 2.035 partidas de exploración con historias al azar y 2.631 de un bot ε-voraz (el 30 % al azar) con energía sensata. Son 4.666 partidas y 208.322 decisiones, en `~/careerlab-data/question-bank/`, fuera de Git porque llevan texto del juego.
- **Catálogo exacto del otro chat** (rama `main-1nddsg`, [motor-exacto.md](https://github.com/aleetreny/huawei/blob/main-1nddsg/lab/reports/ingenieria-inversa/motor-exacto.md)): sus 168 títulos, 403 preguntas y **936 respuestas**, con su efecto exacto y su riesgo oculto entero; su simulador `replica.py` (99 % de los pasos exactos), el bot de 7 reglas y `answer_values.csv`.
- **Partidas con IA del repo:** los resúmenes de `lab/reports/teacher-digests/`, con 286 partidas de Haiku y Opus y 30.917 decisiones de historia que se pueden cruzar con el catálogo.

Ese otro chat llegó antes y con datos mejores a gran parte de las preguntas 1 y 3; aquí se citan sus resultados y se comprueban por separado donde se puede. **Lo nuevo de este informe es la pregunta 2:** si un agente que sólo lee el texto puede elegir bien, y cuánto pierde.

## 1. El banco de preguntas y la "mejor respuesta"

- **El banco está completo:** 168 títulos, 403 preguntas (primera pregunta y continuaciones) y 936 respuestas, en `catalog_v2.json` de `main-1nddsg`. Cada respuesta tiene **siempre el mismo efecto**, sea cual sea el estado (M27 del otro chat). Mis 4.666 partidas de bots vieron 398 de esas preguntas.
- **Respuesta dominante.** En **160 de 403 preguntas (40 %)** hay una respuesta igual o mejor que todas las demás en cada indicador visible y con el mismo riesgo o menos. Es decir, la mejor en cualquier situación.
  - Es FIX en 119 casos, OWN en 25 y GUARD en 11 (categorías en la sección 2).
  - En las otras 243 preguntas hay un intercambio, por ejemplo más Network a cambio de más riesgo, o más Output a cambio de salud. La mejor respuesta depende del momento: del riesgo acumulado, de lo que falta para la próxima evaluación y del techo del nivel.
- **La respuesta de menos riesgo** está en una categoría segura (FIX, OWN, GUARD o ESCALATE) en **372 de 403 preguntas (92 %)**.
- **¿Las partidas que puntúan más eligen siempre lo mismo?** Haiku elige la misma opción en el 73 % de los casos de cada título, juegue con el manual que juegue. Las diferencias de nota entre opciones en las partidas con IA están mezcladas con quién sobrevive, así que no se pueden leer como el efecto de la opción. Lo que sí se mide con el catálogo exacto: **las partidas eliminadas de Haiku cogieron más riesgo evitable**, 21,0 pasos de riesgo por cada 100 decisiones frente a 15,9 en las terminadas (`llm_picks.out`).

## 2. Categorías que un agente reconoce, y lo que valen

**Método.** Antes de mirar ningún resultado se fijaron 10 categorías de comportamiento ([taxonomy.md](../../../scripts/question-bank/taxonomy.md)). Haiku, como sustituto de DeepSeek, etiquetó a ciegas las 936 respuestas leyendo sólo su texto (`labels.json`).

**Las categorías separan el riesgo oculto exacto** (`categories.out`):

| Categoría | Respuestas | Riesgo medio | Con riesgo > 0 | Efecto típico |
|---|---:|---:|---:|---|
| OWN (asumir, disculparse, corregir) | 74 | −0,39 | 14 % | Dignity +1,1 |
| FIX (arreglar bien, plan, acuerdo) | 278 | −0,10 | 11 % | Skill +1,0, Dignity +0,9, Network +0,7 |
| ESCALATE (canal formal) | 35 | −0,03 | 31 % | Dignity +1,2, Network −0,6 |
| GUARD (protegerse con educación) | 82 | 0,00 | 12 % | Health +0,5, Dignity +0,8 |
| SELL (venderse, buscar mérito) | 35 | +0,57 | 46 % | Output +0,5 |
| AVOID (no hacer nada) | 149 | +0,63 | 54 % | Network −0,3 |
| YIELD (ceder, hacer horas) | 93 | +0,96 | 65 % | **Health −1,3** |
| PERSIST (empecinarse) | 28 | +1,00 | 82 % | Network −1,0 |
| ATTACK (atacar, en público) | 55 | +1,20 | 85 % | **Network −1,5** |
| HIDE (ocultar, negar, atajos) | 107 | **+1,68** | 88 % | **Dignity −1,1** |

- Clasificar como "arriesgada" cualquier respuesta de SELL, AVOID, YIELD, PERSIST, ATTACK o HIDE acierta el **78 %**. Partiendo de "ninguna es arriesgada" se acierta el 59 %, y el clasificador por palabras del otro chat acertaba el 66 %.
- Detecta el **92 % de las respuestas de riesgo +2 o más**, que son las peligrosas (con 5 explota).
- El orden de las categorías se mantiene al partir los títulos en dos mitades al azar: la correlación del riesgo medio entre mitades es de 0,82 a 0,97.

**Lo que Haiku y Opus ya hacen** (`llm_picks.out`). Ya eligen casi siempre categorías seguras: FIX el 65 % y HIDE, ATTACK y PERSIST juntas menos del 1 %. Su riesgo evitable (el 6,5 % de las decisiones) está casi todo **dentro de opciones que parecen buenas**: 1.847 en FIX, 585 en OWN y 260 en GUARD. Al mirar las más repetidas sale un patrón de lenguaje:

- **Suben el riesgo, aunque suenen bien:** resolver en privado o fuera del registro ("a solas", "en privado después"), arreglar a medias o más tarde ("parches y arreglarlo luego", "sólo este servicio", "dejar los detalles") y cargar con un compromiso nuevo.
- **Lo bajan:** dejarlo por escrito y a la vista ("documentar la decisión"), arreglarlo entero ("revisar también el resto") y asumirlo en el momento.

Coincide con el vocabulario de M28 del otro chat (*quietly, later, keep* frente a *report, proper, fully, own*).

**¿Cuánto vale una política por categorías?** En el simulador de `main-1nddsg`, 1.000 partidas por brazo con las mismas semillas. La energía y la acción principal siguen siempre las 7 reglas; sólo cambia lo que el bot "ve" de cada opción de historia (`catbot.py`, `catbot.out`):

| Lo que ve el bot de cada opción | Nota | L6 | Crisis de confianza | Despidos |
|---|---:|---:|---:|---:|
| Efecto y riesgo exactos (bot de 7 reglas, "oráculo") | **67,7** | 51 % | 34 | 66 |
| Efecto exacto, riesgo según la categoría | 58,9 | 29 % | 219 | 91 |
| Categoría más etiquetas perfectas de indicador (sólo el signo) | 58,1 | 24 % | 215 | 101 |
| Efecto medio de la categoría, riesgo exacto | 53,7 | 11 % | 27 | 230 |
| Categoría más etiquetas de indicador de Haiku | 49,1 | 5 % | 152 | 208 |
| **Sólo la categoría** (efecto medio y riesgo de su categoría) | **46,7** | 2 % | 132 | 295 |
| Sólo el orden de categorías, sin efectos | 41,6 | 2 % | 240 | 330 |
| Categoría con un 20 % de etiquetas mal | 35,6 | 0 % | 364 | 270 |
| Historias al azar | 12,0 | 0 % | 703 | 3 |

Lectura:

1. **Sí hay una política por categoría que funciona:** recupera dos tercios de la distancia entre el azar y el oráculo (de 12 a 47, sobre 68). Pero sola no basta: deja 21 puntos.
2. **Esos 21 puntos se reparten así:**
   - ~14 por **no saber qué indicador mueve cada opción**. Se pierden en despidos (295): sin saber si una respuesta sube Network u Output, no se llega al techo justo en la evaluación.
   - ~9 por **juzgar el riesgo por la categoría**. Se pierden en crisis de confianza (219 frente a 34).
3. **La segunda dimensión es "qué indicador gana y cuál pierde".** Las etiquetas de Haiku aciertan Network y Dignity, pero **sólo detectan el 24 % de las respuestas que suben Skill** (`tags_acc.out`). Por eso aportan poco: 46,7 → 49,1, frente a 58,1 si fueran perfectas.
4. **Los errores de etiqueta cuestan mucho:** un 20 % de etiquetas mal baja la nota de 47 a 36. Las categorías tienen que ser fáciles y la Skill tiene que decir cómo resolver los casos dudosos.

**Límite importante.** Estos bots aplican una fórmula fija; DeepSeek razona sobre el texto y puede hacerlo mejor o peor. La tabla mide el valor de cada *percepción*, no la nota que sacará DeepSeek. Haiku sustituye a DeepSeek etiquetando; nadie ha medido todavía cómo etiqueta DeepSeek.

## 3. El miniobjetivo de cada etapa

El otro chat lo resolvió con el planificador óptimo (M12, M21 y M24 de `motor-exacto.md`). Con mis 4.666 partidas de bots se confirma por separado (`stages.out`):

- **Ascender depende de estar en el techo justo antes de la evaluación**, no de la nota:

  | Nivel | 0 de 3 en el techo | 1 de 3 | 2 de 3 | 3 de 3 |
  |---|---:|---:|---:|---:|
  | L1 | 0 % | 4 % | 15 % | 51 % |
  | L2 | 6 % | 15 % | 39 % | 78 % |

  Los 3 son Skill, Network y Output. La regla exacta del otro chat acierta el 99,5 %: Skill, Network y Output en el umbral, Dignity 4 o más, y nota distinta de D.
- **Con el estado del mes 5**, lo que más predice la nota final, aparte del nivel, es la **Dignity**. Coincide con M24: la charla de aviso de la evaluación depende de 4·Dignity + Health frente al riesgo.

**Miniobjetivo por etapa**, en forma general (sin números ni eventos):

| Etapa | Miniobjetivo |
|---|---|
| Cada semestre, antes de la evaluación | Llevar Skill, Network y Output al techo del nivel y **sostenerlos hasta la evaluación**. En el último mes, no ceder ninguno de los tres. |
| Siempre | Riesgo oculto bajo: comentario de RR. HH. tranquilo. Si deja de estarlo, sólo respuestas seguras y bajar el riesgo en el trimestre. |
| Antes de cada evaluación | Dignity alta y riesgo bajo, para evitar la charla de aviso, que suma riesgo y quita salud y dignidad. |
| Desde L4 (con Network y Output en el techo) | Skill: es el cuello de botella de los ascensos altos. |
| Niveles altos | Evitar las respuestas que cuestan dinero (se pierde ×2 o ×3). |
| Último trimestre | Riesgo a cero, y salud y dignidad al máximo. |

## 4. Qué propongo para la Skill (en inglés, sin números ni eventos)

Una regla de lectura en dos pasos, que se puede escribir en pocas líneas:

1. **Tipo de respuesta.**
   - Preferir arreglarlo bien y a la vista, asumir el error o protegerse con educación.
   - No ocultar, negar ni tomar atajos; no atacar ni dejar en evidencia; no empecinarse; no ceder a costa de la salud.
   - Pasividad y autobombo sólo con el riesgo tranquilo.
   - Ante dos respuestas constructivas: **la que deja constancia y lo resuelve entero** baja el riesgo; **la privada, parcial o aplazada** lo sube.
2. **Qué indicador mueve.** Antes de la evaluación, elegir la que sube el indicador que falta para el techo y no baja ninguno de los tres. Resolver uno mismo el problema técnico sube Skill: es lo que más se le escapa al lector.

Esta regla se apoya en categorías que Haiku reconoce; el resto del manual (energía y acción principal) ya está en las 7 reglas del otro chat.

## Relevo

1. **Hecho:**
   - Bots de 48 meses con historias al azar o ε-voraces (`run.py`) y su análisis (`analyse.py`, `stages.py`, `make_values.py`).
   - Taxonomía de 10 categorías y etiquetado ciego con Haiku de las 936 respuestas: `labels.json` por categoría y `stat-tags.json` por indicador, ambos sólo con identificadores y códigos.
   - Cruce con el catálogo exacto de `main-1nddsg` (`build_answers.py`, `categories.py`), con las partidas de IA (`llm_picks.py`) y bots de percepción en su simulador (`catbot.py`).
   - Las salidas están en esta carpeta (`*.out`).
2. **Datos:**
   - Partidas de bots en `~/careerlab-data/question-bank/` del contenedor, fuera de Git porque llevan texto del juego.
   - `answers.json` se regenera con `build_answers.py` desde una copia de `main-1nddsg`.
3. **A medias:**
   - El lote ε-voraz se paró en 2.631 de 3.000 partidas: no hacía falta más.
   - Mis estimaciones del valor por respuesta con bots quedan superadas por el catálogo exacto del otro chat y no se usan.
4. **Siguiente paso:**
   - (a) Escribir la regla de la sección 4 en una Skill y probarla con DeepSeek **sólo cuando lo decida Alejandro** (cuota y dinero).
   - (b) Antes, medir **cómo etiqueta DeepSeek**: darle `taxonomy.md` y 100 respuestas, con unos 0,02 USD, y comparar con `labels.json` y con el riesgo exacto.
   - (c) Mejorar la detección de Skill con una pista en la taxonomía y repetir `catbot.py` con las nuevas etiquetas.
   - Comandos:

   ```bash
   git worktree add ../rx-ref origin/main-1nddsg
   python3 scripts/question-bank/build_answers.py --rx ../rx-ref --out /tmp/answers.json
   python3 scripts/question-bank/categories.py --answers /tmp/answers.json --values ../rx-ref/lab/data/ingenieria-inversa/answer_values.csv
   python3 scripts/question-bank/catbot.py --rx ../rx-ref --answers /tmp/answers.json --tags lab/reports/question-bank/stat-tags.json --games 1000
   python3 scripts/question-bank/llm_picks.py --answers /tmp/answers.json
   ```

5. **Normas.** No se lee el motor (sólo las 5 herramientas oficiales y datos ya extraídos por el otro chat). Nada de este informe va a una Skill como número, título o respuesta concreta; sólo la regla general de la sección 4.
