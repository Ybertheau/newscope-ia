import sys
import subprocess
import importlib.util
from pathlib import Path

MIN_PYTHON = (3, 10)
PROJECT_DIR = Path(__file__).resolve().parent.parent
REQUIREMENTS_FILE = PROJECT_DIR / "config" / "requirements.txt"

def check_environment():
    # -------------------
    # Python version
    # -------------------
    if sys.version_info < MIN_PYTHON:
        raise RuntimeError(
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ requis "
            f"(actuel : {sys.version.split()[0]})"
        )
    print(f"Python {sys.version.split()[0]}")

    # -------------------
    # Requirements
    # -------------------
    if not REQUIREMENTS_FILE.exists():
        raise FileNotFoundError(f"{REQUIREMENTS_FILE} introuvable")

    with REQUIREMENTS_FILE.open() as f:
        requirements = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]

    # -------------------
    # Install / Verify
    # -------------------
    def is_installed(package: str) -> bool:
        return importlib.util.find_spec(package) is not None

    def install(package: str):
        print(f"Installation : {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("\n Vérification des dépendances...\n")

    for package in requirements:
        pkg_name = package.split("==")[0]
        if is_installed(pkg_name):
            print(f"{pkg_name} installation OK")
        else:
            install(package)

    print("\n Environnement OK")
