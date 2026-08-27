from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import math
import pandas as pd


@dataclass(frozen=True)
class MarketOpportunity:
    asset: str
    regime: str
    direction: str
    entry: float | None
    invalidation: float | None
    targets: tuple[float, ...]
    expected_return_pct: float
    probability_pct: float
    confidence_pct: float
    risk_reward: float
    score: float
    tradeable: bool
    reasons: tuple[str, ...]
    risks: tuple[str, ...]


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, math.nan)
    return 100 - (100 / (1 + rs))


def _atr(x: pd.DataFrame, period: int = 14) -> pd.Series:
    prev = x.close.shift(1)
    tr = pd.concat([
        x.high - x.low,
        (x.high - prev).abs(),
        (x.low - prev).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def analyze_market(df: pd.DataFrame, asset: str = "BTCUSDT") -> MarketOpportunity:
    required = {"timestamp", "close"}
    if not required.issubset(df.columns):
        raise ValueError("market data requires timestamp and close columns")
    x = df.copy().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    for col in ("close", "high", "low", "volume"):
        if col in x:
            x[col] = pd.to_numeric(x[col], errors="coerce")
    if "high" not in x:
        x["high"] = x.close
    if "low" not in x:
        x["low"] = x.close
    if "volume" not in x:
        x["volume"] = 0.0
    x = x.dropna(subset=["close", "high", "low"]).reset_index(drop=True)
    if len(x) < 60:
        return MarketOpportunity(asset.upper(), "unknown", "WAIT", None, None, (), 0.0, 0.0, 0.0, 0.0, 0.0, False, ("insufficient_history",), ())

    c = x.close
    ema20 = c.ewm(span=20, adjust=False).mean()
    ema50 = c.ewm(span=50, adjust=False).mean()
    ema200 = c.ewm(span=min(200, len(c)), adjust=False).mean()
    rsi = _rsi(c)
    atr = _atr(x).iloc[-1]
    price = float(c.iloc[-1])
    recent_high = float(c.iloc[-21:-1].max())
    recent_low = float(c.iloc[-21:-1].min())
    momentum = float(c.pct_change(20).iloc[-1] * 100)
    vol_ratio = float(x.volume.iloc[-1] / x.volume.rolling(20).mean().iloc[-1]) if x.volume.rolling(20).mean().iloc[-1] > 0 else 1.0

    if price > ema50.iloc[-1] and ema20.iloc[-1] > ema50.iloc[-1]:
        regime = "bullish_trend"
    elif price < ema50.iloc[-1] and ema20.iloc[-1] < ema50.iloc[-1]:
        regime = "bearish_trend"
    else:
        regime = "range_or_transition"

    long_score = 0.0
    short_score = 0.0
    reasons: list[str] = []
    risks: list[str] = []
    if price > ema20.iloc[-1] > ema50.iloc[-1]:
        long_score += 2.0; reasons.append("price_above_ema20_ema50")
    if price < ema20.iloc[-1] < ema50.iloc[-1]:
        short_score += 2.0; reasons.append("price_below_ema20_ema50")
    if rsi.iloc[-1] > 55:
        long_score += 1.0; reasons.append("positive_momentum")
    elif rsi.iloc[-1] < 45:
        short_score += 1.0; reasons.append("negative_momentum")
    if momentum > 2:
        long_score += 1.0
    elif momentum < -2:
        short_score += 1.0
    if vol_ratio > 1.2:
        reasons.append("volume_confirmation")
    if price > recent_high:
        long_score += 1.5; reasons.append("breakout_above_20d_high")
    if price < recent_low:
        short_score += 1.5; reasons.append("breakdown_below_20d_low")

    direction = "LONG" if long_score > short_score else "SHORT" if short_score > long_score else "WAIT"
    edge = max(long_score, short_score)
    # Probability is an evidence score, not a promise. It is intentionally capped
    # until calibrated out-of-sample probabilities are available.
    probability = min(75.0, 50.0 + edge * 5.0)
    confidence = min(80.0, 45.0 + abs(long_score - short_score) * 7.0)
    tradeable = direction != "WAIT" and probability >= 60 and atr > 0

    if direction == "LONG":
        entry = price
        invalidation = price - 1.5 * atr
        target1 = price + 2.0 * atr
        target2 = price + 3.5 * atr
    elif direction == "SHORT":
        entry = price
        invalidation = price + 1.5 * atr
        target1 = price - 2.0 * atr
        target2 = price - 3.5 * atr
    else:
        entry = invalidation = None
        target1 = target2 = price

    expected_return = abs(target1 / price - 1.0) * 100 if tradeable else 0.0
    risk_pct = abs(invalidation / price - 1.0) * 100 if tradeable else 0.0
    rr = expected_return / risk_pct if risk_pct else 0.0
    if regime == "range_or_transition":
        risks.append("market_regime_not_trending")
    if rsi.iloc[-1] > 70 or rsi.iloc[-1] < 30:
        risks.append("momentum_extreme")
    if vol_ratio < 0.7:
        risks.append("weak_volume")
    if not tradeable:
        risks.append("insufficient_confirmed_edge")

    return MarketOpportunity(
        asset=asset.upper(), regime=regime, direction=direction, entry=round(entry, 8) if entry else None,
        invalidation=round(invalidation, 8) if invalidation else None,
        targets=(round(target1, 8), round(target2, 8)) if tradeable else (),
        expected_return_pct=round(expected_return, 2), probability_pct=round(probability, 2),
        confidence_pct=round(confidence, 2), risk_reward=round(rr, 2), score=round(edge, 2),
        tradeable=tradeable, reasons=tuple(dict.fromkeys(reasons)), risks=tuple(dict.fromkeys(risks)),
    )
