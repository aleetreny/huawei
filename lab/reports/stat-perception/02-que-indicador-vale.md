# 02. Qué indicador vale la pena percibir bien

**Conclusión: percibir bien Output vale +2,5 puntos en la réplica; percibir bien Skill resta 2,1.**

27 oct, 15:40 UTC. Sin cuota: sólo la réplica de la línea Motor, con 1.000 partidas por brazo y las mismas semillas.

## Método

Se toma vote5 (la votación de [01](01-siete-formas.md)) y se sustituye **un solo indicador** por su señal real en todas las respuestas. El resto del bot es igual que en 01.

## Resultado ([replica-one-perfect.json](replica-one-perfect.json))

| Indicador hecho perfecto | Nota | Frente a vote5 | Despidos | Crisis de confianza |
|---|---:|---:|---:|---:|
| ninguno (vote5) | 54,2 | — | 207 | 74 |
| **Output** | **56,7** | **+2,5** | 149 | 111 |
| Dignity | 54,5 | +0,3 | 212 | 77 |
| Network | 53,9 | −0,3 | 165 | 167 |
| Health | 53,7 | −0,5 | 221 | 98 |
| Skill | 52,1 | **−2,1** | 237 | 105 |
| los cinco | 55,1 | +0,9 | 112 | 249 |

## Lectura

- **Output es donde está la nota:**
  - con Output bien percibido hay menos despidos, porque el bot llega con Output al techo a la evaluación;
  - coincide con Transmisión (Haiku obedece "no bajes Output" pero no sabe qué opción lo cuesta) y con la regla del ascenso (HALLAZGOS A2).
- **Skill bien percibido empeora:** el bot persigue Skill, que se estanca en los niveles bajos, y pierde evaluaciones. Mejorar la detección de Skill, como proponía la línea Categorías, no compensa.
- Con los cinco perfectos suben las crisis de confianza, porque el bot coge opciones de mucho rendimiento y más riesgo mientras sigue juzgando el riesgo por la categoría. Percibir bien los indicadores no sustituye a percibir el riesgo.
