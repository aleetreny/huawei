---
name: career-status-note
description: "Defines the one-line status note that starts every take_action note in Career Survival: months to the next review, current and best Skill, Network and Output at this level, stalled gains and this month's concerns. Use it on every turn, and when the last note is not in view after a summary or a resume."
---

# Career status note

The career-rules Skill makes every decision; this Skill only defines the note that carries its memory between turns.

## The status line
The note is your memory: it survives summaries and comes back through `check_latest_logs`. Start every note with:
`Review in N | Now S<Skill> N<Network> O<Output> | Best S<..> N<..> O<..> | Stalled: none | Concerns this month: 0`
- **Review in N:** N = 6 - (current_month mod 6), and N = 6 when current_month is a multiple of 6. Reviews come every six months (handbook); N = 1 is the last month before a review, the deadline for review preparation in our plan.
- **Now:** Skill, Network and Output as `observe` shows them before this choice. If you cannot find your last note, rebuild the line from `observe`: Best = Now, Stalled: none.
- **Best:** the highest value of each of the three you have seen at your current level (copy it from your last note and raise it when Now is higher). Reset it to Now when your level changes. A stat under its Best has lost ground since you last held it.
- **Stalled:** a provisional record of an expected gain that did not show up in this run. In a quarterly phase, add `Expect S<..> N<..> O<..>`: the values the chosen action should leave, from its displayed changes. At the next quarterly choice, if the previous note describes that action and nothing else intervened, a stat still below its `Expect` value goes into Stalled. While a stat is in Stalled, prefer another useful investment over paying again for it. The same check works in stories: if your last story choice was one you read as raising a stat and Now shows no rise in it, add that stat to Stalled. Clear the list when your level changes, or when later observations show the stat rising again.
- **Concerns this month:** how many of this month's story choices you judged might bury a problem. Start each month at 0. It records your judgement, not the hidden risk itself.


## When the note is missing or wrong
- If `check_latest_logs` does not show your last note, rebuild the line from `observe`: Best = Now, Stalled: none, Concerns this month: 0.
- Keep the whole note well under 1,000 characters: the game cuts longer notes.
