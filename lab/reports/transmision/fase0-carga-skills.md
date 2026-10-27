# Fase 0. Cómo llega el Skill al modelo

27 oct 2026, rama `alejandro/transmision`. Fuentes: el runner oficial `career_sim_runner` (commit `00b084a8`, instalado con `sh scripts/setup_official_runner.sh`) y el paquete público JiuwenSwarm 0.2.4b3 / openjiuwen 0.1.16 de su entorno. No se ha leído nada del motor del juego.

## Lo que hace el programa oficial

1. **Instalación** (`career_sim_runner/install.py`). Copia cada `skills/<nombre>/` al directorio de Skills de JiuwenSwarm, los registra como Skills locales y escribe `IDENTITY.md` con la plantilla `prompts/identity.md`: la lista de **nombres** de Skills y la `instruction` del `manifest.json`.
2. **IDENTITY.md va en el mensaje de sistema en cada llamada** (`ContextAssembleRail`, sección `context.identity`) y no se comprime nunca. Es el único texto del equipo que el modelo ve siempre, junto con las descripciones.
3. **Skills: modo `all`** (`config.yaml` → `react.skill_mode: all`; `SkillUseRail`). En cada llamada, el mensaje de sistema lleva una sección así:

   ```text
   # Skills

   Read the relevant SKILL.md using read_file before execution.

   Available skills:
   0. <name>: <description>

   1. <name>: <description>
   Select the most relevant skill by reading its SKILL.md first.
   ```

   - **Sólo el nombre y la `description`** del front matter están siempre en el contexto. El orden es el del directorio (alfabético en la práctica).
   - **El cuerpo del SKILL.md sólo entra si el agente lo pide** con la herramienta `skill_tool` (o `read_file`). Llega como resultado de herramienta, una vez, dentro del historial.
4. **Compresión del historial** (`context_engine_config`): resúmenes de mensajes grandes (más del 10 % de la ventana, o más del 5 % con más de 300 s de antigüedad cuando la ocupación pasa del 50 %) y compresión del diálogo al 80 % de la ventana, conservando los 4 últimos mensajes. Con un historial largo, **el cuerpo leído al principio puede acabar resumido**; el mensaje de sistema (identidad + descripciones) no.
5. Si el agente para antes de terminar, el runner manda el mensaje de continuación (`play_headless_continue.md`): “Call check_latest_logs… Call observe… continue”. Tras una compresión, el agente retoma con eso y el mensaje de sistema.

## Lo que hacía nuestro actor de Haiku

`careerlab/actors/claude_cli.py`, `skills_mode=inline` (todos los actores registrados): la identidad oficial **más el cuerpo completo de cada SKILL.md pegado al mensaje de sistema**, siempre presente. El modo `plugin` usa la herramienta Skill de Claude Code, más parecida pero con otro texto de cabecera.

**No coinciden.** En la evaluación oficial:
- el cuerpo puede no leerse nunca, o leerse una vez al principio y quedar lejos (o resumido) cuando el contexto crece;
- la descripción y la `instruction` del manifest se ven siempre.

Esto puede explicar parte de lo que vimos anoche (Haiku no cambia sus respuestas con ningún manual): en nuestras pruebas el manual estaba siempre a la vista, y aun así no mandaba. En la oficial todavía manda menos, salvo lo que esté en la descripción o en la instrucción.

## Consecuencias para el banco

- El banco reproduce la forma oficial: mensaje de sistema = `identity.md` oficial (con la instrucción del manifest) + la sección de Skills con el texto exacto de arriba; el cuerpo sólo llega si el modelo llama a `skill_tool`, una herramienta MCP falsa que devuelve el SKILL.md como la oficial (`skill_content`).
- El juego llega por un servidor MCP falso con las 5 herramientas oficiales: `observe` devuelve la situación reconstruida con el formato exacto del juego, `check_latest_logs` el registro real de esa partida y `take_action` anota la elección y corta la llamada.
- Dos condiciones de contexto: **corta** (mensaje oficial de continuación y la decisión enseguida, como tras una compresión) y **larga** (el agente juega antes varias decisiones reales grabadas de la misma partida, con el Skill leído al principio y cada vez más lejos).
- Se mide también si el agente llega a leer el cuerpo. Si no lo lee, lo que no esté en la descripción o en la instrucción no existe.

Palancas de transmisión que salen de aquí y se prueban en el banco: poner la regla en la `description`, en la `instruction` del manifest o sólo en el cuerpo.
