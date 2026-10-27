"""Enqueue one interleaved batch (T18): round k plays every arm once before round k+1.

    uv run python scripts/secciones/batch.py --name p1-h1 --cut 6 --n 25 --arms f3-lean-v1 f3-lean-clock-v1 ...

Arms are policy names or ids (registered first if a folder path is given). Each job gets
priority = start - k so rounds interleave and later batches queue behind earlier ones.
The job list goes to lab/reports/secciones/batches/<name>.json (used by periods.py --batch).
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from careerlab.cli import _actor, _env_fingerprint, _known_titles, _register
from careerlab.config import load_settings

OUT = Path(__file__).resolve().parents[2] / "lab" / "reports" / "secciones" / "batches"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--cut", type=int, help="stop month; omit for full games")
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--arms", nargs="+", required=True)
    ap.add_argument("--purpose", default="screen")
    ap.add_argument("--why", default="T18 interleaved batch")
    a = ap.parse_args()
    s = load_settings()
    reg = s.registry()
    actor_id, _ = _actor(reg, "claude-cli:haiku" + (f"^{a.cut}" if a.cut else ""))
    env_id = reg.register_environment(_env_fingerprint("real-dev"))
    pids = []
    for arm in a.arms:
        if Path(arm).is_dir():
            pids.append(_register(reg, Path(arm).resolve(), "secciones", titles=_known_titles(s)))
            continue
        row = reg.db.execute("SELECT policy_id FROM policies WHERE policy_id=? OR name=? ORDER BY created_at DESC", (arm, arm)).fetchone()
        if row is None:
            raise SystemExit(f"unknown policy {arm}")
        pids.append(row[0])
    low = reg.db.execute("SELECT COALESCE(MIN(priority), 0) FROM jobs WHERE status='queued' AND origin=?", (s.origin,)).fetchone()[0]
    start = min(low, 0) - 1
    jobs: dict[str, list[str]] = {pid: [] for pid in pids}
    for k in range(a.n):
        for pid in pids:
            jobs[pid] += reg.enqueue(pid, actor_id, env_id, a.purpose, 1, priority=start - k)
    names = {pid: reg.db.execute("SELECT name FROM policies WHERE policy_id=?", (pid,)).fetchone()[0] for pid in pids}
    reg.decide("enqueue", a.name, {"cut": a.cut, "n": a.n, "arms": names, "actor": actor_id}, a.why)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{a.name}.json").write_text(json.dumps({"name": a.name, "cut": a.cut, "n": a.n, "actor": actor_id,
                                                    "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                                    "arms": {names[p]: jobs[p] for p in pids}}, indent=1) + "\n")
    print(json.dumps({names[p]: len(jobs[p]) for p in pids}))


if __name__ == "__main__":
    main()
