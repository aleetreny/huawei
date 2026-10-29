"""Token anatomy of one official game: calls, growth per call, what the model wrote, token score.

    python3 scripts/comprobante/gametokens.py ~/careerlab-data/huawei-deepseek/runs/<run dir> [...]
Reads score_report.json, jiuwen.log (per-call usage) and events.jsonl (tool calls). Prints no game text.
"""
import collections, json, re, sys
from pathlib import Path


def token_score(total: float, months: int) -> float:
    tpm = total / max(1, months)
    s = 100.0 if tpm <= 500_000 else 0.0 if tpm >= 3_000_000 else 100 * (3_000_000 - tpm) / 2_500_000
    return min(s, 50.0) if months < 48 else s


def main(run: Path) -> None:
    sr = json.loads((run / "score_report.json").read_text()) if (run / "score_report.json").exists() else {}
    tu = sr.get("token_usage", {}); es = sr.get("ending_score", {})
    months = es.get("survival_months") or 0
    print(f"== {run.name}")
    print(f"Q {es.get('quantitative_score')}  months {months}  outcome {es.get('outcome')}  cost {tu.get('total_cost')}")
    if tu:
        print(f"tokens total {tu.get('total_tokens'):,}  input {tu.get('input_tokens'):,}  output {tu.get('output_tokens'):,}  "
              f"per month {tu.get('total_tokens', 0) / max(1, months) / 1e3:,.0f}k  token score {token_score(tu.get('total_tokens', 0), months):.1f}")
    us = []
    if (run / "jiuwen.log").exists():
        for line in (run / "jiuwen.log").open(errors="replace"):
            m = re.search(r"'input_tokens': (\d+), 'output_tokens': (\d+), 'total_tokens': (\d+), 'cache_tokens': (\d+), 'reasoning_tokens': (\d+)", line)
            if m:
                us.append(tuple(int(x) for x in m.groups()))
    if us:
        inp = [u[0] for u in us]; out = [u[1] for u in us]; rea = [u[4] for u in us]
        d = [inp[i + 1] - inp[i] for i in range(len(inp) - 1)]
        kept = [out[i] - rea[i] for i in range(len(out) - 1)]
        print(f"model calls {len(us)}  first input {inp[0]:,}  last {inp[-1]:,}  growth/call {sum(d) / len(d):.0f}  "
              f"model-written kept/call {sum(kept) / len(kept):.0f}  tool side/call {(sum(d) - sum(kept)) / len(d):.0f}  reasoning total {sum(rea):,}")
    ev = run / "events.jsonl"
    if ev.exists():
        rows = [json.loads(l) for l in ev.open()]
        rows = [r for r in rows if "payload" in r and r["payload"].get("delta_kind")]
        names = collections.Counter(r["payload"]["delta"]["tool_call"]["name"].split("_")[-1] for r in rows if r["kind"] == "tool_call")
        seq = [r["kind"] for r in rows if r["kind"] in ("tool_call", "tool_result")]
        multi = sum(1 for a, b in zip(seq, seq[1:]) if a == b == "tool_call")
        notes = [len(json.loads(r["payload"]["delta"]["tool_call"]["arguments"]).get("notes") or "") for r in rows
                 if r["kind"] == "tool_call" and r["payload"]["delta"]["tool_call"]["name"].endswith("take_action")]
        print(f"tool calls {dict(names)}  replies with 2+ calls {multi}  note chars mean {sum(notes) / max(1, len(notes)):.0f}")
    tr = run / "transcript.log"
    if tr.exists():
        t = tr.read_text(errors="replace")
        print(f"transcript chars {len(t):,}  (visible text; v4 had 392,725)")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        main(Path(a).expanduser())
