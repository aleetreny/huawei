# Clave propia de OpenRouter para jugar con DeepSeek

**Conclusión: preparado y sin comprar.** Una clave propia de OpenRouter con 10–20 USD da unas 20–40 partidas iguales a las del reto (~0,5 USD cada una). El laboratorio ya la admite sin cambiar código: basta con apuntar `CAREERLAB_TARGET_ENV` a otro archivo.

## Por qué esta vía

- Una partida completa gasta ~70 millones de tokens, casi todos de contexto repetido. OpenRouter manda `deepseek/deepseek-v4-flash` casi siempre a Baidu (96 % de nuestras llamadas), que cobra la caché a 0,0095 USD por millón. Ningún otro proveedor ni crédito gratis la iguala; la comparación está en [nim.md](nim.md) y en el chat del 27 oct.
- Tiene una ventaja más: el vigilante calcula lo que gasta cada partida como el **uso de la clave al acabar menos el uso al empezar**. Con la clave del reto compartida entre chats, ese cálculo incluye también lo que gastan los demás chats a la vez, y puede cortar partidas sin que lo hayan gastado ellas. Con una clave propia, ese cálculo sólo ve lo de ese chat.

## Cómo usarla (cuando se compre)

1. En openrouter.ai: crear la cuenta, cargar 10–20 USD y crear una clave **con límite de crédito**. El vigilante necesita ese límite: con una clave sin límite, `play` se niega a empezar.
2. Pegar la clave en `~/careerlab-data/own-openrouter/.env`, que ya existe, está fuera del repo y tiene `chmod 600`. Dirección `https://openrouter.ai/api/v1`, modelo `deepseek-v4-flash`, sin fijar proveedor. **No tocar el `.env` oficial.**
3. Comprobar la clave (gratis) y lanzar:

   ```bash
   export CAREERLAB_ORIGIN=deepseek CAREERLAB_RUNNER_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Github/huawei/local-runs/official-runner"
   export CAREERLAB_TARGET_ENV=~/careerlab-data/own-openrouter/.env
   uv run python -m careerlab.target key
   uv run python -m careerlab.target play --policy <id> --dry-run --slot 2 --reserve-usd 0
   uv run python -m careerlab.target play --policy <id> --spend --slot 2 --reserve-usd 0 --why "clave propia"
   ```

   - `--reserve-usd 0`: la reserva de 15 USD es de la clave del reto, no de esta.
   - `--slot`: uno que no esté usando otro chat (hoy hay `slot0`–`slot2`). Cada hueco copia su propio `.env`.
   - Los scripts del banco (`ds.py`, `bench.py`, `perceive.py`) leen el mismo `CAREERLAB_TARGET_ENV`. Su freno en `ds.py` se calcula sobre el uso de la clave del reto (`LINE_START_USAGE`), así que con la clave propia no vale tal cual.

## Pendiente

- Comprarla necesita el visto bueno de Alejandro (`NORMAS.md` §4).
- En el registro, estas partidas siguen apareciendo como `route competition-key`. La única marca de que se jugaron con la clave propia es `--why`.
- Zona gris de las normas: usar otra clave para desarrollo local no está prohibido expresamente, pero *"the absence of an express prohibition is not permission"*. Nada de esto entra en la entrega.
