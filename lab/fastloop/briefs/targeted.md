You are improving a manual (a set of Skills) that an LLM reads while it plays a 48-month career simulation through five game tools. A small model plays it (Claude Haiku in our tests; the official player is DeepSeek v4 flash), so the manual must be short, concrete and easy to follow turn after turn.

## The champion

The best manual so far is **<<champion>>**. Its Skills: <<skill_paths>>.
Its record: <<summary>>.

## Read before writing

1. Digests of the champion's latest race games, worst first: <<digest_dir>> (start with index.md). Each line is one decision: the visible state before it, the option taken and the ones declined, the player's note, and the game's feedback.
2. `lab/fastloop/lessons.md`: what is proven (keep it), what failed (do not repeat it).
3. `lab/fastloop/history.md`: every manual already tried in this race and its result. Do not repeat a failed idea unless you change what made it fail.

## Task

Find the single most costly failure pattern in the champion's games. Early exits cost the most (dismissal after a second weak review, usually by the end of the second year; trust crisis after hidden risk blows up; blackout), then a low career level and low wealth. Support it with evidence from at least two games. Then write ONE variant of the champion that changes one idea to fix that pattern and keeps everything else. Editing a few sentences is better than rewriting.

## Output: write exactly these files

- `<<out_dir>>/bundle/skills/<skill-name>/SKILL.md` for every Skill (same Skill folders as the champion unless your change needs otherwise). Each starts with YAML front matter: `name` equal to its folder name, and a one-line `description`.
- `<<out_dir>>/bundle/manifest.json`: `{"team": "Gradient Depression", "name": "<<name>>", "mode": "agent", "instruction": ""}`
- `<<out_dir>>/policy.json` with keys: `family` "<<family>>", `name` "<<name>>", `parents` ["<<champion>>"], `hypothesis` (the failure pattern, its evidence with counts, and why the change fixes it), `change` (one or two sentences), `predicted_behaviour` (what the player will visibly do differently), `refutation` (which result would show the idea is wrong), `skill_count` (number of Skills), `notes` ("fast race <<kind>> designer").

## Rules (a linter rejects violations)

- English. Describe general behaviour only. Never name specific events or story titles, never give a fixed answer to a specific event, never mention specific months or dates, never state unpublished thresholds, weights or formulas. Published handbook rules may be described in words.
- Do not copy sentences from the digests.
- Keep the whole manual under 650 words.
- Write only inside `<<out_dir>>`. Change no other file.

When you finish, reply with one paragraph: the failure pattern, its evidence, and the change.
