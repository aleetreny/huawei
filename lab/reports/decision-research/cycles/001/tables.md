# Tablas reproducibles del ciclo

Exploración histórica. Ningún coeficiente ni diferencia identifica un efecto causal.

Terminales Claude elegibles: 204; trazas extraídas: 99; actor primario con calidad: 53.

## Estado temprano y resultado posterior

Población condicionada a seguir activo y tener una observación válida en ese mes.

| Mes | Promovido | n | Completan | Q media |
|---|---|---:|---:|---:|
| 6 | no | 27 | 10 | 35.90 |
| 6 | sí | 26 | 18 | 55.41 |
| 12 | no | 14 | 2 | 26.24 |
| 12 | sí | 38 | 26 | 53.07 |

## Predicción de Q fuera de muestra

Ridge con ajuste de penalización e imputación/escalado sólo dentro del entrenamiento. Error menor es mejor.

| Mes | Grupo reservado | Modelo | n | RMSE | RMSE media de entrenamiento | MAE |
|---|---|---|---:|---:|---:|---:|
| 6 | policy_id | state | 53 | 15.93 | 17.77 | 13.50 |
| 6 | policy_id | behaviour | 20 | insufficient_support | — | — |
| 6 | policy_id | state_and_behaviour | 20 | insufficient_support | — | — |
| 6 | policy_id | state_on_behaviour_cohort | 20 | insufficient_support | — | — |
| 6 | family | state | 53 | 16.04 | 18.46 | 13.95 |
| 6 | family | behaviour | 20 | insufficient_support | — | — |
| 6 | family | state_and_behaviour | 20 | insufficient_support | — | — |
| 6 | family | state_on_behaviour_cohort | 20 | insufficient_support | — | — |
| 12 | policy_id | state | 52 | 14.52 | 17.69 | 12.22 |
| 12 | policy_id | behaviour | 17 | insufficient_support | — | — |
| 12 | policy_id | state_and_behaviour | 17 | insufficient_support | — | — |
| 12 | policy_id | state_on_behaviour_cohort | 17 | insufficient_support | — | — |
| 12 | family | state | 52 | 14.94 | 18.37 | 12.37 |
| 12 | family | behaviour | 17 | insufficient_support | — | — |
| 12 | family | state_and_behaviour | 17 | insufficient_support | — | — |
| 12 | family | state_on_behaviour_cohort | 17 | insufficient_support | — | — |

## Puntos ausentes entre carreras completadas del actor primario

n = 28. Descomposición del score, no efectos de acciones.

| Dimensión | Puntos Q ausentes, media |
|---|---:|
| level | 16.18 |
| network | 3.39 |
| resilience | 0.21 |
| risk_control | 4.07 |
| skill | 3.30 |
| wealth | 13.28 |

Los meses son puntos de análisis retrospectivo y no reglas de calendario para las Skills. Predicción interna no equivale a validación prospectiva ni a transferencia a DeepSeek.
