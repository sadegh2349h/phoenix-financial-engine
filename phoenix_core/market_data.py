from dataclasses import dataclass
from typing import Any, Dict, List
import requests


@dataclass(frozen=True)
class Candle:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class PublicMarketDataProvider:
    """Public Binance market-data adapter; provider-specific details stay isolated."""

    BASE_URL = "https://api.binance.com/api/v3/klines"

    def fetch_klines(self, symbol: str, interval: str = "1h", limit: int = 500) -> List[Candle]:
        response = requests.get(
            self.BASE_URL,
            params={"symbol": symbol.upper(), "interval": interval, "limit": limit},
            timeout=15,
        )
        response.raise_for_status()
        rows = response.json()
        return [
            Candle(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]))
            for r in rows
        ]
