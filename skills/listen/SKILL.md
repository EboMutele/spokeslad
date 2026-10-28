---
name: listen
description: Daily media monitoring for a product. Collects new mentions of the product, competitors and category from Hacker News, Reddit, GitHub, release feeds and the web, then writes a short digest of what changed, why it matters and what to do. Use daily, before a launch, or when the user asks what people are saying.
argument-hint: "[days to look back, default 2]"
---

# Listen: what changed, why it matters, what to do

Requires `.spokeslad/config.json`. If it is missing, run `/spokeslad:brief` first.

## 1. Collect

Run `"${CLAUDE_PLUGIN_ROOT}/bin/spokeslad" listen --days N` from the project root,
where N is the number of days the user asked for (default 2). It queries HN, Reddit, GitHub issues and competitor releases and feeds,
removes anything already seen, tags each signal (mention, competitor,
competitor-release, category) with a rough sentiment, and saves
`.spokeslad/signals/YYYY-MM-DD.json`.

If sources fail (network limits, rate limits), say which ones, then cover the gap
with WebSearch for the product name, each competitor and each keyword over the last
few days. Also search what the tool cannot reach: X, LinkedIn, newsletters, YouTube
and podcasts. Add anything you find to your notes with links.

## 2. Read, don't skim

The sentiment tag is a keyword heuristic for triage only. Open and read every
mention of the product and every high-engagement item. For each one decide:

- **Respond**: a question we can answer, a misconception, a bug report, a thank-you
  worth acknowledging.
- **Learn**: a pain point, objection or phrase the audience uses. Note it for the
  messaging house.
- **Watch**: competitor moves, category shifts.
- **Escalate**: anything that meets the crisis triggers below.

## 3. Escalate when it's a crisis

Stop and run `/spokeslad:crisis` if any of these appear: a security or data issue;
an outage or data loss affecting users; an accusation of dishonesty, license or
trademark violation, or astroturfing; a thread critical of us gaining traction
quickly; legal or regulatory mention. Tell the user right away.

## 4. Write the digest

Save `.spokeslad/digests/YYYY-MM-DD.md` and show it to the user. Keep it to one
screen:

1. **What changed** since the last digest (counts and the 3 to 5 items that matter).
2. **Why it matters**, in one line each.
3. **What to do**: at most 5 actions, most important first. For replies, draft the
   reply below the action. Drafted replies must say plainly that we made the product,
   answer the actual question, and never argue or pile on.
4. **Messaging notes**: phrases, objections or proof worth adding to messaging.md.

## Rules

- Never reply, post or vote on the user's behalf. Draft only.
- Never create or suggest alternate accounts, and never ask friends to upvote.
- Quote at most a short phrase from any source; link the rest.

## Running it every day

Suggest a daily scheduled task that runs `/spokeslad:listen` in this project, or
`claude -p "/spokeslad:listen"` from cron. Run `/spokeslad:measure` weekly.
