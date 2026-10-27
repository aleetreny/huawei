# Experimento 2. Rondas A y 2 del banco: dónde y cómo escribir cada regla

27 oct 2026, 10:20–11:40 UTC. Haiku por el CLI 2.1.303, entrega oficial (descripción en el mensaje de sistema, cuerpo con `skill_tool`), contexto corto (desde el principio del mes de la situación). Situaciones de títulos **no reservados**; las mismas para todos los brazos. Detalle del banco en [banco.md](banco.md).

## Brazos

| Brazo | Qué cambia |
|---|---|
| `control` | sin Skills |
| `f3lean` | f3-lean-v1, el manual de referencia |
| `t-body-imp` | las 6 reglas, imperativas y numeradas, sólo en el cuerpo; descripción genérica |
| `t-body-why` | igual, y cada regla con su porqué |
| `t-desc` | reglas compactas también en la `description` (siempre a la vista) |
| `t-instr` | reglas compactas también en la `instruction` del manifest (siempre a la vista, en IDENTITY.md) |
| `t-status` | línea de estado que el agente rellena en las notas antes de elegir (meses a la evaluación, RR. HH., dinero, meses que quedan, regla que aplica) |
| `t-multi` | un Skill por regla, cada uno con su descripción |
| `t2-imp` | ronda 2: textos corregidos (bajo riesgo, ceder para agradar también es arriesgado; cierre explícito) |
| `t2-veto` | ronda 2 como filtro: tachar las opciones prohibidas y elegir entre las demás |

## Resultados (acierto %, entre paréntesis el intervalo al 95 %)

| Regla | n | control | f3lean | t-body-imp | t-body-why | t-desc | t-instr | t-status | t-multi | t2-imp | t2-veto |
|---|---:|---|---|---|---|---|---|---|---|---|---|
| No ceder puntos antes de la evaluación | 60 | 62 | 62 | 70 | 72 | 72 | 70 | 72 | 67 | 73 | **77** (65–86) |
| Skill en L4 | 60 | 17 | 5 | 63 | 63 | 63 | 72 | 68 | **77** (65–86) | 62 | 65 |
| Comentario de RR. HH. | 33 | 18 | 58 | **85** (69–93) | 82 | 82 | 79 | 82 | 36 | 82 | 79 |
| Detonantes | 85 | **91** (83–95) | 88 | 82 | 82 | 85 | 87 | 86 | 84 | 89 | 88 |
| Ruina temprana | 60 | 65 | **70** | 63 | — | 65 | 67 | 68 | 65 | 67 | — |
| Cierre | 60 | 62 | 68 | 72 | **77** (65–86) | 77 | 75 | 68 | 70 | 65 | 67 |

Pérdida media de nota frente a la mejor opción (puntos de nota final, simulador): antes de la evaluación 2,20 (control) → 1,40 (`t2-veto`); detonantes 0,53 (control) → 1,83 (`t-body-imp`) y 0,97 (`t2-imp`).

## Lo que se aprende

1. **Haiku lee el Skill siempre** en esta condición (100 % de las situaciones llama a `skill_tool` antes de decidir, 82–98 % con varios Skills). Por eso el sitio de la regla (cuerpo, descripción o instrucción) apenas cambia el resultado aquí: las diferencias entre formatos están dentro del ruido. El sitio importará cuando el cuerpo quede lejos en un historial largo (siguiente experimento).
2. **El reparto trimestral obedece si la regla es imperativa y concreta.** Skill en L4 pasa del 17 % (control) y el 5 % (f3-lean) al 62–77 %; el comentario de RR. HH., del 18 % al 79–85 %. Anoche Haiku no invertía en Skill en L4: el problema era el texto (f3-lean manda recuperar o defusar), no el modelo.
3. **Varios Skills reparten mal la atención:** con un Skill por regla, Haiku lee sólo el que cree relevante y la regla de RR. HH. cae al 36 %.
4. **Una regla mal escrita empeora las decisiones.** “Evita confrontar o exponerte” hizo que Haiku cediera para agradar, que también es una respuesta arriesgada (detonantes: 91 % → 82 %, y la pérdida de nota se triplica). La ronda 2 separa “mantener tu opinión con calma” (seguro) de “ceder para agradar” (arriesgado) y lo arregla (89 %).
5. **El orden es prioridad para Haiku.** En la ronda 2, la regla de Skill (2.ª) ganó a la de cierre (6.ª) en el último trimestre: Haiku eligió Skill learning en el mes 48. La ronda 3 pone las reglas en orden de prioridad y lo dice.
6. **Antes de la evaluación el cuello de botella es la percepción.** Las respuestas no muestran su efecto; Haiku obedece la regla (“no bajes Network ni Output”) pero no reconoce qué opción cuesta Output (seguir el proceso completo, rehacer un informe). Formato filtro (`t2-veto`) es el mejor (77 %); la ronda 3 prueba ejemplos inventados de cómo leer el coste de una opción.
7. **Ruina temprana no es un problema de obediencia:** Haiku casi nunca elige una opción que cuesta dinero con poco dinero (2–3 % en todos los brazos, también sin Skill).

## Cuánto vale cada regla en el simulador

`simvalue.py`: el planificador juega 400 partidas; para una regla, en sus situaciones, obedece con probabilidad p y si no hace lo que hace Haiku sin Skill (acción principal Apply for a key project, energía a recuperar o Network, historia al azar).

| Regla | Nota con obediencia total | Pérdida con p = 0,5 | Pérdida con p = 0 |
|---|---:|---:|---:|
| (ninguna) | 71,1 ± 0,5 | | |
| Antes de la evaluación | | 14,0 | 33,5 |
| Skill en L4 | | 0,3 | 0,6 |
| Comentario de RR. HH. | | 0,8 | 1,3 |
| Detonantes | | 24,2 | 40,1 |
| Ruina temprana | | 17,5 | 41,6 |
| Cierre | | 3,0 | 8,9 |

En las historias, elegir al azar es mucho peor que lo que hace Haiku sin Skill (acierta 62–91 %), así que esas pérdidas son un techo. Lo útil es el orden: **lo que decide la nota son las respuestas a las historias** (antes de la evaluación, detonantes, dinero); **el reparto trimestral vale poco** en el simulador (Skill en L4, 0,6 puntos; RR. HH., 1,3), aunque sea donde un manual más manda. Una estimación más fiel por regla: pérdida media por situación (columna de arriba) × situaciones decisivas por partida (en el informe de la fase 2).
