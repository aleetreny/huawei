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
- [ ] Commit, push y PR.

## Decisiones

- La unidad independiente es la partida; no se convierten meses en réplicas.
- Los datos históricos son descubrimiento. No se atribuye causalidad a sus coeficientes.
- La primera identificación causal será por asignación aleatoria de políticas completas.
- La selección y la confirmación siguen `lab/protocol/prereg-v1.*`.

## Incidencias

- `session-catchup.py` no existe bajo `.codex/skills`; ejecutado desde la raíz real `.agents/skills`, sin contexto pendiente.
- Fetch actualizó main/cloud; una referencia remota colisiona por mayúsculas (`Matteo` / `matteo/...`) en macOS. No se borró ni modificó esa rama; el snapshot de main utilizado sí está actualizado.
