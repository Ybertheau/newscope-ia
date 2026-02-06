import re
import yaml
from pathlib import Path

# =====================
# CONFIG
# =====================
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "stopwords.yaml"

# =====================
# LOAD STOPWORDS
# =====================
def load_stopwords():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Fichier stopwords introuvable : {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    stopwords = set()
    for group in config.get("stopwords", {}).values():
        stopwords.update(w.strip().lower() for w in group)

    blacklist_phrases = [
        p.strip().lower()
        for p in config.get("blacklist_phrases", [])
    ]

    return stopwords, blacklist_phrases


# Chargement global (une seule fois)
ALL_STOPWORDS, BLACKLIST_PHRASES = load_stopwords()

# =====================
# CLEAN TEXT
# =====================
def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    # Suppression phrases presse
    for phrase in BLACKLIST_PHRASES:
        text = text.replace(phrase, " ")

    # URLs
    text = re.sub(r"http\S+", " ", text)

    # Dates
    text = re.sub(r"\b\d{1,2}\s+\w+\s+\d{4}\b", " ", text)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " ", text)

    # Nettoyage caractères
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", " ", text)

    tokens = [
        w for w in text.split()
        if w not in ALL_STOPWORDS and len(w) > 2
    ]

    return " ".join(tokens)

# =====================
# CORPUS
# =====================
def build_corpus(articles):
    corpus = []
    for a in articles:
        text = f"{a.get('title','')} {a.get('summary','')}"
        corpus.append(clean_text(text))
    return corpus
