"""Render a SynthCareer parametric policy as a natural-language Skill.

An LLM worker given this text should make the same decisions as ``ParamPolicy``
on the same observations. Comparing the two decision by decision separates
execution fidelity (problem A) from strategy quality. Numbers in the text are
SynthCareer parameters; this testbed never feeds Skills for the real game.
"""

from __future__ import annotations

from typing import Any

from careerlab.synthetic.policy import complexity, normalize, theta_id


def render_skill(theta: dict[str, Any], name: str | None = None) -> str:
    t = normalize(theta)
    sid = name or f"synth-policy-{theta_id(t)[:8]}"
    lines = ["---", f"name: {sid}",
             "description: Decides every SynthCareer story choice, quarterly Energy action and quarterly main action for one fixed policy. Use it for every decision in the game.",
             "---", "", "# Policy", "",
             "Follow these rules exactly. They are the policy under test; do not add your own strategy.", ""]
    lines += ["## Mode", ""]
    if t["switch_rule"] == "none":
        lines.append(f"Stay in **{t['start_mode'].upper()}** mode for the whole game.")
    elif t["switch_rule"] == "calendar":
        lines.append(f"Be in BUILD mode before month {t['switch_month']} and in DELIVER mode from month {t['switch_month']} on.")
    elif t["switch_rule"] == "state":
        lines.append(f"Start in BUILD. Re-check before every decision: be in DELIVER while Skill >= {t['switch_skill_base']} + "
                     f"{t['switch_skill_step']} x (level number - 1), otherwise BUILD (level number: L1 = 1, L2 = 2, ...).")
    else:
        lines.append("Start in BUILD. Switch to DELIVER when the feedback says your skill looks adequate for the next level; "
                     "switch back to BUILD when it says your skill looks short of the next level or when you are promoted.")
    lines += ["", "Write the current mode at the start of every `notes` field.", "", "## Story choices", "",
              "Classify each option by what it does, then pick the option with the highest preference:"]
    build = {"learn or stretch yourself": 5, "collaborate or share the work": 4, "spend money to solve it": 3,
             "decline politely": 2, "speak up for yourself": 2, "rest or step back": 1}
    deliver = {"speak up for yourself": 5, "collaborate or share the work": 4, "spend money to solve it": 3,
               "decline politely": 2, "learn or stretch yourself": 2, "rest or step back": 1}
    lines.append("- BUILD mode preferences: " + ", ".join(f"{k} ({v})" for k, v in build.items()) + ".")
    lines.append("- DELIVER mode preferences: " + ", ".join(f"{k} ({v})" for k, v in deliver.items()) + ".")
    rule = t["overtime_rule"]
    if rule == "always":
        lines.append("- Extra work or overtime: always take it (preference 7).")
    elif rule == "never":
        lines.append("- Extra work or overtime: never take it if another option exists (preference -2).")
    else:
        lines.append(f"- Extra work or overtime: take it (preference 7) only when Health >= {t['overtime_health']}; otherwise avoid it (-2).")
    if t["health_floor"]:
        lines.append(f"- When Health <= {t['health_floor'] + 1}, an option to rest or step back gets preference 8.")
    if t["wealth_floor"] >= 0:
        lines.append(f"- Spending money: preference 6 when Wealth >= {t['wealth_floor']}, otherwise -1.")
    if t["assert_dignity"]:
        lines.append(f"- When Dignity <= {t['assert_dignity']}, add 3 to speaking up for yourself.")
    if t["risk_reaction"] == "ignore":
        lines.append("- Shortcuts that skip proper work: preference 3 in DELIVER mode, otherwise 0.")
    else:
        lines.append("- Shortcuts that skip proper work: preference 0.")
    lines.append("- Ties: the lower choice number wins.")
    lines += ["", "## Risk warnings", ""]
    if t["risk_reaction"] == "ignore":
        lines.append("Ignore risk warnings.")
    else:
        act = "spend 2 Energy on Defuse legacy risk" if t["risk_reaction"] == "defuse" else "choose Lay low and reduce risk as the main action"
        lines.append(f"Count the risk warnings in the feedback. When at least {t['risk_warnings']} warning(s) arrived in the last 6 months "
                     f"and you have not yet reacted to the latest one, {act} in the next quarterly phase.")
    inv_b, inv_d = round(100 * t["invest_build"]), round(100 * t["invest_deliver"])
    lines += ["", "## Quarterly Energy (plan once at the first Energy decision of the quarter, then execute in order)", ""]
    if t["health_floor"]:
        lines.append(f"1. If Health <= {t['health_floor']}: Health recovery (and a second Health recovery if Health <= {t['health_floor'] - 2}).")
    if t["dignity_floor"]:
        lines.append(f"2. If Dignity <= {t['dignity_floor']} and Energy remains: Mental recovery.")
    if t["risk_reaction"] == "defuse":
        lines.append("3. If a warning reaction is due and 2 Energy remain: Defuse legacy risk.")
    lines.append(f"4. Invest about {inv_b}% of the remaining Energy in BUILD mode and {inv_d}% in DELIVER mode; "
                 f"{round(100 * t['network_share'])}% of the invested points go to Network maintenance, the rest to Skill learning (2 points each).")
    lines.append("5. With 2 or more points left (and Health comfortably above the recovery level): High-intensity work; spend any last point on Prepare report materials.")
    lines.append("If a planned action is unaffordable, skip it; finish the phase when nothing affordable is left.")
    vp = t["visibility_pref"]
    lines += ["", "## Quarterly main action", ""]
    if t["health_floor"]:
        lines.append(f"- If Health <= {t['health_floor']}: Lay low and reduce risk.")
    if t["dignity_floor"]:
        lines.append(f"- Else if Dignity <= {t['dignity_floor']}: Repair a key relationship.")
    lines.append("- BUILD mode: the action that adds the most Skill, then Network.")
    lines.append("- DELIVER mode: the action that adds the most Output" + (", favouring ones that also add Dignity and Network." if vp >= 0.5 else "."))
    lines.append("- Choose No action only if nothing adds what the mode wants.")
    lines += ["", f"(Policy complexity: {complexity(t)} active rules.)", ""]
    return "\n".join(lines)
