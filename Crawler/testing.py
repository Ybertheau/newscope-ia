import feedparser
import yaml
from pathlib import Path

# Chemin vers la racine et le YAML
PROJECT_DIR = Path(__file__).resolve().parent.parent
SOURCES_FILE = PROJECT_DIR / "crawler" / "sources.yaml"

# Charger les sources
def load_sources():
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        categories = yaml.safe_load(f)["categories"]
    sources = {}
    for cat_name, cat_data in categories.items():
        for src_id, src in cat_data["sources"].items():
            src["category"] = cat_name
            src["id"] = src_id
            sources[src_id] = src
    return sources

# Tester chaque flux RSS
def test_rss():
    sources = load_sources()

    for src_id, source in sources.items():
        rss = source["rss"]
        print(f"\n{source['name']} ({src_id})")
        if isinstance(rss, list):
            # Plusieurs flux possibles
            for url in rss:
                feed = feedparser.parse(url)
                print(f"Flux : {url} → {len(feed.entries)} articles")
                for entry in feed.entries[:5]:
                    print(f" - {entry.title}")
        else:
            feed = feedparser.parse(rss)
            print(f"Flux : {rss} → {len(feed.entries)} articles")
            for entry in feed.entries[:5]:
                print(f" - {entry.title}")

if __name__ == "__main__":
    test_rss()
