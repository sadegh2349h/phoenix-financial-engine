from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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
    warmup_rows: int


def shadow_evaluate(
    df: pd.DataFrame,
    *,
    asset: str,
    window_days: int,
    initial_capital: float = 50_000_000.0,
    fee_bps: float = 5.0,
    slippage_bps: float = 5.0,
) -> ShadowEvaluation:
    """Evaluate a strategy on a held-out window with optional indicator warmup.

    Warmup is used whenever the caller supplies extra history.  A deterministic
    fixture containing exactly the requested evaluation window remains valid;
    it simply has zero warmup rather than being rejected.
    """
    if window_days not in {30, 365}:
        raise ValueError("window_days must be 30 or 365")
    required = {"timestamp", "close"}
    if not required.issubset(df.columns):
        raise ValueError("market data requires timestamp and close columns")

    x = df.copy().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    x["close"] = pd.to_numeric(x["close"], errors="coerce")
    x = x.dropna(subset=["close"]).reset_index(drop=True)
    if len(x) < window_days:
        raise ValueError("insufficient history for requested evaluation window")

    available_extra = len(x) - window_days
    warmup = min(50, available_extra)
    x = x.tail(window_days + warmup).reset_index(drop=True)
    evaluation_start = warmup
    eval_prices = x.iloc[evaluation_start:]["close"]
    buy_hold = float((eval_prices.iloc[-1] / eval_prices.iloc[0] - 1.0) * 100.0)
    result = ema_cross_backtest(
        x,
        initial_capital=initial_capital,
        fee_bps=fee_bps,
        slippage_bps=slippage_bps,
        evaluation_start=evaluation_start,
    )
    return ShadowEvaluation(
        asset=asset.upper(),
        window_days=window_days,
        strategy=result,
        buy_and_hold_return_pct=round(buy_hold, 2),
        excess_return_pct=round(result.total_return_pct - buy_hold, 2),
        passed_data_contract=True,
        warmup_rows=warmup,
    )
