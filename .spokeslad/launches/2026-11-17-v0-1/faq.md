# FAQ

**What is Spokeslad?**
A free, open-source Claude Code plugin that runs the launch and public-relations
workflow for software products: messaging, listening, launch planning, drafting,
review and measurement. You publish everything yourself.

**Does it post for me?**
No. It never posts on your behalf, sends messages, replies or votes. That is a design
decision, not a missing feature.

**What do I need?**
Claude Code and Python 3.9 or newer. The helper script uses the standard library only.
`GITHUB_TOKEN` (higher GitHub rate limits) and `ANTHROPIC_API_KEY` (AI-answer probe)
are optional.

**Where does my data go?**
Everything Spokeslad writes stays in a `.spokeslad/` folder in your project. Listening
calls public Hacker News, Reddit and GitHub endpoints. The optional AI probe sends your
buyer questions to the Anthropic API.

**Which channels does it cover?**
It listens on Hacker News, Reddit, GitHub issues and releases, and any RSS or Atom
feed. It drafts for your blog or README, changelog, Show HN, X or Bluesky, LinkedIn,
Reddit, email and creator pitches.

**What does "red team" mean here?**
A separate reviewer agent that only sees your drafts and your messaging file, not the
conversation that wrote them. It checks every claim against your proof and writes the
first critical reply each channel would post.

**What is AI-answer visibility?**
How often AI assistants mention your product when asked questions a buyer would ask,
and in what position. Spokeslad stores the questions so you can track the same ones
over time.

**Is it only for Claude Code plugins?**
No. Any software product works: open-source tools, developer tools, SaaS. It is
strongest where your audience talks on HN, Reddit and GitHub.

**How is it licensed?**
MIT.
