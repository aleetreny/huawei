# Aprender de una ganancia que no aparece

**Con expectativas DeepSeek congeladas no aparece una mejora clara: exigir dos historias distintas cambia54,05→54,41; el aprendizaje se contamina cuando la expectativa de ganancia ya era falsa.** No admitir otro manual/partidas por este resultado.

Seis brazos fijados antes de ejecutar,600semillas nuevas por brazo (202680270+), mismo controlador observado con veto de riesgo y aprendizaje trimestral existente. El brazo nuevo compara el signo que esperaba de la opción elegida con su siguiente panel público, únicamente dentro del mismo mes y nivel. Una expectativa positiva seguida de cero suma evidencia de un posible techo; hacen falta1/2/3historias distintas. Una ganancia posterior por encima lo revoca. Todo se reinicia tras ascenso. No lee efectos verdaderos de opciones ni caps para decidir en los brazosDS. No usa memoria de otra carrera. Los caps verdaderos sólo clasifican errores a posteriori.

| Lecturas | Evidencias requeridas | Q réplica | Δ vs su control (IC95%) | Inferencias de historia/carrera | Inferencias falsas/carrera |
|---|---:|---:|---:|---:|---:|
| DS guardadas | Sin cambio |54,049|—|0|0|
| DS guardadas |1|53,787|−0,262[−1,569;1,044]|19,893|13,022|
| DS guardadas |2|54,412|+0,363[−0,722;1,447]|5,990|1,370|
| DS guardadas |3|54,436|+0,387[−0,546;1,319]|3,600|0,147|
| Signos perfectos, diagnóstico | Sin cambio |60,705|—|0|0|
| Signos perfectos, diagnóstico |2|62,600|+1,895[0,907;2,883]|6,093|0|

No son nuevas lecturas DeepSeek, aprendizaje nativo ni partidas oficiales. Son carreras de réplica condicionadas a dos lecturas guardadas. Los intervalos pareados sólo describen variación entre estas semillas. El diagnóstico con signos perfectos cambia la información y no acredita una política entregable. No sumar su ganancia con otros experimentos.

La distinción importa: **ver cero no permite identificar por sí solo un techo**. También puede significar que la opción nunca daba la ganancia esperada. Repetir una mala expectativa sobre varios eventos puede producir falsa confianza. Más evidencias reducen inferencias falsas, pero aquí tampoco producen un salto hacia75. El resultado no refuta toda actualización de creencias o una observación pública inequívoca de una inversión trimestral.

Datos numéricos completos comprimidos con hashes: [feedback-caps-screen.json](feedback-caps-screen.json), `.json.gz` enlazado dentro. Código: `scripts/deepseek/gpt_feedback_caps.py`. Verificación sintética: dos IDs distintos necesarios, falsa inferencia contabilizada, ganancia posterior revoca, transición de mes excluida. No se ejecutó modelo ni API.

## Relevo

Pantalla completa, ningún proceso pendiente. No seleccionar retrospectivamente2o3 y promoverlo. Reproducir sin API: `uv run python scripts/deepseek/gpt_feedback_caps.py --out /tmp/feedback-caps-screen.json`. La siguiente evidencia viene de las4carreras nativas ya anunciadas, que muestran el resultado real de inversiones y su posterior uso. No modificar sus Skills ni sustituir derrotas.
