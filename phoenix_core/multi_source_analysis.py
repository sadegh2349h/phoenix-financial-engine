from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import pandas as pd

from .market_data import PublicMarketData


@dataclass(frozen=True)
class SourceSignal:
    provider: str
    close: float
    direction: str
    quality: float


@dataclass(frozen=True)
class Consensus:
    direction: str
    confidence: float
    agreement: float
    sources: int
    details: Dict[str, SourceSignal]


def _direction(df: pd.DataFrame) -> str:
    if len(df) < 55:
        return "NEUTRAL"
    close = df["close"]
    ema20 = close.ewm(span=20, adjust=False).mean().iloc[-1]
    ema50 = close.ewm(span=50, adjust=False).mean().iloc[-1]
    return "LONG" if ema20 > ema50 else "SHORT"


def cross_source_consensus(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 200) -> Consensus:
    """Compare independent public sources and only raise confidence when they agree."""
    client = PublicMarketData()
    details: Dict[str, SourceSignal] = {}
    providers = {"binance": client._binance, "coinbase": client._coinbase}
    for name, fetcher in providers.items():
        try:
            frame = fetcher(symbol, interval, limit)
            if frame.empty or frame["close"].isna().any():
                continue
            quality = min(1.0, len(frame) / max(limit, 1))
            details[name] = SourceSignal(name, float(frame["close"].iloc[-1]), _direction(frame), quality)
        except Exception:
            continue
    if not details:
        return Consensus("NEUTRAL", 0.0, 0.0, 0, {})
    directions = [s.direction for s in details.values()]
    best = max(set(directions), key=directions.count)
    agreement = directions.count(best) / len(directions)
    confidence = round(agreement * sum(s.quality for s in details.values()) / len(details), 4)
    return Consensus(best, confidence, agreement, len(details), details)
