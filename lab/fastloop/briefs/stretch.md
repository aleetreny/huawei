You are improving a manual (a set of Skills) that an LLM reads while it plays a 48-month career simulation through five game tools. A small model plays it (Claude Haiku in our tests; the official player is DeepSeek v4 flash), so the manual must be short, concrete and easy to follow turn after turn.

## The champion

The best manual so far is **<<champion>>**. Its Skills: <<skill_paths>>.
Its record: <<summary>>.

## Read before writing

1. Digests of the champion's latest race games, worst first: <<digest_dir>> (start with index.md). Look hardest at the completed games.
2. `lab/fastloop/lessons.md`: what is proven (keep it), what failed (do not repeat it).
3. `lab/fastloop/history.md`: every manual already tried in this race and its result.

## Task: the frontier

Completed careers still lose most of their missing score on career level and wealth: no game in any of our runs went beyond the fifth level, and wealth ends around 40–50 out of 100 even in the best games. Find, in the completed games, the decisions where level or wealth could have grown and did not (promotion windows reached with a weak input, pay or role talks taken without asking for terms, late-career quarters spent on maintenance). Write ONE variant of the champion with one change that grows level or wealth in careers that already survive, without weakening anything that keeps careers alive (see the guardrails in lessons.md). Editing a few sentences is better than rewriting.

## Output: write exactly these files

- `<<out_dir>>/bundle/skills/<skill-name>/SKILL.md` for every Skill (same Skill folders as the champion unless your change needs otherwise). Each starts with YAML front matter: `name` equal to its folder name, and a one-line `description`.
- `<<out_dir>>/bundle/manifest.json`: `{"team": "Gradient Depression", "name": "<<name>>", "mode": "agent", "instruction": ""}`
- `<<out_dir>>/policy.json` with keys: `family` "<<family>>", `name` "<<name>>", `parents` ["<<champion>>"], `hypothesis` (the missed growth, its evidence with counts, and why the change captures it), `change`, `predicted_behaviour`, `refutation`, `skill_count`, `notes` ("fast race <<kind>> designer").

## Rules (a linter rejects violations)

- English. Describe general behaviour only. Never name specific events or story titles, never give a fixed answer to a specific event, never mention specific months or dates, never state unpublished thresholds, weights or formulas. Published handbook rules may be described in words.
- Do not copy sentences from the digests.
- Keep the whole manual under 650 words.
- Write only inside `<<out_dir>>`. Change no other file.

When you finish, reply with one paragraph: the missed growth, its evidence, and the change.
