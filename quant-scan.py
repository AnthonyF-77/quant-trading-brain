#!/usr/bin/env python3
import sys, os
from pathlib import Path

vault = Path(__file__).parent
os.environ.setdefault("OBSIDIAN_VAULT_PATH", str(vault))
sys.path.insert(0, str(vault / "scraper"))

from run_scan import main

if __name__ == "__main__":
    main()
