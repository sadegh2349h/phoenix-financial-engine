from dataclasses import dataclass
from typing import Callable
import pandas as pd

@dataclass(frozen=True)
class BacktestResult:
    trades: int
    wins: int
    losses: int
    win_rate_pct: float
    total_return_pct: float
    max_drawdown_pct: float
    profit_factor: float

def run_backtest(df: pd.DataFrame, signal_fn: Callable, fee_rate: float = 0.0004, slippage_rate: float = 0.0002, initial_capital: float = 1.0) -> BacktestResult:
    """Signals are generated on completed bars and applied to the next bar."""
    equity = initial_capital
    peak = equity
    max_dd = 0.0
    wins = losses = trades = 0
    gross_profit = gross_loss = 0.0
    for i in range(max(0, len(df) - 1)):
        signal = int(signal_fn(df.iloc[i], df.iloc[:i + 1]))
        if signal not in (-1, 1):
            continue
        p0, p1 = float(df.iloc[i].close), float(df.iloc[i + 1].close)
        if p0 <= 0:
            continue
        net_return = signal * (p1 / p0 - 1.0) - 2 * (fee_rate + slippage_rate)
        pnl = equity * net_return
        equity += pnl
        trades += 1
        if pnl > 0:
            wins += 1; gross_profit += pnl
        else:
            losses += 1; gross_loss += abs(pnl)
        peak = max(peak, equity)
        max_dd = max(max_dd, (peak - equity) / peak * 100.0)
    return BacktestResult(trades, wins, losses, round(wins / trades * 100, 2) if trades else 0.0, round((equity / initial_capital - 1) * 100, 2), round(max_dd, 2), round(gross_profit / gross_loss, 3) if gross_loss else 0.0)
