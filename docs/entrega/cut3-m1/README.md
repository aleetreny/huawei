# VERSION — Gradient Depression

Submission for Huawei TechArena UK 2026, *Career Survival*, Cut 3 (final).

- **Platform:** JiuwenSwarm 0.2.4b3, single-agent `agent` mode, designated model `deepseek-v4-flash`.
- **Skills:** one Skill, `skills/career-rules/`, used on every turn. It sets a one-reply turn loop, keeps a one-line status note, reads each story option for likely stat changes and hidden risk, protects Skill, Network and Output just before a review, and sets quarterly Energy and main actions with a plan for each level.
- **Changes since Cut 2 (`mv-5r`):** the hidden costs are named before every review, as in our best development careers; while the HR remark is friendly, one mild risk a month is accepted when it grows Skill, Network or Output more than any safe option; at the starting level the quarter before a review buys one point of Health and spends the rest on the review; a stalled start (two reviews without a promotion) has its own zero-risk protocol.
- **Manifest instruction:** repeats the rules that matter most (the two-call turn loop and never ending a reply with text only; stories and quarterly phases decided separately; options that may bury a problem dropped; review preparation; the quarterly plan from level 4; the growth exception; the stalled-start protocol; the one-line note).
- **No scripts and no reference files.** The agent uses only the official tools and what they return during the run.

Design documents:

- `design/skills_design.md`: what the Skill does, how it is organised and why.
- `design/decision_report.md`: how we decided, the evidence behind each choice and its limits.
