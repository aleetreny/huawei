"""Copies the speaker notes of guion.md into the presentation pages (their `notesdata` block).

    python3 scripts/entrega/cut3_video_notes.py [presentacion.html presentacion-b.html ...]
"""

import json
import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parents[2] / "docs/entrega/cut3-video"


def speaker_notes() -> dict[str, str]:
    text = (DIR / "guion.md").read_text(encoding="utf-8").split("## Notas de grabación")[0]
    notes: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"\*\*\[S(\d+)\]\*\*", line.strip())
        if m:
            current = m.group(1)
            notes[current] = []
        elif line.startswith(("## ", "---")):
            current = None
        elif current is not None and line.strip():
            notes[current].append(line.replace("*", "").strip())
    return {k: "\n".join(v) for k, v in notes.items()}


def main() -> None:
    notes = speaker_notes()
    data = json.dumps(notes, ensure_ascii=False).replace("</", "<\\/")
    for name in sys.argv[1:] or ["presentacion.html", "presentacion-b.html"]:
        page = DIR / name
        html, n = re.subn(r'(<script type="application/json" id="notesdata">).*?(</script>)',
                          lambda m: m.group(1) + data + m.group(2), page.read_text(encoding="utf-8"), flags=re.S)
        if n != 1:
            raise SystemExit(f"{name}: notesdata block not found")
        page.write_text(html, encoding="utf-8")
        print(f"{name}: {len(notes)} slides with notes")


if __name__ == "__main__":
    main()
