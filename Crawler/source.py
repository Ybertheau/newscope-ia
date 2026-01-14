import yaml

SOURCES_FILE = "sources.yaml"

def load_sources():
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["categories"]