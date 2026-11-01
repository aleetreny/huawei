# c3-k6 — Gradient Depression

Submission for Huawei TechArena UK 2026, *Career Survival*, Cut 3 (final).

- **Platform:** JiuwenSwarm 0.2.4b3, single-agent `agent` mode, designated model `deepseek-v4-flash`.
- **Skills:** one Skill, `skills/career-rules/`, used on every turn. It sets a one-reply turn loop, keeps a one-line status note, reads each story option for likely stat changes and hidden risk, protects Skill, Network and Output before each review, switches to a zero-risk protocol when the starting level has stalled, and sets quarterly Energy and main actions in priority order, with a quick reference for stats near a limit.
- **Changes since Cut 2 (`mv-5r`):** back to the story rules of our Cut 1 Skill (`t13-read-v4`) with the Cut 2 turn loop; at the starting level a mild risk may keep Network and Output in both months before the first two reviews; a stalled start (two reviews without promotion) now has an explicit protocol, because in our runs the third review at the starting level was lost to hidden risk rather than to a missing stat; Health and Wealth brakes with concrete cues are in the Skill and in the manifest, and the level-4 Skill quarter from Cut 2 is kept.
- **Manifest instruction:** repeats the rules that matter most (the two-call turn loop and never ending a reply with text only; stories and quarterly phases decided separately; options that may bury a problem dropped; review preparation; the stalled-start protocol; the one-line note).
- **No scripts and no reference files.** The agent uses only the official tools and what they return during the run.

Design documents:

- `design/skills_design.md`: what the Skill does, how it is organised and why.
- `design/decision_report.md`: how we decided, the evidence behind each choice and its limits.
