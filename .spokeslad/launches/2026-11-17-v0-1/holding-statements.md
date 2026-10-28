# Holding statements for launch day

**Install fails for some people**

> Thanks for reporting this. Some installs are failing at [step]. I'm looking at it
> now. In the meantime you can clone the repo and run `claude --plugin-dir ./spokeslad`.
> I'll update this thread when the fix is out.

Fill in the step from the actual error before posting.

**Listening returns nothing or errors (rate limits)**

> Yes, the public Reddit and HN endpoints rate-limit. Spokeslad keeps going with the
> other sources and lists what failed. Setting GITHUB_TOKEN helps for GitHub. I'm
> adding backoff in the next release.

**A critical thread: "AI marketing spam"**

> That's a fair concern and it's the thing I was trying to avoid. It never posts, and
> drafts with hype or unsourced numbers fail a linter before you see them. The rules
> are here: [link to scripts/spokeslad.py lint section]. If you think they miss
> something, I'd like to hear what.

Replace the bracketed link before posting. Reply once; don't argue past that.
