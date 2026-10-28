---
name: brief
description: Set up Spokeslad for a product. Reads the repo and site, interviews the user, and writes the messaging house (.spokeslad/messaging.md) and config (.spokeslad/config.json) that every other Spokeslad skill checks against. Use first, and again whenever positioning, audience or claims change.
argument-hint: "[product repo path or URL]"
---

# Brief: build the messaging house

Good PR teams do not start with content. They start with one agreed list of what we
say, to whom, and what we can prove. Everything else in Spokeslad reads this file.

## 1. Create the workspace

Run `"${CLAUDE_PLUGIN_ROOT}/bin/spokeslad" init` from the project root. It creates
`.spokeslad/` with `config.json`, `messaging.md`, `log.md` and working folders, and
never overwrites existing files. If a brief already exists, read it and update it
instead of starting over.

Suggest adding `.spokeslad/signals/` to `.gitignore` (raw data, can be large).

Then check whether the repo is public (for GitHub: `gh repo view --json visibility`).
If it is public, tell the user plainly that anything committed under `.spokeslad/`
is readable by anyone, including competitors and the people it mentions, and keep
these out of it: `digests/`, `crisis/`, `log.md`, `pitch-list.md` and `pitches.md`
(until sent), and any notes about named people. Offer two options: add those paths to
`.gitignore`, or keep the whole workspace in a separate private repo. Messaging,
plans, published drafts and red-team reports can stay public if the user wants them
as evidence.

## 2. Do the homework before asking anything

Read, in this order, whatever exists: README, docs, CHANGELOG or releases, package
manifest, landing page (WebFetch), recent issues and discussions, and any existing
launch posts. Then search the web for:

- what people already say about the product (and the founder);
- the 3 to 5 alternatives a buyer would actually compare it with, including
  "do nothing" or "build it yourself";
- the words the audience uses for the problem (forum threads, issues, reviews).

Write down what you found with links. Never invent users, quotes or numbers.

## 3. Interview the user, briefly

Ask only what the homework could not answer. At most 6 questions, in one message,
each with your best guess so the user can just confirm:

1. Who is it for first, and who is it deliberately not for?
2. What is the one thing you want people to repeat about it?
3. Which alternatives do you lose to, and why?
4. What can you prove today (numbers, users, benchmarks, demos)?
5. What must we never say (legal, partners, roadmap, competitors)?
6. Who speaks publicly for the product, and in what voice?

## 4. Write the messaging house

Fill `.spokeslad/messaging.md` from the template. Rules:

- Three pillars at most. Each needs at least one proof point with a link. A pillar
  without proof moves to "Do not claim (yet)".
- Approved claims are exact phrasings that are true today. Prefer specific and
  modest ("installs in one command") over big and vague ("the best way to").
- Objections get honest answers, including "you're right, it doesn't do that yet".
- Boilerplate at 25, 50 and 100 words.

## 5. Write the config

Fill `.spokeslad/config.json`:

- `product`: name, aliases (common misspellings too), repo, website, one_liner.
- `competitors`: the alternatives from step 2, with repos and changelog or blog
  feeds where they exist (RSS/Atom URLs).
- `keywords`: 3 to 8 category phrases people search for, not slogans.
- `subreddits`: only communities where the audience really is.
- `key_messages`: one per pillar, with keywords that would show up if someone
  repeated the message in their own words (used to measure pull-through).
- `approved_claims`: mirror the table in messaging.md.
- `never_say`: phrases from question 5 plus anything risky you found.
- `ai_probe.questions`: 5 to 10 questions a buyer would ask an AI assistant when
  looking for this kind of tool. Phrase them as a buyer, never name the product.

## 6. Confirm and log

Show the user the positioning statement, pillars and approved claims (not the whole
file) and ask for corrections. Then append a dated line to `.spokeslad/log.md`.
Finish by suggesting `/spokeslad:listen` for a first baseline.
