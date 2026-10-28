You are reading story events from a workplace career simulation: a software engineer's career over 48 months. Each event offers numbered options. Choosing an option changes the player's visible stats, and some options also change a hidden risk counter.

Visible stats (from the employee handbook):
- Health: physical and mental stamina. Long-term overwork wears it down.
- Dignity: self-respect and recognition at work.
- Skill: professional capability.
- Network: the working relationships you can draw on.
- Output: the visible results you have built up over time.
- Wealth: cumulative wealth (money).

Hidden risk: problems that are not visible yet but can blow up later ("old landmines all go off at once"). The HR partner's monthly comment hints at how much has piled up.

Option types (one per option; if two apply, pick the one that describes the main thing the option does):

| Code | Type | Recognise it by |
|---|---|---|
| FIX | Constructive fix | Deals with the problem directly and professionally: proposes a plan, clarifies, quantifies, negotiates a middle ground, works it out together, delivers properly. |
| OWN | Own and repair | Admits a mistake, apologises, corrects the record, takes responsibility, repairs a relationship that was damaged. |
| HIDE | Hide, deny or cut corners | Lies, denies, conceals a risk or problem, blames someone else, bends a rule, takes a grey-area shortcut, gambles that nobody will notice. |
| ATTACK | Confront or retaliate | Hostile, public or aggressive: hits back, calls someone out in front of others, snaps, gossips, sabotages, humiliates, complains publicly. |
| YIELD | Give in or overextend | Says yes to everything, overworks, sacrifices health or evenings, reworks without question, caves to pressure, lets the day job pile up. |
| AVOID | Stay passive | Says nothing, does nothing, stays out of it, waits, ignores, withdraws, lets it go. |
| GUARD | Protect yourself politely | Declines politely to protect health, time, focus or private life; rests; keeps an agreed limit; keeps to own committed work. |
| ESCALATE | Use the formal channel | Hands it to the manager, HR, security or another formal process; reports it; asks someone else to decide. |
| SELL | Promote yourself | Seeks credit, visibility or advantage: pushes own name, flatters, plays politics, takes the win for yourself. |
| PERSIST | Double down | Keeps going with a course that is already going badly (keep complaining, keep hammering, keep insisting). |

For every option, judge from its wording only:
- type: one code from the table;
- the direction of its immediate effect on each stat: "+" (rises), "-" (falls) or "0" (no clear change);
- risk: "+" if it adds hidden risk, "-" if it reduces hidden risk, "0" if neither.

Answer with JSON only, one entry per option, in this form:
{"options":[{"choice":1,"type":"FIX","health":"0","dignity":"+","skill":"0","network":"+","output":"0","wealth":"0","risk":"0"}]}
