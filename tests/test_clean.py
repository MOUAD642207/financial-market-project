import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from clean import clean_data


def create_raw_df():
    return pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=10, freq="D"),
        "Open": [100.0] * 10,
        "High": [105.0] * 10,
        "Low": [95.0] * 10,
        "Close": [102.0] * 10,
        "Adj Close": [102.0] * 10,
        "Volume": [1000000] * 10,
    })


def test_clean_data_returns_dataframe():
    df = create_raw_df()
    result = clean_data(df, "TEST")
    assert isinstance(result, pd.DataFrame)


def test_clean_data_renames_columns():
    df = create_raw_df()
    result = clean_data(df, "TEST")
    assert "open" in result.columns
    assert "high" in result.columns
    assert "low" in result.columns
    assert "close" in result.columns
    assert "volume" in result.columns


def test_clean_data_adds_timeframe():
    df = create_raw_df()
    result = clean_data(df, "TEST")
    assert "timeframe" in result.columns
    assert result["timeframe"].iloc[0] == "1d"


def test_clean_data_volume_int():
    df = create_raw_df()
    result = clean_data(df, "TEST")
    assert result["volume"].dtype in ["int64", "int32"]
