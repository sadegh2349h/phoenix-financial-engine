from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class BacktestResult:
    trades: int
    wins: int
    losses: int
    win_rate_pct: float
    total_return_pct: float
    max_drawdown_pct: float
    gross_profit: float
    gross_loss: float
    profit_factor: float


def ema_cross_backtest(
    df: pd.DataFrame,
    initial_capital: float = 10_000.0,
    fee_bps: float = 5.0,
    slippage_bps: float = 5.0,
) -> BacktestResult:
    """Baseline research backtest with explicit fees/slippage and equity drawdown."""
    if len(df) < 60:
        return BacktestResult(0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    x = df.copy().sort_values("timestamp").reset_index(drop=True)
    x["ema20"] = x.close.ewm(span=20, adjust=False).mean()
    x["ema50"] = x.close.ewm(span=50, adjust=False).mean()
    x["signal"] = (x.ema20 > x.ema50).astype(int)
    x["position_change"] = x.signal.diff().fillna(0).abs()
    x["asset_return"] = x.close.pct_change().fillna(0)

    cost = (fee_bps + slippage_bps) / 10_000.0
    x["strategy_return"] = x.asset_return * x.signal - x.position_change * cost
    equity = initial_capital * (1 + x.strategy_return).cumprod()
    drawdown = equity / equity.cummax() - 1

    # A position change marks a completed trade only when it exits an existing long.
    exits = (x.signal.shift(1).fillna(0) == 1) & (x.signal == 0)
    trade_returns = x.loc[exits, "strategy_return"]
    trades = int(len(trade_returns))
    wins = int((trade_returns > 0).sum())
    losses = trades - wins
    gross_profit = float(trade_returns[trade_returns > 0].sum())
    gross_loss = float(-trade_returns[trade_returns < 0].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else (float("inf") if gross_profit > 0 else 0.0)

    return BacktestResult(
        trades=trades,
        wins=wins,
        losses=losses,
        win_rate_pct=round(100 * wins / trades, 2) if trades else 0.0,
        total_return_pct=round(100 * (equity.iloc[-1] / initial_capital - 1), 2),
        max_drawdown_pct=round(abs(float(drawdown.min())) * 100, 2),
        gross_profit=round(gross_profit, 6),
        gross_loss=round(gross_loss, 6),
        profit_factor=round(profit_factor, 4) if profit_factor != float("inf") else profit_factor,
    )
