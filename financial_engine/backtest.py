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


def ema_cross_backtest(df: pd.DataFrame, initial_capital: float = 10000.0, fee_bps: float = 5.0) -> BacktestResult:
    """Baseline research backtest; not a production strategy recommendation."""
    if len(df) < 60:
        return BacktestResult(0, 0, 0, 0.0, 0.0, 0.0)

    x = df.copy()
    x["ema20"] = x.close.ewm(span=20, adjust=False).mean()
    x["ema50"] = x.close.ewm(span=50, adjust=False).mean()
    x["signal"] = (x.ema20 > x.ema50).astype(int)
    x["position_change"] = x.signal.diff().fillna(0).abs()
    x["asset_return"] = x.close.pct_change().fillna(0)
    x["strategy_return"] = x.asset_return * x.signal - (x.position_change * fee_bps / 10000)

    equity = initial_capital * (1 + x.strategy_return).cumprod()
    running_max = equity.cummax()
    drawdown = equity / running_max - 1

    trades = int((x.position_change > 0).sum())
    positive = x.loc[x.position_change > 0, "strategy_return"]
    wins = int((positive > 0).sum())
    losses = int((positive <= 0).sum())

    return BacktestResult(
        trades=trades,
        wins=wins,
        losses=losses,
        win_rate_pct=round((wins / trades * 100) if trades else 0.0, 2),
        total_return_pct=round((equity.iloc[-1] / initial_capital - 1) * 100, 2),
        max_drawdown_pct=round(abs(float(drawdown.min())) * 100, 2),
    )
