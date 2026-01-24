from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_articles(corpus, n_topics=10):
    vectorizer = TfidfVectorizer(
        max_df=0.8,
        min_df=2,
        ngram_range=(1, 2)
    )

    X = vectorizer.fit_transform(corpus)

    model = KMeans(
        n_clusters=n_topics,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X)

    return labels, model, vectorizer, X
