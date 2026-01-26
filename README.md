# Newscope-IA est un projet qui permet de :

Récupérer automatiquement les flux RSS des journaux.

Construire un dataset quotidien d’articles.

Analyser les articles avec une intelligence artificielle pour vérifier les sources et classer l’actualité du jour.

# Fonctionnalités principales

Crawler RSS : récupère les articles récents depuis les sources définies dans config/sources.yaml.

Nettoyage et prétraitement : suppression des mots vides (stopwords), nettoyage du texte.

Analyse IA : regroupement des articles par thèmes, extraction de mots-clés et résumé global.

Interface Streamlit : visualisation du dataset et des résultats IA avec pagination.

# Prérequis

Avant de lancer le projet, il faut :

Python 3.10+
https://www.python.org/downloads/

Télécharger Python

Vérifier l’installation :

python --version


Installer les dépendances
Depuis le dossier racine du projet :

pip install -r requirements.txt


Le fichier requirements.txt devrait inclure au minimum :

streamlit
pyyaml
feedparser
requests
beautifulsoup4


Fichiers de configuration :

config/sources.yaml : liste des journaux et flux RSS à récupérer.

config/ peut contenir d’autres réglages (ex. nombre de jours à conserver dans le dataset).

# Lancer le projet

Exécuter le programme pour récupérer les articles :

python main.py


Cela crée un dataset quotidien dans dataset/YYYY-MM-DD.yaml.

Lancer l’interface Streamlit pour explorer les données et les résultats IA :

streamlit run interface.py


Onglet Dataset : liste des articles collectés avec filtres par source et pagination.

Onglet Analyse IA : visualisation des topics, des mots-clés et des articles associés.

# Structure des dossiers
newscope-ia/
├─ config/           # Fichiers de configuration (sources, paramètres)
├─ crawler/          # Scripts pour récupérer et nettoyer les articles
├─ dataset/          # Articles collectés (fichiers YAML journaliers)
├─ ia/               # IA de classement et analyse d'articles
├─ output/           # Résultats IA (topics, mots-clés, résumés)
├─ dashboard.py      # Mise en page via Streamlit
├─ main.py           # Point d’entrée pour lancer le crawler
└─ README.md

# Personnalisation

Limiter les articles par source : modifier MAX_ARTICLES_PER_SOURCE dans crawler/main.py ou ajouter une configuration dans config/.

Conserver uniquement X jours de dataset : définir la valeur dans le fichier de config correspondant.

Ajouter de nouvelles sources : éditer config/sources.yaml avec le nom et le flux RSS du journal.

# Liens utiles
https://www.python.org/downloads/
https://docs.streamlit.io/
https://pyyaml.org/wiki/PyYAMLDocumentation
https://feedparser.readthedocs.io/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

