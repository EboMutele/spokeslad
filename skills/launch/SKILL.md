---
name: launch
description: Produce the full launch kit for an announcement from its plan, all on-message with the messaging house - announcement post, changelog, Show HN, X thread, LinkedIn, Reddit, user email, FAQ and tough questions, demo script and holding statements - then lint and red-team it for the user's approval. Never publishes. Use after /spokeslad:plan or when the user says they are shipping something.
argument-hint: "<launch folder or what is shipping>"
---

# Launch: the kit, written once, consistent everywhere

Requires `.spokeslad/messaging.md` and a plan. If there is no plan for this
announcement, run `/spokeslad:plan` first. Work in the plan's folder,
`.spokeslad/launches/<yyyy-mm-dd>-<slug>/`.

## 1. Load context

Read messaging.md, plan.md, the latest digest, and the actual thing being shipped
(diff, docs, demo). Every claim in every asset must trace back to an approved claim,
a proof point, or something you verified in the product itself.

## 2. Write the core story first

`story.md`: the one-paragraph version of the news. Problem, what changed, who it is
for, proof, how to try it. Every other asset adapts this; none invents new claims.

## 3. Write only the assets the plan calls for

Use these file names so the linter applies the right platform rules:

- `announcement.md`: the canonical post. Lead with the problem and the result, not
  the company. Include install or try-it steps that you have actually checked.
- `changelog.md`: plain, factual, versioned.
- `show-hn.md`: first line is the title, starting `Show HN:`, under 80 characters,
  no hype. The body is a short, personal note from the maker: what it is, why you
  built it, what is rough, what feedback you want. HN readers respect candor about
  limitations. HN reportedly asks that comments not be AI-generated or AI-edited
  (reported March 2026; check the current guidelines): label HN drafts as notes the
  user rewrites in their own words, and never draft HN comment replies as paste-ready text.
- `x-thread.md`: posts separated by lines containing only `---`, each under 280
  characters. First post stands on its own; the link goes in the first or last post.
- `linkedin.md`: under 3000 characters, first two lines carry the point.
- `reddit-<subreddit>.md`: one per community. Read that subreddit's rules and recent
  top posts first and follow them. Say you made it in the first lines. Lead with what
  is useful to that community. If self-promotion is not allowed there, do not write it.
- `email-users.md`: to existing users, short, what changes for them.
- `faq.md`: real questions people will ask, plus `tough-questions.md`: the hardest
  questions a skeptic, competitor or journalist would ask, with honest answers.
- `demo-script.md`: a 60 to 90 second demo, shot by shot, showing the real product.
- `holding-statements.md`: short prepared responses for the 3 most likely things to
  go wrong on launch day (install broken, site down, a sharp critical thread).

For creator and newsletter outreach, run `/spokeslad:pitch` for this launch.

## 4. Quality bar

- Specific beats impressive. Numbers only with a source.
- Write like the spokesperson in messaging.md talks, not like a press release.
- No hype words, no "excited to announce", no fake urgency.
- Never write fake testimonials, invented users, or posts meant to look like they
  come from someone other than the user.

## 5. Check before showing

1. Run `"${CLAUDE_PLUGIN_ROOT}/bin/spokeslad" lint .spokeslad/launches/<folder>` and
   fix every error.
2. Run `/spokeslad:redteam` on the folder. Fix all blocking findings.
3. Write `checklist.md`: each asset, where it goes, when (from the plan), status
   (draft, approved, published) and a box for the user's approval.

## 6. Hand over

Tell the user what is ready, the order to publish in, and anything still open. The
user publishes, under their own name. When they confirm something went out, record it
in `.spokeslad/log.md` with the URL, and suggest `/spokeslad:measure` at T+7.
