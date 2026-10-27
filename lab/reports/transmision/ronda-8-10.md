# Experimento 8. Rondas 8–10: mandar sólo donde se obedece, y una regla de historias tras una cuenta atrás

27 oct 2026, 12:55–13:35 UTC. Contexto corto, entrega oficial, Haiku. Mismas situaciones para todos los brazos.

## Brazos

| Brazo | Qué manda |
|---|---|
| `t8-quarter` | sólo el reparto trimestral, con prioridad: mes 48, salud baja, comentario de RR. HH., L4 o más, crecimiento; historias al juicio del modelo |
| `t9-quarter` | t8 con la línea de RR. HH. definida por exclusión (sólo los dos comentarios suaves dejan crecer) |
| `t10-countdown` | t9 más una sola regla de historias: escribir `Review in N` en cada nota de historia; con N = 1, abrir `reference/review-month.md` |

## Reparto trimestral (acierto %)

| Regla | n | control | f3-lean | t3-instr | t8 | t9 |
|---|---:|---:|---:|---:|---:|---:|
| Skill en L4 | 60 | 17 | 5 | 70 | **85** | 73 |
| Comentario de RR. HH. | 33 | 18 | 58 | 79 | 36 | **73** |
| Cierre | 60 | 62 | 68 | 87 | **93** | 92 |

t9 recupera RR. HH. (73 %) a cambio de algo de Skill en L4 (con el comentario suave, ahora el primer punto de energía va a Defuse). t8 fallaba en RR. HH. por una razón concreta: obedece con el comentario “con el ceño fruncido” (9 de 11), pero no con “inquieto, te las arreglas solo” (0 de 5): esa frase no habla de riesgo y Haiku no la reconoce como “peor”. t9 la define por exclusión.

## Huella en historias (bloque general, 114 decisiones comunes)

| Brazo | Igual que el control | Skill | Riesgo |
|---|---:|---:|---:|
| control repetido | 96 % | +0,82 | −0,19 |
| f3-lean | 93 % | +0,80 | −0,20 |
| t9-quarter | 94 % | +0,78 | −0,18 |
| t10-countdown | 78 % (91 % fuera de los meses previos a una evaluación) | +0,74 | −0,14 |

**La cuenta atrás funciona como interruptor.** En las 132 situaciones del bloque general, Haiku escribió el número correcto de meses todas las veces, abrió la referencia en los 42 meses previos a una evaluación y en ninguno más. Fuera de esos meses, sus historias coinciden con el control (91 %; control repetido 96 %). En t7, con la misma referencia pero sin cuenta atrás, la abría en la mitad de los meses.

**En su mes, la regla mejora la decisión:**

| Bloque general | n | Pérdida control | Pérdida control repetido | f3-lean | t9 | **t10** |
|---|---:|---:|---:|---:|---:|---:|
| Meses previos a una evaluación | 38 | 3,92 | 2,62 | 2,62 | 2,56 | **1,11** |
| Resto de meses | 85 | 0,60 | 0,65 | 0,42 | 0,41 | 0,51 |

(Pérdida media de nota final frente a la mejor opción, en puntos del simulador.)

En las situaciones de la regla `pre_review` (60 comunes), t10 acierta igual que el control (58 % frente a 57 %; pérdida 2,43 frente a 2,66), y `t2-veto` (todas las reglas en el cuerpo) más (72 %). El límite es la **percepción**: Haiku aplica la regla, pero lee mal qué opción cuesta Output (“un plan conjunto con el manager” lo toma por trabajo extra, cuando da Output).

## Conclusión

- Las reglas de reparto trimestral se transmiten sin efectos secundarios en las historias (t8/t9: 94 % igual que el control).
- Una regla de historias se puede aislar con un **interruptor que el modelo calcula y escribe** (la cuenta atrás) y el detalle en un archivo `reference/` que sólo se abre cuando toca. Avisar “sólo en el mes previo” no basta (t6, t7).
- Siguiente: partidas `g5-full` con f3-lean, t9 y t10 intercalados (35 por brazo) y validación final en ≥ 200 situaciones por regla.
