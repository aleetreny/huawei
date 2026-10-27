# Línea DeepSeek: qué entiende DeepSeek de cada respuesta

Rama `alejandro/deepseek`, Mac de Alejandro (donde está la clave). Encargo: [prompt-deepseek.md](../transmision/prompt-deepseek.md).

**Pregunta.** ¿Sabe `deepseek-v4-flash` ver qué indicador sube o baja cada respuesta y cuáles son arriesgadas? ¿Qué categorías reconoce y qué reglas obedece? Con eso, ¿cuál es la forma más masticada de darle las reglas?

## Conclusiones (27 oct, 20:05 UTC)

**Lo más importante: primeras partidas completas de DeepSeek.** `t13-read-v4` saca **71,67** y `t13-read-v5` 66,71 (48 meses, L5, riesgo 0, Health y Dignity al máximo). Antes de hoy, las tres partidas oficiales de DeepSeek habían acabado eliminadas. **Manual recomendado para el corte 1: [`t13-read-v4`](../../policies-src/deepseek/t13-read-v4/)** (commit `09d5735`). Detalles en [mejora-nota.md](mejora-nota.md).

Lo aprendido antes, con el banco y el simulador:

1. **DeepSeek ve bien el riesgo y mal Skill y Output.** Sin ayuda detecta el 83 % de las respuestas que suben el riesgo oculto y el 90 % de las peligrosas, pero sólo el 45 % de las que suben Skill y el 49 % de las que suben Output. Lee los tipos de respuesta mejor que Haiku ([percepcion.md](percepcion.md)).
2. **La mejor categorización es leer cada opción como seis signos más el riesgo**, con definiciones que digan cómo suele moverse cada indicador (prompt v3). Un bot que elige sólo con esa lectura de DeepSeek saca **56,0** en el simulador, frente a 46,7 con los 10 tipos de Haiku (lo que había que superar) y 67,7 el oráculo. Con las mismas definiciones, los 10 tipos solos se quedan en 48,5. Se confirma con los títulos reservados en percepción y en el simulador, aunque no en la pérdida por decisión del banco ([categorizacion.md](categorizacion.md)).
3. **Las pistas de lectura funcionan:** con ellas DeepSeek ve el 78 % de las subidas de Skill (antes 45 %) y el 86 % de los riesgos (antes 83 %). Output sigue a medias (47–54 %), y es la siguiente palanca: +2 puntos si se leyera bien.
4. **Una regla de grupo escrita, por orden, conserva casi todo:** "descarta lo arriesgado; si Health o Dignity están bajas, lo que las baja; en el mes previo a la evaluación, lo que baja Skill, Network u Output; de lo que queda, lo que más sube los indicadores de crecimiento". Con la lectura de DeepSeek saca 53,7 en el simulador.
5. **El manual t13-final se transmite a DeepSeek.** Lo lee en el 100 % de las situaciones y obedece el reparto trimestral casi como Haiku: Skill en L4 pasa del 2 % al 65 % y el comentario de RR. HH. del 15 % al 65 %. No le estropea las historias; probablemente se las mejora (pérdida −0,40 a −0,79 puntos por decisión según el control de referencia). Sólo los detonantes empeoran un poco ([obediencia.md](obediencia.md)).
6. **DeepSeek es menos constante que Haiku:** sin manual repite la misma elección en el 91 % de las historias (Haiku, 96 %), y entre dos lecturas cambia el 12–18 % de las etiquetas. Una sola pasada de etiquetas hace variar la nota del bot 5–7 puntos; por eso las medidas finales mezclan dos pasadas.

7. **Lo masticado: la ficha de lectura y la regla de historias dentro de t13-final** (`t13-read-v1`) arreglan los detonantes (acierto del 81 % al 91 %, pérdida −0,97) y la deriva lejos de Skill, y eligen las opciones de menos riesgo. En la pérdida media de las historias empatan con t13-final (−0,02) y mejoran a no tener manual (−0,47) ([masticado.md](masticado.md)).

8. **Partidas oficiales (2, aprobadas por Alejandro): las dos eliminadas por el riesgo oculto.** Partida 1: despido en el mes 24 en L1 (14,98). Partida 2: crisis de confianza en el mes 30 en L4 (42,51), tras crecer muy bien. En las dos el riesgo lo cargan opciones que parecen constructivas y que DeepSeek lee como prudentes: tratarlo en un 1:1 privado, una denuncia anónima, un cambio por fases, hacer menos para ganar tiempo. Coste: 0,23 y 0,31 USD; una partida completa costaría unos 0,45–0,50 ([partidas-oficiales.md](partidas-oficiales.md)).

**Propuesta.** `t13-read-v1` sigue siendo el candidato (misma pérdida media que t13-final en el banco, menos riesgo, sin el fallo de los detonantes), pero las partidas dicen que **el siguiente paso es frenar el riesgo "constructivo" en las historias**. Hay que hacerlo antes de más partidas, y se puede comprobar gratis en el banco y en el simulador. Ver la lectura de [partidas-oficiales.md](partidas-oficiales.md).

## Gasto de DeepSeek

Presupuesto de la línea: 5 USD (parar a 3 y preguntar). Saldo de la clave al empezar: 0,1905 USD gastados. Gasto exacto en `GET /key`; el gasto por llamada, en `~/careerlab-data/deepseek/calls.jsonl`.

| Hora (UTC) | Qué | Llamadas | Coste (USD) | Acumulado de la línea |
|---|---|---:|---:|---:|
| 16:20 | Piloto: 5 llamadas de percepción (0,00014 por pregunta; 370–1.185 fichas de razonamiento por llamada; proveedores Baidu y Parasail) | 5 | 0,0007 | 0,001 |
| 16:25 | Percepción v1, títulos de diseño × 2 | 579 | 0,06 | 0,07 |
| 16:28–16:50 | Banco de obediencia: control y t13-final, 459 situaciones cada uno | 5.979 | 1,20 | 1,27 |
| 16:30–16:45 | Percepción v2 (×2), v3 (×2, todos los títulos), v1 en títulos reservados (×2) | 1.787 | 0,20 | 1,47 |
| 16:50 | Control repetido en el bloque general (139 situaciones) | 563 | 0,08 | 1,55 |
| 16:55–17:05 | Variante t13-read-v1 en 320 historias | 2.300 | 0,45 | 1,98 |
| 17:18–18:30 | 2 partidas oficiales de t13-read-v1 (aprobadas por Alejandro) | — | 0,54 (0,229 + 0,310) | **2,52** |

## Experimentos

| Informe | Qué mide | Estado |
|---|---|---|
| [percepcion.md](percepcion.md) | Qué ve DeepSeek de cada opción (tipo, signo de cada indicador, riesgo) | hecho |
| [categorizacion.md](categorizacion.md) | Qué agrupación entiende DeepSeek y discrimina; medida única en el simulador; regla de grupo escrita | hecho |
| [obediencia.md](obediencia.md) | Banco oficial con DeepSeek: control frente a t13-final; huella y control repetido | hecho |
| [masticado.md](masticado.md) | t13-final + ficha de lectura + regla de historias, en el banco | hecho |
| [partidas-oficiales.md](partidas-oficiales.md) | 2 partidas oficiales de t13-read-v1 con DeepSeek | hecho |

## Código y datos

- `scripts/deepseek/ds.py`: cliente de la clave (lee `.env` sin copiarlo; sin proveedor fijado; temperatura 0,95; freno de gasto en 3 USD). `ds.py status` da el gasto.
- `perceive.py`: etiquetado y puntuación de la percepción. Prompts en `scripts/deepseek/prompts/`.
- `groupbot.py`: medida única en el simulador (`--bank` da la pérdida por decisión); `LexBot`, la regla escrita.
- `bench.py`: banco oficial con DeepSeek; `obedience.py` y `paired.py`, informes.
- Datos fuera de Git (llevan texto del juego): `~/careerlab-data/deepseek/` (respuestas de DeepSeek, etiquetas, ejecuciones del banco).

## Relevo

**27 oct, NIM: descartado.** NIM retiró `deepseek-v4-flash` el 7 de agosto (HTTP 410) y sólo sirve V4.1 Flash, que es otro modelo ([nim.md](nim.md)). La versión del reto sólo se consigue por OpenRouter.

**27 oct, 18:40 UTC.**
1. **Qué se ha hecho y por qué.**
   - Arnés barato para la clave, con coste por llamada y freno de gasto.
   - Percepción (v1, sin pistas), porque era lo más barato y lo que más faltaba saber.
   - Categorización con una medida única en el simulador: el bot del motor que elige sólo con lo que DeepSeek percibe, `groupbot.py`. Se eligió con los títulos de diseño y se comprobó con los reservados.
   - Banco oficial de obediencia: control, t13-final y control repetido para separar el efecto del manual del ruido de la temperatura.
   - Una variante masticada, `t13-read-v1`, que mete en el manual la lectura ganadora y una regla escrita.
   - 2 partidas oficiales de `t13-read-v1`, con el visto bueno de Alejandro, para comprobar el funcionamiento de punta a punta y el coste.
2. **Resultados:** conclusiones de arriba; detalles y tablas en [percepcion.md](percepcion.md), [categorizacion.md](categorizacion.md), [obediencia.md](obediencia.md), [masticado.md](masticado.md) y [partidas-oficiales.md](partidas-oficiales.md).
   - Datos en `~/careerlab-data/deepseek/` (banco y etiquetas) y `~/careerlab-data/huawei-deepseek/runs/` (partidas), fuera de Git porque llevan texto del juego.
   - El registro de las partidas está exportado en `lab/registry-origins/deepseek/`.
   - Hallazgos B17–B21, C5–C9 y dos descartados en [HALLAZGOS.md](../../../HALLAZGOS.md).
3. **Lo que falló o quedó a medias.**
   - `t13-read-v1` sólo se midió en historias, no en el reparto trimestral (que no cambia).
   - La pérdida por decisión del banco no confirma en los títulos reservados la mejora v1 → v3 que sí se ve en percepción y en el simulador.
   - DeepSeek casi nunca escribe la lectura por opción en el formato pedido; la hace al razonar.
   - Las dos partidas oficiales acabaron eliminadas por el riesgo.
4. **Siguiente paso** (sin gastar en partidas):
   - En la regla de historias, cuando el comentario de RR. HH. no sea el tranquilo, descartar también lo privado, anónimo, a medias, por fases o para ganar tiempo.
   - Acotar por escrito la regla 4 del reparto al trimestre.
   - Medirlo en el banco (detonantes, bloque general y las historias de los meses posteriores a una C) y en el simulador, frente a `t13-read-v1` y `t13-final`.
   - Más partidas oficiales, sólo con el visto bueno de Alejandro.
   - Comandos:

   ```bash
   uv run python scripts/deepseek/ds.py status
   uv run python scripts/deepseek/bench.py run --variant <bundle> --name ds-<arm> --ids ~/careerlab-data/deepseek/ids-ds1-events.txt
   uv run python scripts/deepseek/paired.py --a ds-t13-read --b ds-<arm> --phase e
   uv run python scripts/deepseek/groupbot.py --labels v3=$HOME/careerlab-data/deepseek/labels/ds-v3-r1-full.json+$HOME/careerlab-data/deepseek/labels/ds-v3-r2-full.json --arms signs:flag,signs:flag:strict,signs:flag:calm --games 2000
   CAREERLAB_ORIGIN=deepseek uv run python -m careerlab.target play --policy <name> --spend --games 1 --max-usd-per-game 1.2 --reserve-usd 15   # sólo con aprobación
   ```

   Las etiquetas y la lista de situaciones se regeneran con `perceive.py export` y `bench.py select --per-rule 40 --out ~/careerlab-data/deepseek/ids-ds1.txt`. Si aparece `No module named 'careerlab'` (iCloud), `chflags nohidden .venv/lib/python3.13/site-packages/*.pth` o `PYTHONPATH=.`.
5. **Gasto:** 2,52 USD de los 5 de la línea (quedan 0,48 antes del tope de 3 en que hay que preguntar); la clave lleva 2,71 USD gastados y le quedan 47,29. Cuota de Claude: sólo este chat, sin partidas de Claude.
