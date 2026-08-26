import pandas as pd
from phoenix_core.data_quality import assess_ohlcv


def test_quality_accepts_valid_ohlcv():
    df = pd.DataFrame({
        "timestamp": pd.date_range("2026-01-01", periods=3, freq="h", tz="UTC"),
        "open": [100, 101, 102],
        "high": [102, 103, 104],
        "low": [99, 100, 101],
        "close": [101, 102, 103],
        "volume": [10, 12, 11],
    })
    report = assess_ohlcv(df)
    assert report.score == 100.0
