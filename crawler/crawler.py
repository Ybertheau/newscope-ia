import feedparser
import yaml
from datetime import datetime
from crawler.utils import is_recent, detect_paywall, extract_summary
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SOURCES_FILE = PROJECT_DIR / "config" / "sources.yaml"
SETTINGS_FILE = PROJECT_DIR / "config" / "settings.yaml"
DATASET_DIR = PROJECT_DIR / "dataset"

# ======================
# Charger settings
# ======================
def load_settings():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = yaml.safe_load(f)
        return settings.get("crawler", {})
    return {}

# ======================
# Charger sources depuis YAML
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
def crawl(max_articles_override: int = None):
    settings = load_settings()
    MAX_ARTICLES_PER_SOURCE = max_articles_override or settings.get("max_articles_per_source", 10)

    sources = load_sources()
    articles = []

    for src_id, source in sources.items():
        feed = feedparser.parse(source["rss"])
        count = 0

        for entry in feed.entries:
            if MAX_ARTICLES_PER_SOURCE and count >= MAX_ARTICLES_PER_SOURCE:
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

    DATASET_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = DATASET_DIR / f"{today}.yaml"

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump({"articles": articles}, f, allow_unicode=True, sort_keys=False)

    print(f"{len(articles)} articles collectés (limite par source = {MAX_ARTICLES_PER_SOURCE}) et stockés dans {output_file}")


if __name__ == "__main__":
    crawl()
