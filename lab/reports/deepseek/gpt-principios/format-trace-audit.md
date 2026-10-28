# Cómo llegó una partida real de DeepSeek a76,87

**El76,87 está verificado en el informe original: DeepSeek ejecutó un script del Skill; la política y su memoria se reproducen exactamente. Su familia sigue sin75estable y no sabemos qué técnica usaron los equipos que vio Alejandro.**

Evidencia posterior a la auditoría inicial, incorporada de `main@d05ac39`. El mismo script entregado en `sv1-g1` y `sv1-g2`, con SHA256 `71dadd…9691`, dio13,23 y76,87. El segundo terminaL6, Skill147, Network58 y riesgo final1. No atribuir el resultado al trabajo nuevo de esta auditoría: es un ensayo ya ejecutado porFormato. La capacidad real de `bash`/`code` dentro del Skill consta enB27 y en su informe; nuestro proxy anterior de cinco herramientas+Skill no la reproducía.

## Reproducción independiente del transporte

Se leen los cinco eventos públicos de nuestras partidas, emparejados por ID de herramienta y menú actual, y se ejecuta el script exacto de cada entrega con memoria sólo enRAM. No se lee el paquete ni la base de datos del juego. Datos fuente sólo fuera deGit.

- **750/750 salidas del advisor reproducidas.**
- **747/747 acciones emparejadas aceptadas siguen la salida.**
- **5/5 diccionarios de memoria final coinciden exactamente con las copias guardadas.**
- Un campo numérico visible mal copiado en una llamada (Wealth, carrera13,23); no se ha atribuido a él una derrota.
- Un único session_id de acciones por carrera. Ficheros de estado sobrantes en el directorio no equivalen a sesiones nuevas en esa traza.

La interpretación importante: no tenemos evidencia de que en estas carreras falle seguir el programa o recordar su contabilidad. La lectura de opciones y la política que transforma esas lecturas siguen siendo problemas separados.

## Lo que no debemos confundir con una causa

En76,87, diez de once respuestas elegidas cuyo riesgo es positivo en el catálogo no fueron reconocidas como tales; las diez se etiquetaron comoR-. También omite muchos costes de crecimiento y aun así termina bien. Por tanto, la nota alta no certifica percepción perfecta, y una mejora en exactitud media tampoco certifica una carrera mejor. Las cuentas excluyen llamadas al advisor que no se actuaron.

El saldo bruto de riesgo queda negativo en182/207llamadas de esa carrera, y se elige supuesta limpieza estando ya en cero en111. Es una inconsistencia de estimación, **no una explicación causal suficiente**, pues también aparece en el ganador. Probadas cuatro correcciones con lecturas congeladas/800semillas:

| Cambio | ΔQréplica vs51,71 | IC95% |
|---|---:|---|
| Piso en el contador|−0,176|[−0,421;0,068]|
| Valor sólo de reducción marginal hasta cero|−0,502|[−1,691;0,687]|
| Ambos|+0,057|[−1,108;1,223]|

Otra hipótesis, registrada después: mantener el valor deR- al escoger, pero no cancelar deuda por una conjetura de historia. En800semillas nuevas reduce crisis104→54 y aumenta completas505→529, pero suben despidos178→204 y baja el nivel medio; Q52,84→52,58, Δ−0,260[−1,047;0,526]. No promoverla por mejorar sólo supervivencia o una clase de fallo.

Dos trazas pasan un tonoHRmenor que el comentario público contemporáneo (23/90y39/203comparaciones). **La intervención de un solo campo produce cero cambios de elección en732decisiones aceptadas comparables:** el programa conserva informaciónHRrecibida antes en ese mes y los otros datos permanecen iguales. No afirmar que el transporteHRexplica la diferencia de nota ni gastar en un parche sin otro mecanismo. Es una prueba local; no propaga estados contrafactuales ni prediceQde carrera.

## Magnitudes y lecturas congeladas

La carrera ganadora sólo codifica magnitud doble en2/381opciones; dos carrerasv3lo hacen en196/386y214/374. `simadv` normalizaba a signo. Se comprobó esa interfaz con400semillas nuevas por fuente/brazo, conservando anotaciones insitu sólo donde existen y usando lecturasDSstandalone en todos los nodos no cubiertos, nunca verdad del catálogo.

- Baseline común52,17.
- Lecturas del ganador76,87 congeladas:53,47;26→31carreras de400 conQ>=75. No reproducen75estable.
- Lecturas de la carrera60,45:55,80con signos,56,07con magnitudes. La fuente con mejor nota real no es la que mejor generaliza como mapa congelado.
- Las otras fuentes no abren un salto. No concluir que las magnitudes son malas universalmente ni destilar un mapa de eventos: esa tabla no puede entregarse.

Protocolo: primera anotación efectivamente actuada por nodo. Hay nodos que reaparecen en una traza; se cuentan y se excluyen anotaciones posteriores, sin seleccionarlas por calidad. Dos ejecuciones numéricas antes/después de exigir aceptación real de la acción coinciden fila por fila. Las fuentes son posthoc y no aleatorizadas; no trasladar sus medias a un modelo nuevo.

## Investigación pública actualizada

Alejandro confirma que vio las partidas de otros equipos y que esa evidencia no está publicada. El28octel marcador público muestra227filas, todas0y ambos cortes sin datos. Esto no refuta su observación. Los árboles `main` de los seis repositorios conocidos no contienen helpers de participante con extensionesPython/JS/TS/shell/notebook; los archivos ejecutables encontrados son del runner/documentación/tests. No se ha encontrado una atribución pública del método. No seguir buscando el mismo supuesto reporte público sin una pista nueva.

## Relevo

Ninguna llamada nueva aDeepSeek. Reproducción: `uv run python scripts/deepseek/gpt_format_trace.py`, `gpt_feedback_channel.py`, `gpt_risk_credit.py` y `gpt_format_labels.py`; cada uno guarda hashes y datos numéricos comprimidos. El código original de la primera pantalla de riesgo se conserva en `risk-credit-script-v1.py.gz` con hash exacto; la ampliación posterior queda en el scriptactual.

No promover correcciones de riesgo, etiquetas insitu ni observable-allocation-v1por estos resultados. Próxima prueba distinta: diagnóstico de capacidad con el mismo v4y doce menúsL1, Haiku/Sonnet,25llamadasMaxmáximo incluida admisión. Cuota fresca del28oct:5h1%, semana40%, actorSonnet5.5. Una primera invocación de menú falló antes de llamar al modelo (CLI consumió el prompt como argumento de `--allowedTools`); se conserva el fallo y se corrige orden de flags antes de repetir ese mismo caso. No sustituir resultados ni abrir juegos completos por este diagnóstico pequeño.
