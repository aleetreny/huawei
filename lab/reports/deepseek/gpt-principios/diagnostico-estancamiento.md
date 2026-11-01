# Diagnóstico del estancamiento — 29 octubre 2026

**Conclusión: sí mejoró la eficiencia, pero no hay evidencia suficiente de mejora en juego; las carreras disponibles de cp no superan a v4, y la réplica no permite atribuir toda la diferencia al azar.**

Auditoría documental y recálculo local, sin llamadas a DeepSeek ni a otros modelos, sin partidas. Se integró origin/main en la rama de apoyo alejandro/gpt-principios antes de evaluar. Las modificaciones ajenas de harness.py y nota-s.md quedan fuera.

## Evidencia actual

Fuentes: score_report.json de lab/data/deepseek/partidas, comprobante.md, exploracion/README.md, scripts/exploracion/choice_model.py y HALLAZGOS C45–C67.

| Manual | Notas de juego con informe | Media | 0,8 juego + 0,1 fichas |
|---|---|---:|---:|
| t13-read-v4 | 71,67; 70,22 | 70,945 | 63,108 |
| cp-v5a | 66,27; 65,10; 68,13 | 66,500 | 62,658 |
| cp-v7 | 62,25; 69,88; 28,56 | 53,563 | 50,826 |
| cp-v10 | 22,98; 61,24 | 42,110 | 41,188 |
| cp-v11 | 25,75 | 25,750 | 25,600 |
| cp-v12 | 56,80; 62,83 | 59,815 | 57,852 |

Se incluyen eliminadas con informe; no se imputa nota a las interrumpidas. La tercera de v4 quedó sin informe en L1, mes 22: no prueba una derrota, pero tampoco permite tratar las dos completas como media representativa. Las cifras son descriptivas, con muestras pequeñas y sin emparejamiento; no prueban regresión causal. Falta sumar 0,1 × calidad oficial, desconocida para estas versiones. Eficiencia reconstruida como max(0,min(100,(3M−tokens/mes)/2,5M×100)), limitada a 50 si no termina. Se usaron los meses del score_report, no el estado 49 del CSV.

El registro del corte 1 en HALLAZGOS C45 da 64,75 y puesto 13, top 10 en 68,17: es una fotografía guardada, no una consulta nueva de la clasificación. Sin desglose oficial no se puede deducir exactamente la media de juego ni afirmar que hubo un hundimiento.

## Por qué no aparece la mejora

1. **Muestra de referencia seleccionada y escasa.** Dos carreras buenas fijaron una expectativa de ~71; no conocemos la esperanza de v4 con esa precisión. Tampoco hay base para afirmar que los cinco puntos perdidos por cp son sólo azar.
2. **Se optimiza una palanca que pesa 10 %.** Pasar de eficiencia 63,52 a 100 suma 3,65 a igualdad de juego. Perder 4,56 de juego lo cancela. cp-v5a pierde 4,445 de juego frente a las dos completas de v4 y casi compensa con fichas; cp-v12 pierde 11,13 y no compensa.
3. **El error caro sigue en historias críticas.** La auditoría de Exploración encuentra 26 pérdidas de N/O entre 120 decisiones previas a evaluación de L1; 10 tenían alternativa segura sin pérdida y 16 no. Por tanto hay tanto errores evitables como intercambios reales: ni reescribir todo ni exigir riesgo cero resuelve ambos.
4. **Una regla correcta puede operar sobre una lectura equivocada.** La lista de señales de riesgo confunde privacidad o demora con ocultación. Relajarla globalmente ya produjo regresiones; la hipótesis útil es distinguir reparación discreta de ocultación por evidencia del texto actual, y sólo en el contexto donde aporta.
5. **La réplica es predictiva, no un ensayo de nuevos textos.** choice_model.py usa efectos y riesgo verdaderos como rasgos, además de lecturas, y separa partidas para validación. Ese 87 % mide imitación en situaciones del mismo entorno; no demuestra transferencia a títulos inéditos, proveedor nuevo ni política textual nueva. Los errores del 13 % restante pueden concentrar casi todo el coste. Cambiar pesos a mano no acredita que un Skill provoque ese cambio.
6. **Se mezclaron factores.** cp incorpora redacción, memoria, trimestres, rescate y protocolo. La comparación agregada de familias v4/cp no identifica el efecto de cada pieza. ex-v1 añade cambios de trimestre, salud y texto de rúbrica: es una apuesta fundada, aún sin mejora real confirmada.

## Vías prioritarias sin DeepSeek

### 1. Control limpio para saber qué estamos comparando

Conservar como referencias separadas v4 literal, cp-v12 y ex-v1. Antes de crear otro candidato, preparar una especificación de v4 con sólo el bucle validado (sin cambiar política, memoria ni trimestral). No asumir que hereda eficiencia o juego medidos: sería un control nuevo. Permite separar mejoras de ejecución de cambios de estrategia en una futura prueba autorizada. Hoy sólo comparar archivos y trazas existentes.

### 2. Auditar el coste de las discrepancias, no el porcentaje de coincidencia

Construir con datos pagados un conjunto de decisiones críticas por historia completa: pérdidas evitables de Output/Network, falsas alarmas de riesgo, riesgos reales aceptados y pérdida de ventanas de ascenso. Reservar títulos completos para evaluación, agrupar incertidumbre por partida/título y separar proveedor. Puntuar pérdidas evitables y riesgos graves, además de acierto global; mantener controles de salud y crisis. Primero comprobar que ex-v3 mejora ese subconjunto con evidencia ya disponible de Sonnet y que no reincide en v9. Un revisor genérico o memoria de resultados ya fracasaron: no repetirlos sin una hipótesis distinta.

### 3. Usar ex-v1 como mejora incremental, no como salto demostrado

Es el candidato más concreto ya construido: +1,8 de juego en réplica y +8,5 de calidad media de jueces (77,5 frente a 69). Si ambos trasladaran íntegros, serían ~2,29 de nota total sobre cp-v12, no +10. La calidad oficial y la obediencia real siguen pendientes. Mantener ex-v3 separado: su +0,3 simulado y el banco Sonnet son indicios, no autorización para relajar globalmente el riesgo.

### 4. Validar el simulador justo donde decide la recomendación

Antes de nuevas búsquedas, contrastar fuera de muestra las ventanas de ascenso, pérdidas de N/O y crisis por familia. La tabla publicada predice L6 en 13 % frente a 0 de 14 carreras reales completas: no basta para refutarlo (0,87^14 ≈ 14 %), pero impide vender una calibración perfecta. Hacer validación por títulos y familia, además de partidas; mantener aparte error de simulación y error de estimar comportamiento. Las 4.000 semillas reducen ruido Monte Carlo, no incertidumbre de los pocos juegos que ajustaron el modelo.

## Qué dejaría de hacer

Más versiones por estilo, nuevas arquitecturas de script sin una función concreta que gane, optimizar fichas más allá de 100 y escoger por la mejor carrera. Tampoco tomar 72,4 como máximo matemático: es el mejor planificador medido, no una prueba de optimalidad (A5 lo aclara; B31 usa un lenguaje demasiado fuerte).

## Relevo

Hecho: lectura de estado y normas vigentes tras sincronizar, contraste de Comprobante/Exploración, inspección del modelo de elección y recálculo de juego+fichas desde informes primarios. No se modifican manuales ni scripts; no se usan APIs. Resultado: eficiencia sí, mejora de juego no demostrada; tabla y prioridades anteriores.

Pendiente: no se ejecutó la auditoría exhaustiva por decisiones ni nuevos bancos; el encargo es diagnóstico y vías de mejora. Cualquier prueba futura con DeepSeek requiere autorización nueva: el usuario lo ha prohibido en esta sesión.

Para continuar sin API: leer este informe, exploracion/README.md y scripts/exploracion/choice_model.py; usar lab/data/deepseek/decisiones.csv.gz y los score_report.json. Separar títulos al diseñar la evaluación. No ejecutar bench.py, turnprobe.py ni final_eval.py por inercia (no hacen falta para este diagnóstico).

Documentar en README y ESTADO, comprobar git diff --check, commit/push sólo de estos documentos en alejandro/gpt-principios y solicitar integración en main. No se añaden conclusiones al registro global de hallazgos antes de revisión.
