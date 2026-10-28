# Tough questions

**"This is an AI slop generator for marketing. Why would HN want more of that?"**
Fair worry. The point of the tool is to stop that: drafts that contain hype or
numbers without a source fail a linter, and a separate reviewer reads them like a
cynical commenter before I ever see them. The rules are in the repo; tell me what
they miss.

**"How is this different from Newsjack?"**
Newsjack is good and more established. It focuses on journalists and news cycles:
spotting stories to comment on and pitching reporters. Spokeslad focuses on developer
channels (HN, Reddit, GitHub), launch sizing, and checking drafts before you publish.
Some people will want both.

**"Did you use Spokeslad to write this post?"**
Yes. It drafted it from the messaging file, the linter and reviewer checked it, and I
edited and approved it. The red-team report for this launch is in the repo.

**"Where are the users? Any evidence it works?"**
None yet beyond its own launch. It's v0.1. I'll publish what happens with this launch,
numbers included, at T+7 and T+30.

**"'Spokeslad' is a weird name. And 'PR' means pull request."**
Both true. I avoid "PR" on its own for exactly that reason. The name was the one nobody
else had.

**"Can't I just prompt Claude to write a launch post?"**
You can, and for a small update you should. Spokeslad adds what a single prompt
doesn't: one source of truth across every asset, daily listening, tiering, a check by
code, an independent review, and measurement over time.

**"Does it scrape Reddit or break platform terms?"**
It reads public search endpoints at a low rate and never posts, votes or sends.

**"Why should I trust a tool that does comms to be honest?"**
Don't trust it; check it. Every claim must trace to a proof link in your messaging
file, and the reviewer opens those links.
