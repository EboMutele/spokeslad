---
name: crisis
description: Crisis communications for a software product - outages, security or data incidents, bad releases, backlash threads, accusations. Triages severity, separates known facts from unknowns, drafts a holding statement within minutes and a response plan with update cadence, all for the user's approval. Use the moment something is going wrong publicly, or when /spokeslad:listen escalates.
argument-hint: "<what is happening, links>"
---

# Crisis: fast, factual, human

In a crisis the first public response sets the story. The aim is to be first with
the truth, not first with a guess. Speed matters, but a wrong statement costs more
than a late one.

## 1. Facts in 5 minutes

Gather from the user, the links and the product (status, issues, logs they share):

- **Known**: what is confirmed, since when, who is affected.
- **Unknown**: cause, scope, data impact, time to fix.
- **Being done**: who is working on it, what has been tried.

Never fill an unknown with a likely guess. "We're investigating" is a fact.

## 2. Severity

- **S1**: security or data exposure; data loss; legal or safety risk; product down
  for most users. Respond publicly within 1 hour; updates at least every 2 hours.
- **S2**: a major feature broken for many users; a fast-growing critical thread;
  a credible accusation (licensing, dishonesty, astroturfing). Respond within a few
  hours; update when facts change, at least daily.
- **S3**: a minor bug with complaints; one critical post with little traction.
  Reply where it is being discussed; no general statement.

For S1 involving security or personal data, tell the user that legal and disclosure
obligations may apply and they should involve whoever handles that before making
technical statements. Spokeslad drafts communications, not legal advice.

## 3. Holding statement

Draft `holding-statement.md` in `.spokeslad/crisis/<yyyy-mm-dd>-<slug>/`. Under 100
words, in this order:

1. Acknowledge plainly what is happening, in the users' terms.
2. What we know, only confirmed facts.
3. What we are doing right now.
4. What users should do, if anything (a workaround, a password reset, nothing).
5. When the next update will come and where.

No blame on users, vendors or "a small number of users" minimising. No "we take X
very seriously". Apologise if we caused harm, once, without hedging.

## 4. Response plan

Write `plan.md` in the same folder: where to post (status page, GitHub issue or
discussion pinned, the threads where it is being discussed, X, email to affected
users for S1), who says it (the spokesperson), the update schedule, prepared answers
to the 5 most likely questions, and what not to do: do not delete criticism, do not
argue in threads, do not post from other accounts, do not promise a date you do not
control.

## 5. Check and hand over

Run `"${CLAUDE_PLUGIN_ROOT}/bin/spokeslad" lint` on the folder. For S1 and S2, also
run `/spokeslad:redteam`, but do not let review delay a holding statement past the
response window; if time is short, tell the user what was not checked.

The user approves and posts. Log every public statement with its time and URL in
`.spokeslad/log.md`.

## 6. Afterwards

Once resolved: a final update saying it is fixed, what happened, and what changes so
it does not recur. For S1 and S2, draft a short public postmortem within a week, and
add lessons and new holding statements to messaging.md.
