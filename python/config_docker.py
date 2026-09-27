"""
config_docker.py
----------------
Configuration adaptée pour Airflow dans Docker.
Utilise host.docker.internal pour joindre le PostgreSQL de Windows.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# ============================================================
# CHEMINS
# ============================================================

# Dans le container, le projet est monté sous /opt/airflow
BASE_DIR = Path("/opt/airflow")

# Le .env est monté directement
load_dotenv(BASE_DIR / ".env")


# ============================================================
# CONFIGURATION POSTGRESQL — ADAPTÉE POUR DOCKER
# ============================================================

# ⚠️ On utilise host.docker.internal pour joindre Windows
DB_HOST = "host.docker.internal"
DB_PORT = int(os.getenv("DB_PORT", "5433"))
DB_NAME = os.getenv("DB_NAME", "financial_market_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# ⚠️ On utilise psycopg2 (driver classique), pas psycopg v3
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# ============================================================
# CONFIGURATION YAHOO FINANCE
# ============================================================

YF_TICKERS = os.getenv("YF_TICKERS", "AAPL,MSFT,GOOGL,TSLA,NVDA").split(",")
YF_TICKERS = [t.strip() for t in YF_TICKERS if t.strip()]

YF_START_DATE = os.getenv("YF_START_DATE", "2024-01-01")
YF_END_DATE = os.getenv("YF_END_DATE", None)
YF_INTERVAL = os.getenv("YF_INTERVAL", "1d")


# ============================================================
# LOGS
# ============================================================

LOGS_DIR = Path("/opt/airflow/logs")