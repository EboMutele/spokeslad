---
name: measure
description: Measure what communications are achieving - share of voice against competitors, mention volume and sentiment, key-message pull-through, GitHub stars, and how often AI assistants mention the product when asked buyer questions - and compare with the baseline and launch targets. Reports what changed, why, and what to do. Use weekly, at launch T+7 and T+30, or when the user asks if PR is working.
argument-hint: "[days, default 7]"
---

# Measure: what changed, why, what to do

Requires `.spokeslad/config.json` and some collected signals (`/spokeslad:listen`).

## 1. Collect AI-answer visibility

When someone asks an AI assistant "what's the best tool for X", the answer works like
a press clipping. Measure it with the buyer questions in `config.json`
(`ai_probe.questions`):

- If `ANTHROPIC_API_KEY` is set, add `--probe-ai` to the command below. It asks a
  model without web access, so it reflects what models already "know": a slow,
  lagging signal.
- Also run each question through WebSearch yourself and save what a searching
  assistant would surface: for each question, write
  `.spokeslad/ai-answers/YYYY-MM-DD/qNN.json` as
  `{"question": "...", "answer": "<the names and order a buyer would see>", "source": "web-search"}`.
  Keep the question wording identical across runs so results are comparable.

## 2. Compute

Run `"${CLAUDE_PLUGIN_ROOT}/bin/spokeslad" measure --days N --stars` from the project
root (N from the user, default 7; add `--probe-ai` as above). It appends a row to
`.spokeslad/metrics.csv` and prints share of voice (raw and engagement-weighted),
mentions with rough sentiment, pull-through of each key message, AI mention rate and
average rank, stars, and changes since the last run.

If GitHub or other sources are unreachable, note which numbers are missing rather
than estimating them.

## 3. Interpret honestly

Write `.spokeslad/reports/YYYY-MM-DD.md` and show the user, on one screen:

1. **What changed**: the 3 to 5 numbers that moved, with the actual values.
2. **Why**: link each change to specific events from the signals and log (a launch,
   a thread, a competitor release). If you cannot link it, say it is unexplained.
3. **Against targets**: for active launches, each target from plan.md with actual
   vs. target.
4. **What to do**: at most 3 actions.
5. **Caveats**: small samples (under ~20 mentions, under ~10 AI answers) are noise;
   sentiment is a keyword heuristic; correlation is not attribution.

Read the underlying mentions before claiming a sentiment shift. Never present a
number you did not compute or retrieve.
