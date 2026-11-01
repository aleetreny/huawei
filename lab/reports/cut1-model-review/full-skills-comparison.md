# Confronto integrale delle Skill

Testi completi delle tre versioni valutate, copiati senza modifiche dai rispettivi commit. Per ogni candidato sono inclusi il manifest (che contiene ulteriori istruzioni per l’agente) e tutto il file SKILL.md. Nessuna parte della Skill è stata omessa. Questo documento di confronto non è un pacchetto di submission.

---

## t13-read-v4 — candidato submission

Commit: `09d5735` · policy ID: `f78c8b8834082a8c`

### Manifest completo

```json
{
  "team": "Gradient Depression",
  "name": "t13-read-v4",
  "mode": "agent",
  "instruction": "Follow the career-rules Skill and reread it whenever its rules are not in view. Decide stories only with its Story decisions and quarterly phases only with its quarterly list. In every story, drop options that may bury a problem (private, anonymous, partial, later, hidden, skipping work to save time). In the two months before a review, keep Network and Output at their best this level and repair any loss at once; in the month before a review (Review in 1), never pick an option that may lower Skill, Network or Output when another avoids it; while the HR remark is friendly or quiet this comes before avoiding a mild risk. Start every note with the status line."
}
```

### SKILL.md completo

```markdown
---
name: career-rules
description: "Use on every Career Survival turn. Keeps a one-line status note, reads every story option for likely stat changes and hidden risk, protects Skill, Network and Output in the month before a review, and sets quarterly Energy and main actions in priority order."
---

# Career rules

## How to use this Skill
- **Stories and quarterly phases are separate.** A story is decided only by "Story decisions" below. The quarterly list never picks a story option, and a story rule never picks an Energy or main action.
- Read this Skill again whenever its rules are no longer in view, for example after a summary or a resume.

## Turn loop
1. `observe`. Read `events` first: the monthly HR remark, the review talk, warnings. If your last note is not in view, call `check_latest_logs` with enough entries to find your most recent note and copy its status line.
2. Decide with the section for the current phase.
3. `take_action` with the exact `choice` and a note that starts with the status line, then one short reason. Keep the note well under 1,000 characters. If `success` is false, read the error, observe again and choose a valid option.

## Status line
Start every note with:
`Review in N | Now S<Skill> N<Network> O<Output> | Best S<..> N<..> O<..> | Stalled: none | Concerns this month: 0`
- **Review in N:** months left until the next review month, N = 6 - (current_month mod 6), and N = 6 when current_month is a multiple of 6. Reviews come every six months; our plan treats the month with N = 1 as the deadline for review preparation.
- **Now:** Skill, Network and Output as `observe` shows them before this choice.
- **Best:** the highest value of each of the three you have seen at your current level (copy it from your last note and raise it when Now is higher). Reset it to Now when your level changes. A stat under its Best has lost ground since you last held it.
- **Stalled:** a provisional record of an expected gain that did not show up in this run. In a quarterly phase, add `Expect S<..> N<..> O<..>`: the values the chosen action should leave, from its displayed changes. At the next quarterly choice, if the previous note describes that action and nothing else intervened, a stat still below its `Expect` value goes into Stalled. While a stat is in Stalled, prefer another useful investment over paying again for it. The same check works in stories: if your last story choice was one you read as raising a stat and Now shows no rise in it, add that stat to Stalled. Clear the list when your level changes, or when later observations show the stat rising again.
- **Concerns this month:** how many of this month's story choices you judged might bury a problem. Start each month at 0. It records your judgement, not the hidden risk itself.

## Story decisions
Before choosing, read every option for the likely sign of its effect on Skill, Network, Output, Health, Dignity, Wealth and hidden risk. How options usually move them:
- **Skill** rises when you use your own judgement: analyse, bring data or evidence, prepare properly, think a decision through, learn, design a plan, negotiate with facts, coach someone with questions. This holds for options about people or pay too, not only code.
- **Output** rises when you deliver, ship, finish or cover the work, keep to your own deliverables or make your results visible. It falls when your time or credit goes elsewhere: learning, helping or organising for others, reviewing their work, giving the credit away, apologising and redoing, pausing a delivery, complaining instead of working. Output and Network often trade against each other.
- **Network** rises when you help, involve, credit or work with others; it falls when you confront, refuse, embarrass someone, go over their head or ignore them.
- **Dignity** rises when you act straight, stand your ground calmly, own a mistake or get credit; it falls when you are humiliated, cave in, get blamed or gossip.
- **Health** falls with overtime, weekends, extra load and stress; it rises with rest and boundaries. **Wealth** moves with pay, bonuses and money you spend.
- **Hidden risk** rises with hiding, denying, blaming, shortcuts, gambles, fixing things privately or off the record, anonymous moves, side deals, partial, phased or postponed fixes, skipping necessary work to save time, open conflict, ignoring a known problem, disengaging, and challenging the company, its culture, leaders or rules even through a formal channel. It falls when you document, report a concrete problem openly, follow the process, own a mistake at once or fix the problem fully. Missing a risky option costs far more than flagging a safe one: when in doubt, treat it as risky.

Then apply these steps in order. Skip a step if it would remove every option.
1. **Survive.** Drop any option that could end the run now, for example by taking Health to zero.
2. **Risk.** Drop options that may add hidden risk. If the latest HR remark is anything but the friendly one, or Concerns this month is 1 or more, also drop options that keep a problem private, anonymous, partial, phased or for later, or skip work to save time, even when they solve the immediate problem; prefer an option that documents, reports, owns or fully fixes it. If every option looks risky, choose the smallest and most reversible risk.
   **Exception for the review month (N = 1) while the HR remark is friendly or quiet:** apply step 4 first. A mild risk (handling something privately, partially or later) is then acceptable when it is the only way to keep Skill, Network and Output, because a lost point there can cost the promotion. Hiding, denying, blaming, gambling and cutting corners stay out in every month.
3. **Wellbeing.** If Health or Dignity is low or falling, drop options that lower it.
4. **Review close (N = 1 or 2).** Promotions are lost here. With N = 2, drop options that may lower Network or Output. If Network or Output is under its Best, choose the honest option that most directly raises it back. With N = 1, apply all of this step. Drop options that may lower Skill, Network or Output: going against a person (blaming, correcting in public, refusing, reporting someone, going over a head) may cost Network; giving up time or credit from your own delivery (unplanned work, investigations, rework, the slow thorough path, someone else's problem) may cost Output; avoiding the work or the learning may cost Skill. Never save a point by hiding a problem or cutting a corner.
5. **Grow.** From the rest, choose the option that raises the most of Skill, Network and Output that are not in Stalled, counting twice a stat the latest review talk named as lagging, and minus one for each of them it lowers. In the final quarter of the career, prefer Health, Dignity and lower risk instead. On a tie: lower risk, then more Health and Dignity, then the option that costs no money.

After choosing, add 1 to Concerns this month if the chosen option might bury a problem.

## Quarterly phases only: first matching line wins
These lines choose Energy and main actions only, never a story option. You have 3 Energy per quarter; Skill learning, High-intensity work and Defuse legacy risk cost 2, the others 1. Unused Energy is lost. Choose one affordable Energy action at a time, then observe again.
1. **Last quarter of the career (month 48):** plan Energy and the main action together. Energy: Defuse legacy risk once if the HR remark is not the friendly one, then Health recovery and Mental recovery while either is below full, then Network maintenance. Main action: Lay low and reduce risk if the HR remark is not the friendly one, otherwise Report results to your manager. No Skill learning or High-intensity work.
2. **Health or Dignity in the lower part of its 0–10 range, or falling for several months; or Network or Wealth near zero for months.** Recover first: Health recovery, Mental recovery, Network maintenance or Repair a key relationship, and avoid spending. No Skill learning or High-intensity work until it recovers. Health at zero ends the run.
3. **HR remark.** Friendly ("you are doing all right"): no risk action. Quiet ("some risk, nothing serious yet"): first Energy action Defuse legacy risk, main action from the lines below. Anything else (frowning, uneasy, "you are on your own", angry): first Energy action Defuse legacy risk and main action Lay low and reduce risk, every quarter until the remark is friendly or quiet again.
4. **A review talk named a lagging stat:** until the next review, spend Energy and the main action on it (Prepare report materials for Output, Network maintenance for Network, Skill learning for Skill; main action Apply for a key project, or Apply for rotation when it is Skill).
5. **Network and Output both in Stalled:** Skill learning plus one point on the weakest of Health, Dignity or Network; main action Apply for rotation.
6. **Otherwise:** spend Energy on Skill, Network and Output that are not in Stalled (Prepare report materials, Network maintenance, Skill learning while Health is comfortable). Main action Apply for a key project; if two of the three are in Stalled, the main action that raises the third (Apply for rotation for Skill, Build a mentorship for Network, Showcase results for Output); if all three are, Energy on Health and Dignity and the main action Report results to your manager.
```

---

## observed-growth-v10 — Matteo

Commit: `04e1367` · policy ID: `c8b245267e72ae13`

### Manifest completo

```json
{
  "team": "Gradient Depression",
  "name": "observed-growth-v10",
  "mode": "agent",
  "instruction": ""
}
```

### SKILL.md completo

```markdown
---
name: observed-growth
description: Fills one fixed status line before every choice, holds Skill, Network and Output at their ceilings when each review is applied, keeps hidden risk and Dignity safe, and stops spending on stats that are already capped. Use for every decision of the run.
---

# Observed growth by status line

## How promotion works
- A review is applied at the very start of its month, before that month's events and quarter-end allocation. What counts is your state right after the last decision before it.
- It promotes when Skill, Network and Output are all high enough for your level and Dignity is not low. At the entry level, Network and Output must sit at their ceilings, so one point lost in the decisions just before the review costs the promotion. Built-up hidden risk makes promotion less likely.
- Each stat has a ceiling at each level; gains beyond it are lost. A stat that stops rising when an action should raise it is at its ceiling.
- Staying at the entry level brings weaker reviews and a warning that the next review must be better; after that warning, the next review decides survival.

## Each turn
1. `observe`. Read the statistics and the `events` feedback. Read the handbook once at the start for the review cycle.
2. Fill the status line `Review: near or far | Below best: <stats or none> | Capped: <stats or none> | Risk: calm or raised | Health: ok or low`.
   - **Review near**: the next review comes before the next quarter-end allocation.
   - **Below best**: Skill, Network or Output under its best value at this level.
   - **Capped**: stats that did not rise when an action should have raised them.
   - **Risk raised**: the HR remark is anything but calm, or a warning or incident appeared since the last allocation.
   - **Health low**: Health at or below the middle of its 0–10 range.
3. `take_action` with the exact `choice` number and the note "<status line> → need → why this option".
4. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.

## Story choices
- Never conceal or delay a problem, deny or misrepresent, gossip or leak, cut corners, bet that a known problem will not surface, overpromise or blame colleagues.
- **Honest without rigidity.** Among honest options, prefer one that keeps the other person on side without delaying your own work: brief or time-boxed help, raising it privately or in writing afterwards, refusing only the improper part. Refuse, block or take a public stand only when no such option is honest.
- **Review near**: rule out options whose downside hits Network or Output, unless all do; then the mildest. If Output is Below best, prefer delivering or showing your own result over side work, coaching or rework.
- **Repair at once**: if Network or Output dropped while the review is near, the next story choice is the honest option that most directly restores it.
- **Risk raised**: also avoid steps that put you under formal scrutiny (signed complaints, formal investigations, stand-offs with management) until risk is calm again.
- **Capped stats**: prefer options that build what is not capped; when Network and Output are capped, choose learning, quality and owning the fix.
- Avoid options that cost money while Wealth is low, and options that cost Dignity when Dignity is not high.
- **Health low**: rule out options that cost Health, unless all do.

## Quarter-end allocation, in order
1. **Risk raised**: Defuse legacy risk.
2. **Health low**: Health recovery.
3. **Review near**: lift each Below best stat: Network maintenance, Prepare report materials, Skill learning if Health is ok. Main action: Report results to your manager or Apply for a key project.
4. **Review far**: build what is not capped. Never spend on a Capped stat.
   - Skill not capped: Skill learning while Health is ok; main action Apply for rotation (the largest Skill gain), else Build a mentorship.
   - Network or Output not capped: Network maintenance or Prepare report materials; main action Apply for a key project.
   - Once Network and Output are both capped, Skill is the only blocker: rotation every quarter and Skill learning whenever Health allows; spare Energy on Health recovery.
Avoid High-intensity work. Spend all Energy; unused Energy is lost. Lay low only when Health is low and nothing else is affordable.

## After a weak review or a warning
Every allocation until the next review lifts Below best stats and visible Output. In pay or role talks, cite actual results and ask for concrete terms.
```

---

## BHR — Matteo

Commit: `d73697a` · policy ID: `55adabfe9a000ddf`

### Manifest completo

```json
{
  "team": "Gradient Depression",
  "name": "bhr",
  "mode": "agent",
  "instruction": ""
}
```

### SKILL.md completo

```markdown
---
name: bhr
description: Uses BUILD, HOLD and REPAIR to grow toward review readiness, preserve supported targets and restore losses, with factual memory. Use for every decision.
---

# BHR: Build, Hold, Repair

## Every decision
1. `observe`: read current statistics, phase, events and the last result. Read the handbook initially for timing and available actions. Current evidence governs current values; history supplies commitments and incidents.
2. Recover missing decision-relevant history through public logs, increasing the requested entries until the relevant record is found or unavailable. Entries are not decisions. Do not invent missing facts or sources.
3. Select BUILD, HOLD or REPAIR below. A review is near when it arrives before another allocation opportunity. Prepare before it is applied; do not postpone useful growth to try to arrive ready at the last moment.
4. `take_action` with the exact affordable `choice` and the checkpoint below in `notes`. Check that mode, choice and reason agree. If `success` is false, observe and reconsider; the rejected action is not completed. Stop at `ending_score`.

## Select one mode
Safety overrides every mode: address urgent risk, protect cash and recover Health. HOLD does not suspend these duties.

**BUILD — default.** Work on the strongest supported missing requirement. Protect dimensions already strong while building the weak one. Current-level best values are observations, not proven caps or promotion thresholds.

**HOLD — preserve supported readiness.** State which targets you have met and the public handbook or feedback supporting them. Without reliable targets, a plateau supports only provisional HOLD: Skill, Network and Output must each show earlier growth and repeated comparable investments with no further realised gain, with no outstanding review weakness. One zero gain or merely matching your best is insufficient. State the uncertainty.

In HOLD, prefer an honest option without a stated or previously observed loss to protected targets when safe and affordable. Avoid redundant growth, unnecessary commitments and exposure. Continue delivering existing commitments, reducing risk and maintaining Health. HOLD is not automatically silence, the mildest answer or Lay low. If every option has a cost, choose the safest necessary trade-off and record it.

**REPAIR — restore a protected loss.** After an observed loss to a protected target, record the deficit and choose the safest available action directly addressing it. Return to HOLD only after observed restoration and if the other readiness evidence remains valid; otherwise return to BUILD. Necessary safety costs can override protection: record the exception and reassess.

**Reset after review.** Non-promotion ends HOLD: use feedback, losses and payoffs to diagnose the missing requirement in BUILD. Do not repeat an unsupported readiness assumption. After promotion, reset level-specific targets and best values and start BUILD.

## Choices and allocation
- Be honest and own the fix. Do not conceal, misrepresent, leak, overpromise or blame others. Prefer private clarification, bounded help or refusing only the improper part when these protect relationships and your work.
- Protect Network and Output before reviews and repair relevant losses promptly. Preserve capability and Dignity too. Visible delivery matters when results are weak; optional side work may not address that weakness.
- Address raised risk with Defuse legacy risk. Repeated warnings or unresolved serious incidents also favour reducing exposure, such as Lay low when available. Calm feedback alone does not close incident history. Avoid unnecessary confrontation while vulnerable without hiding problems.
- Recover Health preventively, avoid High-intensity work, keep spending affordable and preserve a modest cash reserve. Avoid additional Health or Dignity losses when either is weak.
- After a weak review or explicit warning, maintain recovery until the next formal result: visible results for output, learning or mentorship for capability, repair for relationships. This overrides an unsupported HOLD assumption.
- After safety and recovery duties, follow the mode. BUILD: learning or rotation for Skill, maintenance for Network, reports or project work for Output. If Network and Output remain strong while promotion stalls, consider Skill as a possible blocker. HOLD: useful maintenance rather than redundant growth. REPAIR: address the recorded deficit.
- Check realised benefits. A zero delta can reflect delay, conditions or offsets; it does not prove a cap. Reconsider repeated investment without useful return. Use remaining Energy productively or for recovery; do not buy an ineffective action merely to exhaust Energy.

## Checkpoint: make the mode auditable
Write a fresh, short checkpoint, comfortably within the public 1000-character limit. Keep complete critical facts first; omit irrelevant diary detail. Do not rely on Continue to save notes.

`MODE: BUILD/HOLD/REPAIR | TARGET: ... [public source/time] | GAP: ... | WHY: this option ...`

For HOLD explain preservation; for REPAIR name the deficit; for BUILD name the missing requirement. State provisional status or a forced safety exception. Update the following decision-relevant facts with observed time and identifiable public source:
- `RISK`: serious incidents separately from current warnings, unresolved status and explicit closure evidence.
- `REVIEW`: latest formal grade, stated weakness and recovery target; distinguish reviews from bonus messages.
- `OPEN`: active commitment, next step and evidence needed for completion.
- `GAIN`: individual action and immediate before→after values; separate advertised gains from actual changes and later feedback.

The selected action's payoff is pending until observed. On the next turn check whether preservation or repair actually happened. Attempts and silence do not establish completion. Distinguish unknown, not reported and explicitly resolved. Correct memory against fresh evidence, retrieve missing history when needed, and never invent identifiers.
```
