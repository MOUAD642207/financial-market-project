"""
validate.py
-----------
Validation métier des données nettoyées.
Applique les règles de cohérence financière avant insertion en base.
Les lignes invalides sont rejetées et loguées.
"""

import pandas as pd
from datetime import datetime, timezone
from loguru import logger


def validate_data(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Valide les règles métier sur un DataFrame nettoyé.

    Règles appliquées :
    - high >= low
    - high >= open et high >= close
    - low <= open et low <= close
    - volume >= 0
    - open, high, low, close > 0
    - observation_timestamp <= maintenant

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame propre retourné par clean_data()
    ticker : str
        Le symbole (pour les logs)

    Retourne
    --------
    pd.DataFrame
        DataFrame validé (lignes invalides supprimées)
    """
    if df.empty:
        logger.warning(f"{ticker} : DataFrame vide, rien à valider")
        return df

    logger.info(f"{ticker} : validation en cours...")
    nb_initial = len(df)

    # Règle 1 : high >= low
    mask_high_low = df["high"] >= df["low"]

    # Règle 2 : high >= open et high >= close
    mask_high_open = df["high"] >= df["open"]
    mask_high_close = df["high"] >= df["close"]

    # Règle 3 : low <= open et low <= close
    mask_low_open = df["low"] <= df["open"]
    mask_low_close = df["low"] <= df["close"]

    # Règle 4 : volume >= 0
    mask_volume = df["volume"] >= 0

    # Règle 5 : prix > 0
    mask_prix_positif = (
        (df["open"] > 0) & (df["high"] > 0) &
        (df["low"] > 0) & (df["close"] > 0)
    )

    # Règle 6 : date <= maintenant
    now = pd.Timestamp.now(tz="UTC")
    # On convertit observation_timestamp en UTC si nécessaire
    ts = pd.to_datetime(df["observation_timestamp"], utc=True)
    mask_date = ts <= now

    # Combinaison de toutes les règles
    mask_valide = (
        mask_high_low &
        mask_high_open & mask_high_close &
        mask_low_open & mask_low_close &
        mask_volume &
        mask_prix_positif &
        mask_date
    )

    # Séparation valides / invalides
    df_valide = df[mask_valide].copy()
    df_invalide = df[~mask_valide]

    nb_rejetees = len(df_invalide)

    if nb_rejetees > 0:
        logger.warning(f"{ticker} : {nb_rejetees} lignes rejetées par la validation")
        logger.warning(f"Exemples de lignes rejetées :")
        logger.warning(df_invalide.head().to_string())

    logger.success(f"{ticker} : validation terminée ({len(df_valide)}/{nb_initial} lignes valides)")
    return df_valide


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    from extract import extract_ticker
    from clean import clean_data

    df_raw = extract_ticker("AAPL")
    df_clean = clean_data(df_raw, "AAPL")
    df_valid = validate_data(df_clean, "AAPL")

    print("=" * 60)
    print("APERÇU DES DONNÉES VALIDÉES")
    print("=" * 60)
    print(df_valid.head())
    print()
    print(f"Shape finale : {df_valid.shape}")