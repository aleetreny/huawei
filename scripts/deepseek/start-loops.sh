#!/bin/zsh
# Start one game loop per slot: start-loops.sh <cap> <policy for slot 0> <policy slot 1> <policy slot 2> [games]
cd "${0:A:h}/../.."
export CAREERLAB_RUNNER_DIR="/Users/alejandrotreny/Library/Mobile Documents/com~apple~CloudDocs/Github/huawei/local-runs/official-runner"
export CAREERLAB_TARGET_ENV="$CAREERLAB_RUNNER_DIR/.env"
cap=$1; shift; games=${4:-4}
for s in 0 1 2; do
  pol=${@[$((s+1))]}
  [ -n "$pol" ] && [ "$pol" != "-" ] && nohup scripts/deepseek/gameloop.sh $pol $s $games $cap >> ~/careerlab-data/deepseek/loop-slot$s.log 2>&1 &
done
