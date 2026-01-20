
from logging import config
import sys
from pathlib import Path
from config.bootstrap import check_environment
from crawler.testing import test_rss
from crawler.crawler import crawl

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

def main():
    print("Newscope-IA")
    try:
        check_environment
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

    print("Pipeline terminé avec succès")

if __name__ == "__main__":
    main()