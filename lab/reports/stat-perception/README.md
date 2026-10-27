# Stat perception: which ways of labelling an option can Haiku do, and what are they worth?

Leah, 27 Oct 2026, 15:00–16:00 UTC, branch `leah/workspace`. This is step (c) of Alejandro's question bank (branch `alejandro/optimistic-gauss-edyw1j`, `lab/reports/question-bank/README.md`): "improve the detection of which stat an option moves, relabel and re-run `catbot.py`".

No game was played. Haiku labelled the 936 dev answers 7 ways on Leah's Pro account (21 calls per way, 147 in all; 1.6 M tokens; 0.62 USD at list price). The team's Max quota was not touched. Everything else ran in the replica of `main-1nddsg`, with no quota.

## Short version

1. **Asking Haiku for every stat on every option is most of the gain.** Ale's labels named only the obvious stats. Replacing them with a direction for all 5 stats on every option raises the replica score **from 49.1 to 53.3**, against 46.7 for category only and 58.1 for perfect labels. That's +4.2 points, and needs no definitions at all.
2. **The best result is a vote of 5 ways of reading: 54.4**, +7.7 over category only. That closes about two thirds of the gap between category only and perfect labels.
3. **The stat worth perceiving is Output, not Skill.**
   - Making Output perfect on top of the vote adds **+2.5**.
   - Making Skill perfect **costs −2.1**: the bot chases Skill, which stalls at the low levels, and loses reviews.
   - The question bank's "Skill detected only 24% of the time" is real, but fixing it doesn't pay.
4. **What Haiku understands, and what backfires** (lessons for writing a manual):
   - **A short meaning of each stat beats a checklist of cues** (53.2 against 52.0).
   - **Meanings halve trust crises** (73 against 136 out of 1,000), because they make costs visible.
   - **Forcing one gain and one cost per option destroys information** (39.7, below category only).
   - **Defining Output as "visible momentum, even promoting yourself" backfired.** Output detection improved (up recall 0.52 → 0.66), but the score fell to 48.1 and trust crises rose to 174: Haiku started labelling risky self-promotion as a gain. **Never name a risky behaviour as a way to gain a stat**, even when it is true.

## Method

- **Data:** Ale's `answers.json` (936 answers, exact effect and category), rebuilt with his `build_answers.py` from `main-1nddsg`. It contains game text, so it stays outside Git under `~/careerlab-data/stat-perception/`.
- **Fair test:** the events were split in two halves before any instruction was written: [split.json](split.json) as node ids, 186 design questions and 217 reserved. I read only the design half to write the meanings and to pick per-stat combinations. Accuracy below is on the **reserved half**. The replica plays the whole catalogue: the instructions are general, but the "defs" meanings were seen against the design half.
- **Labelling:** [label.py](../../../scripts/leah/stat_perception/label.py) shows Haiku one question at a time (event description and options, never effects) and asks for −1, 0 or +1 on Skill, Network, Output, Health and Dignity for every option. Batches of 20 questions, Claude CLI `--model haiku` with no tools.
- **Accuracy:** [evaluate.py](../../../scripts/leah/stat_perception/evaluate.py) reports per stat up/down recall and precision, plus **pairwise order**: within a question, for two options whose true effect on a stat differs, does the labelling order them the same way? That is what a choice needs.
- **Value:** [replica_eval.py](../../../scripts/leah/stat_perception/replica_eval.py) uses Ale's catbot logic. Energy and the main action follow the 7-rule bot. Story options are scored by the category's mean effect, overridden by the labels, with risk judged by the category as a reader would. It runs 1,000 games per arm with the same seeds for every arm, so differences are paired.

## The 7 ways

| Way | What Haiku is told |
|---|---|
| plain | Nothing about the stats; just a direction for all 5 stats on every option |
| defs | A short meaning of each stat in this game, written from the design half. Skill = handling it the professional way (own, document, quantify, set a process, coach, hold a quality bar); Output = your own delivery; Network = goodwill of the people involved; Health; Dignity |
| cues | The same meanings as a checklist of concrete cues |
| contrast | Meanings, plus: compare the options of the question first (they trade one stat for another) |
| reason | Meanings, plus up to 12 words on what the option spends and earns, before the signs |
| trade | Meanings, plus only ONE stat bought and ONE paid per option |
| defs2 | defs with Output redefined as "visible momentum": push your work or standing forward, even promote yourself; disengaging costs it (round 3, from the design half's Output errors) |

Combinations without new calls ([combine.py](../../../scripts/leah/stat_perception/combine.py)):
- **vote5** = plain, defs, cues, contrast, reason;
- **vote5b** = the same with defs2 instead of defs;
- **vote7** = all seven.

Each stat takes the sign most of them give; ties go to 0.

## Results

Reserved half (217 questions, 493 answers). Pair = pairwise order, all stats; Output pair is the same for Output alone.

| Labels | Accuracy | Pair | Skill up recall | Output pair | Output up recall | Output down recall |
|---|---:|---:|---:|---:|---:|---:|
| prior (category's majority sign, no Haiku) | 0.640 | 0.700 | 0.64 | 0.50 | 0.14 | 0.10 |
| Ale's stat tags | 0.723 | 0.731 | 0.30 | 0.71 | 0.50 | 0.53 |
| **plain** | **0.727** | **0.807** | 0.55 | **0.80** | 0.62 | **0.66** |
| defs | 0.684 | 0.793 | 0.73 | 0.72 | 0.52 | 0.62 |
| defs2 | 0.681 | 0.791 | 0.71 | 0.72 | **0.66** | 0.51 |
| cues | 0.678 | 0.779 | 0.65 | 0.74 | 0.60 | 0.65 |
| contrast | 0.675 | 0.803 | 0.78 | 0.72 | 0.56 | 0.62 |
| reason | 0.670 | 0.802 | **0.79** | 0.74 | 0.54 | 0.65 |
| trade | 0.657 | 0.711 | 0.49 | 0.64 | 0.36 | 0.41 |
| vote5 | 0.693 | 0.803 | 0.75 | 0.76 | 0.56 | 0.67 |
| vote5b | 0.703 | 0.803 | 0.73 | 0.77 | 0.60 | 0.63 |

Replica, 1,000 games per arm, same seeds; "vs category" is paired against category only ([replica.json](replica.json)):

| Story perception | Score | vs category | L6+ | Dismissed | Trust crises |
|---|---:|---:|---:|---:|---:|
| Oracle (exact effects and risk) | 67.7 | — | 51% | 66 | 34 |
| Category + perfect signs | 58.1 | +11.4 ± 0.7 | 24% | 101 | 215 |
| **vote5b** | **54.4** | **+7.7 ± 0.8** | 7% | 203 | 81 |
| vote5 | 54.2 | +7.6 ± 0.8 | 5% | 207 | 74 |
| vote7 | 53.8 | +7.2 ± 0.8 | 6% | 206 | 80 |
| reason | 53.5 | +6.8 ± 0.8 | 6% | 219 | 92 |
| plain | 53.3 | +6.6 ± 0.7 | 8% | 181 | 136 |
| defs | 53.2 | +6.5 ± 0.8 | 4% | 213 | 73 |
| contrast | 52.8 | +6.1 ± 0.8 | 6% | 212 | 111 |
| cues | 52.0 | +5.3 ± 0.7 | 4% | 242 | 85 |
| Ale's stat tags | 49.1 | +2.4 ± 0.8 | 5% | 208 | 152 |
| defs2 | 48.1 | +1.5 ± 0.7 | 5% | 240 | 174 |
| Category only | 46.7 | 0 | 2% | 295 | 132 |
| prior | 44.2 | −2.5 ± 0.6 | 2% | 252 | 169 |
| trade | 39.7 | −7.0 ± 0.8 | 1% | 250 | 305 |

The Haiku ways that keep all five stats (plain, defs, cues, contrast, reason) are within about 1.5 points of each other. With paired standard errors around 0.7, the differences among them are small. The clear steps are Ale's tags → any full labelling (+3 to +4), and single way → vote (+1).

### Which stat is worth perceiving ([replica-one-perfect.json](replica-one-perfect.json))

vote5, with one stat replaced by its true sign:

| One stat made perfect | Score | vs vote5 | Dismissed | Trust crises |
|---|---:|---:|---:|---:|
| none (vote5) | 54.2 | — | 207 | 74 |
| **Output** | **56.7** | **+2.5** | 149 | 111 |
| Dignity | 54.5 | +0.3 | 212 | 77 |
| Network | 53.9 | −0.3 | 165 | 167 |
| Health | 53.7 | −0.5 | 221 | 98 |
| Skill | 52.1 | **−2.1** | 237 | 105 |
| all five | 55.1 | +0.9 | 112 | 249 |

Output perception is where the points are: fewer dismissals, because the bot holds Output at the ceiling for the review. This agrees with T20 (rule 7, "Haiku obeys 'do not lower Output' but does not know which option costs Output") and with the promotion rule. Perfect Skill hurts, because Skill stalls at low levels and chasing it costs reviews. Perfect effects on everything also raise trust crises, because the bot takes riskier high-yield options while it still judges risk by category.

### Where Output labelling goes wrong (design half, vote5)

Out of 443 answers: 51 Output gains missed, 46 false Output costs, 24 Output costs missed, 20 false gains.
- Haiku reads Output as **time spent**: a short conversation, a review or a checklist gets marked as a cost.
- In the game, Output tracks **momentum**: it rises when you push your own work or standing forward, and falls when you disengage, dodge, ask for less load, rest instead of working or get worn down.
- defs2 wrote this in and caught more gains. But the phrase "even promote yourself" pulled risky answers in as gains, and the score dropped. Keep the "disengaging costs Output" half; drop the self-promotion half.

## What this means for the manual (for Alejandro and T20)

- **A reader can't vote five times, but one instruction gets most of the way:** "for each option, consider what it does to each of Skill, Network, Output, Health and Dignity" (plain: +6.6 of the vote's +7.7).
- **A short meaning per stat helps against risk** (fewer trust crises). It goes in the review-month reference, behind T20's countdown, so it doesn't spill into other months.
- **For Output, describe only the cost side:** disengaging, dodging, handing work off, asking for less load and getting worn down cost Output; a short conversation or review does not. Never present self-promotion or other risky behaviour as a way to gain a stat.
- **Don't push Skill perception at low levels.**

**Limits:**
- The replica bot applies a formula to the labels. An LLM player reasons over the text and already picks well without a manual (H22: 83% best option). These numbers are the value of perception for a formula player, not a forecast for DeepSeek.
- Haiku stands in for DeepSeek. How DeepSeek labels is step (b) of Ale's plan, his call.
- The accuracy tables are on the reserved half. The replica uses all events.

## Files

- `tags-<way>.json`, `tags-vote5.json`, `tags-vote5b.json`: labels as `{node:choice: {stat: -1|0|1}}`, ids and codes only.
- `split.json`: design and reserved halves as node ids.
- `eval.json`, `replica.json`, `replica-one-perfect.json`: full result tables.
- Scripts in `scripts/leah/stat_perception/`.

## Relevo

1. **Done.**
   - Step (c) of the question bank: 7 labelling ways with Haiku, accuracy on the reserved half, value in the replica, and a per-stat value test.
   - **Main findings:** full five-stat labelling instead of salient tags (+4.2); the vote (+7.7 over category only); **Output is the stat to perceive, Skill isn't**; and what wording backfires.
2. **Data.** This folder, plus `~/careerlab-data/stat-perception/` (answers with text, outside Git).
3. **Not done.**
   - No manual written from this, and no game played.
   - No DeepSeek labelling (Ale's step b).
   - defs3 not written: defs with only the cost side of Output.
4. **Next.**
   - (1) Write defs3 and relabel, about 0.1 USD of Pro quota. It should keep defs' low trust crises and add the Output cost side.
   - (2) Ale's T20 bench: put "consider each of the five stats" plus the Output cost line into the review-month reference of t10/t13 and measure obedience.
   - Commands:
     ```bash
     git worktree add ~/careerlab-data/stat-perception/rx-ref origin/main-1nddsg
     git worktree add ~/careerlab-data/stat-perception/qb-ref origin/alejandro/optimistic-gauss-edyw1j
     (cd ~/careerlab-data/stat-perception/qb-ref && python3 scripts/question-bank/build_answers.py --rx ../rx-ref --out ../answers.json)
     python3 scripts/leah/stat_perception/label.py --answers ~/careerlab-data/stat-perception/answers.json --variant plain --out lab/reports/stat-perception/tags-plain.json
     python3 scripts/leah/stat_perception/evaluate.py --answers ~/careerlab-data/stat-perception/answers.json --split lab/reports/stat-perception/split.json --tags plain=lab/reports/stat-perception/tags-plain.json --catbot-dir /tmp/ct
     .venv/bin/python scripts/leah/stat_perception/replica_eval.py --rx ~/careerlab-data/stat-perception/rx-ref --answers ~/careerlab-data/stat-perception/answers.json --tags-dir /tmp/ct --games 1000
     ```
