from __future__ import annotations

from typing import Any, Dict, List, Optional
import requests
import pandas as pd


class BinancePublicMarketData:
    """Public Spot market-data adapter; no account/API key is required."""

    BASE_URL = "https://api.binance.com"

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout

    def klines(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "1h",
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> pd.DataFrame:
        params: Dict[str, Any] = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": min(max(int(limit), 1), 1000),
        }
        if start_time is not None:
            params["startTime"] = int(start_time)
        if end_time is not None:
            params["endTime"] = int(end_time)

        response = requests.get(
            f"{self.BASE_URL}/api/v3/klines",
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        rows: List[List[Any]] = response.json()

        columns = [
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trade_count",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore",
        ]
        df = pd.DataFrame(rows, columns=columns)
        if df.empty:
            return df

        df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        for col in ["open", "high", "low", "close", "volume", "quote_volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["trade_count"] = pd.to_numeric(df["trade_count"], errors="coerce")
        return df[[
            "timestamp", "open", "high", "low", "close", "volume",
            "quote_volume", "trade_count", "open_time", "close_time"
        ]]
