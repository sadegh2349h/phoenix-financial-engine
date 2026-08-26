from dataclasses import dataclass, asdict
from typing import List
import pandas as pd
import numpy as np


@dataclass(frozen=True)
class MarketAssessment:
    asset: str
    timeframe: str
    direction: str
    confidence: float
    data_quality: float
    trend_score: float
    momentum_score: float
    volatility_score: float
    volume_score: float
    reasons: List[str]


def indicators(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    c = x["close"]
    x["ema20"] = c.ewm(span=20, adjust=False).mean()
    x["ema50"] = c.ewm(span=50, adjust=False).mean()
    d = c.diff()
    gain = d.clip(lower=0).rolling(14).mean()
    loss = -d.clip(upper=0).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    x["rsi14"] = 100 - (100 / (1 + rs))
    prev = c.shift(1)
    tr = pd.concat([x["high"]-x["low"], (x["high"]-prev).abs(), (x["low"]-prev).abs()], axis=1).max(axis=1)
    x["atr14"] = tr.rolling(14).mean()
    x["volume_ma20"] = x["volume"].rolling(20).mean()
    return x


def assess(asset: str, timeframe: str, df: pd.DataFrame, data_quality: float = 100.0) -> MarketAssessment:
    x = indicators(df)
    last = x.iloc[-1]
    trend = 0.0
    momentum = 50.0
    volatility = 50.0
    volume = 50.0
    reasons = []

    if last.ema20 > last.ema50:
        trend = 100.0; reasons.append("EMA20 above EMA50")
    elif last.ema20 < last.ema50:
        trend = 0.0; reasons.append("EMA20 below EMA50")
    else:
        trend = 50.0

    if pd.notna(last.rsi14):
        momentum = float(max(0, min(100, last.rsi14)))
        if 50 <= last.rsi14 <= 70: reasons.append("RSI supports positive momentum")
        elif 30 <= last.rsi14 < 50: reasons.append("RSI indicates weaker momentum")

    if pd.notna(last.atr14) and last.close:
        atr_pct = float(last.atr14 / last.close * 100)
        volatility = max(0.0, min(100.0, 50 + atr_pct * 5))

    if pd.notna(last.volume_ma20) and last.volume_ma20 > 0:
        volume = max(0.0, min(100.0, float(last.volume / last.volume_ma20 * 50)))
        if last.volume > last.volume_ma20: reasons.append("Volume above 20-period average")

    score = 0.40 * trend + 0.30 * momentum + 0.20 * volume + 0.10 * volatility
    confidence = 0.70 * score + 0.30 * data_quality
    direction = "long" if score >= 65 else "short" if score <= 35 else "neutral"

    return MarketAssessment(asset, timeframe, direction, round(confidence, 2), round(data_quality, 2), round(trend, 2), round(momentum, 2), round(volatility, 2), round(volume, 2), reasons)
