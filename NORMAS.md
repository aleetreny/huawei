# Normas de trabajo

Para personas y agentes. Si sólo lees dos archivos, que sean [ESTADO.md](ESTADO.md) y este.

## 1. Orden del repositorio (para que no vuelva a haber 30 ramas sueltas)

1. **Una línea de trabajo = una rama + una carpeta.** La rama se llama `<persona>/<línea>`. Todo lo que produce la línea vive en `lab/reports/<línea>/` (informes) y `scripts/<línea>/` (código). Nada suelto en la raíz ni en `lab/reports/`.
2. **Cada carpeta de línea tiene un `README.md`**, con qué pregunta responde, estado, conclusiones y Relevo al final. Cada experimento es un archivo dentro de esa carpeta y **empieza por su conclusión en una frase**.
3. **Como mucho 3 líneas activas a la vez.** Están en la tabla de [ESTADO.md](ESTADO.md). Para abrir una cuarta, se cierra antes otra.
4. **Cerrar es parte del trabajo.** Cuando una línea termina, o al final de cada día:
   - se junta con `main`;
   - sus hallazgos pasan a [HALLAZGOS.md](HALLAZGOS.md) con su nivel (A, B, C o X) y su fuente;
   - se borra la rama.
   Una rama que lleva un día sin cambios y no está en la tabla de ESTADO se junta o se borra.
5. **Lo viejo va a `docs/historico/` o a `lab/reports/historico/`**, no se borra. Si un código lee una carpeta, la carpeta se queda donde está y se marca como histórica en [lab/reports/README.md](lab/reports/README.md).
6. **Los datos con texto del juego no van a Git**, salvo los que ya están (repo privado). Van en `~/careerlab-data/<línea>/`, y el informe dice cómo regenerarlos.
7. **Prueba antes de partidas.** Una idea se comprueba primero con el simulador o con el banco de situaciones, que son baratos; las partidas con IA sólo confirman. Antes de lanzar partidas, se escribe cuántas hacen falta para ver la diferencia esperada.

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
- Poner en un Skill títulos de eventos, respuestas fijas, meses concretos, umbrales o fórmulas no publicadas, aunque sean ciertos. `uv run careerlab lint <carpeta>` lo vigila. El catálogo de eventos y el simulador sirven para investigar, nunca para copiar a un Skill.
- Pasar texto del juego a un diseñador de manuales.
- Gastar dinero de API sin un presupuesto confirmado por Alejandro. DeepSeek, sólo en las pruebas que él apruebe.
- Lanzar partidas con Claude sin decirlo en tu línea de ESTADO. Topes: 4 partidas a la vez y `--max-five-hour 0.65`.

## 5. Cuota de Claude (cuenta Max)

Ritmo semanal acordado: hasta un 45 % de la semana el 28 oct, un 75 % el 31 oct y un 90 % al final. El laboratorio lo respeta solo (`quota_cap.json`). Si una línea gasta más de un 5 % de la semana en un día, lo dice en su Relevo.
