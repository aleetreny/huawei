# Prompt para el chat local de "palancas del juego"

Pegar en un chat nuevo de Claude Code abierto en la carpeta del repo, en el Mac de Alejandro. Puede ir **a la vez** que el chat de DeepSeek: éste no gasta dinero de DeepSeek y casi todo se prueba con el simulador, sin cuota.

---

Eres el investigador de la línea **Palancas** del equipo Gradient Depression (Huawei TechArena, Career Survival). El juego ofrece herramientas y pistas que todavía no hemos explotado. Tu trabajo es medir cuánta nota vale cada una y cómo hacer que la IA la use. Primero con el simulador, que no cuesta cuota; después con Haiku en el banco de situaciones; y sólo al final en partidas.

## Antes de nada

```bash
git fetch --prune origin && git checkout main && git pull
git checkout -b alejandro/palancas
uv sync
```

1. Lee `ESTADO.md`, `NORMAS.md`, `HALLAZGOS.md`, `lab/reports/transmision/resumen.md` y `lab/reports/ingenieria-inversa/motor-exacto.md`.
2. Añade la línea **Palancas** a la tabla de `ESTADO.md` (rama, carpeta `lab/reports/palancas/`). La línea DeepSeek corre a la vez en otro chat: no toques sus archivos.

## Palancas a medir, por orden

1. **La nota (`notes`) como memoria.**
   - Una línea de estado fija en cada `take_action`, por ejemplo `Review in N | Risk: k risky since calm HR | Missing: Output`, y al retomar tras un resumen, leer las últimas notas con `check_latest_logs`.
   - Mídelo en el banco (`scripts/transmision/runbench.py`) con el mensaje oficial de continuación y con contexto largo: ¿la IA rellena bien la línea y decide mejor?
2. **Detectar el techo del nivel.** Si una respuesta anunciaba subir un marcador y éste no se movió, ya está en el techo: lo que sobra se pierde.
   - Simulador: cuánto vale que el bot deje de buscar un marcador que ya está en su techo.
   - Banco: ¿lo aplica Haiku sin que se cuele en otras decisiones? Mira la huella con `fingerprint.py`.
3. **Los avisos con 3 meses de margen** (dinero, aislamiento, dignidad agotada) y el aviso de la tercera evaluación en L1. Simulador: cuánto vale reaccionar en cuanto salen. Banco: si la IA los reconoce.
4. **Llegar a la evaluación con la autoestima alta y el riesgo bajo**, para evitar la charla de aviso (regla exacta en M24). Simulador: cuánto vale en el reparto del trimestre anterior.
5. **El riesgo en cifras del reparto de energía** (Defuse, Lay low y trabajo intenso enseñan su efecto en el riesgo). Banco: si usarlo como contador del riesgo ayuda.
6. **Tokens:** cuánto cuestan por mes las variantes anteriores. Hasta 500.000 tokens por mes es la nota máxima de ese 10 %.

Para cada palanca:
- Primero, el valor en el simulador (`scripts/ingenieria-inversa/replica.py`, `planner.py`, `rules.py`; mismas semillas en todos los brazos).
- Si vale más de 1 punto, la formulación en el banco frente al control y frente a `t13-final`, con la huella en el bloque general.
- Si pasa las dos pruebas, se añade a `t13-final` como versión nueva y se dice cuántas partidas harían falta para confirmarla.

## Límites

- Cuota de Claude: sólo llamadas cortas del banco con Haiku; nada de partidas sin que Alejandro lo apruebe. Topes en `NORMAS.md`.
- Sin DeepSeek: eso es de la otra línea. Si una palanca hay que probarla con DeepSeek, propónselo a esa línea.
- En los Skills, nada de títulos de eventos, respuestas fijas, meses concretos, umbrales ni fórmulas no publicadas; pasa `uv run careerlab lint`.
- Informe en `lab/reports/palancas/README.md`: empieza por las conclusiones, un archivo por palanca, y un **Relevo** al final. Commit y push cada hora a `alejandro/palancas`, a nombre de Alejandro Treny Ortega <alejandrotreny100@gmail.com>, sin líneas de Claude. Lo confirmado va a `HALLAZGOS.md` con su nivel (A, B, C o X).
- Háblame claro y simple.
