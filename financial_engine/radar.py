from dataclasses import dataclass
from typing import Dict, List
import pandas as pd


@dataclass(frozen=True)
class RadarResult:
    asset: str
    timeframe: str
    price: float
    score: float
    status: str
    confidence: float
    reasons: List[str]


def radar(asset: str, timeframe: str, df: pd.DataFrame, quality: float = 100.0) -> RadarResult:
    x = df.copy()
    x["ema20"] = x.close.ewm(span=20, adjust=False).mean()
    x["ema50"] = x.close.ewm(span=50, adjust=False).mean()
    delta = x.close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, pd.NA)
    x["rsi"] = 100 - 100 / (1 + rs)
    x["vol_ma"] = x.volume.rolling(20).mean()
    last = x.iloc[-1]

    score = 50.0
    reasons: List[str] = []
    if last.ema20 > last.ema50:
        score += 20; reasons.append("short-term trend is above medium-term trend")
    else:
        score -= 20; reasons.append("short-term trend is below medium-term trend")
    if pd.notna(last.rsi):
        if 50 <= last.rsi <= 70:
            score += 15; reasons.append("momentum is supportive")
        elif last.rsi < 45:
            score -= 10; reasons.append("momentum is weak")
    if pd.notna(last.vol_ma) and last.vol_ma > 0 and last.volume > last.vol_ma:
        score += 10; reasons.append("volume is above its 20-period average")
    score = max(0.0, min(100.0, score))
    confidence = round(0.7 * score + 0.3 * quality, 2)
    status = "OPPORTUNITY" if score >= 70 and quality >= 70 else "WATCH" if score >= 55 else "NO_OPPORTUNITY"
    return RadarResult(asset, timeframe, float(last.close), round(score, 2), status, confidence, reasons)
