---
name: pitch
description: Find the creators, newsletter writers, podcasters and analysts who actually cover this space and whose audience matches, verify each with a recent relevant piece, and draft a short personal pitch for each. The modern replacement for a journalist list. Drafts only; the user sends. Use for tier 1 or 2 launches or when the user wants coverage.
argument-hint: "[launch folder]"
---

# Pitch: earned coverage from the people the audience trusts

Third-party voices are what make people believe a launch. Today they are mostly
newsletter writers, YouTubers, podcasters, community leaders and a few journalists.
Requires messaging.md and, ideally, a launch plan with an angle.

## 1. Build the list

Search the web for people who covered this category or close alternatives in the last
6 months: newsletters, YouTube channels, podcasts, blogs, active community members,
and journalists on the beat. Start from where the audience is (messaging.md) and from
who covered competitors.

Keep someone only if you can link a specific recent piece that shows their audience
would care. No piece, no pitch.

Save `.spokeslad/launches/<folder>/pitch-list.md` as a table: name, outlet, audience
fit (one line), evidence link (their recent relevant piece), public contact route
(the one they publish: a form, a tips email, DMs open), fit score 1 to 5, status.

Never guess or scrape private email addresses. Use only contact routes the person
publishes for this purpose.

## 2. Draft each pitch

Save drafts in `.spokeslad/launches/<folder>/pitches.md`, one per person, separated
by a line containing only `---`. Each pitch:

- Under 150 words. Subject line under 60 characters.
- Opens with why them: a specific reference to their piece, in one sentence.
- One sentence on what it is, one on why their audience would care now.
- One concrete offer (early access or an exclusive only if access is genuinely limited): a demo, a first look, the maker for an
  interview, data they can use.
- One clear, easy ask, and an easy no.
- No attachments, no hype, no "hope you're well", no pretend familiarity.

Order the list by fit score. A good list is 5 to 15 people, not 200.

## 3. Rules

- The user sends every pitch personally. Never send, never automate sending.
- One polite follow-up after 5 to 7 days at most, then stop.
- Respect embargoes both ways. If you offer an exclusive, offer it to one person.
- If someone covers it, thank them and log it in `.spokeslad/log.md` with the link.

Run `"${CLAUDE_PLUGIN_ROOT}/bin/spokeslad" lint` on pitches.md before showing the user.
