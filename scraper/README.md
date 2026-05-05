# Quant Trading Brain Scraper

Quant research content scraper for arXiv, RSS feeds, and GitHub.
Writes raw content to sources/00_Inbox/ for later OpenCode processing.

## Setup

```bash
pip install -r requirements.txt
python -m scraper.main
```

## Environment Variables

- `OBSIDIAN_VAULT_PATH` — path to the vault root (default: ../ from scraper dir)
- `GEMINI_API_KEY` — optional, for AI content scoring
- `OPENAI_API_KEY` — optional, fallback for AI scoring

## Sources

- arXiv q-fin (all categories)
- RSS: QuantInsti, PyQuant News, QuantStart, Binance Research
- GitHub trending in finance/python
