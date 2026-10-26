You are writing a manual (a set of Skills) that an LLM reads while it plays a 48-month career simulation through five game tools. A small model plays it (Claude Haiku in our tests; the official player is DeepSeek v4 flash), so the manual must be short, concrete and easy to follow turn after turn.

## Why a bold manual

The race is stuck: <<stuck_count>> challengers built on the champion **<<champion>>** finished without beating it. Its record: <<summary>>. Small edits are not moving the score. Your job is a manual built on a different premise.

## Read before writing

1. `lab/fastloop/lessons.md`: the guardrails are proven; keep them. Everything else may change.
2. `lab/fastloop/history.md`: what was already tried in this race. Pick a premise it does not show, or one that failed for a reason you can fix.
3. The champion's Skills (<<skill_paths>>) and its worst games: <<digest_dir>> — to see what the champion cannot do.
4. The game's published rules: the handbook text quoted in lessons.md and in the champion's Skills.

## Premises to choose from (or invent a better one)

1. First-year promotion sprint: everything serves the first promotion window, then consolidate.
2. Extreme simplicity: the whole manual in at most 150 words, so a small model never loses the thread.
3. A fixed checklist the player writes in its note every turn before choosing.
4. Separate Skills for quarter-end allocation and for story choices, each very short.
5. Reliability first: the manual's only goal is to finish all 48 months; growth only when nothing is at risk.
6. Late-career push: once the career is safe, change mode to reach beyond the fifth level and grow wealth.

## Output: write exactly these files

- `<<out_dir>>/bundle/skills/<skill-name>/SKILL.md` for every Skill. Each starts with YAML front matter: `name` equal to its folder name (lowercase words joined by hyphens), and a one-line `description`.
- `<<out_dir>>/bundle/manifest.json`: `{"team": "Gradient Depression", "name": "<<name>>", "mode": "agent", "instruction": ""}`
- `<<out_dir>>/policy.json` with keys: `family` "<<family>>", `name` "<<name>>", `parents` [], `hypothesis` (the premise, the evidence that motivates it, and why it should beat the champion), `change` (the premise in one sentence), `predicted_behaviour`, `refutation`, `skill_count`, `notes` ("fast race bold designer; premise: ...").

## Rules (a linter rejects violations)

- English. Describe general behaviour only. Never name specific events or story titles, never give a fixed answer to a specific event, never mention specific months or dates, never state unpublished thresholds, weights or formulas. Published handbook rules may be described in words.
- Do not copy sentences from the digests.
- At most 650 words in total.
- Write only inside `<<out_dir>>`. Change no other file.

When you finish, reply with one paragraph: the premise, why it should work, and what would prove it wrong.
