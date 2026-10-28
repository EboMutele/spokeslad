---
name: plan
description: Turn a piece of news (a launch, feature, release, milestone, funding, partnership) into a sized communications plan. Scores the news into tiers 1 to 4, picks channels and assets to match, sets a timeline and measurable targets from the current baseline. Use before /spokeslad:launch, or when the user asks how big to make an announcement.
argument-hint: "<what is being announced>"
---

# Plan: size the news, then plan to match

The most common PR mistake is treating every update like a launch. Big teams tier
their news so effort and audience attention go where they pay off.

Requires `.spokeslad/messaging.md`. Read it, the latest digest in
`.spokeslad/digests/`, and `.spokeslad/metrics.csv` if it exists.

## 1. Get the facts

Ask for (or read from the repo, PR, changelog) exactly what ships, when, for whom,
what it replaces, and what proof exists: demo, numbers, user quotes. Unknowns go in
an "Open questions" list. Do not plan around facts you do not have.

## 2. Score and tier

Score 0 to 3 on each, then add them up:

| Factor | 0 | 3 |
|---|---|---|
| Novelty | Incremental fix | New category or first of its kind (provable) |
| Audience impact | Few users notice | Changes daily work for most of the audience |
| Proof strength | Claims only | Live demo, numbers, outside users vouching |
| Story | Feature list | Clear before/after, a real problem, a person |
| Timing | Crowded week, competitor launching | Open week, relevant conversation underway |

- **Tier 1 (12 to 15)**: a launch. Full campaign. A few times a year at most.
- **Tier 2 (8 to 11)**: notable release. Owned channels plus one or two community posts.
- **Tier 3 (4 to 7)**: changelog-worthy. Changelog, short post, reply where relevant.
- **Tier 4 (0 to 3)**: no announcement. Ship it quietly, mention it in the next roundup.

If the user wants a bigger tier than the score supports, say so plainly and suggest
what would earn it (a demo, a user story, waiting for a quieter week).

## 3. Channels and assets by tier

| Asset | T1 | T2 | T3 |
|---|---|---|---|
| Announcement post (blog or README section) | yes | yes | short |
| Changelog entry | yes | yes | yes |
| Show HN | yes | if new to HN | no |
| X/Bluesky thread | yes | yes | single post |
| LinkedIn post | yes | optional | no |
| Reddit (only subs where it fits the rules) | 1 to 2 | 0 to 1 | no |
| Creator and newsletter pitches | 5 to 15 | 3 to 5 | no |
| Email to existing users | yes | yes | in roundup |
| Demo video or GIF script | yes | optional | no |
| FAQ and tough-questions sheet | yes | short | no |

Check each community's current self-promotion rules before planning a post there.

## 4. Timeline

For tier 1 and 2, lay out dated steps relative to launch day (T):

- T-14 to T-7: brief, pitch list, pitches out (offer an embargo or early access only if the product is not yet public).
- T-5: drafts done, red-team pass, user approves.
- T-1: final check of links, demo, install path; holding statements ready.
- T: publish in a planned order, be present in comments for the first hours.
- T+1 to T+7: answer everything, thank people, collect proof and quotes.
- T+7 and T+30: measure against targets.

Avoid launching into a known crowded day (check the digest for competitor launches
and big industry events).

## 5. Targets

Set 3 to 5 targets from the baseline in metrics.csv, not from hope. For example:
share of voice over 14 days, product mentions, GitHub stars gained, sign-ups or
installs if the user can see them, creator posts published, AI mention rate at T+30.
If there is no baseline, say so and run `/spokeslad:measure` first.

## 6. Output

Write `.spokeslad/launches/<yyyy-mm-dd>-<slug>/plan.md` with: the news in one
sentence, score table, tier, the angle (why anyone should care now), assets list
with owners, timeline, targets, risks and open questions. Show the user the tier,
angle and timeline, and offer to run `/spokeslad:launch` next.
