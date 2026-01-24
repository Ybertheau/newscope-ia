import re

STOPWORDS_FR = set("""
au aux avec ce ces dans de des du elle en et eux il je la le leur lui ma mais me même mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses son sur ta te tes toi ton tu un une vos votre vous
""".split())

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ\s]", " ", text)
    tokens = [
        w for w in text.split()
        if w not in STOPWORDS_FR and len(w) > 2
    ]
    return " ".join(tokens)

def build_corpus(articles):
    corpus = []
    for a in articles:
        text = f"{a.get('title','')} {a.get('summary','')}"
        corpus.append(clean_text(text))
    return corpus
