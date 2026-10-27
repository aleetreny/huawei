# 03. Por qué Haiku se equivoca con Output, y una corrección que sale cara

**Conclusión: Haiku confunde Output con tiempo gastado, y corregirlo diciendo "venderte sube Output" baja la réplica de 53,2 a 48,1 porque arrastra respuestas arriesgadas.**

27 oct, 15:45–15:55 UTC. Errores mirados sólo en la mitad de diseño. Una forma nueva de etiquetado (defs2), medida como en [01](01-siete-formas.md).

## Errores de Output (vote5, mitad de diseño, 443 respuestas)

| Error | Respuestas |
|---|---:|
| Output sube y no se detecta | 51 |
| Se marca que Output baja y no baja | 46 |
| Output baja y no se detecta | 24 |
| Se marca que Output sube y no sube | 20 |

**El patrón.**
- **Haiku trata como coste de Output cualquier uso del tiempo:** una charla corta, una revisión o una lista de comprobación.
- **En el juego, Output sigue al impulso.**
  - Sube cuando empujas tu trabajo, tus resultados o tu posición: entregar, aceptar más trabajo, un plan de recuperación con fechas, seguir centrada en el trabajo, venderte.
  - Baja cuando te desentiendes: callar, tragar, esquivar la responsabilidad, pasar tu trabajo a otro, pedir menos carga, descansar en vez de trabajar o quemarte.

## La corrección (defs2)

defs con Output redefinido como "impulso visible: empuja tu trabajo o tu posición, incluso vendiéndote; desentenderte lo cuesta; una charla corta, una revisión o un poco de ayuda no lo cuestan".

| | defs | defs2 |
|---|---:|---:|
| Subidas de Output detectadas (mitad reservada) | 0,52 | **0,66** |
| Bajadas de Output detectadas | 0,62 | 0,51 |
| Nota en la réplica | **53,2** | 48,1 |
| Crisis de confianza (de 1.000) | **73** | 174 |

Detecta más subidas, pero la nota cae y las crisis de confianza se multiplican por más de dos. "Incluso vendiéndote" hace que Haiku vea como ganancia respuestas de autopromoción, que suelen llevar riesgo oculto, y el bot las elige.

## Lección para el manual

- **No presentar nunca una conducta arriesgada como forma de ganar un indicador**, aunque sea verdad en el juego.
- **De Output, describir sólo el lado del coste:** desentenderse, esquivar, pasar el trabajo a otro, pedir menos carga o quemarse lo bajan; una charla o una revisión no.

Esa es la variante `defs3`, pendiente de medir.
