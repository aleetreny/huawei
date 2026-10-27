#!/bin/zsh
# Official DeepSeek games in one slot, one after another, until the key's usage reaches a cap.
# Never stops a game in play (CAREERLAB_TARGET_NEVER_STOP=1 turns the per-game watchdog off): the cap is
# checked only before starting the next one.
#
#   scripts/deepseek/gameloop.sh <policy> <slot> <games> <usage cap USD> [why]
#
# Needs CAREERLAB_RUNNER_DIR and CAREERLAB_TARGET_ENV (the runner checkout and its .env). Waits while the
# slot is busy. Writes one JSON result per game to ~/careerlab-data/deepseek/games/<policy>-slot<slot>-<n>.json.
# Create ~/careerlab-data/deepseek/STOP to stop after the current game.
policy=$1; slot=$2; games=$3; cap=$4; why=${5:-"DeepSeek score line, 27 Oct (Alejandro: up to 10 USD today)"}
cd "${0:A:h}/../.." || exit 1
export PYTHONWARNINGS=ignore CAREERLAB_ORIGIN=deepseek CAREERLAB_TARGET_PARALLEL=1 CAREERLAB_TARGET_NEVER_STOP=1
out=~/careerlab-data/deepseek/games; mkdir -p $out
for n in $(seq 1 $games); do
  while [ -e ~/careerlab-data/huawei-deepseek/target-slots/slot$slot.busy ] || \
        lsof ~/careerlab-data/huawei-deepseek/target-slots/slot$slot.lock >/dev/null 2>&1; do sleep 20; done
  [ -e ~/careerlab-data/deepseek/STOP ] && { echo "STOP file: stopping"; exit 0; }
  usage=$(uv run python -c "from pathlib import Path; import os; from careerlab.target import key_status; print(key_status(Path(os.environ['CAREERLAB_TARGET_ENV']))['usage'])" 2>/dev/null)
  if (( usage >= cap )); then echo "key usage $usage >= cap $cap: stopping"; exit 0; fi
  echo "$(date -u +%H:%M) slot $slot game $n of $policy (key usage $usage)"
  uv run python -m careerlab.target play --policy $policy --spend --games 1 --slot $slot --max-usd-per-game 20 \
     --reserve-usd 15 --purpose pilot --why "$why" > $out/$policy-slot$slot-$n.json 2> $out/$policy-slot$slot-$n.err
  echo "$(date -u +%H:%M) slot $slot game $n done (exit $?)"
done
