# H-P2a: `climb`, construir con el reparto el indicador que bloquea (P2, meses 6–17)

**Hipótesis (3 líneas).**
1. Qué cambia: un Skill que, tras cada ascenso, manda la energía trimestral y la acción principal a Network y Output (y a la Skill cuando aquellos se estancan).
2. Por qué lo pide la mecánica: tras cada ascenso la barra sube y las historias suben los tres indicadores de forma desigual; en las partidas completas de referencia, L3 quedaba bloqueado por el Output hasta 18 meses con Skill y Network clavadas.
3. Medida: nivel en el mes 18 (partidas cortadas al llegar al mes 18).

**Diseño.** 25 partidas por brazo, intercaladas, 27 oct 01:38–05:08 UTC, lote [`batches/p2-h1-climb.json`](batches/p2-h1-climb.json).

## Resultado

| Brazo | Partidas | Ascienden en la 1.ª | Ascienden en la 2.ª (mes 12) | Ascienden en la 3.ª (mes 18) | Nivel en el mes 18 |
|---|---:|---:|---:|---:|---:|
| f3-lean-v1 | 24 | 11 | 13 | 7 | 2,29 |
| f3-lean + climb (`f3-lean-climb-v1`) | 24 | 11 | 9 | 10 | 2,25 |

- **Sin efecto** en el nivel del mes 18. El P2 sigue dominado por el P1: a los 12 meses, la mitad de las partidas de ambos brazos sigue en L1, y ahí `climb` no actúa.
- Entre las que llegan a L3, el Output y la Network siguen siendo lo que falta (columna "short" de `scripts/secciones/reviews.py`).
- En la prueba final con partidas completas, `climb` v2 (más decisivo: "alimenta el cuello de botella") sí se ejecuta (etiqueta `blocker:` en las notas, informes y mantenimiento de red dirigidos), y las estancias en L2 son más cortas (7,6 frente a 9,9 meses), pero no las de L3 ni L4 (ver resumen).

## Decisión

**Descartada** como palanca medible del P2 con 24 partidas por brazo. El cuello de botella del P2 está antes: en salir de L1.
