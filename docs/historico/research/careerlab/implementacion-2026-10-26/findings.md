# Evidencia y decisiones

- Base `b288805`, estado de las 18:12 UTC. La nube conserva la organización y ejecución; la clave ya está disponible según Alejandro, aunque el estado guardado sigue marcando T5 pendiente.
- Autoresearch primario: tres piezas pequeñas, evaluador fijo, superficie mutable acotada, program.md y resultados por experimento. Su regla de conservar al mejorar una sola métrica y su timeout fijo de entrenamiento no se trasladan directamente a episodios estocásticos de 48 meses.
- La rama main aún no incluye los cambios del diagnóstico PR #4. Se implementarán sus correcciones sin depender de que el informe sea integrado antes.
- Es preciso conservar la distinción entre límites presupuestarios de admisión y un límite duro de facturación por petición: no prometer lo segundo si el programa oficial sólo informa costes al terminar.
- Prueba nueva detectó un fallo previo: el identificador de trabajo no incluía el entorno, aunque la unicidad de celda sí. Encolar la misma política/actor en un segundo entorno colisionaba. Los IDs nuevos incluyen env_id; no se reescriben trabajos históricos.
- Pasan 22 pruebas existentes de core/orígenes. Primera tanda nueva: 14 pasan y una detecta la colisión anterior; se corrige y se vuelve a verificar.
