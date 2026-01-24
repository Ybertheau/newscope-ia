import feedparser
import yaml
from pathlib import Path
from datetime import datetime
from time import mktime

# Chemin vers la racine et le YAML
PROJECT_DIR = Path(__file__).resolve().parent.parent
SOURCES_FILE = PROJECT_DIR / "config" / "sources.yaml"

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

# Extraire une date de publication même si published_parsed est absent
def get_published(entry):
    # Si published_parsed existe
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    # Sinon essayer de parser published en string
    elif hasattr(entry, "published") and entry.published:
        try:
            # feedparser a déjà une fonction pour parser les dates
            time_struct = feedparser._parse_date(entry.published)
            if time_struct:
                return datetime(*time_struct[:6])
        except Exception:
            return None
    return None

# Tester chaque flux RSS
def test_rss():
    sources = load_sources()
    all_ok = True

    for src_id, source in sources.items():
        rss = source["rss"]
        print(f"\n{source['name']} ({src_id})")

        rss_list = rss if isinstance(rss, list) else [rss]

        for url in rss_list:
            feed = feedparser.parse(url)
            n_articles = len(feed.entries)
            print(f"Flux : {url} → {n_articles} articles")

            recent_articles = 0
            for entry in feed.entries[:5]:
                pub_date = get_published(entry)
                pub_str = pub_date.isoformat() if pub_date else "no date"
                print(f" - {entry.title} | {pub_str}")
                if pub_date and (datetime.now() - pub_date).days <= 5:
                    recent_articles += 1

            if recent_articles == 0:
                print(f"Aucun article récent pour ce flux")
                # Ici, tu peux choisir de ne pas bloquer
                # all_ok = False

    return all_ok


if __name__ == "__main__":
    test_rss()
