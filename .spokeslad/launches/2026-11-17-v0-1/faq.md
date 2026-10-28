# FAQ

**What is Spokeslad?**
A free, open-source Claude Code plugin that runs the launch and public-relations
workflow for software products: messaging, listening, launch planning, drafting,
review and measurement. You publish everything yourself.

**Does it post for me?**
No. It never posts on your behalf, sends messages, replies or votes. That is a design
decision, not a missing feature.

**What do I need?**
Claude Code on macOS or Linux (WSL on Windows) and Python 3.9 or newer. The helper script uses the standard library only.
`GITHUB_TOKEN` (higher GitHub rate limits) and `ANTHROPIC_API_KEY` (AI-answer probe)
are optional.

**Where does my data go?**
Everything Spokeslad writes stays in a `.spokeslad/` folder in your project. Like any
Claude Code use, the repo content Claude reads goes to Anthropic. Listening sends your
product name, competitor names and keywords as search terms to Hacker News and GitHub
(and Reddit if you enable it). The optional AI probe sends your buyer questions to the
Anthropic API.

**Which channels does it cover?**
It listens on Hacker News, GitHub issues and releases, any RSS or Atom feed, and
Reddit if you enable it (otherwise Claude covers Reddit through web search). It drafts for your blog or README, changelog, Show HN, X or Bluesky, LinkedIn,
Reddit, email and creator pitches.

**What does "red team" mean here?**
A separate reviewer agent that gets your drafts, your messaging file and the plan, but
never the conversation that wrote them. It is instructed to check every claim against your proof
and write the first critical reply each channel would post.

**What is AI-answer visibility?**
How often your product is named, and in what position, when a buyer-style question is
asked to Claude (optional, with an API key) or run as a web search. Spokeslad stores the questions so you can track the same ones
over time.

**Is it only for Claude Code plugins?**
No. It's designed for any software product: open-source tools, developer tools, SaaS. It is
strongest where your audience talks on HN, Reddit and GitHub.

**How is it licensed?**
MIT.
