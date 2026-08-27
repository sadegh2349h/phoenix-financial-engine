from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phoenix_core.market_data import PublicMarketData
from financial_engine.evaluation import shadow_evaluate


def main() -> None:
    provider = PublicMarketData(timeout=15)
    frame = provider.klines("BTCUSDT", "1d", 1000)
    if len(frame) < 365:
        raise SystemExit(f"insufficient BTC history: {len(frame)} rows")

    rows = []
    for window in (30, 365):
        r = shadow_evaluate(frame, asset="BTCUSDT", window_days=window)
        rows.append({
            "asset": r.asset,
            "window_days": r.window_days,
            "signals": r.strategy.trades,
            "successful_signals": r.strategy.wins,
            "failed_signals": r.strategy.losses,
            "accuracy_pct": r.strategy.win_rate_pct,
            "strategy_return_pct": r.strategy.total_return_pct,
            "benchmark_return_pct": r.buy_and_hold_return_pct,
            "excess_return_pct": r.excess_return_pct,
            "max_drawdown_pct": r.strategy.max_drawdown_pct,
            "profit_factor": r.strategy.profit_factor,
            "final_equity_toman": r.strategy.final_equity,
        })

    payload = {
        "method": "trade_outcome_accuracy",
        "note": "Accuracy is winning completed strategy trades divided by completed strategy trades; it is not a guarantee of future performance.",
        "provider": provider.last_provider,
        "results": rows,
    }
    Path("phoenix_market_evaluation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
