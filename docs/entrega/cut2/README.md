# mv-5r — Gradient Depression

Submission for Huawei TechArena UK 2026, *Career Survival*, Cut 2.

- **Platform:** JiuwenSwarm 0.2.4b3, single-agent `agent` mode, designated model `deepseek-v4-flash`.
- **Skills:** one Skill, `skills/career-rules/`, used on every turn. It sets a one-reply turn loop, keeps a one-line status note, reads each story option for likely stat changes and hidden risk, protects Skill, Network and Output just before a review, and sets quarterly Energy and main actions with a plan for each level.
- **Changes since Cut 1 (`t13-read-v4`):** the same story judgement, played with about a third of the tokens: each decision is one reply with two tool calls, the note is one line, the quarterly plan follows the level, and the hidden costs of polite or helpful options are named at the starting level only.
- **Manifest instruction:** repeats the rules that matter most (the two-call turn loop and never ending a reply with text only; stories and quarterly phases decided separately; options that may bury a problem dropped; review preparation; the quarterly plan from level 4; the one-line note).
- **No scripts and no reference files.** The agent uses only the official tools and what they return during the run.

Design documents:

- `design/skills_design.md`: what the Skill does, how it is organised and why.
- `design/decision_report.md`: how we decided, the evidence behind each choice and its limits.
