import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from validate import validate_data


def create_clean_df():
    return pd.DataFrame({
        "observation_timestamp": pd.date_range("2024-01-01", periods=10, freq="D", tz="UTC"),
        "open": [100.0] * 10,
        "high": [105.0] * 10,
        "low": [95.0] * 10,
        "close": [102.0] * 10,
        "adjusted_close": [102.0] * 10,
        "volume": [1000000] * 10,
        "timeframe": ["1d"] * 10,
    })


def test_validate_data_returns_dataframe():
    df = create_clean_df()
    result = validate_data(df, "TEST")
    assert isinstance(result, pd.DataFrame)


def test_validate_data_removes_invalid_high_low():
    df = create_clean_df()
    df.loc[0, "high"] = 90.0
    df.loc[0, "low"] = 100.0
    result = validate_data(df, "TEST")
    assert len(result) < len(df)


def test_validate_data_removes_negative_volume():
    df = create_clean_df()
    df.loc[0, "volume"] = -100
    result = validate_data(df, "TEST")
    assert len(result) < len(df)


def test_validate_data_keeps_valid():
    df = create_clean_df()
    result = validate_data(df, "TEST")
    assert len(result) == len(df)
