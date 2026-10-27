# Experimento 5. Partidas g1: el manual combinado t3-instr frente a f3-lean

27 oct 2026, 11:48–12:30 UTC. Haiku, CLI 2.1.303, **entrega oficial** (actor `claude-cli:haiku#official`: el mensaje de sistema lleva sólo nombre y descripción del Skill y la instrucción del manifest; el cuerpo se lee con `skill_tool`). Partidas completas, intercaladas, 4 a la vez. Lote en [batches/g1-full.json](batches/g1-full.json).

## Resultado (parado a las 9 partidas de t3-instr)

| Manual | Terminadas / jugadas | Nota Q ± SE | Derrotas |
|---|---:|---:|---|
| f3-lean-v1 | 5/7 | 53,4 ± 6,3 | despido 1, crisis de confianza 1 |
| t3-instr | 1/7 | 32,3 ± 4,8 | despido 3, crisis de confianza 2, agotamiento 1 |

Diferencia −21 ± 8 puntos. Se cancelaron las partidas pendientes de t3-instr.

## Por qué: en el banco obedecía, en la partida empeoraba

1. **La regla se salía de su contexto.** La regla “antes de la evaluación, no cedas Output” y sus ejemplos (“el camino lento y minucioso cuesta Output”) se aplicaron en todos los meses. Las notas lo dicen: “boundary that protects my own delivery (Output)” ya en el mes 1. Haiku dejó de elegir las opciones que enseñan.
   - Skill al empezar el mes 5: f3-lean 8–9 en 7 de 9 partidas; t3-instr 2, 5, 6, 6, 7 en 5 de 8.
   - Sin la Skill de L1 no hay ascenso en el mes 6, y sin ascenso llega el despido del mes 24.
2. **Faltaba una regla de salud.** Una partida agotó la salud en el mes 3 eligiendo historias que la gastaban.
3. **El comentario de RR. HH. más leve (“some risk, not serious yet”) también disparaba Lay low**, que no hace crecer; el banco sólo medía la regla con riesgo 2 o más.

**Lección de método:** el banco medía cada regla sólo donde aplica. Hacen falta también situaciones donde **no** aplica, para ver si la regla se cuela. Se añade el bloque `general` (decisiones de historia al azar, fuera de las reglas) y la regla `low_health`.

## Siguiente

Manual `t6-scoped-instr`: lista completa sólo para el reparto trimestral (donde Haiku obedece y la regla no se cuela) y, en las historias, cuatro filtros con contexto explícito (mes previo a la evaluación, RR. HH. con riesgo acumulado, salud baja, poco dinero); fuera de ellos, el juicio del modelo. Lote `g2-full`, 30 + 30 frente a f3-lean.
