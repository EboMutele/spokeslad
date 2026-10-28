Show HN: Spokeslad – A Claude Code plugin for launch prep that never posts

https://github.com/EboMutele/spokeslad

Hi HN. I'm bad at telling people about things I build, and AI-written launch posts
seem to have made that whole genre worse. So I tried to package what good launches
have in common, as a Claude Code plugin.

You brief it once: who the product is for, what you want people to repeat, what you
can prove, what you must never say. Then it watches HN, Reddit and GitHub, sizes news
into tiers (most updates shouldn't be launches), drafts the posts, and checks them
twice before you see them. First, a small Python linter fails hype words, unsourced
percentages, money and user counts, Show HN titles over 80 characters, and Reddit
posts that don't say you made the thing. Second, a reviewer agent that never sees the
conversation that wrote the drafts checks them against your proof and writes the first
critical reply each channel would post.

It never posts, sends or votes. You publish yourself.

Its first test was this launch. The brief, competitor scan, plan and the red-team
report are in the repo under .spokeslad/. The red team caught real problems, including
claims about the linter that the code didn't back up; the fixes are in the history.
The scan also found other public-relations plugins already exist (Newsjack is the big
one, more journalist-focused), so this is not a first.

Rough edges: it's v0.1 with no users yet, listening is throttled but still hits public
endpoints, and sentiment is a keyword heuristic. I'd love feedback on whether the
review step catches what you'd catch, and on the name, since "PR" means pull request
to most of us.

<!-- Before posting: HN reportedly asks that comments not be AI-generated or AI-edited
(guideline change reported March 2026; confirm on news.ycombinator.com/newsguidelines.html).
Rewrite this text in your own words; use it as notes, not copy. -->
