# Percepción de indicadores (línea de Leah)

**Pregunta.** Leyendo sólo el texto de una respuesta, ¿puede la IA saber qué indicador sube o baja? ¿Qué forma de pedírselo funciona y cuánta nota vale?

Es el paso (c) de la línea **Categorías** de Alejandro ([question-bank/](../question-bank/README.md)), sobre su réplica del juego (línea **Motor**). Rama `leah/workspace`, código en [scripts/stat-perception/](../../../scripts/stat-perception/). Datos con texto del juego, fuera de Git, en `~/careerlab-data/stat-perception/`.

**Estado (27 oct, 16:30 UTC).** Primera ronda terminada: 7 formas de etiquetar con Haiku (cuota Pro de Leah, 0,62 USD a precio de lista; nada de la Max), medidas en una mitad reservada de los eventos y en la réplica. Ningún manual escrito todavía y ninguna partida con IA.

## Conclusiones

1. **Pedir los 5 indicadores en cada opción es casi toda la mejora.**
   - Con las etiquetas de la línea Categorías, que nombran sólo el indicador evidente, la réplica saca 49,1.
   - Con una dirección para Skill, Network, Output, Health y Dignity en cada opción, saca **53,3**.
   - Votando 5 formas de leer, **54,4**.
   - Referencias: sólo la categoría saca 46,7 y las etiquetas perfectas 58,1.

   [01-siete-formas.md](01-siete-formas.md)
2. **El indicador que vale percibir es Output, no Skill.** Con Output perfecto la nota sube +2,5; con Skill perfecto baja −2,1, porque el bot persigue Skill, que se estanca en los niveles bajos, y pierde evaluaciones. Arreglar el "24 % de Skill" no compensa. [02-que-indicador-vale.md](02-que-indicador-vale.md)
3. **Haiku lee Output como "tiempo gastado"; el juego lo trata como impulso.**
   - Output baja al desentenderse, esquivar, pasar el trabajo a otro, pedir menos carga o quemarse.
   - Una charla corta o una revisión no lo bajan.
   - Escribir que la autopromoción sube Output empeora la nota (48,1), porque arrastra respuestas arriesgadas.

   [03-errores-output.md](03-errores-output.md)
4. **Redacción:**
   - Un significado corto de cada indicador funciona mejor que una lista de pistas y reduce a la mitad las crisis de confianza (73 frente a 136 por 1.000 partidas).
   - "Una ganancia y un coste por opción" hunde la nota (39,7).

**Propuesta para el manual.** Va en la referencia del mes previo a la evaluación, detrás del interruptor `Review in N` de Transmisión:

> Before choosing, consider what each option does to each of Skill, Network, Output, Health and Dignity, not just the obvious one.
> Output falls when you disengage, dodge a responsibility, hand your own work to someone else, ask for a lighter load or get worn down. A short conversation, a review or a bit of help does not cost Output.

Nunca presentar una conducta arriesgada (autopromoción, atajos) como forma de ganar un indicador.

**Límites.**
- El bot de la réplica aplica una fórmula a las etiquetas, mientras que una IA razona sobre el texto. Esto mide el valor de percibir, no la nota con DeepSeek.
- Haiku hace de DeepSeek.

## Experimentos

| Archivo | Conclusión en una frase |
|---|---|
| [01-siete-formas.md](01-siete-formas.md) | Pedir dirección en los 5 indicadores de cada opción sube la réplica de 49,1 a 53,3, y votar 5 formas a 54,4. |
| [02-que-indicador-vale.md](02-que-indicador-vale.md) | Percibir bien Output vale +2,5; percibir bien Skill resta 2,1. |
| [03-errores-output.md](03-errores-output.md) | Haiku confunde Output con tiempo gastado, y corregirlo diciendo "venderte sube Output" sale caro. |

## Archivos

| Archivo | Qué es |
|---|---|
| `tags-<forma>.json`, `tags-vote5.json`, `tags-vote5b.json` | Etiquetas `{nodo:opción: {indicador: -1, 0 o 1}}`, sólo identificadores y códigos |
| `split.json` | Mitad de diseño y mitad reservada, como identificadores de nodo |
| `eval.json`, `replica.json`, `replica-one-perfect.json` | Tablas completas de resultados |

Scripts en [scripts/stat-perception/](../../../scripts/stat-perception/):
- `label.py`: etiqueta con Haiku;
- `evaluate.py`: acierto en la mitad reservada;
- `replica_eval.py`: valor en la réplica;
- `combine.py`: votación.

## Herramientas de Leah que siguen en uso

- **Panel de resultados.** [lab/panel/](../../panel/README.md): `scripts/panel/build.py` genera los datos y `lab/panel/live.html` sigue una partida en directo.
- **T11, varios ordenadores sin pisarse.** [t11-multi-machine/](../t11-multi-machine/README.md).
- **Trabajo anterior al 27 oct** (manuales l1-review-clock, f3-lean-polish, l6-routine): en [docs/historico/research/leah/](../../../docs/historico/research/leah/README.md), con un índice de conclusiones.

## Relevo

1. **Hecho.** El paso (c) de Categorías, con 7 formas de etiquetar con Haiku, el acierto en la mitad reservada, el valor en la réplica y el valor de percibir bien cada indicador.
2. **Resultados.** Los de arriba; las tablas están en los archivos `01`–`03` y en los `.json` de esta carpeta.
3. **A medias.**
   - No se ha escrito ningún manual con esto ni se ha jugado ninguna partida.
   - Falta la variante `defs3` (significados más sólo el lado del coste de Output).
   - No se ha medido el etiquetado de DeepSeek: es el paso (b) de Alejandro, y lo decide él.
4. **Siguiente paso.** Probar si la propuesta cambia las **elecciones**, no sólo las etiquetas:
   - unas 150–200 preguntas del mes previo a una evaluación, con un estado típico (evaluación próxima, Network y Output en el techo, RR. HH. tranquilo);
   - Haiku con el manual de Transmisión (`t13-final`), con y sin las dos líneas;
   - puntuar cada elección con `answer_values.csv` de la línea Motor;
   - un bloque de preguntas de otros meses como control de contaminación.

   Coordinarlo antes con Alejandro, porque se solapa con su banco de Transmisión.

   Para regenerar los datos y repetir la medida:
   ```bash
   git worktree add ~/careerlab-data/stat-perception/rx-ref origin/main-1nddsg
   python3 scripts/question-bank/build_answers.py --rx ~/careerlab-data/stat-perception/rx-ref --out ~/careerlab-data/stat-perception/answers.json
   python3 scripts/stat-perception/label.py --answers ~/careerlab-data/stat-perception/answers.json --variant plain --out lab/reports/stat-perception/tags-plain.json
   python3 scripts/stat-perception/evaluate.py --answers ~/careerlab-data/stat-perception/answers.json --split lab/reports/stat-perception/split.json --tags plain=lab/reports/stat-perception/tags-plain.json --catbot-dir /tmp/ct
   .venv/bin/python scripts/stat-perception/replica_eval.py --rx ~/careerlab-data/stat-perception/rx-ref --answers ~/careerlab-data/stat-perception/answers.json --tags-dir /tmp/ct --games 1000
   ```
