#!/bin/sh
# Choice test for t13-perc against t13-final (Leah's stat-perception line). Run from the repo root.
T=$HOME/careerlab-data/transmision
export CAREERLAB_CLAUDE_EXE=$(which claude) UV_PYTHON_PREFERENCE=only-managed
run() { uv run python scripts/transmision/runbench.py run --items $T/bank-items.jsonl --ids "$1" --variant "$2" --name "$3" --context month --slots 4 --max-five-hour 0.80 2>&1 | grep -v -i "authlib\|compatible"; }
run $T/ids-pre-A.txt   lab/policies-src/stat-perception/t13-perc/bundle  perc-pre
run $T/ids-pre-A25.txt lab/policies-src/transmision/t13-final/bundle     t13own-pre
run $T/ids-G1-70.txt   lab/policies-src/stat-perception/t13-perc/bundle  perc-g1
echo ALL-DONE
