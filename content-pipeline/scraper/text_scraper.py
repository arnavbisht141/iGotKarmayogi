import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from scrapling.fetchers import Fetcher

from common.config import BASE_DIR, load_fields

# Topics where free-text Wikipedia search resolves to the wrong article
# (ambiguous acronyms, short names) — exact known-good titles instead.
WIKI_TITLE_OVERRIDES = {
    "survey-design": "Survey methodology",
    "sampling": "Sampling (statistics)",
    "price-statistics": "Price index",
    "python": "Python (programming language)",
    "r": "R (programming language)",
    "sql": "SQL",
    "stata": "Stata",
    "spss": "SPSS",
    "sas": "SAS (software)",
    "gis": "Geographic information system",
    "ai-ml": "Machine learning",
    "apis": "API",
    "cybersecurity": "Computer security",
}


def find_wikipedia_title(topic_name: str) -> str | None:
    params = urllib.parse.urlencode({
        "action": "query", "list": "search", "srsearch": topic_name,
        "format": "json", "srlimit": 1,
    })
    req = urllib.request.Request(
        f"https://en.wikipedia.org/w/api.php?{params}",
        headers={"User-Agent": "competency-content-pipeline/1.0"},
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            results = data.get("query", {}).get("search", [])
            return results[0]["title"] if results else None
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 2:
                time.sleep(3 * (attempt + 1))
                continue
            raise
    return None


def fetch_wikipedia_text(topic_name: str, wiki_title: str | None = None) -> tuple[str, str, str] | None:
    resolved_title = wiki_title or find_wikipedia_title(topic_name) or topic_name
    url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(resolved_title.replace(' ', '_'))}"
    page = Fetcher.get(url)
    if page.status != 200:
        return None

    title_els = page.css("h1#firstHeading .mw-page-title-main")
    title = title_els[0].text.strip() if title_els else topic_name

    paragraphs = page.css("div.mw-parser-output p")
    body = "\n\n".join(p.text.strip() for p in paragraphs if p.text and p.text.strip())
    if not body:
        return None

    return title, url, body


def save_article(field_slug: str, topic_slug: str, topic_name: str, force: bool = False) -> Path | None:
    out_dir = BASE_DIR / "content" / field_slug / topic_slug / "articles"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "wikipedia.md"

    if out_path.exists() and not force:
        return out_path

    result = fetch_wikipedia_text(topic_name, wiki_title=WIKI_TITLE_OVERRIDES.get(topic_slug))
    if result is None:
        return None

    title, url, body = result
    out_path.write_text(f"Title: {title}\nSource: {url}\n\n{body}")
    return out_path


def main(force: bool = False, fields: list | None = None) -> None:
    for field in fields if fields is not None else load_fields():
        for topic in field.topics:
            try:
                path = save_article(field.slug, topic.slug, topic.name, force=force)
                print(f"wrote {path}" if path else f"skipped (no content): {field.slug}/{topic.slug}")
            except Exception as exc:
                print(f"skipped (error: {exc}): {field.slug}/{topic.slug}")
            time.sleep(0.5)


if __name__ == "__main__":
    main(force="--force" in sys.argv)
