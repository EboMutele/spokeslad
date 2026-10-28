# Holding statements for launch day

Notes to adapt in your own words. Fill in specifics from the real error before posting.

**Install fails for some people**

> Thanks for reporting this. Some installs are failing and I'm looking at it now. In
> the meantime this works: `git clone https://github.com/EboMutele/spokeslad` and then
> `claude --plugin-dir ./spokeslad`. I'll update this thread when it's fixed.

**Listening returns nothing or errors**

> The public endpoints rate-limit. Spokeslad waits between requests, retries once,
> keeps going with the other sources and lists what failed. Setting GITHUB_TOKEN helps
> for GitHub.

**A critical thread: "AI marketing spam"**

> That's a fair concern and it's what I was trying to avoid. It never posts, and drafts
> with hype or unsourced claims fail a linter before you see them. The rules are here:
> https://github.com/EboMutele/spokeslad/blob/main/scripts/spokeslad.py
> If they miss something, I'd like to hear what.

Reply once; don't argue past that.
