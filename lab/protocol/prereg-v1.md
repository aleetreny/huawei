# CareerLab pre-registered evaluation protocol — v1

Frozen 26 October 2026 before any policy-selection data exist. The SHA-256 of this file and of `prereg-v1.json` is recorded as a `protocol_frozen` decision in the registry. Any change creates v2 with a new hash; data collected under v1 stay in their own epoch. The 150 scripted episodes of pilot P1 ran before the freeze; they are an infrastructure pilot and are never used for selection.

Sources of the rules below: official scoring (`competition-rules`), the critical audit of 26 October (`research/careerlab/audit-2026-10-26.json`, 43 upheld errors), and the verifiers' objections that the first draft was infeasible this week. Where a rule is a team convention rather than a theorem, it says so.

## 1. Cells and identities

A cell is (policy hash, actor configuration hash, environment fingerprint, epoch). Statistics are never pooled across cells except through the hierarchical model in section 4, which pools policies of the same family **within one actor and epoch**. The environment fingerprint records engine, dataset and FastMCP versions, the official engine settings, the transport (stdio) and the runner. The actor record freezes model ID, harness, prompts, effort, skills mode, context policy, CLI version and isolation flags.

## 2. Outcomes

Primary per-episode outcome, matching the official per-run contribution:

- `Y = 0.8 Q + 0.1 E`, range 0–90.
- `Q` is `quantitative_score` (0–100).
- `E = min(cap, clip(100 (3,000,000 − tokens/T) / 2,500,000, 0, 100))`, with `T` the months survived and `cap = 50` if `T < 48`, else 100 (official token-efficiency rule).
- For actors whose token counts do not represent the target model (scripted, Claude), `E` is replaced by `Ê = 50` if `T < 48`, else the mean `E` of completed target episodes; it is 100 until a target pilot exists.
- The Skill-quality term (10 %) is constant per version and handled separately.

Auxiliary outcomes are descriptive only: `Q`, `T`, completion, `E`, tokens per month, the Kaplan–Meier survival curve, RMST to month 48, ending-dimension contributions, invalid actions, tool errors, interruption rate, usage and cost.

## 3. Data inclusion

1. Every launch gets a launch index within its cell and a block id. A block interleaves all arms being compared.
2. Decisions are taken only at block boundaries, on the **prefix-complete** set: launches `1..k` of each cell, where `k` is the largest index whose predecessors are all resolved. Early failures return first; without this rule the interim mean of a late-benefit policy is biased low.
3. Pending jobs are never observations and are never scored as zero.
4. An operational interruption is first resumed in its own session after observing it (flagged `resumed`). If that fails, the slot gets a replacement attempt in the same block. Interrupted attempts stay on record and are never scored.
5. **Alarms:** an interruption rate above 10 % in a cell; a ratio above 2 between compared arms; or interruptions concentrated in long episodes. Each alarm stops decisions for that comparison until the infrastructure cause is fixed. Best- and worst-case imputations are reported as sensitivity, not used as a gate, because their width does not shrink with `n`.
6. Worker timeouts are at least three times the median duration of completed episodes, so long successful games are not cut.

## 4. Decision model

- Within each actor and epoch: `Y_pj ~ N(μ_p, σ²)`, `μ_p ~ N(m_f, τ_f²)` within family `f`. `τ²` is estimated by DerSimonian–Laird with a floor of 9 (a 3-point between-policy SD), which gives normal posteriors for each `μ_p`.
- **Robustness:** every dormancy or promotion is recomputed with a Bayesian bootstrap of each cell. A decision that flips is recorded as `inconclusive`, and the comparison gets another block.
- Reported intervals: 95 % posterior intervals for decisions; the hedged-capital betting confidence sequence (Waudby-Smith & Ramdas 2024) on `Y/90` for any anytime-valid statement about a finalist.

## 5. Precision and relevance

- **Minimum relevant difference:** Δ = 4 Y-points, about 5 quantitative-score points. A team convention: smaller gains are below the noise of a three-run official score, whose SE is about `0.8 · σ / √3 ≈ 7` at σ = 15.
- **Precision target for a finalist:** posterior SD of `μ` at most 3 Y-points.
- **Planning size:** `n ≈ 9 σ_U² / Δ²` per arm (one-sided α = 0.10, power 0.8). Here `σ_U` is the 80 % upper bound of the pooled SD from the internal pilot, re-estimated after every block. This number guides budgeting and never triggers a decision by itself.
- When the budget cannot reach the target precision, the batch is labelled **estimation**: we choose by posterior mean and report the uncertainty, and we do not claim superiority.

## 6. Actions at block boundaries

| Action | Rule |
|---|---|
| Repeat | Next-block slots among active policies by top-two Thompson sampling (β = 0.5). |
| Generate | At least 20 % of slots go to new candidates. Children per family ≤ ⌈(1 + N_f)^0.5⌉, where N_f is the number of terminal episodes in the family's subtree (progressive widening; the exponent is a lab parameter). |
| Dormant (reversible) | At least 4 terminal episodes, `P(μ_p ≥ μ_leader − Δ) < 0.05`, and stable under the bootstrap refit. The record stores the reason, the evidence and a review trigger. |
| Reopen | (a) Audit: each block, with probability q = 0.2, one dormant policy is drawn (seeded and logged) for 2 episodes; it is reactivated if `P(μ ≥ μ_leader − Δ) ≥ 0.2`. (b) A new child hypothesis built on it. (c) An epoch change. |
| Promote | Top one or two by posterior mean with `P(best) ≥ 0.2`, at the freeze time for a cutoff or when the confirmation budget is reached. |
| Retire | Only invalid, duplicate-hash or non-compliant artefacts. |
| Stagnation | No gain of at least Δ/2 in the leader's posterior mean over three blocks. One slot per block then goes to a contrarian or cross-branch hypothesis, each with a written learning goal. |

## 7. Multiplicity and repeated looks

Development decisions are Bayesian and reversible, and audits check them, so repeated looks during development produce no claims. Only fresh confirmation data support a claim that one version beats another. These data are collected after freezing, with one pre-planned look, using a one-sided 95 % Welch lower bound with Bonferroni correction over at most two claims. If confirmation cannot reach Δ, the result is reported as an estimate. Confirmation data never feed selection; editing a policy after seeing them turns them into development data.

## 8. Actors (problem A)

- The **target actor** is the designated model in JiuwenSwarm 0.2.4b3 through the official runner. Only target cells drive dormancy, promotion and submission.
- Cheap actors (scripted, Claude workers) may:
  1. flag gross execution failures: if at least 3 of the first 4 cheap episodes show the same execution failure (tool misuse, invalid outputs, unfinished games, not low scores), the policy is fixed before target spend;
  2. supply traces for generation;
  3. answer decision-level probes: the same logged observation given to different actors.
- Cheap actors do not prune by score until they earn **pruning authority**. That requires all of: at least 8 shared policies spanning at least 16 Y-points; `P(ρ > 0.5) ≥ 0.8` for the disattenuated correlation; and zero audited false rejections. A single audited false rejection revokes authority for that family. Earning authority is not expected this week.
- With no target actor available, the lab makes no selection claims. It runs infrastructure checks, synthetic validation and harness diagnostics only.

## 9. Late benefits (problem B)

Decisions use only complete episodes. A partial-episode proxy may be used only if all of these hold:

- it is validated on completed target episodes from at least 10 policies;
- the leave-one-family-out Kendall τ between the month-k proxy and the final `Y` is at least 0.7;
- there are no audited false rejections.

Per-month state trajectories are logged for every episode so the proxy can be validated later.

## 10. Specialisation (problem C)

- A mode switch is compared as complete policies against both the `never` and the `always` variants. It is accepted only if `P(μ_switch > max(μ_never, μ_always) + Δ) ≥ 0.8` in fresh games.
- Calendar-triggered variants are diagnostic arms only. They are never shipped, because the rules ban learned thresholds regardless of how they are described.
- Mechanism tests use within-episode randomisation: at pre-declared decision points (quarter starts), the switch is drawn with probability p = 0.5 and logged with the visible state. Analysis estimates causal excursion effects. A time-shift placebo draws the switch month at random from 5–12 at launch.
- A specialisation is spurious if any of these holds:
  - the placebo shows a comparable effect;
  - the gain appears only among survivors;
  - it does not survive fresh games.

## 11. Submission rule (Stage 1 = maximum over at most three scored versions)

- At each cutoff, submit the distinct valid version with the highest posterior predicted version score (0.8 · μ_Q + 0.1 · D̂ + 0.1 · Ê). Content-identical versions are not rescored.
- If two candidates are within Δ/2, prefer the simpler one with lower token use.
- A variance-seeking choice, where the expected maximum rises because a version is uncertain, needs a written justification and must not undermine the design story for expert review.
- After each official release, compare the official score with the prediction. If `|z| > 2`, widen the environment-shift variance and favour policies that are robust across dev conditions.

## 12. Budget split for target episodes

The cost of a target episode is measured in a 2-episode pilot. The remaining target budget is then split: 15 % pilot and audits, 55 % selection, 30 % confirmation and reserve. If fewer than 20 target episodes are affordable, there are at most two finalists and no calibration study.
