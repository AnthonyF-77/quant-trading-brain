"""RSS feed scraper for quant blogs and research sites."""
import os
import json
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from pathlib import Path
from dateutil import parser as dtparser
from urllib.parse import urlparse

FEEDS = [
    {
        "name": "QuantInsti",
        "url": "https://blog.quantinsti.com/feed/",
        "category": "Strategy",
    },
    {
        "name": "PyQuant News",
        "url": "https://www.pyquantnews.com/feed",
        "category": "General",
    },
    {
        "name": "QuantStart",
        "url": "https://www.quantstart.com/feed/",
        "category": "General",
    },
    {
        "name": "Quantpedia",
        "url": "https://quantpedia.com/blog/",
        "category": "Strategy",
    },
    {
        "name": "Binance Research",
        "url": "https://www.binance.com/en/research/feed",
        "category": "Crypto",
    },
]

DAYS_BACK = 7
VAULT_PATH = Path(os.environ.get("OBSIDIAN_VAULT_PATH", str(Path(__file__).parent.parent.parent)))


def fetch_article_content(url: str) -> str:
    """Extract article text from URL."""
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return ""
        soup = BeautifulSoup(resp.text, "lxml")
        for tag in ["script", "style", "nav", "footer", "header", "aside"]:
            for el in soup.find_all(tag):
                el.decompose()
        article = soup.find("article") or soup.find("main") or soup
        return article.get_text(separator=" ", strip=True)[:5000]
    except Exception:
        return ""


def fetch_all():
    """Fetch recent items from all RSS feeds."""
    results = []
    cutoff = datetime.now(timezone.utc).timestamp() - DAYS_BACK * 86400
    out_dir = VAULT_PATH / "sources" / "00_Inbox"
    out_dir.mkdir(parents=True, exist_ok=True)

    for feed in FEEDS:
        print(f"[RSS] Fetching {feed['name']}...")
        try:
            fp = feedparser.parse(feed["url"])
            count = 0
            for entry in fp.entries[:20]:
                published_ts = None
                if entry.get("published_parsed"):
                    try:
                        import time
                        published_ts = time.mktime(entry.published_parsed)
                    except Exception:
                        pass

                if published_ts and published_ts < cutoff:
                    continue

                url = entry.get("link") or entry.get("id", "")
                if not url:
                    continue

                domain = urlparse(url).netloc.replace("www.", "")

                item = {
                    "title": entry.get("title", ""),
                    "url": url,
                    "summary": entry.get("summary", "")[:1000],
                    "published": entry.get("published", ""),
                    "author": entry.get("author", ""),
                    "source": feed["name"],
                    "category": feed["category"],
                    "domain": domain,
                    "source_type": "rss",
                }

                slug = domain.replace(".", "_") + "_" + entry.get("id", "").split("/")[-1][:50]
                slug = "".join(c if c.isalnum() else "_" for c in slug)
                filename = f"rss_{slug}.json"
                out_file = out_dir / filename

                if not out_file.exists():
                    content = fetch_article_content(url)
                    item["content"] = content
                    out_file.write_text(json.dumps(item, indent=2, ensure_ascii=False))

                count += 1

            results.append({"feed": feed["name"], "count": count})
            print(f"  -> {count} items")
            import time; time.sleep(0.5)

        except Exception as e:
            print(f"  -> ERROR: {e}")

    return results


if __name__ == "__main__":
    results = fetch_all()
    print(f"\nDone: {len(results)} feeds processed")
