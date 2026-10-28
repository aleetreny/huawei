# Sustitutos gratis de DeepSeek: ¿quién se equivoca como él?

**Conclusión: el sustituto más parecido en conjunto es Sonnet 5 (76–86 % de coincidencia con DeepSeek, frente a 82–89 % de DeepSeek consigo mismo, y falla en las bajadas de Output casi como él). Para Output a coste cero, Qwen local (8 de sus 9 fallos son los de DeepSeek). Haiku 5.5 y Luna ven Output mucho mejor que DeepSeek y harían parecer buenas ideas que no lo son.** 28 oct 2026, sin gastar de la clave.

## Prueba

- **Muestra:** las mismas 60 situaciones (146 opciones) que DeepSeek ya etiquetó dos veces con `perceive-v3`. Se eligieron 40 con alguna bajada real de Output o Network y 20 al azar (semilla 11).
- **Mismo prompt para todos.** La verdad es la del catálogo de la réplica.
- **Los sustitutos:**
  - **Qwen3.6-35B-A3B** en 4 bits, local con oMLX: 3 tandas de 20, ~4 min por tanda, gratis;
  - **Haiku** con la CLI de Claude: 3 llamadas;
  - **Luna**, en un chat de ChatGPT sin acceso al repo (el repo tiene las respuestas), nivel medio, en un solo mensaje.
- **Datos:** prompts y respuestas en `~/careerlab-data/proxies/` (tienen texto del juego).

## Resultados

Coincidencia con DeepSeek, media frente a sus dos lecturas:

| | Output | Network | Skill | Riesgo |
|---|---:|---:|---:|---:|
| DeepSeek consigo mismo | 82 % | 86 % | 89 % | 87 % |
| Qwen local | 79 % | 76 % | 81 % | 66 % |
| Haiku | 67 % | 77 % | 87 % | 71 % |
| Luna (medio) | 53 % | 76 % | 86 % | 80 % |
| Haiku 4.5 | 65 % | 80 % | 82 % | 83 % |
| Sonnet 4.6 | 74 % | 79 % | 84 % | 83 % |
| **Sonnet 5** | **76 %** | **83 %** | **86 %** | **83 %** |

Bajadas reales que no ven, y cuántas de ellas tampoco ve DeepSeek (lectura 1):

| | Output (20 bajadas) | Network (36 bajadas) | Ve el riesgo real / falsa alarma |
|---|---|---|---|
| DeepSeek | 8 | 7 | 88 % / 24 % |
| Qwen | 9 (8 en común) | 13 (6 en común) | 73 % / 14 % |
| Haiku | 5 (5 en común) | 8 (5 en común) | 86 % / 18 % |
| Luna | 4 (4 en común) | 14 (6 en común) | 88 % / 26 % |
| Haiku 4.5 | 6 (6 en común) | 7 (5 en común) | 83 % / 20 % |
| Sonnet 4.6 | 6 (5 en común) | 9 (5 en común) | 86 % / 20 % |
| **Sonnet 5** | **9 (7 en común)** | 11 (6 en común) | 85 % / 20 % |

## Cómo usarlo

- **Sustituto general:** Sonnet 5 (con la CLI de Claude, `--model claude-sonnet-5`). Es el que más se parece en todo a la vez y el que mejor sustituye a Haiku en el banco y en partidas de prueba.
- **Output (trampa de L1):** Qwen local es gratis, ilimitado y falla en lo mismo. Sirve para filtrar ideas de percepción de Output, por ejemplo leer dos veces en el mes de la evaluación, antes de gastar en DeepSeek.
- **Riesgo (crisis de confianza):** Luna.
- **Ninguno sirve para la nota.** Las ideas que pasen el filtro se confirman con DeepSeek.
- **Muestra pequeña** (20 bajadas de Output). Para usar Qwen en serio, repetirlo antes con las 403 preguntas (gratis, ~1,5 h).
- **Partidas completas con Qwen:** sólo como prueba de humo de un manual nuevo. El historial llega a 150.000–200.000 tokens por llamada, así que en el Mac serían horas por partida, y Qwen decide distinto de DeepSeek en riesgo y Network.
