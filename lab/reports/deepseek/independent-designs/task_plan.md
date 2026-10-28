# Independent Skill designs

- Complete: read project rules, public handbook, competition rules, t13-final and review reference.
- Complete: write three self-contained alternatives, perception guide, falsifiers and critique.
- Complete: check lengths, front matter and content constraints; document handoff.
- Complete: prepare documentation on the existing DeepSeek line for commit/push; request integration in the response.

Scope: design only; no games, API spending, submission, or changes to existing candidate Skills.
Use user general findings as premises; no event mappings from data.

## Errors

- `uv run careerlab lint --help`: local entrypoint cannot import careerlab; `uv run python -m careerlab.cli` works.
- Bundle lint on standalone Skill directories: missing manifest.json and skills/. Expected packaging mismatch; these are proposed files, not final bundles. No claim of bundle validation.
- Shell glob careerlab/lint*: no matching file; no code changes needed. Static document validation is sufficient for this request.
