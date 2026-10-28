# Reconstrucción de los trimestres

**Cambiar los trimestres de un camino fijo no demuestra una mejora del agente completo.**

En la primera carrera de Haiku, el baseline de 65,71–65,93 no reproduce suficientemente el 66,86 real: sus diferencias contrafactuales quedan excluidas. La segunda reproduce el despido y no se rescata cambiando el trimestre. La tercera reproduce aproximadamente 64,15 y llega a 70,47–70,70 al cambiar la gestión trimestral, conservando una explosión.

Se mantienen las historias y respuestas reales; los controladores no reciben las historias futuras para elegir. Un agente que volviera a jugar podría cambiar sus respuestas al cambiar el estado, por lo que estos resultados no son una previsión de nota. Los caminos rescatados sin continuación observada quedan sin puntuar.

La alineación posterior con registros oficiales no corrigió ninguna atribución de las tres carreras de Haiku. En Sonnet sí se corrigieron 12 atribuciones trimestrales; su baseline reproduce 49,95, pero las alternativas no lo llevan a 75.

## Evidencia y relevo

Los detalles numéricos y criterios se conservan en [native-quarter-replay-aligned.json](native-quarter-replay-aligned.json) y en los archivos relacionados de esta carpeta. Los originales con narrativas permanecen fuera de Git. El historial de commits conserva las versiones extensas anteriores de este informe.

No repetir las colecciones terminadas ni presentar estos resultados como una solución para 75 consistente. Consultar el [Relevo principal](README.md#relevo) antes de continuar.
