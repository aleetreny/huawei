# CareerLab cloud portability test — 26 October 2026

Does the CareerLab laboratory (`careerlab/`, `lab/`) at `main` 32a8082 install and run in a Claude Code cloud container? How fast does the game run there, and can Claude workers play there? Everything below was measured in one container on 26 Oct 2026 between 12:57 and 13:30 UTC. Results stay in that container's own `CAREERLAB_DATA`; nothing was merged into the local registry on the Mac.

Rules followed: work only inside the repository checkout; no game packages changed; no files read inside the installed `career_emulator` / `career-emulator-*` packages; no `.sqlite3` game database opened. Run summaries were read from the lab's own `result.json` / `bench_summary.json` files only.

## Verdict

| Step | Result |
|---|---|
| 1. `uv sync`, dataset update, `careerlab doctor` | **PASS** |
| 2. `uv run pytest -q` | **PASS**: 142 passed, 1 skipped on a fresh clone; 143 passed after `git fetch origin Matteo` |
| 3. `careerlab isolation` | **PASS**: all four expected properties hold |
| 4. Throughput, 8 and 16 slots | **PASS**: about 144 steps/s, CPU-bound at 4 vCPUs (about 27 % of the Mac's 530 steps/s) |
| 5. Claude CLI episode end to end | **IN PROGRESS**: CLI present and authenticated; one Haiku episode running (results follow in the next commit) |
| 6. This report on branch `cloud-portability-test` | done |

## Environment

| Item | Value |
|---|---|
| Host | Claude Code on the web, managed remote container (KVM guest) |
| OS | Ubuntu 24.04.5 LTS, Linux 6.18.44, x86_64 |
| CPU | 4 vCPUs (`nproc` = 4), Intel Xeon @ 2.10 GHz, 1 thread per core |
| Memory | 15 GiB, no swap; about 0.5 GiB used at idle |
| Disk | 30 GB writable allowance free at start |
| Network | outbound HTTPS through the environment's agent proxy (PyPI downloads and the Claude API both worked) |
| Python | 3.13.17 (`/usr/bin/python3.13`, pre-installed; uv did not download one) |
| uv | 0.11.32 |
| Node / Claude Code CLI | Node 22.22.0, `claude` 2.1.310 at `/opt/node22/bin/claude` |
| git | 2.43.0 |
| Repository | `aleetreny/huawei` at `main` 32a8082 (clean checkout) |
| Paths | `CAREERLAB_DATA` default `/root/careerlab-data/huawei` (container-local, ephemeral), `CAREERLAB_LAB_DIR` `/home/user/huawei/lab` |

Installed versions (from `doctor` and `uv pip list`): career-emulator-engine 1.0.6, career-emulator-techarena 1.0.8, fastmcp 2.14.7, mcp 1.27.2, numpy 2.5.4, scipy 1.18.1, pytest 9.1.1, pytest-asyncio 1.4.1. These match the pins in `pyproject.toml` and the official runner lock.

## Step 1 — install, dataset update, doctor: PASS

```sh
uv sync
uv run career-emulator-engine update --source distribution --split dev
uv run careerlab doctor
```

- `uv sync`: resolved 101 packages and installed 91 in **3 min 11 s** wall time. Only 2.9 s of that was user CPU, so the time went on downloads through the proxy. A fresh container pays this again (see Problems).
- Dataset update: 3.8 s, printed `Dataset updated at: …/.venv/lib/python3.13/site-packages/career_emulator/data/dataset`.
- `doctor` (0.8 s) reported every expected value: the venv's `career-emulator-engine-mcp` as the MCP executable, `/opt/node22/bin/claude` as the Claude executable, the official engine variables (`ACTIVE_LONG_CHAIN_LIMIT=1`, `MONTHLY_EVENT_LIMIT=3`, `MAX_NOTE_LENGTH=1000`), the gate as committed (scripted, claude-cli and native-subagent allowed) and `official_runner_present: false` (expected: `scripts/setup_official_runner.sh` was not run). The Claude CLI was **available**: `{"loggedIn": true, "authMethod": "oauth_token", "subscriptionType": null}`.
- Harmless warnings on every command: `UV_NATIVE_TLS is deprecated` (set by the environment, not the repo) and fastmcp's `AuthlibDeprecationWarning`.

## Step 2 — unit tests: PASS

```sh
uv run pytest -q
```

- Fresh clone: **142 passed, 1 skipped**, 1 warning, 12.9 s.
- The skip is `tests/test_compliance.py::test_m3_is_verbatim_teammate_text`: "teammate commit 27cd3c1 not available locally". The cloud clone fetches only `main` and the session branch; 27cd3c1 is the tip of `origin/Matteo`.
- After `git fetch origin Matteo`, the test passes and the suite gives **143 passed**, 0 skipped, 12.0 s.

## Step 3 — isolation: PASS

```sh
uv run careerlab isolation      # 15 s
```

```json
{
  "root": "/root/careerlab-data/huawei/servers/isolation-r2s36qgs",
  "T1_separate_db_visible_from_other_process": [false, "observe failed: {'current_state': {'error': 'Unknown session_id: 4028062f9a5a466ca51f7d82b92105c0'}, 'current_event': None, 'choices': [], 'events': ''}"],
  "T2_same_db_visible_from_other_process": [true, "observed"],
  "T3_actions_on_one_session_leave_other_unchanged": true,
  "T3_distinct_session_ids": true,
  "T4_concurrent_observe_returns_own_session": true,
  "T5_competition_mode_second_new_game": {
    "first": {"session_id": "3ab2bcd81a514ced8da65b8cb5e16db3"},
    "second": {"error": "Competition mode: only one game session is allowed."}
  },
  "T6_default_db_shared_across_cwds": {"visible_from_other_cwd": true, "files_created_in_cwd": []}
}
```

| Expected property | Observed |
|---|---|
| A separate `CAREER_EMULATOR_DB` is isolated | yes: T1 `false` (Unknown session_id from the other process) |
| The same path is shared | yes: T2 `true` |
| The default DB is shared across folders | yes: T6 `visible_from_other_cwd: true` |
| Competition mode rejects a second `new_game` | yes: T5 second call returns the error |

The extra checks also hold: T3 sessions on one server do not affect each other, and T4 concurrent `observe` calls return their own sessions. This is the same result as on the Mac (`findings.md`).

## Step 4 — throughput: PASS (CPU-bound)

```sh
uv run careerlab bench --slots 8  --episodes 64 --actor quarterly-wellbeing
uv run careerlab bench --slots 16 --episodes 96 --actor quarterly-wellbeing
uv run careerlab bench --slots 4  --episodes 96 --actor quarterly-wellbeing   # extra: exercises pool rotation
```

Memory and load were sampled every 0.5 s with `free -m` and `/proc/loadavg` (system-wide; about 0.5 GiB used before each run).

| Run | slots | episodes | start-up s | elapsed s | **steps/s** | **episodes/s** | mean steps | median observe ms | median action ms | processes started | peak used memory | peak load1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| requested | 8 | 64 | 3.20 | 13.29 | **144.5** | **4.81** | 30.0 | 15.8 | 34.1 | 8 | 1.13 GiB | 2.3 |
| requested | 16 | 96 | 7.68 | 16.92 | **142.9** | **5.67** | 25.2 | 35.2 | 62.8 | 16 | 1.71 GiB | 7.9 |
| extra | 4 | 96 | 1.32 | 23.24 | 103.2 | 4.13 | 25.0 | 10.1 | 23.1 | 10 (4 + 6 rotations) | 0.97 GiB | 6.7 |

(The 1-minute load average lags; the 13–23 s runs are too short for it to reach its steady value.)

Notes on the numbers:
- **Steps/s is the comparable figure.** Episodes/s depends on episode length: the 16-slot run includes seeds 64–95, which ended sooner (25.2 vs 30.0 mean steps).
- **The ceiling is about 143 steps/s, set by the 4 vCPUs.** Going from 8 to 16 slots adds no throughput and doubles per-call latency (observe 16 → 35 ms, action 34 → 63 ms). The cloud total is **about 27 % of the Mac's 530 steps/s** with 16 processes. Two factors combine: 4 cores instead of 18, and slower calls. Even the least-loaded run here (4 slots: observe 10 ms, action 23 ms) is about 1.6× slower per call than the Mac's ≈ 6 ms + ≈ 14 ms.
- **Start-up** is about 0.3–0.5 s per server process (1.3 s for 4, 3.2 s for 8, 7.7 s for 16).
- **Pool rotation works here.** The 4-slot run gave 24 episodes per slot against `sessions_per_db = 12`, so every slot rotated to a fresh database (10 processes started, peak 7 alive during overlap). All 96 episodes were terminal; none were interrupted. The two requested runs never rotate (at most 8 episodes per slot).
- **The game behaves as it does on the Mac.** All 256 bench episodes were `eliminated`, with 0 rejected actions and 0 interrupted. Median survival was 6–8 months (maximum 19) and mean quantitative_score 12.4–13.3 (SD about 4.5). The Mac's P1 pilot gave quarterly-wellbeing 12.51 (SD 4.74) with a median 6–7.5 months.
- **Memory is not a constraint:** about 80 MiB per slot (server process plus its share of the client), and at most 1.7 GiB of 15 GiB used.
- **Projection for full episodes:** at about 143 steps/s and 170–200 actions per 48-month episode, this container could run about 0.7–0.8 full scripted episodes per second (about 2,600–3,000 per hour), against about 3/s on the Mac. Scripted actors never reach month 48 in practice, so this figure is an upper bound.
- **Recommended setting here:** `--slots 6`–`8` for scripted runs; more slots only add latency.

## Step 5 — Claude CLI worker: in progress

`claude` 2.1.310 is installed and `claude auth status` reports `loggedIn: true`, `authMethod: oauth_token`. Policy p0-minimal-v1 was registered as `ed78f44ccd41adf8` and job `infr-ed78f44c-017798-00000-a1` (claude-cli:haiku, purpose infra) was enqueued and started at 13:05:36 UTC. The episode was still running when this version was committed; the results follow in the next commit.

## Problems found and fixes needed

1. **Run data is ephemeral (main risk).** `CAREERLAB_DATA` defaults to `/root/careerlab-data/huawei` inside the container. The container is reclaimed after inactivity and everything there is lost: the registry, `result.json` files and trajectories. A cloud worker therefore has to run `careerlab export` and move the JSONL (and any `result.json` the orchestrator needs) off the container before the session ends. Trajectories must not be committed (`lab/README.md`), so they either die with the container or need storage outside Git. Fix needed: a documented "end of cloud session" step, for example export to a dedicated results branch, kept separate from the local registry as decided.
2. **Install time on every fresh container.** `uv sync` took 3 min 11 s (network-bound) and has to be repeated in each new container, followed by the dataset update. Fix: put `uv sync && uv run career-emulator-engine update --source distribution --split dev` in the environment's setup script, or add a SessionStart hook, so a session starts ready to run.
3. **One unit test is skipped on a fresh cloud clone.** `test_m3_is_verbatim_teammate_text` needs teammate commit 27cd3c1 (`origin/Matteo`), which the cloud clone does not fetch. Fix: run `git fetch origin Matteo` before `pytest` (then all 143 pass), and mention it in `lab/README.md` or the setup script. The skip is honest (`pytest.skip`), not a failure.
4. **Throughput is CPU-bound at 4 vCPUs**, about 143 steps/s: about a quarter of the Mac. Splitting large scripted screens across several cloud sessions would scale roughly linearly (each session has its own container and its own data directory), but each one then needs the export/merge step from problem 1. For scripted work, the Mac remains the faster single machine.
5. **Claude worker quota and account.** Pending the result of step 5.
6. **Cosmetic warnings.** Every command prints `UV_NATIVE_TLS is deprecated` (an environment variable set by the cloud environment; the fix is `UV_SYSTEM_CERTS` on the environment side, nothing in the repo) and fastmcp's `AuthlibDeprecationWarning` (upstream; pinned by the official lock, so leave it).
7. **No code changes were needed.** The configurable paths worked unchanged: the defaults resolved under `/root`, and the venv's MCP executable and the `claude` on `PATH` were found automatically. Nothing in the repository was modified apart from this report. The runs created the empty `lab/policies/` directory (created by `Settings.ensure()`; Git does not track empty directories).

## What was not done

- `scripts/setup_official_runner.sh` (official JiuwenSwarm target runner) was not run; it was outside the scope of this task.
- No registry export or merge was made; per instructions, cloud results stay separate from the local registry.
