"""Main T20 table: per key rule, the winning formulation's obedience against the no-Skill control on the
final validation set (>= 200 situations per rule), with the reserved titles shown apart.

    uv run python scripts/transmision/final_table.py --items items-final.jsonl --ids ids-V2.txt --winner t10-countdown \
        [--extra pre_review=t2-veto,trigger=t2-veto]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score import arm_results, load_items, score_arm  # noqa: E402

NAMES = {"pre_review": "No ceder puntos antes de la evaluación", "skill_l4": "Skill en L4", "hr_risk": "Comentario de RR. HH.",
         "trigger": "Detonantes", "early_ruin": "Ruina temprana", "closing": "Cierre", "low_health": "Salud baja",
         "general": "Historias fuera de las reglas (efectos secundarios)"}


def pct(t: dict | None) -> str:
    if not t:
        return "—"
    lo, hi = t["ok_ci"]
    return f"{100*t['ok_rate']:.0f} % ({100*lo:.0f}–{100*hi:.0f})"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--winner", required=True)
    ap.add_argument("--extra", default="")
    a = ap.parse_args()
    items = load_items(Path(a.items))
    ids = {line.strip() for line in open(a.ids) if line.strip()}
    arms = {"control": arm_results("control"), a.winner: arm_results(a.winner)}
    extra = dict(x.split("=") for x in a.extra.split(",") if x)
    for arm in set(extra.values()):
        arms[arm] = arm_results(arm)
    print("| Regla | Brazo | Situaciones | Acierto control | Acierto brazo | Pérdida de nota control → brazo | Títulos reservados: n, control → brazo |")
    print("|---|---|---:|---|---|---|---|")
    for rule in NAMES:
        for arm in [a.winner] + ([extra[rule]] if rule in extra else []):
            common = ids & set(arms["control"]) & set(arms[arm])
            c = score_arm(items, arms["control"], "all", common).get(rule)
            w = score_arm(items, arms[arm], "all", common).get(rule)
            ch = score_arm(items, arms["control"], "holdout", common).get(rule)
            wh = score_arm(items, arms[arm], "holdout", common).get(rule)
            if not c or not w:
                continue
            hold = f"{ch['n']}: {100*ch['ok_rate']:.0f} % → {100*wh['ok_rate']:.0f} %" if ch and wh else "—"
            print(f"| {NAMES[rule]} | {arm} | {w['n']} | {pct(c)} | {pct(w)} | {c['regret_mean']:.2f} → {w['regret_mean']:.2f} | {hold} |")


if __name__ == "__main__":
    main()
