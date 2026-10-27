# Cómo sacar la mejor nota del hackathon: análisis desde cero

Escrito el 26 oct 2026 a las 22:30 UTC por el chat `alejandro/carrera-rapida`, a petición de Alejandro: pensar desde los principios básicos cuál es la forma óptima de trabajar hasta el 1 de noviembre, con nuestros datos reales. No implementa nada; propone.

## 1. Qué se puntúa de verdad

Según las reglas oficiales (`local-runs/official-runner/docs/competition-rules.rst`):

- **Nota de una versión** = 80 % juego + 10 % calidad de los SKILL.md + 10 % tokens.
  - **Juego:** la media de 3 partidas oficiales de DeepSeek.
  - **Calidad de los SKILL.md:** cada Skill se puntúa de 0 a 100 como instrucciones para el agente, con una rúbrica publicada: que la descripción diga qué hace y cuándo usarla; pasos ejecutables con prioridades y criterios, también cerca de los límites; coherencia con las reglas publicadas; mirada a los 48 meses; y que siga sirviendo si cambian las palabras o el orden de los eventos.
  - **Tokens:** 100 puntos con 500.000 tokens por mes o menos y 0 con 3 millones o más. Una partida que no termina tiene esta parte limitada a 50.
- **Nota de la fase 1** = la **mejor** de las versiones puntuadas. Hay 3 cortes (27 oct, 30 oct y 1 nov) y en cada uno se puntúa la última versión nueva que hayamos subido. Como máximo, **3 versiones**, y una versión idéntica a otra ya puntuada no se vuelve a evaluar.
- **Fase 2**, sólo para los 10 primeros: nota final = 70 % fase 1 + 30 % jurado. El jurado mira el vídeo, `design/skills_design.md`, `design/decision_report.md` y los propios Skills. **El vídeo es obligatorio desde la primera entrega final**: sin él, la entrega no vale.
- **Las partidas oficiales usan otro conjunto de eventos, cerrado**, y las reglas avisan de que los parámetros pueden cambiar. Lo que medimos en local es una aproximación doble: Haiku en lugar de DeepSeek, y los eventos de desarrollo en lugar de los de la evaluación.

## 2. Qué dicen nuestros datos: por qué no avanzamos

Datos: 274 partidas de Haiku en la carrera (registro de la nube a las 21:39 UTC), más 32 de Matteo, 11 de Leah, 18 de Opus y 1 de DeepSeek.

1. **Entre manuales razonables, el manual apenas cambia la nota.** En los 39 manuales con 4 o más partidas, cada partida varía unos 19 puntos por azar. La diferencia real entre manuales es de unos 2,5 puntos: el manual explica en torno al 2 % de lo que varía la nota. Sólo destacan unos pocos manuales claramente rotos, como F2 (0 de 5 terminadas) o los que no limpian el riesgo.
2. **Por eso los "líderes" se desinflan:**
   - F3: de 61 a 49;
   - la v3 de Matteo: de 71 a 51 (y 55 en la carrera);
   - f1-status-line: de 64,6 a 52,7;
   - F1: de 56,1 a 49,3 en cuanto jugó 6 partidas más.

   Ahora mismo los mejores están todos entre 53 y 56 con 12–18 partidas, y no se distinguen entre sí.
3. **La carrera rápida da vueltas sobre el mismo nivel.** En 2 horas jugó unas 100 partidas, descartó bien los manuales malos y coronó dos campeones (f3-balance-recombined y una variante automática). Los dos cambios son ruido: sus medias son iguales o peores que las del campeón que sustituyen. Además, mi propio modelo tiene un fallo: da a todas las partidas perdidas la misma nota (28,6), aunque las que caen al final valen unos 48. Por eso puede coronar a un manual con peor media real.
4. **La causa de fondo está en la mecánica del juego:**
   - El crecimiento sale sobre todo de las decisiones de los eventos (en la v1 de Matteo, unas 9 de cada 10 subidas de habilidad venían de ahí).
   - Haiku elige la misma opción en cada evento sea cual sea el manual (diagnósticos de la nube, tandas 3 y 5).
   - Nuestros manuales mandan sobre todo en el reparto trimestral, que es la parte pequeña del juego.
5. **Lo que decide cada partida pasa en el primer año.**

   | Situación en el mes 12 | Partidas | Nota media | Terminaron |
   |---|---:|---:|---:|
   | Ascendió en la primera evaluación | 14 | 57 | 12 |
   | Ascendió en la segunda | 11 | 47 | 7 |
   | Seguía sin ascender | 13 | 22 | 0 |

   Eso explica unos dos tercios de lo que varía la nota final. Y con el mismo manual, ese ascenso sale o no según la partida: la v3 ascendió en la primera evaluación 4 de 4 veces y después 0 de 4.
6. **Medimos con el instrumento equivocado.** Haiku y Opus ya ordenaban distinto algunas familias de manuales (correlación de 0,2). DeepSeek ha jugado 1 partida: se quedó en el nivel 1, sacó tres C seguidas y fue despedido en el mes 24, sin limpiar el riesgo ni una vez. Una partida no dice si DeepSeek juega peor; dice que no lo sabemos.

**En una frase:** llevamos dos días optimizando con mucho cuidado algo que (a) apenas cambia entre manuales razonables, (b) depende sobre todo de una parte del juego que nuestros manuales no tocan y (c) se mide con un jugador y unos eventos distintos de los oficiales.

## 3. Cuánto vale cada palanca

Cálculo aproximado. La dispersión de la nota de una versión (media de 3 partidas) es de unos 9 puntos para nuestros mejores manuales (unos 16 por partida, dividido entre la raíz de 3).

| Palanca | Ganancia esperada en la nota de la fase 1 | Seguridad | Coste |
|---|---:|---|---|
| **Subir una versión distinta en cada uno de los 3 cortes** (cuenta la mejor) | **unos +6** frente a una sola versión (+4 con dos) | alta: es estadística pura | casi nulo, pero cada entrega debe ser válida (vídeo y documentos) |
| **Escribir los SKILL.md para la rúbrica de calidad** | +1,5 a +2,5 (hoy un evaluador de prueba les da 64–78; con la rúbrica, 90 o más es realista) | alta | bajo: reescribir y comprobar con unas pocas partidas que no empeoran el juego |
| **Que DeepSeek termine más partidas** | cada 10 puntos más de partidas terminadas ≈ +3; el tamaño real es desconocido | baja: sólo se sabe jugando con DeepSeek | 0,2–0,6 USD y 20–40 minutos por partida |
| Menos tokens por mes (notas cortas, no releer el manual del juego ni los registros) | +0,5 a +1 | media | bajo |
| Seguir buscando manuales con Haiku como hasta ahora | +0,5 a +1 realista (el mejor posible estaría a unos +4, pero no se puede reconocer: harían falta unas 180 partidas por manual para ver 5 puntos) | baja | alto: cuota de Claude |
| **Vídeo y documentos de diseño**, si entramos en los 10 primeros | el 30 % de la nota final | alta si se trabajan bien | trabajo humano; el vídeo hace falta **mañana** |

Notas:
- Para el juego, la variación no es mala: como cuenta la mejor de 3 versiones, no hay que tener miedo al riesgo. Aun así, lo que más sube la nota es terminar más partidas, porque eso sube la media.
- Para la parte de tokens, lo que más pesa es terminar la partida: una partida que no termina se queda en 50.

## 4. Qué estructura conviene

- **Un consejo de Claudes que debata o haga torneos: no.** Los estudios recientes encuentran que los debates entre modelos no superan a métodos simples aunque gasten más. Además, ordenar opiniones no arregla un problema de medida: elegir entre manuales indistinguibles sigue siendo una lotería, y cada debate de Opus sale de la misma cuota que las partidas.
- **Diseñadores automáticos que escriben variantes pequeñas: parar.** Una variante pequeña produce un efecto de pocos puntos, que no se puede detectar. Los dos campeones que han coronado esta noche son ruido, y cada diseño gasta cuota de Opus.
- **Un solo chat director (Opus) con pocas hipótesis grandes: sí, pero con un matiz.** Probar 8 estrategias parecidas con Haiku no las separaría. El chat debe:
  1. probar pocas ideas muy distintas que puedan tener efectos grandes en la parte del juego que importa, con suficientes partidas cada una (unas 20–30 para ver una diferencia de unos 15 puntos);
  2. encargarse de lo que la nota recompensa con seguridad: tres versiones, la rúbrica de calidad y los documentos;
  3. usar subagentes sólo para tareas acotadas (puntuar con la rúbrica, analizar una partida, escribir una versión).
- **La nube, como motor de partidas a demanda**, no como generadora de ideas. Juega las pruebas que pida el director y comprueba que cada versión que vayamos a subir no tiene fallos graves.
- **DeepSeek:** las partidas acordadas antes de cada corte. La compra más rentable sería una medición pequeña con DeepSeek de los 2–3 candidatos, unas 8–10 partidas por unos 4 USD; la decisión es de Alejandro.

### Las ideas grandes que merece la pena probar

1. **Un procedimiento explícito para los eventos.** Ante cada evento, evaluar cada opción según lo que aporta a habilidad, red de contactos y resultados, frente a su coste en salud, dignidad, dinero y riesgo, y elegir siguiendo criterios claros. Es la única forma de que el manual toque la parte que decide la partida. Hay que comprobar primero si de verdad cambia las elecciones del jugador: se ve comparando qué opción elige en los mismos eventos, sin esperar al resultado de la partida.
2. **Un primer año al estilo de los bots que llegaron al nivel 6**: proyecto clave cada trimestre, un punto de salud cada trimestre y limpiar el riesgo en cuanto haya avisos. Los cuatro bots que llegaron al nivel 6 ascendieron en cada una de sus tres primeras evaluaciones.
3. **Una versión escrita para DeepSeek**: corta, con una lista de comprobación por turno y sin ambigüedades. Además puntúa bien en la rúbrica y gasta menos tokens.

## 5. Plan hasta el 1 de noviembre

| Cuándo | Qué |
|---|---|
| 27 oct (corte 1, 24:00 UK) | **Versión 1**: el mejor manual general reescrito para la rúbrica (las mismas reglas, mejor escritas), con una prueba rápida en Haiku de que no empeora. **Vídeo y documentos de diseño listos** (tarea del equipo). Partidas de DeepSeek de antes del corte, según lo acordado. |
| 28–30 oct (corte 2) | Probar las 2–3 ideas grandes (20–30 partidas de Haiku cada una, mirando primero si cambian las decisiones en los eventos). **Versión 2**: la mejor de esas ideas o, si ninguna destaca, otra versión distinta del mejor manual. |
| 31 oct–1 nov (corte 3) | **Versión 3**: la mejor candidata con lo aprendido, pulida para la rúbrica, y los documentos actualizados. |

## 6. Decisiones para Alejandro

1. Pasar a este modo de trabajo: parar los diseñadores automáticos de la nube y dejarla como motor de partidas a demanda, con un chat director.
2. Si se autoriza una medición pequeña con DeepSeek (unas 8–10 partidas, unos 4 USD) antes del corte 2.
3. Quién graba el vídeo para mañana.

## Relevo

1. **Hecho:**
   - análisis de las reglas oficiales y de 274 partidas de la carrera;
   - descomposición del azar frente al efecto del manual;
   - lectura de la partida de DeepSeek;
   - puntuación de prueba de 5 manuales con la rúbrica oficial (Sonnet como evaluador, en la carpeta temporal del chat; no es la nota oficial);
   - este documento.

   No se ha cambiado ningún código ni la carrera.
2. **Datos:** registro `lab/registry/*.jsonl` en `origin/cloud-lab-run` (3b729ef, 21:39 UTC); `lab/fastloop/state.json`; `lab/registry-origins/deepseek/`.
3. **A medias:** nada.
4. **Siguiente paso:** según lo que decida Alejandro en la sección 6.
5. **ESTADO.md:** sin cambios hasta que haya decisión.
