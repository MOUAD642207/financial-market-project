from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class Asset(BaseModel):
    asset_id: int
    symbol: str
    name: str
    asset_type: str
    exchange: Optional[str] = None
    currency: Optional[str] = None


class PriceWithSymbol(BaseModel):
    price_id: int
    asset_id: int
    observation_timestamp: datetime
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    adjusted_close: Optional[float] = None
    volume: int
    symbol: str
    name: str


class AssetStats(BaseModel):
    symbol: str
    name: str
    nb_observations: int
    date_min: date
    date_max: date
    prix_moyen: float
    prix_max: float
    prix_min: float
    volume_total: int


class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime
