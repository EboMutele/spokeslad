---
name: redteam
description: Independent review of any Spokeslad drafts before the user sees or publishes them. Runs the deterministic linter, then sends the drafts to a separate reviewer agent that did not write them, to check every claim against the messaging house and the facts, and to read them like the toughest critic in each channel. Use after /spokeslad:launch, /spokeslad:pitch or /spokeslad:crisis, or on any draft the user wants checked.
argument-hint: "<folder or files to review>"
---

# Red team: the work does not grade itself

## 1. Linter first

Run `"${CLAUDE_PLUGIN_ROOT}/bin/spokeslad" lint <paths>` from the project root. It
catches hype, unsourced numbers, never-say phrases, placeholders, missing Reddit
disclosure and platform limits (Show HN title, X length, LinkedIn length). Fix the
errors before step 2; there is no point paying for judgment on mechanical problems.

## 2. Independent reviewer

Use the `spokeslad:redteam` agent. Give it only: the paths of the drafts, the path of
`.spokeslad/messaging.md`, and the plan if there is one. Do not give it your
reasoning, the conversation, or what you hoped the drafts would achieve. A reviewer
who knows the intent reads what was meant instead of what was written.

## 3. Act on the findings

The agent returns blocking and non-blocking findings. Fix every blocking finding.
Apply non-blocking ones where they improve the draft. If you disagree with a finding,
keep the draft but record the disagreement and your reason.

Save the agent's report and your responses as `redteam.md` in the same folder, then
re-run the linter. Only then show the drafts to the user, with a one-line summary of
what the red team changed.
