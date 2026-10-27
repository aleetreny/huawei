# Lo masticado: t13-final con la ficha de lectura y la regla de historias

**Conclusión.** Añadir a `t13-final` la ficha de lectura v3 y la regla de historias por orden (`t13-read-v1`) **arregla los detonantes** (acierto del 81 % al 91 %, pérdida −0,97 puntos por decisión) y quita la deriva lejos de Skill, pero **en el total de las historias empata con t13-final** (−0,02). Frente a no tener manual baja la pérdida en 0,47 puntos por decisión. Es la versión más segura de las probadas: la que elige las opciones de menos riesgo.

27 oct 2026, rama `alejandro/deepseek`. Manual en [lab/policies-src/deepseek/t13-read-v1/](../../policies-src/deepseek/t13-read-v1/); pasa `careerlab lint` sin errores (8 avisos de revisión; t13-final tiene 7).

## La variante

`t13-final` sin cambios en el reparto trimestral. La sección de historias (antes "elige lo que juzgues mejor") pasa a tener:
1. la cuenta atrás `Review in N` y, con N = 1, la referencia del mes de evaluación, igual que antes;
2. **una lectura por opción**: el signo que probablemente tiene en Skill, Network, Output, Health, Dignity, Wealth y el riesgo, con las pistas de la [categorización v3](categorizacion.md) (Skill sube al usar el propio juicio; Output baja cuando el tiempo o el mérito se van a otros; las señales de riesgo; "ante la duda, marca riesgo");
3. **la regla de historias** por orden: descarta lo arriesgado; si Health o Dignity están bajas, lo que las baja; con N = 1, lo que baja Skill, Network u Output; de lo que queda, lo que más sube los indicadores de crecimiento.

Todo son principios generales: no hay títulos, respuestas, meses concretos ni umbrales nuevos.

## Montaje

Banco oficial con DeepSeek (como en [obediencia.md](obediencia.md)), sólo las **320 historias** del conjunto: mes previo a la evaluación, detonantes, ruina temprana, salud baja, cierre y el bloque general. Las situaciones de reparto trimestral no se repitieron, porque esa parte del manual no cambia. Comparación emparejada con el control, con el control repetido y con t13-final en las mismas situaciones. Coste 0,45 USD.

## Resultados

| Regla | n | Sin manual | t13-final | **t13-read** | t13-read frente a t13-final |
|---|---:|---|---|---|---|
| Mes previo a la evaluación | 43 | 88 % · 1,05 | 88 % · 1,01 | 86 % · 1,28 | +0,26 (−0,44 a +1,09) |
| **Detonantes** | 43 | 88 % · 1,21 | 81 % · 2,16 | **91 % · 1,19** | **−0,97 (−2,37 a −0,02)** |
| Ruina temprana | 41 | 41 % · 1,14 | 49 % · 0,99 | 51 % · 0,95 | −0,04 (−0,14 a +0,04) |
| Salud baja | 17 | 71 % · 3,13 | 65 % · 0,69 | 76 % · 0,48 | −0,22 (−0,58 a +0,00) |
| Bloque general | 172 | 73 % · 1,39 | 76 % · 0,60 | 77 % · 0,78 | +0,18 (−0,14 a +0,65) |
| **Todas** | 320 | 73 % · 1,37 | 74 % · 0,92 | 77 % · 0,91 | −0,02 (−0,30 a +0,30) |

Cada celda: acierto · pérdida media en puntos de nota final por decisión. Frente a no tener manual, t13-read baja la pérdida en −0,47 (−0,95 a −0,08). Frente al control repetido, en el bloque general, −0,11 (−0,33 a +0,09).

**Huella en el bloque general** (139 historias de los meses 1–44):

| Brazo | Skill | Network | Output | Health | Dignity | Riesgo | Igual que el control |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sin manual | +0,88 | +0,71 | +0,08 | −0,11 | +0,99 | −0,14 | — |
| Sin manual, repetido | +0,88 | +0,73 | +0,08 | −0,06 | +0,99 | −0,19 | 91 % |
| t13-final | +0,70 | +0,76 | +0,22 | −0,12 | +0,96 | −0,14 | 87 % |
| **t13-read** | **+0,81** | +0,63 | +0,15 | −0,04 | +0,96 | **−0,22** | 88 % |

**Cómo lo usa DeepSeek.** Lee el Skill siempre. En 243 de las 320 notas dice qué filtro aplicó ("Filter 1 dropped option 3 (R+)"). La lectura por opción la hace en su razonamiento, y sólo la escribe con el formato pedido en 57 de 320 notas. Abre la referencia del mes de evaluación en la mitad de las historias.

**Coste en fichas por historia:**

| Brazo | Entrada | Salida | USD |
|---|---:|---:|---:|
| Sin manual | 13,5 mil | 1,4 mil | 0,0006 |
| t13-final | 26,0 mil | 2,8 mil | 0,0011 |
| t13-read | 30,6 mil | 3,8 mil | 0,0014 |

## Lectura

- El fallo de t13-final con DeepSeek estaba en los detonantes: la regla trimestral "protégete" se colaba en las historias y le hacía elegir arreglos en privado. El primer filtro, "descarta lo arriesgado", lo corrige.
- El resto de la regla no mejora la pérdida media de las historias frente a t13-final: el banco no confirma la ganancia que predice el bot del simulador (56 frente a 48,5). Hay dos razones posibles:
  - DeepSeek ya pondera los efectos por su cuenta cuando tiene un manual;
  - la pérdida por decisión pesa poco los riesgos que llevan a la crisis de confianza, que es donde la lectura más ayuda en el simulador.
- **Propuesta:** t13-read-v1 como candidato para el corte, con t13-final de reserva. Tiene la misma pérdida media, menos riesgo, sin el fallo de los detonantes y con menos sesgo contra Skill. Cuesta un 25 % más de fichas en las historias.
- **Lo que decidiría entre los dos** son partidas oficiales con DeepSeek, que exigen el visto bueno de Alejandro. Una partida completa costó 0,19 USD el 26 oct (16 millones de fichas en 24 meses); 48 meses de t13-read costarían unos 0,4–0,6 USD por partida. Una partida por manual es una anécdota. Con una desviación de unos 12 puntos por partida, 10 partidas por brazo sólo distinguen diferencias de unos 15 puntos, y para ver 5 harían falta unas 45 por brazo (unos 45 USD), más de lo que tiene la clave. Las partidas oficiales sirven para comprobar que el manual funciona de punta a punta con DeepSeek (que no se atasca, cuánto cuesta y si termina), no para elegir entre dos manuales parecidos.
