from __future__ import annotations

import pandas as pd
import numpy as np


def indicators(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    close = x["close"]
    x["ema20"] = close.ewm(span=20, adjust=False).mean()
    x["ema50"] = close.ewm(span=50, adjust=False).mean()
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    x["rsi14"] = 100 - (100 / (1 + rs))
    prev = close.shift(1)
    tr = pd.concat([
        x["high"] - x["low"],
        (x["high"] - prev).abs(),
        (x["low"] - prev).abs(),
    ], axis=1).max(axis=1)
    x["atr14"] = tr.rolling(14).mean()
    x["volume_ma20"] = x["volume"].rolling(20).mean()
    return x


def market_score(df: pd.DataFrame) -> dict:
    x = indicators(df)
    if len(x) < 50:
        return {"score": 50.0, "confidence": 0.0, "direction": "neutral", "evidence": ["insufficient_data"]}

    last = x.iloc[-1]
    score = 50.0
    evidence: list[str] = []

    if last.ema20 > last.ema50:
        score += 15
        evidence.append("ema20_above_ema50")
    elif last.ema20 < last.ema50:
        score -= 15
        evidence.append("ema20_below_ema50")

    if 50 <= last.rsi14 <= 70:
        score += 10
        evidence.append("positive_momentum")
    elif 30 <= last.rsi14 < 50:
        score -= 5
        evidence.append("weak_momentum")

    if pd.notna(last.volume_ma20) and last.volume_ma20 > 0:
        volume_ratio = last.volume / last.volume_ma20
        if volume_ratio >= 1.5:
            score += 10 if score >= 50 else -10
            evidence.append("elevated_volume")

    score = max(0.0, min(100.0, score))
    direction = "long" if score >= 70 else "short" if score <= 30 else "neutral"
    confidence = abs(score - 50) * 2
    return {
        "score": round(score, 2),
        "confidence": round(confidence, 2),
        "direction": direction,
        "evidence": evidence,
        "price": float(last.close),
        "rsi14": None if pd.isna(last.rsi14) else round(float(last.rsi14), 4),
        "atr14": None if pd.isna(last.atr14) else round(float(last.atr14), 6),
    }
