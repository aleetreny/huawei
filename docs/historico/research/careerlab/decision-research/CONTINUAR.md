# Continuar la investigación en este chat

El índice de conclusiones es [insights.jsonl](insights.jsonl); las pruebas pendientes están en [hypotheses.json](hypotheses.json). El informe actual es [la exploración inicial](../../../lab/reports/decision-research/cycles/002/interpretation.md). Se conserva cada ciclo con sus datos, código identificado por hash y límites. No hay un proceso en segundo plano.

## Cada nueva sesión o tanda

1. Leer `ESTADO.md`, este archivo y el informe actual. Seguir en la rama propia; si la PR se ha integrado, revisar el estado antes de crear la continuación. No tocar el plan global.
2. `git fetch origin main cloud-lab-run`, integrar main en la rama de investigación y leer los cambios. No ejecutar un fetch global que falle por `Matteo`/`matteo/...` en macOS.
3. Decidir la pregunta siguiente **antes** de mirar nuevas asociaciones. Mantener `exploration-v1.json` para repetir exactamente el análisis, o crear `exploration-v2.json` explicando qué cambia y por qué. Un cambio después de ver resultados es exploratorio, no una preregistración.
4. Elegir un número de ciclo nuevo. El script rechaza sobrescribir ciclos anteriores. Por ejemplo, el próximo es `003`:

```bash
uv run python scripts/explore_decisions.py \
  --cycle 003 \
  --runs-root "$HOME/careerlab-data/huawei/runs"
```

El script se puede ejecutar en nube o Mac sobre exports y trazas ya guardadas; no inicia el motor, importa registros en vivo ni encola partidas. Para otro origen dar `--export-dir lab/registry-origins/<origen>` y su carpeta de runs, y usar otro `--output-root`; no sumar copias ya importadas al canónico.

5. Revisar `coverage.json` y `manifest.json` **antes** de interpretar `analysis.json`. El linaje muestra trazas nuevas frente a reutilizadas y si cambiaron los exports. Recuperar una traza antigua mejora cobertura, pero no añade una partida nueva. Repetir la regresión sobre los mismos datos tampoco añade evidencia independiente.
6. Revisar extracción: estados consumidos una vez, sesiones, llamadas pendientes, rechazos, pasos, opciones listadas y coincidencia con el resultado exportado. No reconstruir estados a partir de notas ni respuestas memorizadas.
7. Leer `tables.md`; contrastar por políticas y familias. Sólo comparar errores entre modelos sobre **la misma cohorte**. Modelos sin soporte quedan marcados como tales. Una predicción parcial no sirve para podar manuales ni reemplazar partidas completas (§9 de v1).
8. Escribir `interpretation.md`: qué se aprendió, qué no sabemos, datos exactos, límites y siguiente prueba. Añadir eventos al final de `insights.jsonl`, reutilizando el mismo ID si se revisa una conclusión; no borrar la historia. Actualizar prioridades/estado en `hypotheses.json` y enlazar aquí el nuevo informe.
9. Tests relevantes y suite requerida, Relevo, sólo nuestra línea de `ESTADO.md`, commit y push; actualizar la PR o abrir una continuación si ya se fusionó. Ninguna conclusión queda sólo en el chat. Durante tareas de más de una hora, subir también un relevo intermedio.

## Cuándo pasar de explorar a probar

La siguiente prioridad es **MEASURE-01**, recuperar cobertura de nube. Después H-DR-01 prueba una sola regla contra un padre congelado. La nube organiza presupuesto y partidas; este pipeline no las solicita automáticamente. Confirmación y modelo objetivo siguen el protocolo v1.

No afirmar que el score mejoró por un coeficiente, una diferencia entre grupos retrospectivos o una única partida ganadora. Si se necesita un cambio de harness para observar cada decisión, registrar una configuración nueva de actor; no mezclarla con la antigua.

## Archivos de un ciclo

| Archivo | Uso |
|---|---|
| `manifest.json` | Exports, especificación, versiones de código, hashes de trazas y resultados, linaje y hashes de salidas |
| `source/`, `runtime.json` | Copias exactas del código y entorno numérico para reproducir el ciclo; en 001/002 se verificaron las copias contra los hashes tras ejecutar |
| `coverage.json` | Partidas elegibles frente a extraídas por actor y causas de faltantes |
| `episodes.jsonl` | Una fila por partida, estados tempranos, calidad temporal y resultados |
| `actions.jsonl.gz`, `observations.jsonl.gz` | Datos numéricos y claves hash para auditar, sin notas/razonamientos ni texto de historias |
| `predictions.jsonl` | Predicción fuera de muestra por partida y pliegue; útil para revisar errores |
| `analysis.json`, `tables.md` | Asociaciones, soporte, resultados de ridge y contabilidad de puntos |
| `interpretation.md` | Conclusiones humanas, siguiente pregunta y Relevo; no lo genera una regresión |

Los meses 6 y 12 son cortes retrospectivos de análisis. No se convierten en disparadores de calendario ni umbrales aprendidos dentro de las Skills. El resultado de estados es Q; no incluye ahorro de tokens ni calidad documental y no sustituye a Y para seleccionar.

## Contexto metodológico

Se ajustan mediana, escala y penalización sólo con entrenamiento; la evaluación externa reserva grupos completos y la interna elige la penalización. Véanse las guías oficiales de [fuga de información](https://scikit-learn.org/stable/common_pitfalls.html) y [validación por grupos y anidada](https://scikit-learn.org/stable/modules/cross_validation.html). Esta implementación usa NumPy; no añade scikit-learn al proyecto.
