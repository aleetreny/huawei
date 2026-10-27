#!/bin/sh
# Run bank arms one after another: drive.sh <items> <ids> <slots> <arm=variant> ...
items=$1; ids=$2; slots=$3; shift 3
export CAREERLAB_CLAUDE_EXE=$HOME/claude-2.1.303/node_modules/.bin/claude
cd /home/user/huawei
for spec in "$@"; do
  arm=${spec%%=*}; variant=${spec#*=}
  ctx=month; case $arm in *-long) ctx=long;; esac
  uv run python scripts/transmision/runbench.py run --items "$items" --ids "$ids" --variant "$variant" --name "$arm" --context $ctx --slots "$slots" --max-five-hour 0.65
done
