"""
financial_market_pipeline.py
----------------------------
DAG Airflow pour le pipeline ETL financier.
Version finale : 5 tickers en parallèle.
"""

import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


# ============================================================
# AJOUTER LE DOSSIER python/ AU PATH
# ============================================================

sys.path.insert(0, "/opt/airflow/python")


# ============================================================
# FONCTION GÉNÉRIQUE POUR UN TICKER
# ============================================================

def extract_and_load_ticker(ticker: str):
    """
    Tâche générique : extraire un ticker, le nettoyer, le valider,
    le charger dans PostgreSQL.
    """
    import config_docker as config
    from extract import extract_ticker
    from clean import clean_data
    from validate import validate_data
    from loguru import logger

    import load

    logger.info(f"=== Début du pipeline pour {ticker} ===")

    # 1. Extract
    df_raw = extract_ticker(ticker)
    if df_raw.empty:
        raise Exception(f"Aucune donnée extraite pour {ticker}")

    # 2. Clean
    df_clean = clean_data(df_raw, ticker)

    # 3. Validate
    df_valid = validate_data(df_clean, ticker)

    # 4. Load — on passe l'URL Docker explicitement
    engine = load.get_engine(db_url=config.DB_URL)
    result = load.load_ticker_data(engine, ticker, df_valid)

    logger.info(f"=== Résultat {ticker} : {result} ===")

    if result["status"] != "SUCCESS":
        raise Exception(f"Échec du chargement pour {ticker}: {result}")

    return result


# ============================================================
# FONCTIONS SPÉCIFIQUES PAR TICKER (pour Airflow)
# ============================================================

def extract_and_load_aapl():
    return extract_and_load_ticker("AAPL")

def extract_and_load_msft():
    return extract_and_load_ticker("MSFT")

def extract_and_load_googl():
    return extract_and_load_ticker("GOOGL")

def extract_and_load_tsla():
    return extract_and_load_ticker("TSLA")

def extract_and_load_nvda():
    return extract_and_load_ticker("NVDA")


# ============================================================
# DÉFINITION DU DAG
# ============================================================

default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="financial_market_pipeline",
    default_args=default_args,
    description="Pipeline ETL pour les données boursières (5 tickers)",
    schedule="@daily",
    start_date=datetime(2026, 9, 25),
    catchup=False,
    tags=["finance", "etl"],
    max_active_tasks=5,   # Permet 5 tâches en parallèle
) as dag:

    task_aapl = PythonOperator(
        task_id="extract_and_load_aapl",
        python_callable=extract_and_load_aapl,
    )

    task_msft = PythonOperator(
        task_id="extract_and_load_msft",
        python_callable=extract_and_load_msft,
    )

    task_googl = PythonOperator(
        task_id="extract_and_load_googl",
        python_callable=extract_and_load_googl,
    )

    task_tsla = PythonOperator(
        task_id="extract_and_load_tsla",
        python_callable=extract_and_load_tsla,
    )

    task_nvda = PythonOperator(
        task_id="extract_and_load_nvda",
        python_callable=extract_and_load_nvda,
    )