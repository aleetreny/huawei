#!/bin/bash
# usage: run_probe.sh TAG [MAX_DECISIONS]  -> one game of the official runner against fake_multi.py (0 USD), in Formato's slot-fake.
# Starts the JiuwenSwarm instance of slot-fake (one at a time on this Mac), plays, stops it. Logs in ~/careerlab-data/comprobante/fake/TAG/.
set -u
B=$HOME/careerlab-data/comprobante/fake; TAG=$1; MAXD=${2:-50}; OUT=$B/$TAG; mkdir -p "$OUT"
S=$HOME/careerlab-data/formato/slot-fake; SOL=$HOME/careerlab-data/comprobante/sol-probe
HERE=$(cd "$(dirname "$0")" && pwd)
python3 "$HERE/fake_multi.py" 18999 "$OUT/requests.jsonl" "$MAXD" > "$OUT/fake.out" 2>&1 &
FAKE=$!
sleep 1
URL=$(bash $HOME/careerlab-data/formato/up.sh "$S"); echo "url=$URL" > "$OUT/info.txt"
cd "$S/runner"
env -i PATH="$PATH" USER="$USER" HOME="$S/home" uv run python -m career_sim_runner play --submission "$SOL" --ws-url "$URL" --timeout-s 1500 < /dev/null > "$OUT/play.log" 2>&1
echo "play_exit=$?" >> "$OUT/info.txt"
bash $HOME/careerlab-data/formato/down.sh "$S"
kill $FAKE 2>/dev/null
D=$(grep -o 'output_dir: .*' "$OUT/play.log" | tail -1 | cut -d' ' -f2-); [ -n "$D" ] && cp -R "$D" "$OUT/output"
echo DONE >> "$OUT/info.txt"
