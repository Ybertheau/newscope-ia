import feedparser
import json
from datetime import datetime
from sources import SOURCES
from utils import is_recent, detect_paywall, extract_summary

OUTPUT_PATH = "data/articles.json"

def crawl():
    articles = []

    for source in SOURCES.values():
        feed = feedparser.parse(source["rss"])

        for entry in feed.entries:
            if not hasattr(entry, "published_parsed"):
                continue

            if not is_recent(entry.published_parsed):
                continue

            url = entry.link

            article = {
                "title": entry.title,
                "source": source["name"],
                "url": url,
                "published": datetime(*entry.published_parsed[:6]).isoformat(),
                "is_paywalled": detect_paywall(url),
                "summary": extract_summary(url),
                "category": source["category"]
            }

            articles.append(article)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"{len(articles)} articles collectés")

if __name__ == "__main__":
    crawl()
