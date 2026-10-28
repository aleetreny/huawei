# El runtime también está en el camino al 75

**Un ensayo oficial reciente quedó vivo en el mes33/L2 tras negativas repetidas; no se puede usar como derrota ni como prueba de capacidad máxima del modelo.** La configuración local observada pide chino. Preparar una ejecución inglesa comparable es una corrección comprobable sin gastar API, pero su efecto en Q sigue sin medirse.

Esta auditoría es de sólo lectura sobre artefactos producidos por nuestras herramientas oficiales y sobre el código público del runner. No se han abierto bases de datos, paquetes internos del simulador, claves ni archivos de entorno; no se ha reanudado ninguna partida.

## Evidencia directa

Fuente: `~/careerlab-data/huawei-deepseek/runs/deepseek-pilo-0b43b18e-dff20f-00001-a1/`. El resumen reproducible está en [runtime-audit.json](runtime-audit.json).

- El reporte de esa ejecución indica `max_continuations`, sin `ending_score`.
- Hay138 observaciones y137 acciones correctas, sin rechazos de `take_action`.
- La última observación es mes33, L2, Health6, Dignity10, Skill21, Network5, Output6, Wealth12. Sus flags dicen vivo y sin fracaso. No imputamos puntuación terminal a ese estado.
- El primer bloque ejecuta106 acciones; los siguientes registros de finalización contienen poco progreso y muchos no añaden acciones. Hay41 `frame_final`; estos registros incluyen pares y no equivalen a41 reanudaciones independientes. El runner público limita las continuaciones a20.
- El transcript visible contiene42 apariciones de una negativa genérica en chino. El colector excluye los deltas marcados como razonamiento. No copiamos historias ni texto narrativo al informe.
- Las tres configuraciones actuales de slots (`slot0`, `slot1`, `slot2`) contienen `preferred_language: zh`. Son configuraciones actuales, no fingerprints históricos congelados: por eso no certifican por sí solas el idioma configurado durante cada ensayo pasado.

Otros dos reportes t13-read-v2 terminaron por watchdog de presupuesto. Sus deltas usan el gasto total de una clave compartida mientras había concurrencia: **no sumar esas cifras como costes independientes por partida**. Esta auditoría no modifica la contabilidad ni los límites. Las salidas v3/v4/v5 vistas vacías tampoco establecen terminación; no se reinicia nada a partir de un archivo vacío.

## Qué cambia la interpretación

Hay dos problemas distintos. El ensayo no llegó al final por una interrupción del ejecutor, pero tampoco llevaba una carrera fuerte: permanecía en L2. Evitar negativas o corregir el entorno no demuestra que vaya a alcanzar75. A la inversa, una interrupción sin score no demuestra una derrota estratégica.

No sabemos si las negativas dependen del idioma, del contenido, de la longitud del contexto, del servicio u otra condición. No se ha hecho una comparación causal y no se propone elegir un proveedor de hosting. Las reglas del reto prohíben preferencias de proveedor; el parche no las añade.

El arranque de `careerlab.actors.official_runner.prepare_slot` usa stdin cerrado y deja que JiuwenSwarm tome su preferencia no interactiva. No fija explícitamente el idioma. El repositorio participante público [KSL_TechArena](https://github.com/krsnkkv/KSL_TechArena) documenta seleccionar inglés al inicializar; eso es una instrucción de instalación, **no evidencia de su puntuación ni de que sus autores sean el equipo de75**.

## Cambio concreto preparado y probado

El parche [english-runtime.patch.gz](../../../../scripts/deepseek/english-runtime.patch.gz) hace dos cosas para una futura ejecución autorizada:

1. Configura `preferred_language: en` después de la preparación del slot, preservando los demás valores, el modelo, el modo y la versión fijada. No llama al modelo.
2. Incluye el idioma en el registro/fingerprint del actor para impedir que los resultados viejos y nuevos se agrupen como si fueran el mismo actor.

Se aplicó temporalmente a los módulos del laboratorio y se ejecutó `uv run pytest -q tests/test_target.py`: **33 tests pasan**, sin red ni gasto. Los tests nuevos verifican preservación exacta del resto de configuración (incluyendo CRLF), idempotencia, registro del idioma y error temprano ante configuración ausente o ambigua. Después se revirtió ese cambio temporal del ejecutor común. El parche queda revisable en la carpeta de código de esta línea; no se ha aplicado a ninguna instancia real ni se ha iniciado o parado una instancia.

Para comprobarlo sin API en una copia limpia:

```sh
gzip -dc scripts/deepseek/english-runtime.patch.gz > /tmp/huawei-english-runtime.patch
git apply /tmp/huawei-english-runtime.patch
uv run pytest -q tests/test_target.py
git apply --reverse /tmp/huawei-english-runtime.patch
```

Usar una copia limpia evita pisar cambios propios del ejecutor. Aplicar el parche no autoriza partidas ni gasto; sigue vigente la prohibición de llamar a DeepSeek para este objetivo.

## Relevo

- Hecho: auditoría de una traza oficial interrumpida, hashes de sus artefactos, estados visibles, conteo de acciones/negativas y lectura selectiva de la preferencia de idioma. Parche concreto y tests offline preparados.
- No demostrado: causa de las negativas, mejora de puntuación o equivalencia con el entorno de evaluación. El objetivo75 sigue abierto.
- Siguiente: integrar la corrección de configuración cuando se prepare una futura ejecución autorizada y conservar el nuevo fingerprint. No repetir una partida ahora ni incrementar `MAX_CONTINUATIONS` para hacer pasar una prueba local como si fuera la configuración oficial.
