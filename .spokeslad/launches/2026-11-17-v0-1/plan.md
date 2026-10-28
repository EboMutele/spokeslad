# Launch plan: Spokeslad v0.1

**The news in one sentence:** Spokeslad, a free Claude Code plugin that runs the
launch and public-relations workflow for developers, is out, and its first job was
preparing its own launch.

## Score

| Factor | Score | Why |
|---|---|---|
| Novelty | 1 | Other PR plugins exist (Newsjack, Claude-PR-Media-Work-Plugin). Our angle is new; the category is not. |
| Audience impact | 2 | Every builder launching something has this problem, but they can live without it. |
| Proof strength | 2 | Working code with tests and a real self-launch as a demo; no outside users yet. |
| Story | 3 | "A launch tool that launched itself", with all its own launch files public in the repo. |
| Timing | 2 | No known clash; plugin directories are active. Re-check the week before. |
| **Total** | **10** | **Tier 2** |

**How to earn tier 1:** a 60 to 90 second demo video, and two or three outside
developers who used it on their own launch and will say so publicly in their own words.
If both land before T-3, upgrade to tier 1 and add LinkedIn and more pitches.

## Angle

Most developer launches fail quietly, and AI launch copy makes it worse: it reads as
hype and gets punished on HN and Reddit. Spokeslad does the opposite of a hype
machine: it checks every draft against what you can prove, reviews it with a separate
agent, and never posts for you. Proof: this launch's own files are in the repo,
including the red-team report.

## Date

**Tuesday 2026-11-17**, US morning. Avoids US Thanksgiving week (from 2026-11-23).

## Assets (tier 2)

| Asset | File | Owner | Status |
|---|---|---|---|
| Core story | story.md | Spokeslad | draft |
| Announcement (README "Launch notes" and a GitHub release) | announcement.md | Spokeslad, you approve | draft |
| Changelog | changelog.md | Spokeslad | draft |
| Show HN | show-hn.md | you post | draft |
| X / Bluesky thread | x-thread.md | you post | draft |
| r/ClaudeAI showcase megathread comment | reddit-ClaudeAI.md | you post | draft |
| Creator and newsletter pitches (6 to 8) | pitch-list.md, pitches.md | you send | draft |
| Directory submissions (claudemarketplaces.com/submit and similar) | checklist.md | you | to do |
| FAQ and tough questions | faq.md, tough-questions.md | Spokeslad | draft |
| Demo script | demo-script.md | you record | draft |
| Holding statements | holding-statements.md | Spokeslad | draft |
| LinkedIn | none | | skipped at tier 2 |

## Timeline

| When | Date | Step |
|---|---|---|
| T-20 | Wed 2026-10-28 | Brief, baseline, drafts, red team (done in the build session) |
| T-14 | Tue 2026-11-03 | You review drafts. Ask 3 developers to try it on a real project. Pitches out with early access. |
| T-7 | Tue 2026-11-10 | Record demo. Fold early-user feedback into README and drafts. Re-run red team. |
| T-5 | Thu 2026-11-12 | Final approval of all drafts. Submit to plugin directories. |
| T-1 | Mon 2026-11-16 | Fresh-machine install test. Check every link. Re-run `/spokeslad:listen` for clashes. |
| T | Tue 2026-11-17 | Show HN first, then thread, then Reddit megathread. Stay in the HN thread for 3+ hours. |
| T+1 to T+7 | | Answer everything. Fix what people report, fast and publicly. Log coverage. |
| T+7 | Tue 2026-11-24 | `/spokeslad:measure` against targets. |
| T+30 | Thu 2026-12-17 | Measure again, including the AI-answer probe. |

## Targets

The baseline is zero (unreleased), so the first three are starting guesses to
recalibrate after T+7, not forecasts.

1. Every HN comment answered within the first 3 hours: 100%.
2. 10 or more earned mentions (by others, not us) within 14 days.
3. 3 or more creator or newsletter mentions from 6 to 8 pitches.
4. 25 or more GitHub stars from people we don't know by T+14 (guess).
5. Spokeslad named in at least 1 of the 6 buyer questions by T+30 (baseline 0 of 6).

## Risks

- **"Another AI marketing tool" backlash on HN.** Mitigation: candid Show HN text,
  the red-team report in the repo, tough-questions sheet ready.
- **Comparison with Newsjack.** Answer factually and generously; never knock them.
- **Install breaks on launch day.** Mitigation: fresh-machine test at T-1, holding
  statement ready.
- **Reddit removal.** Use the showcase megathread unless you have 50+ karma; read
  Rule 7 first.
- **The name.** "Lad" may read as bro-ish to some; the voice stays dry and
  professional.

## Open questions

- Your karma on r/ClaudeAI and your HN account age (affects Reddit route and HN
  visibility).
- Will you record the demo yourself?
- Any users you can ask to try it before launch?
