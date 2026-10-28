Show HN: Spokeslad – Launch prep for Claude Code that never posts for you

https://github.com/EboMutele/spokeslad

Hi HN. I'm bad at telling people about things I build, and AI-written launch posts
seem to have made that whole genre worse. So I tried to package what good launches
have in common, as a Claude Code plugin.

You brief it once: who the product is for, what you want people to repeat, what you
can prove, what you must never say. Then it listens on HN, Reddit and GitHub, sizes
news into tiers (most updates shouldn't be launches), drafts the posts, and checks
them twice before you see them: a small Python linter (fails hype words, numbers with
no source, Show HN titles over 80 characters, Reddit posts that don't disclose you made
the thing), and a separate reviewer agent that only sees the drafts and your proof,
and writes the first critical reply each channel would post.

It never posts, sends or votes. You publish yourself.

Its first test was this launch. The brief, competitor scan, plan, drafts and red-team
report are in the repo under .spokeslad/. The scan found other PR plugins already
exist (Newsjack is the big one, more journalist-focused), so this is not a first.

Rough edges: it's v0.1 with no users yet, Reddit's public endpoint rate-limits, and
sentiment is a keyword heuristic. I'd love feedback on whether the review step catches
what you'd catch, and on the name, since "PR" means pull request to most of us.
