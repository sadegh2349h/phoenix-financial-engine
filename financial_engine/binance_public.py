from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import requests


@dataclass(frozen=True)
class BinancePublicConfig:
    base_url: str = "https://data-api.binance.vision"
    timeout_seconds: int = 10


class BinancePublicMarketData:
    """Public, unauthenticated Binance Spot market-data adapter.

    This adapter never requests account data and never places trades.
    """

    def __init__(self, config: BinancePublicConfig | None = None) -> None:
        self.config = config or BinancePublicConfig()

    def klines(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "5m",
        limit: int = 1000,
        start_time_ms: int | None = None,
        end_time_ms: int | None = None,
    ) -> pd.DataFrame:
        if not 1 <= limit <= 1000:
            raise ValueError("limit must be between 1 and 1000")

        params: dict[str, Any] = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit,
        }
        if start_time_ms is not None:
            params["startTime"] = start_time_ms
        if end_time_ms is not None:
            params["endTime"] = end_time_ms

        url = f"{self.config.base_url}/api/v3/klines"
        response = requests.get(url, params=params, timeout=self.config.timeout_seconds)
        response.raise_for_status()
        rows = response.json()

        columns = [
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trade_count", "taker_buy_base",
            "taker_buy_quote", "ignore",
        ]
        frame = pd.DataFrame(rows, columns=columns)
        if frame.empty:
            return frame

        numeric = ["open", "high", "low", "close", "volume", "quote_volume", "trade_count", "taker_buy_base", "taker_buy_quote"]
        for column in numeric:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

        frame["timestamp"] = pd.to_datetime(frame["open_time"], unit="ms", utc=True)
        frame["close_timestamp"] = pd.to_datetime(frame["close_time"], unit="ms", utc=True)
        frame = frame[["timestamp", "open", "high", "low", "close", "volume", "quote_volume", "trade_count", "taker_buy_base", "taker_buy_quote", "close_timestamp"]]
        return frame.sort_values("timestamp").reset_index(drop=True)

    def latest_price(self, symbol: str = "BTCUSDT") -> dict[str, Any]:
        url = f"{self.config.base_url}/api/v3/ticker/price"
        response = requests.get(url, params={"symbol": symbol.upper()}, timeout=self.config.timeout_seconds)
        response.raise_for_status()
        payload = response.json()
        return {
            "symbol": payload["symbol"],
            "price": float(payload["price"]),
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
        }
