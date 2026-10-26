# First-review rule transfer: actor-controlled pilot

## Current status

**Prepared, frozen and quota-blocked; zero gameplay episodes in this comparison have started.** On 26 October 2026, the personal Claude Pro account reported five-hour utilisation 99%, then returned `429 usage_limit_reached` at 100%. Reset reported by the service: **26 October 2026, 21:20 Europe/London (UTC)**. Weekly utilisation was 16%, with paid overage disabled. See [quota-block.json](quota-block.json). A `READY` preflight response is not a gameplay result.

**Matteo selected manual resumption.** No automation, background wait or gameplay queue is running. The reset time above is an observation from this preflight, not a scheduled start or a guarantee of future available quota.

Matteo authorised the proposed comparison after the black-box exploration. This pilot tests transfer of the prose, not a lookup-based research bot, a complete career score, or a race-selection decision. It is separate from the frozen prereg-v1 epoch and from the central cloud registry.

## Frozen comparison

- Baseline: existing `observed-growth-v1`, unchanged; bundle SHA-256 `f03981dac92f8b6c56cc1b62e7fbe4e6d3e374e8dd9525af26ae8d90e6794c42`.
- Candidate: `promotion-readiness-v1`, containing only the operational paragraphs of the general-rule draft; SHA-256 `599f7b405eb47ce10e5e8ed5246a00cadb91f2d90c2b353855871855aa7fe65a`. Research findings, numeric separator, answer catalogue and empirical model are absent.
- Four episodes per arm, in four time blocks with one independently generated episode per arm. Two workers at a time. Same Haiku actor, CLI 2.1.303, inline mode, isolated settings and five official tool names. The preflight resolved to `claude-haiku-5-5`; resolved models must be compared after execution.
- Engine 1.0.6, dataset 1.0.8, official engine settings, one competition server per session. Sessions are unseeded and unpaired; a time block is not an identical-state counterfactual.
- Shared research horizon: stop at the first observation of month 7, or an earlier game ending. The controller refuses actions beyond the horizon. No partial career is entered as a completed full-career score.
- Primary outcome: promoted at the first review **and** alive through month 6. Secondary: promotion, survival, adherence, usage and interruptions. Four episodes per arm are exploratory and cannot establish a general or reliable superiority claim.

[protocol.json](protocol.json) freezes the policies, prompt hashes, actor, schedule, environment, primary outcome and quota limits before gameplay. One prelaunch runner revision improved quota rejection reporting after the 429; both protocol revisions and source copies are retained locally. No gameplay outcome informed the revision.

## Isolation and budget

The actor receives only its frozen assigned Skill and the shared task/identity adapted to the research horizon. It has no filesystem tools, other MCP connections, user plugins, project instructions, catalogue or lookup. The controller journals official public before/after observations and actions without selecting choices for the actor.

Data root: `/Users/matteozabban/careerlab-data/matteo-first-review-transfer`, explicit origin `matteotransfer`, separate server storage. No central registry or full-career evaluation tables are written. Only the user's existing personal Claude subscription is used; no API key or paid overage is authorised. Do not start a pair if the current five-hour window is at or above 80%, the weekly window at or above 75%, or paid overage is active. A quota failure leaves the comparison pending; it is not a zero promotion score.

The controller attempts at most eight gameplay slots, with one same-session continuation per interrupted slot. It makes decisions only after balanced blocks. The initial block is bounded; a favourable descriptive result does not automatically authorise an unbounded ablation programme.

## Relevo

**Done:** packaged the prose candidate without event-specific instructions; froze both arms and the protocol; implemented the shared horizon guard, official-tool journal, quota checks, same-session continuation, independent public-state verification and reporting script. Candidate lint passed with no findings. Five focused regression tests passed. A live MCP smoke verified exactly five offered tools, handbook access, game creation, observation and handbook acknowledgement; that infrastructure-only session is excluded from gameplay counts. The actual comparison's launch preflight was rejected by the subscription service before creating any game.

Validation: full suite **242 passed** in 17.14 seconds, with the existing Authlib deprecation warning. Candidate lint also passed against every event title in the research catalogue. The empty-block report records `block_complete: false` with no scored slots.

**Pending:** execute all four balanced pairs when quota permits, generate results, audit notes for actual mechanism execution, then decide whether a separately frozen ablation stage is justified. With four episodes per arm, report counts and uncertainty rather than a winning policy. Preserve all interruptions and do not count unresolved slots as failures.

The bounded execution and reporting commands, from the repository root, are:

```sh
.venv/bin/python scripts/first_review_transfer.py run --root /Users/matteozabban/careerlab-data/matteo-first-review-transfer
.venv/bin/python scripts/analyze_first_review_transfer.py /Users/matteozabban/careerlab-data/matteo-first-review-transfer lab/reports/first-review-transfer
.venv/bin/python -m pytest -q
```

Do not rerun `prepare` on the frozen root or change candidate text in place. The run command verifies frozen script, policy hashes and CLI version, checks live quota, and leaves a `status.json` for pending or completed work. The reporter never treats pending or interrupted slots as zero. After completion, update this report and Matteo's T4 line, commit and push the same branch, and update PR #11. No results are claimed until public final observations and the complete balanced block exist.
