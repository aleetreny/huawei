# Ideas nuevas que podemos probar

Cola de propuestas del equipo. Una idea aquí es una pregunta por comprobar, no una regla demostrada ni una autorización para lanzar partidas. Los experimentos de selección y confirmación siguen [el protocolo v1](../../lab/protocol/prereg-v1.md); la coordinación sigue [ESTADO](../../ESTADO.md).

## Ideas propuestas

| ID | Idea | Evidencia que la motiva | Prueba mínima útil | Estado |
|---|---|---|---|---|
| IDEA-01 | Recuperación explícita del estancamiento con seguridad conservada | En el análisis local de Haiku, al segundo corte completan 2/14 aún L1 frente a 26/38 promovidas; asociación, no efecto de promover | Revisar candidatas ya jugadas y comparar padre/variante con una sola regla, asignación aleatoria por partida e Y completo | Hipótesis; pendiente de diff y presupuesto del organizador |
| IDEA-02 | Proteger entrega y relaciones al elegir entre historias | 1.177/4.701 transiciones alineadas coinciden con pérdidas de Output/Network; pueden ser costes razonables | Auditar una muestra sin ver Q y, si hay pérdidas evitables, comparar un recordatorio general contra el padre | Pendiente de auditoría; no asumir que toda pérdida es un error |
| IDEA-03 | [Exploración aleatoria instrumentada](exploracion-aleatoria.md) | Los lotes aleatorios existentes guardan agregados o tienen poca exposición tardía; falta una tabla fiable de decisiones aleatorias | Recuperar logs propios del lote anterior; si no existen, diseñar un piloto con estado antes/después, opciones factibles y probabilidades conocidas | Propuesta metodológica; sin partidas lanzadas y con alcance reglamentario incierto para escala masiva |

IDEA-01/02 enlazan con [los insights](../careerlab/decision-research/insights.jsonl) y [la cola H-DR](../careerlab/decision-research/hypotheses.json), sin duplicar sus experimentos. Antes de escribir otra variante, revisar F7 delivery/promotion y F8 ya existentes: un cambio de nombre no convierte una prueba repetida en una idea nueva.

## De idea a resultado

Cada propuesta debe decir qué pregunta responde, qué datos usa, qué cambio general probaría, qué resultado la debilitaría y qué falta para ejecutarla. Al probarla, añadir enlace a política/actor/entorno, manifiesto, resultados completos y límites. Conservar estados «sin soporte», «inconclusa» y «refutada»; no borrar ideas que fallen.

Los resultados observacionales generan preguntas. Las reglas de un manual se prueban con partidas nuevas y deben seguir siendo aplicables cuando cambien el texto, el orden o los parámetros del juego. El material de investigación queda separado de los archivos de entrega.

## Relevo

- **Hecho:** sección navegable de ideas, dos propuestas derivadas de la exploración previa y ficha de exploración aleatoria con diseño, límites y auditoría de Matteo. PR nueva sobre main, separada de la PR #3 ya integrada.
- **Evidencia:** rama `Matteo` en `b6e1d63`, resumen e informe del lote aleatorio; fuentes oficiales enlazadas en la ficha. La evidencia local de estado/score viene de `lab/reports/decision-research/cycles/002`.
- **Pendiente:** localizar logs externos propios del lote de Matteo, si existen, y auditar una muestra. El resumen publicado por sí solo no contiene preguntas ni respuestas individuales. No se ha iniciado un collector ni una nueva corrida.
- **Retomar:** leer ESTADO y `research/ideas/exploracion-aleatoria.md`; verificar `git ls-tree -r --name-only origin/Matteo` y los artefactos que se aporten. No leer bases de datos ni paquetes internos del simulador para intentar recuperar decisiones.
- **Validación/publicación:** enlaces y suite requerida antes de commit/push; resultado exacto en `progress.md`. Línea propia en ESTADO y solicitud de integración por PR. No se cambia la cola de la nube ni el protocolo congelado.
