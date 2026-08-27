import pandas as pd

from phoenix_core.financial_engine import FinancialEngine


class StubProvider:
    last_provider = "coinbase"

    def klines(self, symbol, interval, limit):
        n = max(limit, 80)
        idx = pd.date_range("2026-01-01", periods=n, freq="h")
        close = pd.Series(range(100, 100 + n), index=idx, dtype="float64")
        # Regression fixture: deliberately inject missing values in the path that
        # previously caused pandas.NA boolean ambiguity.
        close.iloc[10] = pd.NA
        volume = pd.Series(1000.0, index=idx)
        volume.iloc[15] = pd.NA
        filled = close.ffill()
        return pd.DataFrame({
            "open": filled - 0.5,
            "high": filled + 1,
            "low": filled - 1,
            "close": close,
            "volume": volume,
        })


def test_financial_engine_handles_pandas_na():
    result = FinancialEngine(provider=StubProvider()).analyze(limit=80)
    assert result.last_price > 0
    assert result.momentum in {"strong", "weak", "balanced"}
    assert 0 <= result.confidence <= 100
    assert result.evidence["provider"] == "coinbase"
