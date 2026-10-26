# Fast race scripts (fastloop-v2, from 26 Oct 2026)

Rules: [lab/protocol/fastloop-v2.md](../../lab/protocol/fastloop-v2.md). Team page: [lab/fastloop/README.md](../../lab/fastloop/README.md). Live status: `lab/reports/carrera-rapida.md`.

| File | What it does |
|---|---|
| `driver.py` | The loop: one continuous scheduler (8 Haiku slots, five-hour cap 0.85, front-loaded weekly pace), a ladder step every minute, designers for the step's requests, `ladder add` for finished designs, the status page every 10 minutes. Never commits. |
| `design.py` | One headless designer (Opus, effort max; `FASTLOOP_DESIGN_MODEL`, `FASTLOOP_DESIGN_EFFORT`): writes a policy folder from the champion's Skills, digests of its games, `lab/fastloop/lessons.md` and `history.md`. Briefs in `lab/fastloop/briefs/`. |
| `calibrate.py` | The simulation behind the ladder thresholds. |

Working files go to `~/careerlab-data/huawei/fastloop/`: `driver.log`, `scheduler.out`, `design/<name>/` (digests, prompt, designer reply), `design-logs/`, `rejected/`.

## Switch the cloud race to the fast race (organiser, once)

From the repository root on `cloud-lab-run`, after merging this branch:

```sh
# 1. stop the old loop: no new batch, no ceiling lane, and cut the running batch
touch ~/careerlab-data/huawei/cloud-run/STOP
pkill -f scripts/cloud-run/driver.py; pkill -f scripts/cloud-run/ceiling.py
pkill -f "careerlab run --kind claude-cli"       # in-flight games become interrupted; they are never scored
pkill -f -- "--strict-mcp-config --mcp-config"   # their Haiku workers (this pattern never matches the organiser session)
export CAREERLAB_CLAUDE_EXE=~/claude-2.1.303/node_modules/.bin/claude   # same pin as before: same actor ids
uv run careerlab recover

# 2. start the ladder: champion = best expected score with 8+ race games (F1 on 26 Oct), cancel every other queued job
uv run careerlab ladder init --cancel-others --why "fast race (fastloop-v2), Alejandro 26 Oct"
uv run careerlab ladder add observed-growth-v3 --kind external --why "Matteo: 8 games in his cell, mean 51.0, 5/8 completed"
uv run careerlab ladder add f3-lean-v1 --kind external --why "race contender: 5/5 completed, mean 56.7; plays to 8 games"
uv run careerlab ladder add f3-balance-recombined-v1 --kind external --why "race contender: 6/7 completed, mean 56.5; plays to 8 games"
uv run careerlab ladder add f1-risk-signal-v1 --kind targeted --why "F1 + Defuse on any non-reassuring risk remark (block-5 child)"
uv run careerlab ladder add f1-core-v1 --kind targeted --why "F1 without unused text: same play, fewer tokens"
uv run careerlab ladder step --apply

# 3. start the driver (detached)
mkdir -p ~/careerlab-data/huawei/fastloop
setsid nohup uv run python scripts/fastloop/driver.py >> ~/careerlab-data/huawei/fastloop/driver.out 2>&1 < /dev/null &
```

Stop it with `touch ~/careerlab-data/huawei/fastloop/STOP` (games in flight finish). Restarting is safe: the state lives in `lab/fastloop/state.json` and the registry; the driver refuses to start a second scheduler.

## Organiser routine while it runs (hourly, as before)

1. `git fetch origin --prune`; merge finished team branches; for every merged team manual: `uv run careerlab ladder add <name> --kind external --why "<author>: <evidence>"` (`--first 4` only if it brings 4+ games from another cell with a mean at least the champion's).
2. `uv run careerlab export`; `uv run careerlab ladder status --write`.
3. Commit `lab/registry`, `lab/fastloop/` (state, history, lessons), `lab/reports/carrera-rapida.md` and the new designer folders under `lab/policies-src/`; push `cloud-lab-run` and fast-forward `main` after `uv run pytest -q`.
4. After every new champion, and at least every three hours, add to `lab/fastloop/lessons.md` what the finished challengers taught (one line each, with numbers). The designers read it: this is how discoveries carry over.
5. Look at `~/careerlab-data/huawei/fastloop/driver.log`: repeated designer failures or rejected designs need a look (`design/<name>/designer-reply.md`).
