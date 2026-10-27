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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="lab/policies-src/transmision")
    build(Path(ap.parse_args().out))
