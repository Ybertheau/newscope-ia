import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

def score_volume(count, max_count):
    return count / max_count

def score_sources(articles):
    sources = {a["source"] for a in articles}
    return len(sources) / len(articles)

def score_recency(articles, decay_days=3):
    now = datetime.now()
    scores = []

    for a in articles:
        try:
            published = datetime.fromisoformat(a["published"])
            age_days = (now - published).days
            scores.append(max(0, 1 - age_days / decay_days))
        except:
            continue

    return sum(scores) / len(scores) if scores else 0

def score_coherence(X_cluster):
    if X_cluster.shape[0] < 2:
        return 0

    sim = cosine_similarity(X_cluster)
    return np.mean(sim[np.triu_indices_from(sim, k=1)])

def compute_topic_score(
    topic,
    X,
    indices,
    max_count
):
    volume = score_volume(topic["count"], max_count)
    sources = score_sources(topic["articles"])
    recency = score_recency(topic["articles"])
    coherence = score_coherence(X[indices])

    score = (
        0.4 * volume +
        0.3 * sources +
        0.2 * recency +
        0.1 * coherence
    )

    return {
        "total": round(score, 3),
        "volume": round(volume, 3),
        "sources": round(sources, 3),
        "recency": round(recency, 3),
        "coherence": round(coherence, 3)
    }

def extract_topics(articles, labels, model, vectorizer, X):
    topics = {}
    terms = vectorizer.get_feature_names_out()
    max_count = max(np.bincount(labels))

    for topic_idx in range(model.n_clusters):
        indices = np.where(labels == topic_idx)[0]
        if len(indices) == 0:
            continue

        centroid = model.cluster_centers_[topic_idx]
        keywords = [
            terms[i] for i in centroid.argsort()[-10:][::-1]
        ]

        topic_articles = [articles[i] for i in indices]

        topics[topic_idx] = {
            "count": len(indices),
            "keywords": keywords,
            "articles": topic_articles,
            "score": compute_topic_score(
                {"count": len(indices), "articles": topic_articles},
                X,
                indices,
                max_count
            )
        }

    return topics

    return topics