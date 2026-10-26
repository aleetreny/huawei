"""Write one new challenger for the fast race with a headless Claude designer.

    design.py --kind targeted|stretch|bold        # new folder under lab/policies-src/<family>/
    design.py --repair <policy folder> --errors <file>

The designer reads the champion's Skills, digests of its latest race games (worst
first), lab/fastloop/lessons.md and lab/fastloop/history.md, and writes policy.json
and bundle/ into one new folder. Tools: Read, Glob, Grep, Write, Edit (no shell, no
web). The driver lints, registers and puts the result on the ladder. Prints one JSON
line: {"ok": bool, "kind", "out", "name", "summary" | "error"}.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from careerlab import ladder  # noqa: E402
from careerlab.config import load_settings  # noqa: E402
from careerlab.digest import STAT_KEYS, game_lines  # noqa: E402

BRIEFS = REPO / "lab" / "fastloop" / "briefs"
MODEL = os.environ.get("FASTLOOP_DESIGN_MODEL", "opus")
EFFORT = os.environ.get("FASTLOOP_DESIGN_EFFORT", "max")
TIMEOUT_S = float(os.environ.get("FASTLOOP_DESIGN_TIMEOUT_S", 40 * 60))


def champion_games(reg, state: dict, newest: int = 12) -> list[dict]:
    rows = reg.db.execute(
        "SELECT j.job_id, j.run_dir, e.score, e.completed, e.survival_months, e.dims FROM jobs j JOIN evaluations e USING(job_id) "
        "WHERE j.policy_id=? AND j.actor_id=? AND j.origin=? AND e.outcome IN ('completed','eliminated') ORDER BY e.ingested_at DESC LIMIT ?",
        (state["champion"], state["actor_id"], reg.origin, newest)).fetchall()
    return [dict(r) for r in rows]


def summary(games: list[dict]) -> str:
    if not games:
        return "no race games yet"
    n, done = len(games), sum(g["completed"] for g in games)
    mean = sum(g["score"] for g in games) / n
    exits = sorted(g["survival_months"] for g in games if not g["completed"])
    dims: dict[str, list[float]] = {}
    for g in games:
        if g["completed"]:
            for k, v in json.loads(g["dims"] or "{}").items():
                if v is not None:
                    dims.setdefault(k, []).append(v)
    avg = ", ".join(f"{k} {sum(v) / len(v):.0f}" for k, v in sorted(dims.items()))
    return (f"latest {n} race games: mean score {mean:.1f}, {done}/{n} completed; early exits at months {exits or 'none'}; "
            f"ending dimensions of completed games (0-100): {avg or 'n/a'}")


def write_digests(games: list[dict], out: Path) -> int:
    """Worst four and best two of the champion's latest games, as compact per-decision digests."""
    out.mkdir(parents=True, exist_ok=True)
    ranked = sorted(games, key=lambda g: g["score"])
    pick = ranked[:4] + [g for g in ranked[-2:] if g not in ranked[:4]]
    index = ["| game | outcome | months | score | grades |", "|---|---|---:|---:|---|"]
    written = 0
    for g in pick:
        run_dir = Path(g["run_dir"] or "")
        if not run_dir.exists():
            continue
        lines, grades = game_lines(run_dir)
        head = [f"# {g['job_id']}", "", f"{'completed' if g['completed'] else 'early exit'} at month {g['survival_months']}, score {g['score']:.1f}. "
                f"Ending dimensions: {g['dims']}. Half-year grades: {' '.join(grades) or '—'}.", "",
                f"State before each decision: [{'/'.join(STAT_KEYS)}]. `>` lines are game feedback, shortened.", ""]
        (out / f"{g['job_id']}.md").write_text("\n".join(head + lines) + "\n", encoding="utf-8")
        index.append(f"| [{g['job_id']}]({g['job_id']}.md) | {'completed' if g['completed'] else 'early exit'} | {g['survival_months']} | {g['score']:.1f} | {' '.join(grades)} |")
        written += 1
    (out / "index.md").write_text("# Champion games (worst first)\n\n" + "\n".join(index) + "\n", encoding="utf-8")
    return written


def render(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace(f"<<{key}>>", value)
    return template


def run_designer(prompt: str, extra_dirs: list[Path]) -> tuple[int, str]:
    s = load_settings()
    cmd = [s.claude_executable, "-p", prompt, "--model", MODEL, "--setting-sources", "", "--permission-mode", "acceptEdits",
           "--allowedTools", "Read,Glob,Grep,Write,Edit", "--output-format", "json"]
    if EFFORT:
        cmd += ["--effort", EFFORT]
    for d in extra_dirs:
        cmd += ["--add-dir", str(d)]
    env = {k: os.environ[k] for k in ("HOME", "PATH", "USER", "LOGNAME", "LANG", "TMPDIR", "SHELL") if k in os.environ}
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=TIMEOUT_S, env=env)
    try:
        text = json.loads(proc.stdout).get("result", "")
    except ValueError:
        text = (proc.stdout or proc.stderr)[-2000:]
    return proc.returncode, text


def check_folder(out: Path, name: str) -> str | None:
    meta_path, manifest = out / "policy.json", out / "bundle" / "manifest.json"
    if not meta_path.exists():
        return "policy.json missing"
    if not list((out / "bundle" / "skills").glob("*/SKILL.md")):
        return "no bundle/skills/*/SKILL.md"
    if not manifest.exists():  # the manifest is boilerplate: write it rather than lose the design
        manifest.write_text(json.dumps({"team": "Gradient Depression", "name": name, "mode": "agent", "instruction": ""}, indent=2) + "\n")
    meta = json.loads(meta_path.read_text())
    if meta.get("name") != name:
        return f"policy.json name {meta.get('name')!r} != {name!r}"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["targeted", "stretch", "bold"])
    ap.add_argument("--repair")
    ap.add_argument("--errors")
    args = ap.parse_args()
    s = load_settings()
    reg = s.registry()
    state = ladder.load_state(s.lab_dir / "fastloop" / "state.json")
    champ = reg.db.execute("SELECT name, family, bundle_path FROM policies WHERE policy_id=?", (state["champion"],)).fetchone()

    if args.repair:
        out = Path(args.repair).resolve()
        prompt = render((BRIEFS / "repair.md").read_text(), {"out_dir": str(out), "errors": Path(args.errors).read_text()[:4000]})
        rc, text = run_designer(prompt, [])
        err = check_folder(out, out.name) if rc == 0 else f"designer exit {rc}"
        print(json.dumps({"ok": err is None, "kind": "repair", "out": str(out), "name": out.name, "summary" if err is None else "error": err or text[-1500:]}))
        return 0 if err is None else 1

    stamp = datetime.now(timezone.utc).strftime("%m%d-%H%M%S")
    family = "fast-bold" if args.kind == "bold" else champ["family"]
    name = f"{args.kind}-{stamp}"
    out = REPO / "lab" / "policies-src" / family / name
    work = s.data_dir / "fastloop" / "design" / name
    games = champion_games(reg, state)
    n_digests = write_digests(games, work / "digests")
    skills = sorted(str(p.relative_to(REPO)) for p in Path(champ["bundle_path"]).glob("skills/*/SKILL.md"))
    prompt = render((BRIEFS / f"{args.kind}.md").read_text(), {
        "champion": champ["name"], "family": family, "name": name, "kind": args.kind, "out_dir": str(out.relative_to(REPO)),
        "skill_paths": ", ".join(skills), "digest_dir": str(work / "digests") if n_digests else "(no local game digests: rely on the record and the lessons)",
        "summary": summary(games), "stuck_count": str(state.get("finished_since_crown", 0))})
    (work / "prompt.md").write_text(prompt, encoding="utf-8")
    started = time.time()
    try:
        rc, text = run_designer(prompt, [work])
    except subprocess.TimeoutExpired:
        rc, text = 124, "designer timed out"
    err = check_folder(out, name) if rc == 0 else f"designer exit {rc}"
    (work / "designer-reply.md").write_text(text or "", encoding="utf-8")
    print(json.dumps({"ok": err is None, "kind": args.kind, "out": str(out), "name": name, "minutes": round((time.time() - started) / 60, 1),
                      "summary" if err is None else "error": (text or "")[-1500:] if err is None else f"{err}: {(text or '')[-800:]}"}))
    return 0 if err is None else 1


if __name__ == "__main__":
    sys.exit(main())
