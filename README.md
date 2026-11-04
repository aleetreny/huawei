# Gradient Depression · Huawei TechArena UK 2026 · *Career Survival*

Cómo enseñamos a una IA a sobrevivir una carrera de 48 meses escribiéndole sólo un manual, y todo lo que aprendimos por el camino.

**[Presentación final (18 diapositivas)](https://aleetreny.github.io/huawei/)** · [PDF](https://aleetreny.github.io/huawei/presentacion.pdf) · [Hallazgos](HALLAZGOS.md) · [Recrear el juego](docs/recrear-el-juego.md)

> **In English, in one paragraph.** Career Survival is a text game: an AI lives 48 months in a company, answers three situations a month, splits its energy every quarter and faces a review every six months. Teams do not play; they write a *Skill* (a Markdown manual) that DeepSeek reads inside the official JiuwenSwarm runner. We reverse-engineered the game from our own runs into a replica that matches the real engine move for move 98–99 % of the time, used it to find the ceiling (a perfect player averages ~72), and learned that a manual changes *how* the model works (habits, order, how much it reads) far more than *what it understands*. Our final Skill, `mv-3`, averaged 70.1 in its finished practice careers with less than half the tokens of our first version. Official scores: 64.75 (cut 1), 45.44 (cut 2), cut 3 pending. The working notes are in Spanish; the submissions and the deck are in English.

---

## El reto

- Una IA vive 48 meses en una empresa. Cada mes elige respuesta en 3 historias **sin ver qué cambia cada una**; cada trimestre reparte energía; cada 6 meses hay una evaluación que puede subirla de nivel.
- Se pierde de tres formas: no ascender (despido), dejar que el riesgo oculto explote (crisis de confianza) o agotarse.
- **No jugábamos nosotros:** entregábamos un manual en inglés (Skill) que lee `deepseek-v4-flash`.
- Nota de cada versión: 80 % la media de 3 partidas, 10 % la calidad del SKILL.md y 10 % el ahorro de fichas (tokens). Tres cortes: 27 oct, 30 oct y 1 nov.

## Resultado

| Corte | Manual | Nota oficial | Qué era |
|---|---|---:|---|
| 1 · 27 oct | [`t13-read-v4`](lab/policies-src/deepseek/t13-read-v4/) | **64,75** (puesto 13; el top 10 empezaba en 68,17) | Reglas de lectura de historias y de trimestre afinadas con Haiku y DeepSeek |
| 2 · 30 oct | [`mv-5r`](lab/policies-src/mejora/mv-5r/) | 45,44 | Reglas de v4 con el bucle de dos llamadas por respuesta (fichas ~95–100). La evaluación tiene mucho azar y nuestras partidas se hundieron (C80) |
| 3 · 1 nov | [`mv-3`](lab/policies-src/mejora/mv-3/bundle/skills/career-rules/SKILL.md) | **71,17** (nuestra mejor) | El manual de nuestras mejores carreras: 7 de 9 completas, media 70,1 en práctica |

**Clasificación final:** puesto **28 de los 88 equipos con nota** (227 inscritos), con 71,17 de nota de versión, que da 49,82 de 70 en la etapa 1. El top 10, que pasa al jurado, empezaba en 73,24 de nota de versión: nos quedamos a ~2 puntos, en un campo muy apretado (del puesto 2 al 27, entre 71,5 y 75,5).

Paquetes, documentos de diseño y vídeos de cada corte: [docs/entrega/](docs/entrega/README.md).

## La historia, en seis etapas

**1. Un laboratorio con Claude (26 oct).** Empezamos montando [`careerlab/`](careerlab/): partidas por la vía oficial, un registro y una carrera de manuales (`f1`…`f8`, `o1`…`o3`) jugados por Haiku. La referencia, `f3-lean-v1`, sacaba ~51. Aprendimos rápido que Haiku no se porta como DeepSeek, así que cada idea tenía que acabar confirmándose con el modelo de verdad.

**2. Abrir la caja negra (26–27 oct).** Con miles de partidas de bots (scripts sin IA) y sólo lo que devuelven las 5 herramientas oficiales, reconstruimos las reglas del motor: orden del mes, efecto de cada respuesta, riesgo oculto entero con explosión determinista, regla de ascenso, nota final. El resultado es [`replica.py`](scripts/ingenieria-inversa/replica.py): **98,5 % de los pasos, 99,8 % de los ascensos y 0,35 puntos de error en la nota** sobre 600 partidas nuevas ([motor-exacto.md](lab/reports/ingenieria-inversa/motor-exacto.md)). Un planificador afinado en la réplica sacó 70,5 en el juego real y llegó a L7.

**3. El techo y el suelo (28 oct).** Con la réplica medimos que **una media de 80 no existe**: el jugador perfecto saca ~72,4 (B31). Lo que resta no es jugar mejor las partidas buenas sino **no hundirse**: la trampa del primer ascenso (L1), que se salva llegando a la tercera evaluación con el riesgo oculto a cero (B30, B33), y las crisis de confianza (líneas [Techo](lab/reports/techo/) y [Suelo](lab/reports/suelo/)).

**4. Qué ve DeepSeek (27–29 oct).** DeepSeek detecta el **83 %** de las respuestas arriesgadas, pero sólo ~45–49 % de las que hacen crecer Skill u Output (B17, A6). Obedece las reglas del trimestre y las condiciones que ve por sí mismo, pero en las historias la redacción del manual casi no lo mueve (C26, C27). Calibrando la réplica con 2.743 decisiones reales suyas (C61) vimos que las reglas y los scripts mueven la media ±1–2: **el hueco de ~15 puntos con el jugador perfecto es percepción**, sobre todo en el mes previo a cada evaluación de L1 (C62).

**5. Las fichas (29 oct).** El gasto crecía con el cuadrado del número de llamadas, porque el programa no comprime el historial (C31). El **bucle de dos llamadas por respuesta** (línea [Comprobante](lab/reports/deepseek/comprobante.md)) bajó de ~1,4 M a ~0,5 M fichas por mes y dio nota de fichas 95–100. Preguntamos en Discord y los organizadores lo permitieron, igual que los scripts con estado durante la partida (C49, C60).

**6. Desconfiar de las pruebas baratas (30 oct–1 nov).** El corte 2 se hundió. Tres veces una prueba barata dijo que un cambio era mejor y las carreras completas dijeron lo contrario. Una sola frase de `mv-4` para arreglar un fallo («responder con texto en vez de actuar») empeoró las partidas: con ella, 5 de 11 acabaron antes de tiempo; sin ella (`mv-3`), 7 de 9 completas con media 70,1. Desde ahí sólo nos fiamos de carreras completas ([corte3](lab/reports/corte3/README.md), [mejora](lab/reports/mejora/README.md), [tramos](lab/reports/tramos/)).

## Qué funcionó y qué no

| Funcionó | No funcionó |
|---|---|
| La réplica del motor: probar ideas en segundos y sin gastar | Haiku como sustituto de DeepSeek (no cambia de elección con el texto, C24, C44) |
| Reglas de trimestre: DeepSeek las cumple (B20) | Reescribir cómo leer las historias: DeepSeek elige igual (C26, C27) |
| El bucle de dos llamadas: fichas de ~64 a ~95–100 | Scripts de ayuda: una carrera excelente, pero 3 de 7 acabaron antes y gastaban 1,6× fichas |
| Riesgo a cero antes de la tercera evaluación de L1 | La frase de `mv-4` contra las respuestas sin llamada |
| Preguntar en Discord antes de usar algo dudoso | Las pruebas baratas como criterio final (engañaron tres veces) |
| Un solo Skill, sin umbrales, con criterios concretos (calidad ~70–75) | La línea Formato: mejor partida 76,87, media 49,9 |

Todo lo aprendido, por importancia (A deciden la nota · B confirmado · C pista · X descartado), está en **[HALLAZGOS.md](HALLAZGOS.md)**, con un mapa por tema.

## Recrear el juego

Todo lo necesario para volver a jugar Career Survival fuera de la competición está en el repositorio: la réplica, el catálogo de 403 historias con el efecto y el riesgo exactos de cada respuesta, las partidas de bots y las reglas medidas. Guía: **[docs/recrear-el-juego.md](docs/recrear-el-juego.md)**.

```bash
export BB_DATA=$PWD/lab/data/ingenieria-inversa
python3 scripts/ingenieria-inversa/replica.py play --catalog $BB_DATA/catalog_v2.json --games 200
```

## Mapa del repositorio

| Carpeta | Qué hay |
|---|---|
| [`careerlab/`](careerlab/) | El laboratorio en Python: partidas por la vía oficial, registro, actores de Claude y DeepSeek, `lint` de cumplimiento. Uso en [lab/README.md](lab/README.md) |
| [`scripts/<línea>/`](scripts/) | Código de cada línea: `ingenieria-inversa` (réplica), `deepseek`, `comprobante`, `mejora`, `exploracion`, `entrega`… |
| [`lab/reports/`](lab/reports/README.md) | Un informe por línea de trabajo, con índice. Cada experimento empieza por su conclusión |
| [`lab/policies-src/`](lab/policies-src/) | Todos los manuales (Skills) que probamos, cada uno con su `policy.json` |
| [`lab/data/`](lab/data/) | Partidas de bots y de DeepSeek, bancos de situaciones y etiquetas (llevan texto del juego de desarrollo) |
| [`docs/entrega/`](docs/entrega/README.md) | Lo entregado en cada corte: documentos de diseño, guiones, presentaciones |
| [`docs/historico/`](docs/historico/README.md) | El proyecto hasta el 26 oct: carrera de manuales, investigación inicial |
| [`ESTADO.md`](ESTADO.md) · [`NORMAS.md`](NORMAS.md) | Cierre del proyecto y cómo trabajamos |

Instalación del laboratorio (Python 3.13, [`uv`](https://docs.astral.sh/uv/)):

```bash
uv sync
uv run pytest -q
```

## Equipo

Alejandro Treny, Matteo Zabban y Leah Benarroch. Gran parte de la investigación se hizo con agentes de IA dirigidos por el equipo.

## Sobre las normas

Nada de los Skills entregados contiene números, umbrales, títulos de eventos ni respuestas fijas sacados del motor: las normas lo prohibían aunque fueran ciertos. La réplica y los catálogos salieron sólo de nuestras propias partidas por las 5 herramientas oficiales, sin leer el paquete del motor, y se usaron para investigar, nunca para copiar a un manual.
