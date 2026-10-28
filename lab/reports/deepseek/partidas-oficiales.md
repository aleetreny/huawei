# Partidas oficiales de t13-read-v1 con DeepSeek

**Conclusión.** DeepSeek juega `t13-read-v1` de punta a punta por la vía oficial y aplica la regla de historias en cada nota, pero **las dos partidas acaban eliminadas por el riesgo oculto**:
- partida 1: despido en el mes 24 en L1, nota 14,98;
- partida 2: crisis de confianza en el mes 30 en L4, nota 42,51.

En las dos, el riesgo lo cargan **opciones que parecen constructivas** y que DeepSeek lee como prudentes: tratar algo en un 1:1 privado, una denuncia anónima, un cambio por fases, revisar sólo lo esencial para ganar tiempo. En la primera, además, la regla trimestral "tras una evaluación floja, céntrate en el indicador que falta" se coló en las historias. Coste: 0,54 USD las dos (0,23 y 0,31). Dos partidas son una anécdota, pero señalan el mismo punto débil que el banco: la percepción del riesgo.

27 oct 2026, aprobado por Alejandro en el chat ("juega 2 partidas oficiales de t13-read-v1 con DeepSeek y apunta el coste"). Programa oficial (`career_sim_runner` 00b084a8, JiuwenSwarm 0.2.4b3), juego de desarrollo, clave de la competición; `careerlab.target` con tope de 1,2 USD por partida y 15 USD de reserva. Registro de origen `deepseek`: política `f74ba2d9e708c550`. Datos en `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-f74ba2d9-*` (fuera de Git).

## Partida 1

| Medida | Valor |
|---|---|
| Resultado | eliminado en el mes 24, despido por capacidad (segunda evaluación floja) |
| Nota (`quantitative_score`) | 14,98 |
| Nivel final | L1 |
| Coste exacto | 0,230 USD (18,15 millones de fichas de entrada y 81 mil de salida) |
| Tiempo | unos 25 minutos |

**Qué pasó, por evaluaciones:**
- **Mes 6:** Skill en 7 cuando hacía falta 8 (Network y Output, ya en 3): nota C, sin ascenso.
- **Meses 7–9:** Skill, Network y Output llegan al umbral de L1 (9/3/3) y el comentario de RR. HH. está tranquilo.
- **Meses 9–11:** tras la C, aplicó en las historias la regla trimestral 4 de t13-final ("después de una evaluación floja, gasta en el indicador que falta"). Eligió opciones que ahorraban tiempo para Output:
  - mantener un proceso manual en vez de invertir en automatizarlo (riesgo +2);
  - revisar sólo lo esencial y dejar el resto al autor (+2);
  - la vía rápida en una decisión técnica (+1).

  El comentario de RR. HH. pasó de tranquilo a "frowning" y luego a "angry", y **el riesgo explotó en el mes 11**, justo antes de la evaluación: nota C, sin ascenso.
- **Meses 18 y 24:** en L1, quien no ha ascendido para el mes 12 recibe D por tiempo en el nivel (M11). Dos evaluaciones flojas: despido.

**Por qué no lo paró el filtro "descarta lo arriesgado":**
- La opción del proceso manual la marcaba como arriesgada en la prueba de etiquetado (dos pasadas de dos), pero en la partida su nota sólo cita la regla 4 ("focus on Output") y no menciona el riesgo. **La regla trimestral pesó más que el filtro.**
- La revisión ligera la lee como prudente también en el etiquetado: es un fallo de percepción. La ficha de lectura ya habla de "arreglos parciales", pero no de "hacer menos de lo debido para ganar tiempo".
- En la decisión técnica las dos opciones eran arriesgadas.

**Lo que sí funcionó:** DeepSeek leyó el Skill, escribió `Review in N` y el filtro aplicado en cada nota, y rechazó siempre las opciones de ocultar, mentir o cotillear.

## Partida 2

| Medida | Valor |
|---|---|
| Resultado | eliminado en el mes 30: crisis de confianza (segunda explosión del riesgo) |
| Nota (`quantitative_score`) | 42,51 (parcial de la competición: 29,76) |
| Nivel final | L4 |
| Coste exacto | 0,310 USD (26,99 millones de fichas de entrada y 109 mil de salida) |
| Tiempo | unos 34 minutos |

**Qué pasó:**
- **Crecimiento muy bueno.** Ascendió en las tres primeras evaluaciones: mes 6 (L2, nota C), 12 (L3, B) y 18 (L4, B). En el mes 24 sacó B sin ascender. En el mes 30 tenía Skill 68, Network 35, Output 26 y Health 9.
- **Primera explosión en el mes 8.** Sobrevivió.
- **Meses 25–29:** el comentario de RR. HH. vuelve a subir ("quiet", "uneasy", "frowning", "angry"). En las historias de esos meses eligió seis opciones de riesgo +1 que DeepSeek lee como prudentes (cinco de ellas también como prudentes en la prueba de etiquetado):
  - un cambio por fases con escritura doble;
  - llevar una objeción técnica a un 1:1 privado con el responsable (dos veces);
  - denunciar de forma anónima a RR. HH. un conflicto de interés, y después asumirlo si te descubren;
  - dejar para más tarde aprender una tecnología nueva.

  La regla trimestral sí se activó ("Lay low and reduce risk" en el mes 27), pero no compensó. **Segunda explosión en el mes 30: crisis de confianza.**

## Las dos partidas

| | Partida 1 | Partida 2 | Media |
|---|---:|---:|---:|
| Nota | 14,98 | 42,51 | 28,7 |
| Meses | 24 | 30 | |
| Nivel | L1 | L4 | |
| Coste (USD) | 0,229 | 0,310 | 0,269 |
| Fichas de entrada (millones) | 18,2 | 27,0 | |

Referencia: la única partida oficial anterior con DeepSeek (F1, 26 oct) acabó despedida en el mes 24 con 18,8 y costó 0,185 USD. Ninguna de las tres ha terminado los 48 meses. Por meses jugados, t13-read cuesta lo mismo que F1 (0,009–0,010 USD por mes): una partida completa costaría unos 0,45–0,50 USD.

## Lectura

1. **El cuello de botella con DeepSeek es el riesgo que parece constructivo.** En el banco veía el 86 % de las respuestas que suben el riesgo, pero las que fallan son justo estas: lo privado, lo anónimo, lo parcial o por fases, hacer menos para ganar tiempo. Tienen riesgo +1 o +2 y suenan profesionales. En el juego real, unas pocas seguidas bastan para llegar a 5. La ficha v3 ya nombra "en privado" y "parcial", pero DeepSeek no lo aplica cuando la opción además resuelve el problema.
2. **El texto trimestral se cuela en las historias** (partida 1), como vio la línea de transmisión con Haiku. Una regla escrita para el reparto ("tras una C, gasta en el indicador que falta") se usó para elegir historias.
3. **La regla trimestral del riesgo llega tarde.** Actúa al final del trimestre, cuando el comentario ya está en "uneasy" o peor. Con el riesgo subiendo a +1 por historia, hace falta frenar en las historias en cuanto el comentario deja de ser el tranquilo.

**Qué propongo probar (sin gastar en partidas):**
- En la regla de historias, **"si el comentario de RR. HH. no es el tranquilo, descarta también lo que se haga en privado, en anónimo, a medias, por fases o para ganar tiempo, aunque resuelva el problema"**. Medirlo en el banco con los detonantes y el bloque general.
- Acotar por escrito la regla 4 del reparto: "only for Energy and the main action; stories follow the story rule".
- Comprobar en el simulador cuánto vale (bot con la lectura de DeepSeek y la regla "estricta" cuando RR. HH. no está tranquilo).
