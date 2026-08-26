import os
import requests
from financial_engine.core import assess
from phoenix_core.market_data import PublicMarketDataProvider
import pandas as pd

SYMBOLS = [s.strip().upper() for s in os.getenv("PHOENIX_SYMBOLS", "BTCUSDT,ETHUSDT").split(",") if s.strip()]
INTERVALS = [s.strip() for s in os.getenv("PHOENIX_INTERVALS", "5m,15m,1h,4h").split(",") if s.strip()]


def telegram(text: str) -> None:
    token, chat_id = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=15).raise_for_status()


def run() -> None:
    provider = PublicMarketDataProvider()
    alerts = []
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            candles = provider.fetch_klines(symbol, interval, 200)
            df = pd.DataFrame([c.__dict__ for c in candles])
            result = assess(symbol, interval, df)
            if result.confidence >= 75 and result.direction != "neutral":
                alerts.append(f"PHOENIX | {symbol} | {interval} | {result.direction} | confidence={result.confidence}%")
    if alerts:
        telegram("\n".join(alerts))

if __name__ == "__main__":
    run()
