# Mecánicas emergentes — 27 octubre 2026

Objetivo solicitado: descubrir y comprobar al menos un patrón útil nuevo, partiendo de los últimos experimentos.
Rama propia `alejandro/mecanicas-emergentes`, base `4cec65d` (incluye réplica, M1–M17 y T20). No editar el plan global.

## Fases
1. [x] Leer ESTADO, H1–H25, M1–M17, T18/T20 y código de la réplica.
2. [ ] Formular y probar intervenciones aisladas en la réplica.
3. [ ] Confirmar la mejor hipótesis en semillas nuevas y, si procede, bots por las cinco herramientas oficiales.
4. [ ] Informe con incertidumbre, artefactos reproducibles y principios generales; tests; commit, push y PR.

## Hipótesis escritas antes de simular
- E1: el planificador premia reducir riesgo incluso cuando ya está en cero. Corregir esa valoración podría liberar decisiones para crecer sin más explosiones (no cambia el motor).
- E2: el cierre desde el mes 46 abandona una evaluación que aún puede dar un ascenso en el mes 48. Mantener la preparación de esa evaluación y cerrar después podría mejorar nivel y nota.
- E3: planificar conjuntamente energía y acción principal evita gastos redundantes y puede usar recuperación/aprendizaje como combinación, en vez de comparar cada acción por separado.
- E4: valorar la habilidad por encima del mínimo antes del ascenso podría acelerar el ascenso siguiente; probar sólo tras evaluar E1–E3.

Exploración: brazos base y cambios aislados; 400 semillas por brazo. Selección por nota media incluyendo derrotas. Confirmación: semillas nuevas, diferencia y IC 95%, sin seleccionar de nuevo. Réplica no equivale a motor oficial: confirmar por MCP la intervención ganadora si muestra valor. No IA ni API de pago. No leer internos del motor.

## Errores y límites
- `/goal` ya había creado el objetivo; no se creó un duplicado.
- Fetch completo devuelve colisión macOS `Matteo`/`matteo/*`. Las ramas de interés sí se actualizaron; no se modifica ninguna referencia ajena.
- El primer estado local estaba >100 commits atrasado; se tomó la rama más reciente que incorpora la réplica, no main antiguo.
