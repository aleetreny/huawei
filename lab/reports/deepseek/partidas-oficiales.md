# Partidas oficiales de t13-read-v1 con DeepSeek

**Conclusión (partida 1 de 2; la segunda está en juego).** DeepSeek juega `t13-read-v1` de punta a punta por la vía oficial y aplica la regla de historias en cada nota. Aun así, en la primera partida fue **despedido en el mes 24 sin salir de L1 (nota 14,98)**. La causa: la regla trimestral "tras una evaluación floja, céntrate en el indicador que falta" se coló en las historias y le hizo elegir opciones "eficientes" que cargaban riesgo. El riesgo explotó justo antes de la evaluación del mes 12. Coste: 0,23 USD por partida.

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

En juego.

## Lectura

Es lo mismo que la línea de transmisión vio con Haiku: **el texto sobre el reparto trimestral se cuela en las historias**. Aquí lo hace una regla pensada para el trimestre ("después de una C, gasta en el indicador que falta"), que DeepSeek usa para justificar opciones de historia que ahorran tiempo y cargan riesgo. Arreglos posibles, sin gastar:
1. Acotar la regla 4 al trimestre por escrito: "only for Energy and the main action; in stories the story rule decides".
2. Añadir a la ficha de riesgo "skipping the thorough or proper way to save time".
3. Comprobarlo en el banco (las historias de los meses 7–11 tras una C) antes de más partidas.
