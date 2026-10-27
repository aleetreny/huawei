# Experimento 4. Contexto largo: ¿se olvida la regla cuando el historial crece?

27 oct 2026, 11:45–13:40 UTC. Haiku, entrega oficial. Antes de la situación, el agente juega las **18 decisiones anteriores** grabadas de la misma partida (el Skill se lee al principio y queda cada vez más atrás; unos 600.000–900.000 tokens leídos por situación). 30 situaciones por regla, de títulos no reservados, las mismas en todos los brazos.

| Regla | control | t2-veto (reglas en el cuerpo) | t3-ex (cuerpo, con prioridad y ejemplos) | t3-instr (t3-ex + reglas en la instrucción del manifest) |
|---|---:|---:|---:|---:|
| No ceder puntos antes de la evaluación | 47 | 57 | 57 | 57 |
| Skill en L4 | 7 | 67 | 70 | 67 |
| Comentario de RR. HH. | 33 | 77 | 77 | 80 |
| Detonantes | 87 | 80 | 87 | 87 |
| Cierre | 60 | 73 | 93 | 93 |

(Acierto %, n = 30; intervalos de unos ±15 puntos.)

**Lo que se aprende**
- Con 18 decisiones de historial la obediencia **no cae**: los números son los del contexto corto ([ronda-a.md](ronda-a.md)). En las partidas reales las notas siguen citando las reglas en el mes 40.
- **Poner las reglas también en la instrucción del manifest no añade nada medible** aquí (t3-ex frente a t3-instr). Como la instrucción va en todas las llamadas (y cuesta tokens en todas), sólo merece la pena si DeepSeek se olvida antes que Haiku. Queda como hipótesis para la puerta de DeepSeek.
- En el contexto corto Haiku lee el Skill en el 100 % de las situaciones, también tras el mensaje oficial de continuación.
