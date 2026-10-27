# Línea Formato: cambiar la forma de dar el manual a DeepSeek

**Pregunta.** ¿Se acerca DeepSeek a 75 si cambiamos *qué* recibe el agente, *cuándo*, *en qué forma* y *qué puede hacer con ello*, en vez de escribir mejor el mismo manual?

**Conclusión (27 oct, 22:10 UTC).** El agente oficial puede ejecutar código (`bash`, `code`) y correr un script de la carpeta del Skill en plena partida. Con eso, DeepSeek sólo **lee** cada opción (signos de los indicadores y riesgo) y un **script decide** con memoria propia de la partida. **Ese formato dio la mejor partida de DeepSeek que tenemos: 76,87** (48 meses, L6, por encima de 75), pero **todavía no es estable**: las 5 partidas oficiales de `script-v1` y `script-v3` dan 76,87 · 66,55 · 60,45 · 32,59 · 13,23 (media 49,9), frente a 71,67 y 70,22 de `t13-read-v4` (DeepSeek decide con reglas escritas). Cada partida rota tiene una causa distinta y concreta (un punto perdido en L1, la cartera oculta, explosiones), y el script tiene más techo cuando juega limpio (L5–L6, Skill 103–147). **Para el corte 1, `t13-read-v4` sigue siendo la opción segura.**

Rama `alejandro/formato`. Código en `scripts/formato/`, manuales en `lab/policies-src/formato/`, datos fuera de Git en `~/careerlab-data/formato/`.

## 1. Qué recibe el agente en el programa oficial (medido, coste 0)

Montamos un modelo falso compatible con OpenAI (`~/careerlab-data/formato/fake_llm.py`) y jugamos con el runner oficial (`career_sim_runner` 00b084a8, JiuwenSwarm 0.2.4b3) contra él. Así vemos el mensaje de sistema y las herramientas exactas, sin gastar.

- **52 herramientas.** Además de las 5 del juego y `skill_tool`: `bash`, `code` (Python o JavaScript), `read_file`, `write_file`, `edit_file`, `glob`, `grep`, `list_files`, memoria (`write_memory`…), `todo_*`, `task_tool` (subagentes), `cron`, y otras.
- **`bash` y `code` funcionan en partida headless.** Con el modelo falso pedimos `python3 <skills>/career-probe/script/probe.py`: se ejecutó y devolvió su salida. `write_file` también escribe. Los permisos de JiuwenSwarm están desactivados (`permissions.enabled: false`).
- **El directorio de trabajo de `bash`** es `…/agent/workspace/projects`, al lado de `…/agent/workspace/skills/<skill>/`, donde el instalador copia cada Skill entero (`script/` y `reference/` incluidos). Ruta relativa que funciona: `../skills/<skill>/script/<archivo>`.
- **Mensaje de sistema:** 25.000 caracteres en chino (`preferred_language: zh`, el valor no interactivo), con `IDENTITY.md` (la `instruction` del manifest) y la lista de Skills con su `description`. El cuerpo del SKILL.md sólo llega si el agente lo pide.

Las normas permiten scripts en el Skill (`script/`), prohíben que dañen el entorno o lean fuera de la entrega, y piden en el vídeo explicar por qué se usaron.

## 2. Manual `script-v1`: el agente lee, el script decide

`lab/policies-src/formato/script-v1/bundle/`:
- `manifest.json`: la `instruction` (siempre a la vista, sobrevive a los resúmenes) lleva el bucle y el formato completo de la llamada.
- `skills/career-advisor/SKILL.md`: el bucle, cómo rellenar la línea, la guía de lectura (pistas v3 de la línea DeepSeek, B18) y qué pondera el script.
- `skills/career-advisor/script/advisor.py`: recibe una línea (`sid`, mes, estado, tono de RR. HH., fase y, en historias, los signos de cada opción con `R+`/`R-`), aprende en la partida qué indicador se ha estancado (una subida publicada que no se registra), lleva la cuenta del riesgo desde el último comentario de RR. HH., y devuelve `CHOOSE n` y una línea `NOTE`. Memoria: un JSON por partida en `script/state/`. No ve ningún texto de evento.

La regla del script es la del bot de 7 reglas (`scripts/ingenieria-inversa/rules.py`) sin información privilegiada (techos aprendidos en partida, riesgo por el tono al empezar el mes) y más prudente con el riesgo y la salud, porque las lecturas fallan.

## 3. Simulador (`scripts/formato/simadv.py`)

Juega el script real dentro de la réplica; en las historias le pasa sólo los signos que puso DeepSeek (dos pasadas v3 del catálogo, una al azar en cada encuentro) y el tono de RR. HH. del inicio del mes. 2.000 partidas por brazo:

| Brazo | Nota | Despidos L1 | Crisis de confianza | Salud |
|---|---:|---:|---:|---:|
| Bot de 7 reglas con información exacta (referencia) | 67,9 | 7 % | 3 % | 0 % |
| Script con signos exactos | 63,4 | 13 % | 2 % | 0 % |
| **Script con lecturas de DeepSeek** | **51,5** | 25 % | 14 % | 1 % |

Descomposición (1.000 partidas, script con parámetros prudentes): con riesgo exacto y signos de DeepSeek, 56,9; con signos exactos y riesgo de DeepSeek, 56,7. Cada mitad de la lectura cuesta ~5–6 puntos.

Ajustes probados en la regla (sin salto): proteger los meses 3–5 antes de la evaluación (−3), empujar los indicadores no estancados antes de la evaluación (0). Más prudencia con riesgo y salud: +4 (47,8 → 51,7). Los despidos vienen de llegar a la evaluación del mes 6 o 12 con un punto menos de Network u Output.

## 4. Primeras partidas oficiales de `script-v1` y lo que enseñan (27 oct, 19:56–21:00 UTC)

Dos partidas en paralelo con DeepSeek (slots propios `~/careerlab-data/formato/slot-a`, `slot-b`).
- **El formato funciona mecánicamente.** DeepSeek lee el SKILL.md, monta la línea, ejecuta el script (con la ruta absoluta) y toma su elección: 14 de 14 decisiones al principio, sin fallos de formato. ~12–15 s por decisión, dentro del corte de 2 h del runner.
- **Partida 1 (slot-a): atascada en L1.** El riesgo subió de 0 a 3 en un mes (leyó "N+ O+" una opción con riesgo +2 y usa `R-` de más), explotó en el mes 6, y en el mes 12 llegó con Output un punto por debajo. Es el fallo que el simulador ya predecía (25 % de despidos): con las lecturas de DeepSeek, que el script decida todo deja sin uso el juicio global de DeepSeek.
- **Partida 2 (slot-b):** L3 en el mes 12.

**Lectura de DeepSeek en partida** (`scripts/formato/ingame.py`, primeras 18 opciones): ve el riesgo (86 %) pero marca `R-` de más y casi no ve las subidas de Skill (17 %).

**Lista de comprobación descartada.** Pedir señales sí/no por opción (prompt `scripts/deepseek/prompts/perceive-f1.md`, una pasada del catálogo, 0,05 USD) no mejora la lectura: riesgo 90 % (v3: 88 %), Skill igual, el resto peor.

**Cambio de rumbo: híbrido `script-v2`.** La línea DeepSeek publicó `t13-read-v4`, 71,67 en una partida oficial completa (DeepSeek decide todo). Su traza muestra lo que DeepSeek no hace: nunca rellena "Stalled", y en L4 (meses 30–36) siguió gastando cada trimestre en Network y Output, parados en 36 y 26, mientras Skill, el freno de L4, subía despacio (ascenso a L5 en el mes 42). `script-v2` deja las historias a DeepSeek con las reglas de v4 y pasa al script sólo la contabilidad:
- `phase=status` al empezar cada mes: línea de estado con Best, Stalled y Review in N calculados;
- `phase=quarter` una vez por trimestre: todo el reparto de energía y la acción principal.
Son ~64 llamadas más por partida, no ~230. En el simulador, planificar el trimestre de una vez no pierde nada (51,1 frente a 51,5).

## 5. Resultados de partidas oficiales con DeepSeek (programa oficial, juego de desarrollo)

| Manual | Forma | Partidas (`quantitative_score`) | Detalle | Coste por partida |
|---|---|---|---|---|
| `t13-read-v4` (línea DeepSeek, referencia) | DeepSeek decide todo con reglas escritas | 71,67 · 70,22 · (una atascada en L1, cortada por un choque de puertos) | L5, riesgo 0 | 0,7–0,8 USD |
| **`script-v1`** | DeepSeek lee y etiqueta; el script decide todo | **76,87** · 13,23 | 76,87: 48 meses, **L6**, Skill 147, Network 58, riesgo 1. 13,23: explosión en el mes 6 y un punto de Output perdido antes de la evaluación del mes 12 → despido en el mes 24 | 1,24 (completa) · 0,83 |
| `script-v2` | Historias por DeepSeek (reglas de v4); el script lleva estado y trimestres | 51,12 · 30,6 | 51,12: atascado en L3 (Output). 30,6: dos explosiones por opciones "pragmáticas" (arreglo más tarde, vía corta) que DeepSeek justificó con la excepción de "el riesgo más pequeño" | 0,74 · 0,31 |

**Lectura.**
- `script-v1` da la mejor partida de DeepSeek que tenemos (76,87, por encima de 75) y llega a L6, que ningún manual había alcanzado con DeepSeek. Es todo o nada: si pasa L1, el script juega mejor el resto de la carrera que las reglas escritas (Skill cuando Network y Output se estancan, L5 en el mes 36 frente al 42 de v4).
- Su punto débil es L1, donde un solo error de lectura en el mes previo a la evaluación cuesta el ascenso. En la partida de 13,23, DeepSeek leyó "S+ D+ R-" una opción (arreglar la build a fondo) que costaba Output −1, y el script la eligió.
- El híbrido v2 pierde lo bueno de los dos: DeepSeek, decidiendo, vuelve a tomar riesgos "razonables". Descartado.
- **`script-v3`** = v1 + **recordatorios de lectura justo a tiempo**: cuando quedan 1–2 meses para la evaluación, o el tono de RR. HH. no está tranquilo, la salida del script añade una línea `READ NEXT` con lo que suele costar Output/Network o esconder riesgo, justo antes de que DeepSeek lea la siguiente historia. Además, `R-` sólo cuando la opción documenta, informa, asume o arregla del todo. Tres partidas en juego desde las 21:02 UTC.
- **Fichas:** v1 gasta ~2,3 millones de fichas por mes en la partida completa (110 M en total), frente a ~1,4 M de v4: la llamada extra al script en cada decisión con el contexto lleno. Eso baja la parte de eficiencia (10 % de la versión) de ~64 a ~28, unos 3,6 puntos de la versión. Hay que recortarlo si v3 se confirma.

### `script-v3` (v1 + recordatorios de lectura justo a tiempo), 3 partidas desde las 21:02 UTC

| Partida | Nota | Final | Coste |
|---|---:|---|---:|
| sv3-g1 | 66,55 | 48 meses, L5, Skill 103, Network 33, riesgo 0 | 1,22 USD |
| sv3-g3 | 60,45 | 48 meses, L4, Skill 89, Network 36, riesgo 0 | 1,21 USD |
| sv3-g2 | 32,59 | **ruina en el mes 10** | 0,12 USD |

- **L1 resuelto en las tres** (ascenso en el mes 6); los `READ NEXT` se aplican (26 en una partida). Con v1, 1 de 2 se quedó en L1.
- **Fallo nuevo: la cartera oculta.** El script eligió una opción bien leída como `W-` (−2 de dinero) con la cartera casi vacía. El panel redondea Wealth hacia abajo: mostró 0 seis meses mientras era negativo, y el juego eliminó la partida por ruina. `script-v3b` (sin jugar) prohíbe opciones `W-` con poco dinero visible si hay otra.
- **Donde pierde frente a v4 cuando termina:** Network (33–36 frente a 54) y dinero (25–33 frente a 38), y ascensos atascados a mitad (L2 en los meses 12–18, L3–L4).

### Resumen de las 11 partidas oficiales de la línea y de la referencia

| Manual | Notas | Media | Completas |
|---|---|---:|---:|
| `t13-read-v4` (referencia, línea DeepSeek) | 71,67 · 70,22 | 70,9 | 2 de 2 (una tercera, cortada por un choque de puertos, iba atascada en L1) |
| `script-v1` | 76,87 · 13,23 | 45,1 | 1 de 2 |
| `script-v2` (híbrido) | 51,12 · 30,6 | 40,9 | 1 de 2 |
| `script-v3` | 66,55 · 60,45 · 32,59 | 53,2 | 2 de 3 |

**Fichas.** Las partidas completas con script gastan ~110 M de fichas (~2,3 M por mes) frente a ~70 M de v4: una llamada más por decisión con el contexto lleno. La parte de eficiencia (10 % de la versión) baja de ~64 a ~28 puntos: ~3,6 puntos de la versión.

**Gasto de la línea:** 5,7 USD (partidas 5,67; una pasada de percepción 0,05). Tope anunciado: 8 USD.

## Relevo

**27 oct, 22:40 UTC.** Las 2 partidas de `script-v4` (lanzadas a las 22:25) se pararon a petición de Alejandro en los meses 8–9: no cuentan. Se sigue mañana. `script-v4` y `script-v3b` están listos y sin jugar.


1. **Hecho y por qué.** Medí qué recibe y qué puede hacer el agente oficial (modelo falso, 0 USD): tiene `bash` y `code` y ejecuta scripts del Skill. Probé tres formas de usarlo en partidas oficiales con DeepSeek:
   - `script-v1`: DeepSeek etiqueta y el script decide todo;
   - `script-v2`: híbrido con las reglas de historias de v4;
   - `script-v3`: v1 con recordatorios de lectura que el script imprime justo antes de las lecturas que más cuestan.

   Descarté leer con lista de comprobación (banco, 0,05 USD) y los retoques de la regla del script en el simulador (todos ±0,5).
2. **Resultados.** Tablas de §5. La mejor partida de DeepSeek hasta hoy es de este formato (76,87, L6), pero de media la familia script (49,9) queda por debajo de `t13-read-v4` (70,9, n = 2). Datos y trazas en `~/careerlab-data/formato/runs/<sv1-g1…sv3-g3>/` (play.log, cost.txt, output/events-*.jsonl, advisor-state/). Análisis de lectura en partida: `uv run python scripts/formato/ingame.py <events.jsonl>`.
3. **Qué falló o quedó a medias.**
   - Muestras muy pequeñas: hacen falta más partidas para separar formato y suerte.
   - `script-v3b` (cartera) no se ha jugado.
   - El gasto de fichas del formato script es ~1,6 veces el de v4.
   - El script confía a ciegas en las etiquetas: cada error de lectura en un momento crítico se paga entero.
4. **Siguiente paso** (para el corte 2, 30 oct):
   - **Combinar al revés que v2:** DeepSeek decide las historias con v4 y el script sólo **vigila** (veto). Rechazaría la elección de DeepSeek si sus propias etiquetas dicen `W-` con poco dinero, `-S/-N/-O` en el mes previo a la evaluación, o `R+` con RR. HH. no tranquilo. Además planificaría el trimestre, sobre todo de L3 en adelante, donde el script ganó a v4: L5 en el mes 36 frente al 42 y Skill 147.
   - Recortar fichas: notas de una línea y salida del script mínima.
   - Con permiso, 3 partidas de cada candidato (~1,2 USD cada una).

   Comandos:
   ```sh
   # simulador (gratis)
   uv run python scripts/formato/simadv.py --advisor lab/policies-src/formato/script-v3b/bundle/skills/career-advisor/script/advisor.py \
     --labels ds=$HOME/careerlab-data/deepseek/labels/ds-v3-r1-full.json+$HOME/careerlab-data/deepseek/labels/ds-v3-r2-full.json --games 3000
   # una partida oficial en un slot propio (cuesta ~1,2 USD; arranques escalonados por up.sh)
   cp -R lab/policies-src/formato/script-v3b/bundle ~/careerlab-data/formato/sol-x   # + README.md y design/
   bash scripts/formato/game.sh ~/careerlab-data/formato/slot-a ~/careerlab-data/formato/sol-x <tag>
   ```
   Slots: `~/careerlab-data/formato/slot-{a,b,c,d}` (runner 00b084a8, `.env` copiado de slot0). No tocar `local-runs/official-runner/.env`. Comprobar `lsof` antes de arrancar si otro chat juega.
