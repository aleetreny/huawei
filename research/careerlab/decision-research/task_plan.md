# Investigación de decisiones — plan local

Solicitud: abrir una línea robusta que convierta datos de partidas en mejores estrategias.
Rama: `alejandro/investigacion-decisiones`. Base: `origin/main` en `3c1c993`.
No se edita el plan global del organizador ni el protocolo v1. No se lanzan partidas.

## Fases

- [x] Leer ESTADO, protocolo y método; crear worktree separado.
- [x] Auditar registros, disponibilidad y estructura de trazas oficiales guardadas.
- [x] Escribir protocolo complementario: descubrimiento, experimento y confirmación.
- [x] Entregar auditoría reproducible y primeras hipótesis, con límites explícitos.
- [x] Validar, documentar Relevo y actualizar línea propia en ESTADO (243 tests OK).
- [x] Commit `5d3cb1d`, push y [PR #3](https://github.com/aleetreny/huawei/pull/3) abierta a main.

## Decisiones

- La unidad independiente es la partida; no se convierten meses en réplicas.
- Los datos históricos son descubrimiento. No se atribuye causalidad a sus coeficientes.
- La primera identificación causal será por asignación aleatoria de políticas completas.
- La selección y la confirmación siguen `lab/protocol/prereg-v1.*`.

## Ciclo 001 — primera exploración y estructura continua

Autorizado por Alejandro en este chat: explorar registros existentes, construir estructura reutilizable y subir conclusiones a la rama.
Base de datos actualizada: `origin/main` en `9b8fbe9`, integrada en esta rama; PR #3 sigue abierta.

- [x] Congelar especificación exploratoria antes de mirar asociaciones nuevas.
- [x] Implementar extracción temporal y manifiesto de cobertura/procedencia.
- [x] Ejecutar análisis descriptivo y modelos predictivos pequeños donde haya soporte.
- [x] Publicar ejecuciones 001/002 (mismos datos; corrección de inventario), registro de insights y cola de hipótesis con siguientes pruebas.
- [x] Tests (255), Relevo y línea propia de ESTADO.
- [x] Commit `6995b05`, push y PR #3 actualizada con la exploración y estructura continua (abierta y fusionable).

La continuación ocurre en este chat por ciclos manuales reproducibles. No se crea una automatización ni se lanzan partidas.

## Incidencias

- `session-catchup.py` no existe bajo `.codex/skills`; ejecutado desde la raíz real `.agents/skills`, sin contexto pendiente.
- Fetch actualizó main/cloud; una referencia remota colisiona por mayúsculas (`Matteo` / `matteo/...`) en macOS. No se borró ni modificó esa rama; el snapshot de main utilizado sí está actualizado.
- Al registrar el runtime tras los modelos se usó por error Python 3.9 del sistema, cuyo NumPy tiene arquitectura incompatible. No se llegó a escribir nada en ese intento; se usó el Python 3.13 del mismo venv con el que se ejecutaron los análisis, sin reinstalar paquetes.
