import os
import sys
import subprocess
from pathlib import Path
from config.bootstrap import check_environment
from crawler.testing import test_rss
from crawler.crawler import crawl
from ia.run import run_ia
# Suppression des warnings de configuration Streamlit
os.environ["STREAMLIT_SUPPRESS_CONFIG_WARNINGS"] = "1"

# Définition des chemins
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))
DATASET_DIR = PROJECT_ROOT / "dataset"

# Recherche du dataset le plus récent
def latest_dataset():
    files = sorted(DATASET_DIR.glob("*.yaml"))
    return files[-1] if files else None

# Lancer le dashboard Streamlit
def run_dashboard():
    """Lance Streamlit sur le dashboard"""
    dashboard_path = PROJECT_ROOT / "dashboard.py"
    if not dashboard_path.exists():
        print(f"Dashboard introuvable : {dashboard_path}")
        return
    # On utilise sys.executable pour être sûr que Streamlit est appelé avec le bon Python
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(dashboard_path)])
    
# Pipeline principal
def main():
    print("Newscope-IA\n")

    # 1. Bootstrap
    try:
        check_environment()
    except Exception as e:
        print(f"Bootstrap échoué : {e}")
        return

    # 2. Vérification de l'existence d'un dataset récent
    dataset_file = latest_dataset()
    if dataset_file:
        print(f"Dataset récent trouvé : {dataset_file.name}")
        print("Lancement direct de l'interface...")
        run_dashboard()
        return

    # 3. Test RSS
    try:
        rss_ok = test_rss()
        if not rss_ok:
            print("Certains flux RSS sont problématiques, arrêt du pipeline.")
            return
    except Exception as e:
        print(f"Tests RSS échoués : {e}")
        return

    # 4. Crawl
    try:
        crawl()
    except Exception as e:
        print(f"Crawling échoué : {e}")
        return

    # 5. IA run
    try:
        run_ia()
    except Exception as e:
        print(f"IA échouée : {e}")
        return

    print("\nPipeline IA terminé avec succès")
    
    # 6. Lancer le dashboard après le premier run
    run_dashboard()

if __name__ == "__main__":
    main()
