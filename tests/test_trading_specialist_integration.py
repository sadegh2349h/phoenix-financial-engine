from phoenix_core.trading_specialist import TradingSpecialist


def test_trading_specialist_requires_core_market_data():
    result = TradingSpecialist().analyze({"asset": "BTCUSDT", "timeframes": ["1d"]})
    assert result["status"] == "insufficient_data"
    assert "price_data" in result["missing"]


def test_trading_specialist_integrates_evidence_contract():
    result = TradingSpecialist().analyze({
        "asset": "BTCUSDT",
        "timeframes": ["1d", "4h", "1h"],
        "price_data": [1, 2, 3],
    })
    assert result["status"] == "ready"
    assert result["specialist"] == "trading_specialist"
    assert result["human_approval_required"] is True
    assert "multi_timeframe_technical_analysis" in result["evidence_required"]
    assert "risk_management" in result["evidence_required"]
    assert "backtesting" in result["evidence_required"]
