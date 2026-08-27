from __future__ import annotations

import pandas as pd

from .backtest import BacktestResult
from .multifactor import build_features, score_row


def multifactor_backtest(
    df: pd.DataFrame,
    *,
    initial_capital: float = 50_000_000.0,
    fee_bps: float = 5.0,
    slippage_bps: float = 5.0,
    evaluation_start: int = 0,
) -> BacktestResult:
    required = {"timestamp", "close"}
    if not required.issubset(df.columns) or initial_capital <= 0:
        return BacktestResult(0, 0, 0, 0.0, 0.0, 0.0, 0.0, initial_capital)
    x = build_features(df)
    if len(x) <= evaluation_start:
        return BacktestResult(0, 0, 0, 0.0, 0.0, 0.0, 0.0, initial_capital)
    snapshots = [score_row(row) for _, row in x.iterrows()]
    x["signal"] = [s.signal for s in snapshots]
    x["score"] = [s.score for s in snapshots]
    x["asset_return"] = x.close.pct_change().fillna(0.0)
    x["position_change"] = x.signal.diff().abs().fillna(x.signal)
    cost = (fee_bps + slippage_bps) / 10000.0
    x["strategy_return"] = x.asset_return * x.signal - x.position_change * cost
    e = x.iloc[evaluation_start:].copy().reset_index(drop=True)
    equity = initial_capital * (1.0 + e.strategy_return).cumprod()
    dd = equity / equity.cummax() - 1.0
    groups = e.signal.diff().ne(0).cumsum()
    trades = []
    for _, g in e.groupby(groups):
        if int(g.signal.iloc[0]) == 1:
            trades.append(float((1.0 + g.strategy_return).prod() - 1.0))
    wins = sum(t > 0 for t in trades)
    losses = len(trades) - wins
    gross_profit = sum(t for t in trades if t > 0)
    gross_loss = -sum(t for t in trades if t < 0)
    pf = gross_profit / gross_loss if gross_loss else (float("inf") if gross_profit else 0.0)
    final_equity = float(equity.iloc[-1])
    return BacktestResult(
        len(trades), wins, losses,
        round(100.0 * wins / len(trades), 2) if trades else 0.0,
        round(100.0 * (final_equity / initial_capital - 1.0), 2),
        round(abs(float(dd.min())) * 100.0, 2),
        round(pf, 4), round(final_equity, 2),
    )
