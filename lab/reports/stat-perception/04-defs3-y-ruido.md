# 04. defs3 y cuánto se mueve un etiquetado al repetirlo

**Conclusión: repetir el mismo etiquetado mueve la réplica 1,2 puntos, así que entre formas sueltas sólo cuentan diferencias de más de ~1,5; defs3 sola etiqueta peor (50,9), pero dentro de la votación da la mejor nota hasta ahora (vote5c, 55,1).**

27 oct, 16:15–16:40 UTC. Dos etiquetados más con Haiku, cuenta Pro de Leah, unos 0,2 USD a precio de lista. Medidos como en [01](01-siete-formas.md).

## Ruido de repetición

Se repitió `plain` con las mismas instrucciones ([tags-plain-rerun.json](tags-plain-rerun.json)):

| | plain | plain repetido |
|---|---:|---:|
| Señales iguales entre las dos pasadas | — | 87,8 % |
| Orden por pares (mitad reservada) | 0,807 | 0,798 |
| Nota en la réplica | 53,3 | 52,1 |

**Lectura.**
- Una pasada de Haiku tiene alrededor de un 12 % de señales que cambian al repetirla, y eso mueve la réplica algo más de un punto.
- Las conclusiones grandes de [01](01-siete-formas.md) se mantienen: etiquetas de Categorías 49,1, cualquier etiquetado completo 52–53, y votación 54–55.
- Las diferencias de menos de ~1,5 puntos entre formas sueltas son ruido.

## defs3: significados con sólo el lado del coste de Output

defs, pero con Output descrito como en la propuesta del manual: baja al desentenderse, esquivar, pasar el trabajo a otro, pedir menos carga, descansar en vez de trabajar o quemarse; una charla corta, una revisión o un poco de ayuda no lo cuestan. Sin la parte de "venderte" de defs2 ([03](03-errores-output.md)).

| Etiquetas | Orden por pares | Output: orden por pares | Bajadas de Output detectadas / acertadas | Réplica | Despidos | Crisis |
|---|---:|---:|---:|---:|---:|---:|
| defs | 0,793 | 0,72 | 0,62 / 0,41 | 53,2 | 213 | 73 |
| defs2 | 0,791 | 0,72 | 0,51 / 0,43 | 48,1 | 240 | 174 |
| defs3 | 0,804 | 0,76 | 0,49 / 0,49 | 50,9 | 250 | 115 |
| vote5b (con defs2) | 0,803 | 0,77 | 0,63 / 0,54 | 54,4 | 203 | 81 |
| **vote5c** (con defs3) | **0,809** | 0,77 | 0,62 / 0,53 | **55,1** | 203 | 76 |

**Lectura.**
- defs3 ordena mejor Output por pares, pero detecta menos bajadas.
- Sola queda 2,3 puntos por debajo de defs, más que el ruido de repetición, con más despidos y más crisis.
- En la votación, en cambio, aporta: vote5c es la mejor percepción medida, a 3 puntos de las etiquetas perfectas (58,1).
- **Ninguna redacción de Output mejora a un lector solo.** La mejora viene de juntar varias lecturas.

Datos: [replica-defs3.json](replica-defs3.json), [tags-defs3.json](tags-defs3.json), [tags-vote5c.json](tags-vote5c.json).
