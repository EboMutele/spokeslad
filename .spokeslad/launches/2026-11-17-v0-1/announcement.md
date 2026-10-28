# Spokeslad 0.1: launch and comms prep for people who'd rather be coding

I build things, and like most developers I'm bad at telling anyone about them. The
launches I've seen go well weren't louder. They were prepared: clear about who the
thing is for, honest about what it can do, present in the right threads, and ready
when something broke.

Spokeslad is my attempt to package that preparation as a Claude Code plugin. It's free
and MIT licensed.

## What it does

You run `/spokeslad:brief` once. It reads your repo and site, asks a few questions,
and writes a messaging file: who the product is for, three things you want people to
repeat, the proof behind each, claims you're allowed to make, and things you must
never say. Every other command checks against that file.

- `/spokeslad:listen` collects new mentions of you, your competitors and your category
  from Hacker News, Reddit, GitHub and release feeds, and writes a one-screen digest:
  what changed, why it matters, what to do.
- `/spokeslad:plan` scores your news into tiers 1 to 4, so a bug fix doesn't get a
  launch and a launch doesn't get a tweet.
- `/spokeslad:launch` drafts the kit: announcement, changelog, Show HN post, thread,
  Reddit post, FAQ, a tough-questions sheet, a demo script and holding statements.
- `/spokeslad:pitch` finds newsletter writers and creators who covered your space
  recently, and drafts a short personal note to each.
- `/spokeslad:crisis` triages an outage or a backlash thread and drafts a holding
  statement and a response plan.
- `/spokeslad:measure` tracks share of voice, which of your messages people repeat,
  and how often Claude, and a web search, name you for questions a buyer would ask.

## The part I care about most

Every draft gets checked twice before you see it. First by `spokeslad lint`, a small
script that fails drafts with hype ("revolutionary", "the only"), unsourced
percentages, money and user counts, phrases on your never-say list, leftover placeholders, Show HN titles that
break the format, X posts over the limit, and Reddit posts that don't say you made the
thing. Then by a separate reviewer agent that never sees the conversation that wrote the draft. It
checks each claim against your proof and writes the first critical reply the toughest
reader in each channel would post.

And it never posts on your behalf. No auto-posting, no alternate accounts, no upvote
schemes. You publish under your own name.

## Proof: it launched itself

Spokeslad's first test was preparing this launch. Everything is in the repo under
`.spokeslad/`: the messaging file, the competitor scan (which found that other public-relations
plugins exist, so you won't see "first" or "only" here), the tier score (tier 2, with
what it would take to earn tier 1), these drafts, and the red-team report with what it
changed. It caught real problems, including claims about the linter that the code
didn't back up at the time.

## Honest limits

- It's version 0.1 and has no users yet besides me.
- Listening uses public endpoints that rate-limit. It waits between requests, and
  Reddit is off unless you turn it on (web search covers it otherwise).
- Sentiment tagging is a keyword heuristic for triage. Claude reads the actual posts.
- In developer search, "PR" means pull request. I know.

## Try it

```
/plugin marketplace add EboMutele/spokeslad
/plugin install spokeslad@spokeslad
```

Then open Claude Code in your project and run `/spokeslad:brief`. Feedback, issues and
blunt opinions are welcome on GitHub.
