# Petición a Alejandro: observed-growth-v10 contra tu mejor manual, en el mismo lote

De Matteo, 27 oct 2026. Rama `matteo/confronto-v10` (incluye las fuentes v9–v12 y sus informes).

## Por qué

Con pilotos separados no podemos decir cuál es mejor:

| Manual | Partidas | Q media | Terminadas | Dónde |
|---|---:|---:|---:|---|
| observed-growth-v10 (Matteo) | 8 | 59,6 | 7 de 8 | piloto Matteo, actor `017798b931bc18f8` (CLI 2.1.310) |
| observed-growth-v7 (Matteo) | 9 | 57,6 | 7 de 9 | ídem |
| f3-lean-v1 | 37 | 50,4 | — | T18, secciones |
| periodos-v1 | 37 | 51,5 | — | T18, secciones |
| targeted-1026-201334 (campeón) | 13 | 51,6 | 10 de 13 | carrera rápida |

La v10 parece unos 8 puntos por encima, pero no nos fiamos:
- Con unos 19 puntos de ruido por partida, 8 partidas dan ±6–7 de error.
- Es la mejor de muchas versiones, así que lo normal es que baje: la v3 pasó de 71 a 51.
- Cambian el actor (CLI 2.1.310 frente a 2.1.303), el lote y la hora.
- Tu prueba en el mismo lote del primer semestre dio la v7 con un 40 % de ascensos y f3-lean con un 47 %, sin diferencia.

Si hay ventaja, la v10 la buscaría en L3–L4. Cuando Network y Output ya están al tope, desvía la energía a Skill (rotación y Skill learning), y por eso hacen falta partidas **completas**.

## Qué pedimos

Un cara a cara en el mismo lote, con el mismo actor y las partidas **alternadas** (A, B, A, B…) para que la hora y la cuota afecten igual a los dos brazos:

- **A:** `lab/policies-src/matteo-feedback-growth/observed-growth-v10` (lint OK).
- **B:** tu mejor manual actual: f3-lean-v1, periodos-v1 o el que prefieras.
- **Tamaño:** 30 partidas completas por brazo como mínimo; con 40, mejor. Con unos 19 de ruido, 30 por brazo detectan unos 10 puntos y 40 unos 8–9. Diferencias de 2–3 puntos no se verán con ningún tamaño razonable, y también está bien saberlo.
- **Regla fijada antes de jugar:**
  - Se compara la diferencia de Q media con su error típico.
  - Si P(v10 mejor) ≥ 0,80, la v10 entra como candidata a un corte.
  - Si ≤ 0,20, la v10 se descarta.
  - Entre medias, empate: se elige por tokens y calidad del texto.
- **Métricas secundarias** (sin decidir con ellas):
  - terminadas;
  - ascenso en la primera evaluación;
  - meses en L4;
  - Skill por mes en L4;
  - nivel final.
- **Ahorro:** si quieres, corta las dos ramas con la misma regla. Por ejemplo, una partida que sigue en L1 después de la evaluación del mes 24 cuenta como despedida. Debe valer igual para A y B.

## Por qué tú y no Matteo

La cuota de Matteo va por un 35 % de la semana y no da para 60–80 partidas. Tú ya tienes el montaje del mismo lote con partidas alternadas (T18, `alejandro/lab-secciones`) y la cola. Si no compensa por cuota, una versión barata es jugar sólo la v10 (30 partidas) en tu montaje y compararla con tus 37 de f3-lean. Es más débil, porque cambia la hora, pero cuesta la mitad.

## Relevo

1. **Hecho:** esta petición. No se ha jugado ninguna partida para ella.
2. **Datos de la v10:** `lab/reports/matteo-observed-growth-v10-v12.md`. Las partidas están en `lab/registry-origins/matteo/`.
3. **Siguiente:** Alejandro decide si lo juega, con qué B y cuántas partidas. El resultado va en `lab/reports/confronto-v10.md`.
