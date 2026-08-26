import pandas as pd
import requests

from phoenix_core.data_quality import assess_ohlcv
from phoenix_core.market_data import PublicMarketData


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


def test_coinbase_symbol_mapping():
    assert PublicMarketData._coinbase_product("BTCUSDT") == "BTC-USD"
    assert PublicMarketData._coinbase_product("ETHUSD") == "ETH-USD"


def test_failover_to_coinbase(monkeypatch):
    provider = PublicMarketData()

    def fail(*args, **kwargs):
        raise requests.HTTPError("451")

    monkeypatch.setattr(provider, "_binance", fail)
    monkeypatch.setattr(provider, "_coinbase", lambda *args, **kwargs: provider._frame([
        [i * 3600000, 100+i, 101+i, 99+i, 100.5+i, 10+i] for i in range(60)
    ]))

    df = provider.klines("BTCUSDT", "1h", 60)
    assert provider.last_provider == "coinbase"
    assert len(df) == 60
    assert list(df.columns) == ["timestamp", "open", "high", "low", "close", "volume"]
