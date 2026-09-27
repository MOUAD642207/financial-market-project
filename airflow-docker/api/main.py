"""
main.py
-------
Point d'entrée de l'API FastAPI.
"""

from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from config_api import API_TITLE, API_DESCRIPTION, API_VERSION
from database import get_db
from models import HealthResponse
from routers import assets, prices, stats

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", tags=["Root"])
def read_root():
    """Page d'accueil."""
    return {
        "message": "Bienvenue sur la Financial Market API",
        "version": API_VERSION,
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """Vérifie que l'API et la BDD sont opérationnelles."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "ok",
        "database": db_status,
        "timestamp": datetime.now(),
    }


app.include_router(assets.router)
app.include_router(prices.router)
app.include_router(stats.router)