from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class StrategyDiagnosis:
    root_causes: tuple[str, ...]
    regime: str
    signal_quality: float
    trade_count: int
    recommendation: str


def diagnose_strategy(df: pd.DataFrame, *, trades: int = 0) -> StrategyDiagnosis:
    if not {"timestamp", "close"}.issubset(df.columns):
        return StrategyDiagnosis(("missing_market_data",), "unknown", 0.0, trades, "NO_TRADE")
    close = pd.to_numeric(df.sort_values("timestamp")["close"], errors="coerce").dropna()
    if len(close) < 60:
        return StrategyDiagnosis(("insufficient_history",), "unknown", 0.0, trades, "NO_TRADE")
    ema20 = close.ewm(span=20, adjust=False).mean()
    ema50 = close.ewm(span=50, adjust=False).mean()
    spread = float((ema20.iloc[-1] - ema50.iloc[-1]) / close.iloc[-1])
    regime = "range" if abs(spread) < 0.005 else ("bull" if spread > 0 else "bear")
    causes = []
    if trades < 10:
        causes.append("too_few_trades_for_statistical_confidence")
    if regime == "range":
        causes.append("ema_trend_strategy_is_vulnerable_to_whipsaw_in_range_markets")
    causes.append("single_factor_price_signal_without_volume_sentiment_or_macro_confirmation")
    quality = max(0.0, min(1.0, abs(spread) / 0.03))
    recommendation = "TRADE_CANDIDATE" if quality >= 0.5 and trades >= 10 else "NO_TRADE"
    return StrategyDiagnosis(tuple(causes), regime, round(quality, 4), trades, recommendation)
