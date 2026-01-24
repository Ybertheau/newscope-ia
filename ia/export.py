import yaml
from datetime import datetime
from pathlib import Path
from ia.summary import summarize_cluster

def export_topics(topics, output_dir: Path):
    output_dir.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"topics_{today}.yaml"

    yaml_topics = []

    for topic_id, topic in topics.items():
        summaries = [
            a.get("summary", "")
            for a in topic["articles"]
            if a.get("summary")
        ]

        global_summary = summarize_cluster(summaries)

        yaml_topics.append({
            "topic_id": int(topic_id),
            "articles_count": topic["count"],
            "keywords": topic["keywords"],
            "summary": global_summary,
            "articles": [
                {
                    "title": a["title"],
                    "url": a["url"],
                    "source": a["source"],
                    "published": a["published"]
                }
                for a in topic["articles"]
            ]
        })

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            {"topics": yaml_topics},
            f,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"Fichier IA généré : {output_file}")
