# Experimento 9. Fase 3: escribir para la rúbrica sin cambiar lo que hace el modelo

27 oct 2026, 13:35–15:00 UTC.

## Revisor de rúbrica

`scripts/transmision/rubric.py`: Sonnet recibe el texto oficial de la rúbrica (*Document design quality score* y las reglas de conducta de `competition-rules.rst`), el manual del empleado y un SKILL.md, y devuelve una nota de 0 a 100 con puntos débiles y arreglos. 2–3 pasadas por versión.

| Versión | Nota del revisor | Qué cambia |
|---|---:|---|
| t3-instr (todas las reglas) | 60 (58, 62) | — |
| t9-quarter (sólo reparto) | 58 (58, 58) | sin guía de historias; números como umbrales |
| t11-final | 74 (74, 74) | t10 reescrito: qué decide el Skill y qué no, los 48 meses de un vistazo, aritmética de la energía, tres bandas del comentario de RR. HH., márgenes propios marcados como tales (“our safety margin, not a published limit”), rutas de derrota publicadas |
| t12-final | 72 (72, 72) | + línea tras una evaluación floja; “en nuestras partidas…” (el revisor lo marca como dato de desarrollo) |
| **t13-final** | **73 (72, 72, 74)** | t12 con el nivel alto y el comentario de RR. HH. explicados desde el manual y las charlas |

Lo que el revisor sigue pidiendo y **no** se añade: guía general para las historias. El banco demuestra que cualquier texto de ese tipo cambia 1 de cada 5 historias y empeora las partidas ([bloque-general.md](bloque-general.md)). Es un conflicto real entre la rúbrica (10 %) y la nota en partida (80 %); se resuelve a favor de la partida y se explica en el propio Skill (“This Skill only adds a review countdown…”).

## ¿Cambia el comportamiento? (banco)

| Brazo | Igual que el control en historias (bloque general) | Antes de la evaluación (132): acierto, pérdida | Detonantes (158) | Cierre (20) |
|---|---:|---|---:|---:|
| t10-countdown | 81 % | 62 %, 2,31 | 87 % | 90 % |
| t13-final | 81 % | 68 %, 1,70 | 85 % | 85 % |

Misma huella y mismos aciertos dentro del ruido: la reescritura para la rúbrica no cambia lo que hace Haiku. **t13-final es el manual recomendado** (carpeta [t13-final](../../policies-src/transmision/t13-final/)); juega en el lote `g6-full`.

## Percepción en el mes previo a la evaluación (t14, resultado negativo)

En las partidas, los despidos vienen de perder un punto de Network u Output en el mes previo aunque se aplicó la regla: Haiku no ve que “dar una B justa a un amigo” o “responder con poca implicación a quien pide ayuda” cuesta Network. t14 añade a la referencia (a) calibrar con `check_latest_logs`, que enseña el efecto exacto de las decisiones anteriores de la propia partida, y (b) más señales de coste de Network.

| Brazo | Situaciones `pre_review` (132): acierto | pérdida | pierde un punto necesario | mira el registro |
|---|---:|---:|---:|---:|
| control | 61 % | 2,32 | 31 % | 1 % |
| t13-final | 68 % | 1,70 | 21 % | 0 % |
| t14-final | 68 % | 1,80 | 20 % | **96 %** |

Haiku obedece la orden de mirar el registro (anoche casi nunca lo usaba porque nadie se lo pedía en el momento justo), pero eso no mejora la elección. El límite está en leer el efecto oculto de una opción nueva a partir de su texto, no en la información disponible.
