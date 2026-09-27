import requests

API_URL = "http://localhost:8000"


def get_assets():
    r = requests.get(f"{API_URL}/assets/")
    r.raise_for_status()
    return r.json()


def get_asset(symbol):
    r = requests.get(f"{API_URL}/assets/{symbol}")
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


def get_prices(symbol, limit=100):
    r = requests.get(f"{API_URL}/prices/{symbol}", params={"limit": limit})
    r.raise_for_status()
    return r.json()


def get_stats(symbol):
    r = requests.get(f"{API_URL}/stats/{symbol}")
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


def check_health():
    try:
        r = requests.get(f"{API_URL}/health")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "database": str(e)}
