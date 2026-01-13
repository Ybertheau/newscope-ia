from datetime import datetime, timedelta
from newspaper import Article
import re

def is_recent(date_str, days=5):
    try:
        date = datetime(*date_str[:6])
        return datetime.now() - date <= timedelta(days=days)
    except:
        return False

def detect_paywall(url):
    keywords = ["abonne", "premium", "subscribe", "paywall"]
    return any(k in url.lower() for k in keywords)

def extract_summary(url):
    try:
        article = Article(url, language="fr")
        article.download()
        article.parse()
        article.nlp()
        return article.summary[:500]
    except:
        return ""
