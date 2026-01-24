import sys
from pathlib import Path

from config.bootstrap import check_environment
from tmp.testing import test_rss
from tmp.crawler import crawl
from ia.run import run_ia
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))


def main():
    print("Newscope-IA\n")

    # 1. Bootstrap
    try:
        check_environment()
    except Exception as e:
        print(f"Bootstrap échoué : {e}")
        return

    # 2. Test RSS
    try:
        rss_ok = test_rss()
        if not rss_ok:
            print("Certains flux RSS sont problématiques, arrêt du pipeline.")
            return
    except Exception as e:
        print(f"Tests RSS échoués : {e}")
        return

    # 3. Crawl
    try:
        crawl()
    except Exception as e:
        print(f"Crawling échoué : {e}")
        return

    print("\nPipeline terminé avec succès")

    try:
        run_ia()
    except Exception as e:
        print(f"IA échouée : {e}")
        return
    
    print("\nPipeline IA terminé avec succès")
if __name__ == "__main__":
    main()
