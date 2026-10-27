# Prompt para el chat local de DeepSeek

Pegar tal cual en un chat nuevo de Claude Code abierto en la carpeta del repo, en el Mac de Alejandro (donde está la clave de DeepSeek).

---

Eres el investigador de la línea **DeepSeek** del equipo Gradient Depression (Huawei TechArena, Career Survival). La evaluación oficial la juega `deepseek-v4-flash` dentro de JiuwenSwarm con nuestro manual (Skills). Ya sabemos casi todo del juego y cómo escribirle reglas a Haiku. Tu trabajo es averiguar **qué entiende DeepSeek y qué no**, sobre todo **si sabe ver qué indicador sube o baja cada respuesta y cuáles son arriesgadas**. Con eso hay que diseñar la forma más masticada de darle las reglas del juego.

## Antes de nada

1. Pon al día la carpeta y crea tu rama:
   ```bash
   git fetch --prune origin && git checkout main && git pull
   git checkout -b alejandro/deepseek
   uv sync
   ```
   Si `git checkout main` falla por cambios locales, enséñame `git status` antes de tocar nada.
2. Lee, en este orden: `ESTADO.md`, `NORMAS.md`, `HALLAZGOS.md`, `lab/reports/transmision/resumen.md`, `lab/reports/question-bank/README.md` y `lab/reports/ingenieria-inversa/motor-exacto.md` (M10–M14 y M22–M28). No repitas nada de la sección X de HALLAZGOS.
3. En la tabla de líneas de `ESTADO.md`, añade la línea **DeepSeek** (rama, carpeta `lab/reports/deepseek/`, estado) y marca Transmisión y Categorías como **en pausa, sustituidas por DeepSeek**. Commit y push.

## Lo que ya sabemos y te sirve

- **Banco de situaciones con la respuesta correcta**, en `lab/data/transmision/`. Son 2.389 momentos reales de partidas, cada uno con:
  - el `observe` exacto que ve el jugador;
  - el efecto y el riesgo oculto de cada opción;
  - la nota final que da el simulador por opción.

  Lleva también las elecciones de Haiku por brazo para comparar. Se puntúa con `scripts/transmision/score.py` y `scripts/transmision/fingerprint.py`. El formato está explicado en `lab/data/transmision/README.md`.
- **Catálogo exacto de las 936 respuestas**, con efecto y riesgo: `lab/data/ingenieria-inversa/catalog_v2.json`. La taxonomía de 10 tipos de respuesta está en `scripts/question-bank/taxonomy.md`, y las etiquetas de Haiku en `lab/reports/question-bank/labels.json` y `stat-tags.json`.
- **Cómo llega el Skill en el programa oficial:** el modelo ve siempre el nombre y la descripción de cada Skill y la instrucción del manifest; el cuerpo lo lee con `skill_tool` (`lab/reports/transmision/fase0-carga-skills.md`). `scripts/transmision/runbench.py` y `fake_mcp.py` reproducen esa forma para Claude.
- **Manual actual:** `lab/policies-src/transmision/t13-final/`.
  - Una lista trimestral con prioridad.
  - Una cuenta atrás `Review in N` en cada nota.
  - En el mes previo a la evaluación, `reference/review-month.md`.

  Con Haiku saca 57,2 ± 5,1 frente a 50,5 ± 2,5 de f3-lean-v1 (12 partidas frente a 43). Es la mejor señal que tenemos, pero aún no es concluyente.

## Plan

1. **Arnés barato para DeepSeek**, `scripts/deepseek/`:
   - Llama a DeepSeek por la API compatible con OpenAI de OpenRouter. Lee `API_BASE`, `API_KEY` y `MODEL_NAME` de `local-runs/official-runner/.env`, **sin copiarlos nunca al repo ni imprimirlos**.
   - No fijes proveedor ni enrutado (las normas lo prohíben).
   - Apunta en un archivo el coste y los tokens de cada llamada.
   - Prueba primero con 5 llamadas y enséñame el coste real.
2. **Percepción**, lo primero y lo más barato:
   - Dale a DeepSeek preguntas del catálogo, con su texto y opciones tal como salen en `observe`.
   - Pídele, para cada opción: (a) el tipo según `taxonomy.md`; (b) el signo del efecto en Health, Dignity, Skill, Network, Output y Wealth; (c) si añade riesgo oculto.
   - Compara con el efecto y el riesgo exactos: acierto por indicador y riesgo detectado.
   - Haz lo mismo con Haiku sobre las mismas preguntas, si no está ya en `labels.json` y `stat-tags.json`.
   - Separa los títulos reservados (`holdout` del banco) y no los mires al diseñar.
3. **Obediencia:**
   - El banco en forma oficial con DeepSeek: control (sin Skill) y `t13-final`.
   - Unas 40 situaciones por regla de `ids-V2.txt` más el bloque general (`ids-G1.txt`).
   - Mide si lee el Skill, el acierto por regla y la huella en el bloque general.
4. **La categorización: el objetivo central.** Buscamos la forma de agrupar las respuestas que maximice dos cosas a la vez:
   - (a) **que DeepSeek la entienda:** que ponga cada respuesta en su grupo de forma correcta y estable (repetido, el mismo grupo), leyendo sólo el texto;
   - (b) **que discrimine:** que dentro de cada situación baste con una regla de grupo (“elige la del grupo X; si no hay, la del Y…”, con el contexto visible: riesgo, evaluación cercana, salud) para coger casi siempre la respuesta que más nota da.

   Una categorización que DeepSeek no reconoce no sirve, aunque discrimine perfecto. Una que reconoce perfectamente pero mete juntas respuestas buenas y malas tampoco.

   **Medida única que junta las dos:** la nota en el simulador (`scripts/question-bank/catbot.py`, 1.000 partidas con las mismas semillas) de un bot que elige las historias **sólo con los grupos que ha puesto DeepSeek**, más la regla de grupo. Compáralo con dos referencias:
   - el bot con los efectos exactos (≈ 68), que es el techo;
   - los 10 tipos actuales etiquetados por Haiku (46,7), que es lo que hay que superar.

   Apunta también el acierto de etiquetado y la pérdida de nota en el banco.

   Cómo probar:
   - Prueba varias categorizaciones, de más simple a más fina. Por ejemplo, los 10 tipos actuales; grupos por lo que la respuesta hace a cada indicador; o tipo más indicador.
   - Prueba también la redacción de cada definición: el texto que lee DeepSeek es parte de la categorización.
   - Elige con unos títulos y comprueba con los reservados.
   - La categorización y la regla de grupo ganadoras son la base del manual. Se escriben como principios generales, sin títulos ni respuestas concretas.

5. **Lo masticado.** Con lo que DeepSeek perciba bien y mal, diseña y prueba formas de dar las reglas. Ejemplos:
   - una ficha corta de cómo leer el coste de una opción, si su percepción falla en un indicador concreto;
   - pedirle una línea por opción antes de elegir;
   - los 10 tipos con su respuesta preferida.

   Normas de la prueba:
   - Una variante cada vez, comparada siempre con el control y con t13-final en las mismas situaciones.
   - Mira siempre la huella del bloque general: una regla de historias que cambia más de 1 de cada 10 historias fuera de su contexto ha estropeado partidas antes.
6. **Sólo si te lo apruebo:** 1–2 partidas oficiales con DeepSeek del mejor manual (`make play` del runner), con el coste medido.

## Límites

- **Presupuesto de DeepSeek para toda la línea: 5 USD.** Quedan unos 49,8 USD y hay que reservar 15 para el último corte. Para a 3 USD gastados y pregúntame. Apunta el gasto acumulado en el informe.
- No uses cuota de Claude para partidas. Sí puedes usar Haiku en llamadas cortas del banco, como comparación.
- En los Skills, nada de títulos de eventos, respuestas fijas, meses concretos, umbrales ni fórmulas no publicadas; pasa `uv run careerlab lint`. El catálogo y el banco son para investigar, nunca para copiarlos a un Skill.
- Informe en `lab/reports/deepseek/README.md`. Empieza por las conclusiones, un archivo por experimento, y un **Relevo** al final. Commit y push cada hora a `alejandro/deepseek`, a nombre de Alejandro Treny Ortega <alejandrotreny100@gmail.com>, sin líneas de Claude. Lo que se confirme va a `HALLAZGOS.md` con su nivel (A, B, C o X).
- Háblame claro y simple: qué has probado, qué ha salido y qué propones, sin siglas sin explicar.
