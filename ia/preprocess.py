import re

# =====================
# STOPWORDS
# =====================
STOPWORDS_FR = set("""
au aux avec ce ces dans de des du elle en et eux il je la le leur lui ma mais me même mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses son sur ta te tes toi ton tu un une vos votre vous
""".split())

STOPWORDS_MEDIA = set("""
article réservé abonnés abonnement connectez connexion lire suite
recevez essentiel actualité rubriques services journaux magazines
live direct édition newsletter publié mis jour figaro lefigaro lemonde liberation libération franceinfo
le monde l equipe lequipe 20minutes 20 minutes ouestfrance ouest france sudouest sud ouest courrierinternational courrier international
""".split())

STOPWORDS_TIME = set("""
aujourd aujourd'hui hier demain lundi mardi mercredi jeudi vendredi
janvier février mars avril mai juin juillet août septembre octobre novembre décembre
""".split())

STOPWORDS_NOISE = set("""
temps lecture min minute minutes lire voir savoir
sans paiement paiement gratuit compte créez creer
essentiel actualites journal journaux
""".split())

ALL_STOPWORDS = STOPWORDS_FR | STOPWORDS_MEDIA | STOPWORDS_TIME | STOPWORDS_NOISE

# =====================
# PHRASES À SUPPRIMER (BRUIT FORT)
# =====================
BLACKLIST_PHRASES = [
    "article réservé aux abonnés",
    "connectez-vous pour lire",
    "recevez l'essentiel de l'actualité",
    "rubriques et services",
    "nos journaux et magazines",
    "mis à jour le",
    "publié le",
    "temps de lecture",
    "lecture min",
    "sans paiement",
    "créez un compte",
]

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

    # Dates (ex: 25 janvier 2026, 2026-01-25)
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
