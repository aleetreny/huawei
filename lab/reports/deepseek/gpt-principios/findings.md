# Evidencia inicial
- Reglas locales: automated = .8 Q + .1 diseño + .1 eficiencia; Q es media de tres. 75 final con diseño/eficiencia perfectos requiere Q=68.75; 75 Q es otro objetivo.
- Investigación recuperada sin commit: phase-1/2 y screen/confirmation/contract en independent-designs/principles-evidence; script gpt_principios.py. Son evidencia por auditar, no experimento ejecutado en esta continuación.
- Dos fracasos DeepSeek históricos no prueban techo del modelo; revisión de trazas apunta a retención pre-evaluación y prioridades además de percepción.
- Exa encontró la competición china CareerSim-BDCI26: reglas difieren (allí aparece team); no transferir sin verificar.
- GitHub encontró Kingjinsight/TechArena-UK-2026, candidato relevante por inspeccionar.

## Barrido público
Consultados Exa (reto, leaderboard y 0.75), búsqueda GitHub de Career Survival, TechArena 2026, techarena-career y JiuwenSwarm career. La búsqueda de código del conector devolvió vacío; gh api se usa para listar rutas públicas y el conector para leer archivos.
- RAI-Internal es el runner oficial; Sherlock-shy no mostró paquete participante en main.
- Kingjinsight tiene preliminary con tres Skills; ShriyaSaxena tiene preliminary con tres Skills y plantilla; YuLong111 tiene un Skill. Ninguno identificado como equipo del 0.75.
- Portal Hydro sólo devuelve shell sin ranking mediante extracción; no hay puntuaciones verificadas.
- Documentación oficial online confirma 80/10/10 y DeepSeek v4 flash, agent único. La competición china no sirve como prueba de la UK.

## Skills públicos leídos
Kingjinsight (tres), ShriyaSaxena (tres), YuLong111 (uno): versiones preliminares públicas; sin score ni demostración de 75 en las rutas inspeccionadas. Son guías generales de supervivencia/crecimiento, no hay evidencia de algoritmo secreto. Kingjinsight usa filtro de integridad antes de crecimiento; todos usan realimentación y memoria breve. No copiar su contenido ni sus hipótesis como hechos. Rutas y SHA se registrarán en public-search.json.

## Próxima falsación
La conclusión de insuficiencia de percepción depende de cómo se combinan lecturas y estado. Probaré desacuerdo entre las DOS lecturas DeepSeek ya guardadas como señal de incertidumbre: veto conservador conjunto de riesgo y pérdidas frente a una lectura elegida, con mismos controles trimestrales. No requiere llamadas nuevas ni rediseñar otra taxonomía. Separar efecto de veto y uso de segunda lectura.

## Ranking comprobado en navegador
27 oct, ~18:58 UTC: https://techarena-uk.hydro.ac/contest/6aad0b0020562bf065d1654f/scoreboard muestra 0 y — en Cut-off 1/2 en todas las filas visibles (incluido Gradient Depression). No hay score oficial de 75 corroborado allí. No registrar nombres/datos de participantes innecesarios.

## Incertidumbre, pantalla de 600 semillas
Q observed 47.83, hard_risk 51.92, dual_risk 52.95, dual_average 51.80, dual_pessimistic 50.82, dual_loss 50.76. No hay salto grande; intervalo dual_risk vs hard_risk por calcular en informe. La cautela de todos los signos sacrifica promociones. No pasar esta vía a API ni afirmar 75.

## Aclaración del usuario
El 0.75 significa nota DE PARTIDA estable con DeepSeek; no nota total. Objetivo Q≈75 consistente. La descomposición 80/10/10 NO explica lo observado.

## Contraste con registros reales
Deduplicación por job_id de lab/registry*/**/{actors,policies,evaluations}.jsonl: t13-final Haiku official n12, Q57.24, completadas10 con media64.53; f3-lean official n43, Q50.52, completadas30 media60.37. Ninguna Q>=75 en esos dos grupos. Por tanto evitar derrotas no alcanza: también falta calidad entre carreras completas. Buscar no sólo supervivencia.

## Nuevo control barato antes de gastar proxy
Contrastar planificación CONJUNTA de todas las acciones trimestrales frente a elección codiciosa, bajo las mismas percepciones congeladas. Es una intervención sobre ejecución/uso de efectos conocidos, no otra taxonomía. Riesgo y supuestos visibles iguales; no emplear caps verdaderos en la planificación. Si falla, no pasar a Haiku.

## Falsaciones adicionales
- Plan trimestral conjunto con el mismo valor miope: 400 semillas, 55.46→52.76; salud falla6→41. Optimizar más exactamente un objetivo miope puede empeorar; no refuta planificación conjunta con otro objetivo.
- Preferencia bienestar +5 desde L3/4/5/6: 800 semillas, control53.69; L3 52.49, L4 53.07, L5 53.70, L6 53.68. No arregla 75. No gastar Haiku en estos candidatos.
- Recuperación: cuatro brazos x300 semillas de confirmation reproducidos fila a fila con script actual. screen/confirmation no guardaban hash del script; auditoría recupera evidencia sin fingir trazabilidad perfecta.
- Motor M17/M21: política llamada “óptima” es búsqueda de60 configuraciones; 360 partidas reales media72.39, mediana74.9. No hay prueba de optimalidad global. No asumir imposible75 porque un planificador se queda en72.

## Resultado final del margen observado
2000 semillas:48.8296→51.3717; veto52.9887. El margen no mejora el veto. No proponer otra Skill ni partidas Haiku desde esta pantalla. El valor del factorial es mostrar interacción representación/control, no dar por resuelta la transferencia.
