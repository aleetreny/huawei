# Percepción de indicadores (línea de Leah)

**Pregunta.** Leyendo sólo el texto de una respuesta, ¿puede la IA saber qué indicador sube o baja? ¿Qué forma de pedírselo funciona, cuánta nota vale y cambia eso lo que elige?

Es el paso (c) de la línea **Categorías** de Alejandro ([question-bank/](../question-bank/README.md)), sobre su réplica del juego (línea **Motor**) y su banco de obediencia (línea **Transmisión**). Rama `leah/workspace`, código en [scripts/stat-perception/](../../../scripts/stat-perception/). Datos con texto del juego, fuera de Git, en `~/careerlab-data/stat-perception/` y `~/careerlab-data/transmision/`.

**Estado (27 oct, 16:50 UTC).** Hechos:
- 9 etiquetados con Haiku, medidos en una mitad reservada de los eventos y en la réplica;
- una prueba de elecciones en el banco de Transmisión.

Todo con la cuota Pro de Leah (unos 0,9 USD a precio de lista en etiquetado, y la ventana de 5 horas del 34 % al 42 % en el banco); nada de la Max. No se ha jugado ninguna partida completa. **La línea queda cerrada con Haiku. Lo siguiente es con DeepSeek, en la línea de Alejandro.**

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
5. **Redacción, para quien escriba manuales:**
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

## Archivos

| Archivo | Qué es |
|---|---|
| `tags-<forma>.json`, `tags-vote5*.json`, `tags-plain-rerun.json` | Etiquetas `{nodo:opción: {indicador: -1, 0 o 1}}`, sólo identificadores y códigos |
| `split.json` | Mitad de diseño y mitad reservada, como identificadores de nodo |
| `eval.json`, `replica*.json` | Tablas completas del etiquetado |
| `choice-test.out`, `choice-test-answers.json` | Prueba de elecciones: tablas de `score.py` y `fingerprint.py`, y elecciones por identificador |

Scripts en [scripts/stat-perception/](../../../scripts/stat-perception/):
- `label.py`: etiqueta con Haiku;
- `evaluate.py`: acierto en la mitad reservada;
- `replica_eval.py`: valor en la réplica;
- `combine.py`: votación;
- `run-choice.sh`: prueba de elecciones en el banco de Transmisión.

Manual de la prueba: [lab/policies-src/stat-perception/t13-perc/](../../policies-src/stat-perception/t13-perc/).

## Herramientas de Leah que siguen en uso

- **Panel de resultados.** [lab/panel/](../../panel/README.md): `scripts/panel/build.py` genera los datos y `lab/panel/live.html` sigue una partida en directo.
- **T11, varios ordenadores sin pisarse.** [t11-multi-machine/](../t11-multi-machine/README.md).
- **Trabajo anterior al 27 oct** (manuales l1-review-clock, f3-lean-polish, l6-routine): en [docs/historico/research/leah/](../../../docs/historico/research/leah/README.md), con un índice de conclusiones.

## Relevo

1. **Hecho.**
   - Paso (c) de Categorías: 9 etiquetados con Haiku (7 formas, defs3 y una repetición), medidos en la mitad reservada y en la réplica.
   - El valor de percibir bien cada indicador.
   - Una prueba de elecciones en el banco de Transmisión: t13-perc frente a t13-final y control, comprobación de versión del CLI y bloque general.
2. **Resultados.** Los de arriba; el detalle está en `01`–`05` y en los `.json` y `.out` de esta carpeta.
3. **A medias o descartado.**
   - La línea de percepción no entra en el manual: no mejora las elecciones (05).
   - La prueba de elecciones es de una pasada y n = 60; repetirla sólo merece la pena con una idea nueva.
4. **Siguiente paso.** Esta línea queda cerrada con Haiku. Lo que sigue es de la línea DeepSeek de Alejandro:
   - medir si DeepSeek etiqueta como Haiku, con `label.py` adaptado a su arnés: las mismas instrucciones `plain` y `defs`, comparadas con `split.json`;
   - si una **votación de varias lecturas** se puede convertir en algo que haga un solo lector, por ejemplo dos lecturas dentro de la misma respuesta.

   Para repetir:
   ```bash
   git worktree add ~/careerlab-data/stat-perception/rx-ref origin/main-1nddsg
   python3 scripts/question-bank/build_answers.py --rx ~/careerlab-data/stat-perception/rx-ref --out ~/careerlab-data/stat-perception/answers.json
   python3 scripts/stat-perception/label.py --answers ~/careerlab-data/stat-perception/answers.json --variant plain --out lab/reports/stat-perception/tags-plain.json
   python3 scripts/stat-perception/evaluate.py --answers ~/careerlab-data/stat-perception/answers.json --split lab/reports/stat-perception/split.json --tags plain=lab/reports/stat-perception/tags-plain.json --catbot-dir /tmp/ct
   .venv/bin/python scripts/stat-perception/replica_eval.py --rx ~/careerlab-data/stat-perception/rx-ref --answers ~/careerlab-data/stat-perception/answers.json --tags-dir /tmp/ct --games 1000
   # prueba de elecciones (necesita lab/data/transmision/ descomprimido en ~/careerlab-data/transmision/)
   scripts/stat-perception/run-choice.sh
   ```
