"""arXiv q-fin scraper — fetches recent papers from all q-fin categories."""
import os
import json
import time
import arxiv
from datetime import datetime, timezone
from pathlib import Path
from dateutil import parser as dtparser

CATEGORIES = {
    "q-fin.GN": "General Finance",
    "q-fin.ST": "Statistical Finance",
    "q-fin.TR": "Trading and Market Microstructure",
    "q-fin.PM": "Portfolio Management",
    "q-fin.RM": "Risk Management",
    "q-fin.PR": "Pricing of Securities",
}

DAYS_BACK = 7
VAULT_PATH = Path(os.environ.get("OBSIDIAN_VAULT_PATH", str(Path(__file__).parent.parent)))


def fetch_all():
    """Fetch recent papers from all q-fin categories."""
    results = []
    cutoff = datetime.now(timezone.utc).timestamp() - DAYS_BACK * 86400

    client = arxiv.Client()
    out_dir = VAULT_PATH / "sources" / "00_Inbox"
    out_dir.mkdir(parents=True, exist_ok=True)

    for cat, name in CATEGORIES.items():
        print(f"[arXiv] Fetching {cat} ({name})...")
        try:
            search = arxiv.Search(
                query=f"cat:{cat}",
                max_results=20,
                sort_by=arxiv.SortCriterion.SubmittedDate,
            )
            papers = list(client.results(search))

            cat_results = []
            for p in papers:
                submitted = p.published.datetime()
                if submitted.timestamp() < cutoff:
                    continue

                pdf_url = p.entry_id
                arxiv_id = p.entry_id.split("/")[-1]

                item = {
                    "title": p.title,
                    "authors": [a.name for a in p.authors],
                    "abstract": p.summary,
                    "categories": list(p.categories),
                    "published": p.published.isoformat(),
                    "pdf_url": pdf_url,
                    "arxiv_id": arxiv_id,
                    "comment": p.comment or "",
                    "journal_ref": p.journal_ref or "",
                    "doi": p.doi or "",
                    "source": "arXiv",
                    "subcategory": cat,
                }

                filename = f"arxiv_{arxiv_id}.json"
                out_file = out_dir / filename
                if not out_file.exists():
                    out_file.write_text(json.dumps(item, indent=2, ensure_ascii=False))
                cat_results.append(item)

            results.extend(cat_results)
            print(f"  -> {len(cat_results)} new papers")
            time.sleep(1)

        except Exception as e:
            print(f"  -> ERROR: {e}")

    return results


if __name__ == "__main__":
    results = fetch_all()
    print(f"\nTotal: {len(results)} papers saved to inbox")
