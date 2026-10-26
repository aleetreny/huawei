"""Lint lab/policies-src with titles from local runs (collect_titles) plus story-event titles from the teacher digests."""
import re
import sys
from pathlib import Path
from careerlab.compliance import lint_policy_tree, collect_titles
from careerlab.config import load_settings
from careerlab.digest import calls  # noqa: F401  (keeps the import path identical to the digest tool)

s = load_settings()
titles = set(collect_titles(s.runs_dir))
n_local = len(titles)
for f in Path("lab/reports/teacher-digests").rglob("*-a[0-9].md"):
    for line in f.read_text().splitlines():
        m = re.match(r"- M\d+ \[[^\]]*\] (.+?) → ", line)
        if m and not m.group(1).startswith("Quarterly "):  # published phase names, excluded as in collect_titles
            titles.add(m.group(1).strip())
print(f"{n_local} titles from collect_titles, {len(titles)} with digest story titles")
rep = lint_policy_tree("lab/policies-src", titles)
only = sys.argv[1:]
bad = 0
for k, v in sorted(rep.items()):
    if only and not any(o in k for o in only):
        continue
    errs = [x for x in v if x.severity == "error"]
    bad += len(errs)
    print(k, "OK" if not v else [str(x) for x in v])
print("errors:", bad)
