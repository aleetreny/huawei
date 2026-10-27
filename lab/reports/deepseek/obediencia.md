# Obediencia: el banco oficial con DeepSeek, sin manual y con t13-final

**Conclusión.** DeepSeek lee el Skill siempre y obedece el reparto trimestral de `t13-final` casi como Haiku (Skill en L4: del 2 % al 65 %; comentario de RR. HH.: del 15 % al 65 %). Al contrario que con Haiku, **el manual también le mejora las historias del bloque general** (pérdida −0,79 puntos por decisión, intervalo −1,62 a −0,16). El único empeoramiento está en los detonantes (+0,95, al límite de ser seguro).

27 oct 2026, rama `alejandro/deepseek`. Scripts `scripts/deepseek/bench.py` (bucle de agente), `obedience.py` (informe) y `paired.py` (comparación emparejada).

## Montaje

- **Forma oficial**, como el banco de Haiku (`scripts/transmision/runbench.py`):
  - mensaje de sistema con la identidad oficial (`IDENTITY.md`) y la sección de Skills de JiuwenSwarm (nombre y descripción);
  - mensaje de usuario con el mensaje oficial de continuación;
  - herramientas: las 5 del juego y `skill_tool`, con los mismos nombres, descripciones y esquemas; el cuerpo del SKILL.md sólo llega si DeepSeek lo pide.
- **Contexto:** el agente juega desde el principio del mes; las decisiones anteriores del mes se reproducen tal como se grabaron, y la última es la que se puntúa.
- **Modelo:** `deepseek-v4-flash` con la clave de la competición, temperatura 0,95 como en JiuwenSwarm, razonamiento por defecto, sin fijar proveedor.
- **Situaciones:** 40 decisivas por regla de `ids-V2.txt` (con respuesta de Haiku sin manual y con t13-final o t10) más las 139 del bloque general `ids-G1.txt`. Son 459 en total; 132 de G1 cuentan como "general", junto con las 40 de V2.
- **Puntuación:** la de `scripts/transmision/score.py` (acierto según el simulador o la acción de la regla; pérdida = nota final perdida frente a la mejor opción).
- **Coste:** 0,0010 USD por situación sin manual y 0,0017 con t13-final; 1,20 USD los dos brazos (más 0,03 del piloto).

## Resultados

Comparación emparejada (las mismas situaciones; intervalo al 95 % por remuestreo). Acierto y pérdida, de "sin manual" a "t13-final":

| Regla | n | Acierto | Δ acierto | Pérdida (puntos) | Δ pérdida | Misma elección |
|---|---:|---|---|---|---|---:|
| Mes previo a la evaluación | 43 | 88 % → 88 % | +0 (−7 a +7) | 1,05 → 1,01 | −0,03 (−0,67 a +0,57) | 93 % |
| Skill en L4 (trimestre) | 40 | 2 % → **65 %** | +62 (+48 a +78) | 0,12 → 0,22 | +0,10 (−0,03 a +0,28) | 10 % |
| Comentario de RR. HH. (trimestre) | 40 | 15 % → **65 %** | +50 (+35 a +65) | 0,48 → 0,18 | −0,30 (−0,75 a −0,02) | 28 % |
| Detonantes | 43 | 88 % → 81 % | −7 (−16 a +0) | 1,21 → 2,16 | **+0,95** (−0,00 a +2,45) | 88 % |
| Ruina temprana | 41 | 41 % → 49 % | +7 (−2 a +17) | 1,14 → 0,99 | −0,15 (−0,48 a +0,14) | 83 % |
| Cierre | 40 | 60 % → 78 % | +18 (+0 a +35) | 0,43 → 0,30 | −0,12 (−0,32 a +0,09) | 35 % |
| Salud baja | 40 | 70 % → 85 % | +15 (+0 a +30) | 1,58 → 0,56 | −1,01 (−3,36 a +0,24) | 75 % |
| **Historias del bloque general** | 172 | 73 % → 76 % | +2 (−2 a +7) | 1,39 → **0,60** | **−0,79 (−1,62 a −0,16)** | 87 % |
| Todo | 459 | 61 % → 74 % | +14 (+9 a +18) | 1,06 → 0,72 | −0,34 (−0,74 a −0,01) | 70 % |

**Haiku con las mismas reglas** (t10-countdown, mismo banco, 2.215 situaciones): Skill en L4 del 14 % al 77 %, RR. HH. del 18 % al 60 %, bloque general −0,34 (−0,83 a +0,08), detonantes +0,18.

**DeepSeek sin manual frente a Haiku sin manual** (mismas situaciones): DeepSeek acierta más en el mes previo a la evaluación (88 % frente a 81 %; pérdida 1,05 frente a 1,58) y menos en las reglas trimestrales que nadie le ha dado (Skill en L4: 2 % frente a 15 %).

**Lectura del Skill.** DeepSeek lee SKILL.md en el **100 %** de las situaciones con manual. La referencia del mes de evaluación (`reference/review-month.md`) la abre en el 100 % de los meses previos a una evaluación (cuenta atrás N = 1), pero **también en un 9–26 % de los demás meses** (Haiku sólo la abría en el suyo). Sin manual, consulta el registro en el 100 % de las situaciones y el manual del empleado en un 9 %.

**Huella en el bloque general** (efecto medio de las opciones elegidas en 139 historias de los meses 1–44):

| Brazo | Skill | Network | Output | Health | Dignity | Riesgo | Igual que el control |
|---|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek sin manual | +0,88 | +0,71 | +0,08 | −0,11 | +0,99 | −0,14 | — |
| DeepSeek t13-final | +0,70 | +0,76 | +0,22 | −0,12 | +0,96 | −0,14 | 87 % |
| Haiku sin manual | +0,82 | +0,53 | +0,09 | +0,01 | +1,09 | −0,19 | 86 % |
| Haiku t13-final | +0,74 | +0,72 | +0,16 | −0,10 | +0,99 | −0,13 | 81 % |

| DeepSeek sin manual, repetido | +0,88 | +0,73 | +0,08 | −0,06 | +0,99 | −0,19 | 91 % |

**Control repetido.** DeepSeek sin manual coincide consigo mismo en el 91 % de las historias del bloque general (Haiku, 96 %): la temperatura 0,95 cambia una de cada once. `t13-final` coincide con los dos controles en el 87–88 %, así que **el manual cambia 3–4 historias de cada 100 más que el ruido**, siempre hacia menos Skill y más Output (el control repetido no se mueve: Skill +0,88, Output +0,08).

Frente al control repetido, la pérdida en el bloque general (132 historias de G1) baja de 0,96 a 0,56: −0,40 (−1,06 a +0,03). Entre los dos controles la diferencia es −0,10 (−0,42 a +0,16). **La mejora en historias es probable, pero no segura** con este tamaño.

## Lo que significa

- El manual de la línea de transmisión **se transmite a DeepSeek**: lo lee, obedece el reparto y no le estropea las historias. Probablemente se las mejora un poco, aunque las aparte algo de Skill.
- Los **detonantes** (riesgo ya cargado) son el único punto donde el manual empeora. Es la misma señal pequeña que con Haiku, y el siguiente sitio donde mirar.
- La cuenta atrás no aísla la referencia tan bien como con Haiku: DeepSeek la abre de más. No se nota en la pérdida, pero cuesta tokens.
