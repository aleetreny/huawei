#!/bin/bash
# Cola de partidas oficiales: lanza la siguiente cuando hay menos de MAX en curso; no corta ninguna partida;
# se para si el saldo de la clave baja de MIN_USD. Uso: scripts/corte3/cola.sh "mv-4 mv-3 mv-4 ..." "0 2 3 5 6"
cd "$(dirname "$0")/../.." || exit 1
export PYTHONWARNINGS=ignore CAREERLAB_ORIGIN=deepseek CAREERLAB_RUNNER_DIR=$HOME/huawei/local-runs/official-runner \
  CAREERLAB_TARGET_ENV=$HOME/huawei/local-runs/official-runner/.env CAREERLAB_TARGET_PARALLEL=1 CAREERLAB_TARGET_NEVER_STOP=1
MAX=${MAX:-2}; MIN_USD=${MIN_USD:-0.6}
read -r -a QUEUE <<< "$1"; read -r -a SLOTS <<< "$2"
running() { ps -axo command | grep "[c]areerlab.target play" | grep -v "uv run" | wc -l | tr -d ' '; }
slot_busy() { ps -axo command | grep "[c]areerlab.target play" | grep -v "uv run" | grep -q -- "--slot $1 "; }
remaining() { uv run python -c "from pathlib import Path; import os; from careerlab.target import key_status; print(key_status(Path(os.environ['CAREERLAB_TARGET_ENV']))['limit_remaining'])" 2>/dev/null; }
n=0
for pol in "${QUEUE[@]}"; do
  while [ "$(running)" -ge "$MAX" ]; do sleep 20; done
  rem=$(remaining); if awk "BEGIN{exit !($rem < $MIN_USD)}"; then echo "$(date -u +%H:%M) saldo $rem < $MIN_USD: paro"; exit 0; fi
  slot=""; for s in "${SLOTS[@]}"; do slot_busy "$s" || { slot=$s; break; }; done
  [ -z "$slot" ] && { sleep 20; continue; }
  n=$((n+1)); out=~/careerlab-data/deepseek/games/c3cola-$pol-slot$slot-$n
  echo "$(date -u +%H:%M) lanzo $pol en la ranura $slot (saldo $rem)"
  nohup uv run python -m careerlab.target play --policy "$pol" --spend --games 1 --slot "$slot" --max-usd-per-game ${MAXG:-1.2} \
    --reserve-usd ${RES:-0.2} --purpose confirm --why "Corte 3 (1 nov): $pol vs mv-3/mv-4 to choose the final submission (Alejandro)" \
    > "$out.json" 2> "$out.err" &
  sleep 45
done
echo "$(date -u +%H:%M) cola terminada"
