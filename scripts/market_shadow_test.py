from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phoenix_core.market_data import PublicMarketData
from financial_engine.evaluation import shadow_evaluate
from financial_engine.performance import score, markdown_report, json_report


def main() -> None:
    provider = PublicMarketData(timeout=15)
    requested = 1000
    frame = provider.klines("BTCUSDT", "1d", requested)
    if len(frame) < 365:
        raise SystemExit(
            f"insufficient BTC history: {len(frame)} rows (requested {requested}; "
            "provider returned less than the required 365-day evaluation history)"
        )

    evaluations = []
    for window in (30, 365):
        result = shadow_evaluate(frame, asset="BTCUSDT", window_days=window)
        evaluations.append({
            "window_days": window,
            "score": score(result.strategy, result.buy_and_hold_return_pct),
        })

    report = markdown_report("BTCUSDT", evaluations)
    print(report)
    (ROOT / "phoenix_performance_report.md").write_text(report + "\n", encoding="utf-8")
    (ROOT / "phoenix_performance_report.json").write_text(
        json_report("BTCUSDT", evaluations) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
