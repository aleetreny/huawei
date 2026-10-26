"""Static compliance lint for policy bundles (manifest.json + skills/*/SKILL.md).

Why: a Skill that breaks a fair-play rule scores 0 on document quality or makes
the whole submission invalid, and the rules apply "whatever the derivation".
This lint catches the mechanical cases before a bundle is evaluated or
packaged: invalid front matter, wrongly cased file names (macOS hides them),
non-UTF-8 files and invisible characters (both hide text from the rules),
non-English text, references to simulator internals, team mode or provider
routing, injection phrases, threshold-like numbers, calendar triggers,
ending-score weights and named-event leakage.

Severities: ``error`` blocks a bundle; ``review`` needs a written human
justification (or a rewrite). A clearly negated mention of a reference term
("do not read X") is downgraded from error to review, because it is not
prohibited conduct but still costs tokens and invites scrutiny. Injection
phrases are never downgraded. The lint is a heuristic, not a certificate.

Known event titles come only from our own run trajectories and are used only
to detect leakage into Skill text, never to write policies.
"""

from __future__ import annotations

import codecs
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, replace
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable, Iterator

import yaml

ERROR, REVIEW = "error", "review"

PLACEHOLDER_TEAMS = {"", "your-team-name"}
ROUTING_KEYS = {"provider", "order", "only", "allow_fallbacks", "provider_preferences"}
POLICY_KEYS = ("family", "name", "parents", "hypothesis", "change", "predicted_behaviour", "refutation", "skill_count", "notes")
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SCRIPT_SUFFIXES = {".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".ps1", ".bat", ".rb", ".pl"}
TEXT_SUFFIXES = {"", ".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".tsv", ".rst", ".html", ".htm", ".xml"} | SCRIPT_SUFFIXES
MANIFEST_KEYS = {"team", "name", "mode", "instruction"}  # the published manifest sample

# Names published in the public handbook and rules. A run title that is itself a
# published name (e.g. an action name) is interface wording, so a match is only
# flagged for review.
PUBLISHED_PHRASES = " | ".join([
    "high intensity work", "skill learning", "network maintenance", "defuse legacy risk", "mental recovery",
    "health recovery", "prepare report materials", "apply for a key project", "report results to your manager",
    "fight for resources", "apply for rotation", "showcase results", "build a mentorship",
    "repair a key relationship", "lay low and reduce risk", "quarterly energy actions", "quarterly main action",
    "performance review", "promotion window", "junior engineer", "senior engineer", "staff engineer",
    "principal team lead", "senior principal tech lead", "director of engineering", "senior director",
    "distinguished fellow architecture committee", "chief architect fellow", "health", "dignity", "skill",
    "network", "level", "output", "wealth", "energy", "current level duration",
])


@dataclass(frozen=True)
class Finding:
    severity: str  # "error" | "review"
    file: str      # path relative to the bundle (or policy directory in lint_policy_tree)
    line: int      # 1-based; 0 for file-level findings
    rule: str
    text: str

    def __str__(self) -> str:
        return f"{self.severity.upper():6} {self.file}:{self.line} [{self.rule}] {self.text}"


@dataclass(frozen=True)
class _Rule:
    rule: str
    pattern: re.Pattern[str]
    message: str
    negatable: bool = True  # a negated mention is downgraded to review


def _rx(*parts: str) -> re.Pattern[str]:
    return re.compile("|".join(parts), re.I | re.M)


TERM_RULES = (
    _Rule("team-mode", _rx(r"\bteam[\s_-]*mode\b", r"[\"']?\bmode[\"']?\s*[:=]\s*[\"']?team\b", r"--mode[\s=]+[\"']?team\b",
                           r"\bmulti[\s-]?agents?\b", r"\bsub[\s-]?agents?\b", r"\bleader agent\b", r"\bteammate agents?\b",
                           r"\bteam execution\b", r"\b(?:parallel|role-based) teammates?\b"),
          "JiuwenSwarm team mode or multi-agent execution is prohibited"),
    _Rule("internals", _rx(r"\bsqlite3?\b", r"\bdata ?bases?\b", r"\bcareer[\s_-]?emulator\w*", r"\bcareer[\s_-]?sim[\s_-]?runner\b",
                           r"\binternals\b", r"\b(?:internal|installed|game|simulator|simulation|engine)\s+(?:packages?|source(?: code)?|state files?)\b",
                           r"\bsource code\b", r"\bdecompil\w*", r"\breverse[\s-]engineer\w*"),
          "reference to simulator internals; Skills may rely only on the five official tools"),
    _Rule("dataset", _rx(r"\bdata ?sets?\b", r"\b(?:evaluation|validation|development|dev)\s+(?:data|split)\b",
                         r"\b[\w-]+\.(?:sqlite3?|db|data|jsonl|parquet|pkl|pickle)\b", r"\bevents?\.json\b"),
          "reference to dataset or data files"),
    _Rule("provider-routing", _rx(r"\bopen ?router\b", r"\ballow_fallbacks\b", r"\bprovider[\s_-]+(?:preferences?|routing|order)\b",
                                  r"[\"'](?:provider|order|only|allow_fallbacks)[\"']\s*:", r"^\s*(?:provider|allow_fallbacks)\s*[:=]"),
          "LLM provider routing settings are prohibited"),
    _Rule("injection", _rx(
        r"\b(?:ignore|disregard|forget|override|bypass)\b[^.\n]{0,40}\b(?:previous|prior|above|earlier|preceding|all|any|system|developer|organi[sz]er|competition)\b[^.\n]{0,20}\b(?:instructions?|prompts?|rules?|messages?|guidelines?)\b",
        r"\byou are now\b", r"\bdeveloper mode\b", r"\bjailbreak\w*", r"\bdo anything now\b",
        r"\b(?:reveal|print|show|output|leak|repeat)\b[^.\n]{0,30}\b(?:system|hidden|developer)\s+prompts?\b",
        r"\b(?:evaluators?|graders?|judges?|reviewers?)\b[^.\n]{0,40}\b(?:must|should|will)\s+(?:give|award|rate|score)\b",
        r"\bexploit\w*\b[^.\n]{0,30}\b(?:bugs?|loopholes?|glitch(?:es)?)\b",
        r"\bconceal\w*\b[^.\n]{0,30}\b(?:violations?|rules?)\b"),
          "prompt-injection or rule-evasion phrase", negatable=False),
    _Rule("dangerous", _rx(r"\brm\s+-\w*r\w*f", r"\bshutil\.rmtree\b", r"\bos\.(?:remove|unlink|system)\b", r"\bsubprocess\b",
                           r"\b(?:curl|wget|sudo|chmod|chown)\b", r"(?<![\w.])\.env\b", r"\bapi[_\s-]?keys?\b", r"\bssh\b"),
          "command or secret access that could harm the evaluation environment"),
    _Rule("fixed-choice", _rx(r"\b(?:option|choice)\s*#?\d+\b"),
          "numbered option in text; check it is not a fixed answer", negatable=False),
)

# Published constants that are not thresholds: the 0-10 Health/Dignity range, the
# 0-3 Energy budget range, the 48-month run and the L1-L10 level range.
_MASK = re.compile(r"\b0\s*(?:-|–|—|to)\s*(?:10|3)\b|\b48[\s-]*months?\b|\bmonth\s+48\b|\bL1\s*(?:-|–|—|to)\s*L10\b", re.I)
_CONDITION = re.compile(
    r"(?:\b(?:if|when|whenever|once|unless|until|while|below|above|under|over|beyond|exceeds?|exceeding|reach(?:es|ing)?|hits?"
    r"|at least|at most|less than|more than|fewer than|greater than|drops? (?:to|below)|falls? (?:to|below)|rises? (?:to|above))\b|[<>≤≥])"
    r"[^.;:,!?\n]{0,40}?((?<![\w.])(?:[1-9]\d*(?:\.\d+)?|0\.\d+)\s*%?|\bL(?:[1-9]|10)\b)", re.I)
_SPELLED = re.compile(
    r"\b(?:below|above|under|over|exceeds?|reach(?:es)?|at least|at most|less than|more than|fewer than|greater than"
    r"|drops? (?:to|below)|falls? (?:to|below)|rises? (?:to|above))\s+(?:two|three|four|five|six|seven|eight|nine|ten|half)\b", re.I)
_NUM_TAIL = re.compile(  # "3/10", "4 or lower", "2 and above": a threshold without a leading keyword
    r"(?<![\w.])(?:[1-9]\d*(?:\.\d+)?|0\.\d+)\s*(?:/\s*10\b|or (?:lower|higher|less|more|below|above|fewer|greater|worse|better)\b"
    r"|and (?:below|above|under|over)\b)", re.I)
_NUM_WORDS = r"(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
_SPAN = rf"(?:\d+|one|{_NUM_WORDS})\s+(?:months?|quarters?|years?|reviews?)\b"
_CALENDAR = _rx(  # run on the masked line, so the published 48-month length is not a trigger
    rf"\b(?:after|before|until|by|within|beyond|past|for|during|in|over)\s+(?:the\s+)?{_SPAN}",
    rf"\b{_SPAN}\s+(?:in|left|remain(?:ing)?|to go|later)\b",
    r"\b(?:half[\s-]?way|mid[\s-]?way|(?:first|second|latter) half)\b",
    r"\bmonths?\s*#?\d+",
    r"\b(?:after|before|until|by|from|since|past|beyond)\s+month\b",
    r"\b(?:quarters?|years?)\s*#?\d+\b",
    r"\bQ[1-4]\b", r"\bH[12]\b",
    rf"\b(?:month|quarter|year)\s+(?:one|{_NUM_WORDS})\b",
    r"\b(?:\d+(?:st|nd|rd|th)|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|last|final)\s+(?:month|quarter|year|review|promotion window)s?\b",
    rf"\b(?:first|last|final|initial|opening|closing)\s+(?:\d+|{_NUM_WORDS})\s+(?:months|quarters|years|reviews)\b",
)
_WEIGHT_FIELD = re.compile(r"\b(?:weighted_score|normalized_score|raw_value)\b")
_WEIGHT_WORD = re.compile(r"\bweight(?:s|ed|ing|ings)?\b", re.I)
_SCORE_CONTEXT = re.compile(r"\b(?:score|scores|scoring|ending|dimensions?|quantitative|evaluation)\b", re.I)
_DIM = r"(?:career level|level|wealth|health|dignity|skill|network|risk control)"
_DIM_SHARE = re.compile(rf"\b{_DIM}\b[^.;\n]{{0,60}}?\d+(?:\.\d+)?\s*(?:%|percent|points?)|\d+(?:\.\d+)?\s*(?:%|percent)[^.;\n]{{0,60}}?\b{_DIM}\b", re.I)
_NEGATION = re.compile(r"\b(?:do not|don't|does not|never|must not|should not|cannot|can't|not|no|nor|without|avoid|prohibited|forbidden)\b", re.I)
_SENTENCE_END = re.compile(r"[.!?;](?:\s|$)")
# A negation does not reach past a sentence end or a contrast word ("do not X; instead Y", "never X but Y").
_CLAUSE_END = re.compile(r"[.!?;](?:\s|$)|\b(?:but|instead|however|whereas|rather)\b", re.I)
_WORD = re.compile(r"[^\W\d_]+")
_TOKEN = re.compile(r"[^\W_]+")

# Common function words of other Latin-script languages that are not English words.
FOREIGN_WORDS = frozenset(
    "el los las una unos unas para pero como cuando porque está están también muy sobre entre hasta desde puede tiene "
    "hacer siempre nunca cada salud dignidad energía meses año años acción elegir riesgo nivel que del "
    "les une pour avec dans sont nous vous être avoir mais très chaque toujours jamais "
    "und nicht mit ist eine einen auf für wenn oder sehr immer jede "
    "della sono gli questo quando perché sempre ogni não uma você então".split())


# ---------------------------------------------------------------------------
# Text rules
# ---------------------------------------------------------------------------

def _negated(line: str, start: int) -> bool:
    """True when a negation precedes position ``start`` within the same clause."""
    head = line[:start]
    cut = max((m.end() for m in _CLAUSE_END.finditer(head)), default=0)
    return bool(_NEGATION.search(head[cut:]))


def _sentences(line: str) -> Iterator[str]:
    start = 0
    for match in _SENTENCE_END.finditer(line):
        yield line[start:match.end()]
        start = match.end()
    if line[start:].strip():
        yield line[start:]


def _english(rel: str, lineno: int, line: str) -> list[Finding]:
    out: list[Finding] = []
    runs, run = [], ""
    for ch in line + " ":
        if ch.isalpha() and not ch.isascii() and not unicodedata.name(ch, "").startswith("LATIN"):
            run += ch
        elif run:
            runs.append(run)
            run = ""
    if runs:
        severity = ERROR if any(len(r) >= 2 for r in runs) else REVIEW
        out.append(Finding(severity, rel, lineno, "english", f"non-Latin script {''.join(runs)[:20]!r}; deliverables must be English"))
    words = _WORD.findall(line.lower())
    accented = sorted({w for w in words if any(not c.isascii() for c in w)} - {r.lower() for r in runs})
    accented = [w for w in accented if all(c.isascii() or unicodedata.name(c, "").startswith("LATIN") for c in w)]
    if accented:
        out.append(Finding(REVIEW, rel, lineno, "english", f"accented words {accented[:5]}; check the text is English"))
    foreign = sorted({w for w in words if w in FOREIGN_WORDS})
    if len(foreign) >= 3 or (len(foreign) >= 2 and len(foreign) * 4 >= len(words)):
        out.append(Finding(REVIEW, rel, lineno, "english", f"possible non-English Latin-script text {foreign[:6]}"))
    return out


def _line_findings(rel: str, lineno: int, line: str) -> list[Finding]:
    out = _english(rel, lineno, line)
    for rule in TERM_RULES:
        # One finding per rule per line keeps reports readable, but it must be the most
        # severe one: a negated (review) mention must not hide a later affirmative one.
        best: Finding | None = None
        for match in rule.pattern.finditer(line):
            severity = REVIEW if rule.rule == "fixed-choice" else ERROR
            note = rule.message
            if severity == ERROR and rule.negatable and _negated(line, match.start()):
                severity, note = REVIEW, f"negated mention: {rule.message}"
            if best is None or (severity == ERROR and best.severity == REVIEW):
                best = Finding(severity, rel, lineno, rule.rule, f"{match.group(0).strip()!r}: {note}")
            if severity == ERROR:
                break
        if best:
            out.append(best)
    masked = _MASK.sub(lambda m: " " * len(m.group(0)), line)
    match = _CONDITION.search(masked) or _SPELLED.search(masked) or _NUM_TAIL.search(masked)
    if match:
        out.append(Finding(REVIEW, rel, lineno, "conditional-number",
                           f"{match.group(0).strip()!r}: number in a condition; never present an unpublished threshold as a rule"))
    match = _CALENDAR.search(masked)
    if match:
        out.append(Finding(REVIEW, rel, lineno, "calendar-trigger",
                           f"{match.group(0).strip()!r}: calendar-based trigger; prefer conditions on the run's own state and feedback"))
    out.extend(_weight_findings(rel, lineno, line))
    return out


def _weight_findings(rel: str, lineno: int, line: str) -> list[Finding]:
    """At most one score-weights finding per line: the most severe over every sentence."""
    found: list[tuple[str, str]] = []
    for sentence in _sentences(line):
        for field in _WEIGHT_FIELD.finditer(sentence):
            severity = REVIEW if _negated(sentence, field.start()) else ERROR
            found.append((severity, f"{field.group(0)!r}: ending-score internals must not appear in Skills"))
        context = _SCORE_CONTEXT.search(sentence)
        word = _WEIGHT_WORD.search(sentence)
        if word and context:
            has_number = bool(re.search(r"\d", sentence))
            severity = REVIEW if _negated(sentence, word.start()) and not has_number else ERROR
            found.append((severity, f"{sentence.strip()[:80]!r}: mentions ending-score weights"))
        share = _DIM_SHARE.search(sentence)
        if share and context:
            found.append((ERROR, f"{share.group(0).strip()!r}: states an ending-dimension share"))
    if not found:
        return []
    severity, text = next((f for f in found if f[0] == ERROR), found[0])
    return [Finding(severity, rel, lineno, "score-weights", text)]


# ---------------------------------------------------------------------------
# Named-event leakage
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class _Title:
    raw: str
    tokens: tuple[str, ...]
    published: bool


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _prepare_titles(titles: Iterable[str] | None) -> list[_Title]:
    prepared, seen = [], set()
    for raw in titles or ():
        tokens = tuple(_tokens(raw))
        if not tokens or tokens in seen:
            continue
        seen.add(tokens)
        prepared.append(_Title(raw, tokens, " ".join(tokens) in PUBLISHED_PHRASES))
    return prepared


def _title_findings(rel: str, text: str, titles: list[_Title]) -> list[Finding]:
    """Exact or near-exact (case- and punctuation-insensitive) title matches."""
    if not titles:
        return []
    toks: list[str] = []
    lines: list[int] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for tok in _tokens(line):
            toks.append(tok)
            lines.append(lineno)
    where: dict[str, list[int]] = {}
    for i, tok in enumerate(toks):
        where.setdefault(tok, []).append(i)
    out: list[Finding] = []
    for title in titles:
        n, target = len(title.tokens), " ".join(title.tokens)
        if n == 1:
            if len(target) >= 4 and target in where:
                out.append(Finding(REVIEW, rel, lines[where[target][0]], "event-title",
                                   f"single-word known event title {title.raw!r} appears; check it is generic wording"))
            continue
        starts = set(where.get(title.tokens[0], ()))
        for pos in where.get(title.tokens[1], ()):
            starts.update((pos - 1, pos))
        hit: tuple[int, str] | None = None
        for start in sorted(s for s in starts if s >= 0):
            for size in (n, n - 1, n + 1):
                window = toks[start:start + size]
                if size < 2 or len(window) < size:
                    continue
                joined = " ".join(window)
                if joined == target:
                    hit = (start, "exact")
                elif SequenceMatcher(None, joined, target).ratio() >= 0.9:
                    hit = hit or (start, "near-exact")
                if hit and hit[1] == "exact":
                    break
            if hit and hit[1] == "exact":
                break
        if hit:
            severity = REVIEW if title.published else ERROR
            out.append(Finding(severity, rel, lines[hit[0]], "event-title",
                               f"{hit[1]} match of known event title {title.raw!r}; named-event answers are prohibited"))
    return out


def collect_titles(runs_dir: Path | str, include_quarterly: bool = False) -> set[str]:
    """Event titles seen in local CareerLab trajectories (``kind == 'obs'`` lines).

    Quarterly phase titles are excluded by default: they are interface wording
    from the published rules, not story events.
    """
    from careerlab.mcp_client import phase  # lazy: keeps the lint free of MCP imports

    titles: set[str] = set()
    for path in sorted(Path(runs_dir).rglob("trajectory.jsonl")):
        with path.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if '"obs"' not in line:
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                obs = record.get("obs") if isinstance(record, dict) and record.get("kind") == "obs" else None
                if not isinstance(obs, dict):
                    continue
                if not include_quarterly and phase(obs) in ("energy", "main_action"):
                    continue
                title = (obs.get("current_event") or {}).get("title")
                if isinstance(title, str) and title.strip():
                    titles.add(title.strip())
    return titles


# ---------------------------------------------------------------------------
# Bundle structure
# ---------------------------------------------------------------------------

def _strip_invisible(text: str) -> str:
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


def _scan_text(rel: str, text: str, titles: list[_Title], first_line: int = 1) -> list[Finding]:
    """Text rules per line, then title matching; invisible format characters
    (zero-width spaces, bidi controls, BOM) are reported and removed first so
    they cannot split a term such as 'data<ZWSP>base' past the patterns."""
    out: list[Finding] = []
    for offset, line in enumerate(text.splitlines()):
        hidden = sorted({f"U+{ord(ch):04X}" for ch in line if unicodedata.category(ch) == "Cf"})
        if hidden:
            out.append(Finding(ERROR, rel, first_line + offset, "invisible",
                               f"invisible format characters {hidden[:5]}; they hide text from reviewers and from this lint"))
            line = _strip_invisible(line)
        out.extend(_line_findings(rel, first_line + offset, line))
    for finding in _title_findings(rel, _strip_invisible(text), titles):
        out.append(replace(finding, line=finding.line + first_line - 1))
    return out


def _decode(data: bytes) -> tuple[str, str]:
    """(text, encoding): UTF-8 first, then BOM-marked or NUL-patterned UTF-16/32,
    then Latin-1, so text rules still run on a file saved in the wrong encoding."""
    try:
        return data.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        pass
    if data.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        encoding = "utf-32"
    elif data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        encoding = "utf-16"
    elif data[1::2].count(0) > len(data) // 4:
        encoding = "utf-16-le"
    elif data[0::2].count(0) > len(data) // 4:
        encoding = "utf-16-be"
    else:
        encoding = "latin-1"
    try:
        return data.decode(encoding), encoding
    except UnicodeDecodeError:
        return data.decode("latin-1"), "latin-1"


def _exact(directory: Path, name: str) -> Path | None:
    """The entry named exactly ``name``. macOS filesystems are case-insensitive, so
    ``(d / 'SKILL.md').is_file()`` is also true for 'skill.md', which the Linux
    validator would not accept."""
    try:
        return next((p for p in directory.iterdir() if p.name == name), None)
    except OSError:
        return None


def _case_variant(directory: Path, name: str) -> str:
    try:
        other = next((p.name for p in directory.iterdir() if p.name.lower() == name.lower() and p.name != name), None)
    except OSError:
        other = None
    return f" (found {other!r}; names are case-sensitive on the evaluation system)" if other else ""


def _front_matter(rel: str, text: str, dir_name: str) -> list[Finding]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [Finding(ERROR, rel, 1, "front-matter", "SKILL.md must begin with '---' YAML front matter")]
    close = next((i for i in range(1, len(lines)) if lines[i].strip() in ("---", "...")), None)
    if close is None:
        return [Finding(ERROR, rel, 1, "front-matter", "front matter is not closed with '---'")]
    try:
        data = yaml.safe_load("\n".join(lines[1:close]))
    except yaml.YAMLError as exc:
        return [Finding(ERROR, rel, 1, "front-matter", f"invalid YAML: {str(exc).splitlines()[0]}")]
    if not isinstance(data, dict):
        return [Finding(ERROR, rel, 1, "front-matter", "front matter must be a YAML mapping")]
    out: list[Finding] = []
    name, description = data.get("name"), data.get("description")
    if not isinstance(name, str) or not name.strip():
        out.append(Finding(ERROR, rel, 1, "front-matter", "missing 'name'"))
    else:
        if not KEBAB.match(name) or len(name) > 64:
            out.append(Finding(ERROR, rel, 1, "front-matter", f"name {name!r} must be kebab-case, at most 64 characters"))
        if name != dir_name:
            out.append(Finding(ERROR, rel, 1, "front-matter", f"name {name!r} does not match directory {dir_name!r}"))
    if not isinstance(description, str) or not description.strip():
        out.append(Finding(ERROR, rel, 1, "front-matter", "missing 'description'"))
    elif len(description) > 1024:
        out.append(Finding(REVIEW, rel, 1, "front-matter", "description longer than 1024 characters"))
    if not "\n".join(lines[close + 1:]).strip():
        out.append(Finding(ERROR, rel, close + 1, "front-matter", "Skill body is empty"))
    return out


def _walk(value: Any, path: tuple[str, ...] = ()) -> Iterator[tuple[tuple[str, ...], Any]]:
    """(key path, value) for every key at every depth; list items keep the parent path."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield path + (str(k),), v
            yield from _walk(v, path + (str(k),))
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item, path)


def _key_line(raw: str, key: str, value: Any = None) -> int:
    """Line of ``"key"``, preferring the one that also holds the string value."""
    lines = raw.splitlines()
    hits = [n for n, line in enumerate(lines, 1) if f'"{key}"' in line]
    if isinstance(value, str) and value:
        fragment = json.dumps(value)[1:21]
        hits = [n for n in hits if fragment in lines[n - 1]] or hits
    return hits[0] if hits else 0


def _lint_manifest(bundle: Path, titles: list[_Title]) -> list[Finding]:
    rel, path = "manifest.json", _exact(bundle, "manifest.json")
    if path is None or not path.is_file():
        return [Finding(ERROR, rel, 0, "manifest", f"manifest.json is missing{_case_variant(bundle, 'manifest.json')}")]
    out: list[Finding] = []
    raw, encoding = _decode(path.read_bytes())
    if encoding != "utf-8":
        out.append(Finding(ERROR, rel, 0, "encoding", f"not valid UTF-8 (read as {encoding})"))
    try:
        data = json.loads(raw)
    except ValueError as exc:
        return out + [Finding(ERROR, rel, 0, "manifest", f"invalid JSON: {exc}")]
    if not isinstance(data, dict):
        return out + [Finding(ERROR, rel, 0, "manifest", "manifest must be a JSON object")]
    mode = data.get("mode")
    if mode != "agent":
        out.append(Finding(ERROR, rel, _key_line(raw, "mode"), "team-mode" if mode == "team" else "manifest",
                           f'"mode" must be "agent", found {mode!r}'))
    team = data.get("team")
    if not isinstance(team, str) or team.strip().lower() in PLACEHOLDER_TEAMS:
        out.append(Finding(ERROR, rel, _key_line(raw, "team"), "manifest", "team must be the real team name"))
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        out.append(Finding(ERROR, rel, _key_line(raw, "name"), "manifest", "missing submission name"))
    if not isinstance(data.get("instruction", ""), str):
        out.append(Finding(ERROR, rel, _key_line(raw, "instruction"), "manifest", "instruction must be a string"))
    for key in data:
        if key not in MANIFEST_KEYS and key.lower() not in ROUTING_KEYS:
            out.append(Finding(REVIEW, rel, _key_line(raw, key), "manifest",
                               f"key {key!r} is not in the published manifest; check the runner accepts it"))
    for keys, value in _walk(data):
        key, line = keys[-1], max(_key_line(raw, keys[-1], value), 1)
        if key.lower() in ROUTING_KEYS:
            out.append(Finding(ERROR, rel, line, "provider-routing", f"routing key {key!r} is prohibited"))
            continue
        if len(keys) > 1 and key.lower() == "mode" and isinstance(value, str) and value.strip().lower() == "team":
            out.append(Finding(ERROR, rel, line, "team-mode", f"nested {'.'.join(keys)!r} sets team mode"))
            continue
        if len(keys) > 1 or key not in MANIFEST_KEYS:  # key names such as "team_mode" carry meaning too
            out.extend(_scan_text(rel, key, titles, first_line=line))
        if isinstance(value, str) and keys not in (("team",), ("mode",)):
            out.extend(_scan_text(rel, value, titles, first_line=line))
    return out


def _lint_bundle(bundle: Path, titles: list[_Title]) -> list[Finding]:
    out = _lint_manifest(bundle, titles)
    skills = _exact(bundle, "skills")
    if skills is None or not skills.is_dir():
        return out + [Finding(ERROR, "skills", 0, "skills-dir", f"skills/ directory is missing{_case_variant(bundle, 'skills')}")]
    skill_dirs = sorted(p for p in skills.iterdir() if p.is_dir())
    if not any(_exact(d, "SKILL.md") for d in skill_dirs):
        out.append(Finding(ERROR, "skills", 0, "skills-dir", "no skills/<name>/SKILL.md found"))
    for skill in skill_dirs:
        skill_md = _exact(skill, "SKILL.md")
        if skill_md is None or not skill_md.is_file():
            out.append(Finding(ERROR, f"skills/{skill.name}", 0, "skills-dir",
                               f"Skill directory without SKILL.md{_case_variant(skill, 'SKILL.md')}"))
        for path in sorted(p for p in skill.rglob("*") if p.is_file() and p.name != ".DS_Store"):
            rel = path.relative_to(bundle).as_posix()
            if path.suffix.lower() in SCRIPT_SUFFIXES or "script" in path.relative_to(skill).parts[:-1]:
                out.append(Finding(REVIEW, rel, 0, "script", "executable script in a Skill; include only if the design needs it"))
            data = path.read_bytes()
            text, encoding = _decode(data)
            if encoding != "utf-8":
                if encoding == "latin-1" and b"\0" in data and path != skill_md and path.suffix.lower() not in TEXT_SUFFIXES:
                    out.append(Finding(REVIEW, rel, 0, "binary", "binary supporting file was not scanned; check it holds no text"))
                    continue
                out.append(Finding(ERROR, rel, 0, "encoding", f"not valid UTF-8 (read as {encoding}); Skill text must be UTF-8"))
            if path == skill_md:
                out.extend(_front_matter(rel, text, skill.name))
            out.extend(_scan_text(rel, text, titles))
    return out


def lint_bundle(bundle_dir: Path | str, known_titles: set[str] | None = None) -> list[Finding]:
    """Lint one bundle directory (manifest.json + skills/); file paths are bundle-relative."""
    return _lint_bundle(Path(bundle_dir), _prepare_titles(known_titles))


def _lint_policy_json(policy_dir: Path, bundle: Path, root: Path) -> list[Finding]:
    rel, path = "policy.json", policy_dir / "policy.json"
    if not path.is_file():
        return [Finding(ERROR, rel, 0, "policy-json", "policy.json is missing")]
    try:
        meta = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [Finding(ERROR, rel, 0, "policy-json", f"invalid JSON: {exc}")]
    if not isinstance(meta, dict):
        return [Finding(ERROR, rel, 0, "policy-json", "policy.json must be a JSON object")]
    out = [Finding(ERROR, rel, 0, "policy-json", f"missing key {key!r}") for key in POLICY_KEYS if key not in meta]
    for key in ("hypothesis", "refutation", "predicted_behaviour"):
        if key in meta and not str(meta[key]).strip():
            out.append(Finding(ERROR, rel, 0, "policy-json", f"{key!r} is empty"))
    if meta.get("name") != policy_dir.name:
        out.append(Finding(ERROR, rel, 0, "policy-json", f"name {meta.get('name')!r} differs from directory {policy_dir.name!r}"))
    if policy_dir.parent != root and meta.get("family") != policy_dir.parent.name:
        out.append(Finding(ERROR, rel, 0, "policy-json", f"family {meta.get('family')!r} differs from directory {policy_dir.parent.name!r}"))
    if not isinstance(meta.get("parents", []), list):
        out.append(Finding(ERROR, rel, 0, "policy-json", "parents must be a list"))
    skills = _exact(bundle, "skills")
    count = sum(1 for d in (skills.iterdir() if skills and skills.is_dir() else ()) if d.is_dir() and _exact(d, "SKILL.md"))
    if meta.get("skill_count") != count:
        out.append(Finding(ERROR, rel, 0, "policy-json", f"skill_count {meta.get('skill_count')!r} but bundle has {count} Skills"))
    try:
        manifest_name = json.loads((bundle / "manifest.json").read_text(encoding="utf-8")).get("name")
    except (OSError, ValueError, AttributeError):
        manifest_name = None
    if manifest_name is not None and manifest_name != meta.get("name"):
        out.append(Finding(ERROR, rel, 0, "policy-json", f"manifest name {manifest_name!r} differs from policy name"))
    return out


def lint_policy_tree(root: Path | str, known_titles: set[str] | None = None) -> dict[str, list[Finding]]:
    """Lint every ``<family>/<policy>/bundle`` under ``root``.

    Returns {policy directory relative to root: findings}; finding paths are
    relative to the policy directory ("bundle/skills/...", "policy.json").
    """
    root = Path(root)
    titles = _prepare_titles(known_titles)
    report: dict[str, list[Finding]] = {}
    bundles = sorted(p for p in root.rglob("bundle") if p.is_dir() and ((p / "skills").exists() or (p / "manifest.json").exists()))
    for bundle in bundles:
        policy_dir = bundle.parent
        found = [replace(f, file=f"bundle/{f.file}") for f in _lint_bundle(bundle, titles)]
        found += _lint_policy_json(policy_dir, bundle, root)
        report[policy_dir.relative_to(root).as_posix()] = found
    return report


def main(argv: list[str] | None = None) -> int:
    import argparse

    from careerlab.config import Settings

    settings = Settings()
    parser = argparse.ArgumentParser(description="Lint CareerLab policy bundles for competition compliance.")
    parser.add_argument("root", nargs="?", default=str(settings.lab_dir / "policies-src"))
    parser.add_argument("--runs", default=None, help="run directory for known event titles (default: CareerLab runs dir)")
    parser.add_argument("--no-titles", action="store_true", help="skip the named-event leakage check")
    args = parser.parse_args(argv)
    titles: set[str] | None = None
    if not args.no_titles:
        runs = Path(args.runs) if args.runs else settings.runs_dir
        titles = collect_titles(runs) if runs.is_dir() else None
    errors = 0
    for policy, findings in lint_policy_tree(args.root, titles).items():
        n_err = sum(f.severity == ERROR for f in findings)
        errors += n_err
        print(f"{policy}: {n_err} error(s), {len(findings) - n_err} review")
        for finding in findings:
            print(f"  {finding}")
    print(f"known event titles checked: {len(titles or ())}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
