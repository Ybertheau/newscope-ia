import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def split_sentences(text: str):
    return re.split(r'(?<=[.!?])\s+', text)

def summarize_cluster(texts, max_sentences=3):
    full_text = " ".join(texts)
    sentences = split_sentences(full_text)

    if len(sentences) <= max_sentences:
        return sentences

    vectorizer = TfidfVectorizer(stop_words=None)
    X = vectorizer.fit_transform(sentences)

    scores = X.sum(axis=1).A1
    ranked = np.argsort(scores)[::-1][:max_sentences]

    summary = [sentences[i] for i in sorted(ranked)]
    return summary
