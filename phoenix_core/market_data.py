from __future__ import annotations

from typing import Any, List
import requests
import pandas as pd


class PublicMarketData:
    """Provider-neutral public market data with Binance -> Coinbase failover."""

    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout
        self.last_provider = None

    @staticmethod
    def _frame(rows: List[List[Any]]) -> pd.DataFrame:
        columns = ["open_time", "open", "high", "low", "close", "volume"]
        df = pd.DataFrame(rows, columns=columns)
        if df.empty:
            return df
        df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        for col in columns[1:]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    @staticmethod
    def _coinbase_product(symbol: str) -> str:
        s = symbol.upper()
        if s.endswith("USDT"):
            base = s[:-4]
        elif s.endswith("USD"):
            base = s[:-3]
        else:
            raise ValueError(f"Coinbase fallback requires a USD/USDT symbol: {symbol}")
        return f"{base}-USD"

    def _binance(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        response = requests.get(
            "https://api.binance.com/api/v3/klines",
            params={"symbol": symbol.upper(), "interval": interval, "limit": min(max(limit, 1), 1000)},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return self._frame(response.json())

    def _coinbase(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        mapping = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600, "2h": 7200, "6h": 21600, "1d": 86400}
        if interval not in mapping:
            raise ValueError(f"Unsupported interval for Coinbase fallback: {interval}")
        response = requests.get(
            f"https://api.exchange.coinbase.com/products/{self._coinbase_product(symbol)}/candles",
            params={"granularity": mapping[interval]},
            timeout=self.timeout,
        )
        response.raise_for_status()
        rows = response.json()[-min(max(limit, 1), 300):]
        rows = [[int(r[0]) * 1000, r[3], r[2], r[1], r[4], r[5]] for r in rows]
        return self._frame(rows).sort_values("timestamp").reset_index(drop=True)

    def klines(self, symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 300) -> pd.DataFrame:
        try:
            df = self._binance(symbol, interval, limit)
            self.last_provider = "binance"
            return df
        except requests.RequestException:
            df = self._coinbase(symbol, interval, limit)
            self.last_provider = "coinbase"
            return df


BinancePublicMarketData = PublicMarketData
