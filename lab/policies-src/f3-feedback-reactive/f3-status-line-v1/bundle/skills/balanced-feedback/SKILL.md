---
name: balanced-feedback
description: Fills a fixed status line before every choice and serves the first need it shows. Use for every decision.
---

# Balanced play by status line

## Each turn
1. `observe`. Read `events`, the event text and your last action's result, then each statistic's direction.
2. Fill the status line `Protect: <dimensions or none> | Risk: clear, raised or escalating | Review: <factor or none> | Weakest: <statistic>`.
   - **Protect**: Health or Dignity in the lower part of its 0–10 range or named in a warning; Network or Wealth near zero.
   - **Risk**: a risk signal is warning, HR, compliance, complaint, audit or legacy-problem wording, a statistic warning, or a rising risk entry in `status_updates`. Raised after one recent signal, escalating after repeated or stronger ones. Step down one level only after a whole quarter without a new signal.
   - **Review**: after a C or D, or comments that results fall short, the factor the feedback names (results, capability or relationships), until the next review. If the next grade is still weak, name a different factor.
   - **Weakest**: a falling statistic, else the lowest of Skill, Network and Output.
3. Need: Protect if any, then Risk if raised or escalating, then Review, then Weakest.
4. `take_action` with the exact `choice` number and the note "<status line> → need → why this option".
5. If `success` is false, observe and pick an affordable option. Stop when `ending_score` appears.

## Serving each need
- **Protect**. Energy: Health recovery or Mental recovery first; keep Network and Wealth above zero.
- **Risk raised**: Defuse legacy risk first in the next Energy phase. **Escalating**: Defuse legacy risk in every Energy phase; main action Lay low and reduce risk or Repair a key relationship, whichever fits; no new commitments. In stories prefer disclosing, fixing or closing a problem over postponing, hiding or shifting it.
- **Review**. Main action at the factor: Report results to your manager or Showcase results for results; Build a mentorship or Apply for rotation for capability; Repair a key relationship for relationships. Spare Energy: Prepare report materials.
- **Weakest**. Story: avoid downsides on Protect dimensions; prefer helping the weakest, and a modest gain over a large one with a lasting cost. Energy: spread points; Skill learning or High-intensity work only while Health is comfortable; spend all Energy. Main action: cover gaps Energy missed; rotate rather than repeat.
