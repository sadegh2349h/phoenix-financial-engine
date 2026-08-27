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
    profit_factor: float
    final_equity: float


def ema_cross_backtest(
    df: pd.DataFrame,
    initial_capital: float = 10_000.0,
    fee_bps: float = 5.0,
    slippage_bps: float = 5.0,
    evaluation_start: int = 0,
) -> BacktestResult:
    required = {"timestamp", "close"}
    if not required.issubset(df.columns) or initial_capital <= 0 or len(df) < 60:
        return BacktestResult(0, 0, 0, 0.0, 0.0, 0.0, 0.0, initial_capital)
    x = df.copy().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    x["close"] = pd.to_numeric(x["close"], errors="coerce")
    x = x.dropna(subset=["close"]).reset_index(drop=True)
    if len(x) < 60 or not 0 <= evaluation_start < len(x):
        return BacktestResult(0, 0, 0, 0.0, 0.0, 0.0, 0.0, initial_capital)

    x["ema20"] = x.close.ewm(span=20, adjust=False).mean()
    x["ema50"] = x.close.ewm(span=50, adjust=False).mean()
    # Shift prevents using the current candle's close to trade that same candle.
    x["signal"] = (x.ema20 > x.ema50).astype(int).shift(1).fillna(0)
    x["asset_return"] = x.close.pct_change().fillna(0.0)
    x["position_change"] = x.signal.diff().abs().fillna(x.signal)
    cost = (fee_bps + slippage_bps) / 10000.0
    x["strategy_return"] = x.asset_return * x.signal - x.position_change * cost

    eval_x = x.iloc[evaluation_start:].copy().reset_index(drop=True)
    equity = initial_capital * (1.0 + eval_x.strategy_return).cumprod()
    dd = equity / equity.cummax() - 1.0

    # Count completed long trades whose entry/exit occurs in the evaluation window.
    trade_id = eval_x.signal.diff().ne(0).cumsum()
    trades = []
    for _, g in eval_x.groupby(trade_id):
        if g.signal.iloc[0] == 1:
            trades.append(float((1.0 + g.strategy_return).prod() - 1.0))
    wins = sum(t > 0 for t in trades)
    losses = sum(t <= 0 for t in trades)
    gross_profit = sum(t for t in trades if t > 0)
    gross_loss = -sum(t for t in trades if t < 0)
    pf = gross_profit / gross_loss if gross_loss else (float("inf") if gross_profit else 0.0)
    final_equity = float(equity.iloc[-1])
    return BacktestResult(
        len(trades), wins, losses,
        round(100 * wins / len(trades), 2) if trades else 0.0,
        round((final_equity / initial_capital - 1) * 100, 2),
        round(abs(float(dd.min())) * 100, 2),
        round(pf, 4), round(final_equity, 2),
    )
