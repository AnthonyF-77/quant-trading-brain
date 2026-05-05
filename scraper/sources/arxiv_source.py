"""arXiv q-fin scraper — fetches recent papers from all q-fin categories."""
import os
import json
import time
import requests
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

CATEGORIES = {
    "q-fin.GN": "General Finance",
    "q-fin.ST": "Statistical Finance",
    "q-fin.TR": "Trading and Market Microstructure",
    "q-fin.PM": "Portfolio Management",
    "q-fin.RM": "Risk Management",
    "q-fin.PR": "Pricing of Securities",
}

DAYS_BACK = 7
MAX_RESULTS = 15
VAULT_PATH = Path(os.environ.get("OBSIDIAN_VAULT_PATH", str(Path(__file__).parent.parent)))


def fetch_all():
    """Fetch recent papers from all q-fin categories using arXiv API."""
    results = []
    cutoff_dt = datetime.now(timezone.utc).timestamp() - DAYS_BACK * 86400
    out_dir = VAULT_PATH / "sources" / "00_Inbox"
    out_dir.mkdir(parents=True, exist_ok=True)

    for cat, name in CATEGORIES.items():
        print(f"[arXiv] Fetching {cat} ({name})...")
        try:
            params = {
                "search_query": f"cat:{cat}",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "start": 0,
                "max_results": MAX_RESULTS,
            }
            url = "https://export.arxiv.org/api/query?" + urlencode(params)
            resp = requests.get(url, timeout=30, allow_redirects=True,
                                headers={"User-Agent": "quant-trading-brain/1.0"})

            if resp.status_code != 200:
                print(f"  -> HTTP {resp.status_code}: {resp.text[:200]}")
                time.sleep(2)
                continue

            papers = _parse_atom_feed(resp.text)
            new_count = 0

            for p in papers:
                try:
                    published_ts = _parse_arxiv_date(p.get("published", ""))
                    if published_ts < cutoff_dt:
                        continue
                except Exception:
                    continue

                arxiv_id = p.get("id", "").split("/")[-1]
                if not arxiv_id:
                    continue

                item = {
                    "title": p.get("title", "").replace("\n", " ").strip(),
                    "authors": p.get("authors", []),
                    "abstract": p.get("summary", "").replace("\n", " ").strip(),
                    "categories": [cat],
                    "published": p.get("published", ""),
                    "pdf_url": p.get("id", "").replace("/abs/", "/pdf/") + ".pdf",
                    "arxiv_id": arxiv_id,
                    "source": "arXiv",
                    "subcategory": cat,
                }

                filename = f"arxiv_{arxiv_id}.json"
                out_file = out_dir / filename
                if not out_file.exists():
                    out_file.write_text(json.dumps(item, indent=2, ensure_ascii=False))
                    new_count += 1

            print(f"  -> {new_count} new papers")
            time.sleep(2)

        except Exception as e:
            print(f"  -> ERROR: {e}")

    return results


def _parse_atom_feed(xml_text: str) -> list[dict]:
    """Parse arXiv Atom feed into list of paper dicts."""
    papers = []
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return papers

    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

    for entry in root.findall("atom:entry", ns):
        def get_text(tag, fallback=None):
            el = entry.find(f"atom:{tag}", ns)
            return el.text.strip() if el is not None and el.text else (fallback or "")

        authors = [a.find("atom:name", ns).text
                   for a in entry.findall("atom:author", ns)
                   if a.find("atom:name", ns) is not None and a.find("atom:name", ns).text]

        papers.append({
            "id": get_text("id"),
            "title": get_text("title"),
            "summary": get_text("summary"),
            "published": get_text("published"),
            "authors": authors,
        })

    return papers


def _parse_arxiv_date(date_str: str) -> float:
    """Parse arXiv date string (ISO 8601) to Unix timestamp."""
    from dateutil.parser import isoparse
    return isoparse(date_str).timestamp()


if __name__ == "__main__":
    results = fetch_all()
    print(f"\nTotal papers processed")
