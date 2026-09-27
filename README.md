# Financial Market Data Platform

Plateforme de donnees financieres qui ingere les donnees de marche depuis Yahoo Finance, les nettoie, les stocke dans PostgreSQL, les orchestre avec Airflow, les expose via FastAPI, et les visualise dans un dashboard Streamlit.

## Architecture

Yahoo Finance -> Python ETL -> PostgreSQL -> FastAPI -> Streamlit Dashboard
                                    |
                                    v
                              Apache Airflow
                              (Orchestration)

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.12 |
| Base de donnees | PostgreSQL 16 |
| Orchestration | Apache Airflow 2.10 (Docker) |
| API REST | FastAPI + Uvicorn |
| Dashboard | Streamlit + Plotly |
| Conteneurisation | Docker + Docker Compose |
| Extraction | yfinance |
| Traitement | pandas, numpy |

## Structure du projet

financial_market_project/
- airflow-docker/    : Airflow (DAGs, Dockerfile, docker-compose)
- api/               : API REST FastAPI
- dashboard/         : Dashboard Streamlit
- python/            : Pipeline ETL (extract, clean, validate, load)
- sql/               : Scripts SQL
- tests/             : Tests unitaires et d'integration
- backups/           : Sauvegardes PostgreSQL

## Installation

### Prerequis

- Python 3.12+
- PostgreSQL 16 (port 5433)
- Docker Desktop
- Git

### Etapes

1. Cloner le projet
   git clone https://github.com/MOUAD642207/financial-market-project.git
   cd financial-market-project

2. Creer l'environnement virtuel
   python -m venv venv
   venv\Scripts\activate

3. Installer les dependances
   pip install -r requirements.txt

4. Configurer le .env
   cp .env.example .env
   # Editer .env avec vos identifiants PostgreSQL

5. Creer la base de donnees
   # Executer les scripts dans sql/

6. Lancer le pipeline ETL
   cd python
   python pipeline.py

## Utilisation

### Lancer Airflow (orchestration)

cd airflow-docker
docker compose up -d

Acces : http://localhost:8080 (admin / admin)

### Lancer FastAPI (API REST)

cd api
uvicorn main:app --reload --port 8000

Acces : http://localhost:8000/docs

### Lancer Streamlit (dashboard)

cd dashboard
streamlit run app.py

Acces : http://localhost:8501

## Tests

pytest tests/ -v

24 tests couvrant :
- API FastAPI (8 tests)
- Extraction Yahoo Finance (4 tests)
- Nettoyage pandas (4 tests)
- Validation metier (4 tests)
- Indicateurs techniques (4 tests)

## Endpoints API

| Methode | URL | Description |
|---------|-----|-------------|
| GET | / | Page d'accueil |
| GET | /health | Health check |
| GET | /assets/ | Liste des actifs |
| GET | /assets/{symbol} | Details d'un actif |
| GET | /prices/{symbol} | Prix d'un actif |
| GET | /stats/{symbol} | Statistiques |
| GET | /indicators/{symbol} | Indicateurs techniques |

## Indicateurs techniques

- MA20, MA50, MA200 (moyennes mobiles)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bandes de Bollinger
- Volatilite annualisee

## DAGs Airflow

- financial_market_pipeline : Pipeline ETL pour 5 tickers (quotidien)

## Licence

MIT
