# Percepción de indicadores (línea de Leah)

**Pregunta.** Leyendo sólo el texto de una respuesta, ¿puede la IA saber qué indicador sube o baja? ¿Qué forma de pedírselo funciona, cuánta nota vale y cambia eso lo que elige?

Es el paso (c) de la línea **Categorías** de Alejandro ([question-bank/](../question-bank/README.md)), sobre su réplica del juego (línea **Motor**) y su banco de obediencia (línea **Transmisión**). Rama `leah/workspace`, código en [scripts/stat-perception/](../../../scripts/stat-perception/). Datos con texto del juego, fuera de Git, en `~/careerlab-data/stat-perception/` y `~/careerlab-data/transmision/`.

**Estado (28 oct, 10:30 UTC).** Hechos:
- 9 etiquetados con Haiku, medidos en una mitad reservada de los eventos y en la réplica;
- una prueba de elecciones en el banco de Transmisión;
- un estudio de la trampa del primer ascenso (L1) en la réplica, con 13 brazos;
- un estudio del camino a L6 en la réplica;
- un plan para superar la nota de v4: tokens, rúbrica y juego, con la rúbrica de v4 medida.

Todo con la cuota Pro de Leah (unos 0,9 USD a precio de lista en etiquetado, y la ventana de 5 horas del 34 % al 42 % en el banco); nada de la Max. No se ha jugado ninguna partida completa. **Con Haiku y la réplica no queda nada prometedor. Lo siguiente es con DeepSeek, en la línea de Alejandro.**

## Conclusiones

1. **Para etiquetar, pedir los 5 indicadores en cada opción es casi toda la mejora.**
   - Etiquetas de Categorías, que nombran sólo el indicador evidente: 49,1 en la réplica.
   - Una dirección para Skill, Network, Output, Health y Dignity en cada opción: **52–53**.
   - Votación de 5 lecturas: **54–55**, y la mejor es vote5c con 55,1.
   - Referencias: sólo la categoría saca 46,7 y las etiquetas perfectas 58,1.
   - Repetir un mismo etiquetado mueve la nota 1,2 puntos, así que diferencias menores entre formas sueltas son ruido.

   [01](01-siete-formas.md), [04](04-defs3-y-ruido.md)
2. **El indicador que vale percibir es Output, no Skill.** Con Output perfecto la nota sube +2,5; con Skill perfecto baja −2,1, porque el bot persigue Skill, que se estanca en los niveles bajos. [02](02-que-indicador-vale.md)
3. **Haiku etiqueta Output como "tiempo gastado"; en el juego se comporta más como impulso.**
   - Ninguna redacción de Output mejora a un lector solo: con sólo el lado del coste, defs3 saca 50,9.
   - Decir que la autopromoción sube Output sale caro: 48,1, con más del doble de crisis de confianza.

   [03](03-errores-output.md), [04](04-defs3-y-ruido.md)
4. **Percibir mejor no es elegir mejor.** Al poner la línea de percepción en la referencia del mes previo de `t13-final` (t13-perc), Haiku **no** elige mejor antes de la evaluación. Tiende a peor: pierde un punto necesario en el 30 % de las situaciones frente al 18 %, aunque con n = 60 los intervalos se solapan. Además cambia el 10 % de las historias de otros meses. [05](05-prueba-de-elecciones.md)
5. **La trampa de L1 es sobre todo pérdida forzosa, no sólo percepción.**
   - En los dos meses previos a una evaluación en L1, 2 de cada 3 puntos de Network u Output perdidos no tenían alternativa segura; con lectura perfecta, 3 de cada 4.
   - La nota D de los meses 18 y 24 es consecuencia de fallar los meses 6 y 12.
   - Ninguna de 7 reglas nuevas baja los despidos sin subir las crisis: vetar tipos de respuesta, dos lecturas prudentes, priorizar subidas y llenar en el trimestre.
   - La palanca con efecto sigue siendo leer mejor: con lectura perfecta, acabar en L1 baja del 23 % al 13 %.

   [06](06-trampa-l1.md)
6. **El camino a L6 se pierde en L4, y una regla de trimestre ayuda un poco.**
   - Llegar a L6 vale +7 puntos por partida, pero se llega a L5 en el mes ~43 tras 17–18 meses en L4 ganando Skill, casi todo con historias.
   - La línea de v4 que pone Skill en el trimestre depende de "Stalled", que DeepSeek no rellena, así que no se aplica nunca.
   - Ponerla sin condiciones **a partir de L4** (Skill learning y Apply for rotation, como en t13-final) da +0,6 de nota y L6 del 1 % al 5 % con lectura de Haiku.
   - Empezar en L3 cuesta 1,8.

   [07](07-camino-l6.md)
7. **Para superar a v4 hay más nota fuera del juego que dentro.**
   - Tokens: v4 saca ~64 de 100 (1,35–1,47 M por mes), porque JiuwenSwarm no comprime el historial y cada decisión añade ~1.150 fichas. Recortar a la mitad lo que deja cada decisión daría ~86, **+2,2 puntos**.
   - Calidad del SKILL.md: el revisor da a v4 un **66**, frente a 72,7 de t13-final. Hay +1,4 a +1,9 si se reescribe sin cambiar el comportamiento.
   - En total, unos **+4 de nota automática** sin tocar la estrategia de historias.

   [08](08-subir-nota-v4.md)
8. **Redacción, para quien escriba manuales:**
   - un significado corto de cada indicador funciona mejor que una lista de pistas y reduce a la mitad las crisis de confianza (73 frente a 136 por 1.000 partidas);
   - "una ganancia y un coste por opción" hunde la nota (39,7);
   - nunca presentar una conducta arriesgada como forma de ganar un indicador.

**Para el manual.** Se queda la redacción de `t13-final` en la referencia del mes previo. La línea de percepción ("considera los 5 indicadores; desentenderse cuesta Output") **no** entra: mejora el etiquetado, pero no las elecciones. Lo que sí sirve de esta línea:
- la forma de pedir percepción (los 5 indicadores por opción, significados cortos, votar varias lecturas) para medir a DeepSeek;
- las tres redacciones que no hay que usar.

**Límites.**
- La réplica mide el valor de percibir para un bot que aplica una fórmula, no la nota de una IA.
- La prueba de elecciones es de una sola pasada por brazo y con 60 situaciones.
- Haiku hace de DeepSeek.

## Experimentos

| Archivo | Conclusión en una frase |
|---|---|
| [01-siete-formas.md](01-siete-formas.md) | Pedir dirección en los 5 indicadores de cada opción sube la réplica de 49,1 a 53,3, y votar 5 formas a 54,4. |
| [02-que-indicador-vale.md](02-que-indicador-vale.md) | Percibir bien Output vale +2,5; percibir bien Skill resta 2,1. |
| [03-errores-output.md](03-errores-output.md) | Haiku confunde Output con tiempo gastado, y corregirlo diciendo "venderte sube Output" sale caro. |
| [04-defs3-y-ruido.md](04-defs3-y-ruido.md) | Repetir un etiquetado mueve la réplica 1,2 puntos; defs3 sola etiqueta peor, pero en la votación da la mejor nota (55,1). |
| [05-prueba-de-elecciones.md](05-prueba-de-elecciones.md) | La línea de percepción en la referencia del mes previo no hace elegir mejor a Haiku (pierde un punto necesario un 30 % frente al 18 % de t13-final). |
| [06-trampa-l1.md](06-trampa-l1.md) | 2 de cada 3 puntos perdidos antes de una evaluación en L1 son forzosos, y ninguna de 7 reglas nuevas baja los despidos sin subir las crisis. |
| [07-camino-l6.md](07-camino-l6.md) | L6 vale +7 por partida pero se pierde tiempo en L4; Skill learning y rotation en el trimestre desde L4, sin condiciones, es la única regla que ayuda (+0,6). |
| [08-subir-nota-v4.md](08-subir-nota-v4.md) | Sin cambiar la estrategia hay ~+4 puntos de nota automática sobre v4: tokens (de ~64 a ~86) y calidad del SKILL.md (66 medido). |

## Archivos

| Archivo | Qué es |
|---|---|
| `tags-<forma>.json`, `tags-vote5*.json`, `tags-plain-rerun.json` | Etiquetas `{nodo:opción: {indicador: -1, 0 o 1}}`, sólo identificadores y códigos |
| `split.json` | Mitad de diseño y mitad reservada, como identificadores de nodo |
| `eval.json`, `replica*.json` | Tablas completas del etiquetado |
| `choice-test.out`, `choice-test-answers.json` | Prueba de elecciones: tablas de `score.py` y `fingerprint.py`, y elecciones por identificador |
| `l1-trap.json` | Trampa de L1: nota, despidos, crisis, causas y pérdidas por brazo |
| `l6.json` | Camino a L6: nota, % en L5 y L6, Skill final y mes de L5 por brazo, con lectura perfecta y de Haiku |

Scripts en [scripts/stat-perception/](../../../scripts/stat-perception/):
- `label.py`: etiqueta con Haiku;
- `evaluate.py`: acierto en la mitad reservada;
- `replica_eval.py`: valor en la réplica;
- `combine.py`: votación;
- `run-choice.sh`: prueba de elecciones en el banco de Transmisión;
- `l1_trap.py`: la trampa de L1 en la réplica (causas de cada evaluación fallida, pérdidas forzosas o evitables, brazos);
- `l6.py`: el camino a L6 en la réplica (meses de cada ascenso, por qué fallan las evaluaciones de L4 y L5, reglas de trimestre).

Manual de la prueba: [lab/policies-src/stat-perception/t13-perc/](../../policies-src/stat-perception/t13-perc/).

## Herramientas de Leah que siguen en uso

- **Panel de resultados.** [lab/panel/](../../panel/README.md): `scripts/panel/build.py` genera los datos y `lab/panel/live.html` sigue una partida en directo.
- **T11, varios ordenadores sin pisarse.** [t11-multi-machine/](../t11-multi-machine/README.md).
- **Trabajo anterior al 27 oct** (manuales l1-review-clock, f3-lean-polish, l6-routine): en [docs/historico/research/leah/](../../../docs/historico/research/leah/README.md), con un índice de conclusiones.

## Relevo

1. **Hecho.**
   - Paso (c) de Categorías: 9 etiquetados con Haiku, medidos en la mitad reservada y en la réplica.
   - El valor de percibir bien cada indicador.
   - Una prueba de elecciones en el banco de Transmisión (01–05).
   - **28 oct:** plan para superar a v4 (08): desglose de la nota, modelo de tokens y rúbrica de v4 medida (66).
   - **28 oct:** el camino a L6 en la réplica (07): dónde se pierde el tiempo y 9 variantes de trimestre e historias.
   - **28 oct:** la trampa de L1 en la réplica (06):
     - de qué fallan las evaluaciones;
     - qué parte de las pérdidas es forzosa;
     - 13 brazos con 7 reglas nuevas y sus combinaciones.
2. **Resultados.** Los de arriba; el detalle está en `01`–`06` y en los `.json` y `.out` de esta carpeta.
3. **A medias o descartado.**
   - La línea de percepción no entra en el manual (05).
   - Ninguna regla nueva contra la trampa de L1 gana en la réplica (06), así que no se ha probado en el banco ni en partidas.
   - Las medidas de 06 usan la lectura de Haiku, porque las etiquetas de DeepSeek de Alejandro no están en el repo.
4. **Siguiente paso.** Lo que queda es de la línea DeepSeek:
   - **v4-lean para el corte 2 (08):** línea de estado corta, nota de una frase, sin razonamiento escrito, registro sólo al reanudar, y la línea 5 en "L4 or above" (07). Comprobarlo con la rúbrica y el banco de DeepSeek, y medir tokens con una partida;
   - **medir en las trazas de DeepSeek** qué parte de las ~1.150 fichas por decisión escribe el modelo y qué parte es `observe` (08);
   - medir si leer dos veces y votar dentro de la misma respuesta mejora la percepción de los costes de Network y Output en DeepSeek (con Haiku, la votación quita crisis pero apenas despidos);
   - repetir `l1_trap.py` con las etiquetas de DeepSeek (`--reading` acepta archivos de etiquetas con el formato de `tags-*.json`; las de DeepSeek habría que convertirlas).

   Para repetir:
   ```bash
   git worktree add ~/careerlab-data/stat-perception/rx-ref origin/main-1nddsg
   python3 scripts/question-bank/build_answers.py --rx ~/careerlab-data/stat-perception/rx-ref --out ~/careerlab-data/stat-perception/answers.json
   python3 scripts/stat-perception/label.py --answers ~/careerlab-data/stat-perception/answers.json --variant plain --out lab/reports/stat-perception/tags-plain.json
   python3 scripts/stat-perception/evaluate.py --answers ~/careerlab-data/stat-perception/answers.json --split lab/reports/stat-perception/split.json --tags plain=lab/reports/stat-perception/tags-plain.json --catbot-dir /tmp/ct
   .venv/bin/python scripts/stat-perception/replica_eval.py --rx ~/careerlab-data/stat-perception/rx-ref --answers ~/careerlab-data/stat-perception/answers.json --tags-dir /tmp/ct --games 1000
   # prueba de elecciones (necesita lab/data/transmision/ descomprimido en ~/careerlab-data/transmision/)
   scripts/stat-perception/run-choice.sh
   # trampa de L1 (sin cuota; usa la réplica de main)
   .venv/bin/python scripts/stat-perception/l1_trap.py --games 2000 --arms base,perfect,cat1,fill,vote --json-out /tmp/l1.json
   # rúbrica de un manual (Sonnet; necesita local-runs/official-runner con las reglas oficiales)
   CAREERLAB_CLAUDE_EXE=$(which claude) uv run python scripts/transmision/rubric.py lab/policies-src/deepseek/t13-read-v4/bundle --runs 3
   # camino a L6 (sin cuota)
   .venv/bin/python scripts/stat-perception/l6.py --games 2000 --reading tags-plain.json+tags-plain-rerun.json --arms blind,sk4,sk4r,sk3r,ref
   ```
