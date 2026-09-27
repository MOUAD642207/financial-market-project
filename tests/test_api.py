from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api"))

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_list_assets():
    response = client.get("/assets/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_asset_aapl():
    response = client.get("/assets/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"


def test_get_asset_not_found():
    response = client.get("/assets/INVALID_XYZ")
    assert response.status_code == 404


def test_get_stats():
    response = client.get("/stats/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "nb_observations" in data


def test_get_prices():
    response = client.get("/prices/AAPL?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


def test_get_indicators():
    response = client.get("/indicators/AAPL?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "data" in data
    assert len(data["data"]) > 0
