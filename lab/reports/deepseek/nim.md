# ¿Sirve NVIDIA NIM como DeepSeek gratis?

**Conclusión: preparado y probado contra un servidor falso, sin lanzar; falta la clave de NIM.** La comparación no gasta nada de la clave del reto: el lado de OpenRouter ya está medido dos veces.

## Por qué

- La clave del reto llama a OpenRouter con `deepseek/deepseek-v4-flash` (versión 0423), sin fijar proveedor. De nuestras 10.517 llamadas, el 96 % las sirvió Baidu en fp8 y el resto GMICloud, DeepInfra y otros.
- NVIDIA NIM (build.nvidia.com) sirve gratis los mismos pesos publicados, con un tope de unos 40 mensajes por minuto, pero con su propio sistema de servicio. Si contesta como OpenRouter, nos da banco y partidas sin coste. Si no, sólo sirve para comprobar formatos.
- La API oficial de DeepSeek no sirve: retiró `deepseek-v4-flash` el 10 de septiembre de 2026 y ahora sirve V4.1.

## Diseño

Mismas preguntas, mismo prompt y temperatura 0,95, con `DS_BACKEND=nim`:

| Parte | Datos de OpenRouter (ya pagados) | Qué se repite en NIM | Llamadas | Tiempo a 36 por minuto |
|---|---|---|---|---|
| Percepción `perceive-v3` | r1 y r2: 403 preguntas, 956 opciones | r1 y r2 | ~810 | ~23 min |
| Banco de obediencia, brazo control | `ds-control` y `ds-control-b`: 139 situaciones comunes | `nim-control` | ~830 | ~25 min |

El ruido base es lo que OpenRouter se contradice a sí mismo entre repeticiones. Ya está medido, en porcentaje de opciones con la misma etiqueta:

| tipo | health | dignity | skill | network | output | wealth | risk |
|---|---|---|---|---|---|---|---|
| 85,5 | 87,4 | 84,5 | 86,9 | 82,2 | 81,8 | 96,9 | 88,1 |

Acierto de OpenRouter frente al catálogo: riesgo 82,4–83,0 %, signo de los seis indicadores 77,2–77,3 %.

## Regla de decisión (fijada antes de ver datos de NIM)

NIM sirve de sustituto si se cumplen las cuatro condiciones:

1. `smoke` confirma que el modelo es `deepseek-v4-flash` de abril (no 0731 ni V4.1) y que devuelve razonamiento.
2. En percepción, para cada campo, el acuerdo NIM–OpenRouter no baja más de 3 puntos del acuerdo OpenRouter–OpenRouter (n ≈ 1.900 pares, IC ±1,7).
3. El acierto frente al catálogo (riesgo y signos) queda a menos de 3 puntos del de OpenRouter.
4. En el banco, la misma elección que OpenRouter no baja más de 8 puntos del acuerdo `ds-control`~`ds-control-b` (n = 139, IC ±7), y el porcentaje de situaciones terminadas difiere menos de 5 puntos.

- **Si pasa:** NIM se usa para bancos y partidas de cribado, y OpenRouter sólo para confirmar finalistas.
- **Si falla en algo:** NIM sólo sirve para pruebas de formato, y lo apuntamos en HALLAZGOS como descartado.

## Cómo lanzarlo

1. Crear la cuenta en build.nvidia.com, generar una clave (`nvapi-…`) y comprobar en la ficha de `deepseek-ai/deepseek-v4-flash` la fecha de versión y cómo se activa el razonamiento.
2. Crear `~/careerlab-data/deepseek/nim.env`, fuera del repo, con `chmod 600`:

   ```text
   API_BASE="https://integrate.api.nvidia.com/v1"
   API_KEY="nvapi-..."
   MODEL_NAME="deepseek-ai/deepseek-v4-flash"
   ```

3. Desde `~/huawei-ds`:

   ```bash
   uv run python scripts/deepseek/nimcheck.py smoke
   uv run python scripts/deepseek/nimcheck.py run --limit 10
   uv run python scripts/deepseek/nimcheck.py run
   uv run python scripts/deepseek/nimcheck.py compare --json ~/careerlab-data/deepseek/nimcheck.json
   ```

- `smoke` lista los modelos, hace una llamada normal y una con herramienta, y avisa si no vuelve razonamiento. En ese caso, `NIM_EXTRA` cambia el campo que se envía (por defecto `{"chat_template_kwargs": {"thinking": true}}`; `NIM_EXTRA='{}'` no envía nada).
- `run` se reanuda donde lo dejó. Si NIM devuelve muchos 429, bajar `NIM_RPM`.

## Notas

- El texto del juego va a NVIDIA, como ya va a OpenRouter. Las respuestas quedan en `~/careerlab-data/deepseek/` (`perceive/v3-r*-nim/`, `runs/nim-control/`, `calls-nim.jsonl`), fuera de Git.
- Zona gris de las normas: las reglas limitan el uso de la clave del reto, no prohíben otra API para desarrollo local, pero *"the absence of an express prohibition is not permission"*. Nada de esto entra en la entrega.
- Código: `scripts/deepseek/ds.py` (destino `nim`, ritmo por minuto, `reasoning_content`), `perceive.py` (sufijo `-nim` en las carpetas), `bench.py` (devuelve el razonamiento de NIM en las llamadas con herramientas) y `nimcheck.py`.
- Probado contra un servidor local falso (llamadas, herramientas, reanudación, compare). Sin datos reales todavía.
