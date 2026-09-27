"""
extract.py
----------
Extraction des données de marché depuis Yahoo Finance.
Utilise la bibliothèque yfinance pour télécharger les OHLCV.
"""

import yfinance as yf
import pandas as pd
from loguru import logger

from config import YF_START_DATE, YF_END_DATE, YF_INTERVAL


def extract_ticker(ticker: str) -> pd.DataFrame:
    """
    Télécharge les données OHLCV d'un ticker depuis Yahoo Finance.

    Paramètres
    ----------
    ticker : str
        Le symbole boursier (ex: 'AAPL')

    Retourne
    --------
    pd.DataFrame
        DataFrame brut avec les colonnes Open, High, Low, Close, Adj Close, Volume
        Index = DatetimeIndex
        Retourne un DataFrame vide si aucune donnée n'est trouvée.
    """
    logger.info(f"Extraction de {ticker} depuis Yahoo Finance...")

    try:
        df = yf.download(
            tickers=ticker,
            start=YF_START_DATE,
            end=YF_END_DATE,
            interval=YF_INTERVAL,
            auto_adjust=False,   # Garder Close ET Adj Close séparés
            progress=False,
        )

        if df.empty:
            logger.warning(f"Aucune donnée trouvée pour {ticker}")
            return pd.DataFrame()

        logger.success(f"{ticker} : {len(df)} lignes extraites")
        return df

    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de {ticker} : {e}")
        return pd.DataFrame()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    df = extract_ticker("AAPL")
    print("=" * 60)
    print("APERÇU DES DONNÉES BRUTES")
    print("=" * 60)
    print(df.head())
    print()
    print(f"Shape : {df.shape}")
    print(f"Colonnes : {list(df.columns)}")
    print(f"Index : {df.index.name}")