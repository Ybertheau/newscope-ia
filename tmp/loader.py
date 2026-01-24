import yaml
from pathlib import Path

def load_dataset(dataset_dir: Path):
    articles = []

    for file in sorted(dataset_dir.glob("*.yaml")):
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            articles.extend(data.get("articles", []))

    return articles
