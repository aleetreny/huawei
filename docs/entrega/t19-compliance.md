# t19 status-line compliance note

**Recommendation: retain observation-based `Expect`/`Stalled` memory, but replace the categorical “gains are wasted” and “this count is the risk” claims before incorporating it into t13-read-v2.** Renaming a field does not itself make the underlying instruction compliant.

Internal review, 27 October 2026. Inspected `lab/policies-src/palancas/t19-final/bundle/skills/career-rules/SKILL.md`, especially lines 24–31, and its reference. This note is not a third design document for the submission package. No candidate was modified and no model/API calls or games were made.

## Applicable distinction

The competition rules' “Scope of the prohibitions” includes design documents as well as Skills. “Prohibited hard-coded answers, rules, and thresholds” forbids unpublished mechanics presented as known rules and permits general strategies based on public documentation and current-run feedback. Neither accuracy nor a softer label rescues an encoded development rule.

The status line does **not** contain a supplied numerical ceiling or promotion requirement. Recording current observations and expected changes displayed by the action menu is materially different from importing development values. That supports the design. It does not justify turning one mismatch into a permanent law of the game.

## Specific concerns

| Passage | Assessment | Proposed repair |
|---|---|---|
| `Expect` from the selected action's displayed updates | Defensible current-run evidence; not an unpublished threshold | Derive it only from the current menu, successful action and recorded pre-action panel. Do not insert learned effect magnitudes. |
| Any shortfall means the stat did not take the gain | Overconfident diagnosis: another effect, stale note, failed action or phase transition could invalidate the comparison | Verify a valid consecutive comparison and record the mismatch without asserting its cause. |
| `Stalled` persists at the level; further gains are “wasted” | Main compliance risk: operationally asserts a fixed limit despite avoiding the word “ceiling” | Treat the flag as provisional evidence; deprioritise repeated investment, allow fresh observations to clear it, and reassess after promotion. |
| Concern count is “the risk it does not show yet” | Equates subjective labels with an unobserved quantity | Explicitly distinguish count of concerns from hidden risk; a reset does not establish resolution. |

## Exact safer replacement wording

Replace the `Stalled`, stall-check and “Using Stalled” bullets with:

> **Stalled:** a provisional record of an expected gain not observed in this run. After a successful quarterly action, compare the next panel with the expectation derived from its displayed updates. Compare only when the prior note describes that action and no intervening phase change or other effect invalidates the comparison. If the comparison is unclear, record uncertainty instead of diagnosing a limit.
>
> While that observation remains relevant, prefer another useful investment rather than repeatedly paying for the same unobserved gain. This does not prove further gains are impossible. Clear or revise the flag when later observations contradict it; reassess after promotion. Survival and risk priorities still apply.

In the `Risky this month` bullet, replace the equivalence between the count and unobserved risk with:

> Count story choices you judged potentially concerning this month. This records your judgement, not hidden-risk units. Use it as a reminder to reassess unresolved exposure before seeking growth. Starting a new month's count does not prove earlier problems are resolved; interpret fresh feedback and prior concerns together.

Replace the unconditional instruction to substitute the next non-stalled stat with:

> If an investment is flagged Stalled, consider another useful, affordable action while the observation remains relevant. Do not bypass a survival need or repeat an invalid comparison merely to follow the flag.

Use placeholders rather than demonstration stat values in the note-format example. Keep status first and the whole note within 1,000 characters. For resumption, `check_latest_logs` counts entries, not decisions: retrieve enough recent entries to locate a valid action note instead of assuming `count=3` always includes one.

## Limits and final check

This wording lowers the risk of presenting a hidden fixed rule, but is not organiser approval. The substantive safeguards—current-run evidence, uncertainty, reversible flags and no supplied limits—matter more than the field name. It can also change behaviour and needs validation; the old detection percentages do not automatically transfer to it.

This focused pass does not clear the remainder of t19. Its reference still states review execution timing, and its quarterly body retains fixed stage/level prescriptions and numeric safety margins discussed in review 2. Incorporating the status line must not reintroduce those older passages into the repaired manual.

`TODO(final)`: confirm the exact replacements and field/reset rules in frozen t13-read-v2, then align both design documents with that file. Preserve the status line as observed memory, not a disguised table of game mechanics.

## Relevo

Drafted the two design documents and this focused note from main revision `1044a8b`. No new performance evidence was generated. The delivery README maps each claim to its internal source. Next: bind the drafts to the completed t13-read-v2, resolve every `TODO(final)`, and copy only the approved English design documents into the final package. Commit/push on `alejandro/entrega`; request integration with main.
