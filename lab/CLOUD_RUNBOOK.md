# Running CareerLab unattended in a Claude Code cloud session

Verified on 26 Oct 2026 (`lab/reports/cloud-portability-2026-10-26.md` on branch `cloud-portability-test`). The container has 4 vCPUs and 15 GiB of memory, and `claude` is authenticated through the session's OAuth token. A Haiku worker completed a 48-month episode in 7.7 minutes. Container storage is ephemeral, so everything that matters must be pushed.

```sh
uv sync
uv run career-emulator-engine update --source distribution --split dev
uv run careerlab import                      # lab/registry/*.jsonl -> this machine's registry
uv run careerlab recover
uv run careerlab status
echo '{"max_five_hour": 0.80}' > ~/careerlab-data/huawei/quota_cap.json   # the window is shared with every session on the account
uv run careerlab run --kind claude-cli --slots 6 --max-five-hour 0.80
```

The loop for one block:

1. Run the queued jobs.
2. Make the block decision for each actor (`careerlab.decisions.block_decision`). The rule is pre-registered and must not be changed.
3. Generate children only within progressive widening: at most ⌈(1 + N_f)^0.5⌉ per family, where N_f is the family's terminal episodes. Use the competition playbook only when a stall trigger fires.
4. Lint every new bundle and register it, then enqueue at least 3 Haiku runs for it.
5. `careerlab export`, then commit `lab/registry`, `lab/reports`, `findings.md` and new policy sources to the session branch and push.

Never commit run directories, game databases or trajectories.
