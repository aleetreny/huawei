"""Whole-game question catalogue by stage, from black-box batches (research only, dev text).

Writes a Markdown file OUTSIDE the repository: every story title with the levels and months
where its first stage appears, every question (stage) with its answers, each answer's fixed
effect, its hidden-risk measures and the stage it leads to. Never copy this into a Skill or
hand it to a manual designer.

    python3 catalogo.py --batches b00-random-safe,b01-oracle-eps10,b02-stages \
        --model ~/careerlab-data/ingenieria-inversa/models/m05.json \
        --out ~/careerlab-data/ingenieria-inversa/catalogo-etapas.md
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

from bbdata import IDX, Batch


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batches", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    b = Batch(*args.batches.split(","))
    m = json.loads(Path(args.model).expanduser().read_text())
    first_lv = collections.defaultdict(collections.Counter)
    first_m = collections.defaultdict(list)
    seen_nodes = collections.defaultdict(collections.Counter)
    games = 0
    for g in b.games():
        games += 1
        seen = set()
        for s in g["steps"]:
            if s[1] != "e":
                continue
            nd = b.nodes.get(s[2], {})
            t = nd.get("title", "?")
            seen_nodes[t][s[2]] += 1
            if t not in seen:
                seen.add(t)
                first_lv[t][s[4][IDX["level"]]] += 1
                first_m[t].append(s[0])
    titles = sorted(first_lv, key=lambda t: (min(first_lv[t]), -sum(first_lv[t].values())))
    lines = [f"# Catálogo de preguntas por etapa (dev 1.0.8, {games} partidas de bots)", "",
             "Material de investigación. **No se copia a ninguna Skill ni se pasa a diseñadores.**", "",
             "Columnas de cada respuesta: efecto fijo anunciado; `riesgo` = cambio relativo del comentario de RR. HH.; "
             "`expl3` = exceso de probabilidad de explosión en 3 meses frente a las demás respuestas; `→` = paso siguiente.", ""]
    for t in titles:
        c = first_lv[t]
        tot = sum(c.values())
        months = sorted(first_m[t])
        lv_mix = ", ".join(f"L{k} {v / tot:.0%}" for k, v in sorted(c.items()))
        lines += [f"## {t}", "", f"Aparece {tot} veces (primer paso): {lv_mix}; meses {months[0]}–{months[-1]} (mediana {months[len(months) // 2]}).", ""]
        for node, n in seen_nodes[t].most_common():
            nd = b.nodes.get(node, {})
            lines.append(f"**Paso** `{node}` ({n} veces): {(nd.get('description') or '')[:300]}")
            for ch in nd.get("choices", []):
                e = m["nodes"].get(node, {}).get(str(ch["choice"]))
                if e:
                    eff = ", ".join(f"{k} {v:+g}" for k, v in e["mean"].items() if v)
                    extra = []
                    if "risk" in e:
                        extra.append(f"riesgo {e['risk']:+.2f}")
                    if "blow3" in e:
                        extra.append(f"expl3 {e['blow3']:+.2f}")
                    if e.get("next"):
                        top = max(e["next"], key=e["next"].get)
                        if top != node:
                            extra.append(f"→ `{top}`")
                    lines.append(f"- {ch['choice']}. {ch.get('action', '')} — {eff or 'sin cambios'}; {'; '.join(extra)} (n={e['n']})")
                else:
                    lines.append(f"- {ch['choice']}. {ch.get('action', '')} — sin datos")
            lines.append("")
    out = Path(args.out).expanduser()
    out.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"titles": len(titles), "nodes": sum(len(v) for v in seen_nodes.values()), "out": str(out)}))


if __name__ == "__main__":
    main()
