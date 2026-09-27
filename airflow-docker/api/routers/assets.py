"""
assets.py
---------
Endpoints pour les actifs.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Asset

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/", response_model=List[Asset])
def list_assets(db: Session = Depends(get_db)):
    """Liste tous les actifs."""
    result = db.execute(
        text("""
            SELECT asset_id, symbol, name, asset_type, exchange, currency
            FROM core.assets
            ORDER BY symbol
        """)
    ).fetchall()

    return [dict(row._mapping) for row in result]


@router.get("/{symbol}", response_model=Asset)
def get_asset(symbol: str, db: Session = Depends(get_db)):
    """Récupère un actif par son symbole."""
    result = db.execute(
        text("""
            SELECT asset_id, symbol, name, asset_type, exchange, currency
            FROM core.assets
            WHERE symbol = :symbol
        """),
        {"symbol": symbol.upper()}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail=f"Actif '{symbol}' non trouvé")

    return dict(result._mapping)