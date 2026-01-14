from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re

# =========================
# DATE FILTER
# =========================
def is_recent(published_parsed, days=5):
    try:
        date = datetime(*published_parsed[:6])
        return datetime.now() - date <= timedelta(days=days)
    except Exception:
        return False

# =========================
# PAYWALL HEURISTIC
# =========================
def detect_paywall(url):
    keywords = ["abonne", "abonnement", "premium", "subscribe", "paywall"]
    return any(k in url.lower() for k in keywords)

# =========================
# SIMPLE SUMMARY PAR SOURCE
# =========================
def extract_summary(url, source_domain=None, max_chars=500):
    """
    Extrait un résumé depuis la page si elle appartient à la source déclarée
    """
    try:
        # Vérification rapide du domaine
        if source_domain and source_domain not in url:
            return ""

        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Récupérer le texte principal simple
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        text = clean_text(text)

        return text[:max_chars]

    except Exception:
        return ""

# =========================
# TEXT CLEANING
# =========================
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()
