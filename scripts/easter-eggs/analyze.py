"""Look for hidden content in the prober batches, against the 6,291-game baseline already in the repo.

    python3 scripts/easter-eggs/analyze.py [--data ~/careerlab-data/easter-eggs] [--out lab/reports/easter-eggs/summary.json]

Reports: level changes (jumps, off-review, drops), promotions below the measured minima, stories and system-text
lines never seen in the baseline, terminal states, and the follow-ups of every forced answer.
No game text is written to the summary beyond titles and short new lines (private repo, research only).
"""

from __future__ import annotations

import argparse
import collections
import glob
import gzip
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "lab/data/ingenieria-inversa"
TH = {1: (8, 3, 3), 2: (18, 6, 5), 3: (35, 18, 14), 4: (90, 30, 22), 5: (130, 45, 32), 6: (170, 60, 45)}


def norm(line: str) -> str:
    return re.sub(r"\d+(\.\d+)?", "#", line.strip())


def games(folder: Path):
    for f in sorted(glob.glob(str(folder / "games-*.jsonl.gz"))):
        try:
            with gzip.open(f, "rt") as fh:
                for line in fh:
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        return
        except (EOFError, OSError, UnicodeDecodeError, Exception):
            continue


def load_jsonl(pattern: str) -> dict:
    out = {}
    for f in glob.glob(pattern):
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
                out[d["id"]] = d
            except Exception:
                pass
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(Path.home() / "careerlab-data/easter-eggs"))
    ap.add_argument("--out", default=str(ROOT / "lab/reports/easter-eggs/summary.json"))
    a = ap.parse_args()

    old_nodes = load_jsonl(str(BASE / "*/nodes-*.jsonl"))
    old_titles = {v.get("title") for v in old_nodes.values()}
    old_lines = set()
    for t in load_jsonl(str(BASE / "*/texts-*.jsonl")).values():
        for line in t["t"].split("\n"):
            if line.strip():
                old_lines.add(norm(line))

    summary = {}
    for folder in sorted(Path(a.data).glob("ee-*")):
        nodes = load_jsonl(str(folder / "nodes-*.jsonl"))
        texts = {k: v["t"] for k, v in load_jsonl(str(folder / "texts-*.jsonl")).items()}
        s = collections.Counter()
        level_events, low_promos = [], []
        new_titles, new_lines = collections.Counter(), collections.Counter()
        final_lv, ends = collections.Counter(), collections.Counter()
        forced_follow = collections.defaultdict(collections.Counter)
        for g in games(folder):
            s["games"] += 1
            S = g["steps"]
            prev_lv = None
            for i, st in enumerate(S):
                m, ph, nid, ch, vec, txt, tag = st
                if tag == "p":
                    s["forced"] += 1
                    nxt = next((x for x in S[i + 1:] if x[1] == "e"), None)
                    title = nodes.get(nid, old_nodes.get(nid, {})).get("title")
                    if nxt:
                        forced_follow[f"{title} #{ch}"][nodes.get(nxt[2], old_nodes.get(nxt[2], {})).get("title")] += 1
                t = nodes.get(nid, {}).get("title")
                if ph == "e" and t not in old_titles:
                    new_titles[t] += 1
                if txt and txt in texts:
                    for line in texts[txt].split("\n"):
                        if line.strip() and norm(line) not in old_lines:
                            new_lines[norm(line)[:200]] += 1
                lv = vec[4]
                if prev_lv is not None and lv != prev_lv:
                    d = lv - prev_lv
                    kind = "jump" if abs(d) > 1 else ("down" if d < 0 else "up")
                    kind += "_review" if (m % 6 == 0 and S[i - 1][0] != m) else "_offreview"
                    s[kind] += 1
                    if kind != "up_review":
                        level_events.append([g["g"], m, prev_lv, lv, t])
                    else:
                        pre = S[i - 1][4]
                        sk, out = max(pre[2], vec[2]), max(pre[6], vec[6])
                        thr = TH.get(prev_lv)
                        if thr and (sk < thr[0] or out < thr[2]):
                            low_promos.append([g["g"], m, prev_lv, sk, out, list(thr)])
                prev_lv = lv
            final_lv[prev_lv] += 1
            for code, tid in (g.get("logs") or [])[-2:]:
                ends[code] += 1
        summary[folder.name] = {
            "counts": dict(s),
            "final_levels": {str(k): v for k, v in sorted(final_lv.items(), key=lambda x: (x[0] is None, x[0]))},
            "level_anomalies": level_events[:50],
            "promotions_below_minima": low_promos[:50],
            "new_story_titles": new_titles.most_common(40),
            "new_system_lines": new_lines.most_common(60),
            "forced_followups": {k: v.most_common(5) for k, v in sorted(forced_follow.items())},
        }
        c = s
        print(f"\n=== {folder.name}: {c['games']} games, {c['forced']} forced answers")
        print("  level changes:", {k: v for k, v in c.items() if k.startswith(('up', 'down', 'jump'))})
        print("  final levels:", summary[folder.name]["final_levels"])
        print("  anomalies:", level_events[:10])
        print("  promotions below minima:", len(low_promos), low_promos[:5])
        print("  new story titles:", len(new_titles), new_titles.most_common(15))
        print("  new system lines:", len(new_lines))
        for l, n in new_lines.most_common(25):
            print(f"    {n:4d} | {l}")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
