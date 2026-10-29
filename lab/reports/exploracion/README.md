# Línea Exploración: subir la nota global más allá de lo conocido

**Pregunta.** ¿Dónde está el salto de nota del manual de DeepSeek, contando partidas (80 %), calidad de los SKILL.md (10 %) y fichas (10 %), y con qué candidatos y pruebas se consigue? Rama `claude/gradient-depression-skills-k3b6u0` (se junta con `main` al terminar). Carpetas: `lab/reports/exploracion/`, `scripts/exploracion/`, `lab/policies-src/exploracion/`. Sin DeepSeek: réplica, datos reales ya pagados y jueces de Claude.

**Estado (29 oct, noche):** en curso. Lo hecho está en §1–§4; el Relevo, al final.

## 1. La réplica calibrada con las partidas reales (hecho)

**En una frase:** un modelo de elección ajustado a las 2.743 decisiones de historia reales de la familia v4/cp predice el 87 % de las elecciones de DeepSeek en partidas que no vio, y metido en la réplica reproduce las partidas reales: completas 65,4 (reales 65,3), ~17–20 % de hundimientos (reales 5 de 20), L5 hacia el mes 42–43 (reales ~44), primer ascenso en el mes 6 el 54 % (reales 52 %).

- **Datos.** `scripts/exploracion/calib_data.py` empareja cada decisión de `lab/data/deepseek/decisiones.csv.gz` con su nodo del catálogo de la réplica (2.289 por la tabla, 1.480 más por título, número de opciones y texto de la opción elegida: 3.769 de 3.769). Guarda, por decisión, las opciones con su efecto y riesgo verdaderos y las cuatro pasadas de lectura de DeepSeek (`etiquetas/ds-v1-*-full`, `ds-v3-*-full`). La tabla lleva texto del juego: va a `~/careerlab-data/exploracion/calib.jsonl.gz`, fuera de Git (se rehace con CPU, NORMAS §1.6).
- **Modelo** (`scripts/exploracion/choice_model.py`): logit condicional. Rasgos de cada opción: ganancia útil y desperdiciada (por encima del techo) de Skill/Network/Output, pérdidas, Health/Dignity/Wealth, riesgo verdadero (lineal, «hay riesgo», «riesgo 2 o más»), la lectura media de DeepSeek de cada indicador y del riesgo, y el contexto (mes previo, RR. HH. no amable, Health baja). Validación por partidas (6 de 23 fuera): acierto 87 %, log-verosimilitud −0,26 por decisión; sólo efectos verdaderos 84 %, sólo lecturas 87 %; el azar 40 %. DeepSeek se repite a sí mismo el 90–94 % (B21, C54): 87 % es casi el techo.
- **Lo que dicen los pesos.** DeepSeek evita con fuerza lo que lee como pérdida de Skill (−4,6), Network (−2,2) y Output (−2,0); valora lo que lee como Health (+1,1) y Dignity (+0,8) y lo que lee como «baja el riesgo» (+1,0); el riesgo verdadero pesa −0,6 por punto, −0,45 si hay alguno y −1,0 más si es de 2 o más (ve el riesgo mejor en partida que en las pasadas de lectura). No distingue una subida útil de una que cae sobre el techo.
- **Réplica** (`scripts/exploracion/dssim.py`): historias con ese modelo (muestreado, con las lecturas reales), trimestres con las reglas de la familia (bots de `techo/` y `comprobante/`), y el parche B30 (la tercera evaluación de L1 sólo con el riesgo a 0), que la réplica de `main` no tenía. Sin el parche, el 25 % se quedaba en L1; con él, 12 %.

| Réplica (2.000 partidas) | Media | Completas | Media completas | Despido L1 | Salud | Crisis | L5 en el mes | L6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Réplica antigua, lectura «ruidosa» (techobot) | 41,1 | 41 % | — | 18 % | 7 % | 32 % | — | 1 % |
| **Calibrada, reglas de cp-v12 (`qskill=4`)** | **58,5** | 81 % | **65,4** | 10 % | 6 % | 3 % | 42,6 | 13 % |
| Partidas reales de la familia (20 con final) | ~56,6 | 75 % | 65,3 | 15 % | 5 % | 5 % | ~44 | 0 de 14 |

Error típico de cada media de la réplica: ~0,35 con 2.000 partidas; las comparaciones usan las mismas semillas.

## 2. Dónde están los puntos (hecho)

**El planificador con información perfecta saca 74,4 en la réplica calibrada; DeepSeek, 59,4.** Cambiando quién decide sólo en una parte de la partida (`scripts/exploracion/scriptbot.py`, `SwapBot`):

| El planificador decide sólo… | Media | Ganancia |
|---|---:|---:|
| (nadie: DeepSeek con las reglas de cp-v12 + informes en el trimestre de L1) | 59,4 | — |
| las historias de L1 | 65,4 | **+6,0** |
| … sólo en los dos meses previos a cada evaluación de L1 | 64,2 | +4,8 |
| las historias de L2 | 61,0 | +1,6 |
| las historias de L3 | 61,0 | +1,6 |
| las historias de L4 | 61,5 | +2,2 |
| las historias de L5–L6 | 60,1 | +0,8 |
| los trimestres | 60,9 | +1,5 |
| todas las historias de los dos meses previos a cada evaluación | 67,6 | +8,2 |
| todas las historias | 73,1 | +13,7 |

En las partidas completas la diferencia (65,4 frente a 74,7) se reparte en nivel 2,6, dinero 2,3, Skill 1,7, Network 1,5 y riesgo ~1.

**Por qué pierde las evaluaciones** (`diag_reviews.py`): L1, el 51 % (Output 60 %, Network 40 %, por 1–2 puntos); L2, el 26 % (Output, Network); L3, el 40 % (Network y Output por 2–3 puntos); L4, el 72 % (Skill, mediana 22 puntos; Output 3); L5, el 80 % (Skill 9, Output 4).

**En el mes previo de L1, en las partidas reales** (120 decisiones): el 22 % elige una opción que pierde Network u Output; en 16 de esos 26 casos la única alternativa sin pérdida tenía riesgo, y en 10 había una segura que no vio. Donde DeepSeek se aparta del planificador en ese mes, casi siempre elige un **gesto de integridad** (negarse a hacer campaña, poner una B «justa», corregir en público, reconocimiento formal, el proceso largo): Dignity +2 y Network u Output −1/−2 (C58).

## 3. Lo que vale cada idea en la réplica calibrada (hecho)

Base: reglas de cp-v12 + informes en el trimestre de L1 (`q1out`), 59,4. Cotas «oráculo» marcadas.

| Idea | Media | Δ | Lectura |
|---|---:|---:|---|
| Informes en el trimestre de L1 (`q1out`, de cp-v11) sobre cp-v12 | 59,4 | +0,9 | menos muertes por salud (no gasta Skill learning con Health baja) |
| Recuperar Health en el trimestre con Health ≤ 5 (`qh=5`) / ≤ 6 | 59,9 / 60,0 | +0,5 / +0,6 | muertes por salud a la mitad |
| DeepSeek cuida el triple la salud con Health ≤ 5 (`hcare`) + `qh=5` | 60,3 | +0,9 | muertes por salud 4 % → 0,6 % |
| Pérdidas de N/O en el mes previo de L1 el doble de graves (`l1loss=2`) | 60,0 | +0,6 | |
| Skill el doble desde L4 (`sk4=2`) | 59,7 | +0,3 | |
| Más aversión al riesgo en todo (×1,5) / menos (×0,7) | 59,8 / 57,7 | +0,4 / −1,7 | no hay que tolerar más riesgo |
| Dignity sin valor cuando está en 9–10 (todos los meses / sólo meses previos) | 56,7 / 59,2 | −2,7 / −0,2 | **las opciones «íntegras» son también las que le alejan del riesgo**: más crisis |
| Defuse sólo con RR. HH. frowning o peor | 59,2 | −0,2 | se queda como está |
| Saber los techos en las historias (cota) | 59,3 | 0 | |
| Saber los techos en el trimestre (cota) | 59,8 | +0,4 | |
| Veto oráculo a las opciones que pierden N/O en el mes previo de L1 (riesgo ≤ 1 permitido) | 62,7 | **+3,3** | la cota de la trampa de L1 |
| … el mismo veto con una pasada real de lecturas de DeepSeek | 59,5–60,0 | +0,1–0,6 | **las pérdidas que importan son justo las que no ve** |
| Revisar la opción elegida antes de enviarla en el mes previo de L1, detectando el 50 % / 100 % de las pérdidas | 60,3 / 60,7 | +0,9 / +1,3 | con un 20 % de falsas alarmas, −3,7 |
| DeepSeek más constante (temperatura del modelo ×0,5) | 61,0 | +2,0 | el modelo es algo más aleatorio que DeepSeek (autoacuerdo 86 % frente a 90–94 %) |
| **Script que decide las historias con las lecturas de DeepSeek** (planificador de signos, riesgo y umbrales exactos) | 54,9–56,2 | **−3 a −4,5** | crisis 15 %: confirma C23 |
| Reglas de historias de v4 frente a las de cp (modelos ajustados por separado, mismo trimestre) | 58,7 / 58,0 | +0,7 ± 0,4 | la diferencia real de 5 puntos entre completas (4 frente a 13 partidas) es sobre todo azar |

## 4. El script en partida

Lo que puede ver un script con lo que devuelven las herramientas oficiales en la partida (comprobado en las trazas):
- `observe` da el estado exacto (los seis indicadores, nivel, meses en el nivel, energía) y, en el trimestre, el **efecto exacto de cada acción** (`status_updates`: Output 2, HiddenRisk +1…).
- El comentario mensual de RR. HH. tiene cinco tonos (sonriente, quietly, frowning, uneasy, angry) que en nuestras partidas siguen al riesgo oculto acumulado.
- `check_latest_logs` devuelve, por cada elección, **su efecto nominal** («Chose #1: … Skill +1, Dignity +1, Health +1») y el texto del resultado; con él un techo se detecta sin leer nada (efecto nominal +2 y el indicador no se mueve).
- Las notas de DeepSeek ya llevan bien el estado: «Now» coincide con el estado real en 3.200 de 3.211 notas y «Review in N» en el 96 %. Un script que sólo lleve la memoria no arregla nada medible.

Lo que dice la réplica calibrada: decidir historias con un script pierde (§3); los techos valen +0,4 como mucho y sólo en el trimestre; el planificador perfecto en los trimestres vale +1,5 como cota. **El script no es donde está el salto.** Búsqueda del mejor trimestre por tramos de nivel, en marcha (`qsearch.py`).

## Relevo (29 oct, noche)

1. **Hecho.** Réplica calibrada con las partidas reales (§1), descomposición de la distancia al planificador (§2) y batería de ideas (§3), juez de calidad sobre cp-v12 y v4 (Sonnet 66/66, Opus 73/72–73; lo que más resta: claridad del bucle, afirmaciones nuestras presentadas como reglas —el calendario de la evaluación—, falta de un plan por fases de 48 meses; `data/j00.jsonl`).
2. **Datos.** Pesos del modelo en `lab/data/exploracion/choice_beta*.json`; la tabla de calibración se rehace con `uv run python scripts/exploracion/calib_data.py`.
3. **A medias.** Búsqueda del trimestre por tramos; candidatos de manual; plan para DeepSeek.
4. **Para retomar.** `uv pip install pandas scikit-learn` (el entorno de `uv` no los trae), después `uv run python scripts/exploracion/calib_data.py && uv run python scripts/exploracion/choice_model.py && uv run python scripts/exploracion/fit_subsets.py`, y las baterías con `uv run python scripts/exploracion/dssim.py --arms qskill=4,qskill=4+q1out --games 2000`.
