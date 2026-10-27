# H-P1a: reloj de evaluación (P1, meses 1–5)

**Hipótesis (3 líneas).**
1. Qué cambia: un Skill añadido (`review-clock`) que enseña a calcular, con el calendario publicado del manual del juego y `current_month`, cuántos meses faltan para la evaluación; a reconocer un indicador en su techo; y a no elegir en el mes previo respuestas que puedan costar Network u Output si hay otra honesta (salvo con la salud baja).
2. Por qué lo pide la mecánica: la evaluación se aplica al empezar su mes, así que el último mes decide; en la línea base, casi todos los fallos eran puntos perdidos en los meses 4–5, y Haiku anotaba "review: far" en el mes 5.
3. Medida: % que asciende en la 1.ª evaluación (partidas de 6 meses).

**Diseño.** 2×2: con y sin el módulo sobre dos bases (f3-lean-v1 y bb-mechanics-v1), 25 partidas cortas por brazo, intercaladas, 27 oct 00:54–01:36 UTC, lote [`batches/p1-h1-clock.json`](batches/p1-h1-clock.json). Una primera versión del módulo (v1) se retiró antes de jugar: pedía conservar los indicadores "aunque cueste salud", y los dos bb-mechanics ya habían tenido 3 agotamientos en la línea base; la v2 pone la salud baja por delante.

## Resultado

| Brazo | Partidas | Ascienden en la 1.ª (IC 95 %) | Pérdidas en el mes 5 / en el 4 | Agotamientos |
|---|---:|---:|---:|---:|
| f3-lean-v1 | 24 | 9 = 38 % (21–57) | 16 / 3 | 0 |
| f3-lean + reloj (`f3-lean-clock-v2`) | 25 | 12 = 48 % (30–67) | 11 / 4 | 1 |
| bb-mechanics-v1 | 25 | 15 = 60 % (41–77) | 8 / 4 | 2 |
| bb-mechanics + reloj (`bb-mechanics-clock-v2`) | 25 | 11 = 44 % (27–63) | 17 / 1 | 0 |

- **El módulo se ejecuta**: las notas empiezan con la cuenta atrás y en el mes 5 dicen "review: next month".
- **Pero no cambia el resultado**: +10 puntos sobre f3-lean y −16 sobre bb-mechanics, signos opuestos dentro del ruido (error típico de cada diferencia ≈ 14 puntos). En conjunto, 23 de 50 (46 %) con reloj frente a 24 de 49 (49 %) sin él.
- Las pérdidas del mes 5 siguen ahí. Saber que la evaluación llega no basta: Haiku no sabe qué respuesta le va a costar el punto, y en el estudio de caja negra (H15) sólo un tercio de esas pérdidas tenía una alternativa segura.
- Ascienden todos los que llegan al umbral (47 de 47), como en la línea base.

## Decisión

**No gana.** Se repite una vez el brazo f3-lean + reloj en la ronda 2 (lote `p1-h2`), junto a dos ideas distintas: `cap-trade` (no comprar Dignidad que ya está al máximo a cambio de Network) y `log-check` (leer `check_latest_logs` para ver el efecto exacto de cada respuesta y el techo). Si la réplica tampoco destaca, se descarta.
