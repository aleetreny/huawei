# Carrera rápida: cómo funciona

Desde el 26 de octubre por la noche, la nube juega así (decisión de Alejandro: ir más rápido, no gastar partidas en manuales que no funcionan, poner las partidas donde hay valor y probar ideas valientes cuando nos atascamos). El estado en directo está en [lab/reports/carrera-rapida.md](../reports/carrera-rapida.md).

## La idea en cuatro frases

1. Hay **un campeón**: el mejor manual que tenemos, medido con muchas partidas.
2. Los manuales nuevos son **aspirantes** y suben una escalera: 2 partidas, 4, 8 y, si está muy reñido, 12.
3. Después de cada escalón, el sistema calcula **la probabilidad de que el aspirante sea mejor que el campeón**. Si es muy baja, se descarta y no juega más. Si con 8 o 12 partidas es alta, pasa a ser el nuevo campeón.
4. Siempre hay unos 4 aspirantes en juego. Cuando falta uno, **un diseñador automático** (un chat de Opus al máximo) lee las peores partidas del campeón, encuentra el fallo que más puntos cuesta y escribe una variante que lo arregla, como hizo Matteo a mano.

## Los números de la escalera

| Partidas jugadas | Sigue si la probabilidad de ser mejor es… | Si no |
|---:|---|---|
| 2 | al menos 5 % | descartado |
| 4 | al menos 15 % | descartado |
| 8 | 60 % o más: **nuevo campeón**; entre 35 % y 60 %: 4 partidas más | se queda a las puertas |
| 12 | 60 % o más: **nuevo campeón** | se queda a las puertas |

Simulado con las 153 partidas reales de la carrera: un manual malo se descarta en unas 2 partidas, uno flojo en unas 4. Uno claramente mejor que el campeón gana el título 94 veces de cada 100. Uno algo peor se cuela 13 de cada 100: es el precio de ir rápido.

## Tres tipos de aspirante

- **Variante:** arregla el fallo que más puntos le cuesta al campeón (sobre todo los despidos y las crisis de confianza).
- **Variante ambiciosa:** busca más ascensos y más dinero en las carreras que ya terminan. Nadie ha pasado nunca del nivel 5.
- **Idea valiente:** si 6 aspirantes seguidos no superan al campeón (o pasan 3 horas sin campeón nuevo), los dos siguientes manuales parten de una idea distinta. Por ejemplo: todo al primer ascenso, un manual de 150 palabras, una lista de comprobación en cada turno, o sólo sobrevivir.

Los manuales de Matteo, Leah o cualquiera del equipo entran como aspirantes en cuanto se juntan con `main`.

## Cómo se aprende de una vez para otra

- [lessons.md](lessons.md): lo demostrado (no se toca), lo que falló y dónde se pierden aún los puntos. Lo leen todos los diseñadores. La nube lo amplía tras cada campeón nuevo.
- [history.md](history.md): todos los manuales que han pasado por la escalera y qué les pasó, para no repetir ideas que ya fallaron.

## Lo que no puede hacer

El juego tiene mucho azar y no hay forma oficial de repetir la misma partida. Que una carrera ascienda en la primera ventana, que es lo que más decide si sobrevive, cambia de una partida a otra con el mismo manual. Por eso un resultado con 4 partidas puede ser suerte (al manual v3 de Matteo le pasó: 71 con 4 partidas, 51 con 8). La escalera exige 8 partidas antes de dar el título. Las mejoras grandes se ven rápido; las de pocos puntos, despacio.

## DeepSeek (la clave de 50 dólares)

No se usa para explorar, sólo en momentos concretos y desde el Mac de Alejandro, que es donde está la clave:
1. **Una vez:** 1 partida del campeón para comprobar que el manual funciona en el programa oficial y medir lo que cuesta de verdad.
2. **Antes de cada corte:** 2 partidas del campeón si ha cambiado desde la última comprobación.
3. Si DeepSeek pierde donde Haiku termina, se lee su partida y la lección va a `lessons.md`.

Se mide el gasto exacto antes y después de cada partida, y siempre quedan 15 dólares de reserva para el último corte.

Detalles técnicos: [lab/protocol/fastloop-v2.md](../protocol/fastloop-v2.md) y [scripts/fastloop/README.md](../../scripts/fastloop/README.md).
