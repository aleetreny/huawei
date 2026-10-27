"""Score SKILL.md files with a Sonnet reviewer applying the official document-design rubric (T20, phase 3).

    uv run python scripts/transmision/rubric.py <bundle dir> [--runs 3] [--model sonnet]

The rubric text is quoted from the official competition rules (Document design quality score). The
reviewer sees only the published handbook and the Skill, as the organisers' reviewer would.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULES = HERE.parents[1] / "local-runs" / "official-runner" / "docs" / "competition-rules.rst"
HANDBOOK = Path.home() / "careerlab-data" / "transmision" / "handbook.md"
CLAUDE = os.environ.get("CAREERLAB_CLAUDE_EXE", str(Path.home() / "claude-2.1.303/node_modules/.bin/claude"))


def rubric_text() -> str:
    text = RULES.read_text(encoding="utf-8")
    start = text.index("- **Document design quality score (10%).**")
    end = text.index("- **Token efficiency score (10%).**")
    rules = text[text.index("Submissions must make decisions from the state"):text.index("Prompt injection, manipulation")]
    return text[start:end].strip() + "\n\nRelevant conduct rules:\n" + rules.strip()


PROMPT = """You are the organisers' reviewer for the Career Survival competition. Score one submitted SKILL.md
from 0 to 100 as instructions for the agent, using only this rubric:

{rubric}

The public employee handbook the agent receives:

<handbook>
{handbook}
</handbook>

The Skill under review (one of {n} Skills in the submission: {names}):

<skill>
{skill}
</skill>

Reply with JSON only: {{"score": <0-100>, "strengths": ["..."], "weaknesses": ["..."], "fixes": ["concrete edit", "..."]}}"""


def review(skill: str, names: list[str], model: str) -> dict:
    prompt = PROMPT.format(rubric=rubric_text(), handbook=HANDBOOK.read_text(encoding="utf-8"), skill=skill,
                           n=len(names), names=", ".join(names))
    out = subprocess.run([CLAUDE, "-p", "--model", model, "--setting-sources", "", "--tools", "",
                          "--output-format", "json"], input=prompt, capture_output=True, text=True, timeout=600)
    res = json.loads(out.stdout)["result"]
    m = re.search(r"\{.*\}", res, re.S)
    return json.loads(m.group(0)) if m else {"score": None, "raw": res[:500]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--model", default="sonnet")
    a = ap.parse_args()
    skills = sorted(Path(a.bundle, "skills").glob("*/SKILL.md"))
    names = [p.parent.name for p in skills]
    report = {}
    for p in skills:
        rows = [review(p.read_text(encoding="utf-8"), names, a.model) for _ in range(a.runs)]
        scores = [r["score"] for r in rows if isinstance(r.get("score"), (int, float))]
        report[p.parent.name] = {"mean": round(statistics.mean(scores), 1) if scores else None, "scores": scores,
                                 "weaknesses": [w for r in rows for w in r.get("weaknesses", [])],
                                 "fixes": [f for r in rows for f in r.get("fixes", [])]}
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
