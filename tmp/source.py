from pathlib import Path
import yaml

PROJECT_DIR = Path(__file__).resolve().parent.parent
SOURCES_FILE = PROJECT_DIR / "config" / "sources.yaml"

def load_sources():
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["categories"]