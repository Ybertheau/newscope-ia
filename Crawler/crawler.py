import feedparser
import yaml
from datetime import datetime
from crawler.utils import is_recent, detect_paywall, extract_summary
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent  # remonte de crawler/ → racine
SOURCES_FILE = PROJECT_DIR / "config" / "sources.yaml"
DATASET_DIR = PROJECT_DIR / "dataset"
MAX_ARTICLES_PER_SOURCE = 10  # limite pour chaque journal

# ======================
# Charger les sources depuis YAML
# ======================
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

# ======================
# Crawler
# ======================
def crawl():
    sources = load_sources()
    articles = []

    for src_id, source in sources.items():
        feed = feedparser.parse(source["rss"])
        count = 0

        for entry in feed.entries:
            if count >= MAX_ARTICLES_PER_SOURCE:
                break
            if not hasattr(entry, "published_parsed"):
                continue
            if not is_recent(entry.published_parsed):
                continue

            url = entry.link

            article = {
                "title": entry.title,
                "source": source["name"],
                "source_id": src_id,
                "url": url,
                "published": datetime(*entry.published_parsed[:6]).isoformat(),
                "is_paywalled": detect_paywall(url),
                "summary": extract_summary(url, source_domain=source["rss"].split("/")[2]),
                "category": source["category"]
            }

            articles.append(article)
            count += 1

    # ======================
    # Préparer le dossier dataset
    # ======================
    DATASET_DIR.mkdir(exist_ok=True)

    # Fichier par date
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = DATASET_DIR / f"{today}.yaml"

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump({"articles": articles}, f, allow_unicode=True, sort_keys=False)

    print(f"{len(articles)} articles collectés et stockés dans {output_file}")


if __name__ == "__main__":
    crawl()
