# f3-lean-polish-v1: the R1 candidate rewritten for the rubric and tokens

Leah, 27 Oct 2026, branch `leah/workspace`. This is a proposal for the cutoff-1 submission, not a team decision.

## What and why

- **Starting point.** The cloud's final hand-off recommends **f3-lean-v1** for R1. It's the simplest of the manuals statistically tied at the top: 250 words, 11 of 12 Haiku games completed, mean Q 55.5. Telling the tied leaders apart would take about 130 games each, so improving the *strategy* isn't realistic before tonight.
- **The other 20% of the automated score depends only on the text** and how it is played:
  - **Document quality, 10%.** Each `SKILL.md` is graded on whether:
    - the description says what the Skill does and when to use it;
    - the steps are executable, with priorities, decision criteria and what to do near a limit;
    - the strategy matches the published rules across all 48 months;
    - it still applies when event wording or order changes.
  - **Token efficiency, 10%.** Tokens per month survived: 500k or fewer scores 100, 3M or more scores 0, and a run that ends early is capped at 50. DeepSeek's one game (F1) used about 670k a month, about 93 if completed. So the gain here is a few points; **finishing the game matters far more than trimming text.**

## What changed

`lab/policies-src/f3-feedback-reactive/f3-lean-polish-v1/`. **The same rules as f3-lean-v1**, regrouped by turn type, with a few wording additions:

| f3-lean-v1 rule | f3-lean-polish-v1 |
|---|---|
| Clear: best visible trade-off; lift the weakest statistic in quarterly phases | same, listed under story, Energy and main action |
| Raised: Defuse first in the next Energy phase; stories disclose, fix or close | same |
| Escalating: Defuse every phase; Lay low as main action unless a weak-review plan is active; no new commitments | same; the main-action order is explicit (weak-review plan, then Lay low, then the weakest statistic) |
| Weak-review plan after a C or D: main action at the named factor; spare Energy on Prepare report materials | same |
| Step down after a quiet quarter; recovery overrides growth when Health or Dignity is low or named | same, with recovery stated first |
| — | **added:** one `observe` per decision; notes of a few words; judge signals by meaning, not wording; same rules for the whole career |

- **Length:** 287 words against 250. The extra ~50 tokens, re-read each turn, add up to about 20k tokens a game, under 1% of DeepSeek's monthly use. The token instructions should save more than that.
- **Checks:** `careerlab lint` finds nothing. An earlier draft ordered all rules as "first match wins", which would have dropped Escalating's Defuse while a weak-review plan was active, so it was rewritten to keep the parent's behaviour.
- **Not checked:** no game has been played with it yet, by any model. A rubric score can only be estimated; the organisers grade it.

## Relevo

1. **Done.** The rewrite above, its `policy.json` (parent `f3-lean-v1`, operator "rewrite (same rules)"), and this note. No team files were changed: f3-lean-v1 is untouched, and nothing went to `main`.
2. **Results.** None yet; there's no game data for this copy.
3. **Open.** Whether to submit this or f3-lean-v1 tonight is the team's call (Alejandro, T9).
4. **Next.**
   - Alejandro's pre-cutoff DeepSeek games (T6) could run this copy. That checks DeepSeek follows it and measures tokens per month.
   - Without the key, one Haiku game shows the token count and whether the notes get shorter:

     ```sh
     uv run careerlab register lab/policies-src/f3-feedback-reactive/f3-lean-polish-v1 --by leah
     uv run careerlab enqueue --policy <id> --actor claude-cli:haiku --n 1 --purpose screen --why "polish check"
     uv run careerlab run --kind claude-cli --slots 1
     ```
5. **ESTADO line.** Not added: this isn't a numbered task. It's listed in `research/leah/worklog.md`.
