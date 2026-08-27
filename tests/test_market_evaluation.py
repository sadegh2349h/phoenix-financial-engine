import pandas as pd
import pytest

from financial_engine.evaluation import shadow_evaluate


def make_series(n=365):
    close = [100.0 + i * 0.2 + (i % 7) * 0.1 for i in range(n)]
    return pd.DataFrame({
        "timestamp": pd.date_range("2025-08-01", periods=n, freq="D", tz="UTC"),
        "close": close,
    })


def test_shadow_evaluation_is_deterministic_and_benchmarked():
    result = shadow_evaluate(make_series(), asset="BTCUSDT", window_days=365)
    assert result.asset == "BTCUSDT"
    assert result.window_days == 365
    assert result.passed_data_contract is True
    assert result.strategy.final_equity > 0
    assert result.excess_return_pct == round(
        result.strategy.total_return_pct - result.buy_and_hold_return_pct, 2
    )


def test_shadow_evaluation_rejects_invalid_window():
    with pytest.raises(ValueError):
        shadow_evaluate(make_series(), asset="BTCUSDT", window_days=90)
