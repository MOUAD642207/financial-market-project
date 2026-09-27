"""
config.py
---------
Configuration centralisée du projet.
Charge les variables depuis le fichier .env et expose les paramètres
utilisés par les autres modules du pipeline.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# 1. CHEMINS DU PROJET
# ============================================================

# Racine du projet : on remonte d'un niveau depuis python/
BASE_DIR = Path(__file__).resolve().parent.parent

# Dossiers du projet
LOGS_DIR = BASE_DIR / "logs"
SQL_DIR = BASE_DIR / "sql"
BACKUPS_DIR = BASE_DIR / "backups"

# Créer le dossier logs s'il n'existe pas
LOGS_DIR.mkdir(exist_ok=True)

# ============================================================
# 2. CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
# ============================================================

# Charge le fichier .env situé à la racine
load_dotenv(BASE_DIR / ".env")

# ============================================================
# 3. CONFIGURATION POSTGRESQL
# ============================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "financial_market_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Chaîne de connexion SQLAlchemy
DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# ============================================================
# 4. CONFIGURATION YAHOO FINANCE
# ============================================================

# Liste des tickers (séparés par virgule dans .env)
YF_TICKERS = os.getenv("YF_TICKERS", "AAPL,MSFT,GOOGL").split(",")
YF_TICKERS = [t.strip() for t in YF_TICKERS if t.strip()]

# Date de début et de fin (format YYYY-MM-DD)
YF_START_DATE = os.getenv("YF_START_DATE", "2024-01-01")
YF_END_DATE = os.getenv("YF_END_DATE", None)  # None = aujourd'hui

# Granularité : 1d, 1h, 5m, ...
YF_INTERVAL = os.getenv("YF_INTERVAL", "1d")

# ============================================================
# 5. AFFICHAGE (pour vérifier)
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("CONFIGURATION DU PROJET")
    print("=" * 60)
    print(f"BASE_DIR     : {BASE_DIR}")
    print(f"LOGS_DIR     : {LOGS_DIR}")
    print(f"DB_HOST      : {DB_HOST}")
    print(f"DB_PORT      : {DB_PORT}")
    print(f"DB_NAME      : {DB_NAME}")
    print(f"DB_USER      : {DB_USER}")
    print(f"DB_PASSWORD  : {'*' * len(DB_PASSWORD)}")
    print(f"YF_TICKERS   : {YF_TICKERS}")
    print(f"YF_START     : {YF_START_DATE}")
    print(f"YF_END       : {YF_END_DATE}")
    print(f"YF_INTERVAL  : {YF_INTERVAL}")
    print("=" * 60)