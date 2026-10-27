# Línea DeepSeek: qué entiende DeepSeek de cada respuesta

Rama `alejandro/deepseek`, Mac de Alejandro (donde está la clave). Encargo: [prompt-deepseek.md](../transmision/prompt-deepseek.md).

**Pregunta.** ¿Sabe `deepseek-v4-flash` ver qué indicador sube o baja cada respuesta y cuáles son arriesgadas? ¿Qué categorías reconoce y qué reglas obedece? Con eso, ¿cuál es la forma más masticada de darle las reglas?

## Conclusiones (27 oct, 17:15 UTC)

1. **DeepSeek ve bien el riesgo y mal Skill y Output.** Sin ayuda detecta el 83 % de las respuestas que suben el riesgo oculto y el 90 % de las peligrosas, pero sólo el 45 % de las que suben Skill y el 49 % de las que suben Output. Lee los tipos de respuesta mejor que Haiku ([percepcion.md](percepcion.md)).
2. **La mejor categorización es leer cada opción como seis signos más el riesgo**, con definiciones que digan cómo suele moverse cada indicador (prompt v3). Un bot que elige sólo con esa lectura de DeepSeek saca **56,0** en el simulador, frente a 46,7 con los 10 tipos de Haiku (lo que había que superar) y 67,7 el oráculo. Con las mismas definiciones, los 10 tipos solos se quedan en 48,5. Se confirma con los títulos reservados en percepción y en el simulador, aunque no en la pérdida por decisión del banco ([categorizacion.md](categorizacion.md)).
3. **Las pistas de lectura funcionan:** con ellas DeepSeek ve el 78 % de las subidas de Skill (antes 45 %) y el 86 % de los riesgos (antes 83 %). Output sigue a medias (47–54 %), y es la siguiente palanca: +2 puntos si se leyera bien.
4. **Una regla de grupo escrita, por orden, conserva casi todo:** "descarta lo arriesgado; si Health o Dignity están bajas, lo que las baja; en el mes previo a la evaluación, lo que baja Skill, Network u Output; de lo que queda, lo que más sube los indicadores de crecimiento". Con la lectura de DeepSeek saca 53,7 en el simulador.
5. **El manual t13-final se transmite a DeepSeek.** Lo lee en el 100 % de las situaciones y obedece el reparto trimestral casi como Haiku: Skill en L4 pasa del 2 % al 65 % y el comentario de RR. HH. del 15 % al 65 %. No le estropea las historias; probablemente se las mejora (pérdida −0,40 a −0,79 puntos por decisión según el control de referencia). Sólo los detonantes empeoran un poco ([obediencia.md](obediencia.md)).
6. **DeepSeek es menos constante que Haiku:** sin manual repite la misma elección en el 91 % de las historias (Haiku, 96 %), y entre dos lecturas cambia el 12–18 % de las etiquetas. Una sola pasada de etiquetas hace variar la nota del bot 5–7 puntos; por eso las medidas finales mezclan dos pasadas.

7. **Lo masticado: la ficha de lectura y la regla de historias dentro de t13-final** (`t13-read-v1`) arreglan los detonantes (acierto del 81 % al 91 %, pérdida −0,97) y la deriva lejos de Skill, y eligen las opciones de menos riesgo. En la pérdida media de las historias empatan con t13-final (−0,02) y mejoran a no tener manual (−0,47) ([masticado.md](masticado.md)).

**Propuesta.** `t13-read-v1` como candidato para el corte, con `t13-final` de reserva: misma pérdida media en el banco, menos riesgo, sin el fallo de los detonantes. Cuesta un 25 % más de fichas en las historias. El banco no confirma la ganancia que predice el simulador, así que sólo partidas oficiales dirían más. Con 0,4–0,6 USD por partida, sirven para comprobar que funciona de punta a punta, no para separar dos manuales parecidos (harían falta unas 45 por brazo).

## Gasto de DeepSeek

Presupuesto de la línea: 5 USD (parar a 3 y preguntar). Saldo de la clave al empezar: 0,1905 USD gastados. Gasto exacto en `GET /key`; el gasto por llamada, en `~/careerlab-data/deepseek/calls.jsonl`.

| Hora (UTC) | Qué | Llamadas | Coste (USD) | Acumulado de la línea |
|---|---|---:|---:|---:|
| 16:20 | Piloto: 5 llamadas de percepción (0,00014 por pregunta; 370–1.185 fichas de razonamiento por llamada; proveedores Baidu y Parasail) | 5 | 0,0007 | 0,001 |
| 16:25 | Percepción v1, títulos de diseño × 2 | 579 | 0,06 | 0,07 |
| 16:28–16:50 | Banco de obediencia: control y t13-final, 459 situaciones cada uno | 5.979 | 1,20 | 1,27 |
| 16:30–16:45 | Percepción v2 (×2), v3 (×2, todos los títulos), v1 en títulos reservados (×2) | 1.787 | 0,20 | 1,47 |
| 16:50 | Control repetido en el bloque general (139 situaciones) | 563 | 0,08 | 1,55 |
| 16:55–17:05 | Variante t13-read-v1 en 320 historias | 2.300 | 0,45 | **1,98** |

## Experimentos

| Informe | Qué mide | Estado |
|---|---|---|
| [percepcion.md](percepcion.md) | Qué ve DeepSeek de cada opción (tipo, signo de cada indicador, riesgo) | hecho |
| [categorizacion.md](categorizacion.md) | Qué agrupación entiende DeepSeek y discrimina; medida única en el simulador; regla de grupo escrita | hecho |
| [obediencia.md](obediencia.md) | Banco oficial con DeepSeek: control frente a t13-final; huella y control repetido | hecho |
| [masticado.md](masticado.md) | t13-final + ficha de lectura + regla de historias, en el banco | hecho |

## Código y datos

- `scripts/deepseek/ds.py`: cliente de la clave (lee `.env` sin copiarlo; sin proveedor fijado; temperatura 0,95; freno de gasto en 3 USD). `ds.py status` da el gasto.
- `perceive.py`: etiquetado y puntuación de la percepción. Prompts en `scripts/deepseek/prompts/`.
- `groupbot.py`: medida única en el simulador (`--bank` da la pérdida por decisión); `LexBot`, la regla escrita.
- `bench.py`: banco oficial con DeepSeek; `obedience.py` y `paired.py`, informes.
- Datos fuera de Git (llevan texto del juego): `~/careerlab-data/deepseek/` (respuestas de DeepSeek, etiquetas, ejecuciones del banco).

## Relevo

**27 oct, 17:15 UTC.**
1. **Qué se ha hecho y por qué.**
   - Arnés barato para la clave, con coste por llamada y freno de gasto.
   - Percepción (v1, sin pistas), porque era lo más barato y lo que más faltaba saber.
   - Categorización con una medida única en el simulador: el bot del motor que elige sólo con lo que DeepSeek percibe, `groupbot.py`. Se eligió con los títulos de diseño y se comprobó con los reservados.
   - Banco oficial de obediencia: control, t13-final y control repetido para separar el efecto del manual del ruido de la temperatura.
   - Una variante masticada, `t13-read-v1`, que mete en el manual la lectura ganadora y una regla escrita.
2. **Resultados:** conclusiones de arriba; detalles y tablas en [percepcion.md](percepcion.md), [categorizacion.md](categorizacion.md), [obediencia.md](obediencia.md) y [masticado.md](masticado.md). Datos en `~/careerlab-data/deepseek/` (fuera de Git: llevan texto del juego). Hallazgos B17–B21, C5–C8 y dos descartados en [HALLAZGOS.md](../../../HALLAZGOS.md).
3. **Lo que falló o quedó a medias.**
   - `t13-read-v1` sólo se midió en historias, no en el reparto trimestral (que no cambia).
   - La pérdida por decisión del banco no confirma en los títulos reservados la mejora v1 → v3 que sí se ve en percepción y en el simulador.
   - DeepSeek casi nunca escribe la lectura por opción en el formato pedido; la hace al razonar.
4. **Siguiente paso.**
   - Con el visto bueno de Alejandro: 1–2 partidas oficiales de `t13-read-v1` con DeepSeek (`make play` del runner; unos 0,4–0,6 USD cada una), para comprobar que juega de punta a punta, cuánto cuesta y si termina.
   - Sin gastar: mejorar la lectura de Output (+2 puntos en el simulador si se leyera bien) y probar si la regla escrita mejora con un paso de "el indicador que necesita la próxima evaluación".
   - Comandos:

   ```bash
   uv run python scripts/deepseek/ds.py status
   uv run python scripts/deepseek/perceive.py run --variant v4 --rep 1 --split dev
   uv run python scripts/deepseek/groupbot.py --labels v3=$HOME/careerlab-data/deepseek/labels/ds-v3-r1-full.json+$HOME/careerlab-data/deepseek/labels/ds-v3-r2-full.json --arms signs:flag,signs:flag:strict --games 2000
   uv run python scripts/deepseek/bench.py run --variant <bundle> --name ds-<arm> --ids ~/careerlab-data/deepseek/ids-ds1-events.txt
   uv run python scripts/deepseek/paired.py --a ds-t13-final --b ds-<arm> --phase e
   ```

   Las etiquetas y la lista de situaciones se regeneran con `perceive.py export` y `bench.py select --per-rule 40 --out ~/careerlab-data/deepseek/ids-ds1.txt`.
5. **Gasto:** 1,98 USD de los 5 de la línea; quedan 47,83 en la clave. Cuota de Claude: sólo este chat, sin partidas.

## Independent design review (27 October 2026)

[Three complete alternatives, short perception guide and t13-final critique](independent-designs/README.md). Recommendation: Evidence before preference. This is an untested design judgement, not a measured replacement for t13-read-v1. No games, API spending or changes to existing candidates. Standalone Skills: 387, 332 and 389 words; guide: 127 words.

### Relevo — independent designs

Read the supplied public handbook/rules and current manual including its review reference. Produced three alternatives within this existing line and checked word limits, front matter and report links. Full bundle lint does not apply before packaging. Next: review the proposed consequence-reading approach and validate perception/choice quality before funding full runs. See the report for exact files, falsifiers, limitations and handoff. Request integration of the design report with main; do not automatically submit or replace the current candidate.

## Relevo — independent review 2 (27 October 2026)

[Ranked audit, exact proposed Skill/reference patch, measurement reproductions and handoff](independent-designs/review-2.md). Corrects the previous review's timing criticism; recommends phase separation and survival precedence before changing strategy. Read-only implementation audit: no candidate/code/data edits, model calls or official games. Synthetic checks and saved-result analysis found dropped pending bank continuations, omitted bank terminal settlement, ideal-information context in the label bot and prescription/value metric differences. Recomputed +6.71 ±5.68 SE (95% CI −5.28 to +18.71); no confirmed career-score improvement. Four existing completion tests pass. Patch is proposed only; review it before any implementation or separately authorised model evaluation. Request integration of the report into main.
