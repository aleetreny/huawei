# 09. v4-lean y v4-lean-q: el plan de 08 hecho manual y medido

**Conclusión: v4-lean juega como v4 (misma elección en el 92–93 % de 139 situaciones del banco, dentro del ruido) y sube la rúbrica de ~72 a ~74; el ahorro de tokens que se puede ver con Haiku es pequeño (notas un 25 % más cortas). La palanca de tokens más segura es v4-lean-q, que planifica el trimestre con un solo `observe`: −15 % de tokens por partida en el modelo de 08 (~+0,7 de nota automática), sin depender de cuánto escriba DeepSeek. Corrección: v4 no saca 66 en la rúbrica sino ~70–72.**

28 oct, 10:45–12:30 UTC. Cuenta Pro de Leah: revisor de rúbrica (Sonnet) y banco de Transmisión con Haiku; la ventana de 5 horas pasó de ~41 % a 49 %. Sin cuota del equipo y sin DeepSeek.

## Los manuales

**[v4-lean](../../policies-src/stat-perception/v4-lean/)** es `t13-read-v4` (corte 1) con las reglas de decisión con la misma redacción, salvo:

| Cambio | Para qué |
|---|---|
| Línea de estado `Review in N \| Now S N O \| Best S N O` (sin Stalled, Expect ni Concerns) | Tokens y rúbrica; DeepSeek no rellenaba Stalled ([07](07-camino-l6.md)) |
| Línea 5 del trimestre: "Level 4 or above" en vez de "Network and Output both in Stalled" | Skill desde L4 (+0,6 en la réplica, 07) |
| "Concerns this month ≥ 1" → "you have already chosen an option this month that might bury a problem" | La misma regla de riesgo, sin contador en cada nota |
| Nota: línea de estado más, como mucho, una razón corta; "no escribas análisis fuera de la nota" | Tokens |
| "lower part of its 0–10 range" → "at 4 or below"; "comfortable" → "above 4"; ejemplo de reparto de las 3 de Energy; "costs far more…" como regla nuestra | Rúbrica: criterios concretos |
| Sección "Plan for the 48 months" (3 líneas, apoyada en el manual del empleado) | Rúbrica: mirada a 48 meses |

1.472 palabras frente a 1.609. Lint sin errores (sólo avisos de revisión, como v4).

**[v4-lean-q](../../policies-src/stat-perception/v4-lean-q/)** es v4-lean más una línea: planificar el trimestre tras un solo `observe` y llamar a `take_action` para cada acción de Energy y la principal sin observar entre medias, salvo que una falle.

En nuestras partidas los números de las opciones de Energy (1–8) y de acción principal (1–9) son los mismos en todos los trimestres, y Formato vio en la réplica que planificar el trimestre de una vez no pierde nada.

## Rúbrica (revisor Sonnet, `scripts/transmision/rubric.py`)

| Manual | Notas | Media |
|---|---|---:|
| t13-read-v4 | 58, 68, 72 (por la mañana) · 72, 74, 72, 72, 72, 72 | **70,2** con las 9 (72,3 con las 6 últimas) |
| v4-lean | 72, 74, 72, 74, 74, 80 | **74,3** |

**Corrección de [08](08-subir-nota-v4.md):** con 3 pasadas v4 parecía 66, y con 9 es ~70–72. La ganancia de la rúbrica es **~+2 a +4**, unos +0,2 a +0,4 de nota automática, no los +1,4 a +1,9 que estimé.

Quejas que siguen en v4-lean:
- el mapa de "riesgo oculto" se lee como heurística no publicada;
- la excepción de riesgo leve en el mes previo;
- poca guía sobre los demás finales (aislamiento, obsolescencia).

## Banco de Transmisión con Haiku

69 situaciones del mes previo a la evaluación (conjunto A) y 70 del bloque general (G1), las mismas para los dos manuales, en la forma oficial de entrega del Skill. Detalle en [lean-bank.out](lean-bank.out); elecciones por identificador en [lean-bank-answers.json](lean-bank-answers.json).

| | v4 | v4-lean |
|---|---:|---:|
| Misma elección que v4 | — | **92 % (mes previo) · 93 % (resto)** |
| Acierto, mes previo (61) | 67 % | 67 % |
| Pierde un punto necesario, mes previo | 23 % | 26 % |
| Acierto, bloque general (66) | 74 % | 70 % |
| Pérdida por decisión, bloque general | 0,77 | 0,85 |
| Fichas que escribe el modelo por situación | 49 | 51 |
| Nota (mediana) | 293 caracteres | **220** |
| Fichas de entrada por situación | 66k | 65k |

- **v4-lean elige como v4 dentro del ruido.** El control repetido de Transmisión coincide el 96 %, y nuestro t13-final frente al de Alejandro, con otro CLI, el 88 %. Las diferencias de acierto son 2–3 situaciones de 60–70.
- **Haiku escribe muy poco con los dos manuales** (~50 fichas por decisión). Las notas bajan un 25 %, unas 20 fichas menos por decisión, y eso en tokens es casi nada.
- DeepSeek razona más: sus partidas de v4 sacan ~158 mil fichas de salida, unas 400 por llamada. Si ese razonamiento entra en el historial, v4-lean le ahorraría más que a Haiku. Esto sólo se ve en sus trazas o en una partida oficial.

## Cuánto vale cada cambio de tokens (modelo de 08)

Cada `observe` deja ~650 fichas en el historial: un `observe` de trimestre son ~2.600 caracteres en nuestras partidas. Lo demás de cada decisión (~500 fichas) es lo que escribe el modelo y la respuesta de la herramienta. Simulando las ~384 llamadas de una partida con ese crecimiento:

| Cambio sobre v4 | Fichas por partida | Nota de tokens | Nota automática |
|---|---:|---:|---:|
| Notas −20 fichas por decisión (lo visto con Haiku) | −1 % | +0,6 | +0,1 |
| **Trimestre con un solo `observe` (v4-lean-q)** | **−15 %** | **+7** | **+0,7** |
| El modelo escribe la mitad (−250 fichas por decisión) | −16 % | +8 | +0,8 |
| Las dos cosas | −30 % | +14 | +1,4 |

## Para el corte 2

- **Candidato:** v4-lean-q.
  - Juega como v4 en el banco (93 % de elecciones iguales).
  - Rúbrica ~+2.
  - Línea de L4 (+0,6 en la réplica).
  - Trimestre con un solo `observe` (−15 % de tokens en el modelo).
  - Suma esperada: **~+1,5 de nota automática** sobre v4, más si DeepSeek escribía mucho.
- **Lo que falta y sólo se puede hacer con DeepSeek** (Alejandro):
  - una partida oficial de v4-lean-q para medir tokens por mes (v4: 1,35–1,47 M);
  - comprobar que el trimestre de un solo `observe` no da acciones rechazadas.

## Límites

- La rúbrica es la de nuestro revisor, no la del organizador.
- El banco es con Haiku, no con DeepSeek, y mide decisiones sueltas.
- El ahorro de tokens es de un modelo con supuestos (650 fichas por `observe`, unas 384 llamadas). La parte del trimestre no depende de cuánto escriba el modelo; la de "escribir menos", sí.
- v4-lean-q no se ha podido probar en el banco, que sirve situaciones de una en una.
