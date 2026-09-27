from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from indicators import compute_indicators

router = APIRouter(prefix="/indicators", tags=["Indicators"])


@router.get("/{symbol}")
def get_indicators(
    symbol: str,
    limit: int = Query(300, ge=50, le=2000),
    db: Session = Depends(get_db),
):
    asset = db.execute(
        text("SELECT asset_id, symbol, name FROM core.assets WHERE symbol = :symbol"),
        {"symbol": symbol.upper()}
    ).fetchone()

    if not asset:
        raise HTTPException(status_code=404, detail=f"Actif {symbol} non trouve")

    query = "SELECT observation_timestamp, open, high, low, close, volume FROM core.price_data WHERE asset_id = :asset_id ORDER BY observation_timestamp ASC LIMIT :limit"
    result = db.execute(text(query), {"asset_id": asset.asset_id, "limit": limit}).fetchall()

    if not result:
        raise HTTPException(status_code=404, detail=f"Aucune donnee pour {symbol}")

    df = pd.DataFrame([dict(row._mapping) for row in result])
    df["observation_timestamp"] = pd.to_datetime(df["observation_timestamp"], utc=True)

    df = compute_indicators(df)

    # Convertir le timestamp en string ISO pour JSON
    df["observation_timestamp"] = df["observation_timestamp"].astype(str)

    # Remplacer NaN et inf par None
    df = df.replace([np.inf, -np.inf], np.nan)
    data = df.where(pd.notnull(df), None).to_dict(orient="records")

    # Nettoyer chaque valeur pour JSON
    cleaned_data = []
    for record in data:
        clean_record = {}
        for key, value in record.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                clean_record[key] = None
            else:
                clean_record[key] = value
        cleaned_data.append(clean_record)

    return {
        "symbol": asset.symbol,
        "name": asset.name,
        "data": cleaned_data,
    }
