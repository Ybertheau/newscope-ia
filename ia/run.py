from pathlib import Path
from ia.loader import load_dataset
from ia.preprocess import build_corpus
from ia.clustering import cluster_articles
from ia.topics import extract_topics
from ia.export import export_topics


def run_ia():
    dataset_dir = Path("dataset")
    output_dir = Path("output")

    # Créer le dossier output s'il n'existe pas
    output_dir.mkdir(exist_ok=True)

    # 1. Charger dataset
    articles = load_dataset(dataset_dir)
    print(f"{len(articles)} articles chargés")

    if not articles:
        print("Aucun article à analyser")
        return

    # 2. Préprocessing
    corpus = build_corpus(articles)

    # 3. Clustering
    labels, model, vectorizer, X = cluster_articles(
        corpus,
        n_topics=10
    )

    # 4. Extraction des sujets + scoring
    topics = extract_topics(
        articles=articles,
        labels=labels,
        model=model,
        vectorizer=vectorizer,
        X=X
    )

    # 5. Export YAML
    export_topics(
        topics=topics,
        output_dir=output_dir
    )

    print("Résultats IA exportés dans /output")
