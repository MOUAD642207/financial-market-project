"""
clean.py
--------
Nettoyage et transformation des données brutes de Yahoo Finance.
Objectif : produire un DataFrame propre, prêt pour la validation
et l'insertion dans PostgreSQL.
"""

import pandas as pd
from loguru import logger


# Mapping des colonnes Yahoo → PostgreSQL
COLUMN_MAPPING = {
    "Date": "observation_timestamp",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adjusted_close",
    "Volume": "volume",
}


def clean_data(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Nettoie un DataFrame brut de Yahoo Finance.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame brut retourné par extract_ticker()
    ticker : str
        Le symbole (pour les logs)

    Retourne
    --------
    pd.DataFrame
        DataFrame propre, prêt pour la validation
    """
    if df.empty:
        logger.warning(f"{ticker} : DataFrame vide, rien à nettoyer")
        return df

    logger.info(f"{ticker} : nettoyage en cours...")

    # Étape 1 — Reset de l'index (Date devient une colonne)
    df = df.reset_index()

    # Étape 2 — Aplatir les MultiIndex éventuels
    # (yfinance retourne parfois des colonnes en tuple quand plusieurs tickers)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Étape 3 — Renommer les colonnes
    df = df.rename(columns=COLUMN_MAPPING)

    # Étape 4 — Supprimer les doublons
    nb_avant = len(df)
    df = df.drop_duplicates()
    nb_doublons = nb_avant - len(df)
    if nb_doublons > 0:
        logger.warning(f"{ticker} : {nb_doublons} doublons supprimés")

    # Étape 5 — Supprimer les lignes où OHLC est manquant
    nb_avant = len(df)
    df = df.dropna(subset=["open", "high", "low", "close"])
    nb_nan = nb_avant - len(df)
    if nb_nan > 0:
        logger.warning(f"{ticker} : {nb_nan} lignes avec OHLC manquant supprimées")

    # Étape 6 — Remplir le volume manquant par 0
    df["volume"] = df["volume"].fillna(0)

    # Étape 7 — Convertir les types
    df["observation_timestamp"] = pd.to_datetime(df["observation_timestamp"])
    df["volume"] = df["volume"].astype("int64")

    for col in ["open", "high", "low", "close", "adjusted_close"]:
        if col in df.columns:
            df[col] = df[col].astype("float64")

    # Étape 8 — Trier chronologiquement
    df = df.sort_values("observation_timestamp").reset_index(drop=True)

    # Étape 9 — Ajouter les colonnes de contexte
    df["timeframe"] = "1d"

    logger.success(f"{ticker} : nettoyage terminé ({len(df)} lignes propres)")
    return df


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    from extract import extract_ticker

    df_raw = extract_ticker("AAPL")
    df_clean = clean_data(df_raw, "AAPL")

    print("=" * 60)
    print("APERÇU DES DONNÉES PROPRES")
    print("=" * 60)
    print(df_clean.head())
    print()
    print(f"Shape : {df_clean.shape}")
    print(f"Colonnes : {list(df_clean.columns)}")
    print(f"Types :")
    print(df_clean.dtypes)