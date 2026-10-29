# Normas de trabajo

Para personas y agentes. Si sólo lees dos archivos, que sean [ESTADO.md](ESTADO.md) y este.

## 1. Orden del repositorio (para que no vuelva a haber 30 ramas sueltas)

1. **Una línea de trabajo = una rama + una carpeta.** La rama se llama `<persona>/<línea>`. Todo lo que produce la línea vive en `lab/reports/<línea>/` (informes) y `scripts/<línea>/` (código). Nada suelto en la raíz ni en `lab/reports/`.
2. **Cada carpeta de línea tiene un `README.md`**, con qué pregunta responde, estado, conclusiones y Relevo al final. Cada experimento es un archivo dentro de esa carpeta y **empieza por su conclusión en una frase**.
3. **Como mucho 3 líneas activas a la vez.** Están en la tabla de [ESTADO.md](ESTADO.md). Para abrir una cuarta, se cierra antes otra.
4. **Cerrar es parte del trabajo.** Cuando una línea termina, o al final de cada día:
   - se junta con `main`;
   - sus hallazgos pasan a [HALLAZGOS.md](HALLAZGOS.md) con su nivel (A, B, C o X), su fuente y con qué se midió (`Juego`, `Bot`, `Haiku`, `DeepSeek`…);
   - se borra la rama.
   Una rama que lleva un día sin cambios y no está en la tabla de ESTADO se junta o se borra.
5. **Lo viejo va a `docs/historico/` o a `lab/reports/historico/`**, no se borra. Si un código lee una carpeta, la carpeta se queda donde está y se marca como histórica en [lab/reports/README.md](lab/reports/README.md).
6. **Los datos con texto del juego van a Git sólo si costaron dinero o cuota y no se pueden rehacer** (el repo es privado; decisión del equipo, 29 oct). Las partidas y los bancos de DeepSeek, las etiquetas de percepción y lo que citan sus informes van en `lab/data/deepseek/`, con su README (qué es cada cosa, qué manual y versión del programa, nota, coste y fichas, qué script lo lee). Se exporta con `scripts/deepseek/export_data.py`, que quita claves, cabeceras de autorización y rutas personales. El resto (lo que se rehace con CPU, instalaciones del programa oficial, vídeos y ZIP de entrega) se queda en `~/careerlab-data/<línea>/`, y el informe dice cómo regenerarlo. Ningún archivo de más de 50 MB; nunca un `.env`.
7. **Prueba antes de partidas.** Una idea se comprueba primero con el simulador o con el banco de situaciones, que son baratos; las partidas con IA sólo confirman. Antes de lanzar partidas, se escribe cuántas hacen falta para ver la diferencia esperada.
8. **Los números de HALLAZGOS se ponen al juntar con `main`.** En la rama se usan nombres provisionales (`suelo-1`, `techo-2`…), para que dos líneas en paralelo no gasten el mismo número. Al juntar, se toma el siguiente libre y se añaden los temas en el mapa de HALLAZGOS.
9. **Cada manual candidato y cada prueba pendiente de DeepSeek se apuntan en [pendientes.md](lab/reports/deepseek/pendientes.md)**: padre, qué cambia, qué se ha medido, coste y regla de decisión. Quien gaste DeepSeek la tiene al día.

## 2. Documentar siempre

Lo que sólo está en un chat se pierde. Antes de terminar, si vas a quedarte sin cuota o sin contexto, y cada hora en trabajos largos, deja en el README de tu línea una sección **Relevo** con:
1. qué has hecho y por qué;
2. resultados con números y dónde están los datos;
3. qué falló o quedó a medias;
4. el siguiente paso, con los comandos para retomarlo.

Después, commit y push a tu rama, y actualiza tu línea de la tabla de ESTADO.md.

## 3. Ramas y `main`

- `main` tiene lo común y comprobado. Sólo se escribe en `main` para juntar líneas y mantener ESTADO, HALLAZGOS y NORMAS, con los tests pasando (`uv run pytest -q`) y sin forzar el push.
- Al empezar una sesión en una línea abierta: `git fetch origin && git merge origin/main`. Si hay conflicto en ESTADO.md o HALLAZGOS.md, quédate con la versión de `main` y vuelve a añadir tu línea.
- Commits a nombre de una persona, sin líneas `Co-Authored-By` de Claude.

## 4. Lo que nunca se hace

- Poner claves o secretos en el repo. La clave de la API va sólo en el `.env` del programa oficial.
- Leer el interior del simulador oficial (su paquete, su base de datos, sus archivos). Sólo se usan las 5 herramientas oficiales y lo que devuelven nuestras partidas.
- Poner en un Skill títulos de eventos, respuestas fijas, o umbrales y fórmulas no publicados presentados como reglas del juego, aunque sean ciertos. Tampoco nada sacado del paquete del motor o de sus datos, ni de soluciones de otros que lo hayan descodificado (BDCI, C46). `uv run careerlab lint <carpeta>` lo vigila. El catálogo de eventos y el simulador sirven para investigar, nunca para copiar a un Skill.
  - **Sí se puede, con permiso de los organizadores (29 oct, C49):** citar el calendario publicado (evaluación cada seis meses, 48 meses) con sus meses; describir lo visto en nuestras partidas, marcado como observación o heurística nuestra («in our runs…»); varias llamadas a herramientas por respuesta; y scripts del Skill que usan sólo lo que devuelve la partida en curso, sin memoria entre partidas. El script puede guardar su estado en un archivo del espacio de trabajo durante la partida (C60), pero tiene que empezar de cero en cada partida nueva.
  - **Si un método no está claro, se pregunta en Discord antes de usarlo** (lo exige el reglamento), y la respuesta se apunta en HALLAZGOS.
- Pasar texto del juego a un diseñador de manuales.
- Gastar dinero de API sin un presupuesto confirmado por Alejandro. DeepSeek, sólo en las pruebas que él apruebe.
