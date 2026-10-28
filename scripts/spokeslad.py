#!/usr/bin/env python3
"""Spokeslad command-line helpers.

Deterministic, dependency-free tools that the Spokeslad skills call:

  spokeslad init     create the .spokeslad/ workspace in a project
  spokeslad listen   collect new mentions from HN, Reddit, GitHub and feeds
  spokeslad measure  compute share of voice, sentiment, message pull-through
                     and AI-answer visibility; append to metrics.csv
  spokeslad lint     check drafts for hype, unsourced numbers, banned phrases,
                     leftover placeholders and platform limits

Judgment (what matters, what to say) is left to Claude and to you. These
tools only do what code does better: fetching, counting and rule checks.
Standard library only, Python 3.9+.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

VERSION = "0.1.0"
USER_AGENT = f"spokeslad/{VERSION} (+https://github.com/EboMutele/spokeslad)"
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = PLUGIN_ROOT / "templates"
WORKSPACE = ".spokeslad"
SUBDIRS = ("signals", "digests", "launches", "crisis", "ai-answers", "reports")


# --------------------------------------------------------------------------
# HTTP (module-level so tests can replace it)
# --------------------------------------------------------------------------

def _http_get(url: str, headers: dict | None = None, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (fixed hosts)
        return resp.read().decode("utf-8", errors="replace")


def _http_post_json(url: str, payload: dict, headers: dict, timeout: int = 90) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"User-Agent": USER_AGENT, "content-type": "application/json", **headers},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return json.loads(resp.read().decode("utf-8"))


HTTP_GET = _http_get
HTTP_POST_JSON = _http_post_json
SLEEP = time.sleep


# --------------------------------------------------------------------------
# Workspace and config
# --------------------------------------------------------------------------

def workspace(root: str | Path) -> Path:
    return Path(root) / WORKSPACE


def load_config(root: str | Path) -> dict:
    path = workspace(root) / "config.json"
    if not path.exists():
        raise SystemExit(f"No {path}. Run `spokeslad init` (or /spokeslad:brief) first.")
    with path.open(encoding="utf-8") as fh:
        cfg = json.load(fh)
    cfg.setdefault("product", {})
    cfg.setdefault("competitors", [])
    cfg.setdefault("keywords", [])
    cfg.setdefault("subreddits", [])
    cfg.setdefault("sources", {})
    cfg.setdefault("key_messages", [])
    cfg.setdefault("approved_claims", [])
    cfg.setdefault("never_say", [])
    cfg.setdefault("ai_probe", {})
    return cfg


def entities(cfg: dict) -> list[dict]:
    """Product first, then competitors. Each: {name, aliases, role, repo}."""
    out = []
    p = cfg.get("product", {})
    if p.get("name"):
        out.append({"name": p["name"], "aliases": p.get("aliases", []), "role": "product",
                    "repo": p.get("repo", "")})
    for c in cfg.get("competitors", []):
        if c.get("name"):
            out.append({"name": c["name"], "aliases": c.get("aliases", []), "role": "competitor",
                        "repo": c.get("repo", ""), "feeds": c.get("feeds", [])})
    return out


def _name_patterns(ent: dict) -> list[re.Pattern]:
    names = [ent["name"], *ent.get("aliases", [])]
    if ent.get("repo"):
        names.append(ent["repo"])
    pats = []
    for n in names:
        n = n.strip()
        if n:
            pats.append(re.compile(r"(?<![\w/-])" + re.escape(n) + r"(?![\w-])", re.IGNORECASE))
    return pats


def mentioned(text: str, ent: dict) -> int:
    """Index of first mention of an entity in text, or -1."""
    first = -1
    for pat in _name_patterns(ent):
        m = pat.search(text or "")
        if m and (first == -1 or m.start() < first):
            first = m.start()
    return first


# --------------------------------------------------------------------------
# Rough sentiment (a triage hint only; Claude reads the actual text)
# --------------------------------------------------------------------------

POS = {"love", "loving", "great", "awesome", "amazing", "useful", "helpful", "impressive",
       "excellent", "nice", "brilliant", "fantastic", "recommend", "solid", "favorite",
       "favourite", "thanks", "thank", "works", "fast", "clean", "elegant", "cool"}
NEG = {"hate", "broken", "bug", "bugs", "buggy", "slow", "terrible", "awful", "useless",
       "spam", "scam", "worse", "worst", "crash", "crashes", "fail", "fails", "failed",
       "disappointed", "disappointing", "annoying", "overhyped", "hype", "garbage", "leak",
       "breach", "vulnerability", "insecure", "outage", "down", "sucks", "astroturf",
       "astroturfing", "shill", "misleading"}
NEGATORS = {"not", "no", "never", "isn't", "isnt", "doesn't", "doesnt", "don't", "dont",
            "wasn't", "wasnt", "hardly"}


def rough_sentiment(text: str) -> str:
    words = re.findall(r"[a-z']+", (text or "").lower())
    score = 0
    for i, w in enumerate(words):
        sign = 1 if w in POS else -1 if w in NEG else 0
        if sign and i > 0 and words[i - 1] in NEGATORS:
            sign = -sign
        score += sign
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"


# --------------------------------------------------------------------------
# init
# --------------------------------------------------------------------------

def cmd_init(args) -> int:
    ws = workspace(args.dir)
    ws.mkdir(parents=True, exist_ok=True)
    for sub in SUBDIRS:
        (ws / sub).mkdir(exist_ok=True)
    created = []
    for name in ("config.json", "messaging.md"):
        dest = ws / name
        if not dest.exists():
            shutil.copyfile(TEMPLATES / name, dest)
            created.append(name)
    log = ws / "log.md"
    if not log.exists():
        log.write_text("# Spokeslad log\n\nApprovals, publications and decisions, newest last.\n\n",
                       encoding="utf-8")
        created.append("log.md")
    print(f"Workspace ready at {ws}")
    if created:
        print("Created: " + ", ".join(created))
    print("Next: run /spokeslad:brief to fill in messaging.md and config.json.")
    return 0


# --------------------------------------------------------------------------
# listen
# --------------------------------------------------------------------------

def _iso(ts: float | int | str | None) -> str:
    if ts is None:
        return ""
    if isinstance(ts, (int, float)):
        return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).isoformat()
    return str(ts)


def _strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = (s.replace("&quot;", '"').replace("&#x27;", "'").replace("&#39;", "'")
          .replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#x2F;", "/"))
    return re.sub(r"\s+", " ", s).strip()


def search_terms(cfg: dict) -> list[str]:
    terms = []
    for ent in entities(cfg):
        terms.append(ent["name"])
    terms.extend(cfg.get("keywords", []))
    seen, out = set(), []
    for t in terms:
        k = t.lower().strip()
        if k and k not in seen:
            seen.add(k)
            out.append(t.strip())
    return out


def fetch_hn(term: str, since: dt.datetime) -> list[dict]:
    q = urllib.parse.urlencode({
        "query": f'"{term}"', "tags": "(story,comment)", "hitsPerPage": 50,
        "numericFilters": f"created_at_i>{int(since.timestamp())}",
    })
    data = json.loads(HTTP_GET(f"https://hn.algolia.com/api/v1/search_by_date?{q}"))
    out = []
    for h in data.get("hits", []):
        oid = h.get("objectID")
        title = h.get("title") or h.get("story_title") or ""
        text = _strip_html(h.get("comment_text") or h.get("story_text") or "")
        out.append({
            "id": f"hn:{oid}", "source": "hackernews",
            "title": title, "text": text[:600],
            "url": f"https://news.ycombinator.com/item?id={oid}",
            "link": h.get("url") or "",
            "author": h.get("author", ""), "created_at": _iso(h.get("created_at_i")),
            "score": h.get("points") or 0, "comments": h.get("num_comments") or 0,
            "type": "comment" if h.get("comment_text") else "story",
        })
    return out


def fetch_reddit(term: str, since: dt.datetime, subreddits: list[str]) -> list[dict]:
    params = {"q": f'"{term}"', "sort": "new", "t": "week", "limit": 50, "raw_json": 1}
    if subreddits:
        path = "r/" + "+".join(subreddits) + "/search.json"
        params["restrict_sr"] = "on"
    else:
        path = "search.json"
    data = json.loads(HTTP_GET(f"https://www.reddit.com/{path}?{urllib.parse.urlencode(params)}"))
    out = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        created = d.get("created_utc") or 0
        if created and created < since.timestamp():
            continue
        out.append({
            "id": f"reddit:{d.get('id')}", "source": "reddit",
            "title": d.get("title", ""), "text": (d.get("selftext") or "")[:600],
            "url": "https://www.reddit.com" + d.get("permalink", ""),
            "link": d.get("url", ""), "author": d.get("author", ""),
            "created_at": _iso(created), "score": d.get("score") or 0,
            "comments": d.get("num_comments") or 0,
            "subreddit": d.get("subreddit", ""), "type": "post",
        })
    return out


def _gh_headers() -> dict:
    h = {"Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def fetch_github_issues(term: str, since: dt.datetime) -> list[dict]:
    q = urllib.parse.urlencode({"q": f'"{term}" created:>={since.date().isoformat()}',
                                "sort": "created", "order": "desc", "per_page": 30})
    data = json.loads(HTTP_GET(f"https://api.github.com/search/issues?{q}", _gh_headers()))
    out = []
    for it in data.get("items", []):
        out.append({
            "id": f"gh-issue:{it.get('id')}", "source": "github",
            "title": it.get("title", ""), "text": (it.get("body") or "")[:600],
            "url": it.get("html_url", ""), "link": "",
            "author": (it.get("user") or {}).get("login", ""),
            "created_at": it.get("created_at", ""), "score": it.get("reactions", {}).get("total_count", 0)
            if isinstance(it.get("reactions"), dict) else 0,
            "comments": it.get("comments") or 0,
            "type": "pull_request" if it.get("pull_request") else "issue",
        })
    return out


def fetch_github_releases(repo: str, since: dt.datetime) -> list[dict]:
    data = json.loads(HTTP_GET(f"https://api.github.com/repos/{repo}/releases?per_page=10",
                               _gh_headers()))
    out = []
    for r in data if isinstance(data, list) else []:
        pub = r.get("published_at") or r.get("created_at") or ""
        if pub and _parse_iso(pub) < since:
            continue
        out.append({
            "id": f"gh-release:{r.get('id')}", "source": "github-release",
            "title": f"{repo} {r.get('tag_name', '')}: {r.get('name') or ''}".strip(),
            "text": (r.get("body") or "")[:600], "url": r.get("html_url", ""), "link": "",
            "author": (r.get("author") or {}).get("login", ""), "created_at": pub,
            "score": 0, "comments": 0, "type": "release", "repo": repo,
        })
    return out


def fetch_feed(url: str, since: dt.datetime) -> list[dict]:
    root = ET.fromstring(HTTP_GET(url))
    items = []
    atom = "{http://www.w3.org/2005/Atom}"
    for it in root.iter("item"):
        items.append((it.findtext("title") or "", it.findtext("link") or "",
                      it.findtext("description") or "", it.findtext("pubDate") or "",
                      it.findtext("guid") or it.findtext("link") or ""))
    for it in root.iter(f"{atom}entry"):
        link_el = it.find(f"{atom}link")
        link = link_el.get("href", "") if link_el is not None else ""
        items.append((it.findtext(f"{atom}title") or "", link,
                      it.findtext(f"{atom}summary") or it.findtext(f"{atom}content") or "",
                      it.findtext(f"{atom}updated") or it.findtext(f"{atom}published") or "",
                      it.findtext(f"{atom}id") or link))
    out = []
    for title, link, desc, date, guid in items:
        when = _parse_any_date(date)
        if when and when < since:
            continue
        out.append({
            "id": f"feed:{guid}", "source": "feed", "title": _strip_html(title),
            "text": _strip_html(desc)[:600], "url": link, "link": "", "author": "",
            "created_at": when.isoformat() if when else "", "score": 0, "comments": 0,
            "type": "post", "feed": url,
        })
    return out


def _parse_iso(s: str) -> dt.datetime:
    s = s.strip().replace("Z", "+00:00")
    d = dt.datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def _parse_any_date(s: str) -> dt.datetime | None:
    if not s:
        return None
    try:
        return _parse_iso(s)
    except ValueError:
        pass
    from email.utils import parsedate_to_datetime
    try:
        d = parsedate_to_datetime(s)
        return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def seen_ids(ws: Path) -> set[str]:
    ids = set()
    for f in sorted((ws / "signals").glob("*.json")):
        try:
            for s in json.loads(f.read_text(encoding="utf-8")).get("signals", []):
                ids.add(s["id"])
        except (json.JSONDecodeError, KeyError):
            continue
    return ids


def classify(sig: dict, cfg: dict) -> dict:
    blob = f"{sig.get('title', '')} {sig.get('text', '')} {sig.get('link', '')}"
    found = [e for e in entities(cfg) if mentioned(blob, e) >= 0]
    sig["entities"] = [e["name"] for e in found]
    if sig.get("type") == "release":
        sig["kind"] = "competitor-release"
    elif any(e["role"] == "product" for e in found):
        sig["kind"] = "mention"
    elif found:
        sig["kind"] = "competitor"
    else:
        sig["kind"] = "category"
    sig["sentiment"] = rough_sentiment(blob)
    sig["engagement"] = int(sig.get("score") or 0) + int(sig.get("comments") or 0)
    return sig


def cmd_listen(args) -> int:
    cfg = load_config(args.dir)
    ws = workspace(args.dir)
    (ws / "signals").mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    since = now - dt.timedelta(days=args.days)
    # Reddit is opt-in: its unauthenticated search endpoint is rate-limited and its
    # API terms favour OAuth clients. Without it, /spokeslad:listen covers Reddit
    # through web search.
    src = {"hackernews": True, "reddit": False, "github": True, **cfg.get("sources", {})}
    if args.only:
        wanted = set(args.only.split(","))
        src = {k: (k in wanted) for k in src}

    raw, errors = [], []

    def attempt(label, fn, *a):
        for tries in (1, 2):
            try:
                raw.extend(fn(*a))
                break
            except urllib.error.HTTPError as exc:
                if exc.code == 429 and tries == 1:  # rate limited: wait once, then retry
                    wait = exc.headers.get("Retry-After", "") if exc.headers else ""
                    SLEEP(min(int(wait) if wait.isdigit() else 10, 60))
                    continue
                errors.append(f"{label}: {exc}")
                break
            except (urllib.error.URLError, OSError, ValueError, ET.ParseError) as exc:
                errors.append(f"{label}: {exc}")
                break
        SLEEP(args.delay)

    for term in search_terms(cfg):
        if src.get("hackernews"):
            attempt(f"hackernews '{term}'", fetch_hn, term, since)
        if src.get("reddit"):
            attempt(f"reddit '{term}'", fetch_reddit, term, since, cfg.get("subreddits", []))
        if src.get("github"):
            attempt(f"github '{term}'", fetch_github_issues, term, since)
    if src.get("github"):
        for ent in entities(cfg):
            if ent["role"] == "competitor" and ent.get("repo"):
                attempt(f"releases {ent['repo']}", fetch_github_releases, ent["repo"], since)
    feeds = list(cfg.get("sources", {}).get("feeds", []) or [])
    for ent in entities(cfg):
        feeds.extend(ent.get("feeds", []) or [])
    for url in feeds:
        attempt(f"feed {url}", fetch_feed, url, since)

    old = seen_ids(ws)
    uniq, new = {}, []
    for s in raw:
        if s["id"] in uniq:
            continue
        uniq[s["id"]] = s
        if s["id"] not in old:
            new.append(classify(s, cfg))
    new.sort(key=lambda s: s.get("engagement", 0), reverse=True)

    stamp = now.strftime("%Y-%m-%d")
    out = ws / "signals" / f"{stamp}.json"
    payload = {"collected_at": now.isoformat(), "window_days": args.days, "signals": new,
               "errors": errors}
    if out.exists():  # same-day re-run: merge
        prev = json.loads(out.read_text(encoding="utf-8"))
        ids = {s["id"] for s in prev.get("signals", [])}
        prev["signals"].extend(s for s in new if s["id"] not in ids)
        prev["errors"] = prev.get("errors", []) + errors
        prev["collected_at"] = now.isoformat()
        payload = prev
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.json:
        print(json.dumps({"file": str(out), "new": len(new), "errors": errors}, indent=2))
    else:
        print(render_listen_summary(new, errors, out))
    return 0


def render_listen_summary(new: list[dict], errors: list[str], path: Path) -> str:
    lines = [f"# Listening run: {len(new)} new signals", f"Saved to {path}", ""]
    kinds = {}
    for s in new:
        kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
    if kinds:
        lines.append("By kind: " + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())))
    neg = [s for s in new if s["kind"] == "mention" and s["sentiment"] == "negative"]
    if neg:
        lines += ["", f"## Possible negative mentions ({len(neg)}), read these first"]
        lines += [f"- [{s['source']}] {s['title'] or s['text'][:90]} ({s['url']})" for s in neg[:10]]
    lines += ["", "## Top by engagement"]
    for s in new[:10]:
        ents = ", ".join(s["entities"]) or "category"
        lines.append(f"- [{s['source']}/{s['kind']}] {s['title'] or s['text'][:90]} "
                     f"({s['engagement']} eng., {ents}) {s['url']}")
    rel = [s for s in new if s["kind"] == "competitor-release"]
    if rel:
        lines += ["", "## Competitor releases"]
        lines += [f"- {s['title']} {s['url']}" for s in rel]
    if errors:
        lines += ["", f"## Sources that failed ({len(errors)})"]
        lines += [f"- {e}" for e in errors[:15]]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# measure
# --------------------------------------------------------------------------

METRIC_FIELDS = ["date", "window_days", "signals", "product_mentions", "share_of_voice",
                 "share_of_voice_weighted", "positive", "negative", "neutral",
                 "ai_answers", "ai_mention_rate", "ai_avg_rank", "stars"]


def load_signals(ws: Path, days: int, now: dt.datetime | None = None) -> list[dict]:
    now = now or dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=days)
    out, ids = [], set()
    for f in sorted((ws / "signals").glob("*.json")):
        try:
            sigs = json.loads(f.read_text(encoding="utf-8")).get("signals", [])
        except json.JSONDecodeError:
            continue
        for s in sigs:
            if s.get("id") in ids:
                continue
            when = _parse_any_date(s.get("created_at", ""))
            if when is None or when >= cutoff:
                ids.add(s.get("id"))
                out.append(s)
    return out


def share_of_voice(signals: list[dict], cfg: dict) -> dict:
    ents = entities(cfg)
    counts = {e["name"]: 0 for e in ents}
    weighted = {e["name"]: 0 for e in ents}
    for s in signals:
        if s.get("kind") == "competitor-release":
            continue  # own announcements are not earned voice
        blob = f"{s.get('title', '')} {s.get('text', '')} {s.get('link', '')}"
        for e in ents:
            if mentioned(blob, e) >= 0:
                counts[e["name"]] += 1
                weighted[e["name"]] += 1 + int(s.get("engagement") or 0)
    total, wtotal = sum(counts.values()), sum(weighted.values())
    return {
        "counts": counts,
        "share": {k: (v / total if total else 0.0) for k, v in counts.items()},
        "weighted_share": {k: (v / wtotal if wtotal else 0.0) for k, v in weighted.items()},
    }


def pull_through(signals: list[dict], cfg: dict) -> dict:
    prod = [e for e in entities(cfg) if e["role"] == "product"]
    if not prod:
        return {}
    mine = [s for s in signals
            if mentioned(f"{s.get('title', '')} {s.get('text', '')}", prod[0]) >= 0]
    out = {}
    for m in cfg.get("key_messages", []):
        kws = [k.lower() for k in m.get("keywords", []) if k]
        hits = sum(1 for s in mine
                   if any(k in f"{s.get('title', '')} {s.get('text', '')}".lower() for k in kws))
        out[m.get("id", m.get("message", "?")[:30])] = {
            "message": m.get("message", ""), "hits": hits, "of": len(mine),
            "rate": hits / len(mine) if mine else 0.0}
    return out


def load_ai_answers(ws: Path, date: str | None = None) -> tuple[str, list[dict]]:
    base = ws / "ai-answers"
    if not base.exists():
        return "", []
    days = sorted(d.name for d in base.iterdir() if d.is_dir())
    if not days:
        return "", []
    day = date if date in days else days[-1]
    answers = []
    for f in sorted((base / day).iterdir()):
        if f.suffix == ".json":
            try:
                answers.append(json.loads(f.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                continue
        elif f.suffix in (".md", ".txt"):
            answers.append({"question": f.stem, "answer": f.read_text(encoding="utf-8"),
                            "source": "manual"})
    return day, answers


def ai_visibility(answers: list[dict], cfg: dict) -> dict:
    ents = entities(cfg)
    per = {e["name"]: {"mentioned": 0, "ranks": []} for e in ents}
    for a in answers:
        text = a.get("answer", "")
        positions = sorted((mentioned(text, e), e["name"]) for e in ents if mentioned(text, e) >= 0)
        for rank, (_, name) in enumerate(positions, start=1):
            per[name]["mentioned"] += 1
            per[name]["ranks"].append(rank)
    n = len(answers)
    return {name: {
        "mention_rate": (v["mentioned"] / n if n else 0.0),
        "avg_rank": (sum(v["ranks"]) / len(v["ranks"]) if v["ranks"] else None),
        "mentioned": v["mentioned"], "answers": n} for name, v in per.items()}


def probe_ai(cfg: dict, ws: Path) -> str:
    """Ask Claude the configured buyer questions; save answers for scoring.

    Measures what a model says from its own knowledge (no web), which is a
    lagging but real signal of how the category is being described.
    """
    key = os.environ.get("ANTHROPIC_API_KEY")
    questions = cfg.get("ai_probe", {}).get("questions", [])
    if not key:
        raise SystemExit("ANTHROPIC_API_KEY is not set; skip --probe-ai or set the key.")
    if not questions:
        raise SystemExit("No ai_probe.questions in config.json.")
    model = cfg.get("ai_probe", {}).get("model") or "claude-sonnet-5-5"
    day = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    out = ws / "ai-answers" / day
    out.mkdir(parents=True, exist_ok=True)
    for i, q in enumerate(questions, start=1):
        resp = HTTP_POST_JSON("https://api.anthropic.com/v1/messages", {
            "model": model, "max_tokens": 900,
            "messages": [{"role": "user", "content": q}]},
            {"x-api-key": key, "anthropic-version": "2023-06-01"})
        text = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
        (out / f"q{i:02d}.json").write_text(json.dumps(
            {"question": q, "answer": text, "source": f"anthropic:{model}"}, indent=2),
            encoding="utf-8")
    return day


def fetch_stars(repo: str) -> int | None:
    try:
        data = json.loads(HTTP_GET(f"https://api.github.com/repos/{repo}", _gh_headers()))
        return int(data.get("stargazers_count"))
    except (urllib.error.URLError, OSError, ValueError, TypeError):
        return None


def _fmt_pct(x) -> str:
    return "n/a" if x is None or x == "" else f"{float(x) * 100:.1f}%"


def cmd_measure(args) -> int:
    cfg = load_config(args.dir)
    ws = workspace(args.dir)
    product = cfg.get("product", {}).get("name", "")
    if args.probe_ai:
        probe_ai(cfg, ws)
    sigs = load_signals(ws, args.days)
    sov = share_of_voice(sigs, cfg)
    pt = pull_through(sigs, cfg)
    ai_day, answers = load_ai_answers(ws)
    vis = ai_visibility(answers, cfg) if answers else {}
    stars = {}
    if args.stars:
        for e in entities(cfg):
            if e.get("repo"):
                stars[e["name"]] = fetch_stars(e["repo"])

    prod_sigs = [s for s in sigs
                 if product and product in s.get("entities", [])]
    sent = {k: sum(1 for s in prod_sigs if s.get("sentiment") == k)
            for k in ("positive", "negative", "neutral")}
    pv = vis.get(product, {})
    row = {
        "date": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "window_days": args.days, "signals": len(sigs),
        "product_mentions": sov["counts"].get(product, 0),
        "share_of_voice": round(sov["share"].get(product, 0.0), 4),
        "share_of_voice_weighted": round(sov["weighted_share"].get(product, 0.0), 4),
        **sent,
        "ai_answers": pv.get("answers", 0),
        "ai_mention_rate": round(pv["mention_rate"], 4) if pv else "",
        "ai_avg_rank": round(pv["avg_rank"], 2) if pv and pv.get("avg_rank") else "",
        "stars": stars.get(product) if stars.get(product) is not None else "",
    }
    metrics = ws / "metrics.csv"
    prev = None
    if metrics.exists():
        with metrics.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
            prev = rows[-1] if rows else None
    if not args.dry_run:
        new_file = not metrics.exists()
        with metrics.open("a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=METRIC_FIELDS)
            if new_file:
                w.writeheader()
            w.writerow(row)

    result = {"row": row, "previous": prev, "share_of_voice": sov, "pull_through": pt,
              "ai_visibility": vis, "ai_answers_date": ai_day, "stars": stars}
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(render_measure(result, product))
    return 0


def render_measure(r: dict, product: str) -> str:
    row, prev = r["row"], r["previous"]

    def delta(field):
        if not prev or prev.get(field) in (None, "") or row.get(field) in (None, ""):
            return ""
        d = float(row[field]) - float(prev[field])
        return f" ({'+' if d >= 0 else ''}{d * 100:.1f} pts vs {prev['date']})" \
            if field.startswith(("share", "ai_mention")) else f" ({'+' if d >= 0 else ''}{d:g})"

    lines = [f"# Measurement, last {row['window_days']} days ({row['signals']} signals)", ""]
    if not sum(r["share_of_voice"]["counts"].values()):
        lines.append("- Share of voice: n/a, no mentions of any tracked name in this window "
                     "(run /spokeslad:listen, or check which sources failed)")
    else:
        lines.append(f"- Share of voice: {_fmt_pct(row['share_of_voice'])}{delta('share_of_voice')}")
        lines.append(f"- Engagement-weighted share of voice: "
                     f"{_fmt_pct(row['share_of_voice_weighted'])}{delta('share_of_voice_weighted')}")
    lines.append(f"- {product} mentions: {row['product_mentions']}{delta('product_mentions')} "
                 f"(rough sentiment: {row['positive']} positive, {row['negative']} negative, "
                 f"{row['neutral']} neutral)")
    if row["ai_answers"]:
        rank = row["ai_avg_rank"] or "not mentioned"
        lines.append(f"- AI answers ({r['ai_answers_date']}): mentioned in "
                     f"{_fmt_pct(row['ai_mention_rate'])} of {row['ai_answers']}"
                     f"{delta('ai_mention_rate')}, average rank {rank}")
    else:
        lines.append("- AI answers: none collected yet (see /spokeslad:measure)")
    if r["stars"]:
        lines.append("- GitHub stars: " + ", ".join(
            f"{k} {v if v is not None else 'n/a'}" for k, v in r["stars"].items()))
    lines += ["", "## Share of voice by name"]
    for name, cnt in sorted(r["share_of_voice"]["counts"].items(), key=lambda kv: -kv[1]):
        lines.append(f"- {name}: {cnt} mentions, {_fmt_pct(r['share_of_voice']['share'][name])}")
    if r["ai_visibility"]:
        lines += ["", "## AI answer visibility by name"]
        for name, v in sorted(r["ai_visibility"].items(), key=lambda kv: -kv[1]["mention_rate"]):
            lines.append(f"- {name}: {_fmt_pct(v['mention_rate'])}, avg rank "
                         f"{v['avg_rank'] if v['avg_rank'] else 'n/a'}")
    if r["pull_through"]:
        lines += ["", "## Key message pull-through (share of your mentions repeating it)"]
        for mid, v in r["pull_through"].items():
            lines.append(f"- {mid}: {v['hits']}/{v['of']} ({_fmt_pct(v['rate'])}) {v['message']}")
    lines += ["", "Sentiment is a keyword heuristic for triage. Read the mentions before "
                  "drawing conclusions."]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# lint
# --------------------------------------------------------------------------

HYPE_ERRORS = [
    r"\brevolution(ary|i[sz](e|es|ed|ing))\b", r"game[- ]?chang(er|ing)", r"world'?s first",
    r"best[- ]in[- ]class", r"industry[- ]leading", r"unparalleled", r"unprecedented",
    r"guarantee[ds]?", r"\b\d+x (better|faster|more)\b", r"\bthe only\b", r"#1\b",
    r"\bnumber one\b", r"\bthe best\b", r"\bnever been easier\b", r"\bdisrupt(s|ing|ive)?\b",
    r"\bkiller (app|feature)\b", r"\b(zero|no) learning curve\b",
]
SLOP_WARNINGS = [
    r"\bseamless(ly)?\b", r"\bcutting[- ]edge\b", r"\bsupercharg(e|es|ed|ing)\b",
    r"\bunlock(s|ing)? the (power|potential)\b", r"\bharness(es|ing)? the power\b",
    r"\bin today'?s fast[- ]paced\b", r"\bever[- ]evolving\b", r"\bdelve\b",
    r"\belevate(s|d)? your\b", r"\bleverag(e|es|ing)\b", r"\brobust\b", r"\bmagic(al|ally)?\b",
    r"\beffortless(ly)?\b", r"\bnext[- ]level\b", r"\bempower(s|ing)?\b",
    r"\b(a|the) testament to\b", r"\btake (it|your \w+) to the next level\b",
]
PLACEHOLDERS = [r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bXXX\b",
                r"\{\{[^}]*\}\}", r"lorem ipsum", r"<placeholder>",
                # any [bracketed note] that is not a markdown link, checkbox,
                # footnote or [source: ...] marker, e.g. "[step]", "[link to docs]"
                r"(?<!\])\[(?!source:)(?![ xX]\])(?!\^)[^\]\n]{1,60}\](?![(\[:])"]
NUM_ERRORS = [
    re.compile(r"\b\d[\d,.]*\s?(%|percent\b|x\b)", re.IGNORECASE),           # 40%, 3x
    re.compile(r"[$€£]\s?\d[\d,.]*\s?(k|m|bn|b|million|billion)?\b", re.IGNORECASE),  # $5M
    re.compile(r"\b\d[\d,.]*\s?(k|m)?\+?\s(users|customers|companies|teams|developers|"
               r"downloads|installs|stars|signups|sign-ups|subscribers|readers|businesses)\b",
               re.IGNORECASE),                                                  # 500 teams
    re.compile(r"\bfortune\s?(50|100|500)\b", re.IGNORECASE),
]
NUM_WARN = re.compile(r"\b\d[\d,.]*\s(seconds|minutes|hours|days|weeks|months)\b",
                      re.IGNORECASE)                                            # time claims
URL_RE = re.compile(r"https?://\S+")
IGNORE = "spokeslad-ignore"
SOURCE_MARK = re.compile(r"\[source:[^\]]+\]", re.IGNORECASE)
QUOTED = re.compile(r'"[^"\n]{1,60}"|“[^”\n]{1,60}”|`[^`\n]{1,60}`')


def _approved(line: str, cfg: dict) -> bool:
    low = line.lower()
    for c in cfg.get("approved_claims", []):
        claim = (c.get("claim") if isinstance(c, dict) else str(c)) or ""
        if claim and claim.lower() in low:
            return True
    return False


def _x_len(text: str) -> int:
    # X counts every URL as 23 characters.
    return len(URL_RE.sub("x" * 23, text))


def _split_posts(text: str) -> list[tuple[int, str]]:
    """Split on lines that are exactly '---'. Returns (start_line, body)."""
    posts, buf, start = [], [], 1
    for i, line in enumerate(text.splitlines(), start=1):
        if line.strip() == "---":
            posts.append((start, "\n".join(buf).strip()))
            buf, start = [], i + 1
        else:
            buf.append(line)
    posts.append((start, "\n".join(buf).strip()))
    return [(s, b) for s, b in posts if b]


def _strip_meta(text: str) -> str:
    """Drop HTML comments (notes to the reviewer) but keep line numbers."""
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def lint_text(name: str, text: str, cfg: dict) -> list[dict]:
    findings = []

    def add(line, level, rule, msg):
        findings.append({"file": name, "line": line, "level": level, "rule": rule, "message": msg})

    ignored = {i for i, l in enumerate(text.splitlines(), start=1) if IGNORE in l}
    body = _strip_meta(text)
    lines = body.splitlines()
    never = [p for p in cfg.get("never_say", []) if p]
    in_code = False
    for i, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or i in ignored or not line.strip():
            continue
        sourced = bool(SOURCE_MARK.search(line)) or _approved(line, cfg)
        # Words in quotes or backticks are being mentioned, not claimed
        # (e.g. 'fails hype words like "revolutionary"'), so mask them.
        claimed = QUOTED.sub(lambda m: " " * len(m.group(0)), line)
        for pat in HYPE_ERRORS:
            m = re.search(pat, claimed, re.IGNORECASE)
            if m and not sourced:
                add(i, "error", "hype", f"'{m.group(0)}' is an unprovable or hype claim. "
                    "Cut it, or prove it and add [source: url].")
        for pat in SLOP_WARNINGS:
            m = re.search(pat, line, re.IGNORECASE)
            if m:
                add(i, "warning", "generic-language", f"'{m.group(0)}' reads as filler. "
                    "Say the concrete thing instead.")
        for pat in PLACEHOLDERS:
            m = re.search(pat, line, re.IGNORECASE if "lorem" in pat else 0)
            if m:
                add(i, "error", "placeholder", f"Leftover placeholder '{m.group(0)}'.")
        for phrase in never:
            if phrase.lower() in line.lower():
                add(i, "error", "never-say", f"'{phrase}' is on the never-say list in config.json.")
        if not sourced:
            bare = URL_RE.sub("", claimed)
            m = next((mm for mm in (r.search(bare) for r in NUM_ERRORS) if mm), None)
            if m:
                add(i, "error", "unsourced-number", f"'{m.group(0).strip()}' needs a source: "
                    "add it to approved_claims or mark the line with [source: url].")
            else:
                m = NUM_WARN.search(bare)
                if m:
                    add(i, "warning", "unsourced-number", f"'{m.group(0).strip()}': if this is "
                        "a claim about speed or savings, add [source: url].")

    low = name.lower()
    base = Path(low).name
    if "show-hn" in base:
        first = next(((i, l.strip()) for i, l in enumerate(lines, start=1) if l.strip()), None)
        if first:
            i, title = first
            title = title.lstrip("# ").strip()
            if not title.startswith("Show HN:"):
                add(i, "error", "show-hn-title", "The first line must be the title and start "
                    "with 'Show HN:'.")
            if len(title) > 80:
                add(i, "error", "show-hn-title", f"Title is {len(title)} characters; "
                    "HN allows 80.")
    if "x-thread" in base or base.startswith("x-") or "tweet" in base:
        for start, post in _split_posts(body):
            n = _x_len(post)
            if n > 280:
                add(start, "error", "x-length", f"Post is {n} characters (URLs count as 23); "
                    "the limit is 280.")
    if "linkedin" in base and len(body) > 3000:
        add(1, "error", "linkedin-length", f"{len(body)} characters; LinkedIn posts allow 3000.")
    if "reddit" in base:
        disclose = re.search(r"\b(I|we) (built|made|wrote|created|maintain)\b|\bdisclosure\b|"
                             r"\bmy (project|tool|plugin|side project)\b|\bI'?m the (author|maker|"
                             r"founder|dev)", body, re.IGNORECASE)
        if not disclose:
            add(1, "error", "disclosure", "Reddit post does not say you made this. "
                "Undisclosed self-promotion breaks most subreddit rules.")
    if "pitch" in base and "list" not in base:
        for start, post in _split_posts(body):
            words = len(re.findall(r"\S+", post))
            if words > 180:
                add(start, "warning", "pitch-length", f"Pitch is {words} words; "
                    "aim for under 150.")
    return findings


def cmd_lint(args) -> int:
    cfg = {}
    try:
        cfg = load_config(args.dir)
    except SystemExit:
        pass
    files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files += sorted(f for f in path.rglob("*")
                            if f.suffix in (".md", ".txt") and f.name.lower() not in
                            ("redteam.md", "plan.md", "readme.md", "checklist.md"))
        elif path.exists():
            files.append(path)
        else:
            print(f"Not found: {p}", file=sys.stderr)
    findings = []
    for f in files:
        findings += lint_text(str(f), f.read_text(encoding="utf-8"), cfg)
    errors = [f for f in findings if f["level"] == "error"]
    if args.json:
        print(json.dumps({"files": [str(f) for f in files], "errors": len(errors),
                          "warnings": len(findings) - len(errors), "findings": findings}, indent=2))
    else:
        for f in findings:
            print(f"{f['file']}:{f['line']}: {f['level']} [{f['rule']}] {f['message']}")
        print(f"\n{len(files)} files checked: {len(errors)} errors, "
              f"{len(findings) - len(errors)} warnings.")
    return 1 if errors else 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="spokeslad", description=__doc__.split("\n\n")[0])
    p.add_argument("--version", action="version", version=f"spokeslad {VERSION}")
    p.add_argument("--dir", default=".", help="project root containing .spokeslad/ (default: .)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create the .spokeslad/ workspace").set_defaults(fn=cmd_init)

    pl = sub.add_parser("listen", help="collect new mentions")
    pl.add_argument("--days", type=int, default=2, help="look-back window (default 2)")
    pl.add_argument("--only", help="comma-separated sources: hackernews,reddit,github")
    pl.add_argument("--delay", type=float, default=1.0,
                    help="seconds to wait between requests (default 1.0)")
    pl.add_argument("--json", action="store_true")
    pl.set_defaults(fn=cmd_listen)

    pm = sub.add_parser("measure", help="compute share of voice and AI visibility")
    pm.add_argument("--days", type=int, default=7, help="window (default 7)")
    pm.add_argument("--probe-ai", action="store_true", help="ask Claude the ai_probe questions "
                    "first (needs ANTHROPIC_API_KEY)")
    pm.add_argument("--stars", action="store_true", help="fetch GitHub stars for repos in config")
    pm.add_argument("--dry-run", action="store_true", help="do not append to metrics.csv")
    pm.add_argument("--json", action="store_true")
    pm.set_defaults(fn=cmd_measure)

    pt = sub.add_parser("lint", help="check drafts before anything is published")
    pt.add_argument("paths", nargs="+")
    pt.add_argument("--json", action="store_true")
    pt.set_defaults(fn=cmd_lint)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
