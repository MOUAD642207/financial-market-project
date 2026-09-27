from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db
from models import AssetStats

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/{symbol}", response_model=AssetStats)
def get_stats(symbol: str, db: Session = Depends(get_db)):
    query = "SELECT a.symbol, a.name, COUNT(*) AS nb_observations, MIN(p.observation_timestamp)::date AS date_min, MAX(p.observation_timestamp)::date AS date_max, ROUND(AVG(p.close), 2) AS prix_moyen, MAX(p.high) AS prix_max, MIN(p.low) AS prix_min, SUM(p.volume) AS volume_total FROM core.price_data p JOIN core.assets a ON p.asset_id = a.asset_id WHERE a.symbol = :symbol GROUP BY a.symbol, a.name"
    result = db.execute(text(query), {"symbol": symbol.upper()}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail=f"Aucune donnee pour {symbol}")
    return dict(result._mapping)
