import streamlit as st
import yaml
from pathlib import Path
from math import ceil

# Définition des chemins
PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_ROOT / "dataset"
OUTPUT_DIR = PROJECT_ROOT / "output"

ARTICLES_PER_PAGE = 10

# Configuration de la page
st.set_page_config(
    page_title="Newscope-IA",
    layout="wide"
)
st.title("Newscope-IA")
st.caption("Analyse automatique de l'actualité")
tab_dataset, tab_ai = st.tabs(["Dataset", "Analyse IA"])

# ======================
# Onglet Dataset
# ======================
with tab_dataset:
    st.header("Articles collectés")

    dataset_files = sorted(DATASET_DIR.glob("*.yaml"))
    if not dataset_files:
        st.warning("Aucun dataset disponible")
        st.stop()

    selected_dataset = st.selectbox(
        "Sélectionner un dataset",
        [f.name for f in dataset_files],
        index=len(dataset_files) - 1
    )

    dataset_path = DATASET_DIR / selected_dataset
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    articles = data.get("articles", [])
    st.write(f"{len(articles)} articles")

    sources = sorted(set(a["source"] for a in articles))
    selected_sources = st.multiselect(
        "Filtrer par source",
        sources,
        default=sources
    )

    filtered_articles = [a for a in articles if a["source"] in selected_sources]

    # Pagination
    total_pages = ceil(len(filtered_articles) / ARTICLES_PER_PAGE)
    page = st.session_state.get("dataset_page", 1)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if st.button("◀ Précédent") and page > 1:
            page -= 1
    with col3:
        if st.button("Suivant ▶") and page < total_pages:
            page += 1

    st.session_state["dataset_page"] = page
    st.write(f"Page {page}/{total_pages}")

    start = (page-1)*ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE
    for article in filtered_articles[start:end]:
        with st.expander(article["title"]):
            st.markdown(f"**Source :** {article['source']}")
            st.markdown(f"**Date :** {article['published']}")
            st.markdown(f"**Catégorie :** {article['category']}")
            st.markdown(f"[Lire l'article]({article['url']})")

            if article.get("is_paywalled"):
                st.warning("Article potentiellement payant")

            if article.get("summary"):
                st.markdown("**Résumé :**")
                st.write(article["summary"])

# ======================
# Onglet Analyse IA
# ======================
with tab_ai:
    topic_files = sorted(OUTPUT_DIR.glob("topics_*.yaml"))

    if not topic_files:
        st.warning("Aucun résultat IA disponible")
        st.stop()

    latest_topics = topic_files[-1]

    with open(latest_topics, "r", encoding="utf-8") as f:
        topics_data = yaml.safe_load(f)

    st.subheader(f"Analyse IA : {latest_topics.name}")

    for i, topic in enumerate(topics_data.get("topics", []), start=1):
        st.markdown(f"## Sujet {i}")
        st.markdown(f"**Thème dominant :** {topic.get('label', 'n/a')}")
        st.markdown(f"**Score :** {topic.get('score', 0):.2f}")
        st.markdown(f"**Résumé global :** {topic.get('summary', '')}")
        st.markdown(f"**Mots-clés :** {', '.join(topic.get('keywords', []))}")
        st.markdown(f"**Nombre d'articles :** {topic.get('articles_count', len(topic.get('articles', [])))}")

        articles = topic.get("articles", [])
        total_pages = ceil(len(articles)/ARTICLES_PER_PAGE)
        page_key = f"topic_page_{i}"
        page = st.session_state.get(page_key, 1)

        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            if st.button(f"◀ Précédent {i}") and page > 1:
                page -= 1
        with col3:
            if st.button(f"Suivant ▶ {i}") and page < total_pages:
                page += 1

        st.session_state[page_key] = page
        st.write(f"Page {page}/{total_pages}")

        start = (page-1)*ARTICLES_PER_PAGE
        end = start + ARTICLES_PER_PAGE
        st.markdown("### Articles liés")
        for art in articles[start:end]:
            st.markdown(
                f"- [{art['title']}]({art['url']}) "
                f"({art['source']} – {art.get('published', 'date inconnue')})"
            )
