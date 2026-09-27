"""
database.py
-----------
Connexion à PostgreSQL pour FastAPI.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config_api import DB_URL

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """Générateur de session DB."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()