from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class SignalSnapshot:
    score: float
    regime: str
    signal: int
    reasons: tuple[str, ...]


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    c = pd.to_numeric(x["close"], errors="coerce")
    x["close"] = c
    x["ema20"] = c.ewm(span=20, adjust=False).mean()
    x["ema50"] = c.ewm(span=50, adjust=False).mean()
    x["ema100"] = c.ewm(span=100, adjust=False).mean()
    x["rsi14"] = _rsi(c)
    x["momentum20"] = c.pct_change(20)
    x["volatility20"] = c.pct_change().rolling(20).std()
    x["atr_pct"] = x["volatility20"]
    if "high" in x and "low" in x:
        prev = c.shift(1)
        tr = pd.concat([(x["high"] - x["low"]).abs(), (x["high"] - prev).abs(), (x["low"] - prev).abs()], axis=1).max(axis=1)
        x["atr_pct"] = tr.rolling(14).mean() / c
    if "volume" in x:
        v = pd.to_numeric(x["volume"], errors="coerce")
        x["volume_ratio"] = v / v.rolling(20).mean()
    else:
        x["volume_ratio"] = 1.0
    return x


def score_row(row: pd.Series) -> SignalSnapshot:
    close = float(row["close"])
    ema20, ema50, ema100 = float(row["ema20"]), float(row["ema50"]), float(row["ema100"])
    rsi = float(row["rsi14"]) if pd.notna(row["rsi14"]) else 50.0
    mom = float(row["momentum20"]) if pd.notna(row["momentum20"]) else 0.0
    vol = float(row["volatility20"]) if pd.notna(row["volatility20"]) else 0.0
    vr = float(row["volume_ratio"]) if pd.notna(row["volume_ratio"]) else 1.0

    trend = 1.0 if ema20 > ema50 > ema100 else 0.0
    momentum = max(0.0, min(1.0, 0.5 + mom * 5.0))
    momentum *= 1.0 if 50 <= rsi <= 72 else 0.75 if 45 <= rsi < 50 or 72 < rsi <= 78 else 0.4
    volume = max(0.0, min(1.0, 0.5 + (vr - 1.0) * 0.75))
    regime = "high_volatility" if vol > 0.045 else "low_volatility" if vol < 0.012 else "normal"
    if trend and momentum >= 0.55:
        regime = "bull_trend" if regime == "normal" else regime
    score = 0.45 * trend + 0.35 * momentum + 0.20 * volume
    reasons = []
    if trend: reasons.append("multi_ema_trend_alignment")
    if momentum >= 0.55: reasons.append("positive_momentum")
    if 50 <= rsi <= 72: reasons.append("healthy_rsi")
    if vr > 1.1: reasons.append("volume_confirmation")
    if close > ema20: reasons.append("price_above_ema20")
    signal = 1 if score >= 0.68 and regime != "high_volatility" else 0
    return SignalSnapshot(round(score, 4), regime, signal, tuple(reasons))
