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

def ema_cross_backtest(df: pd.DataFrame, initial_capital: float = 10000.0, fee_bps: float = 5.0, slippage_bps: float = 5.0) -> BacktestResult:
    if len(df) < 60:
        return BacktestResult(0, 0, 0, 0.0, 0.0, 0.0)
    x = df.copy().sort_values("timestamp").reset_index(drop=True)
    x["ema20"] = x.close.ewm(span=20, adjust=False).mean()
    x["ema50"] = x.close.ewm(span=50, adjust=False).mean()
    x["signal"] = (x.ema20 > x.ema50).astype(int)
    x["position_change"] = x.signal.diff().fillna(0).abs()
    x["asset_return"] = x.close.pct_change().fillna(0)
    cost = (fee_bps + slippage_bps) / 10000.0
    x["strategy_return"] = x.asset_return * x.signal - x.position_change * cost
    equity = initial_capital * (1 + x.strategy_return).cumprod()
    drawdown = equity / equity.cummax() - 1
    trade_returns = x.loc[x.position_change > 0, "strategy_return"]
    trades = int(len(trade_returns))
    wins = int((trade_returns > 0).sum())
    return BacktestResult(trades, wins, trades - wins, round(100*wins/trades, 2) if trades else 0.0, round(100*(equity.iloc[-1]/initial_capital-1), 2), round(abs(float(drawdown.min()))*100, 2))
