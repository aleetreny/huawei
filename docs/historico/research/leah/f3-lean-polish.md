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
- **Checked afterwards:** one Haiku game (below). The rubric score can only be estimated; the organisers grade it.

## Result of one Haiku game (27 Oct, 09:52–09:58 UTC)

Game `leah-scre-679bb8b8-614d6e-00000-a1`, origin `leah`, CLI 2.1.295. Compared with f3-lean-v1's 12 Haiku race games (CLI 2.1.303) by `scripts/leah/compare_polish.py`.

| | f3-lean-v1 (12 race games) | f3-lean-polish-v1 (1 game) |
|---|---|---|
| Score | mean 55.5, 11 of 12 completed | **28.5**: dismissed at month 24, never left L1 (grades C C C C) |
| Tokens per month | median 677k (completed); 319k in its one game that ended at month 24 | **278k** over 24 months |
| Model turns | 376 (completed); 180 (the month-24 game) | 174 |
| Note length (median, capped at 200 as in the digests) | 179+ characters | **66** characters |
| Main action | key project 49%, Report results 28%, Lay low 16% | **key project 0%**, Build a mentorship 50%, Report results 50% |
| Energy | Defuse 35%, Prepare report 25%, Health recovery 20%, Skill learning 4% | Defuse 37%, Prepare report 32%, **Skill learning 26%** |

### What it shows

1. **The rewrite was not behaviour-neutral.** It kept every rule, but the explicit main-action order changed what Haiku did.
   - **Main action.** The first review is always a C, so the weak-review plan switched on at once and stayed on. Haiku then followed it strictly: Report results or Build a mentorship, and **never Apply for a key project**. In f3-lean's prose, the same rule left room for key projects in 49% of quarters.
   - **Energy.** "Otherwise lift the weakest statistic" sent a quarter of the Energy to Skill learning, which can't help at L1, where Skill stays stuck around 9.
   - **Result.** Output stayed at 1–3, and the game was dismissed exactly the way the stuck games were yesterday.
2. **The token instructions worked.** Notes were about 60% shorter (66 against 179+ characters), and tokens per month were about 13% lower than f3-lean's game of the same length (278k against 319k). For a completed game, that would be roughly 600k a month instead of about 680k. That's worth a few points of the token score at most.
3. **One game is one game.** The dismissal could partly be luck. But a main-action mix with no key projects at all is a mechanical change, not luck.

### Recommendation

- **Don't submit f3-lean-polish-v1 as it is.** For tonight, f3-lean-v1 as written remains the safer choice.
- **A version worth testing for cutoff 2:** f3-lean's exact text plus only the token lines (one `observe` per decision, notes of a few words). That keeps the measured token saving without touching how the rules read.

## Relevo

1. **Done.** The rewrite above, its `policy.json` (parent `f3-lean-v1`, operator "rewrite (same rules)"), and this note. No team files were changed: f3-lean-v1 is untouched, and nothing went to `main`.
2. **Results.** One Haiku game: 28.5, dismissed at month 24; notes 60% shorter and about 13% fewer tokens per month; no key projects at all (see above).
3. **Open.** Recommendation: submit f3-lean-v1 as written tonight. Whether to try "f3-lean + token lines only" for cutoff 2 is the team's call.
4. **Next.**
   - Alejandro's pre-cutoff DeepSeek games (T6) could run this copy. That checks DeepSeek follows it and measures tokens per month.
   - Without the key, one Haiku game shows the token count and whether the notes get shorter:

     ```sh
     uv run careerlab register lab/policies-src/f3-feedback-reactive/f3-lean-polish-v1 --by leah
     uv run careerlab enqueue --policy <id> --actor claude-cli:haiku --n 1 --purpose screen --why "polish check"
     uv run careerlab run --kind claude-cli --slots 1
     ```
5. **ESTADO line.** Not added: this isn't a numbered task. It's listed in `research/leah/worklog.md`.
