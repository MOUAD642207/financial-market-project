"""
prices.py
---------
Endpoints pour les prix.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from database import get_db
from models import PriceWithSymbol

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/{symbol}", response_model=List[PriceWithSymbol])
def get_prices(
    symbol: str,
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Récupère les prix d'un actif."""
    asset = db.execute(
        text("SELECT asset_id, symbol, name FROM core.assets WHERE symbol = :symbol"),
        {"symbol": symbol.upper()}
    ).fetchone()

    if not asset:
        raise HTTPException(status_code=404, detail=f"Actif '{symbol}' non trouvé")

    query = """
        SELECT
            p.price_id, p.asset_id, p.observation_timestamp, p.timeframe,
            p.open, p.high, p.low, p.close, p.adjusted_close, p.volume,
            a.symbol, a.name
        FROM core.price_data p
        JOIN core.assets a ON p.asset_id = a.asset_id
        WHERE p.asset_id = :asset_id
    """
    params = {"asset_id": asset.asset_id, "limit": limit}

    if start:
        query += " AND p.observation_timestamp >= :start"
        params["start"] = start
    if end:
        query += " AND p.observation_timestamp <= :end"
        params["end"] = end

    query += " ORDER BY p.observation_timestamp DESC LIMIT :limit"

    result = db.execute(text(query), params).fetchall()

    return [dict(row._mapping) for row in result]