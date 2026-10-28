# Calidad de los SKILL.md (10 % de la nota automática)

**Conclusión en una frase:** __CONCLUSION__

Línea abierta el 28 oct 2026. Pregunta: *¿cuánto saca nuestro SKILL.md en la nota de calidad y cómo subirla sin cambiar cómo juega DeepSeek?*

## 0. Lo que dicen las normas

- La nota automática de cada versión es 0,80 × partidas + **0,10 × calidad de los documentos** + 0,10 × fichas (`competition-rules.rst`).
- Cada `SKILL.md` se puntúa de 0 a 100 «como instrucciones para el agente», y la nota es **la media de los Skills** de la entrega. Los documentos de `design/` no cuentan aquí; sólo los lee el jurado.
- Una nota alta exige:
  - que el agente encuentre el Skill y sepa cuándo usarlo (descripción);
  - pasos ejecutables, con prioridades y criterios, y qué hacer cerca de un límite;
  - una estrategia que encaje con las reglas publicadas y mire los 48 meses;
  - que siga valiendo si cambian la redacción o el orden de los eventos.
- **Nota 0** si:
  - falta el *front matter* o es inválido;
  - el Skill está vacío o no tiene que ver con su descripción;
  - contradice el juego;
  - contiene conducta prohibida, como una respuesta fija para un evento con nombre.
- No se publica qué modelo puntúa. **No tenemos la nota de calidad del corte 1.**

**Cuánto vale:** 10 puntos de calidad son 1 punto de nota automática. Para sacar lo mismo jugando harían falta 1,25 puntos más de media en las partidas.

## 1. El juez

`scripts/calidad-skills/judge.py` le pasa a un modelo de Claude, por la CLI:
- la rúbrica oficial literal;
- las reglas publicadas (`handbook.rst`, `rules.rst`, `failure-and-ending.rst` y la parte de contenidos prohibidos de `competition-rules.rst`);
- el SKILL.md.

Pide una nota de 0 a 100, ocho subnotas de 0 a 10, las condiciones de nota 0 que vea y las tres debilidades que más restan. Es un **sustituto para comparar versiones**, no la nota oficial. Trabajo previo con un revisor de Sonnet: [transmision/fase3-rubrica.md](../transmision/fase3-rubrica.md) y [palancas/nota-memoria.md §6](../palancas/nota-memoria.md) (ruido de ±6 con 3 lecturas).

### Calibración (`data/j01-calibracion.jsonl`, 90 lecturas, Haiku y Sonnet × 3)

__TABLA_J01__

- **Los dos jueces ordenan igual los manuales.** Los largos y estructurados (t13-read, f1) sacan 60–70; los cortos sin pasos ejecutables (p0-minimal, native-craft), 14–43.
- **Aplican las condiciones de nota 0:**
  - una respuesta fija para un evento inventado saca 0 en las 6 lecturas;
  - una regla que contradice el manual publicado, 0–22;
  - la plantilla vacía, 0–3.
- **Un umbral de ascenso sin publicar presentado como regla no siempre va a 0:** se castiga hasta ~40, y sólo 1 de cada 6 lecturas lo pone a 0. El juez oficial puede ser más severo: no hay que arriesgarse.

## 2. Nuestro manual entregado y sus reescrituras

`data/j02-reescritura.jsonl`: Haiku y Sonnet × 3 y Opus × 2 por versión, en la misma tanda.

__TABLA_J02__

Qué cambia cada versión (todas en `lab/policies-src/calidad/`; ninguna añade una regla de historias):
- **v4-c1:** sólo arregla redacción.
  - Las pistas de lectura pasan a ser «nuestros supuestos de trabajo», no reglas del juego.
  - N = 1 se llama siempre «el último mes antes de una evaluación» (v4 lo llamaba también «el mes de la evaluación»).
  - Se separan las acciones de energía de las principales: v4 ponía «Repair a key relationship», que es principal, en una lista de energía.
  - Se aclara la energía del último trimestre (v4 listaba más de 3 puntos).
  - Se añade un resumen de los 48 meses y se explica para qué sirve la línea de estado y cómo rehacerla si se pierde.
- **v4-c2:** c1 más límites concretos.
  - Margen propio declarado para Health y Dignity: «4 o menos, no es un límite publicado».
  - Qué hacer con Wealth bajo cero y con Network a cero, que son rutas de derrota publicadas.
- **v4-c3:** c2 reestructurado por Sonnet con las decisiones congeladas.
- **v4-c4:** c2 con la línea de estado en un segundo Skill.

## 3. ¿Cambia lo que elige el modelo? (banco)

__BANCO__

## 4. Qué hacer con los 3 USD de DeepSeek

__DEEPSEEK__

## 5. Conclusiones

__CONCLUSIONES__

## Archivos

| Archivo | Qué hace |
|---|---|
| `scripts/calidad-skills/judge.py` | juez con Claude (Haiku, Sonnet, Opus) sobre la rúbrica oficial |
| `scripts/calidad-skills/ds_judge.py` | el mismo juez con DeepSeek, con tope de gasto propio (sólo en el Mac de Alejandro) |
| `scripts/calidad-skills/summary.py` | tabla de notas, subnotas y condiciones de 0 |
| `lab/reports/calidad-skills/calibracion/` | casos trampa del juez (nunca se entregan) |
| `lab/reports/calidad-skills/data/` | juicios en JSONL (sin texto del juego) |
| `lab/policies-src/calidad/` | reescrituras de `t13-read-v4` |

## Relevo

__RELEVO__
