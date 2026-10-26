# T13 — Opus ceiling measurement

**Pre-stated before any ceiling game.** This file was committed on 26 Oct 2026 at about 15:25 UTC. That was before the ceiling policy was registered and before any game was enqueued. The Results section below is filled in afterwards; nothing above it changes after the first game starts.

## Purpose

User request (26 Oct, relayed by the strategy session): play 4–6 Opus games at maximum effort, using everything we know in general form and no digests of concrete events. The question is how far the best reasoner can get above the current leader when it has all our general knowledge.

- If the gap is large, the rest of the week should keep investing in strategy search.
- If it is small, the effort should move to reliability (fewer dismissals after a second weak review, fewer trust crises) and to token efficiency.

This is a **measurement, never a submission candidate.** The winning games are also new teacher material for T2.

## Design

- **Policy:** `lab/policies-src/ceiling/x0-opus-ceiling-v1/`, family `ceiling`, parent F3 feedback-reactive. It is one Skill that combines:
  - F3's signal states, risk defusing and weak-review recovery;
  - the precedence used by f3-balance-recombined;
  - the two loss routes seen in our runs;
  - a growth mode for promotion and pay when reviews are solid and no warning is active (the score-gap finding);
  - the published handbook rules;
  - the general rules R1–R5 from `lab/reports/teacher-digests/distilled-rules.md`.
- **Clean room:** the Skill is written by a fresh subagent that may read only `findings.md`, `ESTADO.md`, the policy bundles, `research/careerlab/playbook-decisions.md`, `distilled-rules.md` and the handbook (through the official tool). It reads no event digest and no trajectory. The orchestrator of this cloud run had looked at the first 20 lines of one Opus digest earlier, to check the format, so it did not write this Skill itself.
- **Actor:** `claude-cli:opus@max~100k`: Opus, effort `max`, auto-compact at 100k tokens, Claude CLI 2.1.303 (pinned, as for every actor in this registry). This is a new actor cell, never pooled with other cells.
- **Runs:** 4 games, purpose `pilot`, in their own lane with **at most 2 concurrent** workers.
  - The quota governor applies: five-hour cap 0.80 and the seven-day pacing line.
  - **If the 4 games mix completions and eliminations, 2 more are added (6 in total); otherwise the measurement stops at 4.**
  - Games run to real termination. Interrupted attempts get a replacement and are never scored.

## Metrics and thresholds (pre-stated)

**Primary metric:** mean Y and mean Q over the scored games. Y follows prereg-v1 §2: `Y = 0.8 Q + 0.1 Ê`, where Ê = 100 for a completed game and 50 for an early exit, because Claude token counts do not represent the target model.

**Reference:** the current Haiku leader's posterior mean, fixed now: **Y_L = 60.21**. That is F3 feedback-reactive in registry decision #88 (26 Oct 14:07 UTC), the latest recorded Haiku block decision when this file was written. For sensitivity, the report also compares against the leader of the latest Haiku block decision at reporting time.

| Mean Y of the ceiling games | Interpretation |
|---|---|
| ≥ Y_L + 10 = **70.2** | Real headroom: keep investing in strategy search. |
| Y_L + 5 to + 10 = **65.2 – 70.2** | Some headroom: split the effort. |
| < Y_L + 5 = **65.2** | Near the ceiling: move effort to reliability (fewer month-24 dismissals) and token efficiency. |

**Uncertainty:** with 4–6 games this is an estimate, not a claim.

- The 6 earlier opus~100k games had an SD of Q of about 19. That gives an SE of mean Y of about 0.8 · 19 / √4 ≈ 7.6 at n = 4, and about 6.2 at n = 6. This is wider than the 5-point bands above.
- The report gives the mean with a 90 % t interval and names every band the interval touches.
- The band of the point estimate is the reading, labelled "estimate".
- No superiority claim is made. Under prereg §7 a claim needs fresh confirmation data on the target actor.
- Opus's result also mixes its capability with the policy, so it bounds what a weaker model can reach with the same text from above, not from below.

**Our prediction, written before the games:**

- 3–4 of 4 games complete; mean Q about 64; mean Y about 61, with a subjective 80 % range of Y from 52 to 68.
- So we expect "near the ceiling", or the lower edge of "some headroom".
- Reasoning: the 5 completed opus~100k games so far reached Q 59.6–69.8. Every completed game in the registry ends at a career-level score of 50 or below and a wealth score of 48 or below. The growth mode is the untested part.
- If level and wealth rise clearly above those values, the prediction was too low, and the gap is in strategy, not execution.

## Reported after the games

- Per game: Q, Y, months, ending dimensions, half-year grades.
- Where points are still lost, by dimension, compared with the 48 completed games in `findings.md` (level about 16.2 and wealth about 13.1 of about 40 missing points).
- Tokens per survived month, which drive the efficiency term for any actor.
- The interpretation against the thresholds above.
- Digests of the ceiling games: `careerlab digest --model opus`, filtered to the ceiling games, in `lab/reports/teacher-digests/opus-ceiling/`. These become T2 teacher material.

## Results

(pending)
