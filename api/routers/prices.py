from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import PriceWithSymbol

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/{symbol}", response_model=List[PriceWithSymbol])
def get_prices(symbol: str, limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    asset = db.execute(text("SELECT asset_id FROM core.assets WHERE symbol = :symbol"), {"symbol": symbol.upper()}).fetchone()
    if not asset:
        raise HTTPException(status_code=404, detail=f"Actif {symbol} non trouve")
    query = "SELECT p.price_id, p.asset_id, p.observation_timestamp, p.timeframe, p.open, p.high, p.low, p.close, p.adjusted_close, p.volume, a.symbol, a.name FROM core.price_data p JOIN core.assets a ON p.asset_id = a.asset_id WHERE p.asset_id = :asset_id ORDER BY p.observation_timestamp DESC LIMIT :limit"
    result = db.execute(text(query), {"asset_id": asset.asset_id, "limit": limit}).fetchall()
    return [dict(row._mapping) for row in result]
