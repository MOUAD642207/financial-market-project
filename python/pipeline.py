"""
pipeline.py
-----------
Pipeline complet : extract → clean → validate → load.
"""

from loguru import logger
import sys

from config import YF_TICKERS, LOGS_DIR
from extract import extract_ticker
from clean import clean_data
from validate import validate_data
from load import get_engine, load_ticker_data


# ============================================================
# CONFIGURATION DES LOGS
# ============================================================

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level="INFO",
)
logger.add(
    LOGS_DIR / "pipeline_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
)


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def run_pipeline():
    """Exécute le pipeline complet sur tous les tickers."""
    logger.info("=" * 60)
    logger.info("DÉMARRAGE DU PIPELINE")
    logger.info("=" * 60)

    engine = get_engine()
    resultats = []

    for ticker in YF_TICKERS:
        logger.info(f"--- Traitement de {ticker} ---")

        df_raw = extract_ticker(ticker)
        if df_raw.empty:
            logger.error(f"{ticker} : aucune donnée, on passe au suivant")
            resultats.append({"ticker": ticker, "received": 0, "loaded": 0, "status": "FAILED"})
            continue

        df_clean = clean_data(df_raw, ticker)
        df_valid = validate_data(df_clean, ticker)

        result = load_ticker_data(engine, ticker, df_valid)
        resultats.append(result)

    # ============================================================
    # RÉSUMÉ
    # ============================================================
    logger.info("=" * 60)
    logger.info("RÉSUMÉ DU PIPELINE")
    logger.info("=" * 60)
    logger.info(f"{'Ticker':8s} | {'Reçues':>8s} | {'Insérées':>8s} | {'Statut':>10s}")
    logger.info("-" * 60)
    for r in resultats:
        logger.info(f"{r['ticker']:8s} | {r['received']:>8d} | {r['loaded']:>8d} | {r['status']:>10s}")
    logger.info("=" * 60)
    logger.success("PIPELINE TERMINÉ")


if __name__ == "__main__":
    run_pipeline()