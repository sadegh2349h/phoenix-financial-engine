from phoenix_core.trading_specialist import TradingSpecialist


def _valid_market():
    rows = [
        {"open": 100 + i, "high": 102 + i, "low": 99 + i, "close": 101 + i, "volume": 10 + i}
        for i in range(100)
    ]
    return {
        "asset": "BTCUSDT",
        "timeframes": ["1d", "4h", "1h"],
        "price_data": {"1d": rows, "4h": rows, "1h": rows},
        "evidence": {
            "technical_analysis": True,
            "fundamental_analysis": True,
            "sentiment_analysis": True,
            "positioning_analysis": True,
            "backtest": {
                "passed": True,
                "out_of_sample": True,
                "costs_included": True,
                "trades": 40,
            },
        },
        "risk": {
            "stop_loss_defined": True,
            "circuit_breakers_enabled": True,
            "position_size_pct": 0.5,
            "risk_reward_ratio": 2.0,
            "max_drawdown_pct": 8.0,
            "daily_loss_pct": 1.0,
        },
        "candidate_signal": "BUY",
    }


def test_trading_specialist_requires_core_market_data():
    result = TradingSpecialist().analyze({"asset": "BTCUSDT", "timeframes": ["1d"]})
    assert result["status"] == "insufficient_data"
    assert "price_data" in result["missing"]
    assert result["decision"] == "NO_TRADE"


def test_trading_specialist_rejects_unstructured_price_data():
    market = _valid_market()
    market["price_data"] = [1, 2, 3]
    result = TradingSpecialist().analyze(market)
    assert result["status"] == "blocked"
    assert result["decision"] == "NO_TRADE"
    assert any("mapping" in item for item in result["blockers"])


def test_trading_specialist_blocks_missing_risk_or_backtest_evidence():
    market = _valid_market()
    market["risk"]["stop_loss_defined"] = False
    market["evidence"]["backtest"]["costs_included"] = False
    result = TradingSpecialist().analyze(market)
    assert result["status"] == "blocked"
    assert result["decision"] == "NO_TRADE"
    assert any("stop_loss_defined" in item for item in result["blockers"])
    assert any("costs_included" in item for item in result["blockers"])


def test_trading_specialist_requires_human_review_after_all_gates_pass():
    result = TradingSpecialist().analyze(_valid_market())
    assert result["status"] == "ready_for_human_review"
    assert result["decision"] == "BUY"
    assert result["risk_gate"] == "passed"
    assert result["backtest_gate"] == "passed"
    assert result["confidence"] == 0.0
    assert result["human_approval_required"] is True


def test_trading_specialist_rejects_inconsistent_ohlc():
    market = _valid_market()
    market["price_data"]["1h"][0]["high"] = 99
    result = TradingSpecialist().analyze(market)
    assert result["status"] == "blocked"
    assert result["decision"] == "NO_TRADE"
    assert any("OHLC consistency" in item for item in result["blockers"])
