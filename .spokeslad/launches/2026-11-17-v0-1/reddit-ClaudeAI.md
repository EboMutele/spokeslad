<!-- Where: the "Built with Claude" project showcase megathread, unless you have 50+ karma
on r/ClaudeAI. Read Rule 7 (showcase requirements) first and adjust to it. -->

**Spokeslad: a Claude Code plugin that does launch prep and comms for your project (I built it, it's free and MIT)**

I built this because I'm bad at telling people about my projects, and AI launch copy
mostly makes that worse.

What it does in Claude Code:

- `/spokeslad:brief` reads your repo and writes one messaging file: audience, what you
  want people to repeat, proof, approved claims, never-say list.
- `/spokeslad:listen` collects mentions from HN, Reddit and GitHub and gives you a
  one-screen digest.
- `/spokeslad:plan` and `/spokeslad:launch` size the news and draft the posts, FAQ,
  tough questions, demo script and holding statements.
- `/spokeslad:redteam` runs a linter and a separate reviewer agent over every draft
  before you see it.

It never posts for you. You publish.

How Claude is used: the skills and a reviewer subagent do the judgment; a small Python
helper does the counting and rule checks. The first test was its own launch, and those
files are in the repo, including the red-team report.

Repo: https://github.com/EboMutele/spokeslad

It's v0.1. I'd especially like to hear whether the review step catches what you would.
