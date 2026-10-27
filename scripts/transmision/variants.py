"""Build the Skill variants of the obedience bank (T20) from one set of rule texts and several formats.

    uv run python scripts/transmision/variants.py --out lab/policies-src/transmision

Same rules, different transmission: where they live (Skill body, front-matter description, manifest
instruction), how they are written (explained prose, bare imperative, a status line the agent fills in
its notes) and how many Skills carry them. Rules use only published facts and in-run signals: no event
names, fixed answers, concrete months, thresholds or formulas.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

TEAM = "Gradient Depression"

# ----------------------------------------------------------------------------- rules (imperative core)
RULES = {
    "review": (
        "Protect the review",
        "Reviews come every six months. The review is settled as the review month begins, before that month's "
        "stories, so the story choices of the month just before a review month are the last ones that count. "
        "In that month never pick an option that may lower Skill, Network or Output, even if another option "
        "looks more principled or adds Dignity: Dignity and Health can be rebuilt later, a lost point can cost "
        "the promotion. Options that confront, correct or refuse someone in public usually cost Network; "
        "options that take time from your own delivery (extra unplanned work, investigations, rework, helping "
        "outside your role) usually cost Output."),
    "skill": (
        "Build Skill at senior levels",
        "From L4 on, Skill is the slow stat that holds promotion back; Network and Output keep up on their own. "
        "Every quarter at L4 or above, spend 2 Energy on Skill learning and take Apply for rotation as the main "
        "action, unless the risk rule or low Health says otherwise. In stories, prefer the option that teaches "
        "or builds capability."),
    "hr": (
        "Answer the HR remark",
        "Each month an HR partner comments on your risk. Only the smiling, all-right remark means clear. Any "
        "remark that mentions risk, worry or anger means hidden risk is piling up; it blows up when it gets "
        "high, and a second blow-up ends the run. While the remark is not the clear one: in the quarter take "
        "Lay low and reduce risk as the main action and Defuse legacy risk with Energy, until the clear remark "
        "comes back."),
    "trigger": (
        "No detonators under risk",
        "While the HR remark is not the clear one, never pick an option that hides, denies, deceives, "
        "gossips, cuts corners, delays a disclosure, or puts you under formal scrutiny (formal complaints, "
        "investigations, open letters, escalating over your manager's head). These set off the buried risk at "
        "once. Prefer the option that discloses, fixes or closes the problem quietly."),
    "money": (
        "Do not go broke early",
        "Pay is small in the first levels and Wealth starts near zero. While Wealth is only a few months of "
        "pay, refuse options that cost money (paying, buying, treating, lending, fees, gifts). Months with "
        "Wealth below zero end the run."),
    "closing": (
        "Close the career well",
        "The ending evaluation counts level, wealth, health and dignity, skill, risk control and network. In "
        "the last three months of the 48: bring the HR remark back to clear (Lay low and reduce risk, Defuse "
        "legacy risk), restore Health and Dignity with Energy, and in stories pick the option that keeps you "
        "healthy, respected and out of trouble; take on no new risk."),
}
ORDER = ("review", "skill", "hr", "trigger", "money", "closing")

# ----------------------------------------------------------------------------- explained (why) versions
WHY = {
    "review": "Why: a promotion needs Skill, Network and Output all at the level's bar on the day of the review; "
              "in the first levels the bar sits at the top of what the level lets you hold, so there is no spare point.",
    "skill": "Why: the handbook says higher levels set a higher bar; the bar that rises fastest is Skill, and "
             "quarterly Skill actions are the only steady source besides stories.",
    "hr": "Why: the remark is the only visible reading of hidden risk; acting early is cheap, a blow-up costs "
          "Dignity, Wealth and half a year of Output.",
    "trigger": "Why: with risk already buried, an option that could expose it or invite scrutiny makes it go off "
               "on the spot; with a clear remark the same option is usually safe.",
    "money": "Why: early pay barely covers small losses, and an empty wallet held for a few months is a run-ending failure.",
    "closing": "Why: in the last months there is no later review to play for; only the ending evaluation is left.",
}

STATUS_LINE = ("Before every take_action, start the notes with this line and fill it from observe:\n"
               "`Review in <months to the next review month> | HR <clear/risk> | Wealth <ok/low> | Left <months to 48> | Rule <which rule applies> | Pick <choice>`\n"
               "Months to the next review = 6 minus (current_month mod 6), and 0 when current_month is a multiple of 6. "
               "When Review in is 1, the review rule applies to every story choice.")

LOOP = ("## Turn loop\n"
        "1. `observe`; read `events` first (HR remark, review talk, warnings).\n"
        "2. Find the rule that applies below, then `take_action` with the exact `choice` number and a short note.\n"
        "3. If `success` is false, pick another option. Stop when the game ends.\n")


def front(name: str, desc: str) -> str:
    return f"---\nname: {name}\ndescription: {json.dumps(desc)}\n---\n\n"


def rules_md(keys=ORDER, why: bool = False, numbered: bool = True) -> str:
    out = []
    for i, k in enumerate(keys, 1):
        title, text = RULES[k]
        head = f"{i}. **{title}.**" if numbered else f"### {title}\n"
        out.append(f"{head} {text}" + (f"\n   {WHY[k]}" if why else ""))
    return "\n".join(out) + "\n"


def compact(keys=ORDER) -> str:
    """One line per rule, for the always-visible places (instruction, description)."""
    short = {
        "review": "In the month before a review month never pick a story option that may lower Skill, Network or Output (public confrontation costs Network, extra unplanned work costs Output).",
        "skill": "At L4 and above, every quarter: Skill learning with Energy and Apply for rotation as main action, unless risk or low Health says otherwise.",
        "hr": "If the monthly HR remark is anything but the smiling, all-right one: Lay low and reduce risk as main action and Defuse legacy risk with Energy.",
        "trigger": "While that remark is not clear, never pick an option that hides, denies, deceives, gossips, cuts corners or invites formal scrutiny.",
        "money": "While Wealth is only a few months of pay, refuse options that cost money.",
        "closing": "In the last three months: risk back to clear, Health and Dignity up, no new risk.",
    }
    return " ".join(f"({i}) {short[k]}" for i, k in enumerate(keys, 1))


def bundle(out: Path, name: str, skills: dict[str, str], instruction: str = "", hypothesis: str = "") -> None:
    root = out / name
    b = root / "bundle"
    (b / "skills").mkdir(parents=True, exist_ok=True)
    (b / "manifest.json").write_text(json.dumps({"team": TEAM, "name": name, "mode": "agent",
                                                 "instruction": instruction}, indent=2) + "\n")
    for sk, text in skills.items():
        (b / "skills" / sk).mkdir(parents=True, exist_ok=True)
        (b / "skills" / sk / "SKILL.md").write_text(text)
    (root / "policy.json").write_text(json.dumps({
        "family": "transmision", "name": name, "parents": [], "idea_origin": "T20 obedience bank",
        "operator": "transmission variant", "hypothesis": hypothesis or f"Transmission variant {name} of the T20 rules.",
        "predicted_behaviour": "Measured in the obedience bank against the no-Skill control.",
        "refutation": "No gain in right answers over the control on the bank.", "skill_count": len(skills)}, indent=2) + "\n")


DESC_GENERIC = "Decision rules for every Career Survival turn. Read before any story choice or quarterly action."


def build(out: Path) -> None:
    # A. body only, imperative, numbered; generic description
    bundle(out, "t-body-imp", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules_md()},
           hypothesis="Rules only in the Skill body (read on demand), bare imperative.")
    # B. body only, explained (imperative + why)
    bundle(out, "t-body-why", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules_md(why=True)},
           hypothesis="Rules only in the Skill body, each with its reason.")
    # C. compact rules in the description (always in the system prompt); body = full rules
    bundle(out, "t-desc", {"career-rules": front("career-rules", "Use before every choice. " + compact()) + LOOP + "\n## Rules\n" + rules_md()},
           hypothesis="Compact rules in the front-matter description, which the official runner keeps in every system prompt.")
    # D. compact rules in the manifest instruction (always in IDENTITY.md); body = full rules
    bundle(out, "t-instr", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules_md()},
           instruction="Before every choice apply these rules, in this order of priority: " + compact(),
           hypothesis="Compact rules in the manifest instruction, which the official runner keeps in IDENTITY.md on every call.")
    # E. status line the agent must fill in its notes (instruction + body)
    bundle(out, "t-status", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Status line\n" + STATUS_LINE + "\n\n## Rules\n" + rules_md()},
           instruction=STATUS_LINE.replace("\n", " ") + " Rules: " + compact(),
           hypothesis="The agent fills a status line (months to review, HR state, wealth, months left, rule) before each choice.")
    # F. one Skill per rule, each with its own description (all in the system prompt)
    per = {}
    descs = {"review": "Use for every story choice in the month before a review month: keep Skill, Network and Output from dropping.",
             "skill": "Use in every quarterly phase at L4 or above: Skill learning and rotation.",
             "hr": "Use when the monthly HR remark is not the smiling one: lay low and defuse.",
             "trigger": "Use for every story choice while the HR remark mentions risk: no hiding, denying, gossip or formal scrutiny.",
             "money": "Use for every story choice while Wealth is low: no options that cost money.",
             "closing": "Use in the last three months of the career: clear risk, restore Health and Dignity."}
    for k in ORDER:
        title, text = RULES[k]
        nm = {"review": "review-protection", "skill": "senior-skill", "hr": "hr-remark", "trigger": "risk-detonators",
              "money": "early-wealth", "closing": "career-close"}[k]
        per[nm] = front(nm, descs[k]) + f"# {title}\n\n{text}\n\n{WHY[k]}\n"
    bundle(out, "t-multi", per, hypothesis="One Skill per rule, so each rule's trigger sits in the always-visible skill list.")




# ----------------------------------------------------------------------------- round 2 (after bank round A)
# Round A showed two failure modes: "avoid confrontation" made Haiku cave in (pleasing / backing down is itself
# a risky answer), and the closing rule was too vague about the last quarterly phase.
RULES2 = dict(RULES)
RULES2["trigger"] = (
    "No detonators under risk",
    "While the HR remark is not the clear one, never pick an option that hides or denies something, lies or "
    "invents, gossips or mocks, cuts a corner, stays silent to avoid trouble, caves in or agrees just to please, "
    "or blames someone in public; and do not start formal processes (formal complaints, investigations, open "
    "letters, going over your manager's head). Pick the option that is honest, calm and owns the problem: "
    "stating your view respectfully is safe, backing down to please is not.")
RULES2["review"] = (
    "Protect the review",
    "Reviews come every six months and are settled as the review month begins, before that month's stories, so "
    "the story choices of the month just before a review month are the last ones that count. In that month never "
    "pick an option that may lower Skill, Network or Output, even if another option looks more principled or adds "
    "Dignity. Network is lost by blaming, accusing, refusing help or turning against someone in public; Output is "
    "lost by dropping or pausing your own delivery for extra unplanned work, investigations or rework. Keeping "
    "your view calmly and delivering your own work protects both; caving in is not safer.")
RULES2["closing"] = (
    "Close the career well",
    "The ending evaluation counts level, wealth, health and dignity, skill, risk control and network. In the "
    "career's last quarterly phase take Lay low and reduce risk as the main action, and spend Energy first on "
    "Defuse legacy risk if the HR remark is not clear, then on Health recovery and Mental recovery until Health "
    "and Dignity are full, then on Network maintenance; never High-intensity work or Skill learning there. In the "
    "last months' stories pick the option that keeps you healthy, respected and out of trouble.")
RULES2["hr"] = (
    "Answer the HR remark",
    "Each month an HR partner comments on your risk. Only the smiling, all-right remark means clear. Any remark "
    "that mentions risk, worry or anger means hidden risk is piling up; it blows up when it gets high, and a "
    "second blow-up ends the run. While the remark is not the clear one, in every quarterly phase: the first "
    "Energy action is Defuse legacy risk (unless Health is nearly gone) and the main action is Lay low and reduce "
    "risk. This comes before growth, before Skill and before any review plan.")

VETO = ("## How to choose a story option\n"
        "1. Read the context: months to the next review month, the latest HR remark, Wealth, months left.\n"
        "2. Strike out every option a rule below forbids in this context.\n"
        "3. Among the options left, pick the one that best builds Skill, Network and Output without costing Health "
        "or Dignity you cannot spare. If every option is struck out, pick the one that breaks the fewest rules.\n"
        "4. In the take_action notes write which options you struck out and why, in a few words.\n")


def rules2_md(keys=ORDER) -> str:
    return "\n".join(f"{i}. **{RULES2[k][0]}.** {RULES2[k][1]}" for i, k in enumerate(keys, 1)) + "\n"


def build2(out: Path) -> None:
    bundle(out, "t2-imp", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules2_md()},
           hypothesis="Round-2 rule texts (no caving in under risk; explicit last quarterly phase), body imperative.")
    bundle(out, "t2-veto", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n" + VETO + "\n## Rules\n" + rules2_md()},
           hypothesis="Round-2 rules used as a veto filter on story options before the agent's own judgement.")
    bundle(out, "t2-status", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Status line\n" + STATUS_LINE + "\n\n" + VETO + "\n## Rules\n" + rules2_md()},
           instruction=STATUS_LINE.replace("\n", " "),
           hypothesis="Round-2 rules with the status line and the veto filter.")


# ----------------------------------------------------------------------------- round 3
# Round 2: the Skill rule beat the closing rule in the final quarterly phase (rule order = priority for Haiku),
# and "the career's last quarterly phase" was not recognised. Round 3 states the priority and names the
# published end of the career.
RULES3 = dict(RULES2)
RULES3["closing"] = (
    "Close the career well",
    "The career ends after month 48 (the published length); the ending evaluation counts level, wealth, health and "
    "dignity, skill, risk control and network. In the quarterly phase of that final month: main action Lay low and "
    "reduce risk; Energy first on Defuse legacy risk if the HR remark is not clear, then Health recovery and Mental "
    "recovery until Health and Dignity are full, then Network maintenance. Never High-intensity work or Skill "
    "learning there: their gains come too late and their Health cost counts. In the stories of the last months, "
    "pick the option that keeps you healthy, respected and out of trouble.")
RULES3["skill"] = (
    "Build Skill at senior levels",
    "From L4 on, Skill is the slow stat that holds promotion back; Network and Output keep up on their own. In "
    "every quarterly phase at L4 or above (except the career's final month), spend 2 Energy on Skill learning and "
    "take Apply for rotation as the main action. In stories, prefer the option that teaches or builds capability.")
ORDER3 = ("closing", "hr", "review", "trigger", "money", "skill")
PRIORITY = ("Rules are listed in priority order: when two apply, the earlier one wins.")
EXAMPLES = ("## Reading what an option costs\n"
            "Option effects are hidden; read them from the wording. Invented examples (not from the game):\n"
            "- \"Correct the director in front of the client\" lowers Network. \"Raise it with the director privately "
            "afterwards\" keeps it.\n"
            "- \"Spend the week rebuilding a colleague's slides\" lowers Output: your own delivery slips. \"Point them to "
            "the template and finish your release\" keeps it.\n"
            "- \"Agree to the impossible date to keep the peace\" or \"say nothing and hope\" add hidden risk. \"State "
            "calmly what can be done by when\" is safe.\n"
            "- \"Quietly fix it and tell nobody\" hides a problem: hidden risk. \"Fix it and note it in the ticket\" is safe.\n")


def rules3_md(keys=ORDER3) -> str:
    return PRIORITY + "\n\n" + "\n".join(f"{i}. **{RULES3[k][0]}.** {RULES3[k][1]}" for i, k in enumerate(keys, 1)) + "\n"


def compact3() -> str:
    short = {
        "closing": "In the quarterly phase of month 48 (the last): Lay low and reduce risk, Energy on Defuse, Health and Dignity, then Network; never Skill learning or High-intensity work.",
        "hr": "While the monthly HR remark is anything but the smiling, all-right one: first Energy action Defuse legacy risk, main action Lay low and reduce risk.",
        "review": "In the month before a review month never pick a story option that may lower Skill, Network or Output.",
        "trigger": "While that remark is not clear, never pick an option that hides, denies, lies, gossips, cuts corners, caves in to please or starts a formal process.",
        "money": "While Wealth is only a few months of pay, refuse options that cost money.",
        "skill": "At L4 and above, in every quarterly phase except the one of month 48: Skill learning with Energy and Apply for rotation as main action.",
    }
    return "Priority order, earlier wins: " + " ".join(f"({i}) {short[k]}" for i, k in enumerate(ORDER3, 1))


def build3(out: Path) -> None:
    bundle(out, "t3-imp", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules3_md()},
           hypothesis="Round-3 rules in priority order (closing, HR, review, detonators, money, Skill), body imperative.")
    bundle(out, "t3-ex", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules3_md() + "\n" + EXAMPLES},
           hypothesis="Round-3 rules plus invented examples of reading an option's hidden cost from its wording.")
    bundle(out, "t3-instr", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules3_md() + "\n" + EXAMPLES},
           instruction=compact3(),
           hypothesis="Round-3 rules and examples in the body, compact rules in the manifest instruction (always visible).")


# ----------------------------------------------------------------------------- round 4 (pre-review perception, safer detonators)
RULES4 = dict(RULES3)
RULES4["review"] = (
    "Protect the review",
    "Reviews come every six months and are settled as the review month begins, before that month's stories, so the "
    "story choices of the month just before a review month are the last ones that count. In that month never pick an "
    "option that may lower Skill, Network or Output, even if another option looks more principled or adds Dignity. "
    "Before choosing, mark each option: does it go against a person (blaming, correcting, refusing, reporting someone)? "
    "Then it costs Network. Does it take time from your own delivery (extra or unplanned work, investigations, rework, "
    "the slow thorough path, stopping to fix someone else's problem)? Then it costs Output. Pick an option with neither "
    "mark; if every option has one, pick the one whose loss is on a stat that is not holding your promotion back.")
RULES4["trigger"] = (
    "No detonators under risk",
    "While the HR remark is not the clear one, strike out every option that hides or denies something, lies or "
    "invents, gossips or leaks, cuts a corner, or starts a formal process (formal complaints, investigations, open "
    "letters, going over your manager's head). The more worried the remark, the more you prefer the quietest option "
    "left that is not dishonest. Use your own judgement among the options that remain.")


def rules4_md(keys=ORDER3) -> str:
    return PRIORITY + "\n\n" + "\n".join(f"{i}. **{RULES4[k][0]}.** {RULES4[k][1]}" for i, k in enumerate(keys, 1)) + "\n"


def build4(out: Path) -> None:
    bundle(out, "t4-ex", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules4_md() + "\n" + EXAMPLES},
           hypothesis="Round 4: per-option marks for the pre-review rule; detonator rule reduced to vetoes plus 'quietest honest option'.")
    bundle(out, "t4-veto", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n" + VETO + "\n## Rules\n" + rules4_md() + "\n" + EXAMPLES},
           hypothesis="Round 4 rules with the veto procedure and examples.")


# ----------------------------------------------------------------------------- round 5: combined manual v2
# First games of t3-instr: a blackout by month 3 (story choices kept costing Health; no rule protected it) and
# a reviewer flag on the review timing stated as a known rule. Round 5 adds a Health and Dignity floor and words
# the timing as something to plan for.
RULES5 = dict(RULES4)
RULES5["health"] = (
    "Keep Health and Dignity safe",
    "Health at zero ends the run at once, and Dignity left near zero ends it too. When Health is low (4 or less out "
    "of 10): in stories never pick an option that costs Health (overtime, pushing through illness, skipping rest), "
    "and spend Energy on Health recovery before anything else. When Dignity is low (3 or less), Mental recovery "
    "comes first. Skill learning and High-intensity work cost Health: skip them while Health is low.")
RULES5["review"] = (
    "Protect the review",
    "Reviews come every six months. Treat the month before each review month as the deadline: the review talk can "
    "come as the review month opens, before its stories, so plan as if that month's stories will not count. In the "
    "month before a review month never pick an option that may lower Skill, Network or Output, even if another option "
    "looks more principled or adds Dignity. Before choosing, mark each option: does it go against a person (blaming, "
    "correcting, refusing, reporting someone)? Then it costs Network. Does it take time from your own delivery (extra "
    "or unplanned work, investigations, rework, the slow thorough path, stopping to fix someone else's problem)? Then "
    "it costs Output. Pick an option with neither mark; if every option has one, pick the one whose loss is on a stat "
    "that is not holding your promotion back.")
RULES5["skill"] = (
    "Build Skill at senior levels",
    "From L4 on, the review bar rises fastest for Skill; watch whether reviews stall while Network and Output keep "
    "growing. In every quarterly phase at L4 or above (except the career's final month), spend 2 Energy on Skill "
    "learning and take Apply for rotation as the main action, unless a rule above says otherwise. In stories, prefer "
    "the option that teaches or builds capability.")
ORDER5 = ("closing", "health", "hr", "review", "trigger", "money", "skill")


def rules5_md(keys=ORDER5) -> str:
    return PRIORITY + "\n\n" + "\n".join(f"{i}. **{RULES5[k][0]}.** {RULES5[k][1]}" for i, k in enumerate(keys, 1)) + "\n"


def compact5() -> str:
    short = {
        "closing": "In the quarterly phase of month 48 (the last): Lay low and reduce risk, Energy on Defuse, Health and Dignity, then Network; never Skill learning or High-intensity work.",
        "health": "Health 4 or less: no story option that costs Health, Health recovery first; Dignity 3 or less: Mental recovery first.",
        "hr": "While the monthly HR remark is anything but the smiling, all-right one: first Energy action Defuse legacy risk, main action Lay low and reduce risk.",
        "review": "In the month before a review month never pick a story option that may lower Skill, Network or Output (going against a person costs Network; taking time from your own delivery costs Output).",
        "trigger": "While that remark is not clear, never pick an option that hides, denies, lies, gossips, leaks, cuts corners or starts a formal process.",
        "money": "While Wealth is only a few months of pay, refuse options that cost money.",
        "skill": "At L4 and above, in every quarterly phase except the one of month 48: Skill learning with Energy and Apply for rotation as main action.",
    }
    return "Priority order, earlier wins: " + " ".join(f"({i}) {short[k]}" for i, k in enumerate(ORDER5, 1))


def build5(out: Path) -> None:
    bundle(out, "t5-instr", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules5_md() + "\n" + EXAMPLES},
           instruction=compact5(),
           hypothesis="Combined manual v2: round-4 texts, a Health and Dignity floor, timing worded as planning; compact rules in the manifest instruction.")
    bundle(out, "t5-ex", {"career-rules": front("career-rules", DESC_GENERIC) + LOOP + "\n## Rules\n" + rules5_md() + "\n" + EXAMPLES},
           hypothesis="Combined manual v2 with the rules only in the Skill body.")


# ----------------------------------------------------------------------------- round 6: scoped rules
# Games of t3-instr: Skill at the first review fell (S 2-7 at month 5 against 8-9 with f3-lean) because the
# "protect your own delivery" advice leaked out of the pre-review month and Haiku stopped taking the options that
# teach. Round 6 scopes every story rule to its context and leaves story choices to the model's own judgement
# otherwise; quarterly phases (where a manual commands well) get the full priority list.
T6 = """---
name: career-rules
description: "Rules for every Career Survival decision: quarterly Energy and main action, and the few story situations where your usual judgement is not enough. Read before deciding."
---

## Turn loop
1. `observe`; read `events` first: the monthly HR remark, the review talk, any warning.
2. Quarterly phases: apply the quarterly list below. Story events: check the four situations below; if none applies, choose as you judge best.
3. `take_action` with the exact `choice` and a short note naming the rule used, or "judgement". If `success` is false, pick another option.

## Quarterly phases (Energy, then main action): first matching line wins
1. **The career's final month (month 48):** main action Lay low and reduce risk. Energy: Defuse legacy risk if the HR remark mentions risk, then Health recovery and Mental recovery until both are full, then Network maintenance. Never Skill learning or High-intensity work.
2. **Health 4 or less:** Health recovery first. **Dignity 3 or less:** Mental recovery first. No Skill learning or High-intensity work until Health is back.
3. **The HR remark says risk is piling up, serious or worse** (anything stronger than a mild "some risk, not serious yet"): first Energy action Defuse legacy risk; main action Lay low and reduce risk.
4. **L4 or above:** Energy on Skill learning (2) plus one point where needed; main action Apply for rotation. From L4 the review bar rises fastest for Skill.
5. **Otherwise:** Energy and main action on whichever of Skill, Network and Output is furthest from what the next review needs; Apply for a key project lifts all three.

## Story events: only in these situations
- **Month before a review month** (reviews come every six months; the review talk can arrive as the review month opens, so treat the month before as the deadline): do not pick an option that may lower Skill, Network or Output. Going against a person (blaming, correcting in public, refusing, reporting someone) costs Network; giving up time from your own delivery (extra unplanned work, investigations, rework) costs Output. This applies only in that month.
- **HR remark says risk is piling up or worse:** strike out options that hide or deny, lie or invent, gossip or leak, cut a corner, or start a formal process (complaints, investigations, open letters, going over your manager's head). Choose among the rest.
- **Health 4 or less:** strike out options that cost Health (overtime, pushing through illness, skipping rest).
- **Wealth only a few months of pay:** strike out options that cost money.
Otherwise there is no rule: choose the option you judge best for a long, healthy career. Options that teach you, help colleagues or deliver solid work usually pay off.
"""


def build6(out: Path) -> None:
    bundle(out, "t6-scoped", {"career-rules": T6},
           hypothesis="Rules scoped to their context: full priority list for quarterly phases, four narrow story situations, own judgement otherwise.")
    bundle(out, "t6-scoped-instr", {"career-rules": T6},
           instruction="Quarterly phases follow the career-rules list in order. Story events: only in the month before a review month, while the HR remark says risk is piling up, while Health is 4 or less, or while Wealth is low, apply the matching career-rules filter; otherwise choose by your own judgement.",
           hypothesis="t6-scoped with a short always-visible reminder of the scope in the manifest instruction.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="lab/policies-src/transmision")
    o = Path(ap.parse_args().out)
    build(o)
    build2(o)
    build3(o)
    build4(o)
    build5(o)
    build6(o)
