# Biblioteca de enfoques de competiciones para Career Survival

Investigación del 26 de octubre de 2026. **17 casos de 14 competiciones/ediciones, 35 fuentes primarias seleccionadas y 36 fichas de experimentos**, incluidas 12 propuestas contraintuitivas. Las fichas son adaptaciones nuestras pendientes de prueba; no son 36 estrategias ganadoras demostradas ni una entrega de Skills.

El objetivo es que el orquestador tenga alternativas concretas cuando se atasque: mejorar memoria, replantear prioridades, simplificar instrucciones, cambiar la representación, reconstruir módulos relacionados o investigar un cuello de botella de ejecución. Esta carpeta acompaña al laboratorio que Claude construye en paralelo; no modifica su código, protocolo ni plan global.

## Qué leer

1. [Guía para elegir según el atasco](playbook.md): diagnóstico, prioridades, combinaciones y criterios de evaluación.
2. [Casos estudiados](cases.md): qué hicieron los equipos, qué falló y qué se puede transferir.
3. [36 fichas para probar](strategy-cards.md), con [JSON estructurado](strategy-cards.json) para consulta del orquestador.
4. [Fuentes y alcance de lectura](sources.md), [catálogo JSON](sources.json) y [casos JSON](cases.json).
5. [Instrucción breve para Claude](handoff-for-claude.md), sin activar automáticamente ninguna prueba.
6. [Auditoría de cobertura](completion-audit.md), [registro de búsqueda](search-audit.json) y [hallazgos](findings.md).

## Hallazgos que merecen atención

- **Interrupciones y memoria:** AutoAscend gana NetHack con un estado explícito y estrategias que pueden detenerse, atender una emergencia y continuar. Su victoria no supuso completar el juego. [Organizadores](https://nethackchallenge.com/report.html), [métodos](https://proceedings.mlr.press/v176/hambro22a/hambro22a.pdf).
- **Reconstrucciones grandes:** AHC058 y Flatland usan vecindarios que cambian partes relacionadas de un plan. Un cambio pequeño puede no cruzar una barrera entre estrategias. [ALE-Agent](https://sakana.ai/ahc058/), [Flatland](https://jiaoyangli.me/files/2021-ICAPS.pdf).
- **Representación antes que fuerza bruta:** Psyho simplifica a un grupo/trayectoria y luego optimiza; Unagi mejora una representación SAT intermedia. Probar otra abstracción puede rendir más que más variantes de texto. [Psyho](https://github.com/FakePsyho/cpcontests/blob/master/atcoder/awtf2025/approach.md), [Unagi](https://sakana.ai/icfp-2025/).
- **Dejar de rescatar:** Kore incorpora abandono y alternativas cuando una posición no se puede defender. La adaptación es poder reformular un objetivo agotado a partir del feedback, no darse por perdido automáticamente. [Campeón de Kore](https://www.kaggle.com/competitions/kore-2022/writeups/harm-buisman-1st-place-solution).
- **Restar reglas:** el relato ganador de RPS mejora al simplificar su selector. Conviene probar que la política larga realmente ayuda al actor. [Autor](https://github.com/thisisbowen/RPS-Kaggle-1st-Place-Solution).
- **Proteger capacidades anteriores:** el campeón de Lux S3 conserva profesor y oponentes antiguos. Para nosotros sugiere regresiones y diversidad de condiciones; no autoriza entrenamiento ni demuestra que mezclar actores sea fiel al modelo oficial. [Flat Neurons](https://www.kaggle.com/competitions/lux-ai-season-3/writeups/flat-neurons-1st-place-approach-by-flat-neurons).

## Qué significa “ganador” aquí

La biblioteca distingue ganador general, ganador de categoría, puesto etiquetado por la plataforma y puesto declarado por el autor. Hay dos contrastes de podio y un caso que ganó el componente algorítmico pero quedó tercero global. No se suman como 17 victorias generales independientes. El primer premio oficial de ICFP 2025 enumera **MOYOU y Unagi**.

La calidad de una solución ganadora no prueba que cada componente suyo causara la victoria. Los hechos publicados, las interpretaciones de los autores y nuestras propuestas de transferencia permanecen separados. No hay campeón histórico verificado del CareerSim exacto en el material revisado.

## Uso y límites

Escoger fichas por una necesidad observada y probarlas contra un comparador congelado. No cargar todo el catálogo al agente ni añadir todas las mejoras a la vez. El registro estructurado deja `launch_enabled: false`; la investigación no ha ejecutado estas variantes.

Los simuladores abiertos, semillas, replays completos, entrenamiento y acceso al código de otros concursos no son capacidades ni permisos establecidos del juego actual. Las adaptaciones usan procedimientos generales y feedback legítimo. La [regla vinculante actual](https://techarena-career-sim.readthedocs.io/en/latest/competition-rules.html) sigue gobernando cualquier ejecución.

La documentación de investigación es para el equipo. No incluirla íntegra en el ZIP oficial, cuyos entregables deben ser en inglés.
