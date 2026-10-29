"""Real DeepSeek story decisions against the exact catalogue: where do they lose value? (research only:
the catalogue never goes into a Skill.)

Each story decision of an official game (events.jsonl) is matched to the catalogue by title and number of
options, and every option is valued with the tuned planner's value function (exact effects and risk) at
the observed state. Prints, per level, how often the pick is the best one; the causes of the costly picks
(regret > 1 planner unit); per game, picks of a Health/Dignity rise on a stat already at 10 while another
option at the same or lower risk grows Skill/Network/Output more; and how many costly picks cite
hidden-risk words in the agent's own note.

    uv run python scripts/deepseek/real_audit.py ~/careerlab-data/huawei-deepseek/runs/<run>/events.jsonl ...
    uv run python scripts/deepseek/real_audit.py lab/data/deepseek/partidas/t13-read-v4__*/events.jsonl.gz   # Git copy
"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "scripts" / "ingenieria-inversa"))
import planner as P  # noqa: E402
from datapaths import open_text  # noqa: E402
import replica as R  # noqa: E402

CAT = json.load(open(REPO / "lab/data/ingenieria-inversa/catalog_v2.json"))
BY = collections.defaultdict(list)
for nid, nd in CAT["nodes"].items():
    BY[(nd["title"], nd["n_choices"])].append(nid)
PL = P.Planner(**json.load(open(REPO / "lab/data/ingenieria-inversa/politica_optima.json"))["params"])
RISK_WORDS = r"bur(y|ies|ied)|hid|private|later|partial|postpon|delay|defer|quiet|phased|for now|risk"


def risk(nid: str, k) -> int:
    return int(CAT["risk"].get(f"E|{nid}|{k}", 0))


def decisions(path: str):
    """(observation, choice, note) for every multi-option story decision of one game."""
    obs = None
    for line in open_text(path):
        e = json.loads(line)
        p = e.get("payload", {})
        if "delta" in p:
            continue
        if e["kind"] == "tool_result" and str(p.get("tool_name", "")).endswith("observe"):
            try:
                obs = json.loads(p["raw_output"]["result"])
            except (KeyError, ValueError, TypeError):
                pass
        elif e["kind"] == "tool_call" and p.get("tool_call", {}).get("name", "").endswith("take_action") and obs:
            if len(obs.get("choices", [])) > 1 and not obs.get("current_event", {}).get("title", "").startswith("Quarterly"):
                a = json.loads(p["tool_call"]["arguments"] or "{}")
                yield obs, a.get("choice"), a.get("notes", "")
            obs = None


def gain(st: R.State, d: dict) -> dict:
    g = {}
    for k in R.GROWTH:
        x, cur = d.get(k, 0), getattr(st, k)
        g[k] = (min(max(R.cap(st.level, k), cur), cur + x) - cur) if x > 0 else x
    return g


def rows(path: str):
    for obs, ch, note in decisions(path):
        ce = obs["current_event"]
        nids = BY.get((ce["title"], len(obs["choices"])), [])
        if len(nids) != 1:
            continue
        nid, s = nids[0], obs["current_state"]["status"]
        st = R.State(health=s["health"], dignity=s["dignity"], skill=s["skill"], network=s["network"],
                     level=int(str(s["level"]).lstrip("L")), output=s["output"], wealth=s["wealth"],
                     month=obs["current_state"]["time"]["current_month"])
        opts = {int(k): (c["d"], risk(nid, k)) for k, c in CAT["nodes"][nid]["choices"].items()}
        if ch in opts:
            val = {k: PL.value(None, st, d, r) for k, (d, r) in opts.items()}
            yield st, opts, ch, max(val, key=val.get), val, note


def main() -> None:
    bylv = collections.defaultdict(collections.Counter)
    cause, cost = collections.Counter(), collections.Counter()
    for path in sys.argv[1:]:
        wasted = n = cited = costly = 0
        for st, opts, ch, best, val, note in rows(path):
            reg = val[best] - val[ch]
            c = bylv[st.level]
            c["n"] += 1
            c["best"] += ch == best
            c["regret"] += reg
            d, r = opts[ch]
            c["riskier"] += r > min(rr for _, rr in opts.values())
            alts = [k for k, (_, rr) in opts.items() if rr <= r]
            c["missed growth"] += max(sum(gain(st, opts[k][0]).values()) for k in alts) > sum(gain(st, d).values())
            full = [k for k in ("health", "dignity") if getattr(st, k) >= 10]
            waste = any(d.get(k, 0) > 0 for k in full) and any(
                sum(gain(st, opts[k][0]).values()) > sum(gain(st, d).values()) for k in alts)
            n += 1
            wasted += waste
            if reg <= 1:
                continue
            bd, br = opts[best]
            if br > r:
                k = "best is riskier"
            elif waste:
                k = "same/lower risk; a Health/Dignity rise on a stat already at 10"
            elif d.get("dignity", 0) + d.get("health", 0) > bd.get("dignity", 0) + bd.get("health", 0):
                k = "same/lower risk; more Health/Dignity (not full) over growth"
            else:
                k = "same/lower risk; other misread"
            cause[k] += 1
            cost[k] += reg
            if br <= r:
                costly += 1
                cited += bool(re.search(RISK_WORDS, note, re.I))
        print(f"{Path(path).parent.name}: matched {n}, Health/Dignity-at-10 picks {wasted}, "
              f"costly same/lower-risk picks {costly} ({cited} cite hidden-risk words)")
    for lv in sorted(bylv):
        c = bylv[lv]
        n = c["n"]
        print(f"L{lv} n={n:3d} best {c['best'] / n:4.0%} regret/decision {c['regret'] / n:5.2f} "
              f"riskier than the minimum {c['riskier'] / n:4.0%} missed growth {c['missed growth'] / n:4.0%}")
    print("costly picks (regret > 1) by cause: count, total regret")
    for k in cause:
        print(f"  {k:62s} {cause[k]:3d} {cost[k]:6.1f}")


if __name__ == "__main__":
    main()
