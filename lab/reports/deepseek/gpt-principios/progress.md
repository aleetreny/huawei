# Progreso
27 oct 2026: leídos ESTADO/NORMAS/HALLAZGOS, manual Serena, skills Exa y planificación; rama existente alejandro/gpt-principios, fetch y merge origin/main (sin cambios). Recuperado material no seguido; no se toca duplicados iCloud “ 2”. Sin API ni partidas nuevas.

27 oct ~19:17 UTC: barrido ampliado con búsquedas in:readme y listado de forks: añadidos krsnkkv/KSL_TechArena (mismo texto de Shriya), Artepace/slopathone_winningteam (README dice explícitamente untested) y peidi-L/preliminary (borrador). Sin evidencia pública de 75. GitHub search code encuentra principalmente nuestro repo privado, que se excluye de evidencia pública.

313 tests del repo pasan (43.46s; un aviso Authlib preexistente). Réplica recuperación 4x300 coincidencias exactas con resultados recuperados. Pruebas nuevas: incertidumbre3600 carreras, trimestre800, objetivos4000, representación4000. Son carreras de réplica, no juegos ni llamadas IA.

Cierre de este checkpoint: factorial de riesgo corregido y reproducido; pantalla de margen y control sin privilegios terminados. Documentado resultado negativo de transferencia. Sin API, partidas Claude ni subagentes. Objetivo75 permanece abierto.

12 archivos comprimidos verificados por SHA de archivo, SHA descomprimido, tamaño de filas y resúmenes. diff --check limpio tras normalizar CSV.

27 oct19:13 UTC: commit4cd5ac8 y push confirmados; PR22 abierto y adjunto al chat. Integración a main solicitada; objetivo75 activo y sin demostrar.

Continuación: turno anterior clasificado como progreso (PR22 y evidencia causal nueva). Revalidado repo/fetch/merge. Preparadas dos variantes generales con lint sin hallazgos. Banco fijado antes de llamadas:92 situaciones de48 títulos, dos brazos +24 repeticiones de control (208 llamadas máximo). Se sirve sólo la observación objetivo, evitando prefijos con transiciones incoherentes. Piloto1 completa:6.47s, una lectura Skill, cero acciones inválidas; cuota real5h10%, semana37%, cuenta Max. Comienza resto sin cambios de texto, secuencial, guardas0.65/0.45 y máximo4procesos. Ninguna partida oficial ni API DeepSeek.

Auditoría adicional de trazas existentes, sin reanudar nada: t13-read-v2 slot1 terminó por max_continuations, último observe mes33/L2 vivo,137 take_action correctos y cero rechazos. El ejecutor emitió41 frame_final (incluye pares), con muchos sin nuevas acciones después del primer bloque de106. No atribuir esta interrupción a una derrota ni concluir que arreglar el driver resuelve la estrategia: seguía enL2. Slots0/2 tenían cortes de presupuesto; los cargos del watchdog usan el gasto global de una clave compartida y no permiten atribución por partida sin reconciliar concurrencia. Las salidas v3/v4/v5 vacías no prueban que hayan terminado.

Hallazgo de runtime: las tres configuraciones de los slots oficiales contienen preferred_language:zh. La traza t13-read-v2 slot1 tiene42 repeticiones de una negativa en chino,137 acciones correctas, termina viva enmes33/L2 por max_continuations. No prueba causalidad idioma→negativa ni que corregir idioma dé75. Preparado parche concreto en scripts/deepseek/english-runtime.patch.gz para futuras ejecuciones: preferenciaen sólo al preparar slot, fingerprint del actor distinto y tests de preservación de configuración. Aplicado temporalmente al código para probar:33 tests target pasan; revertido después para conservar el ejecutor común y las instancias activas. El parche queda íntegro y revisable en la carpeta de la línea, conforme aNORMAS§1; no es una llamada ni un cambio en una instancia.

Segundo checkpoint:208/208 ensayos válidos, cero acciones inválidas; todosHaiku5.5/CLI2.1.303 y una lecturaSkill. Cuota compartida observada10→11% cincohoras,37→38% semanal. Análisis final completo: autocomprobación no mejora;4→5 riesgos positivos,3→6 elecciones dominadas inmediatas, cumplimiento92/92. No admitir a partidas completas. Tokens reportados son parciales por corte CLI tras elección, no factura ni eficiencia global. Guardados datos numéricos comprimidos, hashes y transporte; narrativa fuera deGit. Objetivo75 abierto.

El diff del parche tiene marcadores de contexto vacíos legítimos que git diff --check trata como espacios; se conserva íntegro comprimido con SHA, sin cambiar su código ni relajar comprobaciones del repo. Copia descomprimida aplicada por git apply --check.
