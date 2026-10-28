# Red-team report: Spokeslad v0.1 launch drafts

Reviewer: the `redteam` agent, run 2026-10-28 with only the draft paths, messaging.md,
plan.md and the repo; it did not see the drafting conversation. Inputs: 12 drafts.
Before review, `spokeslad lint` passed all 12 and the 21 tests passed.

**Verdict: Ready after blocking fixes.** All six blocking findings were fixed the same
day. Responses are below each finding.

## Blocking

1. **The red-team report the drafts promise was not in the repo.** Seven drafts said
   it was. *Response:* this file. Committed with the drafts.

2. **"Fails numbers with no source" was false.** Only percentages and multipliers were
   errors; "10,000 developers" was a warning (exit 0) and "$5M", "Fortune 500 teams"
   and "3 weeks to 2 days" passed silently. *Response:* fixed in code and in wording.
   The linter now fails unsourced percentages, multipliers, money, user counts and
   "Fortune N" claims, and warns on time claims. New tests cover each case. Drafts,
   README and messaging now describe exactly that.

3. **A pitch misquoted its recipient** (AI Blew My Mind: the piece says the hard part
   comes before selling). *Response:* pitch dropped.

4. **Pitches offered "early access" to a repo that is already public.** *Response:*
   replaced with an offer of a walkthrough, stating the repo is public. "Early access
   or exclusives" added to do-not-claim.

5. **HN reportedly bans AI-generated or AI-edited comments** (reported March 2026,
   secondary source; the guidelines page was unreachable from the review sandbox).
   Paste-ready replies would break it. *Response:* tough-questions.md and
   holding-statements.md are now talking points to answer in your own words; the Show
   HN draft carries a note to rewrite it; the launch skill now says the same for every
   future launch. Confirm the rule on the guidelines page before launch.

6. **"Reads public endpoints at a low rate" was unsupported** (no delay, no backoff,
   unauthenticated Reddit). *Response:* `listen` now waits 1 second between requests
   (`--delay`), retries once on HTTP 429 using Retry-After, and Reddit is off by default
   (web search covers it). The answer now states exactly that. Tests added.

## Non-blocking (applied)

- Bracketed placeholders like "[step]" passed the linter: added a generic placeholder
  rule that skips markdown links, checkboxes, footnotes and [source: ...]; filled in the
  holding statements.
- Removed the "adding backoff in the next release" promise (backoff now exists).
- Install workaround now includes the clone step.
- "Only sees the drafts and your proof" overstated isolation: now "never sees the
  conversation that wrote them"; the skill notes isolation is an instruction.
- AI visibility described precisely: Claude (optional, with an API key) or a web search.
  The 2026-10-28 baseline is now committed (ai-answers/ no longer gitignored).
- FAQ: data-flow sentence added; macOS/Linux (WSL on Windows); "designed for any
  software product".
- Promise to publish numbers in a week and a month added to the plan.
- Show HN title: "Show HN: Spokeslad – A Claude Code plugin for launch prep that never
  posts" (72 characters); "PR plugins" changed to "public-relations plugins".
- README, plugin.json and marketplace tagline changed from "Your product's PR team" to
  the 25-word boilerplate; announcement title now says "launch and comms prep".
- Pitch list: dropped AI Engineer Guide (Jan 2026, outside 6 months), HelloConvo
  (misread, no contact route), Flint (co-hosted by a competitor's author); cut a line
  in Ryan Doser's pitch that insulted his readers; added Developers Digest
  (developer-first, plugin posts in October 2026). The list is now short of the plan's
  6 to 8: that gap is recorded in plan.md and pitch-list.md.
- Demo script no longer scripts results in advance.
- Reddit draft now says how it was built (with Claude Code). Rule 7 text still unread.

## The first critical reply, per channel (before fixes)

- Show HN: "'Fails numbers with no source' means % and 3x only; '$5M' passes clean. And
  the red-team report you say is in the repo isn't there."
- X: "Where's the red-team report? It's not in the repo."
- r/ClaudeAI moderator: "Does this meet Rule 7? And this hits Reddit's search.json
  unauthenticated, in a burst, every day."
- README reader: "'Your product's PR team.' I thought this reviewed pull requests."
- Pitch recipient: "Early access? The repo's already public."

## Still open

- Confirm the HN guideline on AI-written comments and r/ClaudeAI Rule 7 yourself.
- Find 3 to 4 more developer-first outlets with recent relevant pieces.
- Get outside users before claiming any results.
