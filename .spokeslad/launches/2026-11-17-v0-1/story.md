Most developer projects don't fail because they're bad. They fail because nobody hears
about them, and the people who built them would rather write code than "do
marketing". AI made this worse: launch copy is now cheap, sounds the same, and gets
punished on Hacker News and Reddit.

Spokeslad is a free, open-source Claude Code plugin that runs the launch and
public-relations workflow big companies use, for developers with no comms team. You
brief it once on what your product is, who it's for and what you can prove. It
watches Hacker News, Reddit and GitHub, sizes your news and plans the launch,
drafts every asset from one messaging source, then checks each draft twice: with a
linter that fails hype and unsourced percentages, money and user counts, and with a
separate reviewer agent, which never sees the conversation that wrote the draft, reading
it like your harshest critic. It never posts on your behalf. You approve and
publish everything yourself.

Its first job was preparing its own launch. The brief, the competitor scan, the plan,
these drafts and the red-team report (with what it changed) are all in the repo.

Install: `/plugin marketplace add EboMutele/spokeslad`, then
`/plugin install spokeslad@spokeslad`.
