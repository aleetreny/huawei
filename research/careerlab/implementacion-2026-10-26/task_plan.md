# Plan: laboratorio adaptativo y presupuesto del objetivo

Solicitud de Alejandro: implementar las mejoras del diagnóstico sobre la estructura existente, gastar con prudencia la clave limitada de DeepSeek y evaluar críticamente autoresearch de Karpathy. Rama `alejandro/laboratorio-adaptativo`; base `b288805`.

## Alcance y contrato

- Desarrollo y pruebas aislados; la nube sigue siendo quien ejecuta partidas. No iniciar llamadas facturables aquí.
- Mantener v1 y su historial congelados. Extensiones nuevas documentadas y versionadas.
- No introducir claves en repo/salida, ni tocar datos internos del simulador.
- Mantener el plan global y las filas de tareas de otros responsables; propia línea de implementación en ESTADO.md.

## Fases

- [x] Leer ESTADO.md y cambios recientes; rama y worktree propios.
- [ ] Revisar fuentes de Karpathy y diseñar adaptación compatible con ruido y crédito finito.
- [ ] Implementar decisiones seguras: robustez, alarmas, ámbitos, datos de confirmación y autoridad.
- [ ] Implementar resúmenes portables, diagnóstico de ejecución, sensibilidad y comparación de actores.
- [ ] Integrar presupuesto persistente, reservas y ejecución del actor objetivo con parada ante coste incierto.
- [ ] Integrar planificación de experimentos y programa de investigación: cambios pequeños, diversidad, bloques completos, confirmación y límites.
- [ ] Probar escenarios end-to-end con actores falsos, recuperación y concurrencia; suite completa.
- [ ] Documentar cobertura de cada mejora, limitaciones, Relevo, commit/push y PR.

## Criterio de terminado

Las mejoras deben estar conectadas al CLI/driver que ya usa el equipo y contar con pruebas de sus garantías. Las hipótesis de estrategia quedan como experimentos evaluables; ninguna se declara ganadora sin datos del objetivo. La integración cloud se solicita mediante PR.

## Incidencias

- X devuelve SOURCE_NOT_AVAILABLE/403 al leer los dos posts. Se revisa el repositorio y su program.md como fuente primaria; no atribuir a los posts cifras que no se han podido verificar.
- La primera búsqueda Context7 de sqlite3 devolvió otros lenguajes: se descarta y se buscará la documentación Python adecuada.
