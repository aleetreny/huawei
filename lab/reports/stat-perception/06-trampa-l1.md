# 06. La trampa del primer ascenso (L1): de qué está hecha y qué no la arregla

**Conclusión: 2 de cada 3 puntos de Network u Output perdidos antes de una evaluación en L1 son forzosos (todas las opciones cuestan o son arriesgadas), también con lectura perfecta; ninguna de las 7 reglas nuevas probadas (vetar tipos de respuesta, dos lecturas, priorizar subidas, llenar en el trimestre) baja los despidos sin subir las crisis de confianza, y la única palanca con ganancia clara sigue siendo leer mejor.**

28 oct, 09:15–10:30 UTC. Sólo la réplica de la línea Motor: sin cuota y sin DeepSeek. 2.000 partidas por brazo con las mismas semillas.

## Montaje

- **Bot.** `LexBot` de la línea DeepSeek (`scripts/deepseek/groupbot.py`) con las reglas de `t13-read-v4` que tiene implementadas:
  - descarta lo arriesgado;
  - ascenso antes que riesgo leve en el mes previo;
  - protege Network y Output dos meses antes en L1;
  - repara lo que baje de su mejor valor;
  - un trimestre parecido al de DeepSeek (preparar informe, Network y proyecto clave).
- **Lectura.**
  - Signos de Haiku: dos pasadas de `plain`, como las dos pasadas de DeepSeek de Alejandro.
  - Riesgo juzgado por el tipo de respuesta de Categorías.
  - Las etiquetas de DeepSeek no están en el repo, así que las notas absolutas son más bajas que las de [mejora-nota.md](../deepseek/mejora-nota.md) (49,7 frente a 53,4). Los brazos se comparan entre sí.
- **Medidas** ([l1_trap.py](../../../scripts/stat-perception/l1_trap.py)):
  - en cada evaluación hecha en L1, qué condición del ascenso falla (Skill, Network u Output bajo el umbral, Dignity bajo 4, nota D);
  - en cada historia de los dos meses previos que cuesta Network u Output, si había una opción segura (sin pérdida y sin riesgo según el efecto exacto): "evitable" o "forzosa";
  - si la ventana de dos meses empezó ya por debajo del umbral, tras el trimestre.

## De qué está hecha la trampa

**Por qué falla cada evaluación en L1** (400 partidas por fila):

| Evaluación | Lectura de Haiku | Lectura perfecta |
|---|---|---|
| Mes 6 | Output 140, Network 88, Skill 28 | Output 98, Network 69, Skill 25 |
| Mes 12 | Output 76, Network 67 | Network 38, Output 36 |
| Mes 18 | **nota D 106**, Output 30, Network 20 | nota D 55, Output 15 |
| Mes 24 | **nota D 104**, Output 38, Network 25 | nota D 53, Network 14 |

- **La nota D sólo aparece en los meses 18 y 24.** Es la consecuencia de haber fallado los meses 6 y 12, no una causa aparte. En la práctica hay **dos oportunidades, los meses 6 y 12**, y las dos se pierden por Network u Output.
- El mes 6 se pierde mucho: el 46 % de las partidas con lectura de Haiku y el 34 % con lectura perfecta. La trampa es perder también el mes 12.

**Puntos de Network u Output perdidos en los dos meses previos** (2.000 partidas):

| Lectura | Forzosos | Evitables |
|---|---:|---:|
| Haiku | 3.432 (67 %) | 1.680 (33 %) |
| Perfecta | 2.600 (77 %) | 784 (23 %) |

**Cómo empieza la ventana en las evaluaciones fallidas de los meses 6 y 12:** el 31 % ya entra por debajo del umbral después del trimestre (431 de 1.381); el 69 % entra en el umbral y pierde un punto en las historias.

## Lo que se probó

| Brazo | Qué añade a las reglas de v4 | Nota | Acaba en L1 | Despidos | Crisis |
|---|---|---:|---:|---:|---:|
| **base** | — | **49,7** | 23,2 % | 441 | 376 |
| cat1 | En L1, el mes previo: descartar tipos que bajan Network la mitad de las veces o más (atacar, empecinarse, venderse, protegerse, escalar, evitar) | 49,5 | 21,2 % | **352** | 412 |
| cat2 | Lo mismo, los dos meses previos | 46,7 | 26,1 % | 320 | 416 |
| nofirst | Si Network u Output están bajo el umbral: primero una opción segura que los suba | 49,8 | 22,9 % | 429 | 379 |
| tworeads | Una opción cuesta si cualquiera de dos lecturas (plain y defs3) lo dice | 48,3 | 26,9 % | 516 | 371 |
| vote | Lectura = votación de 5 lecturas (vote5c) | **50,2** | 24,5 % | 450 | **301** |
| fill | Trimestre previo en L1: Energy primero a lo que les falta a Network y Output, contando el proyecto clave | 49,7 | 23,1 % | 438 | 378 |
| fill+cat1, fill+vote, cat2+nofirst, cat2+tworeads | Combinaciones | 46,4–50,1 | 21–27 % | 338–450 | 306–421 |
| *perfect* | *Lectura perfecta* | *55,7* | *13,1 %* | *244* | *352* |
| *perfect+fill / perfect+cat2* | | *55,5 / 50,2* | *13,2 / 20,9 %* | *245 / 282* | *356 / 429* |

Error típico de cada nota: ~0,4.

## Lectura

- **Vetar tipos de respuesta cambia despidos por crisis.** cat1 quita 89 despidos y añade 36 crisis, con la misma nota. Es el mismo patrón que vio Alejandro al aceptar riesgo para salvar el ascenso: en esos meses, lo que salva el punto suele llevar riesgo.
- **Llenar en el trimestre arregla la entrada, no el resultado.** Las ventanas que empiezan cortas bajan de 431 a 361, pero los despidos no se mueven (441 → 438): esas partidas llegan en el umbral y pierden el punto en las historias igual.
- **Dos lecturas prudentes empeoran.** Marcar como costosa cualquier opción que una de las dos lecturas vea costosa deja menos opciones buenas, y el bot acaba en peores.
- **La votación ayuda poco y sobre todo en riesgo:** +0,5 de nota (dentro del ruido) y 75 crisis menos.
- **Lo que sí mueve la trampa es leer mejor:** con lectura perfecta, acabar en L1 baja del 23 % al 13 %, igual que vio Alejandro con la lectura de DeepSeek (19 % → 9 %). Aun así, con lectura perfecta 3 de cada 4 pérdidas son forzosas, y ninguna regla probada las convierte en evitables.

## Qué queda para el manual

- **Ninguna regla nueva para t13-read-v4 sale de aquí.** Se queda como está.
- **Descartadas en la réplica:**
  - vetar tipos de respuesta antes de la evaluación;
  - una regla de "dos lecturas, la más prudente";
  - priorizar subidas de Network y Output;
  - llenar en el trimestre previo.
- **Lo que hace falta probar es la percepción de los costes de Network y Output en DeepSeek.** Es la línea de Alejandro, y su prompt v4 no lo consiguió.
  - Una vía sin probar con DeepSeek es leer dos veces y votar dentro de la misma respuesta.
  - Otra es la de `alejandro/formato`: que un script decida con la lectura de DeepSeek.

## Límites

- La lectura es la de Haiku, no la de DeepSeek, y el riesgo se juzga por el tipo de respuesta.
- El bot no es DeepSeek. Con esta lectura la nota base es 49,7, no los ~70 de las partidas reales de v4.
- Las conclusiones son comparaciones entre brazos con las mismas semillas.
- No se jugó ninguna partida ni se usó el banco con IA, porque ningún brazo ganó en la réplica (NORMAS §1.7).

Datos: [l1-trap.json](l1-trap.json).
