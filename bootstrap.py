import sys
import subprocess
import importlib.util
from pathlib import Path

# =====================
# CONFIG
# =====================
MIN_PYTHON = (3, 10)
REQUIREMENTS_FILE = "requirements.txt"

# =====================
# PYTHON VERSION CHECK
# =====================
if sys.version_info < MIN_PYTHON:
    print(
        f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ requis "
        f"(actuel : {sys.version.split()[0]})"
    )
    sys.exit(1)

print(f"Python {sys.version.split()[0]}")

# =====================
# REQUIREMENTS CHECK
# =====================
req_path = Path(REQUIREMENTS_FILE)

if not req_path.exists():
    print(f" {REQUIREMENTS_FILE} introuvable")
    sys.exit(1)

with req_path.open() as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

# =====================
# INSTALL / VERIFY
# =====================
def is_installed(package: str) -> bool:
    return importlib.util.find_spec(package) is not None

def install(package: str):
    print(f"Installation : {package}")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", package]
    )

print("\n Vérification des dépendances...\n")

for package in requirements:
    pkg_name = package.split("==")[0]

    if is_installed(pkg_name):
        print(f"{pkg_name} installation OK")
    else:
        install(package)

print("\n Environnement OK")
