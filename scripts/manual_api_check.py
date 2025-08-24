#!/usr/bin/env python3
"""Manual API updates check with optional RSS feed monitoring."""
import requests
from xml.etree import ElementTree
from pathlib import Path
import sys

# Ensure scripts directory and src are on path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR.parent / 'src'))

from daily_api_check import APIUpdateChecker  # type: ignore

# RSS feeds for provider status/announcements
RSS_FEEDS = {
    "openai": "https://status.openai.com/history.rss",
    "anthropic": "https://status.anthropic.com/history.rss",
    "google": "https://status.cloud.google.com/feed.atom",
}

def check_rss_feeds() -> None:
    """Fetch latest entry from each provider RSS feed."""
    print("\n🔔 Checking provider RSS feeds for announcements...")
    for provider, url in RSS_FEEDS.items():
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                print(f"  ⚠️ {provider} feed error: {resp.status_code}")
                continue
            root = ElementTree.fromstring(resp.content)
            # RSS uses item, Atom uses entry
            item = root.find('.//item') or root.find('.//{http://www.w3.org/2005/Atom}entry')
            if item is not None:
                title = item.findtext('title') or item.findtext('{http://www.w3.org/2005/Atom}title', default='No title')
                pub_date = item.findtext('pubDate') or item.findtext('{http://www.w3.org/2005/Atom}updated', default='Unknown date')
                print(f"  📰 {provider}: {title.strip()} ({pub_date.strip()})")
            else:
                print(f"  ℹ️ {provider}: no feed items found")
        except Exception as exc:
            print(f"  ❌ {provider} feed check failed: {exc}")
    print()

def main() -> None:
    check_rss_feeds()
    checker = APIUpdateChecker()
    checker.run_full_check()

if __name__ == "__main__":
    main()
