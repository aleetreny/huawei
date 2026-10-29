"""Per-turn view of turnprobe outputs with the OpenRouter provider and hidden-reasoning tokens that served each
call (joined with ~/careerlab-data/deepseek/calls.jsonl by prompt and completion token counts).

    uv run python scripts/comprobante/probeprov.py ~/careerlab-data/comprobante/turnprobe-cp-v5a-pin-*.json

Prints one line per probe: calls per reply (tak+obs = paired), visible content chars, reasoning tokens, provider.
"""
import glob, json, os, sys
from pathlib import Path

CALLS = Path.home() / "careerlab-data" / "deepseek" / "calls.jsonl"


def main() -> None:
    calls = []
    for line in open(CALLS):
        try:
            calls.append(json.loads(line))
        except ValueError:
            pass
    idx: dict = {}
    for c in calls:
        idx.setdefault((c.get("prompt"), c.get("completion")), []).append(c)
    files = [f for a in sys.argv[1:] for f in sorted(glob.glob(os.path.expanduser(a)))]
    paired = total = 0
    for f in files:
        j = json.load(open(f))
        out = []
        for t in j.get("log", []):
            m = idx.get((t.get("prompt"), t.get("completion")), [])
            prov = (m[-1].get("provider") or "?") if m else "?"
            rs = m[-1].get("reasoning") if m else "?"
            calls_ = t.get("calls", [])
            out.append(f"{'+'.join(x[:3] for x in calls_)}/{t.get('content_chars', 0)}c/r{rs}/{str(prov)[:5]}")
        stories = [t for t in j.get("log", []) if "take_action" in t.get("calls", [])]
        p = sum(1 for t in stories if "observe" in t.get("calls", []))
        paired += p >= max(1, len(stories) - 1)
        total += 1
        print(f"{os.path.basename(f):44s} {' | '.join(out)}")
    if total:
        print(f"probes with the pair in (almost) every story reply: {paired} of {total}")


if __name__ == "__main__":
    main()
