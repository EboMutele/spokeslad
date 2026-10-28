# Messaging house: Spokeslad

The single source of truth for what we say about Spokeslad. Every draft is checked
against this file. If a claim is not here with proof, it does not go out.

Last reviewed: 2026-10-28

## Positioning

For **developers who build and ship software products** (open-source tools, Claude
Code plugins, dev tools, indie SaaS) and **have no comms team**, **Spokeslad** is a
**Claude Code plugin that runs the public-relations workflow** big companies use:
one source of truth for what you say, daily listening, launches sized to the news,
an independent review of every draft, and measurement. Unlike general marketing skill
packs or journalist-focused PR toolkits, it is **built around where developers
actually talk**: Hacker News, Reddit, GitHub and release feeds, with platform rules
checked by code, and it **never publishes anything for you**.

## Audience

- Primary: solo developers and small teams shipping dev tools, open-source projects
  and Claude Code plugins. They already use Claude Code. They hang out on HN,
  r/ClaudeAI, GitHub, X and Bluesky. They distrust marketing and hate hype.
- Secondary: technical founders of early SaaS products preparing a launch.
- Not for: agencies managing many client brands (multi-client tools fit better);
  anyone who wants automated posting, follower growth hacks or press-release
  distribution at scale.

## The problem, in their words

- Builders say good projects die quietly because nobody hears about them, and they
  dread "doing marketing".
- Generic AI launch copy reads as hype; HN and Reddit punish it fast.
- Launches are one-off scrambles: no plan, no prepared answers, no idea afterwards
  whether it worked.
- In developer search, "PR" means pull request. Our audience will not search for
  "PR tool"; they search for launch, Show HN, announcing, getting users.
  (Observed 2026-10-28: buyer-style searches for "PR for a developer tool" return
  pull-request tools only.)

## Pillars

### Pillar 1: Proof or it doesn't ship

- Message: every draft is checked against your approved claims, by code and by a
  separate reviewer agent, before you see it.
- Proof: `spokeslad lint` rules for hype, unsourced numbers, never-say phrases and
  placeholders (scripts/spokeslad.py); the independent red-team agent
  (agents/redteam.md); the test suite (tests/test_spokeslad.py).

### Pillar 2: Built for where developers talk

- Message: it listens on Hacker News, Reddit, GitHub and competitor release feeds,
  and checks drafts against those platforms' rules.
- Proof: `spokeslad listen` sources (HN Algolia API, Reddit search, GitHub issues and
  releases, RSS/Atom); lint rules for Show HN titles, X length with URLs counted as 23
  characters, LinkedIn length and Reddit disclosure.

### Pillar 3: You stay the voice

- Message: Spokeslad drafts, you decide. It never posts, sends, replies or votes,
  and every Reddit draft says you made the thing.
- Proof: no posting code exists in the plugin; the skills' rules sections; the
  Reddit disclosure check in `spokeslad lint`.

Supporting point (not a pillar): it measures share of voice, message pull-through and
how often AI assistants mention you, with numbers computed by code.

## Approved claims

| Claim | Proof |
|---|---|
| never posts on your behalf | No posting code in the repo; README principles |
| checks every draft against your approved claims | skills/redteam, agents/redteam.md, `spokeslad lint` |
| listens on Hacker News, Reddit and GitHub | scripts/spokeslad.py listen |
| standard library only | scripts/spokeslad.py imports |
| MIT licensed | LICENSE |
| free and open source | LICENSE, public repo |

## Do not claim (yet)

- "First" or "only" anything. Other PR plugins exist: Newsjack (elvisun/newsjack,
  journalist and newsjacking focus, about 1.7K stars per a listing verified
  2026-10-25), Claude-PR-Media-Work-Plugin (danielrosehill, agency-style monitoring
  and comms), single-skill PR and crisis packs, and broad marketing packs such as
  coreyhaines31/marketingskills.
- Any user numbers, stars, or results. We have no users yet.
- That it works with agents other than Claude Code. Untested.
- That it improves launch outcomes. Not measured yet.

## Objections and honest answers

| Objection | Answer |
|---|---|
| "Another AI marketing slop machine." | It is built to block slop: a linter fails drafts with hype and unsourced numbers, and a separate reviewer reads drafts like a cynical HN commenter. You can read the rules in the repo. |
| "Why not just use marketingskills or Newsjack?" | Use them if they fit. marketingskills is broad growth marketing; Newsjack focuses on journalists and news cycles. Spokeslad focuses on developer channels and a review step before you publish. They can coexist. |
| "Will it post for me?" | No, by design. You publish under your own name. |
| "Does it need paid APIs?" | No. Listening uses public endpoints; `GITHUB_TOKEN` and `ANTHROPIC_API_KEY` are optional. |
| "Is 'PR' confusing for developers?" | Yes, so we say launch and communications, and "public relations" in full where needed. |
| "Is it proven?" | Not yet. Version 0.1. Its first test was launching itself; that material is in the repo. |

## Voice

- We sound like: a calm, dry senior engineer who has done a few launches. Short
  sentences. Concrete. A little wry.
- We never sound like: a growth hacker, a press release, a LinkedIn influencer.
- Use: launch, announcement, listening, approve, proof, draft.
- Avoid: "PR" alone (pull-request confusion), revolutionary, supercharge, unlock,
  game-changer, "excited to announce".

## Boilerplate

- 25 words: Spokeslad is a free Claude Code plugin that runs launches and public
  relations for software products: listening, planning, on-message drafts, review
  and measurement. You publish.
- 50 words: Spokeslad is a free, open-source Claude Code plugin that gives developers
  the communications workflow big companies use. It listens on Hacker News, Reddit and
  GitHub, sizes and plans launches, drafts every asset from one messaging source,
  checks each draft by code and by an independent reviewer, and measures results. It
  never posts for you.
- 100 words: Spokeslad is a free, open-source Claude Code plugin for developers who
  ship products but have no comms team. You brief it once on what your product is,
  who it's for and what you can prove. Every day it listens on Hacker News, Reddit,
  GitHub and competitor release feeds and tells you what changed and what to do. When
  you ship, it sizes the news, plans the launch and drafts the announcement, Show HN
  post, threads, FAQ and creator pitches, then lints and red-teams them. It measures
  share of voice and AI-answer visibility. You approve and publish everything
  yourself.

## Spokesperson and contacts

- Spokesperson: the maker, EboMutele, speaking in first person.
- Contact: GitHub issues and discussions on EboMutele/spokeslad.
