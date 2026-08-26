from __future__ import annotations
import pandas as pd
from financial_engine.core import assess
from phoenix_core.data_quality import assess_ohlcv
from phoenix_core.market_data import PublicMarketDataProvider
from .telegram import TelegramNotifier


def run_once(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 500) -> dict:
    provider = PublicMarketDataProvider()
    candles = provider.fetch_klines(symbol, interval, limit)
    df = pd.DataFrame([c.__dict__ for c in candles])
    quality = assess_ohlcv(df)
    result = assess(symbol, interval, df, quality.score)
    return {"assessment": result, "quality": quality}


def main() -> None:
    result = run_once()
    assessment = result["assessment"]
    notifier = TelegramNotifier()
    if assessment.direction != "neutral" and assessment.confidence >= 70 and assessment.data_quality >= 70:
        notifier.send(
            f"PHOENIX Market Alert\n{assessment.asset} {assessment.timeframe}\n"
            f"Direction: {assessment.direction}\nConfidence: {assessment.confidence}%\n"
            f"Data quality: {assessment.data_quality}%"
        )


if __name__ == "__main__":
    main()
