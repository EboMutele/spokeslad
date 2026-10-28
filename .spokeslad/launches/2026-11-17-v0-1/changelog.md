# Changelog

## 0.1.0 (2026-11-17)

First release.

- Skills: brief, listen, plan, launch, pitch, redteam, crisis, measure.
- Agent: redteam, an independent reviewer for drafts.
- `spokeslad` helper (Python standard library only):
  - `init` creates the `.spokeslad/` workspace.
  - `listen` collects mentions from Hacker News, Reddit, GitHub issues, competitor
    releases and RSS/Atom feeds, de-duplicated across runs.
  - `measure` computes share of voice (raw and engagement-weighted), key-message
    pull-through, rough sentiment, GitHub stars and AI-answer visibility, and appends
    to `metrics.csv`.
  - `lint` checks drafts for hype, unsourced numbers, never-say phrases,
    placeholders and platform rules (Show HN title, X length, LinkedIn length,
    Reddit disclosure).
- Test suite for the helper.
