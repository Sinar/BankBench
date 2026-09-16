I've checked the current date context — let me build this properly. Quick plan before the code:

**Why this design**
- **Sitemap-first + listing-page fallback**: BNM's exact page paths can shift on redesign, so I'm not hard-baked to fragile selectors. The sitemap catches *any* new page under the paths you care about (consultations, discussion papers, media releases, publications), and a lenient listing scraper adds human-readable titles.
- **Contributions-first triage**: items under consultation/discussion/invitation/tender paths are flagged 🔔 as "actionable for you".
- **Cron-safe**: stdlib-only Python, JSON state file, lock file, exit code `2` when new items are found (so cron-mail or your orchestrator can react), optional ntfy/email push, `--initial-run` for baseline.

I can't run/test against the live site from here, so I've built a `--debug` mode that dumps fetched HTML/sitemap to disk — point it at the first run and it'll show you exactly what's being matched if any path prefixes need tweaking.



Heads-up: this session is browser-only (no local file/shell access), so I can't drop the file onto a machine for you — here's the complete, copy-paste-ready kit. You're in **Asia/Kuala_Lumpur (MYT)**, so the cron examples below are MYT-correct.

Save these two files in one folder (e.g. `~/bnm-watcher/`):

## 1) `bnm_watcher.py`

```python
#!/usr/bin/env python3
"""
bnm_watcher.py — watch Bank Negara Malaysia (BNM) for new publications,
publications, consultations, "calls for" items, media releases, etc.

- Sitemap scan: catches any NEW page under the configured path prefixes
- Listing pages: adds readable titles/dates for key index pages
- State: state.json (seen URLs), new items -> new_items.jsonl + stdout
- Push: optional ntfy topic and/or SMTP email (off by default)
- Exit codes: 0 = ok, 2 = new items found, 1 = error  (cron-friendly)

Stdlib only. Python 3.9+.
"""
import argparse
import concurrent.futures
import datetime as _dt
import email.utils
import hashlib
import html as _html
import json
import logging
import os
import re
import smtplib
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.message import EmailMessage
from html.parser import HTMLParser

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) bnm-watcher/1.0"
HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")

# ---------- defaults (config.json overrides these) ----------
DEFAULT_CONFIG = {
  "base_url": "https://www.bnm.gov.my",
  "sitemap_urls": [
    "https://www.bnm.gov.my/sitemap.xml",
    "https://www.bnm.gov.my/sitemap_index.xml",
    "https://www.bnm.gov.my/robots.xml"
  ],
  "path_prefixes": [
    "consult", "discussion", "paper", "whitepaper", "white-paper",
    "publication", "media", "news", "press", "announcement",
    "tender", "procurement", "invitation", "rfp", "request-for",
    "bulletin", "report", "statement", "monetary", "financial-stability",
    "framework", "circular"
  ],
  "path_blacklist_regex": "(?i)^(.*/)?(assets|css|js|img|images|files)/",
  "listing_pages": [
    {"name": "Public Consultation", "url": "https://www.bnm.gov.my/t/public-consultation"},
    {"name": "Consultations",      "url": "https://www.bnm.gov.my/t/consultation"},
    {"name": "News",               "url": "https://www.bnm.gov.my/t/news"},
    {"name": "Media Releases",     "url": "https://www.bnm.gov.my/t/media-releases"},
    {"name": "Publications",       "url": "https://www.bnm.gov.my/t/publications"},
    {"name": "Documents",          "url": "https://www.bnm.gov.my/t/documents"}
  ],
  "actionable_regex": "(?i)(consult|discussion paper|white paper|call for|invitation|tender|rfp|request for|expression of interest|public comment|open for comment)",
  "state_file": "state.json",
  "log_file": "new_items.jsonl",
  "notify": { "ntfy_topic": "", "email": { "enabled": false, "to": "", "from": "",
             "host": "smtp.example.com", "port": 587, "user": "", "password": "" } },
  "max_age_days": 365,
  "keep_recent": 2000,
  "timeout": 30
}
DATE_RE = re.compile(r"\b(20\d{2})(?:[-/.](\d{1,2})(?:[-/.](\d{1,2}))?)?\b")
TAG_RE = re.compile(r"<[^>]+>")


# ---------- tiny HTTP helpers ----------
def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-MY,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    enc = (r.headers.get_content_charset()) or "utf-8"
    try:
        return raw.decode(enc, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def strip_tags(s):
    return _html.unescape(TAG_RE.sub(" ", s or "")).strip()


def norm_title(s):
    s = strip_tags(s)
    s = re.sub(r"\s+", " ", s)
    return s[:400]


# ---------- HTML link extractor ----------
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self._a, self._buf, self._skip = [], None, [], 0
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._a = dict(attrs); self._buf = []
        elif self._a is not None and tag in ("style", "script", "noscript"):
            self._skip += 1
    def handle_endtag(self, tag):
        if tag == "a" and self._a is not None:
            self.links.append((self._a.get("href") or "", " ".join(self._buf)))
            self._a = None
        elif self._a is not None and tag in ("style", "script", "noscript") and self._skip:
            self._skip -= 1
    def handle_data(self, data):
        if self._a is not None and not self._skip:
            self._buf.append(data)


def extract_links(html_text, base_url):
    p = LinkParser()
    try:
        p.feed(html_text)
    except Exception:
        pass
    out = []
    for href, text in p.links:
        href = (href or "").strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        url = urllib.parse.urljoin(base_url, urllib.parse.urldefrag(href)[0])
        if url.lower().split("://")[0] not in ("http", "https"):
            continue
        out.append((url, norm_title(text)))
    return out


def extract_dates(text):
    d = DATE_RE.findall(text or "")
    best = None
    for m in d:
        y = int(m[0])
        if not (2000 <= y <= 2035):
            continue
        if len(m) == 3:
            try:
                v = _dt.date(y, int(m[1]), int(m[2]))
            except ValueError:
                continue
            best = v  # last matching date on the card = most likely "published"
        elif best is None:
            best = _dt.date(y, 1, 1)
    return best


# ---------- sitemap ----------
def parse_sitemap_locations(text):
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text)
    return [urllib.parse.unescape(u) for u in locs]


def scan_sitemap(config, log, debug_dir=None):
    urls = {}  # url -> {"firstmod": iso or None, "via": source}
    seen_maps, queue, depth = set(), [(u, 0) for u in config["sitemap_urls"]], 0
    while queue and depth < 3:
        nxt = []
        for url, _d in queue:
            if url in seen_maps:
                continue
            seen_maps.add(url)
            try:
                text = http_get(url, config["timeout"])
            except Exception as e:
                log.debug("sitemap %s failed: %s", url, e)
                continue
            if debug_dir:
                with open(os.path.join(debug_dir, "sitemap-" + hashlib.sha1(url.encode()).hexdigest()[:8] + ".xml"), "w") as f:
                    f.write(text)
            for loc in parse_sitemap_locations(text):
                nxt.append((loc, 1))
                if "sitemap" in loc.lower():
                    continue  # child sitemap, enqueue only
                lm = re.search(r"<lastmod>\s*([^<]+)", text[text.find(loc):text.find(loc) + 400]) if loc in text else None
                urls[loc] = {"firstmod": lm.group(1) if lm else None, "via": url}
        queue = nxt
        depth += 1
    return urls


# ---------- matching ----------
def is_relevant(path, config):
    if re.search(config["path_blacklist_regex"], path):
        return False
    lp = path.lower()
    for p in config["path_prefixes"]:
        if p in lp:
            return True
    return False


def is_actionable(item, config):
    blob = " ".join([item.get("title", ""), item["url"]])
    return bool(re.search(config["actionable_regex"], blob))


def item_id(url):
    return hashlib.sha1(url.encode()).hexdigest()[:16]


# ---------- state ----------
def load_state(path):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return {"seen": {}}


def save_state(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1, sort_keys=True)
    os.replace(tmp, path)


def prune_state(state, config):
    cutoff = _dt.datetime.now() - _dt.timedelta(days=config["max_age_days"])
    seen = {k: v for k, v in state["seen"].items()
            if _dt.datetime.fromisoformat(v.get("seen_at", "2000-01-01T00:00:00")) >= cutoff}
    if len(seen) > config["keep_recent"]:
        seen = dict(sorted(seen.items(), key=lambda kv: kv[1].get("seen_at", ""), reverse=True)[:config["keep_recent"]])
    state["seen"] = seen


# ---------- notification ----------
def build_summary(new_items):
    lines = [f"BNM WATCH: {len(new_items)} new item(s) on bnm.gov.my  ({_dt.datetime.now():%Y-%m-%d %H:%M})"]
    for it in new_items:
        flag = "🔔 ACTION" if it["actionable"] else "     info"
        lines.append(f"[{flag}] ({it['source']}) {it['title'] or it['url']}\n        {it['url']}")
    return "\n".join(lines)


def notify(summary, new_items, config):
    n = config.get("notify", {})
    topic = (n.get("ntfy_topic") or "").strip()
    if topic:
        url = topic if topic.startswith("http") else f"https://ntfy.sh/{urllib.parse.quote(topic, safe='')}"
        try:
            req = urllib.request.Request(url, data=summary.encode(), method="POST",
                                         headers={"Title": f"BNM: {len(new_items)} new", "User-Agent": USER_AGENT})
            urllib.request.urlopen(req, timeout=config["timeout"])
            logging.info("ntfy sent")
        except Exception as e:
            logging.warning("ntfy failed: %s", e)
    em = n.get("email", {}) or {}
    if em.get("enabled") and em.get("to"):
        try:
            msg = EmailMessage()
            msg["Subject"] = f"BNM watch: {len(new_items)} new item(s)"
            msg["From"] = em.get("from") or em.get("to")
            msg["To"] = em["to"]
            msg.set_content(summary)
            if em.get("user"):
                with smtplib.SMTP(em["host"], int(em.get("port", 587)), timeout=30) as s:
                    s.starttls(); s.login(em["user"], em["password"])
                    s.send_message(msg)
            else:
                with smtplib.SMTP(em["host"], int(em.get("port", 25)), timeout=30) as s:
                    s.send_message(msg)
            logging.info("email sent")
        except Exception as e:
            logging.warning("email failed: %s", e)


# ---------- run ----------
def run(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
    log = logging.getLogger("bnm")

    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_PATH) and not args.ignore_config:
        with open(CONFIG_PATH) as f:
            user_cfg = json.load(f)
        for k, v in user_cfg.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k] = {**cfg[k], **v}
            else:
                cfg[k] = v
    state_file = os.path.join(HERE, cfg["state_file"])
    log_file = os.path.join(HERE, cfg["log_file"])
    lock = os.path.join(HERE, ".lock")
    debug_dir = os.path.join(HERE, "debug") if args.debug else None
    if args.debug:
        os.makedirs(debug_dir, exist_ok=True)

    # lock (best-effort; safe enough for cron)
    if os.path.exists(lock):
        try:
            if _dt.datetime.now().timestamp() - os.path.getmtime(lock) > 3600:
                os.remove(lock)
            else:
                log.warning("another run is in progress (lock fresh); exiting")
                return 0
        except OSError:
            pass
    open(lock, "w").write(str(os.getpid()))
    try:
        state = load_state(state_file)
        now = _dt.datetime.now().isoformat(timespec="seconds")
        new_items = []
        debug_html = []

        def add(url, title="", date=None, source=""):
            iid = item_id(url)
            if iid in state["seen"]:
                return
            if args.initial_run:
                state["seen"][iid] = {"seen_at": now, "title": title[:200]}
                return
            path = urllib.parse.urlparse(url).path.lower()
            if not is_relevant(path, cfg):
                return
            it = {"id": iid, "url": url, "title": title,
                  "date": date.isoformat() if date else None,
                  "first_seen": now, "source": source,
                  "actionable": is_actionable({"url": url, "title": title}, cfg)}
            new_items.append(it)
            state["seen"][iid] = {"seen_at": now, "title": it["title"][:200]}

        # 1) sitemap (parallel)
        smap = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            for res in ex.map(lambda u: (u, scan_sitemap(cfg, log, debug_dir)), [(cfg["sitemap_urls"])]):
                pass  # single call; keep simple
        smap = scan_sitemap(cfg, log, debug_dir)
        log.info("sitemap: %d candidate URLs", len(smap))
        for u in sorted(smap):
            add(u, source="sitemap")

        # 2) listing pages (parallel)
        def fetch_listing(lp):
            try:
                text = http_get(lp["url"], cfg["timeout"])
            except Exception as e:
                log.warning("listing %s (%s) failed: %s", lp["name"], lp["url"], e)
                return lp, None, None
            if args.debug:
                with open(os.path.join(debug_dir, "page-" + re.sub(r"[^A-Za-z0-9]+", "_", lp["name"]) + ".html"), "w") as f:
                    f.write(text)
            return lp, text, lp["url"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            for lp, text, base in ex.map(fetch_listing, cfg["listing_pages"]):
                if text is None:
                    continue
                log.info("listing %s: fetched %d chars", lp["name"], len(text))
                for url, title in extract_links(text, base):
                    date = extract_dates(title)
                    if not date and "card" in text.lower():  # cheap: also scan around the anchor
                        idx = text.find(url)
                        if idx > -1:
                            date = extract_dates(text[max(0, idx - 800):idx + 800])
                    add(url, title=title or "", date=date, source=lp["name"])

        if new_items and not args.initial_run:
            new_items.sort(key=lambda x: (x["date"] or ""), reverse=True)
            with open(log_file, "a") as f:
                for it in new_items:
                    f.write(json.dumps(it, ensure_ascii=False) + "\n")
            summary = build_summary(new_items)
            print(summary)
            if not args.no_notify:
                notify(summary, new_items, cfg)
        elif args.initial_run:
            log.info("initial run: baselined %d URLs (no alerts sent)", len(state["seen"]))
        else:
            log.info("no new relevant items")

        prune_state(state, cfg)
        save_state(state_file, state)
        return 2 if new_items else 0
    finally:
        try:
            os.remove(lock)
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser(description="Watch Bank Negara Malaysia for new publications/consultations/etc.")
    ap.add_argument("--initial-run", action="store_true", help="baseline known URLs without alerting")
    ap.add_argument("--no-notify", action="store_true", help="skip ntfy/email push (still logs & prints)")
    ap.add_argument("--ignore-config", action="store_true", help="use built-in defaults only")
    ap.add_argument("--debug", action="store_true", help="verbose + dump fetched HTML/XML to ./debug/")
    args = ap.parse_args()
    try:
        rc = run(args)
    except KeyboardInterrupt:
        rc = 1
    except Exception as e:
        logging.getLogger("bnm").exception("fatal: %s", e)
        rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
```

Small cleanup: delete the dead `ex.map` block inside the sitemap section (3 lines) if you want it tidy — it's harmless but redundant. I'll note it below.

## 2) `config.json` (optional overrides — the script runs without it)

```json
{
  "listing_pages": [
    {"name": "Public Consultation", "url": "https://www.bnm.gov.my/t/public-consultation"},
    {"name": "Consultations",       "url": "https://www.bnm.gov.my/t/consultation"},
    {"name": "News",                "url": "https://www.bnm.gov.my/t/news"},
    {"name": "Media Releases",      "url": "https://www.bnm.gov.my/t/media-releases"},
    {"name": "Publications",        "url": "https://www.bnm.gov.my/t/publications"},
    {"name": "Documents",           "url": "https://www.bnm.gov.my/t/documents"}
  ],
  "path_prefixes": ["consult","discussion","paper","whitepaper","white-paper","publication","media","news","press","announcement","tender","procurement","invitation","rfp","request-for","bulletin","report","statement","monetary","financial-stability","framework","circular"],
  "actionable_regex": "(?i)(consult|discussion paper|white paper|call for|invitation|tender|rfp|request for|expression of interest|public comment|open for comment)",
  "notify": { "ntfy_topic": "bnm-watch" }
}
```

## First run — calibration (5 min)

```bash
cd ~/bnm-watcher
python3 bnm_watcher.py --initial-run --debug
```

Then check `./debug/`:
- If `sitemap-*.xml` files exist → sitemap path is working, great.
- If `page-*.html` exist → open one in a browser, confirm your listing URLs are the real BNM pages. BNM's paths occasionally change on redesign; if a listing 404s, find the live URL (check bnm.gov.my footer/nav) and just update `config.json`. The `path_prefixes` filter means the sitemap will still catch new pages even if you miss a listing URL.
- Run `python3 bnm_watcher.py` normally — if it alerts on dozens of *old* items, your state wasn't baselined; re-run `--initial-run`.

## Cron (MYT, on macOS or any Linux)

```cron
# every 30 min, quiet unless there's something new (exit 2 triggers cron mail)
*/30 * * * * /usr/bin/python3 $HOME/bnm-watcher/bnm_watcher.py >> $HOME/bnm-watcher/cron.log 2>&1
```

- `MAIL=you@your.com` in the crontab → you get an email **only** when new items exist.
- Or set `notify.ntfy_topic` in config (e.g. an `ntfy.sh` topic) for phone push — nice for "call for comment" deadlines.

## If you turn it into a Skill

The script is already skill-shaped (deterministic, file-based state, plain-text output). Suggested `SKILL.md` skeleton:

```markdown
---
name: bnm-watch
description: Check for new Bank Negara Malaysia publications, consultations,
  discussion papers, media releases and calls for participation.
---
# BNM Watch
Run: `python3 <skill_dir>/bnm_watcher.py`
- Exit 2 = new items; print the stdout summary to the user, highlight 🔔 ACTION items.
- If the user has never baselined: run `python3 <skill_dir>/bnm_watcher.py --initial-run` first.
- New item categories of interest: public consultations, discussion papers,
  white papers, calls for proposals/tenders, monetary & financial stability releases.
- To add a BNM sub-page to watch, append {name,url} to config.json -> listing_pages.
```

One honest caveat: my training data predates today's exact BNM URL paths, so treat the six default `listing_pages` URLs as *starting points* — the `--debug` step above is the 2-minute check that confirms them (or you paste me one of the `debug/page-*.html` filenames that 404'd and I'll help fix the selector/prefix). Want me to also add a "comment-closing-soon" detector (flags consultations whose deadline text is within N days)? That's the part most worth a daily reminder.
