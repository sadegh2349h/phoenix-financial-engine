import pandas as pd

from phoenix_core.multi_source_analysis import cross_source_consensus
from phoenix_core.learning import OutcomeLedger


def _frame(direction: str) -> pd.DataFrame:
    n = 100
    prices = [100 + i * (1 if direction == "LONG" else -0.4) for i in range(n)]
    return pd.DataFrame({"timestamp": pd.date_range("2026-01-01", periods=n, freq="h"),
                         "open": prices, "high": [p + 1 for p in prices],
                         "low": [p - 1 for p in prices], "close": prices,
                         "volume": [1000] * n})


def test_cross_source_consensus(monkeypatch):
    from phoenix_core import multi_source_analysis as m
    monkeypatch.setattr(m.PublicMarketData, "_binance", lambda *a: _frame("LONG"))
    monkeypatch.setattr(m.PublicMarketData, "_coinbase", lambda *a: _frame("LONG"))
    result = cross_source_consensus()
    assert result.direction == "LONG"
    assert result.sources == 2
    assert result.agreement == 1.0


def test_learning_loop(tmp_path):
    ledger = OutcomeLedger(str(tmp_path / "predictions.jsonl"))
    ledger.record_prediction("p1", "BTCUSDT", "LONG", 0.8, 5, 100.0)
    assert ledger.close_outcome("p1", 2.0)
    assert ledger.metrics()["accuracy_pct"] == 100.0
