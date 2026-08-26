from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
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


class FinancialEngine:
    """Research engine: provider -> quality -> indicators -> structured assessment."""

    def __init__(self, provider: PublicMarketData | None = None) -> None:
        self.provider = provider or PublicMarketData()

    def analyze(self, symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 500) -> MarketAssessment:
        df = self.provider.klines(symbol, interval, limit)
        quality = assess_ohlcv(df)
        if len(df) < 60:
            raise ValueError("Insufficient market history for assessment")

        close = df["close"]
        ema20 = close.ewm(span=20, adjust=False).mean()
        ema50 = close.ewm(span=50, adjust=False).mean()
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss.replace(0, pd.NA)
        rsi = 100 - (100 / (1 + rs))
        tr = pd.concat([
            df["high"] - df["low"],
            (df["high"] - close.shift(1)).abs(),
            (df["low"] - close.shift(1)).abs(),
        ], axis=1).max(axis=1)
        atr = tr.rolling(14).mean()
        volume_ma = df["volume"].rolling(20).mean()

        last = df.iloc[-1]
        e20, e50, r, a, vm = ema20.iloc[-1], ema50.iloc[-1], rsi.iloc[-1], atr.iloc[-1], volume_ma.iloc[-1]
        trend = "bullish" if e20 > e50 else "bearish" if e20 < e50 else "neutral"
        momentum = "strong" if r >= 60 else "weak" if r <= 40 else "balanced"
        volume_ratio = float(last["volume"] / vm) if vm and vm > 0 else 0.0
        volatility = float(a / last["close"]) if last["close"] else 0.0

        score = 50.0
        if trend == "bullish": score += 15
        elif trend == "bearish": score -= 15
        if r >= 60: score += 10
        elif r <= 40: score -= 10
        if volume_ratio >= 1.5: score += 5 if trend == "bullish" else -5 if trend == "bearish" else 0
        confidence = max(0.0, min(100.0, score * 0.7 + quality.score * 0.3))

        return MarketAssessment(
            asset=symbol.upper(), timeframe=interval, last_price=float(last["close"]),
            trend=trend, momentum=momentum, volatility=volatility,
            volume_ratio=round(volume_ratio, 4), confidence=round(confidence, 2),
            data_quality=quality.score,
            evidence={"ema20": float(e20), "ema50": float(e50), "rsi14": float(r), "atr14": float(a), "provider": self.provider.last_provider},
        )
