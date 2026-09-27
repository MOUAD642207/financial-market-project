import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api"))

from indicators import compute_indicators


def create_test_df(n=300):
    return pd.DataFrame({
        "observation_timestamp": pd.date_range("2024-01-01", periods=n, freq="D", tz="UTC"),
        "open": [100.0] * n,
        "high": [105.0] * n,
        "low": [95.0] * n,
        "close": [100.0 + i * 0.1 for i in range(n)],
        "volume": [1000000] * n,
    })


def test_compute_indicators_returns_dataframe():
    df = create_test_df()
    result = compute_indicators(df)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == len(df)


def test_compute_indicators_has_ma_columns():
    df = create_test_df()
    result = compute_indicators(df)
    assert "ma20" in result.columns
    assert "ma50" in result.columns
    assert "ma200" in result.columns
    assert "rsi" in result.columns
    assert "macd" in result.columns


def test_ma20_values():
    df = create_test_df()
    result = compute_indicators(df)
    assert pd.isna(result["ma20"].iloc[0])
    assert not pd.isna(result["ma20"].iloc[25])


def test_rsi_between_0_and_100():
    df = create_test_df()
    result = compute_indicators(df)
    rsi_valid = result["rsi"].dropna()
    assert (rsi_valid >= 0).all()
    assert (rsi_valid <= 100).all()
