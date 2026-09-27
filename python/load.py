"""
load.py
-------
Insertion des données validées dans PostgreSQL.
Gère le cycle de vie d'une ingestion (RUNNING → SUCCESS/FAILED).
"""

import pandas as pd
from sqlalchemy import create_engine, text
from loguru import logger


# ============================================================
# CONNEXION
# ============================================================

def get_engine(db_url=None):
    """
    Crée et retourne un engine SQLAlchemy.
    Accepte une URL custom (utile pour Docker).
    Si db_url est None, utilise config.DB_URL (mode local).
    """
    if db_url is None:
        # Import différé : évite les problèmes au chargement du module
        from config import DB_URL as db_url
    return create_engine(db_url)


# ============================================================
# RÉCUPÉRATION DES IDs
# ============================================================

def get_asset_id(engine, ticker: str) -> int:
    """Récupère l'asset_id correspondant à un ticker."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT asset_id FROM core.assets WHERE symbol = :ticker"),
            {"ticker": ticker}
        ).fetchone()
        return result[0] if result else None


def get_source_id(engine, source_name: str = "Yahoo Finance") -> int:
    """Récupère le source_id de Yahoo Finance."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT source_id FROM core.data_sources WHERE source_name = :name"),
            {"name": source_name}
        ).fetchone()
        return result[0] if result else None


# ============================================================
# GESTION DES INGESTIONS
# ============================================================

def create_ingestion_run(engine, source_id: int) -> int:
    """Crée une nouvelle ligne dans ops.ingestion_runs (status='RUNNING')."""
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO ops.ingestion_runs
                    (source_id, started_at, status, records_received, records_loaded)
                VALUES
                    (:source_id, NOW(), 'RUNNING', 0, 0)
                RETURNING ingestion_run_id
            """),
            {"source_id": source_id}
        ).fetchone()
        run_id = result[0]
    logger.info(f"Ingestion run créé : ingestion_run_id = {run_id}")
    return run_id


def finish_ingestion_run(engine, run_id: int, status: str,
                         records_received: int, records_loaded: int,
                         error_message: str = None):
    """Met à jour l'ingestion run avec le statut final."""
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE ops.ingestion_runs
                SET status = :status,
                    finished_at = NOW(),
                    records_received = :received,
                    records_loaded = :loaded,
                    error_message = :error
                WHERE ingestion_run_id = :run_id
            """),
            {
                "status": status,
                "received": records_received,
                "loaded": records_loaded,
                "error": error_message,
                "run_id": run_id,
            }
        )
    logger.info(f"Ingestion run {run_id} clôturé : status={status}")


# ============================================================
# INSERTION DES DONNÉES
# ============================================================

def insert_price_data(engine, df: pd.DataFrame, asset_id: int,
                      source_id: int, run_id: int) -> int:
    """
    Insère les lignes du DataFrame dans core.price_data.
    Utilise ON CONFLICT DO NOTHING pour éviter les doublons.
    """
    if df.empty:
        return 0

    rows = []
    for _, row in df.iterrows():
        rows.append({
            "asset_id": asset_id,
            "source_id": source_id,
            "ingestion_run_id": run_id,
            "observation_timestamp": row["observation_timestamp"],
            "timeframe": row["timeframe"],
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "adjusted_close": float(row["adjusted_close"]) if pd.notna(row.get("adjusted_close")) else None,
            "volume": int(row["volume"]),
        })

    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO core.price_data
                    (asset_id, source_id, ingestion_run_id, observation_timestamp,
                     timeframe, open, high, low, close, adjusted_close, volume)
                VALUES
                    (:asset_id, :source_id, :ingestion_run_id, :observation_timestamp,
                     :timeframe, :open, :high, :low, :close, :adjusted_close, :volume)
                ON CONFLICT (asset_id, observation_timestamp, timeframe, source_id)
                DO NOTHING
            """),
            rows
        )
        return result.rowcount


# ============================================================
# PIPELINE DE LOAD
# ============================================================

def load_ticker_data(engine, ticker: str, df: pd.DataFrame) -> dict:
    """
    Charge les données d'un ticker dans PostgreSQL.
    Gère le cycle ingestion_run (RUNNING → SUCCESS/FAILED).
    """
    logger.info(f"{ticker} : chargement dans PostgreSQL...")

    asset_id = get_asset_id(engine, ticker)
    if asset_id is None:
        logger.error(f"{ticker} : asset_id introuvable dans core.assets")
        return {"ticker": ticker, "received": len(df), "loaded": 0, "status": "FAILED"}

    source_id = get_source_id(engine)
    if source_id is None:
        logger.error(f"{ticker} : source_id introuvable dans core.data_sources")
        return {"ticker": ticker, "received": len(df), "loaded": 0, "status": "FAILED"}

    logger.info(f"{ticker} : asset_id={asset_id}, source_id={source_id}")

    run_id = create_ingestion_run(engine, source_id)

    try:
        nb_loaded = insert_price_data(engine, df, asset_id, source_id, run_id)
        finish_ingestion_run(
            engine, run_id,
            status="SUCCESS",
            records_received=len(df),
            records_loaded=nb_loaded,
        )
        logger.success(f"{ticker} : {nb_loaded}/{len(df)} lignes insérées")
        return {"ticker": ticker, "received": len(df), "loaded": nb_loaded, "status": "SUCCESS"}

    except Exception as e:
        logger.error(f"{ticker} : erreur lors de l'insertion : {e}")
        finish_ingestion_run(
            engine, run_id,
            status="FAILED",
            records_received=len(df),
            records_loaded=0,
            error_message=str(e),
        )
        return {"ticker": ticker, "received": len(df), "loaded": 0, "status": "FAILED"}


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    from extract import extract_ticker
    from clean import clean_data
    from validate import validate_data

    engine = get_engine()

    df_raw = extract_ticker("AAPL")
    df_clean = clean_data(df_raw, "AAPL")
    df_valid = validate_data(df_clean, "AAPL")

    result = load_ticker_data(engine, "AAPL", df_valid)
    print("=" * 60)
    print("RÉSULTAT DU CHARGEMENT")
    print("=" * 60)
    print(result)