from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, List
import requests
import pandas as pd


class PublicMarketData:
    """Provider-neutral public market data with paginated multi-source failover."""

    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout
        self.last_provider = None
        self.provider_history: list[str] = []

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
        """Paginate Binance klines instead of assuming one request is sufficient."""
        requested = min(max(limit, 1), 5000)
        frames: list[pd.DataFrame] = []
        end_time: int | None = None
        remaining = requested
        while remaining > 0:
            count = min(remaining, 1000)
            params = {"symbol": symbol.upper(), "interval": interval, "limit": count}
            if end_time is not None:
                params["endTime"] = end_time
            response = requests.get(
                "https://api.binance.com/api/v3/klines",
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            raw = response.json()
            if not raw:
                break
            frame = self._frame(raw)
            frames.append(frame)
            remaining -= len(frame)
            if len(frame) < count:
                break
            oldest_ms = int(raw[0][0])
            end_time = oldest_ms - 1
        if not frames:
            return self._frame([])
        return (
            pd.concat(frames, ignore_index=True)
            .drop_duplicates("timestamp")
            .sort_values("timestamp")
            .tail(requested)
            .reset_index(drop=True)
        )

    def _coinbase(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        mapping = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600, "2h": 7200, "6h": 21600, "1d": 86400}
        if interval not in mapping:
            raise ValueError(f"Unsupported interval for Coinbase fallback: {interval}")
        granularity = mapping[interval]
        requested = min(max(limit, 1), 1000)
        frames: list[pd.DataFrame] = []
        end = datetime.now(timezone.utc)
        remaining = requested
        while remaining > 0:
            count = min(remaining, 300)
            start = end - timedelta(seconds=granularity * count)
            response = requests.get(
                f"https://api.exchange.coinbase.com/products/{self._coinbase_product(symbol)}/candles",
                params={"granularity": granularity, "start": start.isoformat(), "end": end.isoformat()},
                timeout=self.timeout,
            )
            response.raise_for_status()
            raw = response.json()
            if not raw:
                break
            frame = self._frame([[int(r[0]) * 1000, r[3], r[2], r[1], r[4], r[5]] for r in raw])
            frames.append(frame)
            oldest = frame["timestamp"].min().to_pydatetime()
            end = oldest - timedelta(seconds=granularity)
            remaining -= len(frame)
            if len(frame) < count:
                break
        if not frames:
            return self._frame([])
        return pd.concat(frames, ignore_index=True).drop_duplicates("timestamp").sort_values("timestamp").tail(requested).reset_index(drop=True)

    def klines(self, symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 300) -> pd.DataFrame:
        errors: list[str] = []
        for provider_name, provider in (("binance", self._binance), ("coinbase", self._coinbase)):
            try:
                df = provider(symbol, interval, limit)
                if len(df) >= min(limit, 30):
                    self.last_provider = provider_name
                    self.provider_history.append(provider_name)
                    return df
                errors.append(f"{provider_name}: only {len(df)} rows")
            except (requests.RequestException, ValueError) as exc:
                errors.append(f"{provider_name}: {type(exc).__name__}")
        raise RuntimeError("No market-data provider returned sufficient history: " + "; ".join(errors))


BinancePublicMarketData = PublicMarketData
