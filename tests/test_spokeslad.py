"""Tests for the Spokeslad CLI. Run with: python3 -m pytest -q"""
import csv
import datetime as dt
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("spokeslad", ROOT / "scripts" / "spokeslad.py")
sl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sl)

NOW = dt.datetime.now(dt.timezone.utc)
RECENT = int((NOW - dt.timedelta(hours=5)).timestamp())
OLD = int((NOW - dt.timedelta(days=30)).timestamp())

CONFIG = {
    "product": {"name": "Spokeslad", "aliases": ["spokes lad"], "repo": "EboMutele/spokeslad"},
    "competitors": [
        {"name": "marketingskills", "repo": "coreyhaines31/marketingskills",
         "feeds": ["https://example.com/feed.xml"]},
        {"name": "claude-gtm-plugin", "repo": "manojbajaj95/claude-gtm-plugin"},
    ],
    "keywords": ["claude code marketing"],
    "subreddits": ["ClaudeAI"],
    "key_messages": [
        {"id": "approval", "message": "You approve everything", "keywords": ["approve", "approval"]},
        {"id": "listen", "message": "It listens daily", "keywords": ["daily digest", "listens"]},
    ],
    "approved_claims": [{"claim": "installs in one command", "proof": "https://x"}],
    "never_say": ["guaranteed virality"],
    "ai_probe": {"questions": ["best PR tool for devs?"]},
}

HN = {"hits": [
    {"objectID": "1", "title": "Show HN: Spokeslad, a PR team in Claude Code", "points": 120,
     "num_comments": 40, "created_at_i": RECENT, "author": "a", "url": "https://github.com/EboMutele/spokeslad"},
    {"objectID": "2", "comment_text": "I tried marketingskills, it is great and useful",
     "story_title": "Ask HN: marketing for devs", "created_at_i": RECENT, "author": "b"},
    {"objectID": "3", "comment_text": "Spokeslad is broken and buggy for me, the install fails",
     "story_title": "Show HN: Spokeslad", "created_at_i": RECENT, "author": "c"},
]}
REDDIT = {"data": {"children": [
    {"data": {"id": "r1", "title": "Spokeslad vs claude-gtm-plugin?", "selftext": "Which one do you approve of?",
              "permalink": "/r/ClaudeAI/comments/r1/", "created_utc": RECENT, "score": 10,
              "num_comments": 5, "subreddit": "ClaudeAI", "author": "d"}},
    {"data": {"id": "r2", "title": "old post about Spokeslad", "selftext": "",
              "permalink": "/r/ClaudeAI/comments/r2/", "created_utc": OLD, "score": 1,
              "num_comments": 0, "subreddit": "ClaudeAI", "author": "e"}},
]}}
GH_ISSUES = {"items": [
    {"id": 99, "title": "Feature: daily digest email", "body": "Spokeslad listens daily, love it",
     "html_url": "https://github.com/EboMutele/spokeslad/issues/1", "user": {"login": "f"},
     "created_at": NOW.isoformat(), "comments": 2},
]}
RELEASES = [
    {"id": 500, "tag_name": "v2.0", "name": "Big release", "body": "New launch skill",
     "html_url": "https://github.com/coreyhaines31/marketingskills/releases/v2.0",
     "published_at": NOW.isoformat(), "author": {"login": "corey"}},
    {"id": 400, "tag_name": "v1.0", "name": "Old", "body": "",
     "html_url": "https://x", "published_at": "2020-01-01T00:00:00Z", "author": {"login": "corey"}},
]
RSS = f"""<?xml version="1.0"?><rss><channel>
<item><title>marketingskills adds pitch skill</title><link>https://example.com/p1</link>
<description>&lt;p&gt;New pitch skill&lt;/p&gt;</description>
<pubDate>{NOW.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate><guid>p1</guid></item>
</channel></rss>"""


def fake_get(url, headers=None, timeout=20):
    if "hn.algolia.com" in url:
        return json.dumps(HN)
    if "reddit.com" in url:
        return json.dumps(REDDIT)
    if "api.github.com/search/issues" in url:
        return json.dumps(GH_ISSUES)
    if "/releases" in url and "coreyhaines31" in url:
        return json.dumps(RELEASES)
    if "/releases" in url:
        return json.dumps([])
    if "api.github.com/repos/" in url:
        return json.dumps({"stargazers_count": 42})
    if "example.com/feed.xml" in url:
        return RSS
    raise AssertionError(f"unexpected URL {url}")


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "HTTP_GET", fake_get)
    assert sl.main(["--dir", str(tmp_path), "init"]) == 0
    (tmp_path / ".spokeslad" / "config.json").write_text(json.dumps(CONFIG))
    return tmp_path


def signals_of(project):
    files = sorted((project / ".spokeslad" / "signals").glob("*.json"))
    return json.loads(files[-1].read_text())


# ---------------------------------------------------------------- init

def test_init_creates_workspace_and_is_idempotent(tmp_path):
    assert sl.main(["--dir", str(tmp_path), "init"]) == 0
    ws = tmp_path / ".spokeslad"
    for sub in sl.SUBDIRS:
        assert (ws / sub).is_dir()
    assert json.loads((ws / "config.json").read_text())["product"]["name"] == "YourProduct"
    (ws / "messaging.md").write_text("mine")
    assert sl.main(["--dir", str(tmp_path), "init"]) == 0
    assert (ws / "messaging.md").read_text() == "mine"


# ---------------------------------------------------------------- listen

def test_listen_collects_classifies_and_filters(project, capsys):
    assert sl.main(["--dir", str(project), "listen", "--days", "2"]) == 0
    data = signals_of(project)
    by_id = {s["id"]: s for s in data["signals"]}
    assert "reddit:r2" not in by_id, "posts outside the window are dropped"
    assert "gh-release:400" not in by_id, "old releases are dropped"
    assert by_id["hn:1"]["kind"] == "mention"
    assert by_id["hn:2"]["kind"] == "competitor"
    assert by_id["hn:2"]["sentiment"] == "positive"
    assert by_id["hn:3"]["sentiment"] == "negative"
    assert by_id["gh-release:500"]["kind"] == "competitor-release"
    assert by_id["reddit:r1"]["entities"] == ["Spokeslad", "claude-gtm-plugin"]
    assert any(s["source"] == "feed" for s in data["signals"])
    assert data["signals"][0]["id"] == "hn:1", "sorted by engagement"
    out = capsys.readouterr().out
    assert "Possible negative mentions" in out and "Competitor releases" in out


def test_listen_skips_already_seen(project):
    sl.main(["--dir", str(project), "listen"])
    first = len(signals_of(project)["signals"])
    assert first > 0
    sl.main(["--dir", str(project), "listen"])
    assert len(signals_of(project)["signals"]) == first, "no duplicates on re-run"


def test_listen_survives_failing_sources(project, monkeypatch):
    def flaky(url, headers=None, timeout=20):
        if "reddit.com" in url:
            raise sl.urllib.error.URLError("blocked")
        return fake_get(url, headers, timeout)
    monkeypatch.setattr(sl, "HTTP_GET", flaky)
    assert sl.main(["--dir", str(project), "listen"]) == 0
    data = signals_of(project)
    assert any("reddit" in e for e in data["errors"])
    assert any(s["source"] == "hackernews" for s in data["signals"])


def test_name_matching_is_word_bounded():
    ent = {"name": "Spoke", "aliases": [], "repo": ""}
    assert sl.mentioned("I like Spoke a lot", ent) >= 0
    assert sl.mentioned("Spokeslad is different", ent) == -1
    assert sl.mentioned("bicycle spokes", ent) == -1


def test_sentiment_handles_negation():
    assert sl.rough_sentiment("this is not useful") == "negative"
    assert sl.rough_sentiment("it is not broken anymore") == "positive"
    assert sl.rough_sentiment("released version 2") == "neutral"


# ---------------------------------------------------------------- measure

def test_measure_share_of_voice_and_pull_through(project, capsys):
    sl.main(["--dir", str(project), "listen"])
    capsys.readouterr()
    assert sl.main(["--dir", str(project), "measure", "--json", "--stars"]) == 0
    r = json.loads(capsys.readouterr().out)
    counts = r["share_of_voice"]["counts"]
    # hn:1, hn:3, reddit:r1, gh-issue:99 mention Spokeslad. Releases are excluded.
    assert counts["Spokeslad"] == 4
    assert counts["marketingskills"] == 2  # hn:2 and the feed post
    assert counts["claude-gtm-plugin"] == 1
    assert r["row"]["share_of_voice"] == round(4 / 7, 4)
    assert r["pull_through"]["approval"]["hits"] == 1  # reddit:r1 says "approve"
    assert r["pull_through"]["listen"]["hits"] == 1    # issue says "listens"
    assert r["stars"]["Spokeslad"] == 42
    rows = list(csv.DictReader((project / ".spokeslad" / "metrics.csv").open()))
    assert len(rows) == 1 and rows[0]["product_mentions"] == "4"


def test_measure_reports_delta_against_previous_run(project, capsys):
    sl.main(["--dir", str(project), "listen"])
    sl.main(["--dir", str(project), "measure"])
    capsys.readouterr()
    sl.main(["--dir", str(project), "measure"])
    out = capsys.readouterr().out
    assert "pts vs" in out
    assert len(list(csv.DictReader((project / ".spokeslad" / "metrics.csv").open()))) == 2


def test_measure_dry_run_does_not_write(project):
    sl.main(["--dir", str(project), "listen"])
    sl.main(["--dir", str(project), "measure", "--dry-run"])
    assert not (project / ".spokeslad" / "metrics.csv").exists()


def test_ai_visibility_rank_and_rate(project):
    day = project / ".spokeslad" / "ai-answers" / "2026-10-01"
    day.mkdir(parents=True)
    (day / "q01.json").write_text(json.dumps({"question": "q1", "answer":
        "Try marketingskills first, or Spokeslad for PR."}))
    (day / "q02.json").write_text(json.dumps({"question": "q2", "answer":
        "Spokeslad is a good fit. claude-gtm-plugin also works."}))
    (day / "q03.md").write_text("Nothing relevant here.")
    _, answers = sl.load_ai_answers(project / ".spokeslad")
    vis = sl.ai_visibility(answers, CONFIG)
    assert vis["Spokeslad"]["mention_rate"] == pytest.approx(2 / 3)
    assert vis["Spokeslad"]["avg_rank"] == pytest.approx(1.5)  # rank 2 then rank 1
    assert vis["marketingskills"]["avg_rank"] == 1


def test_probe_ai_saves_answers(project, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    calls = []

    def fake_post(url, payload, headers, timeout=90):
        calls.append((url, payload, headers))
        return {"content": [{"type": "text", "text": "Spokeslad and marketingskills."}]}
    monkeypatch.setattr(sl, "HTTP_POST_JSON", fake_post)
    day = sl.probe_ai(CONFIG, project / ".spokeslad")
    saved = json.loads((project / ".spokeslad" / "ai-answers" / day / "q01.json").read_text())
    assert saved["answer"].startswith("Spokeslad")
    assert calls[0][2]["anthropic-version"] == "2023-06-01"
    assert calls[0][1]["messages"][0]["content"] == "best PR tool for devs?"


# ---------------------------------------------------------------- lint

def rules(findings, level=None):
    return [f["rule"] for f in findings if level is None or f["level"] == level]


def test_lint_flags_hype_numbers_placeholders_and_never_say():
    text = ("Spokeslad is a revolutionary game-changer.\n"
            "It makes launches 3x faster and grows reach 40%.\n"
            "Used by 500 developers.\n"
            "See [link] for details. TODO add demo\n"
            "Expect guaranteed virality.\n")
    f = sl.lint_text("announcement.md", text, CONFIG)
    errs = rules(f, "error")
    assert errs.count("hype") >= 2
    assert "unsourced-number" in errs
    assert errs.count("placeholder") == 2
    assert "never-say" in errs
    assert "unsourced-number" in rules(f, "warning")  # "500 developers"


def test_lint_accepts_sources_and_approved_claims():
    text = ("It grew 40% in a week [source: https://example.com/stats].\n"
            "Spokeslad installs in one command.\n"
            "The best part: nothing posts without you. <!-- spokeslad-ignore -->\n")
    assert rules(sl.lint_text("announcement.md", text, CONFIG), "error") == []


def test_lint_ignores_code_blocks_and_comments():
    text = "```\nTODO: 10x faster\n```\n<!-- note: TODO 40% -->\nPlain line.\n"
    assert sl.lint_text("announcement.md", text, CONFIG) == []


def test_lint_show_hn_title_rules():
    assert "show-hn-title" in rules(sl.lint_text("show-hn.md", "# My cool tool\nbody", CONFIG))
    long = "Show HN: " + "a" * 80
    assert "show-hn-title" in rules(sl.lint_text("show-hn.md", long, CONFIG))
    assert rules(sl.lint_text("show-hn.md", "Show HN: Spokeslad – PR team in Claude Code\nHi",
                              CONFIG), "error") == []


def test_lint_x_thread_counts_urls_as_23():
    ok = "a" * 250 + " https://example.com/" + "b" * 200
    assert sl._x_len(ok) == 250 + 1 + 23
    thread = "first post\n---\n" + "x" * 281 + "\n---\nlast"
    f = sl.lint_text("x-thread.md", thread, CONFIG)
    assert rules(f, "error") == ["x-length"]
    assert f[0]["line"] == 3


def test_lint_reddit_requires_disclosure():
    assert "disclosure" in rules(sl.lint_text("reddit-ClaudeAI.md", "Check out Spokeslad!", CONFIG))
    assert rules(sl.lint_text("reddit-ClaudeAI.md", "I built Spokeslad because...", CONFIG),
                 "error") == []


def test_lint_cli_exit_codes(tmp_path, capsys):
    good = tmp_path / "announcement.md"
    good.write_text("A plain, honest post.\n")
    assert sl.main(["--dir", str(tmp_path), "lint", str(good)]) == 0
    bad = tmp_path / "x-thread.md"
    bad.write_text("y" * 300)
    assert sl.main(["--dir", str(tmp_path), "lint", str(tmp_path)]) == 1
    assert "x-length" in capsys.readouterr().out


def test_measure_with_no_mentions_says_na(project, capsys):
    assert sl.main(["--dir", str(project), "measure", "--dry-run"]) == 0
    assert "Share of voice: n/a" in capsys.readouterr().out


def test_lint_skips_words_that_are_quoted_not_claimed():
    text = 'The linter fails hype words like "revolutionary" and `10x faster`.\n'
    assert rules(sl.lint_text("announcement.md", text, CONFIG), "error") == []
    assert "hype" in rules(sl.lint_text("announcement.md", "It is revolutionary.", CONFIG))


def test_lint_pitch_length_ignores_pitch_list():
    long = "word " * 300
    assert rules(sl.lint_text("pitch-list.md", long, CONFIG)) == []
    assert "pitch-length" in rules(sl.lint_text("pitches.md", long, CONFIG))
