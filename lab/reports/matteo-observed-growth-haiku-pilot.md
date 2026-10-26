# observed-growth-v1: first autonomous Haiku pilot

## Result

The user authorised local testing through their personal Claude subscription after selecting cloud testing initially. One isolated autonomous Haiku episode completed all 48 months: **64.78/100, L5, 201 actions, 475.9 seconds**. The candidate was `observed-growth-v1`, source commit `bbc7b63`, bundle SHA-256 `f03981dac92f8b6c56cc1b62e7fbe4e6d3e374e8dd9525af26ae8d90e6794c42`. The frozen copy matched the source at completion. Codex did not select gameplay actions or edit instructions mid-run.

| Final dimension | Observation |
|---|---:|
| Health / dignity | 9 / 10 |
| Skill | 110 |
| Network | 33 |
| Output | 29 |
| Wealth displayed | 29 |
| Wealth in ending report | 29.1 |

Promotions: L2 month 6, L3 month 12, L4 month 24, L5 month 48. Reviews: C, B, B, B, B, A, A, A. Minimum observed Health was 3. There were zero rejected actions, one created game session and no non-game tool attempts.

## Configuration and scope

Claude Code 2.1.303, alias `haiku`, resolved model `claude-haiku-5-5`, official prompts and five MCP tools. Registered-configuration hash **08e9167a965ed82c** matches the actor listed in Ale's fetched cloud report. Engine 1.0.6, dataset 1.0.8, FastMCP 2.14.7, competition mode, official engine environment. Matching this recorded hash does not independently confirm unchanged backend routing or model behaviour; retain resolved-model information in comparisons.

Authentication used the user's Claude Pro subscription, not an API key. An initial technical attempt failed before creating a session because the new venv lacked the dataset. The official distribution update fixed it; that attempt remains interrupted and has no score.

## Resource use

Elapsed gameplay: about 7.9 minutes. CLI reported 408 ordinary input tokens, 62,201 output tokens, 205,079 cache-creation input tokens and 21,372,696 cache-read input tokens. Repeated context reads are counted repeatedly; this is not that many unique tokens. List-price-equivalent reported cost was about USD 1.094, **not an additional bill on the subscription**. Overage was disabled in the returned rate-limit metadata.

During the successful episode, account-wide five-hour utilisation changed from 0 to 9%, and weekly utilisation from 0 to 1%. These deltas can include unrelated concurrent account use. One pilot was run; no continuing queue or background fleet was started.

## Behaviour and interpretation

Quarterly actions included 14 key projects, 17 report-preparation actions, 7 health recoveries, 7 legacy-risk cleanups, 7 network-maintenance actions, one mentorship, one results report, one mental recovery and one high-intensity work action. These are action counts, not proof of correct decision-making or causal effects.

The manual is executable by Haiku and produced a full career in this trial. It did not demonstrate faster progression: L5 arrived at month 48, later than the two historical manual Codex exercises at month 42. Actor and environment differences prevent attributing that difference to the manual alone. Repeated key-project choices and relatively low final Network are reasons to audit how the actor implements gap selection and realized-benefit checks, not evidence of a universal better action.

This is one exploratory episode, outside a centrally scheduled comparison block. Do not compare its raw score directly with a posterior Y estimate or claim superiority over Ale's incumbent. Fresh actor-matched candidate and incumbent episodes under the frozen protocol remain necessary.

## Relevo

Numeric evidence, hashes and complete configuration: [JSON summary](matteo-observed-growth-haiku-pilot.json). Raw public-tool responses and worker streams remain outside Git under the user's isolated `careerlab-data/matteo-haiku` directory. Local `run-pilot.py` freezes the candidate and runs one isolated episode using the existing lab worker. No cloud/default registry was imported, written or exported; this does not implement general T11 registry reconciliation.

Installed the pinned CLI, verified subscription authentication, updated the dataset with the official command and completed one pilot. The prior missing-dataset attempt is retained as an interruption. No further runs are queued. Next: inspect adherence to realized-benefit checks and feedback gaps; then decide a small actor-matched block within a user-approved quota allowance. Keep this candidate immutable and version any revised manual separately. The cloud request in the earlier report remains a separate, pending central evaluation.
