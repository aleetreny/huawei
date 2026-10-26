# Evaluating Sustainable Career v0.1

## Current status

Three candidate Skills are in `solution/skills/`. There is no published maximum Skill count in the submission instructions checked on 26 October 2026; they require at least one. This is not permission to ignore later organizer clarifications.

The proposed 100-run evaluation has not started. The competition key is not yet available, and the manifest needs the team's confirmed registered identity. Do not describe random runs or manual Codex-assisted tests as completed runs of the designated competition agent.

Initial checks: all three Skills passed the Skill Creator front-matter validator. A separate manual Codex-assisted exercise reached month 2 after acknowledging the handbook and making three story decisions. This is a partial exercise, not a completed career or evidence of score improvement. The official runner's validation was not executed successfully in the standalone browser environment because that environment lacks a runner dependency (`ruamel.yaml`); use the official checkout's `make sync` rather than treating the browser environment as equivalent.

## Two different test modes

### Manual Codex-assisted exercise

Codex can read the Skills and select choices through the official MCP tools as a manual development exercise. No designated-model API call is made. The current Codex session still has its normal usage limits. Use a new session rather than the user's active browser game, and record the chosen rationale and observed consequences.

The purpose is to identify ambiguity, missing cases, conflicting priorities and tool-handling mistakes. It cannot isolate the benefit of the Skills from Codex's own reasoning or predict the designated model's performance. Large numbers of adaptive manual decisions are not equivalent in speed or cost to the previous random harness. Do not automate a different model or a heuristic script and label it the official agent.

### Official-model candidate runs

Use the official participation repository, exact JiuwenSwarm 0.2.4b3 pin, single-agent mode and the model name supplied by organizers. Clone and synchronize that repository separately from the manual browser environment; the pinned dependencies differ. Do not upgrade or substitute JiuwenSwarm.

Configure `API_BASE`, `API_KEY` and `MODEL_NAME` locally according to the organizer email. Never commit or print the key. Confirm the registered team identity and create `solution/manifest.json` with that identity, a candidate name, `mode: agent` and the routing instruction below. Install the candidate through the official runner.

Suggested manifest instruction:

> Read career-risk-review before choosing actions. Use career-event-decisions for story choices and career-quarterly-planning for Energy and main-action phases. Apply these as one agent using the public handbook and current-run official tool feedback. Observe after actions, update priorities when new evidence appears, and continue until the session ends. Keep action notes concise. Do not delegate decisions to other agents or use fixed event-answer maps.

Within the official checkout, follow `make sync`, the documented environment setup, `make setup` and `make start-jiuwen`. Use the candidate's absolute path with the supported command:

```sh
uv run python -m career_sim_runner play --submission /absolute/path/to/huawei/solution
```

Do not pass `--continue` when evaluating independent runs. Use the public runner's emitted run artifacts and score report to record results; do not read the underlying simulation database. For final submission validation, also supply the real English presentation video. Local play can proceed without the video.

## Proposed 100-run target

1. Freeze the candidate version and the runner revision; record both before testing.
2. Run the first three sessions as an operational and consumption pilot. Check Skill discovery, proper tool use, terminal handling, token usage and any reported cost.
3. Estimate the cost of the remaining runs and the team's remaining authorized credit. Token totals alone are insufficient for dollar estimates without current pricing or provider billing information. Never assume 100 sessions fit within the USD 50 key allowance.
4. If the pilot works and the remaining budget permits, continue toward 100 total sessions, including the pilot. Stop on repeated operational failures, unavailable model, exhausted credit or ambiguous usage accounting.
5. If instructions change, start a new version and report its sessions separately. Do not silently combine results from different candidates.
6. Preserve per-run evidence needed for analysis: session and run IDs, survival months, quantitative score, terminal cause, ending contributions, review feedback and token/cost information when available.

The 100-run request is a target, not an assertion that credit or time is sufficient. Compare with a reasoned no-strategy baseline under the same model when resources permit; random play is only historical context. Formal ablations need additional allocation rather than silently reducing or mixing the candidate batch.

## Reporting

Report attempted runs, scored runs, failures of execution, survival distribution, completion rate, score mean and variability, failure categories and token use. Distinguish early in-game elimination from an infrastructure failure. Do not infer a fixed winning response from one event outcome or present development observations as hidden official rules.
