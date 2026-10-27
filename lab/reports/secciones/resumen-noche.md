# Laboratorio nocturno por periodos (T18): resumen de la noche

Rama `alejandro/lab-secciones`, origen de registro `secciones`, actor Haiku de siempre (`claude-cli:haiku`, CLI 2.1.303). Empezó el 27 oct 2026 a las 00:27 UTC.

**Cómo leer las tablas.** Una partida corta se corta al llegar a un mes dado (actor `claude-cli:haiku^M`, herramienta en `careerlab/truncate.py`); nunca cuenta como terminada ni como eliminada y no tiene nota. La nota (Q) sólo sale de partidas completas. Error estándar (SE) de la media; intervalos de Wilson al 95 % para porcentajes. Cada comparación es contra una referencia jugada en el mismo lote, intercalada.

## Mejor estrategia por periodo

(se rellena durante la noche)

## Tabla viva de hipótesis

| Id | Periodo | Qué cambia | Partidas por brazo | Resultado | Decisión |
|---|---|---|---|---|---|
| [P1-base](p1-base.md) | P1 | 4 manuales: f3-lean (ref.), bb-mechanics-lean, bb-mechanics, observed-growth-v7 | 30 (6 meses) | 47 %, 50 %, 37 %, 40 % ascienden en la 1.ª; 52/52 en el umbral ascienden | ninguno distinto; f3-lean y bb-mechanics-lean a 15 completas |
| [H-P1a](p1-h1-clock.md) | P1 | + `review-clock` (calendario publicado, techos, no ceder N/O el mes previo) | 25 (2×2) + 25 (réplica) | sobre f3-lean: 54 % frente a 39 % (50 y 49 partidas); pérdidas en el mes 5: 0,34 frente a 0,63 por partida; sobre bb-mechanics: 44 % frente a 60 % | **prometedora**; se profundiza |
| [H-P1d](p1-h2.md) | P1 | + `cap-trade` (no comprar Dignidad llena a cambio de Network) | 25 | 40 % frente a 40 % | descartada |
| [H-P1c](p1-h2.md) | P1 | + `log-check` (leer el registro de efectos) | 25 | 36 % frente a 40 %; ~2 llamadas por partida | descartada |
| [P4-bots](p4-bots-cierre.md) | P4 | Defuse + recuperación en el último año (bots) | 200 bots | control de riesgo 65 ± 6 frente a 67 ± 5; nota igual | descartada |

## Revisión de las 2 horas (02:10 UTC)

**Qué he aprendido de la mecánica.**
- El ascenso de la 1.ª evaluación es un interruptor: 143 de 143 partidas que empezaron el mes 6 en el umbral ascendieron, y ninguna por debajo. Toda la varianza del P1 está en llegar al mes 6 sin perder un punto.
- Los puntos se pierden en el mes 5 (y algo en el 4) por respuestas de principios firmes o públicas que suben Dignidad (ya en 10) y cuestan Network, o que quitan tiempo a la entrega propia (Output). Siempre había otra respuesta que conservaba el punto.
- Haiku no sabe cuándo llega la evaluación ni reconoce el techo; si se le enseña a contar con el calendario publicado, lo hace y pierde la mitad de puntos en el mes 5. Las reglas generales sobre "ser discreto" (cap-trade) no cambian su elección.
- `check_latest_logs` enseña el efecto exacto de cada respuesta, pero Haiku apenas lo usa aunque se le pida.
- Con bots: limpiar riesgo "por si acaso" al final no sube el control de riesgo; lo que pesa es lo que crean las respuestas.

**Líneas que mato:** cap-trade, log-check, limpieza preventiva del último año.

**Dos ideas nuevas muy distintas:**
1. *Manual mínimo (G1)*: sólo f3-lean + el reloj en 150 palabras, para ver si DeepSeek (más débil) lo sigue mejor y ahorrar tokens.
2. *Proteger Skill desde L4 con el reloj de 6 meses*: en L4 la evaluación sólo mira la Skill; usar el mismo reloj para planear la Skill por semestre (cuántos meses quedan, cuánto falta por subir).

## Hipótesis descartadas

## Manual compuesto recomendado

## Relevo
