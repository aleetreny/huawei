# Fase 2. Cuánta nota vale cada punto de obediencia

27 oct 2026. Dos estimaciones con el simulador validado (`replica.py`, planificador ajustado) y una comprobación en partidas.

## 1. Pérdida por decisión × decisiones por partida

La pérdida de cada elección del banco ya está en puntos de nota final: es la nota media que se pierde frente a la mejor opción si después se juega bien. Multiplicada por cuántas situaciones decisivas de cada regla salen en una partida (partidas grabadas de bots: candidatas por partida × fracción decisiva), da lo que vale la regla en una partida. Con los números de la validación final ([validacion-final.md](validacion-final.md)):

| Regla | Situaciones decisivas por partida | Pérdida por decisión: control → t10 | Puntos por partida |
|---|---:|---|---:|
| No ceder puntos antes de la evaluación | 3,7 | 2,05 → 1,56 | **+1,8** |
| Skill en L4 | 6,3 | 0,23 → 0,21 | +0,1 |
| Comentario de RR. HH. | 3,9 | 0,43 → 0,30 | +0,5 |
| Detonantes | 4,7 | 0,51 → 0,70 | −0,9 |
| Ruina temprana | 0,4 | 1,57 → 1,40 | +0,1 |
| Cierre | 2,9 | 0,33 → 0,20 | +0,4 |
| Salud baja | 1,2 | 1,05 → 0,94 | +0,1 |
| Historias fuera de las reglas | ~22 | 1,15 → 1,11 | +0,9 |
| **Total** | | | **≈ +3** |

**Límite de esta cuenta:** supone que después de cada decisión se juega bien. Un sesgo que se repite en todas las historias (menos Skill en cada una) apenas cuesta en una sola decisión y mucho en una partida. Por eso esta cuenta no vio el hundimiento de t3-instr (−12 puntos en partidas). La huella del bloque general ([bloque-general.md](bloque-general.md)) es el aviso para ese caso.

## 2. Obediencia parcial en el simulador

`scripts/transmision/simvalue.py`: el planificador (71,1 ± 0,5 de nota en 400 partidas) obedece una regla con probabilidad p; si no, hace lo que hace Haiku sin Skill en el reparto (acción principal Apply for a key project, energía a recuperar o Network) o elige la historia al azar.

| Regla | Pérdida con p = 0,5 | Pérdida con p = 0 |
|---|---:|---:|
| Antes de la evaluación | 14,0 | 33,5 |
| Skill en L4 | 0,3 | 0,6 |
| Comentario de RR. HH. | 0,8 | 1,3 |
| Detonantes | 24,2 | 40,1 |
| Ruina temprana | 17,5 | 41,6 |
| Cierre | 3,0 | 8,9 |

En el reparto trimestral (Skill en L4, RR. HH.) cada punto de obediencia vale **unas centésimas de punto de nota**; en las historias, **décimas** (y el azar es mucho peor que Haiku, que acierta 54–91 % sin Skill). Es decir: **donde un manual manda (el reparto) es donde menos nota hay; donde está la nota (las historias) es donde un manual apenas manda.**

## 3. Partidas

Con 10–30 partidas por brazo, t10 (+3 estimados) queda a −1,8 ± 7,1 de f3-lean en partidas (49,0 frente a 50,8). La diferencia esperada está por debajo de lo que se puede distinguir con este número de partidas (hacen falta ~80 por brazo para 5 puntos). El lote `g6-full` añade 30 por brazo.
