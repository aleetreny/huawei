"""Resumen de una partida oficial: ascensos por mes, explosiones, estado final, llamadas y fichas por mes.
    python3 scripts/corte3/partida.py <run_dir> [...]
"""
import json
import re
import sys
from pathlib import Path

for d in map(Path, sys.argv[1:]):
    ev = d / "events.jsonl"
    if not ev.exists():
        print(d.name, "sin events.jsonl"); continue
    lvl, promos, blows, last = None, [], [], None
    for line in ev.open():
        e = json.loads(line)
        dd = (e.get("payload") or {}).get("delta") or {}
        if dd.get("event_type") != "chat.tool_result" or not (dd.get("tool_name") or "").endswith("observe"):
            continue
        try:
            r = json.loads(dd["raw_output"]["result"])
        except Exception:
            continue
        if not isinstance(r, dict) or "current_state" not in r:
            continue
        st, m = r["current_state"]["status"], r["current_state"]["time"]["current_month"]
        evs = r.get("events") or ""
        if lvl and st["level"] != lvl:
            promos.append(f"{st['level']}@{m}")
        if "Old landmines" in evs and m not in blows:
            blows.append(m)
        lvl, last = st["level"], (m, st)
    rep = json.loads((d / "score_report.json").read_text()) if (d / "score_report.json").exists() else {}
    es, tu = rep.get("ending_score", {}), rep.get("token_usage", {})
    months = es.get("survival_months") or 1
    log = (d / "jiuwen.log").read_text(errors="ignore") if (d / "jiuwen.log").exists() else ""
    m, st = last
    print(f"{d.name}: Q={es.get('quantitative_score')} {es.get('outcome')} meses={months} ascensos={' '.join(promos)} "
          f"explosiones={blows} final S{st['skill']} N{st['network']} O{st['output']} H{st['health']} D{st['dignity']} W{st['wealth']} "
          f"llamadas={log.count('tool_call_count')} sin_llamada={log.count('tool_call_count=0')} "
          f"fichas/mes={tu.get('total_tokens', 0) / months / 1e3:.0f}k")
