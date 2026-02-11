from datetime import datetime
import streamlit as st
import yaml
from pathlib import Path
from math import ceil

# ======================
# CONFIG
# ======================

PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_ROOT / "dataset"
OUTPUT_DIR = PROJECT_ROOT / "output"

ARTICLES_PER_PAGE = 10

st.set_page_config(
    page_title="Newscope-IA",
    layout="wide"
)

st.title("Newscope-IA")
st.caption("Analyse automatique de l'actualité")

tab_ai, tab_dataset = st.tabs([" Analyse IA", " Dataset"])

# =====================================================
#  ONGLET ANALYSE IA
# =====================================================

with tab_ai:

    st.header("Analyse des topics IA")

    topic_files = sorted(OUTPUT_DIR.glob("topics_*.yaml"))

    if not topic_files:
        st.warning("Aucun résultat IA disponible")
        st.stop()

    selected_topic_file = st.selectbox(
        "Sélectionner un topic par date",
        [f.name for f in topic_files],
        index=len(topic_files) - 1,
        key="ai_file_selector"
    )

    topic_path = OUTPUT_DIR / selected_topic_file

    with open(topic_path, "r", encoding="utf-8") as f:
        topics_data = yaml.safe_load(f)

    topics = topics_data.get("topics", [])

    if not topics:
        st.info("Aucun sujet disponible.")
        st.stop()

    st.divider()

    # ======================
    # FILTRES
    # ======================

    all_sources = sorted({
        art["source"]
        for t in topics
        for art in t.get("articles", [])
    })

    all_keywords = sorted({
        kw
        for t in topics
        for kw in t.get("keywords", [])
    })

    col1, col2 = st.columns(2)

    with col1:
        selected_sources = st.multiselect(
            " Filtrer par journal",
            all_sources,
            default=all_sources,
            key="ai_sources_filter"
        )

    with col2:
        selected_keywords = st.multiselect(
            "🏷 Filtrer par mot-clé",
            all_keywords,
            default=all_keywords,
            key="ai_keywords_filter"
        )

    st.divider()

    # ======================
    # AFFICHAGE TOPICS
    # ======================

    displayed_count = 0

    for i, topic in enumerate(topics, start=1):

        topic_keywords = topic.get("keywords", [])
        topic_articles = topic.get("articles", [])

        # Filtre keywords
        if selected_keywords:
            if not any(kw in selected_keywords for kw in topic_keywords):
                continue

        # Filtre sources
        filtered_articles = [
            art for art in topic_articles
            if art["source"] in selected_sources
        ]

        if not filtered_articles:
            continue

        displayed_count += 1

        with st.expander(
            f"Sujet {i} — {topic.get('label', 'n/a')}",
            expanded=False
        ):

            colA, colB = st.columns([2, 1])

            with colA:
                st.markdown("### Résumé")
                st.write(topic.get("summary", ""))

            with colB:
                st.metric("Score", f"{topic.get('score', 0):.2f}")
                st.markdown(f"**Articles :** {len(filtered_articles)}")
                st.markdown(f"**Mots-clés :** {', '.join(topic_keywords)}")

            st.divider()

            total_pages = max(1, ceil(len(filtered_articles) / ARTICLES_PER_PAGE))
            page_key = f"ai_page_{i}"
            page = st.session_state.get(page_key, 1)

            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                if st.button("◀", key=f"ai_prev_{i}") and page > 1:
                    page -= 1

            with col3:
                if st.button("▶", key=f"ai_next_{i}") and page < total_pages:
                    page += 1

            st.session_state[page_key] = page
            st.caption(f"Page {page}/{total_pages}")

            start = (page - 1) * ARTICLES_PER_PAGE
            end = start + ARTICLES_PER_PAGE

            for art in filtered_articles[start:end]:
                st.markdown(
                    f"- [{art['title']}]({art['url']})  \n"
                    f"**{art['source']}** — {art.get('published', '')}"
                )

    if displayed_count == 0:
        st.warning("Aucun sujet ne correspond aux filtres sélectionnés.")


# =====================================================
# ONGLET DATASET
# =====================================================

with tab_dataset:

    st.header("Articles collectés")

    dataset_files = sorted(DATASET_DIR.glob("*.yaml"))

    if not dataset_files:
        st.warning("Aucun dataset disponible")
        st.stop()

    selected_dataset = st.selectbox(
        "Sélectionner un dataset",
        [f.name for f in dataset_files],
        index=len(dataset_files) - 1,
        key="dataset_selector"
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
        default=sources,
        key="dataset_sources_filter"
    )

    filtered_articles = [
        a for a in articles
        if a["source"] in selected_sources
    ]

    total_pages = max(1, ceil(len(filtered_articles) / ARTICLES_PER_PAGE))
    page = st.session_state.get("dataset_page", 1)

    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        if st.button("◀", key="dataset_prev") and page > 1:
            page -= 1

    with col3:
        if st.button("▶", key="dataset_next") and page < total_pages:
            page += 1

    st.session_state["dataset_page"] = page
    st.caption(f"Page {page}/{total_pages}")

    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE

    for article in filtered_articles[start:end]:
        with st.expander(article["title"]):

            st.markdown(f"**Source :** {article['source']}")
            st.markdown(f"**Date :** {article['published']}")
            st.markdown(f"**Catégorie :** {article.get('category', '')}")
            st.markdown(f"[Lire l'article]({article['url']})")

            if article.get("is_paywalled"):
                st.warning("Article potentiellement payant")

            if article.get("summary"):
                st.markdown("**Résumé :**")
                st.write(article["summary"])
