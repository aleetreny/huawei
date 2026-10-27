# Línea Formato: cambiar la forma de dar el manual a DeepSeek

**Pregunta.** ¿Se acerca DeepSeek a 75 si cambiamos *qué* recibe el agente, *cuándo*, *en qué forma* y *qué puede hacer con ello*, en vez de escribir mejor el mismo manual?

**Conclusión provisional (27 oct, 21:00).** El agente oficial puede ejecutar código: tiene las herramientas `bash` y `code` y corre un script de la carpeta del Skill en plena partida. Eso permite separar el trabajo: DeepSeek sólo **lee** (pone signos a cada opción y el tono de RR. HH.) y un **script decide**, siempre igual y con memoria propia de la partida. En el simulador, ese script con las lecturas reales de DeepSeek saca 51,5 (63,4 con lecturas exactas), frente a 15 y 42 de las dos últimas partidas oficiales de DeepSeek. Falta medirlo en partidas oficiales.

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

## Relevo

1. **Hecho:** medido qué ve y qué puede hacer el agente oficial (modelo falso, 0 USD); escrito `script-v1` y su simulador.
2. **Resultados:** simulador arriba. Datos y logs en `~/careerlab-data/formato/` (`system_prompt.txt`, `tools.json`, `obs_seq.txt`).
3. **A medias:** partidas oficiales de `script-v1` con DeepSeek (siguiente).
4. **Retomar:**
   ```sh
   uv run python scripts/formato/simadv.py --advisor lab/policies-src/formato/script-v1/bundle/skills/career-advisor/script/advisor.py \
     --exact --rulebot --labels ds=$HOME/careerlab-data/deepseek/labels/ds-v3-r1-full.json+$HOME/careerlab-data/deepseek/labels/ds-v3-r2-full.json --games 2000
   ```
