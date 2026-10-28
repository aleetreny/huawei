# t13-read-v4 — Gradient Depression

Submission for Huawei TechArena UK 2026, *Career Survival*, Cut 1.

- **Platform:** JiuwenSwarm 0.2.4b3, single-agent `agent` mode, designated model `deepseek-v4-flash`.
- **Skills:** one Skill, `skills/career-rules/`, used on every turn. It keeps a one-line status note, reads each story option for likely stat changes and hidden risk, protects Skill, Network and Output just before a review, and sets quarterly Energy and main actions in priority order.
- **Manifest instruction:** repeats the scope rules that matter most (stories and quarterly phases are decided separately; options that may bury a problem are dropped; review preparation; the status line).
- **No scripts and no reference files.** The agent uses only the official tools and what they return during the run.

Design documents:

- `design/skills_design.md`: what the Skill does, how it is organised and why.
- `design/decision_report.md`: how we decided, the evidence behind each choice and its limits.
