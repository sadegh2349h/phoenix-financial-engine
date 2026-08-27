import pandas as pd

from financial_engine.market_intelligence import analyze_market


def series(n=260):
    close = [100 + i * 0.35 + (i % 5) * 0.05 for i in range(n)]
    return pd.DataFrame({
        "timestamp": pd.date_range("2025-01-01", periods=n, freq="D", tz="UTC"),
        "open": close,
        "high": [p + 1 for p in close],
        "low": [p - 1 for p in close],
        "close": close,
        "volume": [1000 + (i % 10) * 100 for i in range(n)],
    })


def test_market_intelligence_is_deterministic_and_has_risk_gate():
    a = analyze_market(series(), "BTCUSDT")
    b = analyze_market(series(), "BTCUSDT")
    assert a == b
    assert a.direction in {"LONG", "SHORT", "WAIT"}
    assert 0 <= a.probability_pct <= 75
    assert 0 <= a.confidence_pct <= 80
    if a.tradeable:
        assert a.entry is not None
        assert a.invalidation is not None
        assert a.targets
        assert a.risk_reward > 0


def test_market_intelligence_refuses_insufficient_history():
    result = analyze_market(series(20), "BTCUSDT")
    assert result.tradeable is False
    assert result.direction == "WAIT"
    assert "insufficient_history" in result.reasons
