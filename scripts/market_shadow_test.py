from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phoenix_core.market_data import PublicMarketData
from financial_engine.evaluation import shadow_evaluate


def main() -> None:
    provider = PublicMarketData(timeout=15)
    # Request the maximum supported Binance batch.  The evaluator uses the
    # last 30/365 observations when enough history is available. Coinbase's
    # fallback endpoint is limited to 300 candles, so failover must be explicit.
    frame = provider.klines("BTCUSDT", "1d", 1000)
    if len(frame) < 365:
        raise SystemExit(
            f"insufficient BTC history: {len(frame)} rows; "
            "365 daily observations are required for the long-window test"
        )
    for window in (30, 365):
        result = shadow_evaluate(frame, asset="BTCUSDT", window_days=window)
        print({
            "asset": result.asset,
            "window_days": result.window_days,
            "provider": provider.last_provider,
            "strategy_return_pct": result.strategy.total_return_pct,
            "buy_and_hold_return_pct": result.buy_and_hold_return_pct,
            "excess_return_pct": result.excess_return_pct,
            "win_rate_pct": result.strategy.win_rate_pct,
            "max_drawdown_pct": result.strategy.max_drawdown_pct,
            "profit_factor": result.strategy.profit_factor,
            "final_equity_toman": result.strategy.final_equity,
        })


if __name__ == "__main__":
    main()
