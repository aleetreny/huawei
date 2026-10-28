"""Juez de la nota de calidad de los SKILL.md (10 % de la nota automatica de cada version).

Le da a un modelo de Claude, por la CLI, la rubrica oficial literal (competition-rules.rst) y las
reglas publicadas (handbook.rst, rules.rst, failure-and-ending.rst) y le pide una nota 0-100 por
SKILL.md, con subnotas. No sabemos que modelo usa la organizacion: esto es un sustituto para comparar
versiones, no la nota oficial. No usa DeepSeek.

Uso:
  python3 scripts/calidad-skills/judge.py --out lab/reports/calidad-skills/data/j01.jsonl \
      --models haiku,sonnet --reps 3 lab/policies-src/deepseek/t13-read-v4 ...
Cada argumento es una carpeta de manual (busca bundle/skills/*/SKILL.md) o un SKILL.md suelto.
"""
from __future__ import annotations

import argparse, concurrent.futures as cf, glob, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "local-runs" / "official-runner" / "docs"


def rubric() -> str:
    t = (DOCS / "competition-rules.rst").read_text()
    i = t.index("- **Document design quality score (10%).**")
    j = t.index("- **Token efficiency score (10%).**")
    return t[i:j].strip()


def public_rules() -> str:
    parts = []
    for f in ("handbook.rst", "rules.rst", "failure-and-ending.rst"):
        parts.append(f"===== {f} =====\n" + (DOCS / f).read_text())
    t = (DOCS / "competition-rules.rst").read_text()
    i = t.index("Hard-coded") if "Hard-coded" in t else 0
    parts.append("===== competition-rules.rst (prohibited content) =====\n" + t[i:i + 6000])
    return "\n\n".join(parts)


PROMPT = """You are the automated scorer for the "document design quality" component of the Huawei TechArena UK 2026 Career Survival competition.
Teams submit Skills (SKILL.md files) that a single LLM agent (deepseek-v4-flash inside JiuwenSwarm) reads while it plays a 48-month career simulation through five MCP tools (new_game, observe, take_action, check_latest_logs, show_employee_handbook).

Scoring rubric (official text):
<rubric>
{rubric}
</rubric>

Published game rules that participants may rely on:
<public_rules>
{rules}
</public_rules>

Score the SKILL.md below from 0 to 100 as instructions for the agent, following the rubric. Be strict and consistent: use the whole range.
Then give one sub-score from 0 to 10 for each criterion:
- findable: the agent can find the Skill and knows when to open it (name and front matter)
- description: the description says what the Skill does and when to use it
- executable: steps are executable, with priorities and decision criteria
- near_limit: it says what to do near a limit (low health, low dignity, debt, isolation, review deadline, risk warnings)
- rules_match: the strategy matches the published rules (no contradiction, no invented mechanics presented as rules)
- horizon: the strategy looks across the 48 months
- robustness: the same guidance still applies when event wording or order changes
- clarity: concise, unambiguous, easy for a model to follow
Also report zero_conditions (list, empty if none): any of "invalid_front_matter", "empty_or_unrelated", "contradicts_game", "prohibited_conduct", each with the quoted line that triggers it.
List the three weaknesses that cost the most points, each with a quoted line and a concrete fix.

Answer with JSON only, no prose, in this shape:
{{"score": int, "sub": {{"findable": int, "description": int, "executable": int, "near_limit": int, "rules_match": int, "horizon": int, "robustness": int, "clarity": int}}, "zero_conditions": [{{"type": str, "quote": str}}], "weaknesses": [{{"quote": str, "problem": str, "fix": str}}]}}

<skill_file path="{path}">
{skill}
</skill_file>
"""


def skill_files(arg: str) -> list[Path]:
    p = Path(arg)
    if p.is_file():
        return [p]
    fs = sorted(glob.glob(str(p / "bundle" / "skills" / "*" / "SKILL.md"))) or sorted(glob.glob(str(p / "**" / "SKILL.md"), recursive=True))
    return [Path(f) for f in fs]


def ask(model: str, prompt: str, timeout: int = 600) -> str:
    r = subprocess.run(["claude", "-p", "--model", model], input=prompt, capture_output=True, text=True, timeout=timeout, cwd="/tmp")
    return r.stdout


def parse(out: str) -> dict | None:
    m = re.search(r"\{.*\}", out, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except ValueError:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", default="haiku,sonnet")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    rub, rules = rubric(), public_rules()
    jobs = []
    for t in a.targets:
        for f in skill_files(t):
            text = f.read_text()
            rel = os.path.relpath(f, ROOT)
            for m in a.models.split(","):
                for r in range(a.reps):
                    jobs.append((t, rel, text, m, r))
    print(f"{len(jobs)} llamadas", file=sys.stderr)
    out = open(a.out, "a")

    def run(job):
        t, rel, text, m, r = job
        t0 = time.time()
        raw = ask(m, PROMPT.format(rubric=rub, rules=rules, path=rel, skill=text))
        res = parse(raw)
        return {"target": t, "file": rel, "sha": hashlib.sha1(text.encode()).hexdigest()[:10], "words": len(text.split()),
                "model": m, "rep": r, "label": a.label, "sec": round(time.time() - t0, 1),
                "ok": res is not None, **(res or {"raw": raw[-500:]})}

    with cf.ThreadPoolExecutor(a.workers) as ex:
        for row in ex.map(run, jobs):
            out.write(json.dumps(row, ensure_ascii=False) + "\n"); out.flush()
            print(row["file"], row["model"], row.get("score"), row["sec"], file=sys.stderr)


if __name__ == "__main__":
    main()
