import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "python"))

from extract import extract_ticker


def test_extract_ticker_returns_dataframe():
    df = extract_ticker("AAPL")
    assert isinstance(df, pd.DataFrame)


def test_extract_ticker_has_data():
    df = extract_ticker("AAPL")
    assert len(df) > 0


def test_extract_ticker_has_columns():
    df = extract_ticker("AAPL")
    assert "Open" in df.columns
    assert "High" in df.columns
    assert "Low" in df.columns
    assert "Close" in df.columns
    assert "Volume" in df.columns


def test_extract_ticker_invalid_symbol():
    df = extract_ticker("INVALID_SYMBOL_XYZ123")
    assert df.empty
