# 08. Cómo superar la nota de `t13-read-v4` (corte 1): dónde están los puntos

**Conclusión: sin cambiar la estrategia de juego hay unos +3,5 a +4 puntos de nota automática en dos partes que nadie optimiza: los tokens (v4 saca ~64 de 100, y se puede subir a ~86 recortando lo que cada decisión añade al historial) y la calidad del SKILL.md (v4 saca 66 con el revisor, frente a 72,7 de t13-final). En el juego, la trampa de L1 es lo que más vale (hasta +2,3), pero no hay regla que la baje; la línea de L4 (07) suma ~+0,5.**

28 oct, 11:45–12:30 UTC. Fuentes:
- reglas oficiales (`competition-rules.rst` del repositorio oficial, copia local en `~/techarena-career-sim`);
- partidas oficiales de DeepSeek (`lab/registry-origins/deepseek/`);
- [mejora-nota.md](../deepseek/mejora-nota.md);
- el revisor de rúbrica de Transmisión (`scripts/transmision/rubric.py`, Sonnet, 3 pasadas por manual, cuenta Pro de Leah).

## La nota que se juega

Nota automática de una versión = 0,80 × media de 3 partidas + 0,10 × calidad de los SKILL.md + 0,10 × eficiencia de tokens. Una partida que no llega al mes 48 tiene la parte de tokens limitada a 50.

| Parte | v4 | Fuente |
|---|---:|---|
| Partidas | 71,67 y 70,22 completas; esperada ~63–65 contando la trampa de L1 (1 de cada ~9) | registro `deepseek`, [mejora-nota.md](../deepseek/mejora-nota.md) |
| Calidad del SKILL.md | **66** (58, 68, 72 en 3 pasadas; t13-final: 72,7) | `rubric.py`, 28 oct |
| Tokens | **~64**: 1,47 y 1,35 M por mes → 61 y 66 | registro `deepseek` |
| **Automática** | **~65,7 con la trampa, ~70,4 sin ella** | |

## Palanca 1. Tokens (10 %): de ~64 a ~86, +2,2 puntos

**Corrección:** Palancas estimó "como mucho +0,7" con la única partida de DeepSeek que había (24 meses, 667 mil por mes). Las partidas completas de v4 gastan el doble por mes, porque el contexto crece durante los 48 meses.

**Por qué gasta:**
- JiuwenSwarm no comprime el historial. La entrada por llamada crece en línea recta, unas 1.150 fichas por decisión: 37 mil al empezar, ~200 mil en el mes 33.
- `take_action` sólo devuelve `success`, así que cada decisión necesita su `observe`: unas 2 llamadas por decisión.
- Con unas 210 decisiones por partida:

  > tokens ≈ 2 · D · 37k + 1.150 · D² ≈ 15,5 M + 50,7 M ≈ **66 M** (reales: 65–70 M)

**El 77 % del gasto es el crecimiento**, lo que cada decisión deja en el historial: el texto de `observe`, el razonamiento visible y la nota del modelo. No es la base.

| Lo que deja cada decisión | Tokens por partida | Por mes | Nota de tokens | Nota automática |
|---|---:|---:|---:|---:|
| 1.150 (v4 hoy) | ~66 M | ~1,38 M | ~65 | — |
| 900 | ~55 M | ~1,15 M | ~74 | +1,0 |
| **575 (la mitad)** | **~41 M** | **~0,85 M** | **~86** | **+2,2** |

**Qué se puede recortar desde el Skill.** El texto de `observe` es fijo. Lo que escribe el modelo, no:
- el razonamiento visible antes de cada llamada;
- la línea de estado y la nota (v4 pide `Review in N | Now … | Best … | Stalled … | Concerns …` más una razón en cada decisión);
- las relecturas del Skill;
- las llamadas a `check_latest_logs`, cuyo resultado queda en el historial para siempre.

v6 ya pedía notas cortas en inglés, pero no hay partidas completas de v6 para medirlo.

**Lo que falta saber, y sólo se ve en las trazas de DeepSeek** (en el Mac de Alejandro, `~/careerlab-data/huawei-deepseek/runs/*/events.jsonl`): cuántas de esas 1.150 fichas son `observe` y cuántas escribe el modelo. Si el modelo escribe la mitad, recortarlo vale los +2,2. Si `observe` es casi todo, el margen está en hacer menos llamadas, por ejemplo planificar el trimestre con un solo `observe`.

## Palanca 2. Calidad del SKILL.md (10 %): de 66 a ~80–85, +1,4 a +1,9 puntos

El revisor (Sonnet con la rúbrica oficial) da a v4 una media de **66**, y a t13-final 72,7. Las debilidades que repite:
- **la línea de estado es pesada** (Best, Stalled, Expect, Concerns) y fácil de rellenar mal; además alarga cada nota;
- algunas pautas se presentan como mecánica del juego sin estar publicadas ("missing a risky option costs far more…");
- no hay plan a 48 meses (escalera de niveles, sueldo por nivel, dinero), sólo el último trimestre;
- criterios vagos ("lower part of its range", "for several months").

**Ojo con reescribir:** cambiar sólo la redacción cambia el comportamiento. Lo vimos con f3-lean-polish (de 49 % a 0 % de proyectos clave, [histórico](../../../docs/historico/research/leah/f3-lean-polish.md)). Transmisión subió de 58 a 73 sin cambiar el comportamiento, comprobándolo en su banco ([fase3-rubrica.md](../transmision/fase3-rubrica.md)). Una reescritura de v4 tiene que pasar por el banco de DeepSeek antes de jugarse.

**Coincidencia útil:** quitar Stalled, Expect y Concerns de la línea de estado arregla a la vez una queja de la rúbrica, recorta tokens (palanca 1) y no pierde nada, porque DeepSeek no rellena Stalled (07).

## Palanca 3. El juego (80 %)

| Cambio | Ganancia esperada en la nota automática | Estado |
|---|---:|---|
| Trampa de L1 a la mitad (de 1 de cada 9 a 1 de cada 18) | +2,3 | Sin regla que lo consiga: es sobre todo pérdida forzosa (06). La única palanca es percibir mejor; la idea 1 ("leer dos veces") la prueba Alejandro |
| Línea 5 del trimestre: "L4 or above" en vez de "Stalled" | ~+0,5 | Réplica: +0,6 con lectura de Haiku (07); falta el banco de DeepSeek |
| Llegar a L6 | +7 por partida que llega, pero sólo +0,3 de media con la línea anterior | Sin regla para llegar de forma fiable (07) |

## Plan propuesto para el corte 2 (30 oct)

1. **v4-lean** = v4 con:
   - la línea de estado reducida a `Review in N | Now S N O | Best S N O`;
   - nota de una frase;
   - "no escribas el razonamiento, llama directamente a la herramienta";
   - `check_latest_logs` sólo al reanudar;
   - la línea 5 del trimestre en "L4 or above".

   Una sola versión con dos objetivos: tokens y rúbrica.
2. **Comprobarlo sin partidas:** rúbrica (`rubric.py`, 3 pasadas) y banco de DeepSeek (obediencia y huella en el bloque general) frente a v4.
3. **Una o dos partidas oficiales sólo para medir tokens por mes**, con el visto bueno de Alejandro. Con los tokens de cada decisión basta una partida para ver si baja de 1,4 M.

**Si todo sale como en las cuentas:** +2,2 de tokens, +1,4 de rúbrica y +0,5 de L4, unos **+4 puntos de nota automática** sobre v4 sin tocar la estrategia de historias: de ~70,4 a ~74,5 sin trampa de L1, o de ~65,7 a ~69,8 con ella.

## Límites

- La cuenta de tokens es un modelo con los números que publicó Alejandro (base 37k, +1.150 por decisión, ~210 decisiones). No sé qué parte del crecimiento escribe el modelo: eso decide si la palanca 1 vale +2,2 o mucho menos.
- La rúbrica es la de nuestro revisor (Sonnet), no la del organizador. Varía ±7 entre pasadas.
- Las ganancias de juego vienen de la réplica con lectura de Haiku.
