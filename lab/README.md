# CareerLab

The laboratory that generates, evaluates and archives Career Survival policies through the official MCP server. The method and its justification are in [`research/careerlab/method-decision.md`](../research/careerlab/method-decision.md); the pre-registered statistics are in [`protocol/prereg-v1.md`](protocol/prereg-v1.md).

## Install (reproducible)

```sh
uv sync                                    # careerlab + engine 1.0.6 + dataset 1.0.8, every shared
                                           # dependency constrained to the official runner lock
uv run career-emulator-engine update --source distribution --split dev
uv run careerlab doctor                    # versions, paths, CLI account, gate
uv run pytest -q                           # unit tests (no real game)
sh scripts/setup_official_runner.sh        # official JiuwenSwarm runner @ 00b084a8 (target actor)
```

Python 3.13 (`.python-version`). The game server is always started from the installed `career-emulator-engine-mcp` over stdio, with `--update skip` and the engine variables of the official runner (`CAREER_EMULATOR_ACTIVE_LONG_CHAIN_LIMIT=1`, `CAREER_EMULATOR_MONTHLY_EVENT_LIMIT=3`, `CAREER_EMULATOR_MAX_NOTE_LENGTH=1000`) and a private `CAREER_EMULATOR_DB` per server process.

## Paths (move to the cloud by changing environment variables)

| Variable | Default | Holds |
|---|---|---|
| `CAREERLAB_DATA` | `~/careerlab-data/huawei` | registry SQLite (WAL), game databases, run directories, trajectories |
| `CAREERLAB_LAB_DIR` | `<repo>/lab` | gate, protocol, policy sources, registry exports (tracked in Git) |
| `CAREERLAB_RUNNER_DIR` | `<repo>/local-runs/official-runner` | official participation runner |
| `CAREERLAB_MCP_EXE`, `CAREERLAB_CLAUDE_EXE` | from the environment | executables |

Live SQLite files are kept outside the iCloud-synced repository on purpose. Each machine runs its own planner and pool; merge results by exporting the registry (`careerlab export`) and importing JSONL.

## Daily use

```sh
uv run careerlab register lab/policies-src/<family>/<policy>      # immutable, content-hashed
uv run careerlab enqueue --policy <id> --actor scripted --n 20 --purpose screen --why "<decision>"
uv run careerlab run --kind scripted --slots 12                   # rotating stdio pool
uv run careerlab resume                                           # after any crash: observe first, then continue or replace
uv run careerlab status
uv run careerlab export                                           # registry -> lab/registry/*.jsonl
```

`enqueue` refuses work that `gate.json` does not authorise. Real-game Claude workers were opened by the user's decision of 26 Oct (see `gate.json` and `ESTADO.md`). `uv run careerlab lint <policy dir>` checks a proposed policy without registering it.

## Results panel

`lab/panel/index.html` shows the leaderboard, scores over time, the bots and other machines' results. Rebuild its data with `uv run python scripts/panel/build.py` after `git fetch origin`. See [panel/README.md](panel/README.md).

## Playing from a second machine (T11)

The cloud race owns the canonical registry and `lab/registry/`. Any other machine plays under its own **origin**:

```sh
uv run careerlab origin set leah       # stored in the untracked .careerlab-origin (or export CAREERLAB_ORIGIN=leah)
uv run careerlab import                # optional: pull the race's policies, actors and results from lab/registry/
uv run careerlab enqueue --policy <id> --actor scripted:quarterly-wellbeing --n 20 --purpose screen --why "..."
uv run careerlab run --kind scripted --slots 4
uv run careerlab export                # writes lab/registry-origins/leah/, never lab/registry/
```

With an origin set:

- job ids start with the origin (`leah-scre-…`), and replicate numbers sit in a block of their own, so they never clash with the race's or another machine's;
- the data directory defaults to `~/careerlab-data/huawei-<origin>`;
- `run`, `recover` and `resume` only touch this origin's jobs; imported race jobs are never leased;
- block decisions and `report` count this origin's launches only (`report --all-origins` shows everything). The race's prereg-v1 launch order is never changed by another machine;
- `export` only writes this origin's jobs, evaluations and decisions to `lab/registry-origins/<origin>/`.

Every `export` refuses (exit 4) if the target folder already holds rows the local registry lacks. This stops a stale machine from deleting the race's results; run `careerlab import --dir <folder>` first, or pass `--force` only if you mean it. The organiser merges a machine's results into the race with `careerlab import --dir lab/registry-origins/<origin>` and checks that `conflicts` is 0. Merged runs keep their origin and stay out of the race's decisions.

## Layout

```
careerlab/            client, pool, episode runner, registry, scheduler, actors, stats, synthetic, search
lab/gate.json         authorisation gate (edited only after a written answer or a user decision)
lab/protocol/         frozen pre-registration (hashes recorded in the registry)
lab/policies-src/     policy bundles: policy.json + bundle/{manifest.json, skills/*/SKILL.md} or scripted.json
lab/registry/         JSONL exports committed to Git (no trajectories, no game text, no secrets)
lab/reports/          generated reports
```

Trajectories contain development-dataset text returned by the game; they stay under `CAREERLAB_DATA` and are referenced by path and SHA-256, never committed. One exception: `careerlab digest` summaries under `lab/reports/teacher-digests/` (26 Oct) carry shortened game text so the cloud race can study Opus games. They are development material for this private repository only, and no phrase from them may go into a Skill.
