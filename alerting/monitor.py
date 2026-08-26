from __future__ import annotations
import json
from datetime import datetime, timezone
from phoenix_core.market_data import PublicMarketData
from phoenix_core.data_quality import assess_ohlcv
from financial_engine.core import assess
from .telegram import TelegramNotifier


def run_once(symbol="BTCUSDT", interval="1h", limit=300):
    df = PublicMarketData().klines(symbol, interval, limit)
    quality = assess_ohlcv(df)
    result = assess(symbol, interval, df, quality.score)
    return result, quality


def main():
    result, quality = run_once()
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "asset": result.asset,
        "timeframe": result.timeframe,
        "direction": result.direction,
        "confidence": result.confidence,
        "data_quality": quality.score,
        "reasons": result.reasons,
    }
    print(json.dumps(payload, ensure_ascii=False))
    if result.direction != "neutral" and result.confidence >= 70 and quality.score >= 70:
        TelegramNotifier().send(
            "PHOENIX ALERT\n"
            f"{result.asset} {result.timeframe}\n"
            f"Direction: {result.direction}\n"
            f"Confidence: {result.confidence}%\n"
            f"Data quality: {quality.score}%\n"
            "Research alert - not an automatic trade."
        )


if __name__ == "__main__":
    main()
