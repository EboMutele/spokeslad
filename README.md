# Spokeslad

**A free Claude Code plugin that runs launches and public relations for software
products: listening, planning, on-message drafts, review and measurement. You publish.**

It follows the workflow big-company communications teams use: one agreed source of
truth for what you say, daily listening, launches sized to the news, an independent
review of every draft, and numbers instead of vibes. Nothing goes out without your
approval: it drafts, you decide.

Its first test was its own launch: see [`.spokeslad/`](.spokeslad/), including the
[red-team report](.spokeslad/launches/2026-11-17-v0-1/redteam.md) that caught problems
in its own claims.

## Install

In Claude Code:

```
/plugin marketplace add EboMutele/spokeslad
/plugin install spokeslad@spokeslad
```

Requires Python 3.9+ for the helper scripts (standard library only, nothing to install).

## Quick start

Open Claude Code in your product's repo and run:

1. `/spokeslad:brief`: reads your repo and site, asks a few questions, and writes your
   messaging house: positioning, three pillars with proof, approved claims, things
   never to say.
2. `/spokeslad:listen`: first scan of Hacker News, Reddit, GitHub, competitor releases
   and the web, with a one-screen digest.
3. `/spokeslad:measure`: your baseline, including how often AI assistants mention you.

When you ship something: `/spokeslad:plan <what's shipping>`, then `/spokeslad:launch`.

## Commands

| Command | What it does |
|---|---|
| `/spokeslad:brief` | Builds the messaging house and config every other command checks against |
| `/spokeslad:listen` | Daily monitoring and a digest: what changed, why it matters, what to do |
| `/spokeslad:plan` | Scores your news into tiers 1 to 4 and plans channels, timeline and targets to match |
| `/spokeslad:launch` | Writes the launch kit: post, changelog, Show HN, X thread, LinkedIn, Reddit, email, FAQ, tough questions, demo script, holding statements |
| `/spokeslad:pitch` | Finds creators and newsletters who really cover your space and drafts a personal pitch for each |
| `/spokeslad:redteam` | Lint plus an independent reviewer agent that checks every claim and reads like your harshest critic |
| `/spokeslad:crisis` | Severity triage, holding statement in minutes, response plan and update cadence |
| `/spokeslad:measure` | Share of voice, sentiment, message pull-through, stars and AI-answer visibility over time |

## How it works

```
brief (once) ──> listen (daily) ──> plan ──> launch / pitch ──> redteam ──> you approve ──> you publish
                     │                                                                       │
                     └──> crisis (when needed) ──> redteam ──> you approve                   │
                     ▲                                                                       │
                     └──────────────────────────── measure (weekly) <────────────────────────┘
```

Everything lives in a `.spokeslad/` folder in your project:

| Path | Contents |
|---|---|
| `messaging.md` | Positioning, pillars, proof, approved claims, objections, voice, boilerplate |
| `config.json` | Product, competitors, keywords, key messages, approved claims, never-say list, AI probe questions |
| `signals/` | Collected mentions, one file per day (add to `.gitignore`) |
| `digests/` | Daily listening digests |
| `launches/<date-slug>/` | Plan, drafts, red-team report, publishing checklist |
| `crisis/<date-slug>/` | Holding statement and response plan |
| `ai-answers/` | Buyer questions and what AI assistants answered |
| `metrics.csv` | One row per measurement run |
| `log.md` | What was approved and published, with links |

## The `spokeslad` helper

Skills call a small command-line tool for the parts code does better than judgment.
You can run it yourself too (`bin/spokeslad` in the plugin):

```
spokeslad init                     # create .spokeslad/
spokeslad listen --days 2          # collect new mentions from HN, Reddit, GitHub, feeds
spokeslad measure --days 7 --stars # share of voice, pull-through, AI visibility, stars
spokeslad measure --probe-ai       # ask Claude your buyer questions first (ANTHROPIC_API_KEY)
spokeslad lint .spokeslad/launches/2026-11-04-v1   # check drafts; exits 1 on errors
```

`lint` fails drafts on hype ("revolutionary", "the only", "10x faster"), unsourced
percentages, money and user counts (and warns on unsourced time claims), bracketed
placeholders, never-say phrases, leftover placeholders, Show HN titles that break HN's
format, X posts over 280 characters (URLs counted as 23), LinkedIn posts over 3,000
characters, and Reddit posts that do not say you made the thing. Mark a sourced line
with `[source: https://...]`, or add the claim to `approved_claims`.

Set `GITHUB_TOKEN` to raise GitHub API rate limits. `listen` waits a second between
requests (`--delay`) and retries once on rate limits. Reddit's unauthenticated search
is off by default; enable it with `"sources": {"reddit": true}` if you accept its
terms, otherwise `/spokeslad:listen` covers Reddit through web search.

## Running it every day

Set up a daily scheduled task that runs `/spokeslad:listen` in your project, or use
cron with `claude -p "/spokeslad:listen"`. Run `/spokeslad:measure` weekly and at
T+7 and T+30 after each launch.

## Principles

- **You publish, under your name.** Spokeslad never posts, sends, replies or votes.
- **No astroturfing.** No alternate accounts, no fake reviews or testimonials, no
  upvote rings. Every Reddit draft says you made it.
- **Proof or it doesn't ship.** Claims trace back to the messaging house or the
  product itself.
- **The work does not grade itself.** Drafts go through a reviewer agent that never
  sees the conversation that wrote them.
- **Measure, don't guess.** Numbers come from data collected and computed by code,
  with their caveats.

## Development

```
python3 -m pytest -q              # tests for the helper CLI
claude plugin validate . --strict # plugin manifest and structure
claude --plugin-dir .             # try it locally
```

## License

MIT
