#!/bin/bash
# usage: game.sh SLOTDIR SOLUTIONDIR TAG  -> one official game; logs in $B/runs/TAG
B=$HOME/careerlab-data/formato; S=$1; SOL=$2; TAG=$3; OUT=$B/runs/$TAG; mkdir -p $OUT
W="/Users/alejandrotreny/Library/Mobile Documents/com~apple~CloudDocs/Github/huawei/.claude/worktrees/formato"
key() { (cd "$W" && CAREERLAB_ORIGIN=deepseek CAREERLAB_TARGET_ENV=$S/runner/.env uv run python -m careerlab.target key 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["usage"])'); }
U0=$(key); echo "usage_before=$U0" > $OUT/cost.txt
rm -rf "$SOL/skills/career-advisor/script/state"
URL=$(bash $B/up.sh $S); echo "url=$URL" >> $OUT/cost.txt
cd $S/runner
env -i PATH="$PATH" USER="$USER" HOME="$S/home" uv run python -m career_sim_runner play --submission "$SOL" --ws-url "$URL" --timeout-s 5400 < /dev/null > $OUT/play.log 2>&1
echo "play_exit=$?" >> $OUT/cost.txt
bash $B/down.sh $S
sleep 20; U1=$(key); echo "usage_after=$U1" >> $OUT/cost.txt
D=$(grep -o 'output_dir: .*' $OUT/play.log | tail -1 | cut -d' ' -f2-); [ -n "$D" ] && cp -R "$D" $OUT/output
cp -R "$S/home/.jiuwenswarm-instances/career_emu/agent/workspace/skills/career-advisor/script/state" $OUT/advisor-state 2>/dev/null
grep -a -E "quantitative_score|termination_reason|token_usage" $OUT/play.log | tail -3 >> $OUT/cost.txt
echo DONE >> $OUT/cost.txt
