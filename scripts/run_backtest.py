import json
import pandas as pd
from financial_engine.backtest import ema_cross_backtest
from phoenix_core.market_data import PublicMarketDataProvider


def run(symbol: str = "BTCUSDT", interval: str = "1h") -> dict:
    candles = PublicMarketDataProvider().fetch_klines(symbol, interval, 1000)
    df = pd.DataFrame([c.__dict__ for c in candles])
    return {
        "symbol": symbol,
        "interval": interval,
        "samples": len(df),
        "365_candle_baseline": ema_cross_backtest(df.tail(365)),
        "full_window": ema_cross_backtest(df),
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: (v.__dict__ if hasattr(v, "__dict__") else v) for k, v in result.items()}, default=str, indent=2))
