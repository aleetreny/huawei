---
name: survive-then-climb
description: Survival and growth rules for every decision. Use it on every turn, before every choice.
---

# Survive, then climb

Careers end by dismissal after a second weak review or a trust crisis after piled-up risk warnings. Survivors fall short mostly on level and wealth, so once safe, chase promotion.

## Published rules (handbook)
- Each quarter end: 3 Energy (unused is lost), then one main action or none. Crossing a red line brings a warning.
- Energy cost 2: High-intensity work, Skill learning, Defuse legacy risk. Cost 1: Network maintenance, Health recovery, Mental recovery, Prepare report materials.
- Every 6 months: a review (S, A, B solid; C weak; D very weak; bonus from triple base pay down to none) and a promotion window whose hidden bar depends on Skill, Network, Output and level, and rises with level.
- Base pay climbs steeply with level (0.3 Wealth a month at L1, 9.1 at L10): promotion is the route to wealth.
- Early endings: Health gives out; Dignity low or wallet empty for months; Network too weak; Skill below the role; two weak reviews; a second blow-up.

## Turn loop
`observe`; read `events` and your last result first. Then `take_action` with the exact `choice` number and a note: state, signal, rule. If `success` is false, pick an affordable option. Stop at `ending_score`.

## Signals
- Risk signal: warning, HR, compliance, complaint, audit or legacy-problem wording; a statistic warning; a rising risk entry in `status_updates`.
- **Clear** (none recent), **Raised** (one), **Escalating** (repeated or stronger, or any blow-up, since a second ends the run). Step down one state only after a whole quarter without a new signal; reassurance does not shorten it.
- Review plan: from a C or D, or feedback that results fall short, until the next review.

## Precedence: Protect > Risk > Review > Grow
Each rule claims only the slots it names; the rest fall through. Exception: an active review plan keeps the main action even when Escalating.

1. **Protect.** Health or Dignity in the lower part of its 0–10 range or named in a warning: Health recovery or Mental recovery first; Lay low and reduce risk if Health keeps falling. Keep Network and Wealth above zero.
2. **Risk.** Raised: Defuse legacy risk in the next Energy phase. Escalating: Defuse every Energy phase, main action Lay low and reduce risk, no new commitments, formal complaints or open escalations. In stories disclose, fix or close problems rather than postpone, hide or shift them.
3. **Review.** Main action by the factor the feedback names: results, Report results to your manager; relationships, Repair a key relationship; capability or unclear, Apply for a key project. A new weak grade restarts the plan. In the second Energy phase after the C or D, the last before the next review, take Defuse legacy risk plus Prepare report materials whatever the state.
4. **Grow** (default). Main action Apply for a key project, which lifts all three promotion inputs; Report results to your manager when Network or Dignity falls. When Clear, with no plan and Health and Dignity comfortable: High-intensity work plus Prepare report materials (Skill learning when Skill stalls), and story options that raise Output, Skill or standing at a bounded cost.

## Always
- Every Energy phase includes Prepare report materials unless Protect needs all three points. Spend every point.
- Judge statistics by trend and feedback, not raw size. Network maintenance or Build a mentorship only when Network falls or feedback names relationships.
- In stories never add risk wording or push Health or Dignity low.
