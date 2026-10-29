# Corte 2 (30 oct, 24:00 UK): cómo cerrar el paquete

Interno, no va en el ZIP (el script de empaquetado sólo copia `README.md`, `skills_design.md` y `decision_report.md` de esta carpeta).

**Estado (29 oct).** Todo listo menos lo que depende del manual, que decide el chat comprobador de DeepSeek:
- **Documentos para el ZIP, en inglés:** `README.md`, `design/skills_design.md` y `design/decision_report.md`. Se han preparado a partir de los del corte 1, con lo aprendido el 28 y el 29 oct, y lo que depende del manual va marcado `TODO(manual: …)`.
- **Script de empaquetado:** `scripts/entrega/build_cut.py`. Probado con v4 y los documentos del corte 1: validación oficial OK, y avisa de que ese contenido es idéntico al corte 1.

## Pasos cuando haya manual

1. **Rellenar los `TODO(manual)`.** Son diez, en los tres documentos:
   - nombre de la versión;
   - qué cambia y por qué, con el hallazgo de los registros que lo motivó (pregunta 2 del vídeo);
   - fila nueva en la tabla de versiones (§6 del diseño);
   - pruebas del cambio y partidas de DeepSeek con su nota (§5b del informe);
   - por qué se eligió.

   Si el manual cambia las reglas de historias o del trimestre, reescribir §4–§5 del diseño para que digan lo mismo que el Skill. **Los revisores comparan los documentos con el Skill.**
2. **Vídeo.** El del corte 1 (`~/careerlab-data/entrega/cut1/presentation.mp4`, 6 min 22 s, copia en iCloud Drive `huawei-entrega-copia/cut1`) cuenta el diseño de v4.
   - **Si el manual nuevo es un retoque de v4** (mismo Skill, mismas secciones), se puede reutilizar: responde a las 5 preguntas y la validación sólo pide que exista.
   - **Si cambia algo visible para el jurado** (un script, otro reparto trimestral, otra lista de riesgo), conviene grabar uno nuevo. Lo que cambiaría en cada pregunta:
     1. lo mismo;
     2. el hallazgo nuevo de los registros y el cambio;
     3. si se añade un script, por qué;
     4. lo mismo, más el techo de ~72 del jugador perfecto;
     5. lo de §5b: la lectura manda y la redacción apenas la mueve.
   - El jurado sólo ve el ZIP de los 10 primeros. Mejor que cada ZIP lleve un vídeo coherente con sus Skills.
3. **Empaquetar y validar:**

   ```bash
   uv run python scripts/entrega/build_cut.py --policy lab/policies-src/<familia>/<manual> --cut cut2 \
     --design docs/entrega/cut2 --video <presentation.mp4>
   ```

   Deja `~/careerlab-data/entrega/cut2/solution/`, `gradient-depression-<manual>-cut2.zip` y `package.json`. Sale con 1 si hay algún problema:
   - errores de lint;
   - la validación oficial falla;
   - algo no está en inglés o queda un `TODO`;
   - los documentos no nombran el Skill o la versión;
   - se cita un título de evento;
   - no hay vídeo o pasa de 10 min;
   - el contenido es idéntico a un corte ya puntuado (no se volvería a puntuar).
4. **Antes de subir:**
   - comprobar que la última prueba se hizo con JiuwenSwarm 0.2.4b3;
   - copiar `cut2/` a iCloud Drive (`huawei-entrega-copia/`);
   - apuntar en ESTADO (fila Entrega) el manual, el `content_sha256` de `package.json` y la hora.

## Qué no hacer

- **Subir otra vez v4 sin cambios:** idéntico al corte 1, no se puntúa.
- **Dejar en el ZIP este archivo, los informes internos o datos de `lab/data/`.**
