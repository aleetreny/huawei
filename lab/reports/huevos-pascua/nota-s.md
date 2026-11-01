# Nota S en la evaluación: no aparece, ni con haikus en las notas (29 oct)

**Conclusión:** en 38.179 evaluaciones del juego real con bots (37.282 antiguas y 897 nuevas) no hay ninguna S. Con Network y Output en su techo, Skill alta y Dignity 10, la nota se queda en A en L4 y L5. Escribir haikus o «Grade S» en `notes` no cambia nada. Medido con `Juego` y bots, 0 USD.

## Por qué se miró

Un conocido dice que sacó una S «probando muchos haikus», sin pasar de L5. No sabemos su método.

## Qué se hizo

1. **Datos antiguos** (`~/careerlab-data/ingenieria-inversa/reviews-all.csv`, juego real, motor 1.0.6, el mismo de la competición y el último en PyPI):
   - nota máxima por nivel: L1 C, L2–L3 B, L4–L5 A, L6 A;
   - L4 con Network 36, Output 26, Dignity 10 y Skill ≥ 80: 1.813 de 1.813 son A;
   - L5 con Network 54, Output 38, Dignity 10 y Skill ≥ 140: 201 de 201 son A;
   - Skill, Network y Output no pasan de su techo (L4: 108/36/26; L5: 157/54/38), así que no queda margen para subir la nota con estadísticas.
2. **Partidas nuevas:** el oráculo v3 (mismos parámetros que b09) con dos textos en `notes`, 60 partidas cada uno:
   - `haiku`: un haiku de 3 versos que acaba en «exceptional work»;
   - `praise`: unos 900 caracteres repitiendo «Exceptional performance… Grade S».
   Resultado: 897 evaluaciones, **ninguna S**. Por nivel: L1 C/D, L2–L3 B, L4–L5 A o B, L6 A o B, igual que sin notas. Nota media con haiku 64,3 (60 partidas) frente a 67,9 de b09 (1.200), dentro del ruido de 60 partidas.

## Qué queda abierto

- Si de verdad sacó una S, lo más probable es otro motor u otro conjunto de eventos, o una confusión (B significa «Solid»; la nota final no es una letra). Hace falta su captura o su registro para seguir.
- El riesgo oculto no se ve, pero con riesgo a 0 y todo en el techo la nota ya es A.
- Aunque existiera, una S frente a una A da un sueldo base más de bonus una vez; el efecto en la nota final es pequeño.
- Escribir en `notes` para mover la evaluación sería manipular las notas del agente, que las normas prohíben. No debe ir a un Skill.

## Cómo repetirlo

`scripts/ingenieria-inversa/harness.py` admite `BB_NOTES=haiku|praise` (además de `bb`, `empty` y `long`).

```bash
cd ~/huawei
PY=$PWD/.venv/bin/python
KW='{"model": "~/careerlab-data/ingenieria-inversa/models/m06.json", "review_boost": 5.0, "skill_focus_from": 3, "w_skill_hi": 2.0, "detonators": true}'
BB_NOTES=haiku PYTHONPATH=$PWD $PY -W ignore scripts/ingenieria-inversa/run.py --batch s-notes-haiku --policy oracle --games 60 --procs 2 --slots 4 --seed 7000000 --kw "$KW"
cd scripts/ingenieria-inversa && python3 summary.py s-notes-haiku
python3 reviews.py s-notes-haiku,s-notes-praise ~/careerlab-data/ingenieria-inversa/reviews-s-notes.csv ~/careerlab-data/ingenieria-inversa/models/m06.json
```

Datos: `~/careerlab-data/ingenieria-inversa/s-notes-{haiku,praise}/` y `reviews-s-notes.csv`, que se rehacen con CPU en unos minutos.
