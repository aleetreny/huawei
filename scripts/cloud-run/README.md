# Cloud race scripts (cloud-lab-run, 26–27 Oct 2026)

These are the loop scripts the cloud session ran, kept so that a replacement session can resume. Working files go to `$CLOUD_RUN_DIR`, by default `~/careerlab-data/huawei/cloud-run`:

- `logs/`: batch and decision markers and the driver log;
- `next.md`, `teacher.md`, `relevo.md`: the free-text sections of the status report.

| Script | What it does |
|---|---|
| `driver.py` | Main lane. Runs every queued claude-cli job except purpose `pilot` (`careerlab run --slots 6 --max-five-hour 0.80 --limit <non-pilot queued>`). Then queues a replacement attempt for each interrupted slot (prereg-v1 3.4), records the Haiku block decision (`block_decision(..., record=True)`) and writes `logs/batch-N.done.json`. Stops at `END` or when `$CLOUD_RUN_DIR/STOP` exists. A one-shot `batch.json` (`{"slots": .., "limit": ..}`) overrides the next batch. |
| `ceiling.py` | T13 lane. Runs only `pilot` jobs with `--slots 2`. Ceiling jobs have priority −100, so the main lane's `--limit` never leases them. |
| `status.py` | Writes `lab/reports/historico/cloud-run-status.md`. |
| `lint.py` | Runs `lint_policy_tree` with `collect_titles` plus the story-event titles in the teacher digests. Usage: `lint.py [name filter]`. |

Start them detached from the repository root, after `uv sync` and with the CLI pin from `lab/reports/historico/cloud-run-status.md` (Relevo):

```sh
export CAREERLAB_CLAUDE_EXE=~/claude-2.1.303/node_modules/.bin/claude
setsid nohup uv run python scripts/cloud-run/driver.py >> ~/careerlab-data/huawei/cloud-run/driver.out 2>&1 < /dev/null &
setsid nohup uv run python scripts/cloud-run/ceiling.py >> ~/careerlab-data/huawei/cloud-run/ceiling.out 2>&1 < /dev/null &
```

Stop the driver before its `careerlab run` child. If the driver goes first, it cannot record a block decision for a batch that was cut short. Then run `careerlab recover`.
