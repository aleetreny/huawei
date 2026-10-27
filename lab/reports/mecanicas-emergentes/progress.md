# Progreso

- Contexto leído y rama aislada creada. La investigación usa la réplica y catálogo ya publicados, sin acceso a internos del juego ni consumo de Claude/DeepSeek.
- Se fijaron E1–E4 antes de ejecutar nuevas simulaciones.

- Exploración 01: 400 semillas/brazo. Q base 70,94; riesgo recortado 71,70; retrasar cierre 70,93. La mejora del cierre no se sostiene. Se detectó un nombre incorrecto de campo de ascenso en el resumen, sin afectar Q/nivel; corregido para los lotes siguientes. E3/E4 se prueban como combinaciones de trimestre y mayor valor de habilidad acumulada.

- Se localizó fase 3 posterior en `origin/main-1nddsg@da81e4a`: catálogo v2, sampler por mes, política 72,39 real y M18–M23. Integrada sin conflictos en rama propia. Los screen-01/02 corresponden a v1 en memoria: sólo pilotos históricos. Toda confirmación se hará contra v2 y politica_optima.json, no contra la referencia superada.

- Confirmación chain6 (2.000 semillas nuevas) refuta la mejora inicial: −0,50 puntos vs base. Confirmación terminal_q (1.200 semillas nuevas) +0,445; terminal anticipatorio +0,505. E7 aumenta algo L7 pero reduce Q al insistir demasiado en Skill.
- Smoke oficial 4/4 completas, cero acciones rechazadas. Lote confirmatorio 600 partidas lanzado y aislado. Descubierta nómina terminal omitida por ambos generadores de réplica.
- Tests de la base integrando ramas: `uv run --no-sync pytest -q`, 309 passed. La auditoría de datos históricos encontró gzip cortado en c02 (ya documentado por su autor); se retienen sólo registros completos y se informa del corte.

## Cierre de validación
600 partidas oficiales terminadas; análisis final y evidencia portable guardados. Suite final: 306 tests pasan (una advertencia de Authlib). Los 40 primeros resultados de confirmación se reproducen exactamente después de la corrección de liquidación usando el modo histórico explícito. Informe y Relevo completos; publicación en rama propia y PR como último paso.
