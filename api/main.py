from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from config_api import API_TITLE, API_DESCRIPTION, API_VERSION
from database import get_db
from models import HealthResponse
from routers import assets, prices, stats, indicators

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur la Financial Market API"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"
    return {"status": "ok", "database": db_status, "timestamp": datetime.now()}


app.include_router(assets.router)
app.include_router(prices.router)
app.include_router(stats.router)
app.include_router(indicators.router)

