from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
import math
import pandas as pd

from .data_quality import assess_ohlcv
from .market_data import PublicMarketData


@dataclass(frozen=True)
class MarketAssessment:
    asset: str
    timeframe: str
    last_price: float
    trend: str
    momentum: str
    volatility: float
    volume_ratio: float
    confidence: float
    data_quality: float
    evidence: Dict[str, Any]


def _finite_float(value: Any, default: float = 0.0) -> float:
    """Convert scalar-like values safely; pandas.NA must never enter bool/arithmetic logic."""
    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


class FinancialEngine:
    """Research engine: provider -> quality -> indicators -> structured assessment."""

    def __init__(self, provider: PublicMarketData | None = None) -> None:
        self.provider = provider or PublicMarketData()

    def analyze(self, symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 500) -> MarketAssessment:
        df = self.provider.klines(symbol, interval, limit)
        quality = assess_ohlcv(df)
        if len(df) < 60:
            raise ValueError("Insufficient market history for assessment")

        close = pd.to_numeric(df["close"], errors="coerce")
        high = pd.to_numeric(df["high"], errors="coerce")
        low = pd.to_numeric(df["low"], errors="coerce")
        volume = pd.to_numeric(df["volume"], errors="coerce")
        df = df.copy()
        df["close"], df["high"], df["low"], df["volume"] = close, high, low, volume

        close = close.ffill()
        high = high.ffill()
        low = low.ffill()
        volume = volume.fillna(0.0)

        ema20 = close.ewm(span=20, adjust=False).mean()
        ema50 = close.ewm(span=50, adjust=False).mean()
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14, min_periods=14).mean()
        loss = (-delta.clip(upper=0)).rolling(14, min_periods=14).mean()
        rs = gain / loss.replace(0, float("nan"))
        rsi = (100 - (100 / (1 + rs))).fillna(50.0)
        tr = pd.concat([
            high - low,
            (high - close.shift(1)).abs(),
            (low - close.shift(1)).abs(),
        ], axis=1).max(axis=1)
        atr = tr.rolling(14, min_periods=14).mean().bfill()
        volume_ma = volume.rolling(20, min_periods=1).mean()

        last = df.iloc[-1]
        e20 = _finite_float(ema20.iloc[-1])
        e50 = _finite_float(ema50.iloc[-1])
        r = _finite_float(rsi.iloc[-1], 50.0)
        a = _finite_float(atr.iloc[-1])
        vm = _finite_float(volume_ma.iloc[-1])
        last_close = _finite_float(last["close"])
        last_volume = _finite_float(last["volume"])

        if e20 > e50:
            trend = "bullish"
        elif e20 < e50:
            trend = "bearish"
        else:
            trend = "neutral"

        momentum = "strong" if r >= 60 else "weak" if r <= 40 else "balanced"
        volume_ratio = last_volume / vm if vm > 0 else 0.0
        volatility = a / last_close if last_close > 0 else 0.0

        score = 50.0
        if trend == "bullish": score += 15
        elif trend == "bearish": score -= 15
        if r >= 60: score += 10
        elif r <= 40: score -= 10
        if volume_ratio >= 1.5:
            score += 5 if trend == "bullish" else -5 if trend == "bearish" else 0
        confidence = max(0.0, min(100.0, score * 0.7 + _finite_float(quality.score) * 0.3))

        return MarketAssessment(
            asset=symbol.upper(), timeframe=interval, last_price=last_close,
            trend=trend, momentum=momentum, volatility=volatility,
            volume_ratio=round(volume_ratio, 4), confidence=round(confidence, 2),
            data_quality=_finite_float(quality.score),
            evidence={
                "ema20": e20, "ema50": e50, "rsi14": r, "atr14": a,
                "provider": self.provider.last_provider,
            },
        )
