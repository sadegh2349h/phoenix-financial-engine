from __future__ import annotations
import pandas as pd
from phoenix_core.market_data import BinancePublicMarketData
from phoenix_core.data_quality import assess_ohlcv
from financial_engine.core import assess
from .telegram import TelegramNotifier

def run_once(symbol="BTCUSDT", interval="1h", limit=500):
    df=BinancePublicMarketData().klines(symbol,interval,limit)
    quality=assess_ohlcv(df)
    result=assess(symbol,interval,df,quality.score)
    return result,quality

def main():
    result,quality=run_once()
    if result.direction!="neutral" and result.confidence>=70 and quality.score>=70:
        TelegramNotifier().send(f"PHOENIX ALERT\n{result.asset} {result.timeframe}\nDirection: {result.direction}\nConfidence: {result.confidence}%\nData quality: {quality.score}%")

if __name__=="__main__": main()
