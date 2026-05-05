#!/usr/bin/env python3
"""
Quant Trading Brain — Scraper Main
Fetches content from all sources and writes to 00_Inbox.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sources.arxiv_source import fetch as fetch_arxiv
from sources.rss_source import fetch as fetch_rss


def main():
    vault_path = os.environ.get("OBSIDIAN_VAULT_PATH")
    if vault_path:
        os.environ["OBSIDIAN_VAULT_PATH"] = str(Path(vault_path).resolve())

    print("=" * 60)
    print("Quant Trading Brain — Daily Scrape")
    print("=" * 60)

    arxiv_results = fetch_arxiv()
    print()

    rss_results = fetch_rss()
    print()

    inbox_count = len(list(Path(os.environ.get("OBSIDIAN_VAULT_PATH", str(Path(__file__).parent.parent)) / "sources" / "00_Inbox").glob("*.json")))
    print(f"Done. Inbox now has {inbox_count} items.")


if __name__ == "__main__":
    main()
