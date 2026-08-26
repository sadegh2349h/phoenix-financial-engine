import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from financial_engine.radar import radar
from phoenix_core.market_data import PublicMarketDataProvider


def send_telegram(text: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urlencode({"chat_id": chat_id, "text": text}).encode()
    req = Request(url, data=data, method="POST")
    with urlopen(req, timeout=15) as response:
        if response.status != 200:
            raise RuntimeError(f"Telegram HTTP {response.status}")


def main() -> None:
    symbol = os.environ.get("PHOENIX_SYMBOL", "BTCUSDT")
    interval = os.environ.get("PHOENIX_INTERVAL", "5m")
    candles = PublicMarketDataProvider().fetch_klines(symbol, interval, 240)
    rows = [{"timestamp": c.timestamp, "open": c.open, "high": c.high, "low": c.low, "close": c.close, "volume": c.volume} for c in candles]
    import pandas as pd
    result = radar(symbol, interval, pd.DataFrame(rows), 100.0)
    payload = {
        "asset": result.asset,
        "timeframe": result.timeframe,
        "price": result.price,
        "score": result.score,
        "status": result.status,
        "confidence": result.confidence,
        "reasons": result.reasons,
    }
    print(json.dumps(payload, ensure_ascii=False))
    if result.status == "OPPORTUNITY" and result.confidence >= 70:
        send_telegram(f"PHOENIX MARKET RADAR\\n{symbol} {interval}\\nPrice: {result.price}\\nOpportunity score: {result.score}/100\\nConfidence: {result.confidence}/100\\n" + "\\n".join(f"- {r}" for r in result.reasons))


if __name__ == "__main__":
    main()
