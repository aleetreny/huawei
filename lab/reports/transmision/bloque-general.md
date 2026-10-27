# Experimento 7. El bloque general: las reglas de historias se cuelan en el resto de decisiones

27 oct 2026, 12:35–12:55 UTC. Contexto corto, entrega oficial, Haiku.

## Por qué hacía falta

El banco por reglas mide cada regla sólo donde aplica, y la nota de cada opción supone que después se juega bien (el planificador). Así no se ve un sesgo que se repite en todas las decisiones: perder un poco de Skill en cada historia no cuesta casi nada en una situación, pero mucho en una partida. Lo vimos en las partidas g1 ([partidas-g1.md](partidas-g1.md)).

**El bloque general:** 139 decisiones de historia al azar de los meses 1–44 (las mismas partidas grabadas, títulos con reserva del 30 %), decisivas (2 puntos o más entre la mejor y la peor opción). Para cada brazo se mide la **huella**: el efecto medio anunciado de la opción elegida, y el % de decisiones iguales que el control.

## Resultados (138 decisiones comunes)

| Brazo | Skill | Network | Output | Health | Dignity | Riesgo oculto | Igual que el control |
|---|---:|---:|---:|---:|---:|---:|---:|
| control | +0,80 | +0,54 | +0,11 | +0,01 | +1,09 | −0,18 | 100 % |
| control repetido | +0,80 | +0,61 | +0,10 | +0,01 | +1,10 | −0,20 | **96 %** |
| f3-lean-v1 | +0,78 | +0,65 | +0,11 | −0,02 | +1,04 | −0,20 | 93 % |
| t3-instr (manual de g1) | +0,67 | +0,60 | +0,22 | −0,09 | +1,01 | −0,12 | 80 % |
| t6-scoped-instr (reglas de historia acotadas) | +0,75 | +0,74 | +0,15 | −0,09 | +0,97 | −0,11 | 81 % |
| t7-ref-instr (filtros en `reference/`, abiertos sólo si aplican) | +0,67 | +0,61 | +0,17 | −0,08 | +0,93 | **+0,04** | 78 % |

Acierto según el simulador en el mismo bloque: control 74 %, f3-lean 78 %, t3-instr 73 %, t6 79 %. Con una decisión cada vez, el simulador no castiga el sesgo; la huella sí lo enseña.

## Lo que se aprende

1. **Haiku es estable:** repetido, el control elige lo mismo el 96 % de las veces. Una diferencia del 80 % es un cambio de comportamiento, no ruido.
2. **Cualquier regla de historias cambia una de cada cinco historias**, aunque la regla no aplique. Las notas dicen “judgement: no filter applies”, pero la elección cambia: el texto de la regla (“ir contra alguien cuesta Network”, “el trabajo extra cuesta Output”) tiñe el juicio. Las elecciones pierden Skill y ganan riesgo.
3. **Esconder la regla en `reference/` no lo evita.** Haiku abre `reference/review-month.md` en 65 de 139 historias, aunque el mes previo a una evaluación sólo es 1 de cada 6: no reconoce bien ese mes (mes 28 o 40 tomados por “mes previo”). Y dentro del mes correcto, la regla “no bajes Output” le lleva a elegir opciones de riesgo (“seguir con el lanzamiento y apostar”).
4. **f3-lean apenas toca las historias** (93 %) y por eso no las estropea; eso explica parte de su ventaja en partidas.

## Consecuencia

Las reglas de reparto trimestral se transmiten bien (60–90 % de obediencia) y no tocan las historias. Las de historias se transmiten mal y con efectos secundarios. El siguiente manual, `t8-quarter`, sólo manda en el reparto trimestral y deja las historias al juicio del modelo.
