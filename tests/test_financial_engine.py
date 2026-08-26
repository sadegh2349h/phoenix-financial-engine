import pandas as pd

from phoenix_core.financial_engine import FinancialEngine


class FailoverProvider:
    last_provider = "coinbase"

    def klines(self, symbol="BTCUSDT", interval="1h", limit=500):
        n = max(60, limit)
        close = [100.0 + i * 0.25 for i in range(n)]
        return pd.DataFrame({
            "timestamp": pd.date_range("2026-01-01", periods=n, freq="h", tz="UTC"),
            "open": close,
            "high": [x + 1 for x in close],
            "low": [x - 1 for x in close],
            "close": close,
            "volume": [1000.0] * n,
        })


def test_financial_engine_uses_provider_and_records_source():
    assessment = FinancialEngine(provider=FailoverProvider()).analyze(limit=60)
    assert assessment.asset == "BTCUSDT"
    assert assessment.data_quality == 100.0
    assert assessment.evidence["provider"] == "coinbase"
    assert 0.0 <= assessment.confidence <= 100.0
