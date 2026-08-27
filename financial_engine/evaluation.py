from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from .backtest import BacktestResult, ema_cross_backtest


@dataclass(frozen=True)
class ShadowEvaluation:
    asset: str
    window_days: int
    strategy: BacktestResult
    buy_and_hold_return_pct: float
    excess_return_pct: float
    passed_data_contract: bool


def shadow_evaluate(
    df: pd.DataFrame,
    *,
    asset: str,
    window_days: int,
    initial_capital: float = 50_000_000.0,
    fee_bps: float = 5.0,
    slippage_bps: float = 5.0,
) -> ShadowEvaluation:
    """Evaluate a strategy without placing orders and without look-ahead leakage."""
    if window_days not in {30, 365}:
        raise ValueError("window_days must be 30 or 365")
    required = {"timestamp", "close"}
    if not required.issubset(df.columns):
        raise ValueError("market data requires timestamp and close columns")
    x = df.copy().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    x["close"] = pd.to_numeric(x["close"], errors="coerce")
    x = x.dropna(subset=["close"])
    if len(x) < max(60, window_days):
        raise ValueError("insufficient history for requested evaluation window")
    x = x.tail(window_days).reset_index(drop=True)
    buy_hold = float((x["close"].iloc[-1] / x["close"].iloc[0] - 1.0) * 100.0)
    result = ema_cross_backtest(
        x,
        initial_capital=initial_capital,
        fee_bps=fee_bps,
        slippage_bps=slippage_bps,
    )
    return ShadowEvaluation(
        asset=asset.upper(),
        window_days=window_days,
        strategy=result,
        buy_and_hold_return_pct=round(buy_hold, 2),
        excess_return_pct=round(result.total_return_pct - buy_hold, 2),
        passed_data_contract=True,
    )
