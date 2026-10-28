# Tough questions: talking points

These are notes to answer from, in your own words. Do not paste them into HN: HN
reportedly asks that comments not be AI-generated or AI-edited (reported March 2026;
confirm on the guidelines page before launch).

**"This is an AI slop generator for marketing."**
- Fair worry; stopping slop is the point.
- The linter fails hype words and unsourced percentages, money and user counts.
- The reviewer agent checks drafts without seeing the conversation that wrote them.
- The rules are in scripts/spokeslad.py; ask what they miss.

**"How is this different from Newsjack?"**
- Newsjack is good and more established. It focuses on journalists and news cycles.
- Spokeslad focuses on developer channels, launch sizing and checking drafts before you
  publish. Some people will want both. Never knock them.

**"Did Spokeslad write this post?"**
- Be exact: it drafted from the messaging file; the linter and reviewer checked it; you
  rewrote it in your own words for HN. (Only say this if you did rewrite it.)

**"Where are the users? Any evidence it works?"**
- None yet beyond its own launch. It's v0.1.
- Commit: you'll post the numbers in a week and again in a month.

**"The name is weird, and PR means pull request."**
- Both true. That's why the copy says launch and public relations, not PR.

**"Can't I just prompt Claude to write a launch post?"**
- For a small update, yes, and the plan step will tell you so.
- What it adds: one source of truth across assets, listening, tiering, checks by code
  and by a separate reviewer, measurement over time.

**"Does it scrape Reddit or break platform terms?"**
- Reddit is off by default; you turn it on in config. Without it, Reddit is covered
  through web search.
- When on, it makes one unauthenticated search request per term per run, waits a
  second between requests and backs off once on rate limits. It never posts, votes or
  sends.

**"Why trust a comms tool to be honest?"**
- Don't; check it. The reviewer is instructed to check each claim against your proof
  and open the links, and its report is committed alongside the drafts.

**"Where does my data go?"**
- Drafts and data stay in .spokeslad/ in your repo. Like any Claude Code use, the
  repo content Claude reads goes to Anthropic. Listening sends your product,
  competitor names and keywords to HN, GitHub (and Reddit if enabled) as search terms.
