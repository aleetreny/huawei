# Registro de progreso

**La investigación sigue abierta; no hay una solución validada para 75 consistente.** El detalle numérico se conserva en los resultados de cada experimento y el historial de Git permite reconstruir los checkpoints anteriores.

## Trabajo completado

Se revisaron las reglas, los resultados previos y las implementaciones públicas. Se reprodujo el asesor de las cinco trazas reales de DeepSeek y se separaron fallos de lectura, de control y de ejecución. Se completaron pruebas de autocomprobación, capacidad, contexto, feedback y representación numérica; ninguna justificó una nueva estrategia de partida.

La memoria de retornos registrados sí mejoró el controlador de réplica en dos muestras independientes de semillas. Se construyeron un lector del registro, una memoria aislada por sesión y paquetes que sólo incluyen acciones anteriores a la decisión. Sus pruebas no demuestran todavía una mejora con Sonnet o DeepSeek.

## Correcciones metodológicas

Un menú apareció en dos estados distintos. Se corrigió la identificación de las respuestas para vincularlas al panel completo, se conservaron las 62 lecturas existentes y se ejecutaron únicamente las dos que faltaban dentro del máximo original de 64.

Una revisión factual produjo una cita no literal. Se conservó la respuesta y se aplicó el fallback a la primera elección; no se reparó ni se repitió. La continuación quedó documentada antes de ejecutar los casos restantes.

La auditoría de Sonnet atribuyó inicialmente algunas acciones a menús trimestrales desactualizados. Se corrigieron mediante el registro oficial de la misma partida. Las tres reconstrucciones de Haiku no cambiaron; una sigue sin cumplir el criterio de fidelidad y no permite interpretar sus efectos contrafactuales.

Las pruebas de los modos locales tuvieron fallos de arranque en competición. Sus notas se describen sólo sobre partidas válidas, sin interpretar esa muestra incompleta como un efecto causal del modo.

## Relevo

La comparación emparejada de Sonnet terminó: 48 lecturas, sin mejora que justifique promover el paquete. No abrir más pruebas hasta terminar la limpieza de la PR solicitada por Alejandro. La descripción debe ser breve, en español y sin detalles de planes o hashes. Deben pasar los tests y la revisión de datos antes de sacar la PR de borrador.
