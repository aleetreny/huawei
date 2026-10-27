#!/bin/bash
# usage: up.sh SLOTDIR  -> reload dataset + start instance, prints ws url
S=$1; cd "$S/runner"
# one start at a time across all slots on this machine (ports are taken in order of availability)
exec 9>/tmp/careerlab-formato-start.lock; while ! mkdir /tmp/careerlab-formato-start.d 2>/dev/null; do sleep 5; done
trap "sleep 60; rmdir /tmp/careerlab-formato-start.d" EXIT
export HOME="$S/home"
uv run career-emulator-engine update --source distribution --split dev < /dev/null > "$S/dataset.log" 2>&1 || { echo DATASET_FAIL; exit 1; }
uv run jiuwenswarm-start --name career_emu all < /dev/null > "$S/jiuwen.log" 2>&1 &
for i in $(seq 1 90); do
  line=$(uv run jiuwenswarm-start --list 2>/dev/null | awk '$1=="career_emu" && $2=="running"')
  if [ -n "$line" ]; then port=$(echo "$line" | awk '{print $NF}' | cut -d/ -f1); nc -z 127.0.0.1 $port 2>/dev/null && { echo "ws://127.0.0.1:$port"; exit 0; }; fi
  sleep 2
done
echo NO_INSTANCE; exit 1
