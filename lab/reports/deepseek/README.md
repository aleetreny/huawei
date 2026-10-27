# Línea DeepSeek: qué entiende DeepSeek de cada respuesta

Rama `alejandro/deepseek`, Mac de Alejandro (donde está la clave). Encargo: [prompt-deepseek.md](../transmision/prompt-deepseek.md).

**Pregunta.** ¿Sabe `deepseek-v4-flash` ver qué indicador sube o baja cada respuesta y cuáles son arriesgadas? ¿Qué categorías reconoce y qué reglas obedece? Con eso, ¿cuál es la forma más masticada de darle las reglas?

## Conclusiones

Provisionales (27 oct, 16:35 UTC):
1. **DeepSeek ve bien el riesgo y los tipos de respuesta, y mal Skill y Output.** Detecta el 83 % de las respuestas que suben el riesgo y el 90 % de las peligrosas, pero sólo el 45 % de las que suben Skill y el 49 % de las que suben Output ([percepcion.md](percepcion.md)).
2. **Sus 10 tipos valen más que los de Haiku:** un bot que elige sólo con los tipos de DeepSeek saca 55,6–56,8 en el simulador, frente a 51,5 con los de Haiku, en el mismo montaje.
3. **Lo que más vale es percibir bien los signos de cada indicador:** con los seis signos y el riesgo sin error se sacan 67 (el oráculo, 67,7).

## Gasto de DeepSeek

Presupuesto de la línea: 5 USD (parar a 3 y preguntar). Saldo de la clave al empezar: 0,1905 USD gastados.

| Hora (UTC) | Qué | Gasto acumulado de la línea |
|---|---|---:|
| 16:20 | Piloto: 5 llamadas de percepción, 0,0007 USD (0,00014 por pregunta; 370–1.185 fichas de razonamiento por llamada; proveedores Baidu y Parasail) | 0,001 |
| 16:25 | Percepción v1, 289 preguntas × 2 | 0,065 |
| 16:28 | Piloto del banco: 8 situaciones × 2 brazos (0,0012 USD por situación sin manual, 0,0022 con t13-final) | 0,09 |

## Experimentos

| Informe | Qué mide | Estado |
|---|---|---|
| [percepcion.md](percepcion.md) | Qué ve DeepSeek de cada opción (tipo, signo de cada indicador, riesgo) y cuánto vale en el simulador | v1 hecho; v2 (definiciones con pistas) en marcha |
| obediencia | Banco oficial con DeepSeek: control frente a t13-final | en marcha |

## Relevo

27 oct, 16:15 UTC: rama creada, línea añadida a ESTADO.md. Siguiente: arnés en `scripts/deepseek/` y piloto de 5 llamadas.
