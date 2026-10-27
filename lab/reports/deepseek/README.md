# Línea DeepSeek: qué entiende DeepSeek de cada respuesta

Rama `alejandro/deepseek`, Mac de Alejandro (donde está la clave). Encargo: [prompt-deepseek.md](../transmision/prompt-deepseek.md).

**Pregunta.** ¿Sabe `deepseek-v4-flash` ver qué indicador sube o baja cada respuesta y cuáles son arriesgadas? ¿Qué categorías reconoce y qué reglas obedece? Con eso, ¿cuál es la forma más masticada de darle las reglas?

## Conclusiones (27 oct, 17:00 UTC)

1. **DeepSeek ve bien el riesgo y mal Skill y Output.** Sin ayuda detecta el 83 % de las respuestas que suben el riesgo oculto y el 90 % de las peligrosas, pero sólo el 45 % de las que suben Skill y el 49 % de las que suben Output. Lee los tipos de respuesta mejor que Haiku ([percepcion.md](percepcion.md)).
2. **La mejor categorización es leer cada opción como seis signos más el riesgo**, con definiciones que digan cómo suele moverse cada indicador (prompt v3). Un bot que elige sólo con esa lectura de DeepSeek saca **56,0** en el simulador, frente a 46,7 con los 10 tipos de Haiku (lo que había que superar) y 67,7 el oráculo. Con las mismas definiciones, los 10 tipos solos se quedan en 48,5. Se confirma con los títulos reservados en percepción y en el simulador, aunque no en la pérdida por decisión del banco ([categorizacion.md](categorizacion.md)).
3. **Las pistas de lectura funcionan:** con ellas DeepSeek ve el 78 % de las subidas de Skill (antes 45 %) y el 86 % de los riesgos (antes 83 %). Output sigue a medias (47–54 %), y es la siguiente palanca: +2 puntos si se leyera bien.
4. **Una regla de grupo escrita, por orden, conserva casi todo:** "descarta lo arriesgado; si Health o Dignity están bajas, lo que las baja; en el mes previo a la evaluación, lo que baja Skill, Network u Output; de lo que queda, lo que más sube los indicadores de crecimiento". Con la lectura de DeepSeek saca 53,7 en el simulador.
5. **El manual t13-final se transmite a DeepSeek.** Lo lee en el 100 % de las situaciones y obedece el reparto trimestral casi como Haiku: Skill en L4 pasa del 2 % al 65 % y el comentario de RR. HH. del 15 % al 65 %. No le estropea las historias; probablemente se las mejora (pérdida −0,40 a −0,79 puntos por decisión según el control de referencia). Sólo los detonantes empeoran un poco ([obediencia.md](obediencia.md)).
6. **DeepSeek es menos constante que Haiku:** sin manual repite la misma elección en el 91 % de las historias (Haiku, 96 %), y entre dos lecturas cambia el 12–18 % de las etiquetas. Una sola pasada de etiquetas hace variar la nota del bot 5–7 puntos; por eso las medidas finales mezclan dos pasadas.

**Propuesta para el manual:** mantener t13-final como base y añadirle la ficha de lectura v3 y la regla de historias. Es la variante `t13-read-v1`, que se está midiendo en el banco ([masticado.md](masticado.md), en marcha).

## Gasto de DeepSeek

Presupuesto de la línea: 5 USD (parar a 3 y preguntar). Saldo de la clave al empezar: 0,1905 USD gastados. Gasto exacto en `GET /key`; el gasto por llamada, en `~/careerlab-data/deepseek/calls.jsonl`.

| Hora (UTC) | Qué | Llamadas | Coste (USD) | Acumulado de la línea |
|---|---|---:|---:|---:|
| 16:20 | Piloto: 5 llamadas de percepción (0,00014 por pregunta; 370–1.185 fichas de razonamiento por llamada; proveedores Baidu y Parasail) | 5 | 0,0007 | 0,001 |
| 16:25 | Percepción v1, títulos de diseño × 2 | 579 | 0,06 | 0,07 |
| 16:28–16:50 | Banco de obediencia: control y t13-final, 459 situaciones cada uno | 5.979 | 1,20 | 1,27 |
| 16:30–16:45 | Percepción v2 (×2), v3 (×2, todos los títulos), v1 en títulos reservados (×2) | 1.787 | 0,20 | 1,47 |
| 16:50 | Control repetido en el bloque general (139 situaciones) | 563 | 0,08 | 1,55 |
| 16:55– | Variante t13-read-v1 en 320 historias | en marcha | ~0,45 | ~2,0 |

## Experimentos

| Informe | Qué mide | Estado |
|---|---|---|
| [percepcion.md](percepcion.md) | Qué ve DeepSeek de cada opción (tipo, signo de cada indicador, riesgo) | hecho |
| [categorizacion.md](categorizacion.md) | Qué agrupación entiende DeepSeek y discrimina; medida única en el simulador; regla de grupo escrita | hecho |
| [obediencia.md](obediencia.md) | Banco oficial con DeepSeek: control frente a t13-final; huella y control repetido | hecho |
| masticado.md | t13-final + ficha de lectura + regla de historias, en el banco | en marcha |

## Código y datos

- `scripts/deepseek/ds.py`: cliente de la clave (lee `.env` sin copiarlo; sin proveedor fijado; temperatura 0,95; freno de gasto en 3 USD). `ds.py status` da el gasto.
- `perceive.py`: etiquetado y puntuación de la percepción. Prompts en `scripts/deepseek/prompts/`.
- `groupbot.py`: medida única en el simulador (`--bank` da la pérdida por decisión); `LexBot`, la regla escrita.
- `bench.py`: banco oficial con DeepSeek; `obedience.py` y `paired.py`, informes.
- Datos fuera de Git (llevan texto del juego): `~/careerlab-data/deepseek/` (respuestas de DeepSeek, etiquetas, ejecuciones del banco).

## Relevo

**27 oct, 17:00 UTC (provisional; se completa al cerrar la variante).**
1. **Hecho:** arnés, percepción v1–v3, categorización con medida única, banco de obediencia (control, t13-final, control repetido). Se lanzó la variante `t13-read-v1`.
2. **Resultados:** en las conclusiones de arriba y en cada informe.
3. **A medias:** `t13-read-v1` en el banco.
4. **Siguiente:** puntuar la variante con `uv run python scripts/deepseek/paired.py --a ds-t13-final --b ds-t13-read --phase e`. Después, sólo con el visto bueno de Alejandro, 1–2 partidas oficiales con el mejor manual.
